from enum import Enum


class ScanType(str, Enum):
    SYN = "-sS"
    TCP = "-sT"
    UDP = "-sU"
    ACK = "-sA"
    NULL = "-sN"
    FIN = "-sF"
    XMAS = "-sX"


class VersionDetection(str, Enum):
    VERSION = "-sV"
    AGGRESSIVE = "-A"


class HostDiscovery(str, Enum):
    NO_PING = "-Pn"
    SYN_PING = "-PS"
    ACK_PING = "-PA"
    ICMP_PING = "-PE"
    TIMESTAMP_PING = "-PP"
    NETMASK_PING = "-PM"


class PortRange(str, Enum):
    COMMON = "-F"
    SPECIFIC = "-p"
    TOP_PORTS = "--top-ports"
    ALL = "-p-"


class Timing(str, Enum):
    PARANOID = "-T0"
    SNEAKY = "-T1"
    POLITE = "-T2"
    NORMAL = "-T3"
    AGGRESSIVE = "-T4"
    INSANE = "-T5"
