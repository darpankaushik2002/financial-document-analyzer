from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from task import verify_document, analyze_financial_document, assess_risk
from agents import financial_analyst, risk_assessor, verifier
from storage import init_db, save_result, get_result

app = FastAPI(title="Financial Document Analyzer", version="1.0.0")

@app.on_event("startup")
def startup():
    os.makedirs("data", exist_ok=True)
    init_db()

def run_crew(query: str, file_path: str):
    crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor],
        tasks=[verify_document, analyze_financial_document, assess_risk],
        process=Process.sequential,
        verbose=True,
    )
    # IMPORTANT: pass both query and file_path so tasks can use them
    return crew.kickoff(inputs={"query": query, "file_path": file_path})

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    query: str = Form(default="Summarize this financial document and highlight key points."),
):
    if not query or not query.strip():
        query = "Summarize this financial document and highlight key points."

    analysis_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{analysis_id}.pdf"

    try:
        # Save upload
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Run CrewAI pipeline
        output = run_crew(query=query.strip(), file_path=file_path)

        # Crew output formatting: safely stringify
        output_str = str(output)

        # Best-effort split: since Task outputs are sequential, we keep the full combined output too.
        # For DB fields, store whole output in analysis and keep others empty if parsing fails.
        verification_txt = ""
        analysis_txt = output_str
        risk_txt = ""

        # Store to DB
        save_result(
            analysis_id=analysis_id,
            filename=file.filename,
            query=query.strip(),
            verification=verification_txt,
            analysis=analysis_txt,
            risk=risk_txt,
        )

        return {
            "status": "success",
            "id": analysis_id,
            "filename": file.filename,
            "query": query.strip(),
            "result": output_str,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

@app.get("/results/{analysis_id}")
async def results(analysis_id: str):
    res = get_result(analysis_id)
    if not res:
        raise HTTPException(status_code=404, detail="Result not found")
    return {"status": "success", "data": res}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)