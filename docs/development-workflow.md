
## 1. Development Workflow

### 1.1 Table of Contents
1. Overview
2. Core Principles
   - ISTQB Testing Fundamentals
   - TDD Fundamentals
3. Development Iteration Workflow
   - Step 1: Analysis & Planning (ISTQB: Test Analysis & Design)
   - Step 2: Test Design (TDD: Red Phase)
   - Step 3: Implementation (TDD: Green Phase)
   - Step 4: Refactoring & Quality (TDD: Refactor Phase)
   - Step 5: Integration Testing (ISTQB: Test Execution)
   - Step 6: Review & Documentation (ISTQB: Test Closure)
4. Quality Gates
   - Definition of Ready
   - Definition of Done
5. Testing Strategy
   - Test Pyramid
   - Risk-Based Testing Priority
6. Tools and Standards
   - Testing Tools
   - Code Quality Tools
   - Documentation Standards
7. Iteration Metrics
   - Track Per Iteration
   - Success Criteria
8. Emergency Procedures
   - When Tests Fail
   - When Behind Schedule

## 2. Overview
This document defines the repeatable development workflow for the Codenames MCP Server project, incorporating ISTQB testing best practices and Test-Driven Development (TDD) principles.

## 3. Core Principles

### 3.1 ISTQB Testing Fundamentals
- **Early Testing**: Testing activities begin during requirements analysis
- **Defect Prevention**: Focus on preventing defects through good design and testing
- **Risk-Based Testing**: Prioritize testing based on risk assessment
- **Independent Testing**: Maintain objectivity in test design and execution
- **Test Documentation**: Maintain clear, traceable test artifacts

### 3.2 TDD Fundamentals
- **Red-Green-Refactor**: Write failing test → Make it pass → Improve code
- **Test First**: No production code without a failing test
- **Incremental Development**: Small, focused changes
- **Continuous Feedback**: Tests provide immediate feedback on code quality

## 4. Development Iteration Workflow

### 4.1 Step 1: Analysis & Planning (ISTQB: Test Analysis & Design)
**Duration**: 15-30 minutes per feature

1. **Requirements Analysis**
   - Define user story or feature requirement
   - Identify acceptance criteria
   - Document expected behavior and edge cases
   - Identify risk areas and priorities

2. **Test Planning**
   - Define test objectives for this iteration
   - Identify test conditions and scenarios
   - Plan test data requirements
   - Define entry/exit criteria

3. **Design Considerations**
   - Identify interfaces and dependencies
   - Plan for testability (dependency injection, mocking)
   - Consider error handling and edge cases
   - Document API contracts

**Deliverables**:
- User story with acceptance criteria
- Test scenarios list
- Interface/API design notes

### 4.2 Step 2: Test Design (TDD: Red Phase)
**Duration**: 30-45 minutes per feature

1. **Unit Test Design**
   - Write failing unit tests for new functionality
   - Focus on one small behavior at a time
   - Use descriptive test names that explain intent
   - Follow AAA pattern (Arrange, Act, Assert)

2. **Integration Test Design**
   - Design tests for component interactions
   - Plan MCP protocol testing (tools, resources, sampling)
   - Define test doubles/mocks for external dependencies

3. **Acceptance Test Design**
   - Write high-level behavioral tests
   - Define end-to-end scenarios
   - Plan user journey testing

**Example Test Structure**:
```python
class TestGameStateManagement:
    def test_should_create_new_game_with_25_words_when_initialized(self):
        """GIVEN: Game initialization request
           WHEN: create_new_game is called
           THEN: Game state contains exactly 25 words"""
        pass  # This should fail initially (Red)
    
    def test_should_assign_roles_correctly_when_players_join(self):
        pass
    
    def test_should_validate_spymaster_clue_format(self):
        pass
```

**Deliverables**:
- Failing unit tests
- Integration test stubs
- Acceptance criteria as executable tests

### 4.3 Step 3: Implementation (TDD: Green Phase)
**Duration**: 45-90 minutes per feature

1. **Minimal Implementation**
   - Write the simplest code that makes tests pass
   - Don't over-engineer or add unnecessary features
   - Focus on making the red tests green

2. **Progressive Implementation**
   - Implement one failing test at a time
   - Run tests frequently (every 2-3 minutes)
   - Commit small, working increments

3. **Integration Points**
   - Implement MCP tool interfaces
   - Add sampling integration points
   - Ensure proper error handling

**Guidelines**:
- No production code without a failing test
- Make tests pass with minimal code
- Commit after each green test
- Keep implementation cycles short (5-10 minutes)

**Deliverables**:
- Working code that passes all tests
- MCP tool implementations
- Updated documentation

### 4.4 Step 4: Refactoring & Quality (TDD: Refactor Phase)
**Duration**: 30-45 minutes per feature

1. **Code Quality Improvement**
   - Remove duplication
   - Improve naming and clarity
   - Extract methods/classes for better design
   - Ensure SOLID principles

2. **Test Quality Review**
   - Review test clarity and maintainability
   - Consolidate redundant tests
   - Improve test readability
   - Ensure good test coverage

3. **Documentation Update**
   - Update docstrings and comments
   - Update API documentation
   - Update architectural decisions

**Quality Checklist**:
- [ ] All tests pass
- [ ] No code duplication
- [ ] Clear, expressive names
- [ ] Proper error handling
- [ ] Documentation updated

**Deliverables**:
- Refactored, clean code
- Improved test suite
- Updated documentation

### 4.5 Step 5: Integration Testing (ISTQB: Test Execution)
**Duration**: 30-60 minutes per feature

1. **Component Integration Testing**
   - Test interactions between game engine components
   - Verify MCP protocol compliance
   - Test sampling request/response cycles

2. **System Integration Testing**
   - Test with actual MCP client connections
   - Verify end-to-end workflows
   - Test error scenarios and edge cases

3. **User Acceptance Testing**
   - Manual testing of user scenarios
   - Verify acceptance criteria are met
   - Test with different client capabilities

**Test Execution Guidelines**:
- Execute tests in order of risk/priority
- Document any defects found
- Verify fixes don't break existing functionality
- Test both happy path and error scenarios

**Deliverables**:
- Test execution results
- Defect reports (if any)
- Verified acceptance criteria

### 4.6 Step 6: Review & Documentation (ISTQB: Test Closure)
**Duration**: 15-30 minutes per feature

1. **Code Review**
   - Review implementation against requirements
   - Check adherence to coding standards
   - Verify test quality and coverage

2. **Documentation Review**
   - Update architectural documentation
   - Review API documentation
   - Update user guides if needed

3. **Retrospective Notes**
   - Document lessons learned
   - Identify process improvements
   - Note any technical debt incurred

**Review Checklist**:
- [ ] Requirements met
- [ ] Code quality standards met
- [ ] Tests comprehensive and maintainable
- [ ] Documentation current
- [ ] No critical technical debt

**Deliverables**:
- Reviewed and approved code
- Updated documentation
- Retrospective notes

## 5. Quality Gates

### 5.1 Definition of Ready (before starting iteration)
- [ ] Requirements clearly defined
- [ ] Acceptance criteria specified
- [ ] Dependencies identified
- [ ] Test environment available

### 5.2 Definition of Done (before completing iteration)
- [ ] All tests pass (unit, integration, acceptance)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No critical defects
- [ ] Acceptance criteria verified
- [ ] Performance acceptable

## 6. Testing Strategy

### 6.1 Test Pyramid
1. **Unit Tests (70%)**
   - Fast, isolated, deterministic
   - Test individual functions and classes
   - Mock external dependencies

2. **Integration Tests (20%)**
   - Test component interactions
   - Test MCP protocol compliance
   - Test database/state persistence

3. **End-to-End Tests (10%)**
   - Test complete user journeys
   - Test with real MCP clients
   - Test cross-system integration

### 6.2 Risk-Based Testing Priority
1. **High Risk**: Game logic correctness, state consistency
2. **Medium Risk**: MCP protocol compliance, error handling
3. **Low Risk**: UI presentation, performance optimization

## 7. Tools and Standards

### 7.1 Testing Tools
- **pytest**: Unit and integration testing
- **unittest.mock**: Mocking dependencies
- **pytest-asyncio**: Async testing support
- **coverage.py**: Code coverage measurement

### 7.2 Code Quality Tools
- **ruff**: Linting and formatting
- **mypy**: Type checking
- **pre-commit**: Automated quality checks

### 7.3 Documentation Standards
- Docstrings for all public methods
- Type hints for all function signatures
- README updates for significant changes
- API documentation for MCP tools

## 8. Iteration Metrics

### 8.1 Track Per Iteration
- Time spent per workflow step
- Number of tests written/passing
- Code coverage percentage
- Defects found and fixed
- Requirements implemented vs planned

### 8.2 Success Criteria
- All acceptance criteria met
- Test coverage > 85%
- No critical defects
- Code review approved
- Documentation current

## 9. Emergency Procedures

### 9.1 When Tests Fail
1. Stop adding new features
2. Identify root cause
3. Fix failing tests first
4. Ensure no regression
5. Continue with normal workflow

### 9.2 When Behind Schedule
1. Reassess scope and priorities
2. Focus on minimum viable implementation
3. Document technical debt
4. Plan catch-up in next iteration
5. Maintain quality standards

This workflow ensures consistent quality, early defect detection, and maintainable code while following industry best practices from ISTQB and TDD methodologies.
