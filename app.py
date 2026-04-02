import gradio as gr
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.react_agent import agent

def answer_question(question: str) -> str:
    if not question.strip():
        return "Please enter a question."
    
    try:
        return agent(question)
    
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn = answer_question,
    inputs = gr.Textbox(
        label="Ask a question about JPMorgan, Goldman Sachs or Bank of America",
        placeholder="e.g. What are the main risks for JPMorgan in 2025?",
        lines=2,
    ),
    outputs=gr.Textbox(
        label="Answer (from real 10-K filings)",
        lines=15,
    ),
    title = "Fintech Audit AI",
    description = "An AI agent that answers questions using real SEC 10-K filings from JPMorgan, Goldman Sachs and Bank of America. Powered by RAG + local LLM.",
    examples = [
        ["What are the main risks for JPMorgan?"],
        ["How does Goldman Sachs manage market risk?"],
        ["What is Bank of America's growth strategy?"],
        ["Compare how JPMorgan and Goldman Sachs manage risk differently?"],
    ],
)

if __name__ == "__main__":
    demo.launch()
