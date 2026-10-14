import streamlit as st
from main import run_research

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Multi-Agent Research System")
st.write(
    "Enter a topic and let your AI research system "
    "generate a research report."
)

st.divider()

topic = st.text_input(
    "Enter your research topic",
    placeholder="e.g., Impact of Generative AI on software development"
)

if st.button("🚀 Start Research", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("AI agents are researching your topic..."):
            try:
                report = run_research(topic)

                st.success("Research completed!")

                st.subheader("📄 Research Report")
                st.markdown(report)

                st.download_button(
                    label="📥 Download Report",
                    data=str(report),
                    file_name="research_report.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info(
                    "Check your terminal for the full error details."
                )