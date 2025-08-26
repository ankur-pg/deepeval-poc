"""
Main evaluation script for real estate analysis prompt testing
"""
import json
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
# Import custom components
from models.llm_integration import GeminiModel, load_prompt_template, create_test_input
from metrics.custom_metrics import BuyerProfileAccuracyMetric, FormatComplianceMetric, ThemeStructureMetric
from data.test_data import MARINA_BAY_DATA, YIELD_INVESTOR_SCENARIO, LEGACY_BUYER_SCENARIO


def create_test_cases():
    """Create test cases for evaluation"""
    
    # Initialize the model
    gemini_model = GeminiModel()
    prompt_template = load_prompt_template()
    
    test_cases = []
    
    # Test scenarios with expected outcomes
    scenarios = [
        {
            "name": "Marina Bay - Legacy Buyer",
            "data": MARINA_BAY_DATA,
            "expected_profile": "legacy_owner_occupier",
            "expected_challenge": "price_sensitivity"
        },
        {
            "name": "Pinnacle Duxton - Yield Investor", 
            "data": YIELD_INVESTOR_SCENARIO,
            "expected_profile": "yield_investor",
            "expected_challenge": "market_competition"
        },
        {
            "name": "One Raffles Place - Legacy Buyer",
            "data": LEGACY_BUYER_SCENARIO, 
            "expected_profile": "legacy_owner_occupier",
            "expected_challenge": "age_condition"
        }
    ]
    
    for scenario in scenarios:
        # Create input
        test_input = create_test_input(scenario["data"])
        
        # Generate output
        actual_output = gemini_model.generate_response(prompt_template, scenario["data"])
        
        # Create expected output (simplified for demo)
        expected_output = f"""Expected analysis for {scenario['expected_profile']} with {scenario['expected_challenge']} challenge.
        Should contain 3 bullet points under 80 characters each following Unit-Project-Location structure."""
        
        # Create test case
        test_case = LLMTestCase(
            input=test_input,
            actual_output=actual_output,
            expected_output=expected_output,
            context=[json.dumps(scenario["data"])]
        )
        
        test_cases.append(test_case)
        
        # Print the generated output for review
        print(f"\n{'='*50}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'='*50}")
        print("Generated Output:")
        print(actual_output)
        print("\n")
    
    return test_cases


def run_evaluation():
    """Run the complete evaluation"""
    
    print("Creating test cases...")
    test_cases = create_test_cases()
    
    print(f"Running evaluation on {len(test_cases)} test cases...")
    
    # Define metrics to evaluate
    metrics = [
        # Custom metrics for our specific requirements
        BuyerProfileAccuracyMetric(threshold=0.8),
        FormatComplianceMetric(threshold=1.0),
        ThemeStructureMetric(threshold=0.7)
    ]
    
    # Run evaluation
    results = evaluate(
        test_cases=test_cases,
        metrics=metrics
    )
    
    # Print results manually
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print("-" * 30)
        
        # Run each metric on this test case
        for metric in metrics:
            score = metric.measure(test_case)
            print(f"{metric.__name__}: {score:.2f} ({'PASS' if metric.is_successful() else 'FAIL'})")
            print(f"  Reason: {metric.reason}")
    
    return results


def analyze_single_scenario(data_payload, scenario_name="Custom"):
    """Analyze a single scenario for quick testing"""
    
    gemini_model = GeminiModel()
    prompt_template = load_prompt_template()
    
    print(f"\n{'='*50}")
    print(f"Analyzing: {scenario_name}")
    print(f"{'='*50}")
    
    # Generate analysis
    result = gemini_model.generate_response(prompt_template, data_payload)
    
    print("Input Data:")
    print(json.dumps(data_payload, indent=2))
    print("\nGenerated Analysis:")
    print(result)
    
    # Quick format check
    lines = [line.strip() for line in result.split('\n') if line.strip()]
    bullet_lines = [line for line in lines if line.startswith(('•', '-', '*')) or (len(line) > 10 and not line.endswith(':'))]
    
    print(f"\nQuick Format Check:")
    print(f"Number of bullets: {len(bullet_lines)}")
    for i, bullet in enumerate(bullet_lines[:3], 1):
        clean_bullet = bullet.replace('•', '').replace('-', '').replace('*', '').strip()
        print(f"Bullet {i} ({len(clean_bullet)} chars): {clean_bullet}")
    
    return result


if __name__ == "__main__":
    # Run single scenario analysis first
    print("Running single scenario analysis...")
    analyze_single_scenario(MARINA_BAY_DATA, "Marina Bay Residences")
    
    # Run full evaluation
    print("\n" + "="*60)
    print("STARTING FULL EVALUATION")
    print("="*60)
    
    results = run_evaluation()
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
