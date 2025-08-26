# DeepEval POC - Prompt Evaluation

A comprehensive proof-of-concept demonstrating how to evaluate LLM prompts using deepeval framework with custom business metrics for real estate market analysis.

## Overview

This POC evaluates a sophisticated real estate analysis prompt that deduces buyer profiles and generates investment theses based on property data. It includes custom metrics for:
- Buyer profile identification accuracy
- Format compliance (3 bullets, 80 char limit)
- Theme structure validation (Unit-Project-Location)

## Project Structure

```
deepeval/
├── prompts/
│   └── real_estate_analysis_prompt.txt     # Main analysis prompt template
├── data/
│   └── test_data.py                        # Test scenarios (Waterfront, Towers, etc.)
├── metrics/
│   └── custom_metrics.py                   # Custom evaluation metrics
├── models/
│   └── llm_integration.py                  # Gemini model integration
├── evaluate.py                             # DeepEval framework integration
├── simple_evaluate.py                      # Standalone evaluation script
├── requirements.txt                        # Dependencies
├── .env                                    # Configuration (API keys)
└── README.md                               # This file
```

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Google Gemini API key

### 2. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd deepeval

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file with your API keys:

```bash
# Copy the example file
cp .env-example .env

# Edit .env file with your API key
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

## How to Run

### Option 1: Complete Evaluation (Recommended)

Run the full evaluation across all test scenarios:

```bash
python simple_evaluate.py
```

This will:
1. Analyze a single scenario first (Waterfront Residences)
2. Run comprehensive evaluation on all 3 test scenarios
3. Generate detailed metrics for each scenario
4. Provide summary results and insights

### Option 2: DeepEval Framework (Advanced)

For integration with deepeval's full framework:

```bash
python evaluate.py
```

Note: This requires OpenAI API key for standard deepeval metrics.

### Option 3: Single Scenario Analysis

To analyze a specific property scenario:

```python
from simple_evaluate import analyze_single_scenario
from data.test_data import WATERFRONT_RESIDENCE_DATA

# Analyze a single scenario
result = analyze_single_scenario(WATERFRONT_RESIDENCE_DATA, "Waterfront Test")
```

## Test Scenarios

The POC includes three pre-configured real estate scenarios:

1. **Waterfront Residences** - 1200 sqft legacy buyer scenario
2. **The Compact Towers** - 750 sqft yield investor scenario  
3. **Premium Towers** - 1500 sqft premium legacy buyer scenario

Each scenario includes:
- Property details (size, config, location)
- Market context (competitive listings, transactions)
- Expected buyer profile and challenges

## Custom Metrics Explained

### Buyer Profile Accuracy Metric
- Validates if the model correctly identifies investor vs owner-occupier profiles
- Based on unit size analysis against market context
- Threshold: 80% accuracy required

### Format Compliance Metric
- Ensures exactly 3 bullet points
- Validates max 80 characters per bullet
- Threshold: 100% compliance required

### Theme Structure Metric
- Checks Unit-Project-Location thematic structure
- Uses keyword analysis for each bullet
- Threshold: 70% adherence required

## Sample Output

```
==================================================
Analyzing: Waterfront Residences
==================================================
Generated Analysis:
* Unit: Rare 1200 sqft 2BR – unmatched space & waterfront views.
* Project: Freehold luxury; a trophy asset, immune to lease decay concerns.
* Location: Prime waterfront address, shielded from peripheral price dips.

Quick Format Check:
Number of bullets: 3
Bullet 1 (62 chars): Unit: Rare 1200 sqft 2BR – unmatched space & waterfront views.
Bullet 2 (73 chars): Project: Freehold luxury; a trophy asset, immune to lease decay concerns.
Bullet 3 (71 chars): Location: Prime waterfront address, shielded from peripheral price dips.

Quick Metric Evaluation:
Buyer Profile Accuracy: 1.00 (✅ PASS)
Format Compliance: 1.00 (✅ PASS)
Theme Structure: 1.00 (✅ PASS)
```

## DeepEval Core Metrics

DeepEval provides a comprehensive set of built-in metrics for LLM evaluation. Here are the core metrics available:

### 📊 **Quality & Relevance Metrics**
- **AnswerRelevancyMetric**: Measures how relevant the answer is to the input question
- **FaithfulnessMetric**: Evaluates if the answer is grounded in the provided context
- **ContextualRelevancyMetric**: Assesses relevance of retrieved context to the question
- **ContextualPrecisionMetric**: Measures precision of context retrieval
- **ContextualRecallMetric**: Evaluates recall of relevant information from context

### 🛡️ **Safety & Ethics Metrics**
- **ToxicityMetric**: Detects toxic, harmful, or offensive content
- **BiasMetric**: Identifies potential bias in model responses
- **HallucinationMetric**: Detects factually incorrect or made-up information
- **PIILeakageMetric**: Identifies potential personally identifiable information leaks

### 🎯 **Task-Specific Metrics**
- **SummarizationMetric**: Evaluates quality of text summarization
- **ToolCorrectnessMetric**: Assesses correct usage of tools/functions
- **JsonCorrectnessMetric**: Validates JSON format and structure compliance
- **ArgumentCorrectnessMetric**: Evaluates logical argument structure

### 🔒 **Specialized Metrics**
- **PromptAlignmentMetric**: Measures adherence to prompt instructions
- **RoleAdherenceMetric**: Evaluates if model maintains assigned role
- **TaskCompletionMetric**: Assesses if specific tasks are completed
- **KnowledgeRetentionMetric**: Tests retention of information across conversations

### 🖼️ **Multimodal Metrics**
- **MultimodalAnswerRelevancyMetric**: Answer relevance for image+text inputs
- **MultimodalFaithfulnessMetric**: Faithfulness for multimodal content
- **ImageCoherenceMetric**: Evaluates visual coherence in generated images
- **TextToImageMetric**: Assesses text-to-image generation quality

### 💬 **Conversational Metrics**
- **ConversationCompletenessMetric**: Evaluates conversation completeness
- **TurnRelevancyMetric**: Assesses relevance of individual conversation turns

### 🚫 **Misuse Detection**
- **MisuseMetric**: Detects potential misuse of the model
- **NonAdviceMetric**: Ensures model doesn't give advice in restricted domains

### Usage Example with Standard DeepEval Metrics

```python
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ToxicityMetric,
    BiasMetric
)
from deepeval.test_case import LLMTestCase

# Create test case
test_case = LLMTestCase(
    input="Your input question",
    actual_output="Model's response",
    expected_output="Expected response",
    context=["Supporting context"]
)

# Define metrics
metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.8),
    ToxicityMetric(threshold=0.1),
    BiasMetric(threshold=0.2)
]

# Run evaluation
evaluate(test_cases=[test_case], metrics=metrics)
```

### Custom vs Built-in Metrics

**This POC uses custom metrics because:**
- Built-in metrics require OpenAI API access (additional cost)
- Our use case needs domain-specific evaluation (real estate analysis)
- Custom metrics provide more control over evaluation logic
- Business-specific requirements (format compliance, theme structure)

**When to use built-in metrics:**
- General LLM quality assessment
- Safety and ethics evaluation
- Standard RAG pipeline evaluation
- Comparative benchmarking across models

**When to create custom metrics:**
- Domain-specific requirements (like our real estate use case)
- Unique format or structure requirements
- Business logic validation
- Cost-sensitive evaluations (avoiding additional API calls)

## 🎯 Minimal Essential Metrics

For efficient evaluation, you only need **2-3 core metrics** to validate your real estate analysis prompt:

### **Critical Metrics (Must Pass)**

#### 1. Format Compliance Metric 🔴 **CRITICAL**
- **Purpose**: Validates strict format requirements
- **Checks**: 3 bullets, ≤80 characters, Unit-Project-Location structure
- **Why Critical**: Non-compliant output is unusable in production
- **Threshold**: 100% (must be perfect)

#### 2. Output Relevance Metric 🔴 **CRITICAL** 
- **Purpose**: Ensures response uses input data appropriately
- **Checks**: Property-specific terms, investment context, data utilization
- **Why Critical**: Irrelevant analysis provides no business value
- **Threshold**: 70% (good data utilization)

### **Optional Metric (Nice to Have)**

#### 3. Logical Consistency Metric 🟡 **OPTIONAL**
- **Purpose**: Basic reasoning validation
- **Checks**: No contradictions, appropriate buyer language, positive framing
- **Why Useful**: Prevents obviously flawed recommendations
- **Threshold**: 60% (basic consistency)

### **Quick Evaluation Options**

**Option A: Ultra-Fast Check (2 metrics)**
```bash
# Test critical metrics only - fastest validation
python minimal_evaluate.py
# Choose option 2 for quick check
```

**Option B: Minimal Complete (3 metrics)**  
```bash
# Include logical consistency - comprehensive but fast
python minimal_evaluate.py  
# Choose option 1 for full minimal evaluation
```

**Option C: Full Custom (Original)**
```bash
# All custom metrics including buyer profile accuracy
python simple_evaluate.py
```

### **Results Interpretation**

**✅ PRODUCTION READY**: Both critical metrics pass
- Format compliance ≥ 100%
- Output relevance ≥ 70%

**⚠️ NEEDS REFINEMENT**: Any critical metric fails
- Fix format issues first (most common)
- Then improve data utilization

### **Sample Minimal Output**

```
⚡ QUICK CHECK: Waterfront Residences
Generated Output: [3 investment theses...]

⚡ Quick Assessment:
❌ Format Compliance: 0.36 (Format: 7/3 bullets, 71% char compliance)
❌ Output Relevance: 0.52 (Relevance: 52% data utilization, context-appropriate)

⚠️  NEEDS REFINEMENT
```

### **Cost & Speed Comparison**

| Approach | Metrics | Time | API Calls | Best For |
|----------|---------|------|-----------|----------|
| Ultra-Fast | 2 Critical | ~3 sec | 1 (Gemini) | Quick validation |
| Minimal | 3 Essential | ~5 sec | 1 (Gemini) | Development testing |
| Full Custom | 3 Detailed | ~8 sec | 1 (Gemini) | Comprehensive analysis |
| Full DeepEval | 5+ Standard | ~15 sec | 3+ (OpenAI+Gemini) | Research/benchmarking |

### **Recommendation**

**Start with Ultra-Fast (2 metrics)** for most use cases:
- Covers 80% of potential issues
- Fastest feedback loop
- Zero additional API costs
- Perfect for CI/CD integration

**Upgrade to Full Custom only when:**
- You need buyer profile accuracy validation
- Detailed reporting is required
- You're optimizing for edge cases

## Extending the POC

### Adding New Test Scenarios

1. Add your scenario to `data/test_data.py`:
```python
NEW_SCENARIO = {
    "unitData": {
        "address": "Your address",
        "sqft": 1000,
        # ... other fields
    },
    # ... rest of the structure
}
```

2. Include it in evaluation by updating `simple_evaluate.py`

### Creating Custom Metrics

1. Extend `BaseMetric` in `metrics/custom_metrics.py`:
```python
class YourCustomMetric(BaseMetric):
    def measure(self, test_case: LLMTestCase) -> float:
        # Your evaluation logic here
        return score
```

2. Add to metrics list in evaluation scripts

### Using Different LLMs

1. Create new model wrapper in `models/llm_integration.py`
2. Update the model initialization in evaluation scripts

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file has the correct API key
2. **Import Errors**: Activate the virtual environment before running
3. **SSL Warnings**: These are harmless urllib3 warnings on macOS

### Dependencies Issues

If you encounter package conflicts:
```bash
pip install --upgrade deepeval google-generativeai python-dotenv
```

## Results Interpretation

The evaluation provides:
- **Individual Scores**: 0.0-1.0 for each metric
- **Pass/Fail Status**: Based on predefined thresholds
- **Detailed Reasons**: Explanations for each score
- **Summary Statistics**: Overall performance across scenarios

## Next Steps

1. Review the POC_SUMMARY.md for detailed results analysis
2. Experiment with different prompt variations
3. Add more diverse test scenarios
4. Integrate with CI/CD for continuous evaluation

## Contributing

To contribute to this POC:
1. Add new test scenarios or metrics
2. Improve prompt templates
3. Enhance evaluation logic
4. Add support for additional LLMs
