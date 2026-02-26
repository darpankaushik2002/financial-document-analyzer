import os
from celery_app import celery_app
from main import run_crew
from storage import init_db, save_result

@celery_app.task(name="worker.run_analysis_job")
def run_analysis_job(analysis_id: str, query: str, file_path: str, filename: str):
    init_db()
    output = run_crew(query=query, file_path=file_path)
    output_str = str(output)

    save_result(
        analysis_id=analysis_id,
        filename=filename,
        query=query,
        verification="",
        analysis=output_str,
        risk="",
    )
    # Cleanup file (worker side)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass

    return {"id": analysis_id, "status": "done"}