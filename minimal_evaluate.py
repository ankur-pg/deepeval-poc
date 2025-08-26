"""
Minimal evaluation script using only essential metrics
"""
import json
from models.llm_integration import GeminiModel, load_prompt_template, create_test_input
from metrics.minimal_metrics import MinimalFormatMetric, MinimalRelevanceMetric, MinimalLogicMetric
from data.test_data import MARINA_BAY_DATA, YIELD_INVESTOR_SCENARIO, LEGACY_BUYER_SCENARIO


class SimpleTestCase:
    """Simple test case for manual evaluation"""
    def __init__(self, input_text, actual_output, expected_output, context=None):
        self.input = input_text
        self.actual_output = actual_output
        self.expected_output = expected_output
        self.context = context or []


def minimal_evaluation():
    """Run evaluation with minimal essential metrics only"""
    
    print("🎯 MINIMAL EVALUATION - Essential Metrics Only")
    print("="*60)
    
    # Initialize model
    gemini_model = GeminiModel()
    prompt_template = load_prompt_template()
    
    # Test scenarios
    scenarios = [
        ("Waterfront Residences", MARINA_BAY_DATA),
        ("Compact Towers", YIELD_INVESTOR_SCENARIO),
        ("Premium Towers", LEGACY_BUYER_SCENARIO)
    ]
    
    # Minimal essential metrics
    metrics = [
        MinimalFormatMetric(threshold=1.0),      # Must pass - critical
        MinimalRelevanceMetric(threshold=0.7),   # Must pass - critical  
        MinimalLogicMetric(threshold=0.6)        # Optional - nice to have
    ]
    
    results = []
    
    for scenario_name, data in scenarios:
        print(f"\n📊 Evaluating: {scenario_name}")
        print("-" * 40)
        
        # Generate response
        test_input = create_test_input(data)
        actual_output = gemini_model.generate_response(prompt_template, data)
        
        # Create test case
        test_case = SimpleTestCase(
            input_text=test_input,
            actual_output=actual_output,
            expected_output="Expected investment theses",
            context=[json.dumps(data)]
        )
        
        print("Generated Output:")
        print(actual_output[:200] + "..." if len(actual_output) > 200 else actual_output)
        print()
        
        # Run minimal metrics
        scenario_results = {}
        critical_passed = 0
        
        for metric in metrics:
            score = metric.measure(test_case)
            success = metric.is_successful()
            is_critical = metric.__name__ in ["Format Compliance", "Output Relevance"]
            
            if is_critical and success:
                critical_passed += 1
            
            scenario_results[metric.__name__] = {
                'score': score,
                'success': success,
                'critical': is_critical,
                'reason': metric.reason
            }
            
            # Display with priority indicators
            priority = "🔴 CRITICAL" if is_critical else "🟡 OPTIONAL"
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{priority} {metric.__name__}: {score:.2f} ({status})")
            print(f"   └─ {metric.reason}")
        
        # Overall assessment
        overall_pass = critical_passed >= 2  # Must pass both critical metrics
        results.append((scenario_name, scenario_results, overall_pass))
        
        print(f"\n{'🎉 OVERALL: PASS' if overall_pass else '⚠️  OVERALL: NEEDS IMPROVEMENT'}")
        print(f"Critical metrics passed: {critical_passed}/2")
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 MINIMAL EVALUATION SUMMARY")
    print("="*60)
    
    total_pass = sum(1 for _, _, passed in results if passed)
    
    for scenario_name, results_dict, overall_pass in results:
        status = "✅" if overall_pass else "❌"
        print(f"{status} {scenario_name}: {'PASS' if overall_pass else 'FAIL'}")
        
        # Show critical metrics only in summary
        for metric_name, result in results_dict.items():
            if result['critical']:
                status_icon = "✅" if result['success'] else "❌"
                print(f"    {status_icon} {metric_name}: {result['score']:.2f}")
    
    print(f"\nOverall Success Rate: {total_pass}/{len(results)} scenarios passed")
    
    return results


def quick_check(data_payload, scenario_name="Quick Test"):
    """Ultra-fast check with just critical metrics"""
    
    print(f"⚡ QUICK CHECK: {scenario_name}")
    print("-" * 30)
    
    gemini_model = GeminiModel()
    prompt_template = load_prompt_template()
    
    # Generate response
    result = gemini_model.generate_response(prompt_template, data_payload)
    
    # Create test case
    test_case = SimpleTestCase(
        input_text=create_test_input(data_payload),
        actual_output=result,
        expected_output="Quick test",
        context=[json.dumps(data_payload)]
    )
    
    # Run only critical metrics
    critical_metrics = [
        MinimalFormatMetric(threshold=1.0),
        MinimalRelevanceMetric(threshold=0.7)
    ]
    
    print("Generated Output:")
    print(result)
    print("\n⚡ Quick Assessment:")
    
    all_critical_pass = True
    for metric in critical_metrics:
        score = metric.measure(test_case)
        success = metric.is_successful()
        if not success:
            all_critical_pass = False
        
        status = "✅" if success else "❌"
        print(f"{status} {metric.__name__}: {score:.2f}")
    
    print(f"\n{'🎉 READY FOR PRODUCTION' if all_critical_pass else '⚠️  NEEDS REFINEMENT'}")
    
    return all_critical_pass


if __name__ == "__main__":
    print("Choose evaluation mode:")
    print("1. Minimal evaluation (3 metrics, all scenarios)")
    print("2. Quick check (2 critical metrics, Waterfront only)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        quick_check(MARINA_BAY_DATA, "Waterfront Residences")
    else:
        minimal_evaluation()
