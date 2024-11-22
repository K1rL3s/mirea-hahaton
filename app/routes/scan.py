from fastapi import APIRouter

from app.schemas.scan_request import ScanRequest

router = APIRouter()


@router.post("/scan/")
async def start_scan(scan_request: ScanRequest):
    task_result: TaskiqResult = await Taskiq.send_task(
        "scan_network", scan_request.targets,
    )
    return {"task_id": task_result.task_id}


@router.get("/results/{task_id}")
async def get_scan_results(task_id: str):
    # Логика получения результатов по task_id из базы
    pass
