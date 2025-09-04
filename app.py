import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💸 Personal Expenses Planner with Insights")

# File uploader (CSV or Excel)
uploaded_file = st.file_uploader("Upload your expenses file", type=["csv", "xlsx"])

if uploaded_file:
    # Detect file type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        # Handle Excel with multiple sheets
        xls = pd.ExcelFile(uploaded_file)
        sheet = st.selectbox("Select a sheet", xls.sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet)

    # Ensure correct columns
    if "Date" in df.columns and "Category" in df.columns and "Amount" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        st.subheader("📊 Data Preview")
        st.write(df.head())

        # Total expenses
        total = df["Amount"].sum()
        st.metric("Total Expenses", f"₹{total:,.2f}")

        # Expenses over time
        st.subheader("Expenses Over Time")
        time_series = df.groupby("Date")["Amount"].sum()
        st.line_chart(time_series)

        # Genre-wise breakdown
        st.subheader("Genre-wise Breakdown")
        category_summary = df.groupby("Category")["Amount"].sum().reset_index()
        category_summary["Percentage"] = (category_summary["Amount"] / total) * 100
        st.dataframe(category_summary)

        # Step 1: User-defined budget goals
        st.subheader(" Define Your Budget Goals (must sum to 100%)")
        categories = ["Food", "Travel", "Shopping", "Rent", "Entertainment", "Bills"]

        inputs = {}
        cols = st.columns(len(categories))
        for i, cat in enumerate(categories):
            with cols[i]:
                inputs[cat] = st.number_input(f"{cat} (%)", min_value=0, max_value=100, value=0, step=1)

        total_input = sum(inputs.values())

        if total_input < 100:
            st.warning(f"⚠ You still have {100 - total_input}% left to allocate.")
            proceed = False
        elif total_input > 100:
            st.error(f"🚨 You have exceeded the 100% limit by {total_input - 100}%. Please adjust.")
            proceed = False
        else:
            st.success("✅ Perfect! Your allocations add up to 100%.")
            proceed = st.button("Proceed to Experiment with Sliders and see charts and graphs!")

        # Step 2: Auto-adjust sliders (only if valid input)
        if proceed:
            if "budget_goals" not in st.session_state:
                st.session_state.budget_goals = inputs.copy()

            st.subheader("⚡ Experiment: Adjust and Auto-Redistribute (always sum = 100%)")

            selected_cat = st.selectbox("Select category to adjust", categories)

            new_val = st.slider(
                f"{selected_cat} (%)",
                0, 100, int(st.session_state.budget_goals[selected_cat])
            )

            diff = new_val - st.session_state.budget_goals[selected_cat]
            st.session_state.budget_goals[selected_cat] = new_val

            if diff != 0:
                others = [c for c in categories if c != selected_cat]
                adjust = diff / len(others)
                for c in others:
                    st.session_state.budget_goals[c] -= adjust
                    st.session_state.budget_goals[c] = max(0, min(100, st.session_state.budget_goals[c]))

            total_slider = sum(st.session_state.budget_goals.values())
            if total_slider != 0:
                for c in categories:
                    st.session_state.budget_goals[c] = (st.session_state.budget_goals[c] / total_slider) * 100

            st.write(pd.DataFrame(st.session_state.budget_goals.items(), columns=["Category", "Goal (%)"]))

        # Step 3: Compact comparison
        if "budget_goals" in st.session_state:
            st.subheader("Budget vs Actual (Compact View)")
            for _, row in category_summary.iterrows():
                cat, amt, perc = row["Category"], row["Amount"], row["Percentage"]
                goal = st.session_state.budget_goals.get(cat, 0)

                col1, col2, col3 = st.columns([2, 3, 2])
                with col1:
                    st.markdown(f"**{cat}**")
                with col2:
                    progress_val = min(int((perc / goal) * 100), 100) if goal > 0 else 0
                    st.progress(progress_val)
                with col3:
                    if perc > goal:
                        st.markdown(f" {perc:.1f}% vs {goal:.1f}%")
                    else:
                        st.markdown(f" {perc:.1f}% vs {goal:.1f}%")

            # Step 4: Pie chart comparison
            st.subheader("Budget Goals vs Actual Spending")

            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            axes[0].pie(category_summary["Amount"], labels=category_summary["Category"], autopct="%1.1f%%", startangle=90)
            axes[0].set_title("Actual Spending")

            axes[1].pie(st.session_state.budget_goals.values(), labels=st.session_state.budget_goals.keys(), autopct="%1.1f%%", startangle=90)
            axes[1].set_title("Budget Goals")

            st.pyplot(fig)

            # Overspending alerts
            st.subheader("⚠ Overspending Analysis & Suggestions")
            thresholds = {"Food": 20, "Travel": 15, "Shopping": 15, "Entertainment": 10, "Bills": 20, "Rent": 40}
            for _, row in category_summary.iterrows():
                cat, amt, perc = row["Category"], row["Amount"], row["Percentage"]
                threshold = thresholds.get(cat, 20)
                if perc > threshold:
                    st.error(f"{cat}: {perc:.1f}% of total (above recommended {threshold}%).")
                else:
                    st.success(f"{cat}: {perc:.1f}% of total (within recommended {threshold}%).")

    else:
        st.error("CSV/Excel must have columns: Date, Category, Amount")
else:
    st.info("Upload a CSV or Excel file to begin (columns: Date, Category, Amount).")
