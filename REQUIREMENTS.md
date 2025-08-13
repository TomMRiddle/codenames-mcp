


# AI Agent Development Workflow

## Purpose
This file provides a concise, actionable workflow for autonomous AI agents developing the Codenames MCP Server. It is optimized for context extraction, decision-making, and reproducible execution.

## Context Sources
- `pyproject.toml`: Single source of truth for dependencies, automation, and tool configuration.
- `docs/`: Authoritative documentation for architecture, requirements, and standards.

## Workflow Steps

## Reproducible Git Commit & Push Steps
1. Stage all changes:
   - `git add .`
2. Check status and review changes:
   - `git status --short`
   - `git diff --cached` (to see staged changes)
3. Write a commit message summarizing the actual changes:
   - Focus only on what was modified (e.g., updated docs, config, code, etc.)
4. Commit changes:
   - `git commit -m "<concise, accurate message>"`
5. Push to remote:
   - `git push`
6. Verify on remote (optional):
   - Check repository on GitHub or use `git log` to confirm.
1. **Analyze Requirements**
   - Extract user stories, acceptance criteria, and risk areas from documentation.
   - Identify interfaces, dependencies, and testability needs.
   - Output: Structured requirements and test scenarios.

2. **Design Tests First**
   - Write failing unit, integration, and acceptance tests for each requirement.
   - Use descriptive names and AAA pattern (Arrange, Act, Assert).
   - Output: Executable test suite (Red phase).

3. **Implement Minimal Code**
   - Write only enough code to pass the tests.
   - Commit after each passing test; keep changes small and focused.
   - Output: Working code that passes all tests (Green phase).

4. **Refactor for Quality**
   - Remove duplication, improve clarity, and ensure SOLID principles.
   - Update documentation and test coverage.
   - Output: Clean, maintainable code and updated docs.

5. **Integrate & Validate**
   - All Python code changes are automatically formatted, linted, tested, and checked for coverage via pre-commit hooks.
   - Pre-commit runs the full test suite and enforces coverage only when Python files are changed in a commit.
   - If any part of the MCP server implementation is non-Python, reevaluate the pre-commit configuration to ensure it covers all new additions and maintains project standards.
   - Output: Test results and defect reports.

6. **Review & Document**
   - Review code, tests, and documentation for completeness and quality.
   - Document lessons learned and technical debt.
   - Output: Approved code and current documentation.

## Quality Gates
- **Ready:** Requirements and acceptance criteria are clear; dependencies identified.
- **Done:** All tests pass; code reviewed; documentation updated; no critical defects.

## Testing Strategy

## Testing Workflow

Testing is central to the Codenames MCP Server project and follows a test-driven, context-aware approach:

1. **Test Design**
   - Write failing unit, integration, and acceptance tests for each requirement before implementation (Red phase).
   - Use descriptive names and the AAA pattern (Arrange, Act, Assert).
   - Focus on high-risk areas first (game logic, state consistency).
   - Use mocks and stubs for external dependencies.

2. **Test Implementation**
   - Use FastMCP's in-memory transport for fast, isolated tests by passing the server instance directly to the client.
   - Organize all tests in the `tests/`.
   - Capture logs with `caplog_for_fastmcp(caplog)` for assertions.
   - Use `ctx.debug`, `ctx.info`, `ctx.warning`, and `ctx.error` for structured logging in tools.
   - Use `ctx.elicit` for structured user input and `ctx.sample` for LLM-based text generation in tests.

3. **Test Patterns**
   - Unit tests: Parameter parsing, route mapping, schema generation.
   - Integration tests: Mock HTTP clients, end-to-end execution, error handling.
   - OpenAPI: Create focused test files for new features (see FastMCP docs for file structure).

4. **Recommended Testing Steps**
   - Install dependencies: `poetry install`
   - Runs automatically on pre-commit hooks: All code is formatted, linted, tested, and checked for coverage on every commit.

5. **Success Criteria**
   - >85% test coverage
   - All acceptance criteria met
   - No critical defects

Refer to FastMCP documentation for advanced patterns, file organization, and extension points for testing MCP tools and protocols.




## Metrics
- Track time per workflow step, test coverage, defects, and requirements completion.
- Success: >85% test coverage, all acceptance criteria met, no critical defects.

## Emergency Protocols
- On test failure: Stop new features, fix failing tests, prevent regression.
- Behind schedule: Reassess scope, focus on MVP, document technical debt, maintain quality.

## Agent Guidance
- Always reference `pyproject.toml` and `docs/` for standards and requirements.
- Request clarification if context is missing or ambiguous.
- Automate, validate, and document every change for reproducibility.
   - Follows best practices for formatting (Black), linting (Flake8, flake8-black), and CI/CD.

