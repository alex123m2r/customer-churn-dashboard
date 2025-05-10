# Customer Churn Dashboard 📊

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-awesome-orange.svg)

Welcome to the **Customer Churn Dashboard**, your one-stop shop for slicing, dicing, and conquering customer churn! 🎉 Built with Flask, this sleek web app lets you upload CSV datasets, predict churn, simulate retention strategies, and chat with a snarky AI assistant who’s *almost* as smart as you. Whether you’re a data nerd or a business guru, this dashboard will help you keep those customers from ghosting you. Ready to dive in? Let’s make churn a thing of the past! 🚀

## What’s This All About? 🤔

Ever wonder why customers are ditching your business faster than a bad date? This dashboard uses machine learning (fancy, right?) to analyze churn patterns, predict revenue losses, and suggest ways to keep customers hooked. Upload your data, sip some coffee, and let the Random Forest model and interactive charts do the heavy lifting. Plus, there’s a chatbot that’s ready to answer your burning churn questions—because who doesn’t love a sassy AI sidekick? 😎

## Features That’ll Blow Your Mind 💥

- 📤 **Upload Multiple Datasets**: Throw in any of the five sample CSVs (`Sample_dataset1.csv` to `Sample_dataset5.csv`) or your own. No judgment if your data’s a mess—we’ll clean it up!
- 🤖 **Churn Assistant Chatbot**: Ask about churn rates, revenue impacts, or retention tips. It’s like having a data scientist in your pocket, minus the coffee stains.
- 📉 **Interactive Charts**: Visualize churn distribution, tenure, charges, and more with pretty graphs that even your boss will understand.
- 🛠️ **Retention Strategy Simulator**: Play “what if” with churn reduction percentages and see how much revenue you could save. Spoiler: It’s a lot!
- 🗂️ **Customer Segmentation**: Discover which contract types are churn magnets (looking at you, month-to-month plans).
- 📅 **Date Filtering**: Zero in on specific signup months/years to spot trends. Requires a `SignupDate` column, because time travel isn’t *that* easy.
- 📄 **PDF Reports**: Download a polished report with all your insights, perfect for impressing stakeholders or framing on your wall.
- 🌟 **Slick UI**: Dark theme, animations, and a responsive design that looks good on your laptop or your phone during a lunch break.

## Folder Structure 📂

Here’s how we’ve organized the chaos (you’re welcome):

```
customer-churn-dashboard/
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   └── favicon.ico
│   │   └── favicon.png
│   ├── js/
│   │   └── script.js
├── templates/
│   └── index.html
├── tmp/
│   └── app.log
├── CONTRIBUTING.md
├── LICENSE.txt
├── README.md
├── Sample_dataset1.csv
├── Sample_dataset2.csv
├── Sample_dataset3.csv
├── Sample_dataset4.csv
├── Sample_dataset5.csv
├── app.py
├── folder_structure.txt
├── requirements.txt
├── venv_creator.bat
├── webpage_server_host_runner.bat
```

- **static/**: CSS, JavaScript, and favicon files to make the dashboard pretty.
- **templates/**: HTML template for the dashboard’s frontend.
- **app.py**: The Flask backend that does all the number-crunching.
- **Sample_dataset*.csv**: Five sample datasets to get you started.
- **venv_creator.bat**: Sets up your virtual environment (because we’re not savages).
- **webpage_server_host_runner.bat**: Launches the server and opens your browser.
- **app.log**: Logs errors and debug info, because even apps need a diary.
- **requirements.txt**: Lists Python dependencies, so you don’t have to guess.

## Prerequisites ⚙️

Before you embark on this churn-busting adventure, make sure you have:

- 🐍 **Python 3.8+**: Download it from [python.org](https://www.python.org/downloads/). No Python, no party.
- 📡 **Internet Connection**: For installing dependencies and fetching CDNs (Bootstrap, jQuery, etc.).
- 🖥️ **Windows**: The batch files (`venv_creator.bat`, `webpage_server_host_runner.bat`) are Windows-specific. Linux/Mac users, you’ll need to translate to shell scripts (PRs welcome!).
- 🧠 **A Bit of Patience**: If you skip steps, don’t blame us when errors start throwing shade.

## Setup Instructions 🛠️

Follow these steps to get the dashboard up and running. Don’t skip the virtual environment step, unless you love error messages. 😏

1. **Clone the Repository** 📥
   ```bash
   git clone https://github.com/Vezz-z/customer-churn-dashboard.git
   cd customer-churn-dashboard
   ```

2. **Create the Virtual Environment** 🏗️
   - Run the magical `venv_creator.bat`:
     ```bash
     .\venv_creator.bat
     ```
   - **What it does**:
     - Checks for Python.
     - Creates a `venv/` folder if it doesn’t exist.
     - If `venv/` exists, choose to delete it or install packages.
     - Installs dependencies from `requirements.txt`.
   - **Pro Tip**: Say “y” when asked to install packages, or the app might throw a tantrum.

3. **Run the Server** 🚀
   - Fire up the server with:
     ```bash
     .\webpage_server_host_runner.bat
     ```
   - **What happens**:
     - Activates the virtual environment.
     - Starts `app.py`.
     - Opens your browser to `http://localhost:5000`.
     - Logs output to `%TEMP%\app_output.txt` and `app.log`.
   - **Note**: If you see “Virtual environment not found,” rerun `venv_creator.bat` first. Reading is hard, we know.

4. **Explore the Dashboard** 🌐
   - Your browser should pop open to the dashboard. If not, visit `http://localhost:5000`.
   - Stop the server with `Ctrl+C` when you’re done being amazed.

## Usage Guide 📖

Here’s how to wield this dashboard like a churn-slaying superhero:

1. **Upload a Dataset** 📤
   - Go to the “Upload Customer Data” section.
   - Select a CSV file (e.g., `Sample_dataset1.csv`) or your own.
   - Enter your **Current Monthly Revenue** (in ₹). *Pro Tip*: Don’t leave it blank, or you’ll get the dreaded “Revenue is 0” message. 🙄
   - Click “Analyze” and watch the magic happen.

2. **Explore Insights** 📊
   - **Dataset Summary**: Check total customers, attributes, missing values, and data quality.
   - **Charts**: Dive into churn distribution, tenure vs. churn, and more. Scroll through the “Insights” section.
   - **Key Metrics**: See churn rate, model accuracy, and revenue at risk.

3. **Filter by Date** 📅
   - Use the “Date Range Analysis” section to filter by signup month/year (requires `SignupDate` in your dataset).
   - Click “Apply” to refresh insights for the selected period.

4. **Chat with the Churn Assistant** 🤖
   - Click “Churn Assistant” or use the floating robot icon.
   - Try quick questions like “What is the current churn rate?” or type your own.
   - The bot’s got answers on churn rates, revenue, and recommendations. Don’t ask it for dating advice, though.

5. **Simulate Retention Strategies** 🛠️
   - In the “Retention Strategy Simulator,” enter a churn reduction percentage (0–100).
   - See how much revenue you could save. Dream big!

6. **Check Customer Segments** 🗂️
   - The “Customer Segmentation” section shows churn by contract type (if `contract` is in your dataset).
   - Ask the chatbot “Which customer segment has the highest churn?” for details.

7. **Download a Report** 📄
   - Hit “Download PDF Report” to get a professional PDF with all your insights.
   - Perfect for meetings or showing off your data prowess.

## Dataset Requirements 📋

Your CSV needs to play nice with the dashboard. Here’s the deal:

- **Mandatory Columns**:
  - `churn`: Indicates churn status (`True`/`False`, `yes`/`no`, case-insensitive).
  - `totalCharges`: Numeric, total customer charges.
- **Optional Columns**:
  - `id`: Customer ID (ignored during analysis).
  - `tenure`: Numeric, months with the company.
  - `monthlycharges`: Numeric, monthly charges.
  - `contract`: Categorical (e.g., “month-to-month,” “one year”).
  - `SignupDate`: Date format (e.g., `YYYY-MM-DD`) for date filtering.
- **Sample Datasets**:
  - Use `Sample_dataset1.csv` to `Sample_dataset5.csv` for testing. They’re ready to roll!
- **Tips**:
  - Ensure `churn` is present, or you’ll get a polite error.
  - Missing values? We’ll handle them, but cleaner data = happier dashboard.

## Troubleshooting 😵

Running into issues? Don’t panic—here’s how to fix the usual suspects:

- **“Virtual environment not found”**:
  - Run `venv_creator.bat` first. It’s not optional, folks.
- **“Current Revenue is 0”**:
  - Enter a valid number in the “Current Monthly Revenue” field. Zero or blank inputs make the dashboard sad. 😢
  - Check `app.log` for clues if it persists.
- **Server won’t start**:
  - Verify Python is in your PATH (`python --version`).
  - Check `%TEMP%\app_output.txt` and `app.log` for errors.
  - Rerun `venv_creator.bat` to reinstall dependencies.
- **Charts missing**:
  - Ensure your dataset has `tenure`, `monthlycharges`, or `contract` for relevant charts.
  - Check browser console (`F12`) for errors.
- **Date filter fails**:
  - Your dataset needs a `SignupDate` column. Add it or skip filtering.
- **Still stuck?**:
  - Email [mohammedparvezofficial@gmail.com](mailto:mohammedparvezofficial@gmail.com) or open an issue on GitHub. We don’t bite.

## Contributing 🤝

Love this project and want to make it even better? We welcome contributions! Here’s how:

1. Fork the repo and clone it:
   ```bash
   git clone https://github.com/Vezz-z/customer-churn-dashboard.git
   ```
2. Create a branch:
   ```bash
   git checkout -b feature/amazing-stuff
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Added amazing stuff"
   ```
4. Push and open a pull request:
   ```bash
   git push origin feature/amazing-stuff
   ```
5. Follow our [Contributing Guidelines](CONTRIBUTING.md).

Ideas: Add new charts, improve the chatbot’s wit, or make the batch files cross-platform. Go wild! 🌈

## Contributors ✒️

Meet the brilliant minds who turned this churn dashboard into a masterpiece! 🧠 These folks wrestled data, tamed algorithms, and made the UI so pretty you’ll want to frame it. Give them a follow—they’re basically the Avengers of churn analysis. 😎

| **Name** | **Role** | **What we do** | **GitHub** | **Email** |
|----------|----------|-------------|------------|-----------|
| Mohammed Parvez Y | Project Lead, Model Development, Algorithm Selection & Training | Leading the charge and making algorithms behave since day one. Bow to the churn master! 👑 | [Vezz-z](https://github.com/Vezz-z) | [mohammedparvezofficial@gmail.com](mailto:mohammedparvezofficial@gmail.com) |
| Vignesh R | Data Collection, Data Cleaning, Feature Engineering | Tames wild datasets like a data whisperer. Messy CSVs? Not on his watch! 🧹 | [Vigneshravi2004](https://github.com/Vigneshravi2004) | [vigneshravi0723@gmail.com](mailto:vigneshravi0723@gmail.com) |
| Sanjula S | Model Building, Model Evaluation, UI Design | Builds models and UIs so sleek, you’ll forget Excel exists. Multitasking queen! 💃 | [sanjula-2005](https://github.com/sanjula-2005) | [sanjuselvaraaj@gmail.com](mailto:sanjuselvaraaj@gmail.com) |
| Metilda Evelin Angel S | Data Analytics, Predictions, Model Training | Crunches numbers and predicts churn like a fortune teller with a PhD. 🔮 | [Metilda-18](https://github.com/Metilda-18) | [metilda1804@gmail.com](mailto:metilda1804@gmail.com) |
| Dharani G | Deployment, Interface Creation, Feature Engineering | Deploys apps and crafts interfaces so smooth, you’ll think it’s magic. 🪄 | [dharaniGaneshram](https://github.com/dharaniGaneshram) | [dharaniganeshram5@gmail.com](mailto:dharaniganeshram5@gmail.com) |

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. Basically, use it, tweak it, share it—just give us a shout-out. 😊

## Contact Us 📬

Got questions, feedback, or just want to say hi? Reach out:
- **Email**: [mohammedparvezofficial@gmail.com](mailto:mohammedparvezofficial@gmail.com)
- **GitHub**: [Vezz-z/customer-churn-dashboard](https://github.com/Vezz-z/customer-churn-dashboard)

## Acknowledgments 🙌

A big thank you to:
- **Flask** for powering the backend.
- **Bootstrap** for the snazzy UI.
- **Scikit-learn** for making ML less painful.
- **You**, for using this dashboard to fight churn like a boss.

Now go forth and keep those customers happy! 💪 If you love this project, give it a ⭐ on GitHub—it’s like a virtual high-five.

---
*Built with 💖 by Vezzz and team. Last updated: May 2025.*