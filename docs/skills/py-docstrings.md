# Skill: py-docstrings

## Purpose
Add detailed, professional docstrings to Python functions following Google docstring style. **Every docstring must include examples.**

## When to Use
- Adding documentation to undocumented functions
- Upgrading existing minimal docstrings to comprehensive ones
- Ensuring consistent documentation style across a codebase

## Format Template

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """One-line summary of what the function does.

    More detailed explanation of the function's behavior, context, and usage.
    Explain any important details about how it works or edge cases it handles.

    Args:
        param1: Description of the first parameter and what values it expects.
        param2: Description of the second parameter, including type hints and
                any constraints or special values.

    Returns:
        Description of what is returned. If a dict, list, or complex type,
        describe the structure. Example: "A dictionary where keys are category
        names (strings) and values are lists of items."

    Raises:
        SpecificException: Description of when this exception is raised.
        AnotherException: Description of when this exception is raised.
        (Use "None" if no exceptions are raised or if they're caught internally)

    Example:
        >>> function_name("input", 42)
        expected_output

        >>> function_name("other_input", -1)
        other_expected_output
    """
    # Function body here
```

## Instructions

1. **Summary Line**: Write a concise one-liner describing what the function does
2. **Description**: Add 2-3 sentences explaining the function's purpose, when to use it, and any important behavior
3. **Args**: 
   - List each parameter with its type
   - Provide a clear description of what values it expects
   - Mention defaults, constraints, or special handling if relevant
4. **Returns**:
   - Describe the return value and its type
   - For complex types (dict, list, custom objects), explain the structure
   - Include concrete examples when helpful
5. **Raises**:
   - List exceptions the function explicitly raises or propagates
   - Include a brief description of the condition that triggers each
   - Use "None" if the function doesn't raise exceptions
6. **Example (REQUIRED)** ⭐:
   - **ALWAYS include at least one example**
   - Provide realistic usage examples showing typical behavior
   - Include an example showing edge cases or error conditions if applicable
   - Format as doctest-compatible examples with `>>>` prompt
   - Include expected output on the next line
   - If the function prints output, show that in a comment

## Style Guidelines

- Use complete, grammatically correct sentences
- Be specific: avoid vague descriptions like "process the data"
- Keep parameter descriptions concise but informative
- For collections, specify what the elements are (e.g., "list of strings", not just "list")
- Use consistent terminology and voice (active, present tense)
- Include example outputs that are realistic or show the structure returned

## Common Patterns

**For file I/O functions:**
```
Returns:
    The complete file contents as a string.

Raises:
    FileNotFoundError: If the file does not exist.
    OSError: If the file cannot be opened or read.

Example:
    >>> content = read_file("data.txt")
    >>> len(content) > 0
    True
```

**For extraction/parsing functions:**
```
Returns:
    A list of strings, each representing a [unit]. If no matches are found,
    returns an empty list.

Example:
    >>> extract_items("item1, item2, item3")
    ['item1', 'item2', 'item3']

    >>> extract_items("no matches here")
    []
```

**For categorization/grouping functions:**
```
Returns:
    A dictionary where keys are [category type] and values are lists of
    [item type]. Example: {"Category1": ["item1", "item2"], "Category2": [...]}

Example:
    >>> categorize_items(["A: item1", "B: item2", "A: item3"])
    {'A': ['item1', 'item3'], 'B': ['item2']}
```

**For safe wrapper functions:**
```
Raises:
    None (exceptions are caught and handled internally; errors are
    reported via [print/logging/return value])

Example:
    >>> result = safe_process("valid_input")
    >>> result is not None
    True

    >>> result = safe_process("invalid_input")
    # Error message printed
    >>> result
    {}
```

## How to Apply

1. Identify the function(s) that need docstrings
2. For each function, gather:
   - What the function does
   - What parameters it expects (check type hints)
   - What it returns
   - What exceptions it raises (or handles)
   - **Good example usage (required!)**
3. Use the template above to structure the docstring
4. **Ensure at least one Example is included**
5. Run any existing tests to verify behavior hasn't changed
6. If available, use doctest to verify examples are accurate

## Tools to Use

- **view**: Read the function code first
- **edit**: Replace old docstring or add new one
- **bash**: Run tests with `python -m pytest` to verify

