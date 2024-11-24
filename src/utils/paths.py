from pathlib import Path


XML_DIR_PATH = (Path(__file__).parent.parent / "static" / "xml").resolve()


def xml_template(filename: str) -> str:
    return str((XML_DIR_PATH / filename).resolve())
