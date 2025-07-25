import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from services.search import web_search
from services.summarize import summarize_text
from services.schemas import StateSchema
from fpdf import FPDF
import uuid
load_dotenv()

# Nodes
def research_node(state: StateSchema):

    articles = web_search(state.topic)
    return {"search_results": articles}

def summarize_node(state: StateSchema):
    articles = state.search_results or []

    if not articles:
        return {"summary": "No relevant search results to summarize.", "citations": []}

    summary = summarize_text(articles) 

 
    citations = []
    for art in articles:
        source = art.get("source", "Unknown Source")
        year = art.get("published_date", "n.d.") 
        title = art.get("title", "Untitled")
       
        citation = f"{source} ({year}): {title}"
        citations.append(citation)

    return {"summary": summary, "citations": citations}

def report_node(state: StateSchema):
    citations_text = ""
    if state.citations:
        citations_text = "\n".join(f"[{i+1}] {c}" for i, c in enumerate(state.citations))
    else:
        citations_text = "No citations available."

    report = f"""
# Research Report: {state.topic}

---

## Introduction

The topic of **"{state.topic}"** is of growing interest in today's rapidly evolving technological and socio-economic landscape. This report aims to explore and synthesize key insights derived from various credible sources, providing a comprehensive understanding of the subject matter. Through an automated web search and summarization process, the report presents a distilled overview of current trends, challenges, and emerging perspectives related to the topic. The goal is to facilitate further learning, spark critical thought, and encourage evidence-based discussions around "{state.topic}".

---

## Key Findings

{state.summary}

---

## Conclusion

In conclusion, the research on **"{state.topic}"** reveals a multifaceted perspective that integrates technological advancements, societal impacts, and evolving methodologies. The insights synthesized from the literature emphasize the significance of this topic in both academic and practical domains. As the field continues to develop, further investigation and continuous monitoring of new information are crucial. This report serves as a foundational stepping stone for deeper inquiry and informed decision-making in relation to "{state.topic}".

---

## References

{citations_text}
"""
    return {"report": report.strip()}



# Graph building
builder = StateGraph(StateSchema)
builder.add_node("research", research_node)
builder.add_node("summarize", summarize_node)
builder.add_node("report", report_node)

builder.set_entry_point("research")
builder.add_edge("research", "summarize")
builder.add_edge("summarize", "report")
builder.add_edge("report", END)

app = builder.compile()

def run_research_pipeline(topic: str) -> str:
    output = app.invoke({"topic": topic})
    return output.get("report", "")
