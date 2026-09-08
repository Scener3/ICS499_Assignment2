"""
SQL Processing Module
Handles SQL parsing, processing, and reconstruction
"""

import re
from typing import List, Dict, Tuple, Optional


try:
    from .anonymizer import DataAnonymizer
except ImportError:
    from anonymizer import DataAnonymizer


class SQLProcessor:
    """Processes SQL files for anonymization"""
    
    def __init__(self, anonymizer: DataAnonymizer, verbose: bool = False):
        """
        Initialize SQL processor
        
        Args:
            anonymizer: Data anonymization engine
            verbose: Enable verbose output
        """
        self.anonymizer = anonymizer
        self.verbose = verbose
        self.tables_processed = 0
        self.rows_processed = 0
    
    def process_file(self, input_file: str, output_file: str):
        """
        Process an entire SQL file
        
        Args:
            input_file: Path to input SQL file
            output_file: Path to output SQL file
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        processed_content = self.process_sql_content(sql_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        if self.verbose:
            print(f"\nProcessed {self.rows_processed} rows across {self.tables_processed} tables")
    
    def process_sql_content(self, sql_content: str) -> str:
        """
        Process SQL content
        
        Args:
            sql_content: Raw SQL content
            
        Returns:
            Processed SQL content
        """
        statements = self.split_sql_statements(sql_content)
        
        processed_statements = []
        for statement in statements:
            if statement.strip():
                processed = self.process_statement(statement)
                processed_statements.append(processed)
        
        return '\n\n'.join(processed_statements)
    
    def split_sql_statements(self, sql_content: str) -> List[str]:
        """Split SQL content into individual statements"""
        statements = []
        current = []
        
        for line in sql_content.split('\n'):
            current.append(line)
            if line.rstrip().endswith(';'):
                statements.append('\n'.join(current))
                current = []
        
        if current:
            statements.append('\n'.join(current))
        
        return statements
    
    def process_statement(self, statement: str) -> str:
        """Process a single SQL statement"""
        stripped = statement.strip()
        
        # Check if it's an INSERT statement
        if stripped.upper().startswith('INSERT'):
            return self.process_insert_statement(statement)
        else:
            return statement
    
    def process_insert_statement(self, statement: str) -> str:
        """Process an INSERT statement"""
        # Parse the INSERT statement
        table_name, columns, values_rows = self.parse_insert(statement)
        
        if table_name is None:
            return statement
        
        self.tables_processed += 1
        
        # Identify PII columns
        pii_columns = self.anonymizer.detector.identify_pii_columns(columns)
        
        if not pii_columns:
            return statement
        
        if self.verbose:
            print(f"\nTable: {table_name}")
            print(f"PII columns: {pii_columns}")
        
        # Process each row
        processed_rows = []
        for row in values_rows:
            processed_row = self.process_row(row, pii_columns)
            processed_rows.append(processed_row)
            self.rows_processed += 1
        
        # Reconstruct the INSERT statement
        return self.reconstruct_insert(table_name, columns, processed_rows)
    
    def parse_insert(self, statement: str) -> Tuple[Optional[str], List[str], List[List[str]]]:
        """Parse an INSERT statement"""
        # Normalize whitespace
        normalized = ' '.join(statement.split())
        
        pattern = r'INSERT\s+INTO\s+`?(\w+)`?\s*\(([^)]+)\)\s*VALUES\s*(.+?);?$'
        match = re.match(pattern, normalized, re.IGNORECASE | re.DOTALL)
        
        if not match:
            pattern = r'INSERT\s+INTO\s+`?(\w+)`?\s*VALUES\s*(.+?);?$'
            match = re.match(pattern, normalized, re.IGNORECASE | re.DOTALL)
            
            if match:
                table_name = match.group(1)
                columns = []
                values_str = match.group(2)
            else:
                return None, [], []
        else:
            table_name = match.group(1)
            columns = [col.strip().strip('`') for col in match.group(2).split(',')]
            values_str = match.group(3)
        
        rows = self.parse_values_rows(values_str)
        
        return table_name, columns, rows
    
    def parse_values_rows(self, values_str: str) -> List[List[str]]:
        """Parse multiple value rows"""
        rows = []
        current_row = []
        current_value = ''
        in_string = False
        escape_next = False
        parentheses_depth = 0
        
        i = 0
        while i < len(values_str):
            char = values_str[i]
            
            if escape_next:
                current_value += char
                escape_next = False
            elif char == '\\':
                current_value += char
                escape_next = True
            elif char == "'":
                in_string = not in_string
                current_value += char
            elif char == '(' and not in_string:
                parentheses_depth += 1
                if parentheses_depth == 1:
                    i += 1
                    continue
                else:
                    current_value += char
            elif char == ')' and not in_string:
                parentheses_depth -= 1
                if parentheses_depth == 0:
                    if current_value:
                        current_row.append(current_value.strip())
                        current_value = ''
                    if current_row:
                        rows.append(current_row)
                        current_row = []
                else:
                    current_value += char
            elif char == ',' and not in_string and parentheses_depth == 1:
                current_row.append(current_value.strip())
                current_value = ''
            elif parentheses_depth >= 1:
                current_value += char
            
            i += 1
        
        if current_value or current_row:
            if current_value:
                current_row.append(current_value.strip())
            if current_row:
                rows.append(current_row)
        
        return rows
    
    def process_row(self, row: List[str], pii_columns: Dict[int, str]) -> List[str]:
        """Process a single row of values"""
        return self.anonymizer.anonymize_row(row, pii_columns)
    
    def reconstruct_insert(self, table_name: str, columns: List[str], 
                           rows: List[List[str]]) -> str:
        """Reconstruct INSERT statement"""
        if columns:
            column_str = ', '.join(f'`{col}`' if not col.startswith('`') else col 
                                   for col in columns)
            values_str = ',\n'.join(
                f"({', '.join(str(val) for val in row)})" 
                for row in rows
            )
            return f"INSERT INTO `{table_name}` ({column_str}) VALUES\n{values_str};"
        else:
            values_str = ',\n'.join(
                f"({', '.join(str(val) for val in row)})" 
                for row in rows
            )
            return f"INSERT INTO `{table_name}` VALUES\n{values_str};"
    
    def print_summary(self):
        """Print processing summary"""
        print("\n=== Anonymization Summary ===")
        print(f"Tables processed: {self.tables_processed}")
        print(f"Rows processed: {self.rows_processed}")
        
        stats = self.anonymizer.get_mapping_stats()
        print(f"Total values anonymized: {stats['total_anonymized']}")
        print("\nUnique mappings:")
        for pii_type, count in stats['unique_mappings'].items():
            print(f"  {pii_type}: {count}")