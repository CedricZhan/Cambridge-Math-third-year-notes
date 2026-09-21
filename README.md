# Cedric Zhan's Third-Year Mathematics Notes

This repository contains the LaTeX sources, compiled PDFs, and static website for Cedric Zhan's third-year mathematics lecture notes.

## Editing and compiling notes

Course sources live in `tex/`. Edit the matching `.tex` file, then compile every course from PowerShell:

```powershell
.\scripts\compile-notes.ps1
```

The generated PDFs are written to `dist/pdfs/`, where the website links to them.

## Previewing the website

Serve the `dist/` directory with any static web server. For example:

```powershell
python -m http.server 4173 --directory dist
```

Then open `http://localhost:4173`.
