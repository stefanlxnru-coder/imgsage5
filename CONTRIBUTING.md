# 🤝 Contributing to ImgSage

Thank you for your interest in contributing to ImgSage! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs

- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide system information
- Include error messages and logs
- Check if the issue has already been reported

### 💡 Suggesting Enhancements

- Use the GitHub issue tracker
- Describe the feature clearly
- Explain why this feature would be useful
- Include mockups if applicable

### 🔧 Pull Requests

- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Update documentation
- Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- OpenAI API key (for testing)

### Local Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/imagesage.git
   cd imagesage
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

5. **Run the application**
   ```bash
   python start.py
   # or
   streamlit run ImageSEOStream/app.py
   ```

### Development Dependencies

For development, install additional tools:

```bash
pip install black flake8 mypy pytest
```

## 📝 Coding Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Keep functions small and focused
- Write descriptive variable names
- Add docstrings to functions and classes

### Code Formatting

We use `black` for code formatting:

```bash
black ImageSEOStream/
```

### Linting

We use `flake8` for linting:

```bash
flake8 ImageSEOStream/
```

### Type Checking

We use `mypy` for type checking:

```bash
mypy ImageSEOStream/
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python ImageSEOStream/test_app.py

# Run with pytest (if installed)
pytest ImageSEOStream/
```

### Writing Tests

- Write tests for new features
- Ensure good test coverage
- Use descriptive test names
- Mock external dependencies

### Test Structure

```python
def test_feature_name():
    """Test description"""
    # Arrange
    # Act
    # Assert
```

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure your code follows standards**
   - Run `black` for formatting
   - Run `flake8` for linting
   - Run `mypy` for type checking
   - Run tests to ensure they pass

2. **Update documentation**
   - Update README if needed
   - Add docstrings to new functions
   - Update CHANGELOG.md

3. **Test your changes**
   - Test locally
   - Ensure no regressions
   - Test edge cases

### Pull Request Guidelines

1. **Create a descriptive title**
   - Use present tense
   - Be specific about the change

2. **Write a detailed description**
   - Explain what the PR does
   - Link to related issues
   - Include screenshots if UI changes

3. **Keep PRs focused**
   - One feature per PR
   - Keep changes small and manageable
   - Break large changes into multiple PRs

### Review Process

1. **Automated checks must pass**
   - Code formatting
   - Linting
   - Type checking
   - Tests

2. **Code review**
   - At least one approval required
   - Address review comments
   - Update PR as needed

3. **Merge**
   - Squash commits if needed
   - Use conventional commit messages

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 10, macOS 12.0]
 - Python Version: [e.g. 3.11.0]
 - Browser: [e.g. Chrome 120.0]

**Additional context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 📚 Documentation

### Code Documentation

- Use docstrings for all functions and classes
- Follow Google docstring format
- Include type hints
- Provide examples for complex functions

### User Documentation

- Keep README.md up to date
- Update DEPLOYMENT.md for deployment changes
- Add inline comments for complex logic
- Create tutorials for new features

## 🔒 Security

### Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Follow security best practices
- Report security issues privately

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do not** create a public issue
2. Email the maintainers privately
3. Provide detailed information
4. Allow time for response and fix

## 🎯 Getting Help

### Questions and Support

- Check existing issues and discussions
- Search documentation
- Ask in GitHub Discussions
- Create an issue for bugs

### Community Guidelines

- Be respectful and inclusive
- Help others when possible
- Follow the code of conduct
- Provide constructive feedback

## 🙏 Acknowledgments

Thank you to all contributors who have helped make ImgSage better!

---

**Happy Contributing! 🚀**
