import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Initialize web search
search = DuckDuckGoSearchRun()


# Agent 1: Research Agent
def research_agent(topic):
    search_results = search.run(
        f"Research {topic}. Find reliable sources and key facts."
    )

    prompt = ChatPromptTemplate.from_template("""
    You are a research agent.

    Topic: {topic}

    Web search results:
    {results}

    Extract the important facts, evidence, and source references.
    Clearly distinguish verified information from uncertain claims.
    """)

    chain = prompt | llm

    result = chain.invoke({
        "topic": topic,
        "results": search_results
    })

    return result.content


# Agent 2: Analysis Agent
def analysis_agent(topic, research):
    prompt = ChatPromptTemplate.from_template("""
    You are an analytical research agent.

    Topic: {topic}

    Research findings:
    {research}

    Analyze the findings.
    Identify major themes, benefits, drawbacks, and insights.
    Do not invent facts.
    """)

    chain = prompt | llm

    result = chain.invoke({
        "topic": topic,
        "research": research
    })

    return result.content


# Agent 3: Writer Agent
def writer_agent(topic, analysis):
    prompt = ChatPromptTemplate.from_template("""
    You are a professional research report writer.

    Topic: {topic}

    Analysis:
    {analysis}

    Create a report containing:
    1. Introduction
    2. Key Findings
    3. Benefits
    4. Challenges
    5. Conclusion

    Use clear, beginner-friendly language.
    Do not add unsupported facts.
    """)

    chain = prompt | llm

    result = chain.invoke({
        "topic": topic,
        "analysis": analysis
    })

    return result.content


# Agent 4: Reviewer Agent
def reviewer_agent(topic, report):
    prompt = ChatPromptTemplate.from_template("""
    You are a critical report reviewer.

    Topic: {topic}

    Report:
    {report}

    Check for:
    - Unsupported claims
    - Missing important information
    - Contradictions
    - Clarity and organization

    Return an improved report.
    Flag claims that need further verification.
    Do not invent evidence or sources.
    """)

    chain = prompt | llm

    result = chain.invoke({
        "topic": topic,
        "report": report
    })

    return result.content


# Main workflow
def run_research(topic):
    print("\n🔍 Research Agent working...")
    research = research_agent(topic)

    print("\n🧠 Analysis Agent working...")
    analysis = analysis_agent(topic, research)

    print("\n✍️ Writer Agent working...")
    report = writer_agent(topic, analysis)

    print("\n✅ Reviewer Agent working...")
    final_report = reviewer_agent(topic, report)

    return final_report


# Run the system
if __name__ == "__main__":
    topic = input("Enter your research topic: ")

    final_report = run_research(topic)

    print("\n\n========== FINAL REPORT ==========\n")
    print(final_report)

    with open("research_report.md", "w", encoding="utf-8") as file:
        file.write(final_report)

    print("\nReport saved to research_report.md")