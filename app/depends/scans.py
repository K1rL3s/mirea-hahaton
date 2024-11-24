from app.exceptions.scans import (
    InvalidRate,
    InvalidSpecificRange,
    InvalidTopPortRange,
    InvalidVersionIntensity,
)
from schemas.scan_api import ScanRequest
from utils.enums.nmap import PortRange, VersionDetection


async def check_scan_request(scan_request: ScanRequest) -> ScanRequest:
    if scan_request.version_detection == VersionDetection.VERSION_INTENSITY:
        if (
            scan_request.version_intensity_value is None
            or scan_request.version_intensity_value < 1
            or scan_request.version_intensity_value > 9
        ):
            raise InvalidVersionIntensity

    if scan_request.port_range == PortRange.SPECIFIC:
        if scan_request.specific_range is None:
            raise InvalidSpecificRange
        if "-" in scan_request.specific_range:
            from_, to_ = map(int, scan_request.specific_range.split("-"))
            if from_ < 1 and to_ > 65535:
                raise InvalidSpecificRange
        else:
            ports = scan_request.specific_range.split()
            for port in ports:  # 1-65535
                if not port.isdigit() or int(port) < 1 or int(port) > 65535:
                    raise InvalidSpecificRange

    if scan_request.port_range == PortRange.TOP_PORTS:
        if scan_request.top_range is None or scan_request.top_range < 1:
            raise InvalidTopPortRange

    if scan_request.min_rate is not None and scan_request.max_rate is not None:
        if scan_request.min_rate > scan_request.max_rate:
            raise InvalidRate

    return scan_request
