---
title: Fintech Audit AI
emoji: 📊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# 📊 Fintech Audit AI

An AI agent that answers questions using real SEC 10-K filings from JPMorgan, Goldman Sachs and Bank of America.

## What it does
- Downloads real SEC EDGAR filings
- Chunks and embeds them locally
- Uses ReAct multi-step reasoning to answer financial questions
- Powered by RAG + Groq LLM

## Stack
- sentence-transformers (embeddings)
- ChromaDB (vector store)
- Groq API (LLM)
- Gradio (UI)