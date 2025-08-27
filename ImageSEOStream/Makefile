.PHONY: help install run test clean deploy docker-build docker-run

# Default target
help:
	@echo "ImgSage - Advanced AI Image Analyzer & SEO Optimizer"
	@echo ""
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  run         - Run the application locally"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean temporary files"
	@echo "  deploy      - Deploy to Render"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run the application locally
run:
	@echo "🚀 Starting ImgSage..."
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	rm -rf temp_input/
	rm -rf processed_images/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .streamlit/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Deploy to Render
deploy:
	@echo "🚀 Deploying to Render..."
	@echo "Make sure you have:"
	@echo "1. Connected your GitHub repository to Render"
	@echo "2. Set the OPENAI_API_KEY environment variable"
	@echo "3. Configured the build and start commands"
	git push origin main

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t imagesage .

# Run Docker container
docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8501:8501 -e OPENAI_API_KEY="your-api-key-here" imagesage

# Development setup
dev-setup: install
	@echo "🔧 Setting up development environment..."
	@echo "✅ Development environment ready!"
	@echo "Run 'make run' to start the application"

# Production setup
prod-setup: install
	@echo "🔧 Setting up production environment..."
	@echo "✅ Production environment ready!"
	@echo "Set OPENAI_API_KEY environment variable before running"
