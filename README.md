# Discounted Cash Flow (DCF) Model for Stock Valuation 📊💹

Welcome to the **Discounted Cash Flow (DCF) Model**, a powerful tool built with **Flask** that allows you to project the intrinsic value of a stock based on its future cash flows. This project provides a simple yet effective way to assess whether a stock is overvalued or undervalued using financial modeling.

🚀 **Key Features**:
- **Stock Ticker Input**: Enter the stock ticker of the company you're interested in.
- **Projection Years**: Specify the number of years you want to project for.
- **Predictions & Insights**: Receive a detailed analysis of the company's future cash flows, along with a prediction of the intrinsic stock price.
- **Interactive Flask App**: The model runs on a Flask-based web app where users can input data and see results in real-time.

## 🚀 How to Run the Project

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Jack-0ut/dcf.git
cd dcf-model
``` 

### 2. Set Up the Virtual Environment
Set up and activate your virtual environment:

```bash
python -m venv venv
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate
``` 

### 3. Install Dependencies
Install all necessary dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application
Start the Flask server:

```bash
python app.py
```
The app will be available at http://127.0.0.1:5000/ in your web browser.

### 5. Use the DCF Model
Open the app in your browser.
Enter the stock ticker (e.g., AAPL for Apple, MSFT for Microsoft).
Specify the number of years to project the future cash flows.
Click on Submit to see the model’s prediction and detailed data on the intrinsic stock price.

### 🔧 Technologies Used
Flask: Lightweight web framework for creating the interactive application.
yFinance: Fetching real-time stock data for valuation.
NumPy & Pandas: Data handling and calculations.
Matplotlib & Plotly: Visualization of data and trends.

### ⚖️ License
This project is licensed under the MIT License.

### 🔄 Contribute
Contributions are welcome! If you would like to improve or add features to this project, feel free to fork the repository and create a pull request. You can also open issues for any bugs or suggestions.