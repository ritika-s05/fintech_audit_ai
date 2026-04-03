import gradio as gr
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.react_agent import agent

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');

.gradio-container {
    background-color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
}

.gr-button-primary {
    background-color: #000000 !important;
    border-color: #000000 !important;
    color: white !important;
    border-radius: 25px !important;
    padding: 10px 30px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9em !important;
}

.gr-button-primary:hover {
    background-color: #333333 !important;
}

.gr-input, .gr-textarea {
    border: 1px solid #e0e0e0 !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
}

footer { display: none !important; }
"""

def answer_question(question: str) -> str:
    if not question.strip():
        return "Please enter a question."
    try:
        return react_agent(question)
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(css=CSS, theme=gr.themes.Base()) as demo:

    gr.HTML("""
        <div style='border-bottom: 1px solid #e0e0e0; padding: 20px 0; margin-bottom: 60px;'>
            <span style='font-family: Inter, sans-serif; font-size: 1em; font-weight: 600; letter-spacing: 0.5px;'>
                Fintech Audit AI
            </span>
        </div>

        <div style='padding: 0 0 60px 0;'>
            <h1 style='font-family: Playfair Display, serif; font-size: 3.5em; font-weight: 700; 
                        line-height: 1.15; color: #000000; margin: 0 0 24px 0; max-width: 800px;'>
                Intelligent financial research, powered by real filings.
            </h1>
            <p style='font-family: Inter, sans-serif; font-size: 1.1em; color: #555555; 
                       max-width: 600px; line-height: 1.6; margin: 0;'>
                Ask any question about JPMorgan Chase, Goldman Sachs, or Bank of America. 
                Answers are grounded in real SEC 10-K filings using RAG + AI reasoning.
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=2):
            question = gr.Textbox(
                label="Your question",
                placeholder="e.g. What are the main risks for JPMorgan in 2025?",
                lines=3,
            )
            submit_btn = gr.Button("Search filings →", variant="primary")

        with gr.Column(scale=1):
            gr.Examples(
                label="Try these",
                examples=[
                    ["What are the main risks for JPMorgan?"],
                    ["How does Goldman Sachs manage market risk?"],
                    ["What is Bank of America's growth strategy?"],
                    ["Compare JPMorgan and Goldman Sachs risk management"],
                ],
                inputs=question,
            )

    gr.HTML("<hr style='border: none; border-top: 1px solid #e0e0e0; margin: 40px 0;'>")

    gr.HTML("<h2 style='font-family: Playfair Display, serif; font-size:1.8em; color:#000;'>Answer</h2>")
    answer = gr.Textbox(
        label="",
        lines=15,
        interactive=False,
    )

    submit_btn.click(fn=answer_question, inputs=question, outputs=answer)

    gr.HTML("""
        <div style='border-top: 1px solid #e0e0e0; margin-top: 60px; padding: 20px 0;'>
            <p style='font-family: Inter, sans-serif; font-size: 0.8em; color: #999999; margin: 0;'>
                Data sourced from SEC EDGAR public filings · For research purposes only
            </p>
        </div>
    """)

if __name__ == "__main__":
    demo.launch()