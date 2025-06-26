.PHONY: help dev-frontend dev-backend dev

# Default model provider (can be overridden with MODEL=ollama)
MODEL ?= gemini

help:
	@echo "Available commands:"
	@echo "  make dev-frontend              - Starts the frontend development server (Vite)"
	@echo "  make dev-backend [MODEL=...]   - Starts the backend development server"
	@echo "  make dev [MODEL=...]           - Starts both frontend and backend development servers"
	@echo ""
	@echo "MODEL options:"
	@echo "  gemini  - Use Google Gemini models (default)"
	@echo "  ollama  - Use local Ollama/Llama3.2 models"
	@echo ""
	@echo "Examples:"
	@echo "  make dev MODEL=gemini"
	@echo "  make dev MODEL=ollama"

dev-frontend:
	@echo "Starting frontend development server..."
	@cd frontend && npm run dev

dev-backend:
	@echo "Starting backend development server with MODEL=$(MODEL)..."
	@cd backend && MODEL_PROVIDER=$(MODEL) langgraph dev

# Run frontend and backend concurrently
dev:
	@echo "Starting both frontend and backend development servers with MODEL=$(MODEL)..."
	@make dev-frontend & make dev-backend MODEL=$(MODEL) 