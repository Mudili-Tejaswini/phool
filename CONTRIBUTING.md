# Contributing to Phool Intelligence

Thank you for your interest in contributing! This document outlines the process for submitting changes.

---

## Getting Started

1. **Fork** the repository and clone your fork locally.
2. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Development Workflow

### Running tests
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

All tests must pass before opening a pull request.

### Code style
- Follow [PEP 8](https://pep8.org/).
- Use type hints in all function signatures.
- Add docstrings to every public function and class.

### Adding a new model
1. Add the model to `MODELS` dict in `src/model.py`.
2. Add corresponding tests in `tests/test_model.py`.
3. Update `README.md` with the new model's metrics.

### Adding a new data attribute
1. Update the encoding maps in `src/features.py`.
2. Update `FIELDNAMES` in `scripts/scrape.py`.
3. Add standardization logic in `scripts/preprocess.py`.
4. Update the advisor form in the HTML dashboard.

---

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR.
- Write a clear title and description.
- Reference any related issues with `Fixes #123`.
- Ensure CI checks pass before requesting review.

---

## Reporting Issues

Please open a GitHub Issue with:
- A clear title describing the problem
- Steps to reproduce
- Expected vs actual behaviour
- Python version and OS

---

## Code of Conduct

Be respectful, constructive, and collaborative. All contributors are expected to maintain a welcoming environment for everyone.
