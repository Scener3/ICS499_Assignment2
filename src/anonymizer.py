"""
Core Anonymization Engine
Maintains consistency and coordinates anonymization
"""

from typing import Dict, Any, Optional, List


try:
    from .pii_detector import PIIDetector
    from .data_generator import DataGenerator
except ImportError:
    from pii_detector import PIIDetector
    from data_generator import DataGenerator


class DataAnonymizer:
    """Core anonymization engine with consistency management"""
    
    def __init__(self, detector: PIIDetector, generator: DataGenerator):
        """
        Initialize the anonymizer
        
        Args:
            detector: PII detection component
            generator: Data generation component
        """
        self.detector = detector
        self.generator = generator
        
        # Maintain mappings for consistency - 4 PII types
        self.value_mappings = {
            'name': {},
            'email': {},
            'phone': {},
            'address': {}
        }
        
        # Track statistics
        self.stats = {
            'total_anonymized': 0,
            'name': 0,
            'email': 0,
            'phone': 0,
            'address': 0
        }
    
    def anonymize_value(self, value: str, pii_type: str, context: Optional[Dict] = None) -> str:
        """
        Anonymize a single value consistently
        
        Args:
            value: Original value
            pii_type: Type of PII
            context: Additional context
            
        Returns:
            Anonymized value
        """
        # Handle NULL values
        if not value or value.upper() == 'NULL':
            return value
        
        clean_value = value.strip("'\"")
        
        if not clean_value:
            return value
        
        # Ensure pii_type exists in mappings
        if pii_type not in self.value_mappings:
            self.value_mappings[pii_type] = {}
            self.stats[pii_type] = 0
        
        # Check if we have a mapping for this value
        if clean_value in self.value_mappings[pii_type]:
            anonymized = self.value_mappings[pii_type][clean_value]
        else:
            anonymized = self.generator.generate(pii_type, context)
            
            self.value_mappings[pii_type][clean_value] = anonymized
            
            self.stats['total_anonymized'] += 1
            if pii_type in self.stats:
                self.stats[pii_type] = self.stats.get(pii_type, 0) + 1
        
        # Preserve original formatting
        if value.startswith("'") and value.endswith("'"):
            return f"'{anonymized}'"
        elif value.startswith('"') and value.endswith('"'):
            return f'"{anonymized}"'
        
        return anonymized
    
    def anonymize_row(self, values: List[str], pii_columns: Dict[int, str]) -> List[str]:
        """
        Anonymize a row of values
        
        Args:
            values: List of values in the row
            pii_columns: Dictionary mapping column index to PII type
            
        Returns:
            List of anonymized values
        """
        anonymized_values = values.copy()
        
        name_mapping = {}
        for idx, pii_type in pii_columns.items():
            if pii_type == 'name' and idx < len(values):
                original_name = values[idx].strip("'\"")
                anonymized_name = self.anonymize_value(values[idx], 'name')
                name_mapping[original_name] = anonymized_name.strip("'\"")
                anonymized_values[idx] = anonymized_name
        
        for idx, pii_type in pii_columns.items():
            if pii_type == 'name' or idx >= len(values):
                continue
            
            context = {}
            
            if pii_type == 'email':
                for name_idx, name_type in pii_columns.items():
                    if name_type == 'name' and name_idx < len(values):
                        original_name = values[name_idx].strip("'\"")
                        if original_name in name_mapping:
                            context['name'] = name_mapping[original_name]
                            break
            
            anonymized_values[idx] = self.anonymize_value(values[idx], pii_type, context)
        
        return anonymized_values
    
    def get_mapping_stats(self) -> Dict:
        """Get statistics about the anonymization process"""
        return {
            'total_anonymized': self.stats['total_anonymized'],
            'unique_mappings': {
                pii_type: len(mappings) 
                for pii_type, mappings in self.value_mappings.items()
                if len(mappings) > 0
            }
        }