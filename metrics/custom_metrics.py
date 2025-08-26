"""
Custom evaluation metrics for real estate analysis prompt
"""
import re
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from typing import List


class BuyerProfileAccuracyMetric(BaseMetric):
    """Evaluates if the model correctly identifies the buyer profile"""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.evaluation_cost = 0  # No additional API calls needed
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measures accuracy of buyer profile identification
        Returns 1.0 if correct, 0.0 if incorrect
        """
        actual_output = test_case.actual_output.lower()
        expected_context = test_case.input.lower()
        
        # Analyze the input data to determine expected buyer profile
        expected_profile = self._determine_expected_profile(test_case.input)
        
        # Check if the output indicates the correct profile
        if expected_profile == "yield_investor":
            # Look for investor-focused language
            investor_keywords = ["yield", "investor", "rental", "returns", "income"]
            score = 1.0 if any(keyword in actual_output for keyword in investor_keywords) else 0.0
        else:  # legacy/owner-occupier
            # Look for owner-occupier focused language
            owner_keywords = ["legacy", "owner", "occupier", "home", "family", "lifestyle"]
            score = 1.0 if any(keyword in actual_output for keyword in owner_keywords) else 0.0
        
        self.score = score
        self.reason = f"Expected {expected_profile}, analysis shows {'correct' if score > 0.5 else 'incorrect'} identification"
        self.success = score >= self.threshold
        
        return score
    
    def _determine_expected_profile(self, input_data: str) -> str:
        """Determine expected buyer profile based on input data"""
        # Extract sqft information (simplified logic)
        if "1200" in input_data or "1500" in input_data:
            return "legacy_owner_occupier"  # Larger units
        else:
            return "yield_investor"  # Smaller units
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Buyer Profile Accuracy"


class FormatComplianceMetric(BaseMetric):
    """Evaluates format compliance: 3 bullets, max 80 chars each"""
    
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.evaluation_cost = 0
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measures format compliance
        Returns score based on adherence to format requirements
        """
        actual_output = test_case.actual_output.strip()
        
        # Split into lines and filter out empty ones
        lines = [line.strip() for line in actual_output.split('\n') if line.strip()]
        
        # Remove any headers or extra text, focus on bullet points
        bullet_lines = []
        for line in lines:
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                bullet_lines.append(line)
            elif len(line) > 10 and not line.endswith(':'):  # Likely a bullet without symbol
                bullet_lines.append(line)
        
        # If no clear bullets found, treat all substantial lines as bullets
        if not bullet_lines:
            bullet_lines = [line for line in lines if len(line) > 10]
        
        score_components = []
        
        # Check number of bullets (should be exactly 3)
        bullet_count_score = 1.0 if len(bullet_lines) == 3 else 0.0
        score_components.append(bullet_count_score)
        
        # Check character count for each bullet
        char_count_scores = []
        for bullet in bullet_lines:
            # Remove bullet symbols for character counting
            clean_bullet = re.sub(r'^[•\-\*]\s*', '', bullet)
            char_count = len(clean_bullet)
            char_score = 1.0 if char_count <= 80 else max(0.0, 1.0 - (char_count - 80) / 40)
            char_count_scores.append(char_score)
        
        avg_char_score = sum(char_count_scores) / len(char_count_scores) if char_count_scores else 0.0
        score_components.append(avg_char_score)
        
        # Overall score
        self.score = sum(score_components) / len(score_components)
        
        self.reason = f"Bullets: {len(bullet_lines)}/3, Avg char compliance: {avg_char_score:.2f}"
        self.success = self.score >= self.threshold
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Format Compliance"


class ThemeStructureMetric(BaseMetric):
    """Evaluates adherence to Unit-Project-Location theme structure"""
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        self.evaluation_cost = 0
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measures adherence to Unit-Project-Location theme structure
        """
        actual_output = test_case.actual_output.lower()
        
        # Extract bullet points
        lines = [line.strip() for line in actual_output.split('\n') if line.strip()]
        bullet_lines = []
        
        for line in lines:
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                bullet_lines.append(line)
            elif len(line) > 10 and not line.endswith(':'):
                bullet_lines.append(line)
        
        if not bullet_lines:
            bullet_lines = [line for line in lines if len(line) > 10]
        
        theme_scores = []
        
        # Define theme keywords
        unit_keywords = ['sqft', 'spacious', 'bedroom', 'unit', 'space', 'layout', 'floor', 'view']
        project_keywords = ['residence', 'building', 'development', 'amenities', 'facilities', 'estate']
        location_keywords = ['mrt', 'location', 'district', 'neighborhood', 'area', 'mins', 'walk', 'proximity']
        
        for i, bullet in enumerate(bullet_lines):
            if i == 0:  # First bullet should focus on unit
                score = 1.0 if any(keyword in bullet for keyword in unit_keywords) else 0.5
            elif i == 1:  # Second bullet should focus on project
                score = 1.0 if any(keyword in bullet for keyword in project_keywords) else 0.5
            elif i == 2:  # Third bullet should focus on location
                score = 1.0 if any(keyword in bullet for keyword in location_keywords) else 0.5
            else:
                score = 0.5  # Extra bullets get neutral score
            
            theme_scores.append(score)
        
        self.score = sum(theme_scores) / len(theme_scores) if theme_scores else 0.0
        self.reason = f"Theme structure adherence across {len(bullet_lines)} bullets"
        self.success = self.score >= self.threshold
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Theme Structure"
