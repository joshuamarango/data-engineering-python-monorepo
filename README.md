# data-engineering-python-monorepo
Template for setting up data engineering monorepo for IaC, Data Products, Data Pipelines &amp; Data Modelling.

## Getting Started

### Setting up your environment with uv

This repository uses [uv](https://github.com/astral-sh/uv) for Python package management. uv is a fast, reliable Python package installer and resolver that serves as a replacement for pip and virtualenv.

#### 1. Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Create and sync the virtual environment

Once uv is installed, run the following commands in the root directory of this repository to create a virtual environment and install all dependencies:

```bash
# Create a virtual environment and sync all packages
uv sync --all-packages

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows
```

The `uv sync` command will:
- Create a virtual environment in the `.venv` directory if it doesn't exist
- Install all packages specified in your requirements files
- Ensure all dependencies are compatible

#### 3. Verify your environment

After activating the virtual environment, you can verify that everything is set up correctly:

```bash
python -c "import sys; print(f'Using Python {sys.version} from {sys.executable}')"
```

You should see output indicating that Python is running from the `.venv` directory.


