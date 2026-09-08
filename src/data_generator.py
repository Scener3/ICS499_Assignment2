"""
Synthetic Data Generation Module
Generates realistic fake data for anonymization
"""

from faker import Faker
from typing import Dict, Any, Optional
import re
import random


class DataGenerator:
    """Generates realistic synthetic data using Faker"""
    
    def __init__(self, seed: int = 42, locale: str = 'en_US'):
        """
        Initialize the data generator
        
        Args:
            seed: Random seed for reproducibility
            locale: Locale for Faker (default: en_US)
        """
        self.fake = Faker(locale)
        Faker.seed(seed)
        self.seed = seed
        
        # List of realistic email domains
        self.email_domains = [
            'gmail.com',
            'yahoo.com',
            'hotmail.com',
            'outlook.com',
            'aol.com',
            'icloud.com',
            'protonmail.com',
            'mail.com',
            'zoho.com',
            'gmx.com',
            'fastmail.com',
            'live.com',
            'msn.com'
        ]
        
        # Initialize random with seed for reproducibility
        random.seed(seed)
    
    def generate_name(self) -> str:
        """Generate a realistic full name"""
        return self.fake.name()
    
    def generate_email(self, name: Optional[str] = None) -> str:
        """
        Generate a realistic email address
        
        Args:
            name: Name to base email on (optional)
        """
        if name:
            # Generate email from name
            parts = name.lower().split()
            if len(parts) >= 2:
                first = parts[0]
                last = parts[-1]
                first = re.sub(r'[^a-z]', '', first)
                last = re.sub(r'[^a-z]', '', last)
                if first and last:
                    domain = random.choice(self.email_domains)
                    
                    format_choice = random.randint(1, 3)
                    
                    if format_choice == 1:
                        # first.last@domain
                        return f"{first}.{last}@{domain}"
                    elif format_choice == 2:
                        # firstlast@domain
                        return f"{first}{last}@{domain}"
                    else:
                        # first_last@domain
                        return f"{first}_{last}@{domain}"
        
        # Fallback to Faker's email generator
        return self.fake.email()
    
    def generate_phone(self) -> str:
        """Generate a realistic phone number"""
        return self.fake.phone_number()
    
    def generate_address(self) -> str:
        """Generate a realistic street address"""
        return self.fake.street_address()
    
    def generate(self, pii_type: str, context: Optional[Dict] = None) -> str:
        """
        Generate synthetic data based on PII type
        
        Args:
            pii_type: Type of PII to generate
            context: Additional context (e.g., name for email generation)
            
        Returns:
            Generated synthetic value
        """
        if pii_type == 'name':
            return self.generate_name()
        elif pii_type == 'email':
            name = context.get('name') if context else None
            return self.generate_email(name)
        elif pii_type == 'phone':
            return self.generate_phone()
        elif pii_type == 'address':
            return self.generate_address()
        else:
            return self.fake.text(max_nb_chars=50)