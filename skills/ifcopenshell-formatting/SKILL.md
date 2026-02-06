---
name: IfcOpenShell Formatting
description: "Format extracted IFC values (text, numbers, measures) using Selector Syntax."
---

# IfcOpenShell Formatting

Format extracted IFC values using **Selector Syntax**.

## Function Index

| Function | File | Description |
|----------|------|-------------|
| `format_text()` | [format_text.py](scripts/format_text.py) | Text formatting (upper, lower, title, concat) |
| `format_numbers()` | [format_numbers.py](scripts/format_numbers.py) | Number formatting (round, int, custom) |
| `format_metric()` | [format_metric.py](scripts/format_metric.py) | Metric length formatting |
| `format_imperial()` | [format_imperial.py](scripts/format_imperial.py) | Imperial length formatting (feet/inches) |

---

## Formatting Functions Reference

| Function | Example | Result |
|----------|---------|--------|
| `upper(value)` | `upper("Foo")` | `FOO` |
| `lower(value)` | `lower("Foo")` | `foo` |
| `title(value)` | `title("foo bar")` | `Foo Bar` |
| `concat(v1, v2, ...)` | `concat("a", "b")` | `ab` |
| `round(value, precision)` | `round(3.14, 0.1)` | `3.1` |
| `int(value)` | `int(3.9)` | `3` |
| `number(v, dec, mil)` | `number(1234.5, ",", ".")` | `1.234,5` |
| `metric_length(v, prec, dec)` | `metric_length(3.1, 0.1, 2)` | `3.10` |
| `imperial_length(...)` | See script | `3' - 6"` |

---

## Imperial Length Parameters

`imperial_length(value, precision, input_unit, output_unit, suppress_zero_inches)`

- **value**: Length value
- **precision**: Fractional precision (4 = 1/4")
- **input_unit**: "foot" or "inch"
- **output_unit**: "foot" or "inch"
- **suppress_zero_inches**: true/false

---

## Quick Reference

**Basic usage:**
```python
import ifcopenshell.util.selector
formatted = ifcopenshell.util.selector.format('function("value")')
```

For complete examples, see the [scripts/](scripts/) directory.
