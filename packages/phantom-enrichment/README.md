# Project Structure

```
phantom-enrichment/
├── phantom_enrichment/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── orchestrator.py
│   ├── datasources/
│   │   ├── __init__.py
│   │   └── excel_handler.py
│   ├── enrichment/
│   │   ├── __init__.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   └── hardcover/
│   │       ├── __init__.py
│   │       └── client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── book.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging_config.py
│   │   └── exceptions.py
│   └── main.py
├── tests/
│   └── # (Test files will go here later)
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Setup

### 1. Installing Poetry

`pipx` is a tool to install and run Python applications in isolated environments. It's the preferred way to install tools like Poetry globally.

Install `pipx`:

```Bash
pip install --user pipx
```

Add `pipx` to `PATH`:

```Bash
python -m pipx ensurepath
```

Install Poetry using `pipx`:

```Bash
pipx install poetry
```

Confirm version:

```Bash
poetry --version
```

### 2. Setting Up Environment

Head to project directory:

```Bash
cd path/to/phantom-enrichment
```

Install dependencies using Poetry:

```Bash
poetry install
```

Activate virtual environment:

```Bash
poetry env activate
```

## Execution

### 1. Test Runs

To execute, follow the steps below:

1. Place your Excel file (e.g., `my_books.xlsx`) containing at least Title and Author columns inside the input directory.
2. Ensure the output and log directories exist (default: `./output`, `./logs`). The app will create them if they don't, but it's good practice.
3. Make sure your Poetry virtual environment is active (`poetry shell` or execute `poetry env activate` command).
4. Execute the CLI command from your project root directory.

```Bash
# Example using default provider (isbndb) and default sheet (0)
poetry run phantom-enrichment enrich books --input my_books.xlsx

# Example specifying output filename and sheet name
poetry run phantom-enrichment enrich books -i my_books.xlsx -o enriched_editions.xlsx --sheet "MasterList"

# Example using an absolute path for input
poetry run phantom-enrichment enrich books -i "/path/to/your/library.xlsx"
```

5. Look for the generated Excel file (e.g., `my_books_enriched.xlsx` or `enriched_editions.xlsx`) in your output directory.
6. Examine the console output and the log file (e.g., `logs/phantom_enrichment.log`) for detailed progress, warnings, and errors.