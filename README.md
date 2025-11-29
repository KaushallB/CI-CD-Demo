This repository showcases the CI/CD pipelines and automated testing infrastructure implemented for WealthWise (https://wealthwisee.me), a personal finance management platform.

Note: The actual WealthWise application runs from a private repository directly connected to Render for production deployments. This repository contains the same workflow files and test structure for **learning and demonstration purposes**.

## Overview

- **Automated Testing:** Comprehensive test suite using `pytest` for unit and integration tests.
- **CI/CD Workflows:** GitHub Actions workflows for automated testing, code quality, and security scanning on every push and pull request.
- **Security:** Integration of static analysis and dependency vulnerability checks.


## Features

- Flask application structure  based on my project Wealtwisee
- Test files covering forms, routes, security, and helpers
- GitHub Actions workflows for:
  - Running tests and linting
  - Security scanning (Bandit, Safety)
  - Code quality checks
  - Automatic Deloyment
- Template for environment variable management

