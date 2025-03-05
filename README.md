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

## Development Workflow

### Setting up Pre-commit Hooks with Commitizen

This repository uses [Commitizen](https://commitizen-tools.github.io/commitizen/) to standardize commit messages and [pre-commit](https://pre-commit.com/) to enforce code quality checks before commits.

#### 1. Install pre-commit and Commitizen

With your virtual environment activated, install pre-commit and Commitizen:

```bash
uv pip install pre-commit commitizen
```

#### 2. Create a pre-commit configuration file

Create a `.pre-commit-config.yaml` file in the root of the repository:

```bash
touch .pre-commit-config.yaml
```

#### 3. Configure pre-commit with Commitizen

Add the following content to the `.pre-commit-config.yaml` file:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/commitizen-tools/commitizen
    rev: v3.5.3
    hooks:
    -   id: commitizen
        stages: [commit-msg]
```

#### 4. Create a Commitizen configuration

Create a `.cz.toml` file in the root of the repository to configure Commitizen:

```bash
touch .cz.toml
```

Add the following content to the `.cz.toml` file:

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
```

#### 5. Install the pre-commit hooks

Install the pre-commit hooks with:

```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

#### 6. Using Commitizen for commits

Now, instead of using `git commit` directly, you can use:

```bash
cz commit
```

This will guide you through creating a standardized commit message. Alternatively, if you use `git commit`, the pre-commit hook will validate your commit message against the Commitizen format.

The conventional commit format follows this pattern:
```
type(scope): subject

body

footer
```

Where `type` is one of:
- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- perf: Performance improvements
- test: Adding or modifying tests
- build: Changes to build system
- ci: Changes to CI configuration
- chore: Other changes that don't modify src or test files
