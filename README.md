# Secure Enterprise RAG Chatbot

An internal company chatbot that answers questions from private organizational data, with access controlled by user role.

## Features
- **RBAC:** Finance sees financial docs, HR sees employee/payroll data, C-level sees everything. Enforced at retrieval time via metadata filters.
- **Guardrails:** PII detection/masking and out-of-scope question handling.
- **Evaluation:** Ragas metrics (faithfulness, answer relevancy, context precision) run automatically in CI.
- **Monitoring:** LangSmith tracing, plus token usage and cost tracking with alerts.
- **Deployment:** Dockerized and deployed on Azure.

## Tech Stack
| Layer | Tools |
|---|---|
| Framework | LangChain, Docling |
| Vector DB | Qdrant |
| LLM | GPT-OSS / Llama via Groq |
| Backend | FastAPI |
| Frontend | Streamlit |
| Evals & Monitoring | Ragas, LangSmith |
| Cloud | Azure |

## Architecture
_Diagram coming soon._

## Roles & Access
| Role | Access |
|---|---|
| Finance | Financial reports, marketing expenses |
| HR | Employee data, payroll |
| Marketing | Marketing docs |
| Engineering | Engineering docs |
| C-Level | All company data |
| Employee | General company info |

## Project Structure
```
├── data/        # source documents
├── src/         # application code
├── tests/       # RBAC, guardrail and eval tests
└── .env.example # required environment variables