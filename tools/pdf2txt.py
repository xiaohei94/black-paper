#!/usr/bin/env python3
"""
PDF to TXT Converter

Recursively converts PDF files to UTF-8 encoded text files using pdfminer.six.
Designed for the black-paper repository to enable AI assistants to read papers.

Usage:
    python tools/pdf2txt.py [folders...]
    
    If no folders specified, defaults to "main paper" and "branch paper"
    
Examples:
    python tools/pdf2txt.py
    python tools/pdf2txt.py "main paper" "branch paper"
    python tools/pdf2txt.py .
"""

import os
import sys
from pathlib import Path
from io import StringIO

try:
    from pdfminer.high_level import extract_text_to_fp
    from pdfminer.layout import LAParams
except ImportError:
    print("ERROR: pdfminer.six is not installed. Install with: pip install pdfminer.six", file=sys.stderr)
    sys.exit(1)


def normalize_text(text):
    """
    Normalize text by:
    - Converting line endings to Unix style (\n)
    - Stripping trailing whitespace from each line
    - Ensuring file ends with single newline
    """
    lines = text.splitlines()
    normalized_lines = [line.rstrip() for line in lines]
    # Remove trailing empty lines
    while normalized_lines and not normalized_lines[-1]:
        normalized_lines.pop()
    # Join with newline and add final newline
    return '\n'.join(normalized_lines) + '\n' if normalized_lines else ''


def convert_pdf_to_txt(pdf_path):
    """
    Convert a single PDF file to UTF-8 text.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        tuple: (success: bool, message: str)
    """
    txt_path = pdf_path.with_suffix('.txt')
    
    try:
        # Use StringIO to capture text output
        output = StringIO()
        
        # Configure LAParams for better text extraction
        # These parameters help maintain logical reading order
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5,
            detect_vertical=False,
            all_texts=False
        )
        
        # Extract text from PDF
        with open(pdf_path, 'rb') as pdf_file:
            extract_text_to_fp(pdf_file, output, laparams=laparams, output_type='text')
        
        # Get the extracted text
        text = output.getvalue()
        
        if not text.strip():
            return False, "Empty text extracted"
        
        # Normalize the text
        normalized_text = normalize_text(text)
        
        # Write to UTF-8 text file
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(normalized_text)
        
        return True, f"Converted successfully ({len(normalized_text)} bytes)"
        
    except Exception as e:
        return False, f"Error: {type(e).__name__}: {str(e)}"


def find_pdfs(folders):
    """
    Recursively find all PDF files in the given folders.
    
    Args:
        folders: List of folder paths to search
        
    Yields:
        Path objects for each PDF file found
    """
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"WARNING: Folder not found: {folder}", file=sys.stderr)
            continue
        
        if not folder_path.is_dir():
            print(f"WARNING: Not a directory: {folder}", file=sys.stderr)
            continue
        
        # Recursively find all PDF files
        for pdf_path in folder_path.rglob('*.pdf'):
            if pdf_path.is_file():
                yield pdf_path


def main():
    """Main entry point for the PDF to TXT converter."""
    
    # Determine which folders to process
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
    else:
        # Default folders
        folders = ["main paper", "branch paper"]
    
    print(f"PDF to TXT Converter")
    print(f"Searching for PDFs in: {', '.join(repr(f) for f in folders)}")
    print()
    
    # Find all PDFs
    pdf_files = list(find_pdfs(folders))
    
    if not pdf_files:
        print("No PDF files found.")
        return 0
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    print()
    
    # Convert each PDF
    success_count = 0
    error_count = 0
    
    for pdf_path in sorted(pdf_files):
        # Display relative path for readability
        try:
            display_path = pdf_path.relative_to(Path.cwd())
        except ValueError:
            display_path = pdf_path
        
        success, message = convert_pdf_to_txt(pdf_path)
        
        if success:
            status = "[OK]"
            success_count += 1
        else:
            status = "[ERR]"
            error_count += 1
        
        print(f"{status} {display_path}")
        if not success:
            print(f"     {message}")
    
    # Summary
    print()
    print(f"Conversion complete: {success_count} successful, {error_count} failed")
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
