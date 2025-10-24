# PDF to TXT Conversion Tools

This directory contains tools for converting PDF research papers to UTF-8 text format, enabling AI assistants to read and analyze papers in this repository.

## `pdf2txt.py`

Recursively converts PDF files to UTF-8 encoded text files using `pdfminer.six`.

### Usage

```bash
# Convert PDFs in default folders ("main paper" and "branch paper")
python tools/pdf2txt.py

# Convert PDFs in specific folders
python tools/pdf2txt.py "main paper" "branch paper"

# Convert PDFs in current directory
python tools/pdf2txt.py .
```

### Requirements

- Python 3.11+
- pdfminer.six

Install dependencies:
```bash
pip install pdfminer.six
```

### Features

- Recursively finds all PDF files in specified folders
- Converts each PDF to a UTF-8 `.txt` file with the same basename
- Normalizes line endings (Unix style) and strips trailing spaces
- Preserves logical reading order as best as pdfminer allows
- Resilient to errors: continues on failures and prints diagnostics
- Outputs `[OK]` or `[ERR]` status for each file

### Automatic Conversion

The GitHub Actions workflow `.github/workflows/pdf2txt.yml` automatically runs this script when:
- A new or updated PDF is pushed to `main paper/` or `branch paper/` folders
- The workflow is manually triggered via workflow_dispatch

The workflow automatically commits any new or changed `.txt` files back to the repository.
