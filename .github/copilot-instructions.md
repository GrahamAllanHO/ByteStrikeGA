# ByteStrikeGA Copilot Instructions

## Repository shape

This repository is a workshop content tree, not a single application. The important top-level split is:

- `starter-files/`: learner starting points, often incomplete or intentionally simplified
- `solution files/`: reference answers and example artifacts
- `blueprint-data.txt`: shared sample input for the early blueprint-decoder exercises

Both trees are organized by language (`Javascript`, `Python`, `C#`), then by `part-01` through `part-06`, then by task folders.

Treat `starter-files/` and `solution files/` as parallel tracks. When editing, stay within the track the user names instead of wiring code across both trees unless they explicitly ask for both.

## High-level architecture

The repo progresses through the same workshop themes in multiple languages rather than implementing one shared system:

- Parts 1-3 center on a local-file "blueprint decoder" flow that reads content, extracts `{* ... *}` secrets with regex, then grows into safer wrappers, categorization, tests, and docs.
- Part 4 shifts to remote retrieval exercises. JavaScript and C# move to the "League" theme (`leagueMission.js`, `LeagueHQ.cs`), while Python continues in `blueprint_decoder.py`.
- Part 5 adds security and operational concerns such as URL validation, structured logging, and security-focused tests.
- Part 6 adds production-readiness artifacts such as test suites, CI/CD workflow examples, monitoring, runbooks, security/compliance docs, and deployment scaffolding.

The intent is curricular progression: later parts build on patterns introduced earlier, but each task folder is still fairly self-contained.

## Build, test, and lint commands

There is no repository-wide build, test, or lint toolchain configured at the root:

- no root `package.json`
- no root Python project file such as `pyproject.toml` or `requirements.txt`
- no `.sln` or `.csproj`
- no checked-in `.github/workflows/` directory

Use task-local commands only when the task folder clearly provides or implies its own setup. The part-06 materials include example commands that are instructional, not confirmed root commands:

### JavaScript task examples

From `solution files/Javascript/part-06/task-01-test-suite/README.md`:

```bash
npm test
npm test -- --coverage
npm run test:watch
npm test -- blueprint_decoder.test.js
```

### C# task examples

From `solution files/C#/part-06/task-01-test-suite/README.md`:

```bash
dotnet test --verbosity normal
dotnet test --collect:"XPlat Code Coverage"
```

### Python task examples

Part-06 materials reference pytest-based examples:

```bash
pytest --cov=blueprint_decoder --cov-report=html
```

### Java demo task example

The repo now also contains a task-local Java demo project at `starter-files/Java/demo` with its own Maven setup:

```bash
cd 'starter-files/Java/demo'
mvn test
mvn -q exec:java
```

Do not assume any of these commands work from the repository root without adding the missing project scaffolding for the specific task you are working on.

## Java demo structure

The Java demo is a focused CLI example and is intentionally scoped to `starter-files/Java/demo` rather than the broader part-based workshop tree.

- `pom.xml`: local Maven project with JUnit 5, Picocli, and `exec-maven-plugin`
- `src/main/java/demo/Demo.java`: Picocli command entry point and orchestration only
- `src/main/java/demo/BlueprintReader.java`: blueprint file discovery and secret extraction
- `src/main/java/demo/SecretEntry.java`: parsed `label` / `value` model
- `src/main/java/demo/SecretFormatter.java`: table layout and Picocli ANSI styling
- `src/test/java/demo/*.java`: unit tests split by responsibility

When editing this Java demo, preserve the single-responsibility split instead of collapsing logic back into one class unless the user explicitly asks for that simplification.

## Key conventions

- Quote paths in shell commands. `solution files/` contains a space, and `C#` contains `#`.
- Part and task folder names matter. There are two sibling `part-01/task-02-*` folders in several language trees, so do not rely on "task 2" as a unique identifier without the full folder name.
- Naming conventions follow language norms, but the repo is intentionally mixed:
  - Python uses snake_case filenames and functions.
  - C# uses PascalCase filenames and types.
  - JavaScript mixes `blueprint_decoder.js` with camelCase files such as `leagueMission.js` and may use either CommonJS or ESM depending on the exercise.
  - Java follows standard Maven folder layout in `starter-files/Java/demo` and uses PascalCase class names.
- Starter files are often TODO skeletons, while solution files may be complete code, partial artifacts, or README-only guidance depending on the part and language.
- Part 4 and later are not perfectly symmetric across languages. Do not assume the same filenames, task names, or abstraction boundaries exist in JavaScript, Python, and C#.
- Common exercise patterns across files are:
  - regex extraction of `{* ... *}` markers
  - small wrapper functions such as read/extract/categorize/safe decode flows
  - retry/backoff for remote fetches
  - URL allowlists and logging that avoids exposing secrets

## Source docs incorporated here

The root `README.md` describes the repository as a GitHub Copilot workshop with guided exercises and advanced prompting content. No `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, Cursor rules, Windsurf rules, Aider conventions, Cline rules, or existing Copilot instruction file were present when these instructions were written.
