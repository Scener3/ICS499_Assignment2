# Data Anonymizer for SQL files

## Programming Language and Technologies
- *Python 3.x*: Programming Language
- *Claude*: Used for research/debugging/assisted code

## External Libraries
- *Faker* (Version 22.0.0): Used for generating fake synthetic data such as  
names, emails, phone, and addresses.

## How our program works
- Our program READ -> DETECT -> ANONYMIZE -> WRITE
1. Read: Reads the file and splits into individual statements
2. Detect: Each INSERT statement parses the column name and identity PII columns
3. Anonymize: For each PII, we check if it has been used before. If yes then we use the existing value, otherwise create a new synthetic value and store it.
4. Write: Reconstruct the SQL with the anonymized values and write to an output sql file.

## Installation
### Clone repo
git clone <repo-url>
### Install dependencies
pip install -r requirements.txt

## How to run
python3 main.py <input_file.sql> <output_file.sql>  
Example: python3 main.py data/sample.sql output/anonymized.sql

### Expected input
1. CREATE TABLE statements: Define the table structure
2. INSERT statements - Containing the actual data with PII  
It is important to have both, but the program will be modifying the INSERT statements. CREATE TABLE is important due understanding the variable structure.

CREATE TABLE customers (
    customer_id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    address VARCHAR(200)
);

INSERT INTO customers VALUES
(1, 'John Smith', 'john.smith@gmail.com', '612-555-1234', '123 Main St, Minneapolis, MN');

### Generated Output
The program will produce a new SQL file with  
1. All PII replaced with realistic synthetic data
2. Provides same structure and syntax as input
3. Non-PII data unchanged
4. Consistent anonymization across the entire file
5. Seeded output, generating multiple time will result in the same previous output

## Anonymization Strategy
1. PII Detection:
    - Name: Columns containing 'name', 'first', 'last'
    - Emails: Columns containing 'email', 'mail'
    - Phones: Columns containing 'phone', 'mobile', 'cell'
    - Addresses: Columns containing 'address', 'street', 'city', 'zip'
2. Synthetic Data Generation:
    - We utilize Faker library to generate the realistic synthetic data such as names, emails, phones and addresses

## Maintain Consistency
    - By maintaining a mapping dictionary of the a person to the synthetic data helps ensure that same input always produces the same output. This provides consistency across the table and also email addresses matching the anonymized names.
### SQL Structure Preservation
    - Only the INSERT statements are modified
    - CREATE TABLE statements remain unchanged
    - Non-PII columns are untouched
    - SQL syntax is maintained

# Design Decisions: Why We Selected Our Approach

This document explains the key design decisions made during the development of the data anonymizer.

## Comparison of Approaches

| Decision | Why We Chose It | Alternative Considered | Why We Rejected Alternative |
|----------|----------------|----------------------|---------------------------|
| **Column Name Matching** | Reliable, avoids false positives | Value matching | Could mistake product names for person names (e.g., "Phone Case" as phone number) |
| **In-Memory Mapping** | Simple, fast, no storage needed | Database/file storage | Overkill for one-way anonymization; adds unnecessary complexity |
| **Email-Name Link** | Maintains realism between names and emails | Random unrelated emails | Less realistic; breaks the natural connection between a person's name and email |
| **Regex SQL Parsing** | No dependencies, handles INSERT statements well | Full SQL parser library (e.g., sqlparse) | Added complexity and dependency not needed for this assignment |
| **Seeded Random (42)** | Reproducible results for testing and debugging | Random seed each time | Harder to test and debug; inconsistent behavior |

---

## Explanation

### 1. Column Name Matching over Value Matching

**Our Choice:** Identify PII by looking at column names (e.g., `email`, `phone`, `name`)

**Why:** 
- Column names are usually descriptive and consistent in SQL schemas
- A column named `email` almost certainly contains email addresses
- Checking column names is faster than examining every value

**Alternative:** Look at the actual data values to identify PII

**Why Rejected:**
- Could misidentify product names (e.g., "iPhone 15") as phone numbers
- Could mistake business names (e.g., "Smith & Co") as person names
- Slower: requires examining every value in every row

---

### 2. In-Memory Mapping over Database/File Storage

**Our Choice:** Use a Python dictionary to store original→anonymized value mappings

**Why:**
- Simple: Just a dictionary, no external dependencies
- Fast: O(1) lookup time for consistency checks
- Sufficient: For typical SQL files (thousands of rows), memory usage is minimal
- One-way: We don't need to reverse the mapping, so no need to persist it

**Alternative:** Store mappings in a database or file

**Why Rejected:**
- Overkill for one-way anonymization
- Adds complexity (need to manage file I/O or database connections)
- Slower: File/database lookups are slower than in-memory dictionary lookups

---

### 3. Email-Name Link over Random Unrelated Emails

**Our Choice:** Generate email addresses based on the anonymized name

**Why:**
- Realistic: People often have emails based on their names (e.g., john.smith@gmail.com)
- Maintains relationship: If "John Smith" becomes "Allison Hill", then "john.smith@gmail.com" should become "allison.hill@gmail.com"
- Believable test data: Names and emails that match look more realistic

**Alternative:** Generate random unrelated email addresses

**Why Rejected:**
- Less realistic: A person named "Allison Hill" with email "random123@yahoo.com" looks suspicious
- Breaks the natural connection between name and email
- Reduces believability of the anonymized data

---

### 4. Regex SQL Parsing over Full SQL Parser Library

**Our Choice:** Use regular expressions to parse INSERT statements

**Why:**
- No dependencies: Don't need to install sqlparse, sqlglot, or other libraries
- Simple: INSERT statements follow a predictable pattern
- Sufficient: Assignment only requires handling INSERT statements
- Easy to debug: Regex patterns are visible and testable

**Alternative:** Use a full SQL parser library (e.g., sqlparse, sqlglot)

**Why Rejected:**
- Added complexity: Full SQL parsers are more complex than needed
- Dependency: Adds external library requirement
- Overkill: We only need to parse INSERT statements, not complex queries

---

### 5. Seeded Random (42) over Random Seed

**Our Choice:** Use a fixed seed (42) for Faker and Python's random module

**Why:**
- Reproducible: Running the program twice with same input produces same output
- Testable: Can write tests that expect specific outputs
- Debuggable: Can reproduce the exact same scenario if something goes wrong
- Demonstrates consistency: Shows the program behaves predictably

**Alternative:** Use a random seed each time the program runs

**Why Rejected:**
- Harder to test: Can't write tests that expect specific outputs
- Harder to debug: Can't reproduce the same scenario
- Inconsistent: Same input would produce different outputs on different runs

---

## Summary

Our design philosophy follows these principles:

1. **Simple over Complex**: Use the simplest solution that works
2. **Reliable over Clever**: Choose approaches that are predictable
3. **Realistic over Random**: Generate data that looks believable
4. **Consistent over Varied**: Same input always gives same output

These decisions result in a solution that is:
- Easy to understand
- Easy to test
- Easy to explain
- Easy to maintain

## Known Limitations
1. INSERT statement is the only one being processed, other statements are unchanged.
2. Handles only standard INSERT VALUES statement and not complex INSERT statements
3. Column name dependency is one of the issue that it can come up, since it is a recoginition based on patterns that we have listed, if the keyword is not listed within it then it will miss it completely and not process it.
4. Currently our program only generate common email formats such as first-last and last-first name and doesn't exactly follow random # followup afterwards.