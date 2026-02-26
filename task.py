from crewai import Task
from agents import financial_analyst, risk_assessor, verifier

# Task 1: Verify / classify document
verify_document = Task(
    description=(
        "You will be given inputs:\n"
        "- file_path: path to the uploaded PDF\n"
        "- query: the user question\n\n"
        "Step 1) Use the tool read_financial_pdf(file_path) to extract text.\n"
        "Step 2) Determine if this looks like a financial document (earnings report, annual report, bank statement, invoice, etc.).\n"
        "Step 3) Output:\n"
        "- doc_type (string)\n"
        "- readability (good/partial/empty)\n"
        "- short_reason (1-3 lines)\n"
    ),
    expected_output=(
        "A short structured output with doc_type, readability, and short_reason."
    ),
    agent=verifier,
)

# Task 2: Main analysis grounded in the PDF + answer query
analyze_financial_document = Task(
    description=(
        "You will be given inputs:\n"
        "- file_path: path to the uploaded PDF\n"
        "- query: the user question\n\n"
        "Instructions:\n"
        "1) Call read_financial_pdf(file_path) to get the document text.\n"
        "2) Answer the user's query using only the extracted text.\n"
        "3) Extract key numbers if present (revenue, profit, margins, cash flow, debt, guidance). If missing, say 'Not found'.\n"
        "4) Provide a concise conclusion.\n\n"
        "Output format (use headings):\n"
        "## Answer to Query\n"
        "## Key Extracted Metrics\n"
        "## Notes / Assumptions\n"
        "## Disclaimer\n"
        "Disclaimer must say this is informational and not financial advice.\n"
    ),
    expected_output="A clear analysis using the required headings.",
    agent=financial_analyst,
)

# Task 3: Risk assessment grounded in the PDF
assess_risk = Task(
    description=(
        "You will be given inputs:\n"
        "- file_path: path to the uploaded PDF\n"
        "- query: the user question\n\n"
        "Instructions:\n"
        "1) Call read_financial_pdf(file_path) to get the document text.\n"
        "2) Identify realistic risks mentioned or implied in the document.\n"
        "3) Separate risks into: Business, Financial, Market/Macro, Operational, Regulatory.\n"
        "4) If the document doesn't mention risks, say that explicitly.\n"
        "5) Keep it concise and non-alarmist.\n\n"
        "Output format:\n"
        "## Risk Summary\n"
        "## Risk Breakdown\n"
        "## What to Verify Next\n"
    ),
    expected_output="A structured risk assessment grounded in the PDF.",
    agent=risk_assessor,
)