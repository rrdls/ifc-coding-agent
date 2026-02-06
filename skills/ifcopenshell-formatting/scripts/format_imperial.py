"""
Format imperial length values.

Example: imperial_length with feet and inches.
"""
import ifcopenshell.util.selector

def format_imperial_example():
    """Demonstrate imperial length formatting."""
    # imperial_length(value, precision, input_unit, output_unit, suppress_zero_inches)
    
    # Feet only
    result = ifcopenshell.util.selector.format(
        'imperial_length(3.0, 4, "foot", "foot", true)'
    )
    print(f"3 feet: {result}")  # 3'
    
    # With zero inches shown
    result = ifcopenshell.util.selector.format(
        'imperial_length(3.0, 4, "foot", "foot", false)'
    )
    print(f"3 feet (with zero): {result}")  # 3' - 0"
    
    # Convert to inches
    result = ifcopenshell.util.selector.format(
        'imperial_length(3.5, 4, "foot", "inch", true)'
    )
    print(f"3.5 feet in inches: {result}")  # 42"

if __name__ == "__main__":
    format_imperial_example()
