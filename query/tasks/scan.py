from faststream.nats import NatsRouter

from schemas.scan_query import ScanInput, ScanOutput

router = NatsRouter()


@router.subscriber(subject="scan-input")
@router.publisher(subject="scan-output")
async def scan_handler(scan: ScanInput):
    print(scan.task_id, scan.message)
    return ScanOutput(task_id=scan.task_id, message=scan.message)
