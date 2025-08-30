# Finance ChatBot Assistant

An AI‑powered personal finance chatbot built with Streamlit, Cohere, and SQLite. It helps users understand their spending, estimate taxes, and get budget and investment guidance—all through natural conversation and interactive visual insights.

---

##  Features

- **Conversational Assistant**: Ask about budgeting, taxes, investments, and more—your chatbot responds with clear, actionable insights.
- **Budget Summary**: Generate breakdowns of monthly expenses categorized automatically.
- **Spending Insights**: Get helpful tips and highlight areas where you might improve.
- **Tax Estimator**: Simple calculation of tax liability based on annual income (INR).
- **Investment Suggestions**: Tailored guidance to help save or invest your surplus.
- **Visual Insights**: Pie charts and visual cues to help you understand your financial habits.
- **Custom Modules**:  
  ‣ `assistant.py` – AI orchestration (Cohere integration)  
  ‣ `finance_utils.py` – Finance logic (budgeting, taxes, suggestions)  
  ‣ `db.py` – Data persistence via SQLite (or Google Sheets as an alternative)
- **Easy Deployment**: Hosted on Streamlit Cloud, accessible from anywhere.

---

##  Architecture

[ User Input (Streamlit UI) ]
           ↓
[ Cohere AI Model ] ← Prompt processing
           ↓
[ Finance Utils ] (budget, tax, investment)
           ↓
[ Persistence Layer ] (SQLite )
           ↓
[ Streamlit UI ] (Chat responses + visual insights)

---

##  Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/gunaa69/Finance_ChatBot.git
   cd Finance_ChatBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup your Cohere API key**
   - Locally: Create a `.env` file with:
     ```
     COHERE_API_KEY=your_cohere_api_key_here
     ```
   - On Streamlit Cloud: Add it in **Secrets** with key `COHERE_API_KEY`.

4. **Run the app locally**
   ```bash
   streamlit run app.py
   ```

5. **Deploy on Streamlit Cloud**
   - Push your changes to GitHub.
   - Connect the repository on Streamlit Cloud.
   - Go to "Manage App" → set secrets → deploy.

---

##  Video Demo

Check out a quick preview of the app in action:  
*(Embedded or linked video preview here when available)*

---

##  Future Enhancements

- Voice-based interaction for hands-free use.
- Real-time finance API integration (bank accounts, stock data).
- Advanced AI insights: saving goals, spending predictions.
- Full mobile app version for on-the-go financial help.

---

##  Acknowledgments

- **Cohere** for providing powerful NLP capabilities.
- **Streamlit** for enabling fast and interactive app development.


---


Questions, feedback, or collaboration ideas?  
Open an issue or reach out via GitHub.
