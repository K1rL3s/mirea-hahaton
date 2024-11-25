import uuid
from typing import Any

from database.repos.scan_port import ScanPortsRepo
from database.repos.scan_result import ScanResultRepo


class ScanTaskService:
    def __init__(
        self,
        scan_repo: ScanResultRepo,
        ports_repo: ScanPortsRepo,
    ) -> None:
        self.scan_repo = scan_repo
        self.ports_repo = ports_repo

    async def response(self, task_id: uuid.UUID) -> dict[str, Any]:
        scan_result = await self.scan_repo.get_by_uuid(uuid=task_id)
        data = {
            "task_id": task_id,
            "end": all(result.end for result in scan_result),
            "ips": [],
        }

        for result in scan_result:
            ports = await self.ports_repo.get_by_uuid_ip(task_id, result.ip)
            ports_schema = {"open": [], "closed": []}
            for port in ports:
                if port.status == "open":
                    ports_schema["open"].append(port)
                else:
                    ports_schema["closed"].append(port.port)

            data["ips"].append(
                {
                    "ip": result.ip,
                    "ptr": result.ptr_record,
                    "ports": ports_schema,
                    "end": result.end,
                },
            )

        return data
