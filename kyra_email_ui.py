
import streamlit as st
from enhanced_email_sender import send_email
import os
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Ky’ra Email Sender", layout="centered")
st.title("📧 Ky’ra Email Sender Dashboard")

to_emails = st.text_input("Recipient Email(s) [comma-separated]")
subject = st.text_input("Subject")
html_content = st.text_area("HTML Content", height=200)
uploaded_files = st.file_uploader("Attachments (Optional)", accept_multiple_files=True)

if st.button("Send Email"):
    if not to_emails or not subject or not html_content:
        st.warning("Please fill all the required fields.")
    else:
        try:
            attachments = []
            for uploaded_file in uploaded_files:
                with NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    attachments.append({
                        "path": tmp.name,
                        "filename": uploaded_file.name,
                        "type": uploaded_file.type
                    })

            send_email(
                to_emails=[email.strip() for email in to_emails.split(",")],
                subject=subject,
                html_content=html_content,
                attachments=attachments if attachments else None
            )
            st.success(f"✅ Email sent successfully to: {to_emails}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {str(e)}")
