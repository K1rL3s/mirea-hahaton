import asyncio
import os
from xml.etree import ElementTree as ET

from faststream.nats.annotations import NatsBroker
from loguru import logger

from schemas.query.scan_query import ScanIPSchema, ScanPortSchema, ScanResultSchema


def is_discover_open_port(string: str) -> bool:
    # example: Discovered open port <port>/<protocol> on <ip>
    if string.startswith("Discovered open port"):
        return True
    return False


def parse_discover_open_port(scan_ip: ScanIPSchema, string: str) -> ScanPortSchema:
    # example: Discovered open port <port>/<protocol> on <ip>
    port = string.split(" ")[3]
    protocol = port.split("/")[1]
    port = port.split("/")[0]
    return ScanPortSchema(
        task_id=scan_ip.task_id,
        ip=scan_ip.ip,
        port=int(port.split("/")[0]),
        protocol=protocol,
        state="open",
    )


async def parse_xml_result(scan_ip: ScanIPSchema, broker: NatsBroker) -> None:
    if not os.path.exists(f"{scan_ip.task_id}-{scan_ip.ip}.xml"):
        logger.info("break 3")
        return await mark_ip_as_end(scan_ip, broker)

    tree = ET.parse(f"{scan_ip.task_id}-{scan_ip.ip}.xml")
    root = tree.getroot()
    host = root.find("host")
    if host.find("status").attrib["state"] == "down":
        logger.info("break 2")
        return await mark_ip_as_end(scan_ip, broker)

    ports = host.find("ports")
    if not ports:
        logger.info("break 3")
        return await mark_ip_as_end(scan_ip, broker)

    for port in ports.findall("port"):
        port_id = port.attrib["portid"]
        protocol = port.attrib["protocol"]
        state = port.find("state").attrib["state"]
        service = port.find("service").attrib["name"]
        reason = (
            port.find("state").attrib.get("reason")
            + " "
            + port.find("state").attrib.get("reason_ttl")
        )

        await broker.publish(
            message=ScanPortSchema(
                task_id=scan_ip.task_id,
                ip=scan_ip.ip,
                port=int(port_id),
                protocol=protocol,
                state=state,
                service=service,
                reason=reason,
            ),
            subject="scan-ip-port",
        )

    for extraport in host.findall("extraports"):
        state = extraport.attrib["state"]
        for extrareason in extraport.findall("extrareasons"):
            reason = extrareason.attrib["reason"]
            protocol = extrareason.attrib["proto"]
            ports = extrareason.attrib["ports"].split(",")
            for port in ports:
                if "-" in port:
                    start, end = port.split("-")
                    for p in range(int(start), int(end) + 1):
                        await broker.publish(
                            message=ScanPortSchema(
                                task_id=scan_ip.task_id,
                                ip=scan_ip.ip,
                                port=p,
                                protocol=protocol,
                                state=state,
                                reason=reason,
                            ),
                            subject="scan-ip-port",
                        )
                else:
                    await broker.publish(
                        message=ScanPortSchema(
                            task_id=scan_ip.task_id,
                            ip=scan_ip.ip,
                            port=int(port),
                            protocol=protocol,
                            state=state,
                            reason=reason,
                        ),
                        subject="scan-ip-port",
                    )

    ptr_record = None
    hostnames = host.find("hostnames")
    if hostnames:
        for hostname in hostnames.findall("hostname"):
            if hostname.attrib["type"] == "PTR":
                ptr_record = hostname.attrib["name"]
                break

    await mark_ip_as_end(scan_ip, broker, ptr_record)


async def mark_ip_as_end(
    scan_ip: ScanIPSchema,
    broker: NatsBroker,
    ptr_record: str | None = None,
) -> None:
    await broker.publish(
        message=ScanResultSchema(
            task_id=scan_ip.task_id,
            ip=scan_ip.ip,
            ptr_record=ptr_record,
        ),
        subject="scan-ip-final",
    )


async def read_nmap_stream(
    stream: asyncio.StreamReader,
    broker: NatsBroker,
    scan_ip: ScanIPSchema,
) -> None:
    while True:
        line = await stream.readline()
        if not line:  # Поток завершен
            await parse_xml_result(scan_ip, broker)
            break
        line = line.decode().strip()
        if is_discover_open_port(line):
            await broker.publish(
                message=parse_discover_open_port(scan_ip, line),
                subject="scan-ip-port",
            )
            continue
