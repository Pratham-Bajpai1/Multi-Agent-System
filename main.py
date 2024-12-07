import time
from agents import ResearchAgent, UseCaseGenerator, DatasetCollector
from report_generator import generate_reports
from utils import SERP_API_KEY
import streamlit as st
import os


# Initialize agents
research_agent = ResearchAgent(api_key=SERP_API_KEY)
use_case_agent = UseCaseGenerator(llm_provider="cohere")  # or "cohere" or "huggingface"
dataset_agent = DatasetCollector()

def main():
    # Page Configuration
    st.set_page_config(page_title="Multi-Agent Use Case Generator", layout="wide")

    # Initialize session state
    if "generated" not in st.session_state:
        st.session_state.generated = False
    if "company" not in st.session_state:
        st.session_state.company = ""
    if "industry" not in st.session_state:
        st.session_state.industry = ""
    if "use_case_results" not in st.session_state:
        st.session_state.use_case_results = []

    # Title and Description
    st.title("AI-Powered Multi-Agent System")
    st.write("""
        This system generates innovative AI/ML use cases tailored for a company in a specific industry.
        Provide your inputs below, and the system will generate a detailed report.
    """)

    # Input Section
    with st.form("input_form"):
        st.header("Enter Details")
        company = st.text_input("Company Name", placeholder="e.g., OpenAI")
        industry = st.text_input("Industry", placeholder="e.g., Artificial Intelligence")
        submit = st.form_submit_button("Generate Use Cases")

    # Process Inputs
    if submit:
        if not company or not industry:
            st.error("Both fields are required!")
        else:
            with st.spinner("Generating use cases, please wait..."):
                st.session_state.company = company
                st.session_state.industry = industry

                # Step 1: Research Industry
                research_query = (f"Conduct market research for the company '{company}' in the industry '{industry}'."
                                  f"Provide concise, insightful key findings about the company's strategic focus, recent innovations, and market positioning.)"
                                  f"Include relevant sources, such as official websites, industry reports, or expert analyses, for credibility."
                                  f"Focus on specific themes like:"
                                  f"1. AI/ML adoption and technological innovations."
                                  f"2. Competitor strategies and market trends."
                                  f"3. Challenges and opportunities within the industry.")

                research_results = research_agent.search(research_query)

                # Step 2: Generate Use Cases
                st.session_state.use_case_results = use_case_agent.generate(industry, company)

                # Step 3: Collect Datasets
                datasets = dataset_agent.collect(industry)

                # Step 4: Generate Report
                market_research_report_path = "Market_Research_Report.xlsx"
                use_case_report_path =  "Use_Case_Feasibility_Report.docx"
                generate_reports(research_results, st.session_state.use_case_results, datasets, company, industry)

                st.session_state.generated = True

        # Display Results
        if st.session_state.generated:
            st.success("Top 5 Use Cases Generated!")
            for idx, use_case in enumerate(st.session_state.use_case_results[:5], start=1):
                st.subheader(f"{idx}. {use_case['Use Case']}")
                st.write(f"**Description**: {use_case['Description']}")
                st.write(f"**Benefits**: {' '.join(use_case['Benefits'])}")
                st.markdown("---")

            # Download buttons
            market_research_report_path = "Market_Research_Report.xlsx"
            use_case_report_path = "Use_Case_Feasibility_Report.docx"

            with open(market_research_report_path, "rb") as excel_file:
                st.download_button(
                    label="Download Market Research Report (Excel)",
                    data=excel_file,
                    file_name=market_research_report_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            with open(use_case_report_path, "rb") as doc_file:
                st.download_button(
                    label="Download Use Case Feasibility Report (DOC)",
                    data=doc_file,
                    file_name=use_case_report_path,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            st.info("For detailed use cases or resource links, refer to the above reports.")

            # Reset Button
            if st.button("Generate New Use Cases"):
                st.session_state.generated = False
                st.session_state.company = ""
                st.session_state.industry = ""
                st.session_state.use_case_results = []
                st.experimental_rerun()

if __name__ == "__main__":
    main()