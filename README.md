# Financial Document Analyzer (CrewAI) — Debug Challenge Submission

## 📌 Overview

This project is a corrected and improved version of a CrewAI-based Financial Document Analyzer exposed through a FastAPI API.

The system allows users to upload a financial PDF document (earnings report, statement, filing, etc.), ask a query, and receive:

- Document verification
- Structured financial analysis
- Risk assessment
- Persisted results in SQLite
- API-based retrieval of past analyses

The primary goal of this submission was to debug deterministic runtime failures, fix unsafe prompt design, resolve dependency conflicts, and ensure the system runs reliably end-to-end.

---

# ✅ Deterministic Bugs Fixed

## 1) Undefined LLM Initialization (`llm = llm`)
**Bug:**  
`agents.py` contained `llm = llm`, causing immediate runtime failure.

**Fix:**  
Proper LLM initialization using:

```python
from crewai import LLM
MODEL_NAME = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")
llm = LLM(model=MODEL_NAME)

## 2) Unsafe / Hallucination-Oriented Prompts

  Bug:
  Original prompts explicitly instructed agents to:

  Hallucinate financial advice

  Generate fake URLs

  Ignore document grounding

  Fix:
  Prompts were rewritten to:

  Ground all outputs in extracted PDF text

  Explicitly say "Not found" if data is missing

  Avoid speculation

  Include a clear informational disclaimer

  Workflow now follows:

  Extract → Answer → Highlight Missing Data → Structured Output


##3) Broken Tool Implementation

  Bug:
  tools.py referenced a non-existent Pdf class.

  Fix:
  Implemented a working PDF tool using pypdf.PdfReader and CrewAI's @tool decorator.

  @tool("read_financial_pdf")
  def read_financial_pdf_tool(file_path: str) -> str:

  The tool:

  Validates file existence

  Cleans whitespace

  Handles empty/scanned PDFs safely


##4) Incorrect Agent Parameter (tool= instead of tools=)

  Bug:
  Agents were initialized with tool=[...].

  Fix:
  Corrected to:

  tools=[read_financial_pdf_tool]

##5) Uploaded File Path Not Passed to Tasks

  Bug:
  The API saved uploaded PDFs, but crew.kickoff() only received {query}.
  Tasks could not access the file.

  Fix:
  Now passing both inputs:

  crew.kickoff(inputs={
      "query": query,
      "file_path": file_path
  })
##6) Dependency Conflicts (Pydantic v1 vs v2)

  Bug:
  pydantic==1.10.13 and pydantic_core==2.8.0 were pinned together — incompatible.

  Fix:
  Standardized to Pydantic v2:

  pydantic>=2.8.2,<3.0.0

  Removed manual pydantic_core pin.

🚀 Setup Instructions
1️⃣ Clone Repository
git clone <repo_url>
cd financial-document-analyzer
2️⃣ Create Virtual Environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Mac/Linux:

python3 -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables

Create a .env file:

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=openai/gpt-4o-mini

5️⃣ Run the Application
uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000/docs
📌 API Endpoints
GET /

Health check

POST /analyze

Upload a PDF + provide a query.

Request:

file (PDF)

query (optional)

Response:

{
  "status": "success",
  "id": "...",
  "filename": "...",
  "query": "...",
  "result": "..."
}
GET /results/{analysis_id}

Retrieve stored analysis from SQLite.

⚙️ Design Decisions

Sequential multi-agent orchestration ensures verification before analysis.

Tool-based grounding prevents hallucination.

SQLite ensures persistence without external infrastructure.

FastAPI provides clear, testable endpoints.

📊 Limitations

OCR not implemented (scanned PDFs may return empty text warning).

Celery worker included but API currently runs synchronously.

No authentication layer (intended for demo/internal use).

🧠 Summary

This submission:

Fixes all deterministic runtime crashes

Eliminates hallucination-prone prompts

Corrects dependency conflicts

Restores proper tool integration

Ensures file path is correctly passed through the pipeline

Provides a stable, testable FastAPI interface

The system now runs reliably end-to-end with correct grounding, structured output, and safe error handling.


  ✅ Architectural Improvements
✔ Grounded Multi-Agent Flow

Three specialized agents:

Document Verifier

Financial Analyst

Risk Assessor

Executed sequentially using CrewAI’s Process.sequential.

✔ Structured Output Design

Financial analysis includes:

Answer to Query

Key Extracted Metrics

Notes / Assumptions

Disclaimer

Risk analysis includes:

Risk Summary

Risk Breakdown

What to Verify Next

✔ Safe Error Handling

File cleanup after processing

API returns structured HTTP errors

SQLite persistence for reproducibility

✔ SQLite Result Storage

All analyses are stored in:

analysis.db

Results retrievable via:

GET /results/{analysis_id}