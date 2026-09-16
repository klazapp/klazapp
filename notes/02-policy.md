# 02 / The package isn't in your package.json

**Project:** [TypeScript Package Scan](https://github.com/klazapp/typescript-package-scan)

## The constraint

Reading direct dependencies misses packages introduced transitively. Teams also need to express exactly which package/version combinations they want to detect, without burying the rule in ad hoc shell commands.

## What the implementation does

The tool reads targets from YAML or JSON, collects a resolved dependency tree, and compares occurrences with the configured package names and versions. It keeps paths on matching results and exposes separate result categories:

```typescript
return { found, presentDifferent, notFound };
```

The CLI formats the result for humans, can write JSON and CSV reports, and uses nonzero statuses for matches or execution errors. Consumers can also use the library separately from its CLI presentation.

## The matching boundary

The inspected `compare.ts` uses `Set.has` for version matching. An empty version set matches any version. This is exact-string matching, not evaluation of semantic-version ranges.

There is also a distinction between a matching report and an exhaustive inventory: when the same package has both a matching and a nonmatching occurrence, this implementation records the matching occurrences in `found`. It only fills `presentDifferent` for that target when no occurrence matched.

## The trade-off

An explicit policy is easy to review, but it must be kept current. “No matches” means no configured target matched the inspected tree. It does not establish that every dependency is safe, maintained, licensed appropriately or free from vulnerabilities.

The JSON artwork on the profile reproduces an example from the repository documentation. Its package/version values are historical example data, not a current advisory or a scan run performed for this profile.

## Inspect it

[Matching logic](https://github.com/klazapp/typescript-package-scan/blob/main/src/compare.ts) · [Tree collection](https://github.com/klazapp/typescript-package-scan/blob/main/src/tree.ts) · [CLI and reports](https://github.com/klazapp/typescript-package-scan/blob/main/src/cli.ts)

[Back to the profile](../README.md#tooling)
