---
name: IfcOpenShell Discovery
description: "LAST RESORT: Discover actual IFC naming conventions (materials, types, Psets) when zero-result queries suggest terminology mismatches. Use only after standard filtering fails."
---

# IfcOpenShell Discovery

> ⚠️ **LAST RESORT**: Use this skill ONLY when you cannot find elements using standard filtering skills.

## When to Use Discovery

**DO NOT start here.** First try:
1. `ifcopenshell-filtering` → Filter by class, type, material name
2. `ifcopenshell-extracting` → Extract specific attributes

**USE Discovery ONLY when:**
- Standard filters return 0 results unexpectedly
- You don't know the exact naming convention (e.g., "epoxy paint" vs "Tinta Epóxi")
- The user's query uses different terminology than the IFC model

## The Exploration Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│  1. TRY STANDARD APPROACH FIRST                                 │
│     └─ Use ifcopenshell-filtering with user's terms             │
│                                                                 │
│  2. IF ZERO RESULTS → EXPLORE                                   │
│     └─ List unique values to discover actual nomenclature       │
│                                                                 │
│  3. IDENTIFY PATTERN                                            │
│     └─ Find the correct naming convention                       │
│                                                                 │
│  4. RE-QUERY WITH CORRECT TERMS                                 │
│     └─ Apply the discovered pattern                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Discovery Strategies

**The core pattern is simple**: When a query returns zero results, write an inline script to list all unique values for that attribute in the IFC model.

**Common examples** (but applicable to ANY IFC attribute):

### 1. List Unique Materials
When filtering by material returns 0 results, list all unique materials to discover the actual naming convention.

### 2. List Unique PropertySets
When property queries fail, list all Psets to discover what properties actually exist.

### 3. List Unique Types/Classes
When filtering by type fails, list all unique element types to discover the correct classification.

**You can apply this to anything**: attributes, classifications, spatial structures, relationships, etc. The goal is always to discover the actual nomenclature used in the model.


## Best Practices

1. **Explore once, cache results** - Don't call discovery multiple times
2. **Look for patterns** - Materials often share prefixes
3. **Check case sensitivity** - "paint" ≠ "Paint" ≠ "PAINT"
4. **Consider language** - Models may use Portuguese, English, Spanish, or other languages
5. **Write inline scripts** - No need for separate files, write exploration code directly in sandbox
