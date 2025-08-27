.PHONY: help install test lint format clean build deploy run dev

# Default target
help:
	@echo "🎯 ImgSage - Available Commands"
	@echo "================================"
	@echo "install    - Install dependencies"
	@echo "test       - Run tests"
	@echo "lint       - Run linting checks"
	@echo "format     - Format code with Black"
	@echo "clean      - Clean up temporary files"
	@echo "build      - Build the application"
	@echo "deploy     - Deploy to production"
	@echo "run        - Run the application locally"
	@echo "dev        - Run in development mode"
	@echo "docker     - Build and run with Docker"
	@echo "security   - Run security checks"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .[dev]

# Run tests
test:
	@echo "🧪 Running tests..."
	python ImageSEOStream/test_app.py
	pytest ImageSEOStream/ -v --cov=ImageSEOStream --cov-report=html

# Run linting
lint:
	@echo "🔍 Running linting checks..."
	flake8 ImageSEOStream/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 ImageSEOStream/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	mypy ImageSEOStream/ --ignore-missing-imports

# Format code
format:
	@echo "🎨 Formatting code..."
	black ImageSEOStream/
	isort ImageSEOStream/

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf temp_input/
	rm -rf processed_images/
	rm -f *.zip

# Build application
build:
	@echo "🔨 Building application..."
	python -m build

# Deploy to production
deploy:
	@echo "🚀 Deploying to production..."
	@echo "Please configure your deployment platform (Render, Heroku, etc.)"
	@echo "See DEPLOYMENT.md for detailed instructions"

# Run locally
run:
	@echo "🏃 Running ImgSage locally..."
	python start.py

# Development mode
dev:
	@echo "🔧 Running in development mode..."
	streamlit run ImageSEOStream/app.py --server.port=8501 --server.address=localhost

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t imagesage:latest .

docker-run:
	@echo "🐳 Running with Docker..."
	docker run -p 8501:8501 -e OPENAI_API_KEY="your-api-key" imagesage:latest

docker: docker-build docker-run

# Security checks
security:
	@echo "🔒 Running security checks..."
	bandit -r ImageSEOStream/ -f json -o bandit-report.json
	safety check

# Full development workflow
dev-setup: install format lint test
	@echo "✅ Development environment setup complete!"

# Pre-commit checks
pre-commit: format lint test
	@echo "✅ Pre-commit checks passed!"

# Release preparation
release: clean format lint test security build
	@echo "✅ Release preparation complete!"
