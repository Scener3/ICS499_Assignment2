#!/usr/bin/env python3
"""
Data Anonymizer - Main Entry Point
Anonymizes PII in SQL files

Usage: python main.py <input_file.sql> <output_file.sql>
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pii_detector import PIIDetector
from data_generator import DataGenerator
from anonymizer import DataAnonymizer
from sql_processor import SQLProcessor

def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file.sql> <output_file.sql>")
        print("Example: python main.py data/sample.sql output/anonymized.sql")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Initializing anonymizer...")
    detector = PIIDetector()
    generator = DataGenerator(seed=42)
    anonymizer = DataAnonymizer(detector, generator)
    processor = SQLProcessor(anonymizer, verbose=True)
    
    print(f"Processing {input_file}...")
    processor.process_file(input_file, output_file)
    
    print(f"\n✅ Anonymized SQL written to {output_file}")
    processor.print_summary()

if __name__ == "__main__":
    main()