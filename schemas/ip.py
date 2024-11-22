from ipaddress import IPv4Address, IPv4Network

from schemas.base import BaseSchema


class OneIP(BaseSchema):
    ip: IPv4Address


class OneDomain(BaseSchema):
    doamin: IPv4Address


class CIDRNotation(BaseSchema):
    cidr: IPv4Network
