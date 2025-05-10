# Contributing to Customer Churn Dashboard 🤝

Welcome to the churn-fighting squad! 🎉 Thanks for considering a contribution to the **Customer Churn Dashboard**, the slickest tool for keeping customers from ghosting your business. Whether you’re fixing a pesky bug, adding a shiny new chart, or making our chatbot sassier, we’re thrilled to have you on board. Ready to make churn cry? Let’s dive in! 💻

## Why Contribute? 🌟

Because you’re awesome, and this project deserves your brilliance! By contributing, you’ll:
- Help businesses save millions by outsmarting churn. 💰
- Flex your coding skills on a real-world Flask app. 🐍
- Join a crew of data nerds who think churn is the ultimate villain. 😈
- Get a shout-out in our [Contributors section](README.md#contributors-✒️) (fame, baby!).

No contribution is too small—whether it’s a typo fix or a new ML model, we want your magic. ✨

## How Can You Contribute? 🛠️

Not sure where to start? Here are some ways to make your mark:

- 🐛 **Report Bugs**: Found something broken? Tell us before it ruins someone’s day.
- 💡 **Suggest Features**: Got a wild idea for a new chart or chatbot quip? We’re listening.
- 💻 **Submit Code**: Fix bugs, add features, or refactor our code to be less... chaotic.
- 📝 **Improve Docs**: Make our `README.md` or code comments clearer than a sunny day.
- 🎨 **Enhance UI**: Got CSS skills? Make our dashboard even prettier.

## Setting Up Your Environment ⚙️

Before you start coding, let’s get your machine ready. Follow these steps, and don’t skip the virtual environment part unless you *love* error messages. 😏

1. **Clone the Repo** 📥
   ```bash
   git clone https://github.com/Vezz-z/customer-churn-dashboard.git
   cd customer-churn-dashboard
   ```

2. **Set Up the Virtual Environment** 🏗️
   - Run our fancy batch file (Windows only, sorry Linux/Mac folks):
     ```bash
     .\venv_creator.bat
     ```
   - Choose `y` to install dependencies from `requirements.txt`. If `venv/` exists, pick `b` to update packages or `a` to nuke it and start fresh.
   - **Linux/Mac?** Create a virtual environment manually:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

3. **Test the App** 🚀
   - Launch the server:
     ```bash
     .\webpage_server_host_runner.bat
     ```
     Or, for Linux/Mac:
     ```bash
     source venv/bin/activate
     python app.py
     ```
   - Visit `http://localhost:5000` in your browser. If it doesn’t open, check `app.log` or `%TEMP%\app_output.txt` for clues.

4. **Verify It Works** ✅
   - Upload a sample dataset (`Sample_dataset1.csv`) and play with the dashboard. If charts load and the chatbot sasses you back, you’re golden!

## Code Contribution Steps 💾

Ready to write some code? Follow these steps to avoid breaking everything (no pressure). 😜

1. **Fork the Repo** 🍴
   - Click the “Fork” button on [Vezz-z/customer-churn-dashboard](https://github.com/Vezz-z/customer-churn-dashboard).
   - Clone your fork:
     ```bash
     git clone https://github.com/Vezz-z/customer-churn-dashboard.git
     ```

2. **Create a Branch** 🌿
   - Name it something descriptive, like `feature/cool-chart` or `bugfix/churn-rate`:
     ```bash
     git checkout -b feature/cool-chart
     ```

3. **Make Your Changes** ✍️
   - Fix bugs, add features, or refactor. Check the [Code Style Guidelines](#code-style-guidelines) to keep things tidy.
   - Test locally with `webpage_server_host_runner.bat` or `python app.py`.
   - Update `README.md` or add comments if your changes affect usage.

4. **Commit Your Changes** 📌
   - Write clear commit messages:
     ```bash
     git commit -m "Add super cool churn prediction chart"
     ```
   - Keep commits focused (e.g., one for code, one for docs).

5. **Push to Your Fork** 📤
   ```bash
   git push origin feature/cool-chart
   ```

6. **Open a Pull Request** 📬
   - Go to the original repo: [Vezz-z/customer-churn-dashboard](https://github.com/Vezz-z/customer-churn-dashboard).
   - Click “New Pull Request” and select your branch.
   - Fill out the PR template (if we have one) or describe:
     - What you changed and why.
     - How you tested it.
     - Any issues it fixes (e.g., “Fixes #42”).
   - Submit and wait for our review. We’re nice, promise! 😊

## Code Style Guidelines 📏

Let’s keep this codebase cleaner than a freshly uploaded CSV! 🧹 Follow these rules to make your code sparkle and avoid a lecture from our sassy chatbot. 😈 We want contributions that fit seamlessly into our churn-fighting masterpiece, so stick to these guidelines for Python, JavaScript, HTML/CSS, and general awesomeness. Your code’s gonna shine brighter than our dashboard’s dark theme! 🌟

### Python (app.py) 🐍
Our Flask backend is the brain of the operation, so keep it sharp and PEP 8-compliant. No one wants to debug a mess that looks like it was written by a caffeinated squirrel.

- **Follow PEP 8**: Stick to [PEP 8](https://www.python.org/dev/peps/pep-0008/) like it’s your life’s mission. Run `pylint` or `flake8` if you’re feeling fancy.
- **Indentation**: Use 4 spaces. Tabs? We don’t speak that language.
- **Line Length**: Keep lines under 88 characters (Black’s default). Wrap long lines like a pro.
- **Docstrings**: Every function needs a docstring. Make it clear, not a novel.
  ```python
  def clean_data(df):
      """Cleans the dataframe like a data janitor. Returns a shiny dataset."""
      pass
  ```
- **Variable Names**: Be descriptive. Use `churn_rate`, not `cr`. Snake_case for variables, CamelCase for classes.
- **Imports**: Group imports: standard library, third-party, then local. One per line.
  ```python
  import os
  import pandas as pd
  from flask import Flask
  ```
- **Error Handling**: Catch specific exceptions, not a vague `except:`. Log errors to `app.log`.
  ```python
  try:
      df = pd.read_csv(file)
  except FileNotFoundError:
      logging.error("CSV file went AWOL!")
  ```
- **Functions**: Keep them short (under 30 lines if possible). One function, one job.
- **Comments**: Explain *why*, not *what*. Use `#` sparingly.
  ```python
  # Calculate churn rate because stakeholders love percentages
  churn_rate = df["churn"].mean()
  ```

### JavaScript (script.js) 💻
Our frontend JS handles the dashboard’s magic, from AJAX calls to chatbot sass. Keep it tidy, or we’ll make you debug jQuery in the dark.

- **CamelCase**: Functions and variables use camelCase (e.g., `sendChatMessage`, `currentRevenue`).
- **Indentation**: 2 spaces. No tabs, unless you want a stern talking-to.
- **Line Length**: Aim for 80 characters. Break long lines for readability.
- **Comments**: Use `//` for single lines, `/* */` for blocks. Explain complex logic.
  ```javascript
  // Don’t ask why this AJAX call works, just trust me
  $.ajax({ ... });
  ```
- **Functions**: Keep them focused (under 20 lines). Use arrow functions for callbacks.
  ```javascript
  const updateCharts = () => {
      // Update those fancy charts
  };
  ```
- **Async/Await**: Prefer `async/await` over `.then()` for AJAX calls.
  ```javascript
  async function fetchData() {
      try {
          const response = await $.ajax({ ... });
          return response;
      } catch (error) {
          console.error("AJAX call took a nap:", error);
      }
  }
  ```
- **jQuery**: Stick to jQuery for DOM manipulation (it’s in `script.js`). Avoid vanilla JS unless necessary.
- **Error Handling**: Catch errors and show user-friendly alerts.
  ```javascript
  $.ajax({
      error: () => alert("Oops, the server’s throwing a tantrum!")
  });
  ```

### HTML/CSS (index.html, styles.css) 🎨
Our dashboard’s UI is prettier than a churn-free revenue report, so keep the HTML and CSS clean and accessible.

- **HTML**:
  - Use lowercase tags and attributes: `<div class="hero-section">`, not `<DIV CLASS="HERO">`.
  - Semantic tags: `<section>`, `<nav>`, not just `<div>` soup.
  - Accessibility: Add ARIA labels for interactive elements.
    ```html
    <button aria-label="Toggle chatbot">Chat</button>
    ```
  - Indentation: 2 spaces, align attributes for readability.
    ```html
    <div class="card" id="insights">
        <h2>Insights</h2>
    </div>
    ```
- **CSS**:
  - Use custom properties: Stick to `--primary-color`, `--accent-color`, etc., from `styles.css`.
  - Organize with comments:
    ```css
    /* Hero Section */
    .hero-section {
        background: var(--primary-color);
    }
    ```
  - Class Names: Kebab-case (e.g., `.chat-message`). No IDs for styling.
  - Indentation: 2 spaces. Group related rules.
  - Media Queries: Group at the end of the file.
    ```css
    @media (max-width: 768px) {
        .sidebar { display: none; }
    }
    ```
  - Avoid `!important`. If you need it, you’re probably doing something wrong.

### General Rules 🌐
These apply to everyone, because we’re all in this churn-fighting boat together.

- **File Naming**: Kebab-case for files (e.g., `my-new-chart.js`). No spaces or uppercase.
- **Testing**: Test with `Sample_dataset1.csv` before committing. Ensure charts load and the chatbot doesn’t crash.
- **Dependencies**: Update `requirements.txt` for new Python packages. Avoid adding unused libraries (looking at you, `gunicorn`).
  ```text
  pandas==2.0.3
  ```
- **Commits**: Small, focused commits with clear messages.
  ```bash
  git commit -m "Fix chatbot crash on empty input"
  ```
- **Logging**: Use `app.log` for Python errors. Console.log for JavaScript debugging, but remove before committing.
- **No Breaking Changes**: Don’t mess with the chatbot’s soul or the dashboard’s dark theme. We’re attached.
- **Optional Linters**:
  - Python: Run `pylint app.py` or `flake8` for PEP 8 compliance.
  - JavaScript: Use `eslint` with `camelcase` and `indent` rules.
  - CSS: Try `stylelint` for consistent formatting.
  - Not mandatory, but they’ll make your code extra shiny.

Got it? Now go write code that makes our dashboard proud. If you don’t, we’ll send the chatbot to haunt your dreams with churn stats. 😜