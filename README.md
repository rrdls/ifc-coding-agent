# IFC Coding Agent

A skills-based coding agent for flexible BIM information retrieval from IFC models using natural language queries.

## Overview

This project implements a coding agent that uses IfcOpenShell domain knowledge encapsulated as **skills** to dynamically generate Python code for answering natural language queries about Building Information Models (BIM) encoded in Industry Foundation Classes (IFC) format.

Unlike traditional approaches that rely on predefined domain tools, this agent consults skill documentation to generate appropriate code on-the-fly, enabling flexible responses to diverse and unanticipated queries.

## Academic Reference

This implementation accompanies the following research paper:

> **A Skills-Based Coding Agent for Flexible BIM Information Retrieval**  
<!-- > Ramos, R. & Calvetti, D.   -->
> *2026 European Conference on Computing in Construction (EC3)*  
> Corfu, Greece, July 12–15, 2026

The agent achieves **84.7% overall accuracy** on the FNDE-BIM-Bench benchmark (85 queries across 5 IFC disciplines) using GPT-5-mini as the LLM backbone.

## Requirements

- Python 3.10+
- OpenRouter API key (or OpenAI API key)
- IfcOpenShell

## Installation

```bash
# Clone the repository
git clone https://github.com/rrdls/ifc-coding-agent.git
cd ifc-coding-agent

# Create virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
# env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
# Or for OpenAI direct:
# OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Interactive Mode

```bash
python main.py --model gpt-5-mini
```

### Single Query Mode

```bash
python main.py --model gpt-5-mini --query "How many walls are in the model?"
```

### Run Benchmark

```bash
# Run all queries with a specific model
python benchmark_runner.py --model gpt-5-mini

# Run a single query
python benchmark_runner.py --model gpt-5-mini --query ARQ_E01

# Run a range of queries (0-indexed)
python benchmark_runner.py --model gpt-5-mini --start 0 --end 9

# List available models
python benchmark_runner.py --list-models
```

> **Note:** Skill extraction is always enabled. Reusable functions are automatically extracted from successful queries.

### Reset Experiment Environment

```bash
# Interactive mode (asks for confirmation)
python reset_experiment.py

# Silent mode (no confirmation)
python reset_experiment.py --yes

# Dry-run (show what would be removed)
python reset_experiment.py --dry-run

# Create backup before reset
python reset_experiment.py --backup
```

## Available Models

| Key | Provider | Model |
|-----|----------|-------|
| `gpt-5-mini` | OpenRouter | openai/gpt-5-mini |
| `gpt-4o` | OpenRouter | openai/gpt-4o |
| `claude-haiku-4.5` | OpenRouter | anthropic/claude-haiku-4.5 |
| `claude-sonnet-4.5` | OpenRouter | anthropic/claude-sonnet-4.5 |
| `gemini-2.5-pro-high` | OpenRouter | google/gemini-2.5-pro-preview |
| `gpt-4o-openai` | OpenAI | gpt-4o |
| `gpt-5-mini-openai` | OpenAI | gpt-5-mini |

Run `python benchmark_runner.py --list-models` for the complete list.

## Project Structure

```
ifc-coding-agent/
├── main.py                    # Agent initialization and interactive mode
├── benchmark_runner.py        # Benchmark execution runner
├── skill_builder.py           # Skill extraction from successful queries
├── skill_tracking_backend.py  # Tracks skill access during execution
├── planning_middleware.py     # Enforces planning before code execution
├── reset_experiment.py        # Reset experiment environment
├── dataset/
│   └── benchmark_dataset.json # FNDE-BIM-Bench (85 queries)
├── projects/
│   └── fnde/                  # IFC models (ARQ, ELE, EST, HAF, HEP)
├── skills/
│   ├── ifcopenshell-*/        # Base IfcOpenShell skills
│   └── learned/               # Generated skills library
├── sandbox/                   # Generated scripts and plans
└── results/                   # Benchmark results
```

## Architecture

The agent follows the canonical **model-tools-instructions** pattern:

1. **LLM Backbone**: GPT-5-mini (configurable)
2. **Generic Tools**: Shell command execution, file operations
3. **Skills Module**: IfcOpenShell documentation via progressive disclosure
4. **Skill Generation**: Extracts reusable functions from successful executions
5. **Code Validation**: AST-based analyzer with auto-correction subagent

## FNDE-BIM-Bench

A custom benchmark with 85 queries across:

- **3 Query Types**: DirectLookup (20), FilteredAggregation (36), MultiStep (29)
- **5 IFC Disciplines**: Architecture, Electrical, Structural, Cold Water, Sewage

## License

MIT License

<!-- ## Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{ramos2026skills,
  title={A Skills-Based Coding Agent for Flexible BIM Information Retrieval},
  author={Ramos, Renato and Calvetti, Diego},
  booktitle={2026 European Conference on Computing in Construction},
  year={2026},
  address={Corfu, Greece}
}
``` -->
