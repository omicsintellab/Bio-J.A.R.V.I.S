# Contributing to BIO - J.A.R.V.I.S

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to BIO - J.A.R.V.I.S. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for BIO - J.A.R.V.I.S. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- **Use the GitHub Issues search** — check if the issue has already been reported.
- **Check if the issue has been fixed** — try to reproduce it using the latest `main` or development branch in the repository.
- **Isolate the problem** — ideally create a reduced test case.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for BIO - J.A.R.V.I.S, including completely new features and minor improvements to existing functionality.

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as much detail as possible.
- **Explain why this enhancement would be useful** to most BIO - J.A.R.V.I.S users.

### Pull Requests

*   Fill in the required template
*   Do not include issue numbers in the PR title
*   Include screenshots and animated GIFs in your pull request whenever possible.
*   Follow the Python style guides (PEP 8).
*   Include new tests that cover your changes if applicable.
*   Ensure the test suite passes (`pytest`).

## Development Setup

1.  **Clone the repo** and create a branch from `main`.
2.  **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run tests**:
    ```bash
    pytest
    ```
