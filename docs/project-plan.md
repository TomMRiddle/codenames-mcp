# Codenames MCP Server - Project Plan

## Overview
A standalone Model Context Protocol (MCP) server that implements a complete Codenames game experience. The server provides pure game logic and state management while leveraging the client's LLM capabilities through MCP sampling for all AI decisions.

## Key Architecture Principles
1. **No Built-in AI**: Server contains only game logic, rules, and state management
2. **Client LLM Sampling**: Use MCP sampling to get all AI decisions from the connected LLM
3. **Pure Game Engine**: Focus on providing comprehensive game tools and resources
4. **Role-based Information Isolation**: Strict separation between spymaster and team knowledge, filtered by player type
5. **Sampling-driven Gameplay**: All intelligent decisions come from client LLM via sampling requests
6. **Player Type Security**: Information access controlled by whether roles are USER (human) or LLM (AI)

## MVP Implementation Strategy

**Core MVP Phases (1-4)**: Integrated development with validation throughout
- Phase 1: MCP Server Foundation with sampling capabilities
- Phase 2: Game State & Internal Logic (with integrated validation)
- Phase 3: MCP Tools Interface (user/LLM-facing)
- Phase 4: Sampling Integration (completing the AI workflows)

**Integrated Development Approach**: 
- Write tests alongside every implementation from Phase 1
- Validation logic integrated into all phases, not separate
- Clear separation: MCP Tools (external) vs Internal Functions (server logic)
- Production monitoring built on same validation foundation

### Phase 1: MCP Server Foundation with Sampling
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

### Phase 2: Game State & Internal Logic (with Integrated Validation)
**Goal**: Implement core game mechanics with validation built-in

3. **Core game state management (with validation)**
   - Game board generation (25 words, team assignments)
   - Turn tracking and validation (internal role switching)
   - Win/lose condition checking with validation
   - State persistence and serialization
   - **Integrated validation**: All state changes validated in real-time

4. **Internal game functions (not MCP tools)**
   - `_switch_role_internal(role)` - Internal role management for game flow
   - `_validate_hint_format(word, number)` - Microsoft-pattern validation
   - `_validate_move_legality(card_index, role)` - Move validation
   - `_check_win_conditions()` - Game end detection
   - `_update_game_state(action, validation_result)` - State management

5. **MCP Resources for game context**
   - `game://rules/codenames` - Complete game rules and mechanics
   - `game://state/board` - Current board state (role-filtered by player type)
   - `game://state/history` - Move and hint history
   - `game://context/current-role` - Active role context (spymaster/team, filtered by player type)

### Phase 3: MCP Tools Interface (Minimal External Interface)
**Goal**: Provide minimal external interface - only out-of-turn actions

6. **Essential MCP Tools (only out-of-turn actions)**
   - `create_new_game(red_spymaster="user"|"llm", red_team="user"|"llm", blue_spymaster="user"|"llm", blue_team="user"|"llm")` - User initiates a new game with player type configuration (returns initial game status)
   - `end_game()` - User terminates current game

**Note**: All turn-based actions (hints, guesses, role switching) are handled internally by the MCP server through automatic elicitation and sampling sequences. Game status is provided automatically at each step, eliminating the need for separate status queries. Status information is filtered based on player types to maintain information security.

### Phase 4: Internal Game Flow Management (MCP-Initiated Sequences)
**Goal**: Server manages all turn-based interactions internally

7. **Internal turn management**
   - Server automatically manages spymaster → team → spymaster sequences
   - No external validation needed - server controls all legal actions
   - Turn-based elicitation and sampling initiated by server, not external tools

8. **Internal elicitation and sampling (MCP-initiated)**
   - `_elicit_board_preference()` - Server asks user for word source during game creation
   - `_sample_word_list()` - Server requests word generation from LLM during setup
   - `_elicit_spymaster_hint()` - Server prompts for hint during spymaster turn (USER spymasters only)
   - `_sample_spymaster_hint()` - Server requests hint from LLM during spymaster turn (LLM spymasters only)
   - `_elicit_team_guess()` - Server prompts for guess during team turn (USER teams only)
   - `_sample_team_guess()` - Server requests guess from LLM during team turn (LLM teams only)
   - `_elicit_continue_guessing()` - Server asks if team wants to continue guessing (USER teams only)
   - `_sample_continue_guessing()` - Server requests continuation decision from LLM (LLM teams only)

9. **Role-based sampling contexts and dynamic prompts (MVP CRITICAL)**
   - `_generate_spymaster_context()` - Create role-specific context with full board knowledge for LLM spymasters
   - `_generate_team_context()` - Create role-specific context with limited board info for LLM teams
   - `_build_dynamic_prompts()` - Generate game state-aware prompts for sampling requests
   - `_filter_context_by_role()` - Ensure appropriate information isolation in sampling contexts

10. **Internal game flow functions**
   - `_run_spymaster_turn()` - Complete spymaster turn sequence with validation
   - `_run_team_turn()` - Complete team turn sequence with choice management
   - `_advance_turn()` - Move to next role/team automatically
   - `_handle_game_end()` - Process win/lose conditions
   - `_calculate_available_guesses(hint_number)` - Determine max guesses (hint_number + 1)
   - `_offer_continue_choice(remaining_guesses)` - Present strategic choice to team
   - `_determine_player_types()` - Track which roles are USER vs LLM for each team
   - `_filter_status_by_player_type()` - Show spymaster view only when USER spymasters present

**Note**: All sampling tools trigger internal validation before applying changes to game state.

---

## Architecture: MCP Tools vs Internal Flow Management

### MCP Tools (Minimal External Interface)
**Only out-of-turn actions that don't require game state validation:**
- `create_new_game(red_spymaster, red_team, blue_spymaster, blue_team)` - User starts a new game with player type configuration (returns initial status and triggers internal setup sequence)
- `end_game()` - User terminates game (safe anytime)

**Player Types**: Each role can be either "user" (human interaction via elicitation) or "llm" (AI interaction via sampling)

### Internal Flow Management (MCP-Initiated)
**All turn-based interactions managed by server with automatic status updates:**
- **Board Setup**: Server elicits preferences and samples words during `create_new_game()`
- **Spymaster Turns**: Server elicits hints (USER) or samples hints (LLM), validates internally, and provides role-appropriate status
- **Team Turns**: Server elicits guesses (USER) or samples guesses (LLM), manages continuation, and provides role-appropriate status
- **Role Switching**: Server advances turns automatically with status updates
- **Information Isolation**: Server filters contexts and status information based on player types (USER vs LLM)

### Key Benefits of This Architecture
1. **No illegal tool calls**: User can't make moves out of turn
2. **Simplified validation**: Server controls all legal actions internally
3. **Cleaner interface**: Only 2 external tools needed
4. **Robust game flow**: Server manages complex turn sequences automatically
5. **Automatic status updates**: Game status provided at each step, no separate queries needed
6. **Better UX**: User just creates game and receives continuous updates as it progresses
7. **Information security**: Spymaster view only shown when USER spymasters are present

### Validation Integration
**Validation is integrated throughout all phases:**
- Phase 2: Internal validation functions built into game logic
- Phase 3: MCP tools trigger internal validation before state changes
- Phase 4: Sampling results validated before applying to game state
- All phases: Same validation logic used for testing and production monitoring

---

## Microsoft-Inspired Validation Best Practices

### Design Principles (from Semantic Kernel guidance)
- **Descriptive naming**: Functions clearly convey their validation purpose
- **Minimal parameters**: Use primitive types for validation inputs
- **Clear return schemas**: Structured validation results with detailed error information
- **Local state management**: Keep sensitive validation logic server-side
- **Token optimization**: Minimize validation overhead in LLM interactions

### Validation Function Patterns
```python
# Following Microsoft's plugin patterns
@validation_function(description="Validates hint format according to Codenames rules")
def validate_hint_format(hint_word: str, hint_number: int) -> ValidationResult:
    """Returns structured validation result with success/failure and detailed context"""
    
@validation_function(description="Checks move legality for current game state")  
def validate_move_legality(card_index: int, current_role: str) -> ValidationResult:
    """Validates if the move is allowed given current game state and role"""
```

### Integration with Testing & Production
- **Test-driven validation**: Each validation rule generates test scenarios
- **Production monitoring**: Same validation logic used for real-time rule enforcement
- **Structured error reporting**: Consistent error format for both dev and prod
- **Performance tracking**: Validation metrics collection for optimization

---

## Integrated Testing & Production Strategy

### Development Testing (Integrated Throughout Phases 1-4)
**Approach**: Write tests alongside implementation using validation logic

- **Unit Tests**: Test individual functions and validation rules
- **Integration Tests**: Test MCP tool workflows and sampling integration
- **Game Logic Tests**: Test complete game scenarios using validation framework
- **Rule Compliance Tests**: Comprehensive rule enforcement scenarios
- **Performance Tests**: Ensure validation doesn't impact game responsiveness

### Production Monitoring & Validation
**Approach**: Extend validation framework for live monitoring

- **Real-time Rule Enforcement**: Same validation logic used in development
- **Audit Trails**: Log all game actions and validation results
- **Anomaly Detection**: Identify unusual patterns or potential issues
- **Performance Monitoring**: Track validation overhead and game performance
- **Error Reporting**: Detailed logging for debugging production issues

### Validation-Driven Development
**Core Principle**: Validation logic serves as the foundation for both testing and production

1. **Write validation rules first** - Define what "correct" looks like
2. **Generate test cases from rules** - Every validation rule becomes test scenarios
3. **Use same validation in production** - Ensures consistency between dev and prod
4. **Monitor validation results** - Real-time insights into system health

## Post-MVP Enhancements (Future Phases)

### Advanced Sampling Workflows
- **Sophisticated prompt engineering**: Advanced prompting strategies beyond basic game state
- **Strategic sampling preferences**: Difficulty preference, risk tolerance, play style customization
- **Multi-turn reasoning**: Complex strategic planning across multiple turns

### Statistics & Analytics (Post-MVP)
- Game statistics tool for performance analysis
- Hint effectiveness tracking using audit data
- Strategy pattern analysis from production logs
- Performance metrics and optimization

### Learning & Analytics
- Game analytics resources built on validation framework
- Advanced monitoring dashboards
- A/B testing framework for rule modifications

### Production Operations
- Automated alerting for validation failures
- Scalability and load testing

### Polish & Advanced Features
- Multiple difficulty levels
- Tournament mode
- Custom word themes
- Multi-language support

## MVP Documentation Requirements

### API Documentation
- MCP tool specifications with examples
- Resource schemas and access patterns
- Sampling workflow documentation
- Error handling and validation responses

### Integration Guide
- Client setup and connection examples
- Role-based usage patterns
- Complete game flow walkthroughs
- Troubleshooting common issues

## Key Sampling Workflows

### Board Generation Workflow
1. `_elicit_board_preference()` - "Would you like to provide 25 words or have AI generate them?"
2. **Option A**: User provides exactly 25 words via elicitation
3. **Option B**: `_sample_word_list()` - AI generates 25 words via sampling
4. `_validate_word_list(words)` - Apply validation rules (see word-validation-strategy.md)
5. `_create_board_from_words(words)` - Final board with team assignments

### Spymaster Turn Workflow
1. Server provides board context via resource (for LLM spymasters) or filtered status (for USER spymasters)
2. **LLM Spymaster**: `_sample_spymaster_hint(context)` - Client samples hint using spymaster context
3. **USER Spymaster**: `_elicit_spymaster_hint()` - Client prompts user for hint via elicitation
4. Server validates hint legality using `_validate_hint_format()`
5. If valid, hint is recorded and **updated game status is automatically provided** (filtered by player types)

### Team Turn Workflow
1. Server provides hint and limited board context
2. **LLM Team**: `_sample_team_guess(context)` - Client samples guess using team context
3. **USER Team**: `_elicit_team_guess()` - Client prompts user for guess via elicitation
4. Server processes guess using `_validate_move_legality()` and updates board
5. **After each guess**: Updated game status automatically provided (filtered by player types)
6. **After each correct guess**: 
   - **LLM Team**: `_sample_continue_guessing()` - Client samples whether to continue
   - **USER Team**: `_elicit_continue_guessing()` - Client prompts user for choice
7. **Team choice overrides available guesses**: Team can end turn voluntarily even with guesses remaining
8. Turn ends when: team chooses to stop, makes incorrect guess, or exhausts all available guesses
9. **Turn completion**: Final updated game status automatically provided (filtered by player types)

### Strategic Turn Management
**Key Rule**: Teams always have the choice to end their turn early (applies to both USER and LLM teams)
- **Hint "1"**: After 1 correct guess → choice to continue for bonus guess
- **Hint "2"**: After 1st correct guess → choice to attempt 2nd word
- **Hint "2"**: After 2nd correct guess → choice to continue for bonus guess
- **Risk vs Reward**: Teams balance getting points vs risk of hitting opponent/assassin cards
- **USER Teams**: Choice presented via elicitation (`_elicit_continue_guessing()`)
- **LLM Teams**: Choice made via sampling (`_sample_continue_guessing()`)

### Role Isolation Strategy
- **Sampling contexts** are strictly filtered by role and player type
- **LLM Spymaster context**: Includes full board knowledge via sampling only
- **USER Spymaster context**: Gets full board knowledge via filtered status display
- **Team context**: Only includes revealed cards and current hint (both USER and LLM)
- **Server enforcement**: Information boundaries maintained at both sampling and status levels
- **Game status filtering**: Spymaster view only displayed when USER spymasters are present
- **LLM spymasters**: Get full context via sampling, never via status display
- **USER spymasters**: Get full context via filtered status display when appropriate
- **Security guarantee**: No information leakage between roles or player types

## Technology Stack
- **MCP SDK**: Latest Python MCP SDK with sampling support
- **Game Logic**: Pure Python game state management
- **Persistence**: JSON-based game state serialization
- **Validation**: Custom validation logic for rules enforcement

## Success Criteria
1. **Functional MVP**: Complete game playable through MCP tools with all player type combinations
2. **Sampling Integration**: All AI decisions via client LLM sampling (for LLM players)
3. **Elicitation Integration**: All human decisions via client elicitation (for USER players)
4. **Rule Compliance**: Perfect adherence to Codenames rules with integrated validation
5. **Information Security**: No knowledge leakage between roles, proper filtering by player type
6. **Documentation**: Complete API documentation and usage examples for all configurations

## Future Enhancements
- Multiple difficulty levels
- Tournament mode with multiple games
- Advanced analytics and learning
- Custom word themes
- Multi-language support

---
*Document created: August 8, 2025*
*Status: Design phase - ready for implementation*
*Next Step: Begin Phase 1 - MCP Server Foundation*
