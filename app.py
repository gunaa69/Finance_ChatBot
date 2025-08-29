# app.py
import streamlit as st
import os
import cohere
from dotenv import load_dotenv
import json
import pandas as pd
import matplotlib.pyplot as plt
from assistant import AIOrchestrator
from finance_utils import generate_budget_summary, spending_insights, simple_tax_estimator, investment_suggestions
from db import save_user, save_budget, save_chat


# Load environment variables from .env
load_dotenv()

# Get Cohere API key from environment
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None

def generate_cohere_response(prompt, model="command-r-plus", max_tokens=100):
    """Generate a response using Cohere's API."""
    if not co:
        return "Cohere API key not found. Please set COHERE_API_KEY in your .env file."
    response = co.generate(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens
    )
    return response.generations[0].text.strip()

st.set_page_config(page_title="Personal Finance Chatbot", layout="wide", page_icon="💸")

# instantiate orchestrator
ai = AIOrchestrator()


# UI: header + sidebar
st.title("💸 Personal Finance Chatbot")
st.markdown("Intelligent guidance for savings, taxes, and investments. All amounts are in INR.")


# Sidebar: user config
st.sidebar.header("User Settings")
name = st.sidebar.text_input("Your name", "User")
user_type = st.sidebar.selectbox("I am a:", ["Student", "Professional", "Other"])
income_currency = "INR"
annual_income = st.sidebar.text_input(f"Estimated annual income ({income_currency})", value="500000")
try:
    annual_income = float(annual_income.replace(",", ""))
except ValueError:
    annual_income = 0.0


# Save or create user (simple)
if st.sidebar.button("Register / Save Profile"):
    uid = save_user(name, user_type)
    st.sidebar.success(f"Saved profile (id={uid})")
    st.balloons()

# Chat column + Budget column
col1, col2 = st.columns([2, 1])


with col1:
    st.subheader("Chat with the AI")
    user_text = st.text_input("Ask about savings, taxes, investments, budgets, or planning:")
    if st.button("Send"):
        if user_text.strip() == "":
            st.warning("Type a message first.")
        else:
            ctx = f"User is a {user_type}. Annual income ~ ₹{annual_income:,.2f}."
            with st.spinner("Thinking..."):
                text = generate_cohere_response(f"{ctx}\n{user_text}")
            st.success(text)
            st.snow()
            # Save the chat if user registered (rudimentary logic)
            try:
                save_chat(1, "user", user_text)
                save_chat(1, "assistant", text)
            except Exception:
                pass


    st.markdown("---")
    # Quick prompts / templates
    st.markdown("**Quick prompts:**")
    if st.button("How much should I save each month?"):
        sample = f"Given annual income ₹{annual_income:,.2f}, what percent should I save monthly? I'm a {user_type}."
        with st.spinner("Thinking..."):
            text = generate_cohere_response(sample)
        st.success(text)


with col2:
    st.subheader("Budget & Insights")
    st.markdown("Enter your monthly expenses below. All values in INR.")
    default_expenses = {
        "Rent": 15000,
        "Groceries": 4000,
        "Transport": 2000,
        "Entertainment": 2500,
        "Subscriptions": 800,
        "Shopping": 3000,
        "Investments": 5000
    }
    st.write("#### Monthly Expenses")
    expense_inputs = {}
    cols = st.columns(2)
    for idx, (cat, val) in enumerate(default_expenses.items()):
        with cols[idx % 2]:
            expense_inputs[cat] = st.number_input(f"{cat}", min_value=0, value=val, step=100)
    if st.button("Analyze Budget"):
        expenses = {cat: amt for cat, amt in expense_inputs.items()}
        try:
            # Save budget
            try:
                save_budget(1, json.dumps(expenses))
            except Exception:
                pass
            summary_md, total = generate_budget_summary(expenses)
            st.markdown(summary_md)
            # Pie chart
            df = pd.DataFrame(list(expenses.items()), columns=["Category", "Amount"])
            fig, ax = plt.subplots()
            ax.pie(df["Amount"], labels=df["Category"], autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)

            # Insights
            st.write("### 🔍 Spending Insights")
            for ins in spending_insights(expenses):
                st.info(ins)

            # Investment suggestions
            surplus = max(0.0, (annual_income / 12) - total)
            st.write("### 💡 Investment Suggestions")
            for sug in investment_suggestions(user_type, surplus):
                st.write("-", sug)

            # Tax estimator
            st.write("### 🧾 Simple Tax Estimate")
            tax = simple_tax_estimator(annual_income, deductions=0.0)
            st.write(f"- Taxable income: ₹{tax['taxable_income']:,.2f}")
            st.write(f"- Tax before cess: ₹{tax['tax_before_cess']:,.2f}")
            st.write(f"- Cess (4%): ₹{tax['cess_4pct']:,.2f}")
            st.write(f"- **Estimated total tax:** ₹{tax['total_tax']:,.2f}")

        except Exception as e:
            st.error("Failed to analyze budget. Please check your inputs.")
            st.exception(e)


st.markdown("---")
st.caption("All calculations and suggestions are for informational purposes only. All values are in INR.")
