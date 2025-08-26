"""
Minimal essential metrics for real estate analysis prompt evaluation
"""
import re
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


class MinimalFormatMetric(BaseMetric):
    """Essential format validation: 3 bullets, 80 chars max"""
    
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.evaluation_cost = 0
    
    def measure(self, test_case: LLMTestCase) -> float:
        """Measures basic format compliance"""
        actual_output = test_case.actual_output.strip()
        
        # Extract bullet points
        lines = [line.strip() for line in actual_output.split('\n') if line.strip()]
        bullet_lines = []
        
        for line in lines:
            if line.startswith(('•', '-', '*')):
                bullet_lines.append(line)
            elif len(line) > 20 and not line.endswith(':') and not line.startswith('**'):
                bullet_lines.append(line)
        
        # Score components
        bullet_count_score = 1.0 if len(bullet_lines) == 3 else 0.0
        
        # Character count compliance
        char_scores = []
        for bullet in bullet_lines:
            clean_bullet = re.sub(r'^[•\-\*]\s*', '', bullet)
            char_count = len(clean_bullet)
            char_score = 1.0 if char_count <= 80 else 0.0
            char_scores.append(char_score)
        
        avg_char_score = sum(char_scores) / len(char_scores) if char_scores else 0.0
        
        # Final score
        self.score = (bullet_count_score + avg_char_score) / 2
        self.reason = f"Format: {len(bullet_lines)}/3 bullets, {avg_char_score:.0%} char compliance"
        self.success = self.score >= self.threshold
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Format Compliance"


class MinimalRelevanceMetric(BaseMetric):
    """Essential relevance validation: Uses input data appropriately"""
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        self.evaluation_cost = 0
    
    def measure(self, test_case: LLMTestCase) -> float:
        """Measures output relevance to input data"""
        actual_output = test_case.actual_output.lower()
        input_data = test_case.input.lower()
        
        # Extract key data points from input
        relevance_indicators = []
        
        # Check for property-specific terms
        property_terms = ['sqft', 'bedroom', 'freehold', 'leasehold', 'mrt', 'view']
        for term in property_terms:
            if term in input_data and term in actual_output:
                relevance_indicators.append(1)
            elif term in input_data:
                relevance_indicators.append(0)
        
        # Check for investment/real estate context
        investment_terms = ['investment', 'value', 'asset', 'price', 'market', 'property']
        investment_score = sum(1 for term in investment_terms if term in actual_output) / len(investment_terms)
        relevance_indicators.append(investment_score)
        
        # Check for specific property names (indicates specific rather than generic analysis)
        if any(term in actual_output for term in ['waterfront', 'compact towers', 'premium towers', 'central district']):
            specific_score = 1.0
        relevance_indicators.append(specific_score)
        
        self.score = sum(relevance_indicators) / len(relevance_indicators) if relevance_indicators else 0.0
        self.reason = f"Relevance: {self.score:.0%} data utilization, context-appropriate"
        self.success = self.score >= self.threshold
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Output Relevance"


class MinimalLogicMetric(BaseMetric):
    """Optional: Basic logical consistency check"""
    
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
        self.evaluation_cost = 0
    
    def measure(self, test_case: LLMTestCase) -> float:
        """Measures basic logical consistency"""
        actual_output = test_case.actual_output.lower()
        
        # Check for contradictory statements
        consistency_score = 1.0
        
        # Check for balanced tone (not contradictory)
        if 'excellent' in actual_output and 'poor' in actual_output:
            consistency_score -= 0.3
        
        # Check for appropriate buyer language
        if '750' in test_case.input:  # Smaller unit
            if 'spacious' in actual_output or 'large' in actual_output:
                consistency_score -= 0.2
        
        if '1500' in test_case.input:  # Larger unit
            if 'compact' in actual_output or 'efficient size' in actual_output:
                consistency_score -= 0.2
        
        # Ensure positive framing (investment thesis should be positive)
        negative_terms = ['avoid', 'poor', 'bad', 'risky', 'decline']
        negative_count = sum(1 for term in negative_terms if term in actual_output)
        if negative_count > 1:
            consistency_score -= 0.2
        
        self.score = max(0.0, consistency_score)
        self.reason = f"Logic: {'Consistent' if self.score > 0.7 else 'Some inconsistencies'} reasoning"
        self.success = self.score >= self.threshold
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Logical Consistency"
