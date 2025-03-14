"""
pypdf is the original.
PyPDF2 is a very good fork that was recently merged back into pypdf.
PyPDF3 and PyPDF4 are both bad forks. TLDR; use pypdf.
"""

from pathlib import Path
from typing import List

from pypdf import PdfReader, PdfWriter


def split_pdf():
    with open("input.pdf", "rb") as infile:
        infile = open(r"input.pdf", "rb")
        reader = PdfReader(infile)

    for idx, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[idx])
        with open(rf"{idx + 1}.pdf", "wb") as f:
            writer.write(f)


def combine_pdf(combined_file_name: str, infiles: List[str]):
    infiles = sorted(infiles, key=lambda infile: int(Path(infile).name.split(".")[0]))
    writer = PdfWriter()
    for infile in infiles:
        writer.add_page(PdfReader(infile).pages[0])
    with open(combined_file_name, "wb") as f:
        writer.write(f)
