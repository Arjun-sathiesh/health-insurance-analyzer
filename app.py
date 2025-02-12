import streamlit as st
import time
import pypdf
import google.generativeai as genai

# Dummy user credentials (Replace with a database in a real system)
USER_CREDENTIALS = {"admin": "password123", "user": "userpass"}

# App Title
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🔐 Health Insurance Claim Management</h1>", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# Login system
if not st.session_state["logged_in"]:
    st.markdown("### 🔑 **Login to your account**")
    username = st.text_input("👤 Username", key="username_input")
    password = st.text_input("🔒 Password", type="password", key="password_input")

    if st.button("Login", use_container_width=True):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username  # Store username in session state
            st.success("✅ Login Successful! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")
else:
    # Sidebar with user details and logout option
    with st.sidebar:
        st.markdown(f"<h3>✅ Logged in as: <span style='color: green;'>{st.session_state['username']}</span></h3>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()

    # Claim submission form
    st.markdown("## 📝 **Submit a Health Insurance Claim**")
    with st.form("claim_form"):
        policy_number = st.text_input("🏷️ Policy Number")
        patient_name = st.text_input("🧑‍⚕️ Patient Name")
        hospital_name = st.text_input("🏥 Hospital Name")
        treatment_details = st.text_area("📋 Treatment Details")
        bill_amount = st.number_input("💰 Bill Amount ($)", min_value=0.0, step=0.1)
        submit = st.form_submit_button("🚀 Submit Claim")

        if submit:
            st.success("✅ Claim Submitted Successfully!")

    # File upload for supporting documents
    document = st.file_uploader("📂 Upload Supporting Documents (PDF)", type=["pdf"])

    # Initialize decision and reason variables
    decision = ""
    reason = ""

    if document:
        st.info("📖 Extracting text from PDF...")
        progress = st.progress(0)
        for i in range(1, 5):
            time.sleep(0.5)
            progress.progress(25 * i)
        
        reader = PdfReader(document)
        document_text = reader.pages[0].extract_text()
        st.success("✅ Document Uploaded & Processed!")

        # AI Analysis Function with Acceptance or Rejection Decision
        def AI_analysis(text, policy, patient):
            prompt = f"""
            Analyze the health insurance claim based on the following details:
            
            **Patient Name:** {patient}
            **Policy Number:** {policy}
            **Claim Details:** {text}
            
            Provide insights into:
            1. Claim Validity Check
            2. Coverage Eligibility
            3. Fraud Detection Probability
            4. AI Recommendations for Approval or Further Review
            
            Based on the analysis, provide a clear decision:
            - **Accepted**: If everything is correct and meets policy conditions.
            - **Rejected**: If there are issues, specify the problem (e.g., insufficient coverage, fraud suspicion, missing information).
            
            Format the output as follows:
            - Decision: Accepted/Rejected
            - Reason (if Rejected)
            """

            # Configure Generative AI
            genai.configure(api_key="AIzaSyCSl9V3uB3CRT9j2xU2tJTtYvgDp3aphqs")  # Replace with a secure method
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            
            result_text = response.text.strip()

            # Extract Decision
            if "Rejected" in result_text:
                decision = "❌ **Claim Status: Rejected**"
                reason = result_text.split("Reason:")[1] if "Reason:" in result_text else "Issue not specified."
            else:
                decision = "✅ **Claim Status: Accepted**"
                reason = "No issues found."

            return decision, reason

        st.write("⏳ Analyzing Claim... Please wait.")
        decision, reason = AI_analysis(document_text, policy_number, patient_name)

    # Tab layout for claim results
    tab1, tab2 = st.tabs(["📊 Claim Analysis", "🔎 Fraud Detection"])
    
    with tab1:
        st.markdown("<h2 style='color: #2ECC71;'>📊 Claim Analysis</h2>", unsafe_allow_html=True)
        st.write(decision)  # Display accepted or rejected status
        if "Rejected" in decision:
            st.error(f"**Reason:** {reason}")
        else:
            st.success("✅ Claim is valid and eligible for processing.")

    with tab2:
        st.markdown("<h2 style='color: #E74C3C;'>🔎 Fraud Detection Insights</h2>", unsafe_allow_html=True)
        fraud_check = "Low" if "valid" in reason.lower() else "High"
        st.write(f"📌 **Fraud Probability:** `{fraud_check}`")

