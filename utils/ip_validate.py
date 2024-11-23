import re
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

ipv4_cidr_regex = re.compile(
    r"^([0-9]{1,3}\.){3}[0-9]{1,3}(/([0-9]|[1-2][0-9]|3[0-2]))?$",
)
ipv4_regex = re.compile(
    r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$",
)
ipv6_regex = re.compile(
    r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$",
)
ipv6_cidr_regex = re.compile(
    r"^(?:(?:(?:[A-F0-9]{1,4}:){6}|(?=(?:[A-F0-9]{0,4}:){0,6}(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![:.\w]))(([0-9A-F]{1,4}:){0,5}|:)((:[0-9A-F]{1,4}){1,5}:|:)|::(?:[A-F0-9]{1,4}:){5})(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}|(?=(?:[A-F0-9]{0,4}:){0,7}[A-F0-9]{0,4}(?![:.\w]))(([0-9A-F]{1,4}:){1,7}|:)((:[0-9A-F]{1,4}){1,7}|:)|(?:[A-F0-9]{1,4}:){7}:|:(:[A-F0-9]{1,4}){7})(?![:.\w])\/(?:12[0-8]|1[01][0-9]|[1-9]?[0-9])$",
)


def convert_ip(
    ip: str,
) -> (
    IPv4Address
    | IPv6Address
    | IPv4Network
    | IPv6Network
    | tuple[IPv4Address, IPv4Address]
    | list[IPv4Address]
    | list[IPv6Address]
    | None
):
    if match := ipv4_cidr_regex.match(ip):
        return IPv4Network(match.group(), strict=False)
    if match := ipv6_cidr_regex.match(ip):
        return IPv6Network(match.group(), strict=False)
    if match := ipv4_regex.match(ip):
        return IPv4Address(match[0])
    if (
        (len(ips := ip.split(":")) == 2)
        and (left_match := ipv4_regex.match(ips[0]))
        and (right_match := ipv4_regex.match(ips[1]))
    ):
        return IPv4Address(left_match[0]), IPv4Address(right_match[0])
    if match := ipv6_regex.match(ip):
        return IPv6Address(match.group())
    if (len(ips := ip.split(","))) > 1 and all(ipv4_regex.match(ip) for ip in ips):
        return [IPv4Address(ipv4_regex.match(ip)[0]) for ip in ips]
    if (len(ips := ip.split(","))) > 1 and all(ipv6_regex.match(ip) for ip in ips):
        return [IPv6Address(ipv4_regex.match(ip)[0]) for ip in ips]
    return None
