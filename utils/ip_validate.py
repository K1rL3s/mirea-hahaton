import re
from ipaddress import IPv4Address, IPv4Network, IPv6Address

ipv4_cidr_regex = re.compile(
    r"^([0-9]{1,3}\.){3}[0-9]{1,3}(/([0-9]|[1-2][0-9]|3[0-2]))?$",
)
ipv4_regex = re.compile(
    r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$",
)
ipv6_regex = re.compile(
    r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$",
)


def convert_ip(
    ip: str,
) -> IPv4Address | IPv6Address | tuple[IPv4Address, IPv4Address] | IPv4Network | None:
    if match := ipv4_cidr_regex.match(ip):
        return IPv4Network(match.group(), strict=False)
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
    return None
