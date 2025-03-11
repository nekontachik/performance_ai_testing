# Contributing to AI API Load Testing

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure your API keys in the `.env` file:
```bash
cp .env.example .env
# Edit the .env file with your API keys
```

## Testing

Before submitting a pull request, please make sure your changes pass all tests:

```bash
cd locustfiles
python verify_api_keys.py
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if needed
3. The pull request will be merged once it has been reviewed and approved

## Style Guide

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments to explain complex code
- Keep functions small and focused on a single task

## Security

- Never commit API keys or other sensitive information
- Use environment variables for sensitive information
- Always use the `.env.example` file for placeholder values

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license. 