import pandas as pd
from pathlib import Path

def read_table(path: Path, **kwargs) -> pd.DataFrame:
    ext = path.suffix.lower()
    if ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        return pd.read_csv(path, sep=sep, encoding=kwargs.get("encoding", "utf-8"))
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=kwargs.get("sheet", 0))
    elif ext == ".json":
        return pd.read_json(path)
    elif ext == ".html":
        tables = pd.read_html(path)
        if not tables:
            raise ValueError("В HTML не найдено таблиц")
        return tables[0]
    raise ValueError(f"Чтение {ext} не поддерживается.")

def write_table(df: pd.DataFrame, path: Path, **kwargs) -> None:
    ext = path.suffix.lower()
    if ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        df.to_csv(path, sep=sep, index=False, encoding=kwargs.get("encoding", "utf-8"))
    elif ext == ".xlsx":
        df.to_excel(path, index=False)
    elif ext == ".json":
        df.to_json(path, orient="records", force_ascii=False, indent=2)
    elif ext == ".html":
        df.to_html(path, index=False)
    else:
        raise ValueError(f"Запись {ext} не поддерживается.")