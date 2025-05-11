import streamlit as st
from expense_manager import Expense, ExpenseTracker
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Settings ---
st.set_page_config(page_title="SpendWise - Expense Tracker", layout="centered")

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Login Function ---
def login():
    st.title("🔐 Login to SpendWise")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- Logout Function ---
def logout():
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.success("✅ Logged out successfully!")
        st.rerun()

# --- Main App ---
if not st.session_state.logged_in:
    login()
else:
    st.title("💸 SpendWise – Smart Expense Tracker")

    tracker = ExpenseTracker()

    # --- Monthly Budget ---
    st.sidebar.header("📅 Monthly Budget")
    budget_str = st.sidebar.text_input("Set Monthly Budget", "1000")
    try:
        budget = int(budget_str)
        if budget <= 0:
            st.error("Budget must be a positive integer.")
    except ValueError:
        st.error("Please enter a valid integer value for the budget.")

    # --- Add Expense ---
    st.sidebar.header("➕ Add New Expense")
    with st.sidebar.form("expense_form"):
        amount_str = st.text_input("Amount", "0")
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
        description = st.text_input("Description")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    st.error("Amount must be greater than zero.")
                else:
                    new_expense = Expense(amount, category, description)
                    tracker.add_expense(new_expense)
                    st.success("✅ Expense added successfully!")
            except ValueError:
                st.error("Please enter a valid numeric value for the amount.")

    # --- View Expenses ---
    st.markdown("## 📊 Your Expense History")
    expenses = tracker.get_expenses()
    if expenses:
        df = pd.DataFrame(expenses)
        df["Amount"] = df["Amount"].astype(float)
        df["Date"] = pd.to_datetime(df["Date"])

        now = datetime.now()
        this_month_df = df[df["Date"].dt.month == now.month]
        total_spent = this_month_df["Amount"].sum()

        # --- Budget Bar and Alerts ---
        st.markdown("### 📈 Monthly Budget Usage")
        percent = min(total_spent / budget, 1.0)
        st.progress(percent, text=f"Used ${total_spent:.2f} of ${budget:.2f}")

        if total_spent >= budget:
            st.error("🚨 You’ve reached your budget limit!")
        elif total_spent >= 0.8 * budget:
            st.warning("⚠️ You're close to your monthly limit!")

        # --- Table and Charts ---
        st.dataframe(df)

        with st.expander("🔍 Insights"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📌 By Category")
                fig = px.pie(df, names="Category", values="Amount", title="Expense Breakdown")
                st.plotly_chart(fig)

            with col2:
                st.markdown("### 📅 Over Time")
                fig2 = px.line(df.sort_values("Date"), x="Date", y="Amount", markers=True)
                st.plotly_chart(fig2)

        # --- Delete Expense ---
        st.markdown("## ❌ Delete an Expense")
        expense_to_delete = st.selectbox("Select an expense to delete", df["Description"].tolist())
        if st.button("Delete Selected Expense"):
            if expense_to_delete:
                tracker.delete_expense(expense_to_delete)
                st.success(f"✅ Expense '{expense_to_delete}' deleted successfully!")
            else:
                st.error("Please select an expense to delete.")

    else:
        st.info("No expenses yet. Use the sidebar to add one!")

    # --- Logout Button ---
    logout()

    # --- Footer ---
    st.write("💡 **Built with ❤️ by Alishba Musharraf**")
