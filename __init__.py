"""
DeepEval POC for Real Estate Analysis Prompt Evaluation

This package evaluates the performance of LLMs on real estate market analysis tasks,
specifically focused on premium property analysis and investment advisory.

Key Features:
- Custom metrics for buyer profile identification
- Format compliance checking (3 bullets, 80 char limit)
- Theme structure validation (Unit-Project-Location)
- Integration with Google Gemini model
- Multiple test scenarios for comprehensive evaluation

Usage:
    python evaluate.py

Structure:
    - prompts/: Contains the analysis prompt template
    - data/: Test data scenarios (Waterfront, Towers, etc.)
    - metrics/: Custom evaluation metrics
    - models/: LLM integration (Gemini)
    - evaluate.py: Main evaluation script
"""

__version__ = "1.0.0"
__author__ = "Real Estate Analytics Team"
