import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import read_financial_pdf_tool

load_dotenv()

MODEL_NAME = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")

llm = LLM(
    model=MODEL_NAME,
    temperature=0.2,
    max_tokens=1500,
    timeout=120,
)
financial_analyst = Agent(
    role="Financial Analyst",
    goal=(
        "Analyze the provided financial document and answer the user's query using ONLY the document content. "
        "If something is missing from the document, say so explicitly."
    ),
    backstory=(
        "You are a careful financial analyst. You ground every claim in the provided document text "
        "and avoid making unsupported assumptions."
    ),
    verbose=True,
    memory=False,
    tools=[read_financial_pdf_tool],
    llm=llm,
    allow_delegation=False,
    max_iter=3,
)

risk_assessor = Agent(
    role="Risk Assessor",
    goal=(
        "Identify realistic risks and uncertainties mentioned or implied by the document (macro, business, liquidity, concentration, etc.). "
        "Stay grounded in the document and avoid fear-mongering."
    ),
    backstory=(
        "You specialize in practical risk analysis and clearly communicate uncertainty. "
        "You do not fabricate extreme scenarios."
    ),
    verbose=True,
    memory=False,
    tools=[read_financial_pdf_tool],
    llm=llm,
    allow_delegation=False,
    max_iter=3,
)

verifier = Agent(
    role="Document Verifier",
    goal=(
        "Verify the uploaded file is readable and appears to be a financial document (report/statement/filing). "
        "Summarize what kind of document it is based on the extracted text."
    ),
    backstory=(
        "You are strict about classification. If the content looks non-financial or unreadable, you say so."
    ),
    verbose=True,
    memory=False,
    tools=[read_financial_pdf_tool],
    llm=llm,
    allow_delegation=False,
    max_iter=2,
)