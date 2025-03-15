
import streamlit as st
import pandas as pd
import os
import yagmail
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Email Configuration
EMAIL_SENDER = "Enter your mail address"
EMAIL_PASSWORD = "Enter your password"
UPLOAD_FOLDER = "folder list"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to read CSV
def fetch_payslip_data(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return None

# Function to generate PDF
def generate_payslip(employee_name, base_salary, deductions, net_pay):
    filename = os.path.join(UPLOAD_FOLDER, f"{employee_name}_Payslip.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Company Name: XYZ Ltd.")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Employee: {employee_name}")
    c.drawString(100, 710, f"Base Salary: ${base_salary}")
    c.drawString(100, 690, f"Deductions: ${deductions}")
    c.drawString(100, 670, f"Net Pay: ${net_pay}")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 650, "Thank you for your hard work!")
    c.save()
    return filename

# Function to send email
def send_payslip_email(employee_email, employee_name, payslip_file):
    try:
        yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
        subject = f"Payslip for {employee_name}"
        body = f"Dear {employee_name},\n\nPlease find attached your payslip for this month.\n\nBest Regards,\nXYZ Ltd."
        yag.send(to=employee_email, subject=subject, contents=body, attachments=payslip_file)
        return True
    except Exception as e:
        st.error(f"Error sending email to {employee_email}: {e}")
        return False

# Streamlit App UI
st.title("Payslip Generator & Email Sender")

# File uploader
uploaded_file = st.file_uploader("Upload Employee Salary CSV", type=["csv"])

if uploaded_file:
    df = fetch_payslip_data(uploaded_file)
    if df is not None:
        st.write("### Employee Salary Data")
        st.dataframe(df)

        if st.button("Generate & Send Payslips"):
            for _, row in df.iterrows():
                name, email, base_salary, deductions, net_pay = row["Name"], row["Email address"], row["GROSS"], row["Deduction"], row["Net_Pay"]
                payslip_file = generate_payslip(name, base_salary, deductions, net_pay)
                send_payslip_email(email, name, payslip_file)

            st.success("Payslips generated and emails sent successfully!")
