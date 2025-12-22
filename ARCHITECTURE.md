# FAO-Sim Architecture Documentation

## Project Structure

```
LAPS/
├── faosim/                         # Main package
│   ├── __init__.py                 # Package initialization
│   ├── cli.py                      # Command-line interface
│   │
│   ├── core/                       # Core components
│   │   ├── __init__.py
│   │   ├── schemas.py              # Pydantic data models
│   │   └── orchestrator.py         # Main workflow orchestrator
│   │
│   ├── modules/                    # Functional modules
│   │   ├── __init__.py
│   │   ├── rag_knowledge_base.py   # RAG knowledge base (LangChain + ChromaDB)
│   │   ├── forecasting_engine.py   # TimesFM forecasting engine
│   │   ├── campaign_generator.py   # Campaign parameter generator
│   │   ├── evaluation_engine.py    # Campaign evaluation & scoring
│   │   └── optimization_loop.py    # Genetic algorithm optimization
│   │
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       └── helpers.py              # Helper functions
│
├── examples/                       # Example files
│   ├── user_constraints_example.json
│   ├── fb_ads_guide.txt            # Sample knowledge base
│   ├── quick_start.py              # Quick start script
│   └── run_optimization.sh         # Shell script example
│
├── tests/                          # Test suite
│   ├── __init__.py
│   └── test_schemas.py             # Schema validation tests
│
├── docs/                           # Documentation (future)
├── data/                           # Data directory (created at runtime)
├── config/                         # Configuration files
├── output/                         # Output directory (created at runtime)
│
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup
├── .env.example                    # Environment variables example
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
├── README.md                       # Main documentation
└── ARCHITECTURE.md                 # This file
```

## Module Overview

### 1. Core Modules (`faosim/core/`)

#### `schemas.py`
Defines all data structures using Pydantic v2:

- **Input Schemas**:
  - `HistoricalData`: Historical campaign performance data
  - `Goal`: Optimization goal and target metrics
  - `UserConstraints`: User-defined constraints and goals

- **Campaign Schemas**:
  - `AudienceTargeting`: Audience targeting parameters
  - `AdCreative`: Ad creative configuration
  - `BiddingStrategy`: Bidding and optimization strategy
  - `CampaignParameters`: Complete campaign configuration

- **Output Schemas**:
  - `ForecastMetrics`: Forecasted performance metrics
  - `ForecastResult`: Evaluation result for a campaign
  - `OptimizationResult`: Final optimization results

- **RAG Schemas**:
  - `KnowledgeBaseDocument`: Document structure
  - `ParameterSpace`: Searchable parameter space

#### `orchestrator.py`
Main workflow coordinator that:
- Initializes all modules
- Coordinates the optimization workflow
- Manages data flow between components
- Exports results in multiple formats

### 2. Functional Modules (`faosim/modules/`)

#### `rag_knowledge_base.py`
RAG (Retrieval-Augmented Generation) Knowledge Base:

**Key Features**:
- Loads documents (PDF, DOCX, TXT)
- Creates embeddings using OpenAI
- Stores in ChromaDB vector database
- Provides semantic search and retrieval
- Extracts parameter space for optimization

**Main Classes**:
- `RAGKnowledgeBase`: Main knowledge base class

**Key Methods**:
- `load_documents()`: Load and parse documents
- `build_knowledge_base()`: Create vector store
- `extract_parameter_space()`: Extract optimization parameters
- `query()`: Query knowledge base

#### `forecasting_engine.py`
Performance forecasting using TimesFM:

**Key Features**:
- Forecasts campaign performance metrics
- Supports TimesFM or fallback models
- Calculates economic metrics (CPA, ROAS, ROI)
- Provides confidence intervals

**Main Classes**:
- `ForecastingEngine`: Forecasting engine

**Key Methods**:
- `forecast_metrics()`: Forecast single campaign
- `batch_forecast()`: Forecast multiple campaigns
- `vectorize_campaign_params()`: Convert params to features

**Forecasted Metrics**:
- CPM (Cost per 1000 impressions)
- CTR (Click-through rate)
- CPC (Cost per click)
- CR (Conversion rate)
- CPA (Cost per acquisition)
- ROAS (Return on ad spend)
- ROI (Return on investment)

#### `campaign_generator.py`
Campaign variant generation:

**Key Features**:
- Generates diverse campaign configurations
- Implements genetic algorithm operations
- Random initialization with constraints
- Crossover and mutation operations

**Main Classes**:
- `CampaignGenerator`: Campaign generator

**Key Methods**:
- `generate_initial_population()`: Create initial campaigns
- `crossover()`: Combine two parent campaigns
- `mutate()`: Apply random mutations
- `generate_from_winners()`: Create next generation

**Generated Parameters**:
- Audience targeting (age, gender, location, interests)
- Creative format and content
- Bidding strategy and budget
- Ad placements

#### `evaluation_engine.py`
Campaign evaluation and scoring:

**Key Features**:
- Evaluates campaigns against goals
- Multi-criteria fitness scoring
- Performance analysis and benchmarking
- Winner/failure classification

**Main Classes**:
- `EvaluationEngine`: Evaluation engine

**Key Methods**:
- `evaluate_campaign()`: Evaluate single campaign
- `evaluate_batch()`: Evaluate multiple campaigns
- `get_top_campaigns()`: Get best performers
- `analyze_performance_distribution()`: Statistical analysis

**Fitness Scoring**:
- Primary metric: 60% weight
- ROAS profitability: 30% weight
- Forecast confidence: 10% weight

#### `optimization_loop.py`
Main genetic algorithm optimization loop:

**Key Features**:
- Iterative optimization process
- Generation-based evolution
- Convergence tracking
- Early stopping mechanism

**Main Classes**:
- `OptimizationLoop`: Optimization loop controller

**Key Methods**:
- `run()`: Execute complete optimization
- `_generate_next_generation()`: Create next generation
- `_log_generation_stats()`: Log statistics
- `get_convergence_plot_data()`: Export convergence data

**Optimization Flow**:
1. Generate initial population
2. Forecast performance
3. Evaluate against goals
4. Select best performers
5. Generate next generation (crossover + mutation)
6. Repeat until convergence or max loops

### 3. CLI Interface (`faosim/cli.py`)

Command-line interface for running optimizations:

**Features**:
- Load configuration from JSON
- Flexible logging options
- Multiple export formats
- Progress tracking

**Usage**:
```bash
python -m faosim.cli \
  --config config.json \
  --knowledge-base docs/*.pdf \
  --output-dir ./output \
  --export-format both
```

## Data Flow

```
1. User Input (JSON)
   ↓
2. Load Historical Data + Goals
   ↓
3. Build RAG Knowledge Base
   ↓
4. Extract Parameter Space
   ↓
5. Generate Initial Campaign Population
   ↓
6. ┌─────────── OPTIMIZATION LOOP ───────────┐
   │                                          │
   │  A. Forecast Performance (TimesFM)      │
   │  B. Evaluate Against Goals              │
   │  C. Select Winners                      │
   │  D. Generate Next Generation            │
   │     - Crossover                         │
   │     - Mutation                          │
   │                                          │
   │  Repeat until:                          │
   │  - Max loops reached OR                 │
   │  - Convergence achieved                 │
   │                                          │
   └──────────────────────────────────────────┘
   ↓
7. Export Winning Campaigns (JSON/CSV)
```

## Key Algorithms

### Genetic Algorithm

**Population**: Set of campaign configurations

**Fitness Function**:
```
fitness = 0.6 × (metric_performance / target) +
          0.3 × (roas / 2.0) +
          0.1 × confidence
```

**Selection**: Elitism (keep top N performers)

**Crossover**: Uniform crossover of campaign parameters
```python
offspring.audience = random.choice([parent1.audience, parent2.audience])
offspring.creative = random.choice([parent1.creative, parent2.creative])
offspring.bidding = blend(parent1.bidding, parent2.bidding)
```

**Mutation**: Random parameter adjustments (20% probability)
```python
if random() < 0.2:
    campaign = mutate(campaign)
```

### Forecasting Formula

```
CPA = CPM / (CTR × CR × 1000)
ROAS = Selling Price / CPA
ROI = (Selling Price - Product Cost - CPA) / CPA
```

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...              # For embeddings

# Optional
ANTHROPIC_API_KEY=sk-ant-...       # Alternative LLM
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
LOG_LEVEL=INFO
```

### User Constraints Schema

```json
{
  "product_cost": float,
  "selling_price": float,
  "historical_data": {
    "cpm": float,
    "ctr": float (0-1),
    "cpc": float,
    "cr": float (0-1),
    "daily_budget": float
  },
  "goal": {
    "metric": "ROAS" | "ROI" | "CPA" | "CTR" | "CR",
    "target_value": float,
    "tolerance": float (0-1)
  },
  "max_loops": int,
  "population_size": int,
  "min_daily_budget": float,
  "max_daily_budget": float
}
```

## Dependencies

### Core
- Python 3.9+
- Pydantic 2.0+ (data validation)
- LangChain (RAG framework)
- ChromaDB (vector database)

### AI/ML
- OpenAI (embeddings)
- TimesFM (forecasting)
- PyTorch (deep learning)
- Scikit-learn (ML utilities)

### Optimization
- DEAP (genetic algorithms)
- NumPy (numerical computing)
- Pandas (data manipulation)

### Utilities
- Loguru (logging)
- python-dotenv (environment)
- tqdm (progress bars)

## Performance Considerations

### Optimization
- **Population Size**: 10-50 campaigns (balance diversity vs. speed)
- **Generations**: 5-20 loops (diminishing returns after 10-15)
- **Parallel Processing**: Batch forecasting for efficiency
- **Early Stopping**: Halt if no improvement for 3 generations

### Memory
- Vector DB: ~100MB per 1000 documents
- Campaign Cache: ~1KB per campaign
- Forecast Cache: ~2KB per forecast

### Speed
- Setup: 10-30 seconds (RAG + models)
- Per Generation: 5-15 seconds (20 campaigns)
- Total Run: 1-5 minutes (typical optimization)

## Testing

Run tests:
```bash
pytest tests/
pytest --cov=faosim --cov-report=html
```

Test coverage areas:
- Schema validation
- Module integration
- End-to-end workflows
- Edge cases and errors

## Future Enhancements

1. **Real-time Integration**: Connect to Facebook Marketing API
2. **Advanced Forecasting**: Custom time series models
3. **Multi-objective**: Pareto optimization for multiple goals
4. **A/B Testing**: Built-in experiment framework
5. **Monitoring**: Real-time performance tracking
6. **Scaling**: Multi-account management

## License

MIT License - See LICENSE file for details.
