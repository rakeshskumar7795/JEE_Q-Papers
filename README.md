# JEE Previous Year Papers Dashboard (2007-2025)

A Streamlit app that shows every PDF in the `papers/` folder on one page,
grouped by year, with search, filters, an in-app PDF viewer and downloads.

## Project structure

```
jee_dashboard/
  app.py                  Main Streamlit app
  utils/scanner.py        Finds PDFs, reads year/exam/paper/shift from names
  utils/pdf_view.py       PDF viewer popup + file reading
  .streamlit/config.toml  Theme and server settings
  papers/                 <-- put your PDFs here
  requirements.txt
  run.bat                 Windows: double-click to install and start
  start_dashboard.vbs     Windows: start in the background (no console window)
  stop_dashboard.bat      Windows: stop the background dashboard
```

## Quick start (Windows, no typing)

1. Copy your PDFs into the `papers` folder.
2. Double-click `run.bat` (first time installs the packages, then starts the app).
3. The dashboard opens at http://localhost:8501.

Later you can use `start_dashboard.vbs` to start it with no black window, and
`stop_dashboard.bat` to stop it.

## Run from a terminal instead

```
cd path\to\jee_dashboard
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Adding papers

Copy the PDFs into `papers/` (sub-folders are fine). The year is read from
the file name or folder name, for example:

- `JEE_Advanced_2015_Paper1.pdf`
- `2012/Paper-2.pdf`
- `jee-main-2019-april-9-shift-1.pdf`

Files with no 4-digit year go under "Other". Detected automatically:
`advanced`, `main`, `paper 1/2`, `shift 1/2`, `solution` / `answer` / `key`.

New files appear after a browser refresh, or click "Rescan papers folder"
in the sidebar. The page also lists any years in 2007-2025 with no files yet.
