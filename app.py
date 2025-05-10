from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.inspection import permutation_importance
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import io
import base64
import logging
import os
from datetime import datetime
import time
import threading
import webbrowser
import warnings; warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(filename='tmp/app.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)

# Global variables
global_data = None
global_model = None
feature_importance = None
model_accuracy = None
churn_rate = None
is_churn = None
current_revenue = 0

def clean_data(df):
    """Clean and preprocess the input dataframe."""
    try:
        logging.info("Starting data cleaning process")
        
        # Validate dataset
        if df.empty:
            raise ValueError("Uploaded dataset is empty")
        if len(df) < 10:
            raise ValueError("Dataset too small (minimum 10 rows required)")
        
        # Convert categorical columns to lowercase
        df.columns = df.columns.str.lower()
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].str.lower()

        # Handle missing values
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            if df[col].isnull().all():
                raise ValueError(f"Column {col} contains only missing values")
            df[col] = df[col].fillna(df[col].median())
        
        for col in categorical_cols:
            if df[col].isnull().all():
                raise ValueError(f"Column {col} contains only missing values")
            df[col] = df[col].fillna(df[col].mode()[0])
        
        # Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        logging.info(f"Removed {initial_rows - len(df)} duplicates")
        
        # Convert TotalCharges to numeric
        if 'totalcharges' in df.columns:
            df['totalcharges'] = pd.to_numeric(df['totalcharges'], errors='coerce')
            if df['totalcharges'].isnull().all():
                raise ValueError("TotalCharges contains only invalid values")
            df['totalcharges'] = df['totalcharges'].fillna(df['totalcharges'].median())
        
        # Convert MonthlyCharges to numeric
        if 'monthlycharges' in df.columns:
            df['monthlycharges'] = pd.to_numeric(df['monthlycharges'], errors='coerce')
            if df['monthlycharges'].isnull().all():
                raise ValueError("MonthlyCharges contains only invalid values")
            df['monthlycharges'] = df['monthlycharges'].fillna(df['monthlycharges'].median())

        # Validate data types
        if 'tenure' in df.columns:
            df['tenure'] = df['tenure'].astype(float)
        
        if 'monthlycharges' in df.columns:
            df['monthlycharges'] = df['monthlycharges'].astype(float)
        
        # Remove ID columns
        id_columns = [col for col in df.columns if 'id' in col.lower()]
        df = df.drop(columns=id_columns, errors='ignore')
        
        # Calculate data quality score
        missing_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        duplicate_ratio = (initial_rows - len(df)) / initial_rows
        data_quality_score = 100 * (1 - (missing_ratio + duplicate_ratio) / 2)
        
        logging.info("Data cleaning completed successfully")
        return df, data_quality_score
    
    except Exception as e:
        logging.error(f"Error in clean_data: {str(e)}")
        raise

def generate_charts(df):
    """Generate charts for visualization with error handling."""
    try:
        logging.info("Generating charts")
        churn_col = is_churn
        charts = {}

        # Churn Distribution
        plt.figure(figsize=(8, 6))
        churn_counts = df[churn_col].replace({'yes': 1, 'no': 0, True: 1, False: 0}).value_counts()
        labels = ['Retained', 'Churned'] if 0 in churn_counts.index else ['Churned']
        plt.pie(churn_counts, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
        plt.title('Customer Churn Distribution', fontweight='bold')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        charts['churn_distribution'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        # Tenure vs Churn
        if 'tenure' in df.columns and not df['tenure'].isnull().all():
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x='tenure', hue=churn_col, multiple='stack')
            plt.title("Tenure vs Churn", fontweight='bold')
            plt.xlabel("Tenure (Months)", fontweight='bold')
            plt.ylabel("Count", fontweight='bold')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            charts['tenure_vs_churn'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

        # Monthly Charges vs Churn
        if 'monthlycharges' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.kdeplot(data=df, x='monthlycharges', hue=churn_col, fill=True)
            plt.title("Monthly Charges vs Churn", fontweight='bold')
            plt.xlabel("Monthly Charges", fontweight='bold')
            plt.ylabel("Density", fontweight='bold')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            charts['charges_vs_churn'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

        # Contract Type vs Churn
        if 'contract' in df.columns and not df['contract'].isnull().all():
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x='contract', hue=churn_col)
            plt.title("Churn by Contract Type", fontweight='bold')
            plt.xlabel("Contract Type", fontweight='bold')
            plt.ylabel("Count", fontweight='bold')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            charts['contract_vs_churn'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

        # Feature Importance
        if feature_importance is not None:
            plt.figure(figsize=(12, 6))
            importance_df = pd.DataFrame(feature_importance)
            plt.barh(importance_df['Feature'], importance_df['Importance'], color='#4B5EAA')
            plt.xlabel("Feature Importance", fontweight='bold')
            plt.ylabel("Features", fontweight='bold')
            plt.title("Most Important Features for Churn Prediction", fontweight='bold')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            charts['feature_importance'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

        # Churn Rate Over Time
        if 'tenure' in df.columns and 'monthlycharges' in df.columns:
            plt.figure(figsize=(12, 6))
            tenure_bins = pd.cut(df['tenure'], bins=10)
            churn_by_tenure = df.groupby(tenure_bins, observed=True)[churn_col].apply(
                lambda x: x.replace({'yes': 1, 'no': 0, True: 1, False: 0}).mean() * 100
            )
            revenue_loss = df.groupby(tenure_bins, observed=True).apply(
                lambda x: x[churn_col].replace({'yes': 1, 'no': 0, True: 1, False: 0}).sum() * x['monthlycharges'].mean()
            )
            ax1 = plt.gca()
            line1, = ax1.plot(churn_by_tenure.index.astype(str), churn_by_tenure.values, marker='o', color='#D32F2F', label='Churn Rate (%)')
            ax1.set_xlabel("Tenure Range", fontweight='bold')
            ax1.set_ylabel("Churn Rate (%)", fontweight='bold')
            ax1.set_title("Churn Rate and Revenue Loss Over Tenure", fontweight='bold')
            ax2 = ax1.twinx()
            line2, = ax2.plot(revenue_loss.index.astype(str), revenue_loss.values, marker='s', color='#1976D2', label='Revenue Loss (₹)')
            ax2.set_ylabel("Revenue Loss (₹)", fontweight='bold')
            lines = [line1, line2]
            labels = [line.get_label() for line in lines]
            ax1.legend(lines, labels, loc='upper right')
            plt.tight_layout()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            charts['churn_over_time'] = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

        logging.info(f"Generated {len(charts)} charts successfully")
        return charts
    except Exception as e:
        logging.error(f"Error in generate_charts: {str(e)}")
        return {}

def generate_recommendations(feature_importance):
    """Generate actionable recommendations based on feature importance."""
    try:
        logging.info("Generating recommendations")
        recommendations = []
        for feature in feature_importance[:5]:
            feature_name = feature['Feature'].lower()
            if 'contract' in feature_name:
                recommendations.append("Offer longer-term contracts with discounts to boost loyalty.")
            elif 'tenure' in feature_name:
                recommendations.append("Introduce loyalty programs for long-term customers.")
            elif 'monthlycharges' in feature_name:
                recommendations.append("Optimize pricing with competitive or tiered plans.")
            elif 'totalcharges' in feature_name:
                recommendations.append("Provide discounts for high-spending customers.")
            else:
                recommendations.append(f"Optimize {feature_name} based on customer feedback.")
        recommendations.extend([
            "Engage at-risk customers with personalized offers.",
            "Streamline onboarding to highlight product value."
        ])
        return recommendations
    except Exception as e:
        logging.error(f"Error in generate_recommendations: {str(e)}")
        return []

def generate_pdf_report(data_info, insights, charts, recommendations, data_quality_score, revenue_message):
    """Generate a formatted PDF report."""
    try:
        logging.info("Generating PDF report")
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph("Customer Churn Analysis Report", styles['Title']))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Dataset Overview
        story.append(Paragraph("Dataset Overview", styles['Heading2']))
        story.append(Paragraph(f"Total Customers: {data_info['rows']}", styles['Normal']))
        story.append(Paragraph(f"Columns: {data_info['columns']}", styles['Normal']))
        story.append(Paragraph(f"Missing Values: {data_info['missing_values']}", styles['Normal']))
        story.append(Paragraph(f"Data Quality Score: {data_quality_score:.2f}%", styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Churn Statistics
        story.append(Paragraph("Churn Statistics", styles['Heading2']))
        story.append(Paragraph(f"Churn Rate: {insights['churn_rate']*100:.2f}%", styles['Normal']))
        story.append(Paragraph(f"Model Accuracy: {insights['model_accuracy']*100:.2f}%", styles['Normal']))
        if insights['potential_monthly_loss'] is not None and insights['potential_monthly_loss'] > 0:
            story.append(Paragraph(f"Monthly Revenue at Risk: ₹{insights['potential_monthly_loss']:.2f}", styles['Normal']))
            story.append(Paragraph(f"Annual Revenue at Risk: ₹{insights['potential_yearly_loss']:.2f}", styles['Normal']))
        else:
            story.append(Paragraph(revenue_message, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Charts
        story.append(Paragraph("Graphical Analysis", styles['Heading2']))
        for chart_name, chart_data in charts.items():
            img_buffer = io.BytesIO(base64.b64decode(chart_data))
            img = Image(img_buffer, width=5*inch, height=3*inch)
            story.append(img)
            story.append(Paragraph(chart_name.replace('_', ' ').title(), styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        # Recommendations
        story.append(Paragraph("Recommendations", styles['Heading2']))
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        logging.error(f"Error in generate_pdf_report: {str(e)}")
        raise

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and analysis."""
    global global_data, global_model, feature_importance, model_accuracy, churn_rate, is_churn, current_revenue
    
    try:
        logging.info("Processing file upload")
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'})
        
        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'Invalid file format'})
        
        # Get current_revenue from FormData
        current_revenue = request.form.get('current_revenue', 0)
        try:
            current_revenue = float(current_revenue)
            if current_revenue < 0:
                current_revenue = 0
        except (ValueError, TypeError):
            current_revenue = 0
        
        df = pd.read_csv(file)
        df, data_quality_score = clean_data(df)
        global_data = df

        # Find Churn column (case-insensitive)
        churn_cols = [col for col in df.columns if col.lower() == 'churn']
        if not churn_cols:
            return jsonify({
                'success': False,
                'data_info': {
                    'rows': int(len(df)),
                    'columns': int(len(df.columns)),
                    'missing_values': int(df.isnull().sum().sum()),
                    'column_names': df.columns.tolist() + ['All'],
                    'data_quality_score': float(data_quality_score)
                },
                'warning': 'No Churn column found.'
            })
        is_churn = churn_cols[0]

        data_info = {
            'rows': int(len(df)),
            'columns': int(len(df.columns)),
            'missing_values': int(df.isnull().sum().sum()),
            'column_names': df.columns.tolist() + ['All'],
            'data_quality_score': float(data_quality_score)
        }

        # Calculate churn rate
        churn_values = df[is_churn].replace({'yes': 1, 'no': 0, True: 1, False: 0})
        if churn_values.isna().all():
            return jsonify({'success': False, 'error': 'Churn column contains invalid values'})
        churn_rate = float(churn_values.mean())
        logging.info(f"Churn rate: {churn_rate*100:.2f}%")

        # Prepare data for model
        df_model = df.copy()
        le = LabelEncoder()
        for col in df_model.select_dtypes(include=['object']).columns:
            df_model[col] = le.fit_transform(df_model[col])
        
        X = df_model.drop(is_churn, axis=1)
        y = df_model[is_churn].replace({'yes': 1, 'no': 0, True: 1, False: 0})
        
        if X.empty or len(X.columns) < 1:
            return jsonify({'success': False, 'error': 'No valid features for model training'})

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        if len(X_train) < 5 or len(X_test) < 2:
            return jsonify({'success': False, 'error': 'Dataset too small for model training'})
        
        # Train Random Forest with GridSearchCV
        rf = RandomForestClassifier(random_state=42)
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5]
        }
        grid_search = GridSearchCV(rf, param_grid, cv=5, n_jobs=-1)
        grid_search.fit(X_train, y_train)
        global_model = grid_search.best_estimator_
        logging.info(f"Best RF params: {grid_search.best_params_}")
        
        y_pred = global_model.predict(X_test)
        model_accuracy = float(accuracy_score(y_test, y_pred))
        logging.info(f"Model accuracy: {model_accuracy*100:.2f}%")
        
        # Feature importance using permutation importance
        perm_importance = permutation_importance(global_model, X_test, y_test, n_repeats=10, random_state=42)
        importance_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': perm_importance.importances_mean
        })
        importance_df = importance_df.sort_values(by='Importance', ascending=False)
        feature_importance = importance_df.to_dict(orient='records')
        logging.info(f"Feature importance: {feature_importance[:5]}")

        # Revenue loss based on current_revenue
        monthly_loss = float(current_revenue * churn_rate) if current_revenue > 0 else 0
        yearly_loss = float(monthly_loss * 12) if current_revenue > 0 else 0
        revenue_message = "Current Revenue is 0, no revenue loss predicted" if current_revenue == 0 else ""

        insights = {
            'churn_rate': float(churn_rate),
            'model_accuracy': float(model_accuracy),
            'potential_monthly_loss': monthly_loss,
            'potential_yearly_loss': yearly_loss,
            'feature_importance': [
                {'Feature': item['Feature'], 'Importance': float(item['Importance'])}
                for item in feature_importance[:5]
            ]
        }

        charts = generate_charts(df)
        if not charts:
            logging.warning("No charts generated")
        
        response = {
            'success': True,
            'data_info': data_info,
            'insights': insights,
            'charts': charts
        }
        if revenue_message:
            response['revenue_message'] = revenue_message

        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in upload: {str(e)}")
        return jsonify({'success': False, 'error': f'Analysis failed: {str(e)}'})

@app.route('/filter_by_date', methods=['POST'])
def filter_by_date():
    """Filter data by month and year."""
    global global_data, global_model, feature_importance, model_accuracy, churn_rate, current_revenue
    
    try:
        logging.info("Processing date filter")
        data = request.json
        month = data.get('month')
        year = data.get('year')

        if not month or not year:
            return jsonify({'success': False, 'error': 'Missing month or year'})

        # Assume SignupDate column
        df = global_data.copy()
        if 'signupdate' not in df.columns:
            return jsonify({'success': False, 'error': 'SignupDate column not found or invalid'})
        
        df['signupdate'] = pd.to_datetime(df['signupdate'], errors='coerce')
        if df['signupdate'].isna().all():
            return jsonify({'success': False, 'error': 'Invalid SignupDate values'})
        
        df = df[(df['signupdate'].dt.month == int(month)) & (df['signupdate'].dt.year == int(year))]
        if df.empty:
            return jsonify({'success': False, 'error': 'No data for selected date range'})

        global_data = df
        data_info = {
            'rows': int(len(df)),
            'columns': int(len(df.columns)),
            'missing_values': int(df.isnull().sum().sum()),
            'column_names': df.columns.tolist() + ['All'],
            'data_quality_score': float(clean_data(df.copy())[1])
        }

        churn_rate = float(df[is_churn].replace({'yes': 1, 'no': 0, True: 1, False: 0}).mean())
        df_model = df.copy()
        le = LabelEncoder()
        for col in df_model.select_dtypes(include=['object']).columns:
            df_model[col] = le.fit_transform(df_model[col])

        X = df_model.drop(is_churn, axis=1)
        y = df_model[is_churn].replace({'yes': 1, 'no': 0, True: 1, False: 0})

        if X.empty or len(X.columns) < 1:
            return jsonify({'success': False, 'error': 'No valid features for model training'})

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(rf, param_grid={'n_estimators': [100, 200], 'max_depth': [10, 20, None]}, cv=5)
        grid_search.fit(X_train, y_train)
        global_model = grid_search.best_estimator_

        y_pred = global_model.predict(X_test)
        model_accuracy = float(accuracy_score(y_test, y_pred))

        perm_importance = permutation_importance(global_model, X_test, y_test, n_repeats=10, random_state=42)
        importance_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': perm_importance.importances_mean
        })
        importance_df = importance_df.sort_values(by='Importance', ascending=False)
        feature_importance = importance_df.to_dict(orient='records')

        # Use stored current_revenue from last upload (not ideal, but aligns with script.js)
        current_revenue = float(request.form.get('current_revenue', 0)) if request.form.get('current_revenue') else 0
        monthly_loss = float(current_revenue * churn_rate) if current_revenue > 0 else 0
        yearly_loss = float(monthly_loss * 12) if current_revenue > 0 else 0
        revenue_message = "Current Revenue is 0, no revenue loss predicted" if current_revenue == 0 else ""

        insights = {
            'churn_rate': float(churn_rate),
            'model_accuracy': float(model_accuracy),
            'potential_monthly_loss': monthly_loss,
            'potential_yearly_loss': yearly_loss,
            'feature_importance': [
                {'Feature': item['Feature'], 'Importance': float(item['Importance'])}
                for item in feature_importance[:5]
            ]
        }

        charts = generate_charts(df)
        response = {
            'success': True,
            'data_info': data_info,
            'insights': insights,
            'charts': charts
        }
        if revenue_message:
            response['revenue_message'] = revenue_message

        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in filter_by_date: {str(e)}")
        return jsonify({'success': False, 'error': f'Filter failed: {str(e)}'})

@app.route('/predict_revenue', methods=['POST'])
def predict_revenue():
    """Predict future revenue based on current revenue and churn rate."""

    global current_revenue
    try:
        logging.info("Predicting revenue")
        data = request.json
        current_revenue = data.get('current_revenue', 0)
        try:
            current_revenue = float(current_revenue)
            if current_revenue < 0:
                current_revenue = 0
        except (ValueError, TypeError):
            current_revenue = 0
        
        if current_revenue == 0:
            return jsonify({
                'success': True,
                'monthly_loss': 0.0,
                'yearly_loss': 0.0,
                'future_revenue': 0.0,
                'message': 'Current Revenue is 0, no loss predicted'
            })
        
        monthly_loss = float(current_revenue * churn_rate)
        yearly_loss = float(monthly_loss * 12)
        future_revenue = float(current_revenue - yearly_loss)
        
        logging.info(f"Revenue prediction: Monthly loss ₹{monthly_loss:.2f}, Yearly loss ₹{yearly_loss:.2f}")
        return jsonify({
            'success': True,
            'monthly_loss': monthly_loss,
            'yearly_loss': yearly_loss,
            'future_revenue': future_revenue
        })
    except Exception as e:
        logging.error(f"Error in predict_revenue: {str(e)}")
        return jsonify({'success': False, 'error': f'Revenue prediction failed: {str(e)}'})

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot queries."""
    try:
        logging.info("Processing chat request")
        if global_data is None:
            return jsonify({'response': 'Please upload a dataset first.'})

        data = request.json
        query = data.get('query', '').lower()
        
        # Get current_revenue from JSON
        current_revenue = data.get('current_revenue', 0)
        logging.info(f"Received current_revenue: {current_revenue}") # Debug log
        try:
            current_revenue = float(current_revenue)
            if current_revenue < 0:
                current_revenue = 0
        except (ValueError, TypeError):
            current_revenue = 0
        
        if 'churn rate' in query:
            response = f"The current churn rate is {churn_rate*100:.2f}%."
        elif 'revenue' in query or 'loss' in query:
            if current_revenue == 0:
                response = "Current Revenue is 0, no revenue loss predicted."
            else:
                monthly_loss = float(current_revenue * churn_rate)
                yearly_loss = float(monthly_loss * 12)
                response = f"Churn impacts revenue by ₹{monthly_loss:.2f} monthly and ₹{yearly_loss:.2f} annually."
        elif 'reasons' in query or 'factors' in query:
            response = "Top 3 factors for churn:\n" + "\n".join(
                f"{i+1}. {f['Feature']} (Importance: {f['Importance']:.4f})" for i, f in enumerate(feature_importance[:3])
            )
        elif 'reduce churn' in query or 'recommendations' in query:
            recommendations = generate_recommendations(feature_importance)
            response = "Recommendations to reduce churn:\n" + "\n".join(f"{i+1}. {rec}" for i, rec in enumerate(recommendations))
        elif 'model accuracy' in query or 'accuracy' in query or 'accurate' in query:
            response = f"The churn prediction model accuracy is {model_accuracy*100:.2f}%."
        elif 'trend' in query:
            response = f"Churn rate trend: {churn_rate*100:.2f}% currently, analyze over time in the Insights section."
        elif 'segment' in query:
            if 'contract' in global_data.columns:
                segment_churn = global_data.groupby('contract')[is_churn].mean().to_dict()
                response = "Churn by contract type:\n" + "\n".join(
                    f"{k}: {v*100:.2f}%" for k, v in segment_churn.items()
                )
            else:
                response = "Segment analysis unavailable due to missing contract data."
        else:
            response = "Try asking about churn rate, revenue impact, churn reasons, recommendations, model accuracy, churn trend, or customer segments."

        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error in chat: {str(e)}")
        return jsonify({'response': f'Error: {str(e)}'})

@app.route('/download_report', methods=['GET'])
def download_report():
    """Download a PDF report."""
    try:
        logging.info("Generating PDF report")
        if global_data is None:
            return jsonify({'error': 'No data uploaded yet'})
        
        current_revenue = float(request.form.get('current_revenue', 0)) if request.form.get('current_revenue') else 0
        data_info = {
            'rows': int(len(global_data)),
            'columns': int(len(global_data.columns)),
            'missing_values': int(global_data.isnull().sum().sum()),
            'data_quality_score': float(clean_data(global_data.copy())[1])
        }
        monthly_loss = float(current_revenue * churn_rate) if current_revenue > 0 else 0
        yearly_loss = float(monthly_loss * 12) if current_revenue > 0 else 0
        revenue_message = "Current Revenue is 0, no revenue loss predicted" if current_revenue == 0 else ""
        insights = {
            'churn_rate': float(churn_rate),
            'model_accuracy': float(model_accuracy),
            'potential_monthly_loss': monthly_loss,
            'potential_yearly_loss': yearly_loss
        }
        charts = generate_charts(global_data)
        recommendations = generate_recommendations(feature_importance)
        
        pdf_buffer = generate_pdf_report(data_info, insights, charts, recommendations, data_info['data_quality_score'], revenue_message)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'churn_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except Exception as e:
        logging.error(f"Error in download_report: {str(e)}")
        return jsonify({'error': f'Error generating report: {str(e)}'})

def open_browser():
    time.sleep(1)
    webbrowser.open_new("http://localhost:5000")
    os.system("echo(")
    os.system("echo The webpage has opened successfully.")
    os.system("echo(")
    os.system("echo Press Ctrl+C to close the server.")
    os.system("echo(")
    os.system("echo For more details visit the following files: ")
    os.system("echo # '%CD%\\tmp\\app_output.txt' for console outputs.")
    os.system("echo # '%CD%\\tmp\\app.log' for detailed logs.")
    os.system("echo(")

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=False)
