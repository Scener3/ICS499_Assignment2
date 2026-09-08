"""
PII Detection Module
Identifies which columns contain personally identifiable information
"""

import re
from typing import Optional, Dict, List


class PIIDetector:
    """Detects PII columns based on column names and patterns"""
    
    def __init__(self):
        """Initialize PII detection patterns"""
        self.pii_patterns = {
            'name': [
                r'^name$',
                r'^full_name$',
                r'^fullname$',
                r'.*first.*name.*',
                r'.*last.*name.*',
                r'.*customer.*name.*',
                r'.*contact.*name.*',
                r'.*user.*name.*',
                r'.*person.*name.*',
                r'.*patient.*name.*',
                r'.*emergency.*contact.*',
            ],
            'email': [
                r'.*email.*',
                r'.*e-mail.*',
                r'.*e_mail.*',
                r'.*mail.*',
            ],
            'phone': [
                r'.*phone.*',
                r'.*mobile.*',
                r'.*cell.*',
                r'.*telephone.*',
                r'.*contact.*number.*',
                r'.*fax.*',
            ],
            'address': [
                r'.*address.*',
                r'.*street.*',
                r'.*city.*',
                r'.*state.*',
                r'.*province.*',
                r'.*zip.*',
                r'.*postal.*',
                r'.*country.*',
                r'.*location.*',
                r'.*mailing.*',
                r'.*shipping.*',
                r'.*billing.*',
            ]
        }
    
    def detect_pii_type(self, column_name: str) -> Optional[str]:
        """
        Detect PII type based on column name
        
        Args:
            column_name: Name of the column
            
        Returns:
            PII type ('name', 'email', 'phone', 'address') or None
        """
        column_lower = column_name.lower().strip()
        column_lower = column_lower.strip('`').strip('"').strip("'")
        
        for pii_type, patterns in self.pii_patterns.items():
            for pattern in patterns:
                if re.match(pattern, column_lower, re.IGNORECASE):
                    return pii_type
        
        return None
    
    def detect_pii_from_value(self, value: str) -> Optional[str]:
        """
        Detect PII type based on value pattern
        
        Args:
            value: Value to check
            
        Returns:
            PII type or None
        """
        if not value or value.upper() == 'NULL':
            return None
        
        # Remove quotes for checking
        clean_value = value.strip("'\"")
        
        if not clean_value:
            return None
        
        # Check email pattern
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', clean_value):
            return 'email'
        
        # Check phone pattern
        if re.match(r'^[\+]?[\d\s\-\(\)]{7,}$', clean_value):
            return 'phone'
        
        # Check name pattern (two words starting with capitals)
        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$', clean_value):
            return 'name'
        
        return None
    
    def identify_pii_columns(self, columns: List[str]) -> Dict[int, str]:
        """
        Identify PII columns from a list of column names
        
        Args:
            columns: List of column names
            
        Returns:
            Dictionary mapping column index to PII type
        """
        pii_columns = {}
        
        for idx, column in enumerate(columns):
            pii_type = self.detect_pii_type(column)
            if pii_type:
                pii_columns[idx] = pii_type
        
        return pii_columns