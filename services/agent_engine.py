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

This report provides an academic overview of the topic "{state.topic}", synthesizing key information extracted from relevant sources and research articles.

---

## Key Findings

{state.summary}

---

## Conclusion

Based on the synthesized information, the findings highlight significant aspects and trends related to the topic under study, providing valuable insights for further exploration and understanding.

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
