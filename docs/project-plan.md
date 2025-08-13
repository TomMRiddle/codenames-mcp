
## 1. Codenames MCP Server - Project Plan

### 1.1 Table of Contents
1. Overview
2. Key Architecture Principles
3. MVP Implementation Strategy
   - Phase 1: MCP Server Foundation with Sampling
   - Phase 2: Game State & Internal Logic (with Input/Output Validation)
   - Phase 3: MCP Tools Interface (Minimal External Interface)
   - Phase 4: Internal Game Flow Management (MCP-Initiated Sequences)
4. Architecture: MCP Tools vs Internal Flow Management

## 2. Overview
A standalone Model Context Protocol (MCP) server that implements a complete Codenames game experience. The server provides pure game logic and state management while leveraging the client's LLM capabilities through MCP sampling for all AI decisions.

## 3. Key Architecture Principles
1. **No Built-in AI**: Server contains only game logic, rules, and state management
2. **Client LLM Sampling**: Use MCP sampling to get all AI decisions from the connected LLM
3. **Pure Game Engine**: Focus on providing comprehensive game tools and resources
4. **Role-based Information Isolation**: Strict separation between spymaster and team knowledge, filtered by player type
5. **Sampling-driven Gameplay**: All intelligent decisions come from client LLM via sampling requests
6. **Player Type Security**: Information access controlled by whether roles are USER (human) or LLM (AI)

## 4. MVP Implementation Strategy

**Core MVP Phases (1-4)**: Integrated development with validation throughout
- Phase 1: MCP Server Foundation with sampling capabilities
- Phase 2: Game State & Internal Logic (with integrated validation)
- Phase 3: MCP Tools Interface (user/LLM-facing)
- Phase 4: Sampling Integration (completing the AI workflows)

**Integrated Development Approach**: 
- Write tests alongside every implementation from Phase 1
- Production validation logic built into game business logic
- Clear separation: MCP Tools (external) vs Internal Functions (server logic)
- Operational monitoring separate from test validation

### 4.1 Phase 1: MCP Server Foundation with Sampling
**Goal**: Establish basic MCP server with sampling capabilities

1. **Initialize MCP Python project with sampling support**
   - Set up pyproject.toml with latest MCP SDK
   - Configure sampling capabilities in server initialization
   - Set up project structure optimized for sampling workflows

2. **Core MCP server with sampling architecture**
   - Server initialization with tools, resources, and sampling endpoints
   - Sampling request/response handlers
   - Context management for different sampling scenarios
   - **Role-based sampling contexts**: Essential infrastructure for spymaster vs team information isolation
   - **Dynamic prompt generation**: Game state-aware prompts for effective LLM sampling

### 4.2 Phase 2: Game State & Internal Logic (with Input/Output Validation)
**Goal**: Implement core game mechanics with validation at system boundaries

3. **Core game state management (with basic validation)**
   - Game board generation (25 words, team assignments)
   - Turn tracking (internal role switching)
   - Win/lose condition checking
   - State persistence and serialization
   - **Input/Output validation**: Validate external inputs and dynamic outputs only

4. **Internal game functions (not MCP tools)**
   - State management: `_switch_role_internal()`, `_update_game_state()`, `_check_game_exists()`
   - Board operations: `_create_board_from_words()`, `_reveal_card()`, `_get_card_team()`
   
   **Note**: See Section 12.2 for complete function specifications.

5. **MCP Resources for game context**
   - `game://rules/codenames` - Complete game rules and mechanics
   - `game://state/board` - Current board state (role-filtered by player type)
   - `game://state/history` - Move and hint history
   - `game://context/current-role` - Active role context (spymaster/team, filtered by player type)

### 4.3 Phase 3: MCP Tools Interface (Minimal External Interface)
**Goal**: Provide minimal external interface - only out-of-turn actions

6. **Essential MCP Tools (only out-of-turn actions)**
   - `create_new_game(red_spymaster, red_team, blue_spymaster, blue_team)` - User initiates new game with player type configuration
   - `end_game()` - User terminates current game

**Note**: All turn-based actions are handled internally by the server. See Section 12.1 for detailed tool specifications.

### 4.4 Phase 4: Internal Game Flow Management (MCP-Initiated Sequences)
**Goal**: Server manages all turn-based interactions internally

7. **Internal turn management**
   - Server automatically manages spymaster → team → spymaster sequences
   - No validation needed - server controls all legal actions
   - Turn-based elicitation and sampling initiated by server, not external tools

8. **Internal elicitation and sampling (MCP-initiated)**
   - Board setup: `_elicit_board_preference()`, `_sample_word_list()`
   - Player interactions: `_elicit_spymaster_hint()`, `_sample_spymaster_hint()`, `_elicit_team_guess()`, `_sample_team_guess()`
   - Turn continuation: `_elicit_continue_guessing()`, `_sample_continue_guessing()`

9. **Role-based sampling contexts and dynamic prompts (MVP CRITICAL)**
   - Context generation: `_generate_spymaster_context()`, `_generate_team_context()`
   - Prompt management: `_build_dynamic_prompts()`, `_filter_context_by_role()`

10. **Internal game flow functions**
   - Turn management: `_run_spymaster_turn()`, `_run_team_turn()`, `_advance_turn()`
   - Game state: `_handle_game_end()`, `_determine_player_types()`, `_filter_status_by_player_type()`
   - Choice management: `_calculate_available_guesses()`, `_offer_continue_choice()`

**Note**: See Section 12.2 for complete function specifications.

**Note**: All external inputs (through tool calls, sampling and elicitation) undergo context-specific validation within the functions that handle them, before applying changes to game state.

---

## 5. Architecture: MCP Tools vs Internal Flow Management

### 5.1 MCP Tools (Minimal External Interface)
**Only out-of-turn actions:**
- `create_new_game()` - User starts new game with player type configuration 
- `end_game()` - User terminates game

**Player Types**: "user" (human via elicitation) or "llm" (AI via sampling). See Section 12.1 for details.

### 5.2 Internal Flow Management (MCP-Initiated)
**All turn-based interactions managed by server with automatic status updates:**
- **Board Setup**: Server elicits preferences and samples words during `create_new_game()`
- **Spymaster Turns**: Server elicits hints (USER) or samples hints (LLM), validates internally, and provides role-appropriate status
- **Team Turns**: Server elicits guesses (USER) or samples guesses (LLM), manages continuation, and provides role-appropriate status
- **Role Switching**: Server advances turns automatically with status updates
- **Information Isolation**: Server filters contexts and status information based on player types (USER vs LLM)

### 5.3 Key Benefits of This Architecture
1. **No illegal tool calls**: User can't make moves out of turn
2. **Architecture prevents errors**: Server controls all legal actions through design
3. **Cleaner interface**: Only 2 external tools needed
4. **Robust game flow**: Server manages complex turn sequences automatically
5. **Automatic status updates**: Game status provided at each step, no separate queries needed
6. **Better UX**: User just creates game and receives continuous updates as it progresses
7. **Information security**: Spymaster view only shown when USER spymasters are present

### 5.4 Architecture Benefits
**Architecture and validation work together:**
- Phase 2: Context-specific validation within game logic functions, internal logic controlled by architecture
- Phase 3: MCP tools validate inputs within their specific contexts before state changes
- Phase 4: Sampling and elicitation functions validate inputs based on expected game state
- All phases: Architecture prevents illegal actions, validation protects against bad data within specific contexts

---

## 6. MCP Input/Output Validation Patterns

### 6.1 Schema-Based Validation (from MCP SDK patterns)
- **JSON Schema**: Use inputSchema for tool parameters and output validation
- **Type Safety**: Leverage Python type hints for automatic schema generation
- **Structured Responses**: Return structured data with proper error handling

### 6.2 Input Validation Functions
```python
#### 6.2.1 MCP SDK pattern for input validation
@server.call_tool()
async def handle_tool_call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "create_new_game":
        # Validate player types
        for role, player_type in arguments.items():
            if player_type not in ["user", "llm"]:
                raise ValueError(f"Invalid player type '{player_type}' for {role}")
        
        # Continue with validated inputs
        return await process_game_creation(arguments)
    
    raise ValueError(f"Unknown tool: {name}")
```

### 6.3 Error Handling Best Practices
- **Specific Exceptions**: Raise ValueError for invalid inputs, not generic Exception
- **Structured Error Responses**: Provide clear error messages for debugging
- **Input Sanitization**: Clean and validate external data at system boundaries

### 6.4 Integration with Testing & Production
- **Requirements-based test design**: Game rules drive systematic test case creation
- **Separate validation concerns**: Production validation built into business logic, test validation in test suites
- **Independent verification**: Tests verify production code behavior without shared validation dependencies
- **Monitoring production code**: Operational metrics track production validation performance

---

## 7. Integrated Testing & Production Strategy

### 7.1 Development Testing (Integrated Throughout Phases 1-4)
**Approach**: Requirements-based testing with test cases derived from game rules

- **Unit Testing**: Test individual functions against specific rule requirements
- **Integration Testing**: Test MCP tool workflows and sampling integration
- **Functional Testing**: Test complete game scenarios against rule compliance
- **System Testing**: Comprehensive rule enforcement and game flow validation
- **Performance Testing**: Ensure rule validation doesn't impact game responsiveness

### 7.2 Production Monitoring & Operations
**Approach**: Context-specific validation within game logic to protect system integrity

- **Player Type Validation**: Validate player types during game creation (`create_new_game()`)
- **Board Preference Validation**: Validate user preferences within `_elicit_board_preference()`
- **Word List Validation**: Validate LLM-generated words within `_sample_word_list()`
- **Hint Validation**: Validate hint format within `_elicit_spymaster_hint()` and `_sample_spymaster_hint()`
- **Guess Validation**: Validate guesses against current board within guess functions
- **Choice Validation**: Validate yes/no responses within continue functions
- **Error Recovery**: Graceful handling when validation fails within specific contexts
- **Operational Logging**: Record validation failures with context about which function failed

### 7.3 Requirements-Based Testing Strategy
**Core Principle**: Game rules define testable requirements that drive test case design

1. **Requirements analysis** - Game rules define acceptance criteria and constraints
2. **Test case design** - Derive test scenarios directly from game rule requirements
3. **Test implementation** - Create test-specific validation and assertion logic
4. **Test execution** - Verify production code behavior against requirements

## 8. MVP Documentation Requirements

### 8.1 API Documentation
- MCP tool specifications with examples
- Resource schemas and access patterns
- Sampling workflow documentation
- Error handling and validation responses

### 8.2 Integration Guide
- Client setup and connection examples
- Role-based usage patterns
- Complete game flow walkthroughs
- Troubleshooting common issues

## 9. Key Sampling Workflows

### 9.1 Overview
- **Board Generation**: User choice or AI generation with output validation
- **Spymaster Turns**: Role-specific hint generation with input/output validation
- **Team Turns**: Guess processing with input validation and choice management
- **Information Security**: Strict role-based filtering for USER vs LLM player types

**Note**: See Section 12.3 for detailed role isolation strategy and security guarantees.

## 10. Technology Stack
- **MCP SDK**: Latest Python MCP SDK with sampling support
- **Game Logic**: Pure Python game state management
- **Persistence**: JSON-based game state serialization
- **Input/Output Validation**: Boundary validation for external data

## 11. Success Criteria
1. **Functional MVP**: Complete game playable through MCP tools with all player type combinations
2. **Sampling Integration**: All AI decisions via client LLM sampling (for LLM players)
3. **Elicitation Integration**: All human decisions via client elicitation (for USER players)
4. **Rule Compliance**: Perfect adherence to Codenames rules through architecture and input/output validation
5. **Information Security**: No knowledge leakage between roles, proper filtering by player type
6. **Documentation**: Complete API documentation and usage examples for all configurations

---
*Document created: August 8, 2025*
*Status: Design phase - ready for implementation*
*Next Step: Begin Phase 1 - MCP Server Foundation*

---

## 12. Appendix: Detailed Reference

### 12.1 MCP Tools Reference

#### 12.1.1 `create_new_game(red_spymaster, red_team, blue_spymaster, blue_team)`
**Purpose**: User initiates a new game with player type configuration
**Parameters**: Each role can be "user" (human interaction via elicitation) or "llm" (AI interaction via sampling)
**Returns**: Initial game status and triggers internal setup sequence
**Usage**: Only out-of-turn action that doesn't require game state validation

#### 12.1.2 `end_game()`
**Purpose**: User terminates current game
**Parameters**: None
**Returns**: Confirmation of game termination
**Usage**: Safe to call anytime, terminates all internal game processes

### 12.2 Internal Functions Reference

#### 12.2.1 Game State Management
- `_switch_role_internal(role)` - Internal role management for game flow
- `_advance_turn()` - Move to next role/team automatically
- `_check_win_conditions()` - Game end detection
- `_update_game_state(action)` - State management with basic sanitization
- `_check_game_exists()` - Verify game state exists before operations
- `_create_board_from_words(words)` - Initialize game board with team assignments
- `_reveal_card(card_index)` - Reveal a card and update game state
- `_get_card_team(card_index)` - Get team assignment for a specific card

#### 12.2.2 Input/Output Validation (Production Critical)
- `_validate_word_list(words)` - Ensure word list meets technical requirements (count, format)

#### 12.2.3 Sampling & Elicitation Infrastructure
- `_elicit_board_preference()` - Server asks user for word source, validates preference format
- `_sample_word_list()` - Server requests word generation from LLM, validates count and format
- `_elicit_spymaster_hint()` - Server prompts for hint (USER spymasters), validates hint format
- `_sample_spymaster_hint()` - Server requests hint from LLM (LLM spymasters), validates hint format
- `_elicit_team_guess()` - Server prompts for guess (USER teams), validates guess against board
- `_sample_team_guess()` - Server requests guess from LLM (LLM teams), validates guess against board
- `_elicit_continue_guessing()` - Server asks if team wants to continue, validates yes/no response
- `_sample_continue_guessing()` - Server requests continuation decision from LLM, validates yes/no response

#### 12.2.4 Context Generation & Role Isolation
- `_generate_spymaster_context()` - Create role-specific context with full board knowledge for LLM spymasters
- `_generate_team_context()` - Create role-specific context with limited board info for LLM teams
- `_build_dynamic_prompts()` - Generate game state-aware prompts for sampling requests
- `_filter_context_by_role()` - Ensure appropriate information isolation in sampling contexts

#### 12.2.5 High-Level Game Flow
- `_run_spymaster_turn()` - Complete spymaster turn sequence with validation
- `_run_team_turn()` - Complete team turn sequence with choice management
- `_handle_game_end()` - Process win/lose conditions
- `_calculate_available_guesses(hint_number)` - Determine max guesses (hint_number + 1)
- `_offer_continue_choice(remaining_guesses)` - Present strategic choice to team
- `_determine_player_types()` - Track which roles are USER vs LLM for each team
- `_filter_status_by_player_type()` - Show spymaster view only when USER spymasters present

### A.3 Role Isolation Strategy Reference

**Sampling Contexts**: Strictly filtered by role and player type
- **LLM Spymaster context**: Includes full board knowledge via sampling only
- **USER Spymaster context**: Gets full board knowledge via filtered status display
- **Team context**: Only includes revealed cards and current hint (both USER and LLM)

**Server Enforcement**: Information boundaries maintained at both sampling and status levels
- **Game status filtering**: Spymaster view only displayed when USER spymasters are present
- **LLM spymasters**: Get full context via sampling, never via status display
- **USER spymasters**: Get full context via filtered status display when appropriate
- **Security guarantee**: No information leakage between roles or player types
