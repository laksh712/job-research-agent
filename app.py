import streamlit as st
import time
from datetime import datetime
from fpdf import FPDF
import os

from agent import run_agent

st.set_page_config(
    page_title="Job Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("Job Research Agent")
st.markdown("*AI-powered company research for interview prep — powered by LangGraph + Llama 3.3*")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    company = st.text_input(
        "Company name",
        placeholder="e.g. Razorpay, CRED, Postman, Groww...",
        help="Enter any tech company name"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Research this company", type="primary", use_container_width=True)

if run_btn and company:
    st.divider()

    with st.status(f"Researching {company}...", expanded=True) as status:
        st.write("Searching tech stack...")
        time.sleep(0.5)
        st.write("Searching engineering culture...")
        time.sleep(0.5)
        st.write("Searching interview patterns...")
        time.sleep(0.5)
        st.write("Searching recent news...")
        time.sleep(0.5)
        st.write("Generating your brief...")

        report = run_agent(company)
        status.update(label="Research complete!", state="complete")

    st.markdown(report)
    st.divider()

    # Download as Markdown
    md_filename = f"{company.lower().replace(' ', '_')}_brief.md"
    st.download_button(
        label="Download as Markdown",
        data=report,
        file_name=md_filename,
        mime="text/markdown",
        use_container_width=True
    )

elif run_btn and not company:
    st.warning("Please enter a company name.")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray; font-size:12px;'>"
    "Built by Laksh — LangGraph + Llama 3.3-70B + Tavily | "
    "<a href='https://github.com/laksh712/job-research-agent'>GitHub</a>"
    "</p>",
    unsafe_allow_html=True
)