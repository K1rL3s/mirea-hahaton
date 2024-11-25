from io import BytesIO

import aiohttp
import pandas as pd
import sqlalchemy
from dishka import AsyncContainer
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import VulnerabilityModel

DBU_XLSX_URL = "https://bdu.fstec.ru/files/documents/vullist.xlsx"


async def get_xlsx(url: str) -> BytesIO:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            response.raise_for_status()
            content = await response.read()
            return BytesIO(content)


async def parse_xlsx_to_models(xlsx_buffer: BytesIO) -> list[VulnerabilityModel]:
    df = pd.read_excel(xlsx_buffer, skiprows=2)

    vulnerabilities = []
    for _, row in df.iterrows():
        vulnerability = VulnerabilityModel(
            id=str(row["Идентификатор"]),
            name=row["Наименование уязвимости"],
            description=row["Описание уязвимости"],
            vendor=row["Вендор ПО"],
            soft_name=row["Название ПО"],
            version=row["Версия ПО"],
            type=row["Тип ПО"],
            os=row["Наименование ОС и тип аппаратной платформы"],
            class_=row["Класс уязвимости"],
            date=str(row["Дата выявления"]),
            cvss2=str(row["CVSS 2.0"]),
            cvss3=str(row["CVSS 3.0"]),
            danger_level=row["Уровень опасности уязвимости"],
            elimination_methods=row["Возможные меры по устранению"],
            status=row["Статус уязвимости"],
            is_exploitation=row["Наличие эксплойта"],
            elimination_info=row["Информация об устранении"],
            urls=row["Ссылки на источники"],
            other_id=row["Идентификаторы других систем описаний уязвимости"],
            other_info=row["Прочая информация"],
            realtions=row["Связь с инцидентами ИБ"],
            method_exploitation=row["Способ эксплуатации"],
            method_fix=row["Способ устранения"],
            cwe_description=row["Описание ошибки CWE"],
            cwe_type=row["Тип ошибки CWE"],
        )
        vulnerabilities.append(vulnerability)

    max_length = 1024
    for vulnerability in vulnerabilities:
        for attr, value in vulnerability.__dict__.items():
            if isinstance(value, str) and len(value) > max_length:
                # Обрезаем поле до допустимой длины
                setattr(vulnerability, attr, value[:max_length])

    return vulnerabilities


async def save_vulnerabilities_to_db(
    vulnerabilities: list[VulnerabilityModel],
    session: AsyncSession,
) -> None:
    async with session.begin():
        await session.execute(sqlalchemy.delete(VulnerabilityModel))
        session.add_all(vulnerabilities)


async def process_vulnerabilities(
    container: AsyncContainer,
    url: str = DBU_XLSX_URL,
) -> list[VulnerabilityModel]:
    async with container() as request_container:
        session = await request_container.get(AsyncSession)
        xlsx_buffer = await get_xlsx(url)
        vulnerabilities = await parse_xlsx_to_models(xlsx_buffer)
        await save_vulnerabilities_to_db(vulnerabilities, session)
        return vulnerabilities
