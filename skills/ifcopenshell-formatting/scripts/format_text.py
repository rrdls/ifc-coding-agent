"""
Format text values.

Example: upper, lower, title, concat.
"""
import ifcopenshell.util.selector

def format_text_example():
    """Demonstrate text formatting functions."""
    # Upper case
    result = ifcopenshell.util.selector.format('upper("Foo")')
    print(f"upper: {result}")  # FOO
    
    # Lower case
    result = ifcopenshell.util.selector.format('lower("Foo")')
    print(f"lower: {result}")  # foo
    
    # Title case
    result = ifcopenshell.util.selector.format('title("foo bar")')
    print(f"title: {result}")  # Foo Bar
    
    # Concatenate
    result = ifcopenshell.util.selector.format('concat("foo", "bar")')
    print(f"concat: {result}")  # foobar

if __name__ == "__main__":
    format_text_example()
