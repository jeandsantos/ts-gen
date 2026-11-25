# Share ordered, named recipes across all entry points

Python construction, command-line flags, and versioned YAML resolve to one immutable recipe model and generation implementation, so equivalent inputs produce equivalent data without duplicating validation or signal semantics. A single `.add()` appends an operation in execution order, and nested recipes scope transformations to a contribution rather than requiring special targeting rules.

Random streams derive from the generation seed and each operation's full group/name path rather than operation position or a shared mutable generator. This preserves existing draws when unrelated operations are added, at the cost of making names part of the reproducibility contract: renaming or moving an operation changes its stream, and CLI-generated names can shift when another operation of the same type is inserted.

YAML uses an ordered operation list with explicit names, a schema version, and safe data loading; arbitrary Python callables remain available only through Python. Reproducibility covers identical recipes, ranges, seeds, and supported runtimes, not arbitrary slicing, chunking, dependency upgrades, or unchanged results after intentionally reordering transformations.
