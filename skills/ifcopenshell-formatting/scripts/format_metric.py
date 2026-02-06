"""
Format metric length values.

Example: metric_length with precision and decimals.
"""
import ifcopenshell.util.selector

def format_metric_example():
    """Demonstrate metric length formatting."""
    # metric_length(value, precision, decimal_places)
    result = ifcopenshell.util.selector.format('metric_length(3.123, 0.1, 2)')
    print(f"metric_length: {result}")  # 3.10

if __name__ == "__main__":
    format_metric_example()
