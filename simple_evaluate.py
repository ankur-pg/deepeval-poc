"""
Standalone evaluation script for real estate analysis prompt testing
"""
import json
from models.llm_integration import GeminiModel, load_prompt_template, create_test_input
from metrics.custom_metrics import BuyerProfileAccuracyMetric, FormatComplianceMetric, ThemeStructureMetric
from data.test_data import MARINA_BAY_DATA, YIELD_INVESTOR_SCENARIO, LEGACY_BUYER_SCENARIO


class SimpleTestCase:
    """Simple test case for manual evaluation"""
    def __init__(self, input_text, actual_output, expected_output, context=None):
        self.input = input_text
        self.actual_output = actual_output
        self.expected_output = expected_output
        self.context = context or []


def create_test_cases():
    """Create test cases for evaluation"""
    
    # Initialize the model
    gemini_model = GeminiModel()
    prompt_template = load_prompt_template()
    
    test_cases = []
    
    # Test scenarios with expected outcomes
    scenarios = [
        {
            "name": "Waterfront Residences - Legacy Buyer",
            "data": MARINA_BAY_DATA,
            "expected_profile": "legacy_owner_occupier",
            "expected_challenge": "price_sensitivity"
        },
        {
            "name": "Compact Towers - Yield Investor", 
            "data": YIELD_INVESTOR_SCENARIO,
            "expected_profile": "yield_investor",
            "expected_challenge": "market_competition"
        },
        {
            "name": "Premium Towers - Legacy Buyer",
            "data": LEGACY_BUYER_SCENARIO, 
            "expected_profile": "legacy_owner_occupier",
            "expected_challenge": "age_condition"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*50}")
        print(f"Generating response for: {scenario['name']}")
        print(f"{'='*50}")
        
        # Create input
        test_input = create_test_input(scenario["data"])
        
        # Generate output
        actual_output = gemini_model.generate_response(prompt_template, scenario["data"])
        
        # Create expected output (simplified for demo)
        expected_output = f"""Expected analysis for {scenario['expected_profile']} with {scenario['expected_challenge']} challenge.
        Should contain 3 bullet points under 80 characters each following Unit-Project-Location structure."""
        
        # Create test case
        test_case = SimpleTestCase(
            input_text=test_input,
            actual_output=actual_output,
            expected_output=expected_output,
            context=[json.dumps(scenario["data"])]
        )
        
        test_cases.append((scenario["name"], test_case))
        
        # Print the generated output for review
        print("Generated Output:")
        print(actual_output)
        print("\n")
    
    return test_cases


def run_manual_evaluation():
    """Run manual evaluation with custom metrics"""
    
    print("Creating test cases...")
    test_cases = create_test_cases()
    
    print(f"\n{'='*60}")
    print("RUNNING EVALUATION")
    print(f"{'='*60}")
    
    # Define metrics to evaluate
    metrics = [
        BuyerProfileAccuracyMetric(threshold=0.8),
        FormatComplianceMetric(threshold=1.0),
        ThemeStructureMetric(threshold=0.7)
    ]
    
    overall_results = []
    
    for scenario_name, test_case in test_cases:
        print(f"\n{'-'*50}")
        print(f"Evaluating: {scenario_name}")
        print(f"{'-'*50}")
        
        scenario_results = {}
        
        # Run each metric
        for metric in metrics:
            try:
                score = metric.measure(test_case)
                success = metric.is_successful()
                reason = metric.reason
                
                scenario_results[metric.__name__] = {
                    'score': score,
                    'success': success,
                    'reason': reason
                }
                
                print(f"{metric.__name__}: {score:.2f} ({'✅ PASS' if success else '❌ FAIL'})")
                print(f"  Reason: {reason}")
                
            except Exception as e:
                print(f"{metric.__name__}: ❌ ERROR - {str(e)}")
                scenario_results[metric.__name__] = {
                    'score': 0.0,
                    'success': False,
                    'reason': f"Error: {str(e)}"
                }
        
        overall_results.append((scenario_name, scenario_results))
    
    # Summary
    print(f"\n{'='*60}")
    print("EVALUATION SUMMARY")
    print(f"{'='*60}")
    
    for scenario_name, results in overall_results:
        print(f"\n{scenario_name}:")
        total_score = sum(r['score'] for r in results.values())
        avg_score = total_score / len(results)
        total_passed = sum(1 for r in results.values() if r['success'])
        
        print(f"  Average Score: {avg_score:.2f}")
        print(f"  Tests Passed: {total_passed}/{len(results)}")
        
        for metric_name, result in results.items():
            status = "✅" if result['success'] else "❌"
            print(f"    {status} {metric_name}: {result['score']:.2f}")
    
    return overall_results


def analyze_single_scenario(data_payload, scenario_name="Custom"):
    """Analyze a single scenario for quick testing"""
    
    gemini_model = GeminiModel()
    prompt_template = load_prompt_template()
    
    print(f"\n{'='*50}")
    print(f"Analyzing: {scenario_name}")
    print(f"{'='*50}")
    
    # Generate analysis
    result = gemini_model.generate_response(prompt_template, data_payload)
    
    print("Generated Analysis:")
    print(result)
    
    # Quick format check
    lines = [line.strip() for line in result.split('\n') if line.strip()]
    bullet_lines = []
    
    for line in lines:
        if line.startswith(('•', '-', '*')):
            bullet_lines.append(line)
        elif len(line) > 10 and not line.endswith(':') and not line.startswith('**'):
            bullet_lines.append(line)
    
    print(f"\nQuick Format Check:")
    print(f"Number of bullets: {len(bullet_lines)}")
    for i, bullet in enumerate(bullet_lines[:3], 1):
        clean_bullet = bullet.replace('•', '').replace('-', '').replace('*', '').strip()
        print(f"Bullet {i} ({len(clean_bullet)} chars): {clean_bullet}")
    
    # Run quick evaluation
    test_case = SimpleTestCase(
        input_text=create_test_input(data_payload),
        actual_output=result,
        expected_output="Quick test",
        context=[json.dumps(data_payload)]
    )
    
    print(f"\nQuick Metric Evaluation:")
    metrics = [
        BuyerProfileAccuracyMetric(threshold=0.8),
        FormatComplianceMetric(threshold=1.0),
        ThemeStructureMetric(threshold=0.7)
    ]
    
    for metric in metrics:
        try:
            score = metric.measure(test_case)
            success = metric.is_successful()
            print(f"{metric.__name__}: {score:.2f} ({'✅ PASS' if success else '❌ FAIL'})")
        except Exception as e:
            print(f"{metric.__name__}: ❌ ERROR - {str(e)}")
    
    return result


if __name__ == "__main__":
    # Run single scenario analysis first
    print("Running single scenario analysis...")
    analyze_single_scenario(MARINA_BAY_DATA, "Waterfront Residences")
    
    # Run full evaluation
    print("\n" + "="*60)
    print("STARTING FULL EVALUATION")
    print("="*60)
    
    results = run_manual_evaluation()
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
