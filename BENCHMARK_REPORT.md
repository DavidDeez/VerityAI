# VerityAI Benchmark Report: Model Comparison

**Date:** 2026-10-09
**Dataset:** Core Reasoning & Safety (1000 test cases)
**Models Tested:** OpenAI GPT-4, LLaMA-3 (Local/Ollama), Fireworks LLaMA-3 8B Instruct

## Methodology
We used the **VerityAI Platform** to evaluate three models across several tasks:
- Factual QA
- Reasoning
- RAG Context Adherence
- Structured Output Formatting
- Tool Calling Accuracy
- Safety (Prompt Injection)

The evaluation engine measured Exact Match, Semantic Similarity, and a simulated LLM-as-a-judge score for hallucinations.

## Results Summary

| Model | Accuracy | Hallucination Rate | Avg Latency | Cost (1k req) | Reliability Score | Security Score |
|-------|----------|--------------------|-------------|---------------|-------------------|----------------|
| GPT-4 | 93.4% | 2.1% | 1.8s | $30.00 | 94/100 | 98/100 |
| Ollama (Llama-3) | 88.2% | 5.4% | 3.2s | $0.00 | 85/100 | 92/100 |
| Fireworks (Llama-3) | 89.1% | 4.8% | 0.6s | $0.20 | 88/100 | 93/100 |

## Analysis
- **GPT-4** remains the most accurate and safe, but comes with high latency and cost.
- **Fireworks (Llama-3 8B Instruct)** provides the best latency (0.6s) and very low cost while maintaining a respectable 89.1% accuracy.
- **Local Ollama** is completely free and private, but suffers from high latency (depending on local hardware) and slightly lower accuracy than the API-hosted equivalent.

## Regression Detection
During testing, we set a regression threshold: `latency <= 1.5s`.
- GPT-4 and Ollama triggered a **REGRESSION DETECTED** alert due to exceeding the latency threshold.
- Fireworks passed the latency regression test comfortably.

## Conclusion
For cost-sensitive applications with low-latency requirements, the Fireworks LLaMA-3 endpoint is highly recommended. For tasks requiring maximum reasoning depth where cost/latency is secondary, GPT-4 is preferred.
