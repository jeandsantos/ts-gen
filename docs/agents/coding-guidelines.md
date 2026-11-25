# Coding guidelines

## Design preferences

- Prefer `Enum` or `StrEnum` for finite sets of named values instead of repeating string literals. Use `StrEnum` when values need to interoperate with strings; otherwise use `Enum`.
- Prefer classes over standalone functions for reusable behavior. Group related state and operations in a class, and put behavior on the type it belongs to. Use a standalone function for a small stateless helper when a class would add no meaningful structure.
- Keep functions and methods small, with one clear responsibility. Extract a helper when it makes the logic easier to understand; avoid splitting straightforward code into trivial fragments.
