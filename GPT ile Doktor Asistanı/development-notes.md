# Virtual Environment Setup (.venv)

This project uses a virtual environment to isolate all Python dependencies from the global system environment. It ensures consistent package management across different development machines.

## 1. Requirements

Before creating the environment, make sure that:
- Python 3.8 or higher is installed
- Pip is available
- You are working inside the project root directory

## 2. Create the Virtual Environment

Use one of the following commands depending on your operating system:

### Windows (PowerShell)
```powershell
python -m venv .venv
```

### macOS / Linux (Bash)
```bash
python3 -m venv .venv
```

## 3. Activate the Virtual Environment

### Windows (PowerShell)
```powershell
.venv\Scripts\Activate
```

### macOS / Linux (Bash)
```bash
source .venv/bin/activate
```

## 4. Install Project Dependencies

If a `requirements.txt` file exists, install the necessary packages using:

```bash
pip install -r requirements.txt
```

## 5. Deactivate the Virtual Environment

When you finish working, deactivate the environment:

```bash
deactivate
```

## 6. Update Dependencies

If packages change, update the requirements file:

```bash
pip freeze > requirements.txt
```

## Note

**Do not push the `.venv/` folder to version control.** Add the following line to `.gitignore`:

```
.venv/
```


---

uvicorn doctor_assistant_api:app --reload

