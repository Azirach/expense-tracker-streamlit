# Personal Expenses Planner with Insights 💸

A Streamlit web application to analyze and plan your personal expenses with interactive visualizations and budget tracking.

## Features

- Upload and analyze expenses from CSV and Excel (.xlsx) files 
- View spending trends with interactive charts
- Set and adjust budget goals for different categories
- Auto-redistributing budget allocation sliders
- Compare actual spending vs budget goals with progress bars
- Visual insights with pie charts and line graphs
- Smart overspending alerts and recommendations

## Setup

1. Clone the repository
2. Create a virtual environment:
```sh
python -m venv .venv
.venv\Scripts\activate  # For Windows
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Run the application:
```sh
streamlit run app.py
```

## Data File Format
Your expense data file (CSV or Excel) must have these columns:
- Date: Transaction date
- Category: Expense category (Food, Travel, Shopping, Rent, Entertainment, Bills)
- Amount: Transaction amount

## Budget Categories
The application supports these expense categories:
- Food
- Travel 
- Shopping
- Rent
- Entertainment
- Bills

## Usage
1. Upload your expenses file (CSV or Excel)
2. Define budget goals as percentages (must total 100%)
3. Experiment with budget allocations using interactive sliders
4. View insights and spending analysis
5. Check for overspending