"""
Format numeric values.

Example: round, int, number formatting.
"""
import ifcopenshell.util.selector

def format_numbers_example():
    """Demonstrate number formatting functions."""
    # Round
    result = ifcopenshell.util.selector.format('round(3.123, 0.1)')
    print(f"round: {result}")  # 3.1
    
    # Integer
    result = ifcopenshell.util.selector.format('int(3.123)')
    print(f"int: {result}")  # 3
    
    # Custom number format (decimal and thousands separators)
    result = ifcopenshell.util.selector.format('number(1234.56, ",", ".")')
    print(f"number: {result}")  # 1.234,56

if __name__ == "__main__":
    format_numbers_example()
