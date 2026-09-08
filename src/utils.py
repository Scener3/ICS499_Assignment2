"""
Utility Functions
Helper functions for the anonymizer
"""

import re
import hashlib
from typing import Any, Dict, List, Optional


def clean_sql_value(value: str) -> str:
    """Clean a SQL value by removing quotes"""
    if not value:
        return value
    
    value = value.strip()
    
    if value.upper() == 'NULL':
        return value
    
    if len(value) >= 2:
        if (value[0] == "'" and value[-1] == "'") or \
           (value[0] == '"' and value[-1] == '"'):
            return value[1:-1]
    
    return value


def is_quoted(value: str) -> bool:
    """Check if a value is quoted"""
    if not value or len(value) < 2:
        return False
    
    return (value[0] == "'" and value[-1] == "'") or \
           (value[0] == '"' and value[-1] == '"')


def get_quote_char(value: str) -> Optional[str]:
    """Get the quote character used for a value"""
    if is_quoted(value):
        return value[0]
    return None


def escape_sql_string(value: str) -> str:
    """Escape special characters in SQL string"""
    value = value.replace('\\', '\\\\')
    value = value.replace("'", "\\'")
    value = value.replace('"', '\\"')
    return value


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def normalize_column_name(column: str) -> str:
    """Normalize column name"""
    column = column.strip().strip('`').strip('"').strip("'")
    return column.lower()