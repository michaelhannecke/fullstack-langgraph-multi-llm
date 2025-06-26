# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a fullstack application demonstrating LangGraph-powered AI research agent with:
- **Frontend**: React + Vite + TypeScript with Tailwind CSS and Shadcn UI components
- **Backend**: LangGraph agent using Google Gemini models for web research with citations
- **Architecture**: Agent performs iterative web research through query generation, web search, reflection, and answer synthesis

## Development Commands

### Starting Development Servers
```bash
# Run both frontend and backend with different model providers
make dev                    # Uses Google Gemini models (default)
make dev MODEL=ollama      # Uses local Ollama/Llama3.2 models
make dev MODEL=gemini      # Explicitly use Gemini models

# Run individually
make dev-frontend          # Starts Vite dev server on localhost:5173
make dev-backend           # Starts LangGraph dev server on localhost:2024
make dev-backend MODEL=ollama  # Backend with Ollama models
```

### Frontend Commands
```bash
cd frontend
npm install          # Install dependencies
npm run dev         # Start development server
npm run build       # Build for production (TypeScript + Vite)
npm run lint        # Run ESLint
npm run preview     # Preview production build
```

### Backend Commands
```bash
cd backend
pip install .       # Install Python dependencies
langgraph dev       # Start LangGraph development server
python examples/cli_research.py "question"  # Run CLI research example
```

### Linting and Type Checking
- **Frontend**: `npm run lint` (ESLint with TypeScript rules)
- **Backend**: Uses `ruff` for linting and `mypy` for type checking (configured in pyproject.toml)

## Architecture Overview

### Backend Agent Flow (LangGraph)
The research agent in `backend/src/agent/graph.py` follows this workflow:
1. **Query Generation**: Generate initial search queries from user input
2. **Web Research**: Execute parallel web searches using Google Search API
3. **Reflection**: Analyze results to identify knowledge gaps
4. **Iterative Refinement**: Generate follow-up queries if needed (configurable max loops)
5. **Answer Synthesis**: Combine research into final answer with citations

### Key Backend Components
- `graph.py`: Main LangGraph state machine with nodes and edges
- `state.py`: TypedDict state definitions for different graph phases
- `tools_and_schemas.py`: Pydantic schemas for structured outputs
- `prompts.py`: Prompt templates for different agent phases
- `app.py`: FastAPI server that serves both API and frontend static files
- `langgraph.json`: LangGraph configuration file

### Frontend Architecture
- **App.tsx**: Main component using `@langchain/langgraph-sdk/react` for streaming
- **Components**: Modular UI components in `src/components/`
- **Streaming**: Real-time updates from LangGraph backend via WebSocket-like streaming
- **Activity Timeline**: Visual representation of agent progress through research phases

### Configuration
- **Environment**: Backend requires `GEMINI_API_KEY` in `secrets/.env` file
- **API URLs**: Frontend automatically switches between dev (localhost:2024) and prod (localhost:8123)
- **Agent Configuration**: Configurable via `Configuration` class in `configuration.py`

### Model Providers
The system supports two LLM providers:

**Google Gemini (default)**:
- Uses Google Gemini models for all text generation
- Integrated Google Search API with grounding metadata for citations
- Models: `gemini-2.0-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`

**Ollama (local)**:
- Uses local Ollama/Llama3.2 models for text generation
- Still uses Google Search API for web research (only available through Google)
- Requires Ollama server running on `http://localhost:11434`
- Model: `llama3.2:latest`

**Important**: Web research always uses Google Search API regardless of model provider, as this functionality is only available through Google's ecosystem.

### Docker Deployment
- Uses multi-stage build combining frontend build with backend server
- Requires Redis and Postgres for production LangGraph deployment
- Frontend served at `/app/` route to avoid conflicts with LangGraph API routes

## Key Patterns

### State Management
- LangGraph uses TypedDict-based state that flows through graph nodes
- Frontend uses React hooks for local state and streaming integration
- Agent state includes research loop counting and configurable parameters

### Error Handling
- Backend uses structured outputs with retry logic for LLM calls
- Frontend displays error states and provides retry mechanisms
- Graceful degradation when frontend build is missing

### Citation System
- Web research results include grounding metadata from Google Search
- URLs are shortened for token efficiency then restored in final output
- Citations are embedded in markdown format within agent responses