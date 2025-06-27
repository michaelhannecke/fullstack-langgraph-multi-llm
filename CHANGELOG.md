# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Multi-LLM Provider Support**: Added support for choosing between Google Gemini and local Ollama/Llama3.2 models
  - New `MODEL` parameter for Makefile: `make dev MODEL=gemini` or `make dev MODEL=ollama`
  - Automatic model provider detection and configuration
  - LLM factory pattern for clean provider abstraction

- **Enhanced Configuration System**:
  - Added `model_provider` field to Configuration class (`gemini` or `ollama`)
  - Added `ollama_base_url` configuration option (defaults to `http://localhost:11434`)
  - Added `get_models_for_provider()` method for dynamic model mapping
  - Environment variable support for `MODEL_PROVIDER`

- **New LLM Factory** (`backend/src/agent/llm_factory.py`):
  - `create_query_generator_llm()` - Creates LLM for query generation
  - `create_reflection_llm()` - Creates LLM for reflection tasks  
  - `create_answer_llm()` - Creates LLM for final answer generation
  - Supports both `ChatGoogleGenerativeAI` and `ChatOllama` models

- **Documentation**:
  - Created comprehensive `CLAUDE.md` file with development commands and architecture overview
  - Added model provider documentation with usage examples
  - Updated README.md with Ollama prerequisites and model selection instructions

### Changed
- **Environment Configuration**:
  - **BREAKING**: Moved environment file from `backend/.env` to `secrets/.env`
  - Updated all code references to use new environment file location
  - Enhanced `secrets/.env` with Ollama configuration documentation

- **Makefile Enhancements**:
  - Added `MODEL` parameter support with `gemini` (default) and `ollama` options
  - Updated help documentation with usage examples
  - Improved command descriptions and parameter passing

- **LLM Initialization**:
  - Refactored `generate_query()` function to use LLM factory
  - Updated `reflection()` function with provider-aware model selection
  - Enhanced `finalize_answer()` function with dynamic model switching
  - Improved `web_research()` function with proper Gemini model handling

- **Dependencies**:
  - Added `langchain-ollama` to `backend/pyproject.toml`
  - Updated dependency list to support both Gemini and Ollama providers

### Fixed
- **Ollama Compatibility Issues**:
  - Fixed "model not found" errors when using `make dev MODEL=ollama`
  - Resolved incorrect model name passing between frontend and backend
  - Fixed web research function to always use compatible Gemini models for Google Search API
  - Ensured custom reasoning models are properly handled for each provider

- **Model Name Resolution**:
  - Fixed configuration system to properly map provider-specific model names
  - Resolved issues with frontend model selection conflicting with Ollama provider
  - Updated CLI example to use stable model names (removed preview suffixes)

- **Environment Loading**:
  - Fixed environment variable loading path resolution using `pathlib`
  - Updated `langgraph.json` to reference new environment file location
  - Corrected relative path calculations for cross-platform compatibility

### Technical Details

#### Architecture Changes
- **Hybrid Model Approach**: 
  - Text generation uses selected provider (Gemini or Ollama)
  - Web research always uses Google Search API (only available through Google ecosystem)
  - Maintains compatibility while providing choice

- **Model Mapping Strategy**:
  - **Gemini**: Uses configured models (`gemini-2.0-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`)
  - **Ollama**: Uses `llama3.2:latest` for all text generation tasks
  - Frontend model selection respected for Gemini, ignored for Ollama (uses appropriate fallback)

#### Files Modified
- `Makefile` - Added MODEL parameter and help documentation
- `backend/src/agent/configuration.py` - Enhanced with provider support
- `backend/src/agent/graph.py` - Updated all LLM initialization points
- `backend/src/agent/llm_factory.py` - **NEW** - LLM factory implementation
- `backend/pyproject.toml` - Added langchain-ollama dependency
- `backend/langgraph.json` - Updated environment file path
- `backend/examples/cli_research.py` - Fixed default model name
- `secrets/.env` - **MOVED** from `backend/.env` with enhanced documentation
- `README.md` - Added model provider documentation and prerequisites
- `CLAUDE.md` - **NEW** - Comprehensive development guide

#### Breaking Changes
- Environment file location changed from `backend/.env` to `secrets/.env`
- Requires manual environment file relocation for existing installations
- Ollama support requires Ollama installation and `llama3.2:latest` model

#### Prerequisites for Ollama
- Install Ollama from https://ollama.ai
- Pull Llama3.2 model: `ollama pull llama3.2:latest`
- Ensure Ollama server is running: `ollama serve`

### Usage Examples

```bash
# Use Google Gemini models (default)
make dev
make dev MODEL=gemini

# Use local Ollama/Llama3.2 models
make dev MODEL=ollama

# Run individual components
make dev-frontend
make dev-backend MODEL=ollama
```

---

## Development Notes

This version maintains backward compatibility (defaults to Gemini) while adding flexible LLM provider support. The implementation ensures that Google Search API functionality remains available regardless of model provider choice, as this capability is unique to Google's ecosystem.

All changes have been tested for syntax correctness and Makefile parameter handling. The modular design allows for easy addition of future LLM providers.