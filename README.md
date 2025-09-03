# Personal Expenses Planner with Insights 💸

A Streamlit web application to analyze and plan your personal expenses with interactive visualizations and budget tracking.

## Features

- Upload and analyze expenses from CSV files
- View spending trends over time
- Interactive budget planning with auto-adjusting allocations
- Compare actual spending vs budget goals
- Visual insights with charts and progress bars
- Overspending alerts and recommendations

## Setup

1. Clone the repository
2. Create a virtual environment:
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Run the application:
```sh
streamlit run app.py
```

## CSV Format
Your expense data should have these columns:
- Date
- Category
- Amount