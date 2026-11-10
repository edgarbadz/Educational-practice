from pathlib import Path
from docx import Document

def convert_docx_simple(src_path: Path, dst_path: Path):
    try:
        doc = Document(src_path)
    except Exception:
        raise ValueError("Не удалось прочитать документ. Возможно, файл поврежден.")

    text_paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

    ext = dst_path.suffix.lower()
    
    if ext == ".txt":
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write("\n".join(text_paragraphs))
            
    elif ext == ".docx":
        new_doc = Document()
        for p_text in text_paragraphs:
            new_doc.add_paragraph(p_text)
        new_doc.save(dst_path)
        
    else:
        raise ValueError(f"Запись в {ext} на данном этапе не поддерживается.")
