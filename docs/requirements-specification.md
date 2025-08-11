# Requirements Specification - Codenames MCP Server

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for the Codenames MCP Server, providing a testable foundation for implementation and validation.

### 1.2 Scope
The Codenames MCP Server implements a complete Codenames game engine accessible via the Model Context Protocol, enabling AI and human players to participate in games through MCP-compatible clients.

**Primary Learning Objectives (MVP Focus)**:
- Master MCP sampling for AI decision-making
- Master MCP elicitation for human interaction
- Implement MCP resources for game context
- Learn MCP tool registration and execution patterns

**Secondary Objectives (Post-MVP)**:
- Game feature completeness and polish
- Performance optimization and concurrent game support
- Advanced error handling and edge cases

### 1.3 Definitions and Acronyms
- **MCP**: Model Context Protocol
- **Spymaster**: Player who gives clues to their team
- **Operative**: Player who makes guesses based on clues
- **Board**: 5x5 grid of 25 word cards
- **Clue**: One-word hint given by spymaster with a number indicating related cards

## 2. Functional Requirements

### 2.1 Game Initialization (F001)

#### FR-001: Create New Game
**Priority**: High  
**Risk**: High  

**Description**: The system shall create a new Codenames game instance with a unique game ID.

**System Constraints**:
- SC-001-1: Game ID must be unique across all games [Tested by: TC-001-1, TC-001-2]
- SC-001-2: Initial game status must be "waiting_for_players" [Tested by: TC-001-1]
- SC-001-3: Board must remain empty until game initialization complete [Tested by: TC-001-3]
- SC-001-4: Game instance must be immediately queryable after creation [Tested by: TC-001-1, TC-001-2]

**Acceptance Criteria**:
- AC-001-1: GIVEN no existing game, WHEN create_new_game is called, THEN a unique game ID is returned [Tested by: TC-001-1]
- AC-001-2: GIVEN a new game is created, WHEN querying game state, THEN status is "waiting_for_players" [Tested by: TC-001-1]
- AC-001-3: GIVEN a new game is created, WHEN checking game board, THEN board is empty until initialization complete [Tested by: TC-001-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-001-1 Create First Game
    [Tags]    AC-001-1    AC-001-2    SC-001-1    SC-001-2    SC-001-4
    [Documentation]    Test creation of first game with unique ID and correct status
    Given No Games Exist
    When Call Create New Game
    Then Unique Game ID Is Returned
    And Game Status Is    waiting_for_players
    And Game Is Immediately Queryable

TC-001-2 Create Multiple Games
    [Tags]    SC-001-1    SC-001-4
    [Documentation]    Test creation of multiple games with unique IDs
    Given One Game Already Exists
    When Call Create New Game
    Then Different Game ID Is Returned
    And Both Games Exist Independently
    And Each Has Unique Identifier

TC-001-3 Empty Board Until Initialization
    [Tags]    AC-001-3    SC-001-3
    [Documentation]    Test that board remains empty until game start
    Given New Game Created
    When Checking Game Board
    Then Board Is Empty
    And Board Generation Occurs Only After Game Start
```

#### FR-002: Add Players to Game
**Priority**: Medium  
**Risk**: Medium  

**Description**: The system shall allow adding players to a game with specified roles and types.

**System Constraints**:
- SC-002-1: Player name: non-empty string, max 50 characters [Tested by: TC-002-2]
- SC-002-2: Player type: must be "USER" or "LLM" [Tested by: TC-002-3]
- SC-002-3: Maximum 8 players per game [Tested by: TC-002-4]
- SC-002-4: Minimum 4 players to start game [Tested by: TC-002-1]

**Acceptance Criteria**:
- AC-002-1: GIVEN a waiting game, WHEN adding a player with name and type (USER/LLM), THEN player is added successfully [Tested by: TC-002-1]
- AC-002-2: GIVEN a game with players, WHEN querying players, THEN correct player list with roles is returned [Tested by: TC-002-1]
- AC-002-3: GIVEN a game with 4+ players, WHEN checking if ready, THEN game can be started [Tested by: TC-002-1]
- AC-002-4: GIVEN a game with <4 players, WHEN checking if ready, THEN game cannot be started [Tested by: TC-002-1]

**Test Cases**:
```robot
*** Test Cases ***

TC-002-1 Valid Player Addition
    [Tags]    AC-002-1    AC-002-2    AC-002-3    AC-002-4    SC-002-4
    [Documentation]    Test successful player addition to game
    Given Game Waiting For Players
    When Add Player    Alice    USER
    Then Player Is Added Successfully
    And Player List Shows    Alice    USER

TC-002-2 Invalid Player Name Validation
    [Tags]    SC-002-1
    [Documentation]    Test validation of empty player name
    Given Game Waiting For Players
    When Try To Add Player With Empty Name
    Then Error Is Returned    Player name cannot be empty
    And Player Is Not Added To Game

TC-002-3 Invalid Player Type Validation
    [Tags]    SC-002-2
    [Documentation]    Test validation of invalid player type
    Given Game Waiting For Players
    When Try To Add Player    Bob    INVALID
    Then Error Is Returned    Player type must be USER or LLM
    And Player Is Not Added To Game

TC-002-4 Maximum Players Validation
    [Tags]    SC-002-3
    [Documentation]    Test maximum player limit enforcement
    Given Game With Players    8
    When Try To Add Another Player
    Then Error Is Returned    Maximum 8 players allowed
    And Player Is Not Added To Game
```

### 2.2 Board Generation (F002)

#### FR-003: Generate Game Board
**Priority**: High  
**Risk**: High  

**Description**: The system shall generate a 5x5 board with 25 words and assign team colors.

**System Constraints**:
- SC-003-1: Must generate exactly 25 unique words [Tested by: TC-003-1]
- SC-003-2: Must assign exactly 9 red cards, 8 blue cards, 7 neutral cards, and 1 assassin card [Tested by: TC-003-2]
- SC-003-3: Each position (0-24) must have exactly one word [Tested by: TC-003-1]
- SC-003-4: All words must be unique on the board [Tested by: TC-003-3]
- SC-003-5: Word list must contain minimum 1000 common English words [Tested by: TC-003-4]
- SC-003-6: No proper nouns, plurals, or compound words allowed [Tested by: TC-003-4]
- SC-003-7: Words must be between 3-12 characters [Tested by: TC-003-4]

**Acceptance Criteria**:
- AC-003-1: GIVEN a game ready to start, WHEN generate_board is called, THEN exactly 25 unique words are placed [Tested by: TC-003-1]
- AC-003-2: GIVEN a generated board, WHEN checking assignments, THEN exactly 9 red cards, 8 blue cards, 7 neutral cards, and 1 assassin card exist [Tested by: TC-003-2]
- AC-003-3: GIVEN a generated board, WHEN querying word positions, THEN each position (0-24) has exactly one word [Tested by: TC-003-1]
- AC-003-4: GIVEN a generated board, WHEN checking for duplicates, THEN all words are unique [Tested by: TC-003-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-003-1 Standard Board Generation
    [Tags]    AC-003-1    AC-003-3    SC-003-1    SC-003-3
    [Documentation]    Test standard 5x5 board generation with unique words
    Given Game Ready To Start
    When Generate Board Is Called
    Then Exactly 25 Unique Words Are Placed
    And Each Position 0-24 Has Exactly One Word

TC-003-2 Color Assignment Validation
    [Tags]    AC-003-2    SC-003-2
    [Documentation]    Test correct color distribution on generated board
    Given Generated Board
    When Checking Card Color Assignments
    Then Exactly 9 Red Cards Exist
    And Exactly 8 Blue Cards Exist
    And Exactly 7 Neutral Cards Exist
    And Exactly 1 Assassin Card Exists

TC-003-3 Word Uniqueness Validation
    [Tags]    AC-003-4    SC-003-4
    [Documentation]    Test that all words on board are unique
    Given Generated Board
    When Checking All 25 Words
    Then All Words Are Unique
    And No Duplicates Exist

TC-003-4 Word Quality Constraints
    [Tags]    SC-003-5    SC-003-6    SC-003-7
    [Documentation]    Test word selection criteria and quality
    Given Word List For Board Generation
    When Selecting Words For Board
    Then Words Are From List Of 1000+ Common English Words
    And No Proper Nouns Are Included
    And All Words Are 3-12 Characters Long
```

#### FR-004: Starting Team Selection
**Priority**: Medium  
**Risk**: Low  

**Description**: The system shall randomly determine which team (red/blue) goes first.

**System Constraints**:
- SC-004-1: Team selection must be random (50/50 probability) [Tested by: TC-004-1]
- SC-004-2: Starting team receives extra card (9 vs 8) [Tested by: TC-004-2, TC-004-3]
- SC-004-3: Turn order must be consistent with starting team selection [Tested by: TC-004-2, TC-004-3]
- SC-004-4: Both red and blue must be valid starting options [Tested by: TC-004-1]

**Acceptance Criteria**:
- AC-004-1: GIVEN a new board, WHEN game starts, THEN either red or blue team is selected to go first [Tested by: TC-004-1]
- AC-004-2: GIVEN team selection, WHEN checking turn order, THEN starting team has first turn [Tested by: TC-004-2, TC-004-3]
- AC-004-3: GIVEN starting team selection, WHEN the starting team is red, THEN red team gets 9 cards (extra card) [Tested by: TC-004-2]
- AC-004-4: GIVEN starting team selection, WHEN the starting team is blue, THEN blue team gets 9 cards (extra card) [Tested by: TC-004-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-004-1 Random Team Selection
    [Tags]    AC-004-1    SC-004-1    SC-004-4
    [Documentation]    Test random selection of starting team
    Given New Board Ready To Start
    When Game Initialization Occurs
    Then Either Red Or Blue Team Is Selected Randomly
    And Both Options Are Possible Outcomes

TC-004-2 Red Team Starts
    [Tags]    AC-004-2    AC-004-3    SC-004-2    SC-004-3
    [Documentation]    Test red team starting configuration
    Given Red Team Selected To Start
    When Checking Initial Game State
    Then Red Team Has First Turn
    And Red Team Has 9 Cards On Board
    And Blue Team Has 8 Cards On Board

TC-004-3 Blue Team Starts
    [Tags]    AC-004-4    SC-004-2    SC-004-3
    [Documentation]    Test blue team starting configuration
    Given Blue Team Selected To Start
    When Checking Initial Game State
    Then Blue Team Has First Turn
    And Blue Team Has 9 Cards On Board
    And Red Team Has 8 Cards On Board
```

### 2.3 Player Role Assignment (F003)

#### FR-005: Assign Spymasters
**Priority**: High  
**Risk**: High  

**Description**: The system shall assign one spymaster per team from available players.

**System Constraints**:
- SC-005-1: Each team must have exactly one spymaster [Tested by: TC-005-1]
- SC-005-2: Spymasters cannot be operatives simultaneously [Tested by: TC-005-1]
- SC-005-3: Team sizes should be balanced (±1 player) [Tested by: TC-005-1]

**Acceptance Criteria**:
- AC-005-1: GIVEN players ready for role assignment, WHEN assign_spymasters is called, THEN exactly one spymaster per team is assigned [Tested by: TC-005-1]
- AC-005-2: GIVEN spymaster assignment, WHEN checking player roles, THEN spymasters have role "spymaster" [Tested by: TC-005-1]
- AC-005-3: GIVEN spymaster assignment, WHEN checking remaining players, THEN non-spymasters have role "operative" [Tested by: TC-005-1]
- AC-005-4: GIVEN team assignments, WHEN checking balance, THEN teams have equal number of players (±1) [Tested by: TC-005-1]

**Test Cases**:
```robot
*** Test Cases ***

TC-005-1 Spymaster Assignment
    [Tags]    AC-005-1    AC-005-2    AC-005-3    AC-005-4    SC-005-1    SC-005-2    SC-005-3
    [Documentation]    Test assignment of spymasters and operatives with balanced teams
    Given Players Ready For Role Assignment
    When Assign Spymasters Is Called
    Then Exactly One Spymaster Per Team Is Assigned
    And Spymasters Have Role    spymaster
    And Non-Spymasters Have Role    operative
    And Teams Have Equal Number Of Players Plus Or Minus 1
```

#### FR-006: Role-Based Information Access
**Priority**: High  
**Risk**: High  

**Description**: The system shall filter game information based on player roles and types.

**System Constraints**:
- SC-006-1: Spymasters must see all card colors regardless of reveal status [Tested by: TC-006-1]
- SC-006-2: Operatives must see only revealed card colors [Tested by: TC-006-2]
- SC-006-3: USER players must receive human-readable information with sensitive data filtered [Tested by: TC-006-3]
- SC-006-4: LLM players must receive structured context appropriate for AI processing [Tested by: TC-006-4]

**Acceptance Criteria**:
- AC-006-1: GIVEN a spymaster player, WHEN querying board, THEN all card colors are visible [Tested by: TC-006-1]
- AC-006-2: GIVEN an operative player, WHEN querying board, THEN only revealed card colors are visible [Tested by: TC-006-2]
- AC-006-3: GIVEN a USER type player, WHEN accessing information, THEN sensitive data is hidden [Tested by: TC-006-3]
- AC-006-4: GIVEN an LLM type player, WHEN accessing information, THEN appropriate context is provided for AI decision-making [Tested by: TC-006-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-006-1 Spymaster Full Board Access
    [Tags]    AC-006-1    SC-006-1
    [Documentation]    Test spymaster can see all card colors
    Given Spymaster Player
    When Querying Board Information
    Then All Card Colors Are Visible
    And Unrevealed Colors Are Shown

TC-006-2 Operative Limited Access
    [Tags]    AC-006-2    SC-006-2
    [Documentation]    Test operative sees only revealed card colors
    Given Operative Player
    When Querying Board Information
    Then Only Revealed Card Colors Are Visible
    And Unrevealed Cards Show No Color

TC-006-3 USER Information Filtering
    [Tags]    AC-006-3    SC-006-3
    [Documentation]    Test USER type player information filtering
    Given USER Type Player
    When Accessing Game Information
    Then Data Is Human-Readable
    And Sensitive Information Is Appropriately Filtered

TC-006-4 LLM Structured Context
    [Tags]    AC-006-4    SC-006-4
    [Documentation]    Test LLM type player receives structured data
    Given LLM Type Player
    When Accessing Game Information
    Then Structured Data Is Provided
    And Context Is Suitable For AI Decision-Making
```

### 2.4 Spymaster Clue Giving (F004)

#### FR-007: Give Valid Clue
**Priority**: High  
**Risk**: High  

**Description**: The system shall accept and validate spymaster clues according to Codenames rules.

**System Constraints**:
- SC-007-1: Must be exactly one word (no hyphens, spaces, or compound words) [Tested by: TC-007-3]
- SC-007-2: Cannot be a word currently on the board (case-insensitive) [Tested by: TC-007-2]
- SC-007-3: Must include a number (0-9) indicating related cards [Tested by: TC-007-4]

**Acceptance Criteria**:
- AC-007-1: GIVEN spymaster's turn, WHEN giving a valid clue (word + number), THEN clue is accepted and recorded [Tested by: TC-007-1]
- AC-007-2: GIVEN a clue is given, WHEN checking game state, THEN turn switches to operative guessing phase [Tested by: TC-007-1]
- AC-007-3: GIVEN a recorded clue, WHEN operatives query current clue, THEN clue word and number are available [Tested by: TC-007-1]
- AC-007-4: GIVEN clue validation, WHEN clue word matches board word, THEN clue is rejected [Tested by: TC-007-2]

**Test Cases**:
```robot
*** Test Cases ***

TC-007-1 Valid Clue Acceptance
    [Tags]    AC-007-1    AC-007-2    AC-007-3
    [Documentation]    Test that valid clue is accepted and recorded
    Given Spymaster Turn With Board Containing    APPLE    TREE    CAR
    When Spymaster Gives Clue    FRUIT    2
    Then Clue Is Accepted And Recorded
    And Turn Switches To Operative Guessing Phase

TC-007-2 Invalid Clue Word On Board
    [Tags]    AC-007-4    SC-007-2
    [Documentation]    Test that clue word matching board word is rejected
    Given Spymaster Turn With Board Containing    APPLE    TREE    CAR
    When Spymaster Gives Clue    APPLE    1
    Then Error Is Returned    Clue word cannot match board words
    And Turn Remains With Spymaster

TC-007-3 Invalid Clue Multiple Words
    [Tags]    SC-007-1
    [Documentation]    Test that multi-word clue is rejected
    Given Spymaster Turn
    When Spymaster Gives Clue    RED FRUIT    2
    Then Error Is Returned    Clue must be exactly one word
    And Turn Remains With Spymaster

TC-007-4 Invalid Clue Number Out Of Range
    [Tags]    SC-007-3
    [Documentation]    Test that clue number outside 0-9 range is rejected
    Given Spymaster Turn
    When Spymaster Gives Clue    FRUIT    15
    Then Error Is Returned    Clue number must be 0-9
    And Turn Remains With Spymaster
```

#### FR-008: Clue History Tracking
**Priority**: Low  
**Risk**: Low  

**Description**: The system shall maintain a history of all clues given during the game.

**System Constraints**:
- SC-008-1: Must store all clues in chronological order [Tested by: TC-008-1]
- SC-008-2: Must record clue word, number, team, and timestamp for each clue [Tested by: TC-008-2]
- SC-008-3: Must preserve clue history for game duration [Tested by: TC-008-2]
- SC-008-4: Clue history must be accessible for validation and gameplay [Tested by: TC-008-3]

**Acceptance Criteria**:
- AC-008-1: GIVEN multiple clues given, WHEN querying clue history, THEN all clues are listed in chronological order [Tested by: TC-008-1]
- AC-008-2: GIVEN a clue in history, WHEN checking details, THEN clue word, number, team, and timestamp are recorded [Tested by: TC-008-2]
- AC-008-3: GIVEN clue history, WHEN validating new clue, THEN previous clues are considered for uniqueness [Tested by: TC-008-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-008-1 Chronological Clue Ordering
    [Tags]    AC-008-1    SC-008-1
    [Documentation]    Test clues are stored in chronological order
    Given Multiple Clues Have Been Given
    When Querying Clue History
    Then Clues Are Listed In Chronological Order
    And Most Recent Clue Appears Last

TC-008-2 Complete Clue Details
    [Tags]    AC-008-2    SC-008-2    SC-008-3
    [Documentation]    Test complete clue information is recorded
    Given Clue Has Been Recorded
    When Checking Clue Details In History
    Then Clue Word Is Recorded
    And Clue Number Is Recorded
    And Team Is Recorded
    And Timestamp Is Recorded

TC-008-3 Clue Validation Against History
    [Tags]    AC-008-3    SC-008-4
    [Documentation]    Test clue history is accessible for validation
    Given Clue History Exists
    When Validating New Clue
    Then Previous Clues Are Checked
    And History Is Accessible For Validation Rules
```

### 2.5 Team Guessing (F005)

#### FR-009: Make Valid Guess
**Priority**: High  
**Risk**: High  

**Description**: The system shall process operative guesses and update game state accordingly.

**System Constraints**:
- SC-009-1: Word must exist on the current board [Tested by: TC-009-1]
- SC-009-2: Word must not be already revealed [Tested by: TC-009-1]
- SC-009-3: Guess count is limited by current clue number + 1 [Tested by: TC-009-2]
- SC-009-4: Team can choose to end turn without using all guesses [Tested by: TC-009-5]

**Acceptance Criteria**:
- AC-009-1: GIVEN operative's turn, WHEN guessing a valid unrevealed word, THEN word is revealed with its color [Tested by: TC-009-1]
- AC-009-2: GIVEN a correct team guess, WHEN word matches team color, THEN team can continue guessing (within clue limit) [Tested by: TC-009-2]
- AC-009-3: GIVEN an incorrect guess, WHEN word is neutral or opponent color, THEN turn ends immediately [Tested by: TC-009-3]
- AC-009-4: GIVEN assassin guess, WHEN operative selects assassin card, THEN game ends with guessing team losing [Tested by: TC-009-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-009-1 Valid Guess Processing
    [Tags]    AC-009-1    SC-009-1    SC-009-2
    [Documentation]    Test processing of valid unrevealed word guess
    Given Operative Turn With Clue    FRUIT    2
    And Unrevealed Word    APPLE
    When Operative Guesses    APPLE
    Then Word APPLE Is Revealed With Its Color
    And Guess Count Is Decremented
    And Feedback On Correctness Is Provided

TC-009-2 Correct Team Guess Continuation
    [Tags]    AC-009-2    SC-009-3
    [Documentation]    Test team can continue guessing after correct guess
    Given Operative Turn With Team Color Match
    When Operative Guesses Correctly
    Then Team Can Continue Guessing Within Clue Limit
    And Remaining Guess Count Is Shown

TC-009-3 Incorrect Guess Ends Turn
    [Tags]    AC-009-3
    [Documentation]    Test turn ends on incorrect guess
    Given Operative Turn
    When Operative Guesses Neutral Or Opponent Color
    Then Turn Ends Immediately
    And Turn Switches To Opposing Team

TC-009-4 Assassin Game Over
    [Tags]    AC-009-4
    [Documentation]    Test game ends when assassin is guessed
    Given Operative Turn
    When Operative Guesses Assassin Card
    Then Game Ends Immediately
    And Guessing Team Loses

TC-009-5 Voluntary Turn End
    [Tags]    SC-009-4
    [Documentation]    Test operative can voluntarily end turn
    Given Operative Turn With Remaining Guesses
    When Operative Chooses To End Turn
    Then Turn Ends Without Using All Guesses
    And Turn Switches To Opposing Team
```

#### FR-010: Guess Validation and Feedback
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall validate guesses and provide immediate feedback.

**System Constraints**:
- SC-010-1: Must be a word currently on the board (case-insensitive) [Tested by: TC-010-1]
- SC-010-2: Cannot guess already revealed words [Tested by: TC-010-2]
- SC-010-3: Must provide immediate feedback on guess correctness [Tested by: TC-010-3]

**Acceptance Criteria**:
- AC-010-1: GIVEN an invalid word guess, WHEN word not on board, THEN error message is returned and turn continues [Tested by: TC-010-1]
- AC-010-2: GIVEN already revealed word, WHEN guessed again, THEN error message is returned and turn continues [Tested by: TC-010-2]
- AC-010-3: GIVEN valid guess processing, WHEN guess is made, THEN immediate feedback on correctness is provided [Tested by: TC-010-3]
- AC-010-4: GIVEN guess feedback, WHEN guess is processed, THEN remaining guess count is updated [Tested by: TC-010-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-010-1 Invalid Word Not On Board
    [Tags]    AC-010-1    SC-010-1
    [Documentation]    Test error when guessing word not on board
    Given Operative Turn
    When Operative Guesses    ZEBRA
    Then Error Is Returned    Word not found on board
    And Turn Continues With Same Operative

TC-010-2 Already Revealed Word
    [Tags]    AC-010-2    SC-010-2
    [Documentation]    Test error when guessing already revealed word
    Given Operative Turn
    And Word Was Previously Revealed    APPLE
    When Operative Guesses    APPLE
    Then Error Is Returned    Word already revealed
    And Turn Continues With Same Operative

TC-010-3 Valid Guess Feedback
    [Tags]    AC-010-3    AC-010-4    SC-010-3
    [Documentation]    Test immediate feedback and count update
    Given Operative Turn With Guesses Remaining    2
    When Operative Guesses Valid Unrevealed Word
    Then Immediate Feedback On Card Type Is Provided
    And Remaining Guess Count Is Updated Appropriately
```

### 2.6 Turn Management (F006)

#### FR-011: Turn Progression
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall manage turn progression between spymaster and operative phases, and between teams.

**System Constraints**:
- SC-011-1: Spymaster phase must precede operative phase [Tested by: TC-011-1]
- SC-011-2: Turn switches to opposing team after operative phase ends [Tested by: TC-011-2]
- SC-011-3: Must track current team and phase accurately [Tested by: TC-011-3]
- SC-011-4: Must identify specific player role for current turn [Tested by: TC-011-3]

**Acceptance Criteria**:
- AC-011-1: GIVEN spymaster gives clue, WHEN clue is accepted, THEN turn switches to operative guessing phase [Tested by: TC-011-1]
- AC-011-2: GIVEN operative guessing phase, WHEN turn ends (wrong guess/pass/limit reached), THEN turn switches to opposing team spymaster [Tested by: TC-011-2]
- AC-011-3: GIVEN turn switches, WHEN checking current turn, THEN correct team and phase are indicated [Tested by: TC-011-3]
- AC-011-4: GIVEN any phase, WHEN querying whose turn, THEN specific player or team role is identified [Tested by: TC-011-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-011-1 Normal Turn Progression
    [Tags]    AC-011-1    SC-011-1
    [Documentation]    Test normal progression from spymaster to operative phase
    Given Red Spymaster Gives Valid Clue
    When Clue Is Processed
    Then Turn Switches To Red Operative Guessing Phase
    And Operative Can Make Guesses Up To Clue Number Plus 1

TC-011-2 Turn Ends On Wrong Guess
    [Tags]    AC-011-2    SC-011-2
    [Documentation]    Test turn ends and switches teams on wrong guess
    Given Operative Guessing Phase With Remaining Guesses
    When Operative Guesses Neutral Or Opponent Color
    Then Turn Ends Immediately
    And Turn Switches To Opposing Team Spymaster

TC-011-3 Turn State Tracking
    [Tags]    AC-011-3    AC-011-4    SC-011-3    SC-011-4
    [Documentation]    Test accurate tracking of current turn state
    Given Any Point In Game
    When Querying Current Turn State
    Then System Returns Specific Team And Phase
    And Identifies Which Player Should Act Next
```

Scenario: Turn ends on voluntary pass (AC-011-2)
  Given operative with remaining guesses
  When operative chooses to end turn
  Then turn switches to opposing team spymaster
  And remaining guesses are forfeited
```

### 2.7 Win/Loss Detection (F007)

#### FR-012: Team Victory Conditions
**Priority**: High  
**Risk**: High  

**Description**: The system shall detect and declare victory when a team finds all their words.

**System Constraints**:
- SC-012-1: Victory check must occur after each card reveal [Tested by: TC-012-1]
- SC-012-2: Game must end immediately upon victory condition [Tested by: TC-012-1]
- SC-012-3: Winning team must be clearly identified and recorded [Tested by: TC-012-2]
- SC-012-4: Game status must change to "finished" upon victory [Tested by: TC-012-1]

**Acceptance Criteria**:
- AC-012-1: GIVEN red team words, WHEN all red cards are revealed, THEN red team wins immediately [Tested by: TC-012-1]
- AC-012-2: GIVEN blue team words, WHEN all blue cards are revealed, THEN blue team wins immediately [Tested by: TC-012-2]
- AC-012-3: GIVEN victory condition, WHEN team wins, THEN game status changes to "finished" [Tested by: TC-012-1]
- AC-012-4: GIVEN finished game, WHEN checking winner, THEN winning team is clearly identified [Tested by: TC-012-2]

**Test Cases**:
```robot
*** Test Cases ***

TC-012-1 Red Team Victory
    [Tags]    AC-012-1    AC-012-3    SC-012-1    SC-012-2
    [Documentation]    Test red team wins when all red cards revealed
    Given Game With Nine Red Cards On Board
    And Eight Red Cards Already Revealed
    When Red Team Reveals Final Red Card
    Then Red Team Wins Immediately
    And Game Status Changes To Finished

TC-012-2 Blue Team Victory
    [Tags]    AC-012-2    AC-012-4    SC-012-3
    [Documentation]    Test blue team wins when all blue cards revealed
    Given Game With Eight Blue Cards On Board
    And Seven Blue Cards Already Revealed
    When Blue Team Reveals Final Blue Card
    Then Blue Team Wins Immediately
    And Winner Query Returns Blue Team
```

#### FR-013: Assassin Loss Condition
**Priority**: High  
**Risk**: High  

**Description**: The system shall end the game immediately if the assassin card is revealed.

**System Constraints**:
- SC-013-1: Game must end immediately upon assassin reveal [Tested by: TC-013-1]
- SC-013-2: Team that guessed assassin loses automatically [Tested by: TC-013-1]
- SC-013-3: Opposing team wins by default (no need to complete cards) [Tested by: TC-013-1]
- SC-013-4: Game status must record assassin as loss reason [Tested by: TC-013-2]

**Acceptance Criteria**:
- AC-013-1: GIVEN any team's turn, WHEN assassin card is guessed, THEN game ends immediately [Tested by: TC-013-1]
- AC-013-2: GIVEN assassin revealed, WHEN checking winner, THEN opposing team (who didn't guess assassin) wins [Tested by: TC-013-1]
- AC-013-3: GIVEN assassin loss, WHEN checking game status, THEN status is "finished" with reason "assassin" [Tested by: TC-013-2]

**Test Cases**:
```robot
*** Test Cases ***

TC-013-1 Red Team Hits Assassin
    [Tags]    AC-013-1    AC-013-2    SC-013-1    SC-013-2
    [Documentation]    Test red team hitting assassin results in blue team victory
    Given Red Teams Operative Turn
    When Red Operative Guesses Assassin Card
    Then Game Ends Immediately
    And Blue Team Wins
    And Red Team Loses Due To Assassin

TC-013-2 Assassin Loss Reason Tracking
    [Tags]    AC-013-3    SC-013-4
    [Documentation]    Test assassin loss reason is properly recorded
    Given Any Team Hits Assassin
    When Checking Final Game Status
    Then Status Is Finished
    And Loss Reason Is Recorded As Assassin
    And Winning Team Is Clearly Identified
```

### 2.8 MCP Tool Interface (F008)

#### FR-014: Tool Registration
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall register appropriate MCP tools for game interaction.

**System Constraints**:
- SC-014-1: Must register all game management tools at server startup [Tested by: TC-014-1]
- SC-014-2: Tool schemas must provide accurate validation for inputs [Tested by: TC-014-2]
- SC-014-3: Must include required tools: create_game, join_game, start_game, give_clue, make_guess, get_game_state, get_board_view, end_turn [Tested by: TC-014-1]
- SC-014-4: Tool execution must map to appropriate game functions [Tested by: TC-014-3]

**Acceptance Criteria**:
- AC-014-1: GIVEN MCP server startup, WHEN tools are registered, THEN all game management tools are available [Tested by: TC-014-1]
- AC-014-2: GIVEN tool registration, WHEN listing tools, THEN tool descriptions and schemas are accurate [Tested by: TC-014-2]
- AC-014-3: GIVEN tool schemas, WHEN validating inputs, THEN proper JSON schema validation occurs [Tested by: TC-014-2]
- AC-014-4: GIVEN tool execution, WHEN called with valid parameters, THEN appropriate game functions are invoked [Tested by: TC-014-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-014-1 Tool Registration At Startup
    [Tags]    AC-014-1    SC-014-1    SC-014-3
    [Documentation]    Test all required game tools are registered at server startup
    Given MCP Server Is Starting
    When Server Initialization Completes
    Then All Required Game Tools Are Registered
    And Tools List Includes Create Game Join Game Start Game Give Clue Make Guess Get Game State Get Board View End Turn

TC-014-2 Tool Schema Validation
    [Tags]    AC-014-2    AC-014-3    SC-014-2
    [Documentation]    Test tool schemas provide accurate validation
    Given Registered Tools With Schemas
    When Client Queries Tool Definitions
    Then Accurate Schemas Are Returned
    And Input Validation Works According To Schemas

TC-014-3 Tool Execution Mapping
    [Tags]    AC-014-4    SC-014-4
    [Documentation]    Test tool calls map to appropriate game functions
    Given Registered MCP Tool
    When Called With Valid Parameters
    Then Corresponding Game Function Is Invoked
    And Appropriate Response Is Returned
```

#### FR-015: Resource Management
**Priority**: High  
**Risk**: Low  

**Description**: The system shall provide game state and rules as MCP resources.

**System Constraints**:
- SC-015-1: Must provide complete Codenames rules as accessible resource [Tested by: TC-015-1]
- SC-015-2: Game state resource must be in structured format [Tested by: TC-015-2]
- SC-015-3: Must notify clients of resource updates when game state changes [Tested by: TC-015-3]
- SC-015-4: Resource access must be consistent and reliable [Tested by: TC-015-1, TC-015-2]
- SC-015-5: Rules resource must include game flow and player interaction patterns [Tested by: TC-015-1]
- SC-015-6: Must provide example game scenarios for client understanding [Tested by: TC-015-4]

**Acceptance Criteria**:
- AC-015-1: GIVEN resource requests, WHEN querying game rules, THEN complete Codenames rules are provided [Tested by: TC-015-1]
- AC-015-2: GIVEN game in progress, WHEN requesting game state resource, THEN current state is provided in structured format [Tested by: TC-015-2]
- AC-015-3: GIVEN resource updates, WHEN game state changes, THEN clients are notified of resource updates [Tested by: TC-015-3]
- AC-015-4: GIVEN client discovery, WHEN accessing rules resource, THEN game flow patterns and interaction examples are included [Tested by: TC-015-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-015-1 Game Rules Resource Access
    [Tags]    AC-015-1    SC-015-1    SC-015-4
    [Documentation]    Test complete Codenames rules are accessible as resource
    Given MCP Server Is Running
    When Client Requests Game Rules Resource
    Then Complete Codenames Rules Are Returned
    And Rules Include All Game Mechanics And Victory Conditions

TC-015-2 Game State Resource Format
    [Tags]    AC-015-2    SC-015-2    SC-015-4
    [Documentation]    Test game state resource provides structured format
    Given Active Game
    When Client Requests Game State Resource
    Then Structured Format Is Returned
    And Includes Current Turn Board State And Revealed Cards

TC-015-3 Resource Update Notifications
    [Tags]    AC-015-3    SC-015-3
    [Documentation]    Test clients receive resource update notifications
    Given Client Subscribed To Resources
    When Game State Changes Card Revealed Turn Switch
    Then Resource Update Notification Is Sent
    And Client Can Retrieve Updated Game State

TC-015-4 Client Discovery Support
    [Tags]    AC-015-4    SC-015-5    SC-015-6
    [Documentation]    Test rules resource supports client discovery and learning
    Given New Client Connection
    When Rules Resource Is Accessed
    Then Complete Game Rules Are Provided
    And Game Flow Patterns Are Explained
    And Example Scenarios Are Included
    And Client Can Understand Required Actions
```

### 2.9 Sampling Integration (F009)

#### FR-016: AI Decision Support
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall use MCP sampling to request AI decisions for LLM players.

**System Constraints**:
- SC-016-1: Must provide complete game context in sampling requests [Tested by: TC-016-1, TC-016-2]
- SC-016-2: Must validate LLM responses before executing as game actions [Tested by: TC-016-3]
- SC-016-3: Must implement fallback handling for sampling failures [Tested by: TC-016-4]
- SC-016-4: Sampling context must be role-appropriate (spymaster vs operative) [Tested by: TC-016-1, TC-016-2]

**Acceptance Criteria**:
- AC-016-1: GIVEN LLM spymaster turn, WHEN clue is needed, THEN sampling request is sent with game context [Tested by: TC-016-1]
- AC-016-2: GIVEN LLM operative turn, WHEN guess is needed, THEN sampling request includes current clue and board state [Tested by: TC-016-2]
- AC-016-3: GIVEN sampling response, WHEN LLM provides decision, THEN response is validated and executed as if human input [Tested by: TC-016-3]
- AC-016-4: GIVEN sampling failure, WHEN LLM doesn't respond, THEN appropriate fallback or error handling occurs [Tested by: TC-016-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-016-1 LLM Spymaster Sampling
    [Tags]    AC-016-1    SC-016-1    SC-016-4
    [Documentation]    Test LLM spymaster sampling with appropriate context
    Given LLM Spymasters Turn
    When Clue Decision Is Needed
    Then Sampling Request Includes Team Words And Board State
    And Context Is Filtered For Spymaster Role

TC-016-2 LLM Operative Sampling
    [Tags]    AC-016-2    SC-016-1    SC-016-4
    [Documentation]    Test LLM operative sampling with role-appropriate context
    Given LLM Operatives Turn With Active Clue
    When Guess Decision Is Needed
    Then Sampling Request Includes Current Clue And Visible Board
    And Context Is Filtered For Operative Role

TC-016-3 Response Validation
    [Tags]    AC-016-3    SC-016-2
    [Documentation]    Test LLM response validation and execution
    Given LLM Sampling Response Received
    When Processing AI Decision
    Then Response Is Validated Against Game Rules
    And Valid Responses Are Executed As Player Actions

TC-016-4 Sampling Failure Handling
    [Tags]    AC-016-4    SC-016-3
    [Documentation]    Test handling of LLM sampling failures
    Given LLM Sampling Request Times Out
    When No Response Is Received
    Then Appropriate Error Handling Occurs
    And Game State Remains Consistent
```

#### FR-017: Context-Aware Prompting
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall provide appropriate context in sampling requests based on player role and game state.

**System Constraints**:
- SC-017-1: Must filter sensitive information based on player role [Tested by: TC-017-2, TC-017-4]
- SC-017-2: Must include relevant game history in sampling context [Tested by: TC-017-3]
- SC-017-3: Spymaster context must include team words and full board state [Tested by: TC-017-1]
- SC-017-4: Operative context must include only visible board and current clue [Tested by: TC-017-2]

**Acceptance Criteria**:
- AC-017-1: GIVEN spymaster LLM sampling, WHEN requesting clue, THEN team words and board state are provided [Tested by: TC-017-1]
- AC-017-2: GIVEN operative LLM sampling, WHEN requesting guess, THEN current clue and visible board state are provided [Tested by: TC-017-2]
- AC-017-3: GIVEN sampling context, WHEN providing game history, THEN relevant previous clues and guesses are included [Tested by: TC-017-3]
- AC-017-4: GIVEN role-based context, WHEN sampling, THEN sensitive information is filtered based on player role [Tested by: TC-017-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-017-1 Spymaster Context Provision
    [Tags]    AC-017-1    SC-017-3
    [Documentation]    Test spymaster LLM gets complete board context
    Given LLM Spymaster Sampling Request
    When Context Is Prepared
    Then Team Words Are Included
    And Full Board State With All Colors Is Provided

TC-017-2 Operative Context Filtering
    [Tags]    AC-017-2    SC-017-1    SC-017-4
    [Documentation]    Test operative LLM gets filtered context
    Given LLM Operative Sampling Request
    When Context Is Prepared
    Then Only Current Clue Is Included
    And Board Shows Only Revealed Cards
    And Team Colors Are Hidden For Unrevealed Cards

TC-017-3 Game History Inclusion
    [Tags]    AC-017-3    SC-017-2
    [Documentation]    Test game history is included in sampling context
    Given Sampling Request With Game In Progress
    When Context Includes History
    Then Relevant Previous Clues And Guesses Are Included
    And Context Is Appropriately Sized For AI Processing

TC-017-4 Role Based Filtering
    [Tags]    AC-017-4    SC-017-1
    [Documentation]    Test role-based information filtering in sampling
    Given Different Player Roles Requesting Context
    When Sampling Context Is Prepared
    Then Sensitive Information Is Filtered Per Role
    And Spymasters See More Than Operatives
```

#### FR-018: User Elicitation Support
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall use MCP elicitation to request decisions from USER players when appropriate.

**System Constraints**:
- SC-018-1: Must provide game context with available options for user decisions [Tested by: TC-018-1, TC-018-2]
- SC-018-2: Must filter sensitive information based on user's role [Tested by: TC-018-3]
- SC-018-3: Must include relevant game state and history for informed decisions [Tested by: TC-018-2]
- SC-018-4: Elicitation format must be human-readable and clear [Tested by: TC-018-1]

**Acceptance Criteria**:
- AC-018-1: GIVEN USER spymaster turn, WHEN clue input is needed, THEN elicitation request is sent with game context and available options [Tested by: TC-018-1]
- AC-018-2: GIVEN USER operative turn, WHEN guess is needed, THEN elicitation request includes current clue and available words [Tested by: TC-018-2]
- AC-018-3: GIVEN elicitation context, WHEN providing game state, THEN relevant previous clues and guesses are included [Tested by: TC-018-2]
- AC-018-4: GIVEN role-based elicitation, WHEN requesting input, THEN sensitive information is filtered based on player role [Tested by: TC-018-3]

**Test Cases**:
```robot
*** Test Cases ***

TC-018-1 User Spymaster Elicitation
    [Tags]    AC-018-1    SC-018-1    SC-018-4
    [Documentation]    Test USER spymaster elicitation with game context
    Given USER Spymasters Turn
    When Clue Input Is Required
    Then Elicitation Request Is Sent
    And Context Includes Game State And Team Words
    And Format Is Human-Readable

TC-018-2 User Operative Elicitation
    [Tags]    AC-018-2    AC-018-3    SC-018-1    SC-018-3
    [Documentation]    Test USER operative elicitation with appropriate context
    Given USER Operatives Turn With Active Clue
    When Guess Input Is Required
    Then Elicitation Includes Current Clue
    And Shows Available Unrevealed Words
    And Includes Relevant Game History

TC-018-3 Role Based Information Filtering
    [Tags]    AC-018-4    SC-018-2
    [Documentation]    Test role-based filtering in user elicitation
    Given USER Player Elicitation
    When Context Is Prepared
    Then Information Is Filtered Based On Player Role
    And Operatives Dont See Hidden Card Colors
    And Spymasters See Complete Board State
```

### 2.10 Information Isolation (F010)

#### FR-019: Spymaster Information Security
**Priority**: High  
**Risk**: High  

**Description**: The system shall prevent information leakage between spymasters and operatives.

**System Constraints**:
- SC-019-1: Card colors must be hidden from operatives until revealed [Tested by: TC-019-1]
- SC-019-2: All card colors must be visible to spymasters [Tested by: TC-019-2]
- SC-019-3: Role-based filtering must be applied consistently regardless of team [Tested by: TC-019-3]
- SC-019-4: Information serialization must respect role-based access controls [Tested by: TC-019-4]

**Acceptance Criteria**:
- AC-019-1: GIVEN operative player request, WHEN querying board, THEN card colors are hidden except for revealed cards [Tested by: TC-019-1]
- AC-019-2: GIVEN spymaster player request, WHEN querying board, THEN all card colors are visible [Tested by: TC-019-2]
- AC-019-3: GIVEN role-based requests, WHEN accessing information, THEN appropriate data filtering is applied based on spymaster vs operative role regardless of team [Tested by: TC-019-3]
- AC-019-4: GIVEN information isolation, WHEN data is serialized, THEN role-appropriate filtering is applied [Tested by: TC-019-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-019-1 Operative Board View Filtering
    [Tags]    AC-019-1    SC-019-1
    [Documentation]    Test operative sees only revealed card colors
    Given Game With Mixed Revealed Unrevealed Cards
    When Operative Requests Board View
    Then Only Revealed Card Colors Are Shown
    And Unrevealed Cards Show No Color Information

TC-019-2 Spymaster Full Board Access
    [Tags]    AC-019-2    SC-019-2
    [Documentation]    Test spymaster sees all card colors
    Given Game With Mixed Revealed Unrevealed Cards
    When Spymaster Requests Board View
    Then All Card Colors Are Visible
    And Complete Board State Is Provided

TC-019-3 Cross Team Role Consistency
    [Tags]    AC-019-3    SC-019-3
    [Documentation]    Test role-based filtering is consistent across teams
    Given Red Spymaster And Blue Operative
    When Each Requests Board Information
    Then Red Spymaster Sees All Colors
    And Blue Operative Sees Only Revealed Colors
    And Filtering Is Role-Based Not Team-Based

TC-019-4 Data Serialization Security
    [Tags]    AC-019-4    SC-019-4
    [Documentation]    Test role-appropriate filtering during serialization
    Given Board Data Being Serialized For Client
    When Serialization Occurs
    Then Role-Appropriate Filtering Is Applied
    And Sensitive Data Is Not Exposed To Wrong Roles
```

#### FR-020: Player Type Security
**Priority**: High  
**Risk**: High  

**Description**: The system shall handle USER and LLM player types with appropriate information access.

**System Constraints**:
- SC-020-1: USER players must receive human-readable format with role-based filtering [Tested by: TC-020-1]
- SC-020-2: LLM players must receive structured data suitable for AI processing [Tested by: TC-020-2]
- SC-020-3: Information format and filtering must be applied per player type [Tested by: TC-020-3]
- SC-020-4: Player type must be validated and recorded during game join [Tested by: TC-020-4]

**Acceptance Criteria**:
- AC-020-1: GIVEN USER type player, WHEN requesting information, THEN human-readable format is provided with appropriate filtering [Tested by: TC-020-1]
- AC-020-2: GIVEN LLM type player, WHEN requesting information, THEN structured data suitable for AI processing is provided [Tested by: TC-020-2]
- AC-020-3: GIVEN mixed player types, WHEN information is accessed, THEN appropriate format and filtering per player type [Tested by: TC-020-3]
- AC-020-4: GIVEN player type validation, WHEN player joins, THEN type is validated and recorded correctly [Tested by: TC-020-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-020-1 USER Player Information Format
    [Tags]    AC-020-1    SC-020-1
    [Documentation]    Test USER type player receives human-readable information
    Given USER Type Spymaster
    When Requesting Game Information
    Then Human-Readable Format Is Provided
    And Role-Based Filtering Shows All Card Colors
    And Format Is Suitable For Human Consumption

TC-020-2 LLM Player Structured Data
    [Tags]    AC-020-2    SC-020-2
    [Documentation]    Test LLM type player receives structured data
    Given LLM Type Operative
    When Requesting Game Information
    Then Structured Data Format Is Provided
    And Role-Based Filtering Hides Unrevealed Colors
    And Format Is Suitable For AI Processing

TC-020-3 Mixed Player Type Handling
    [Tags]    AC-020-3    SC-020-3
    [Documentation]    Test mixed player types receive appropriate formats
    Given Game With USER Spymaster And LLM Operative
    When Both Request Board Information
    Then USER Gets Human-Readable Format With Full Colors
    And LLM Gets Structured Data With Filtered Colors
    And Each Receives Appropriate Format For Their Type

TC-020-4 Player Type Validation
    [Tags]    AC-020-4    SC-020-4
    [Documentation]    Test player type validation during game join
    Given Player Attempting To Join Game
    When Player Type Is Specified
    Then Type Is Validated As USER Or LLM
    And Player Type Is Recorded Correctly
    And Invalid Types Are Rejected
```

## 3. Non-Functional Requirements

### 3.1 MCP Protocol Compliance (NF001)

#### NFR-001: Protocol Adherence
**Priority**: High  
**Risk**: Medium  

**Description**: The system shall fully comply with MCP specification requirements.

**System Constraints**:
- SC-NF001-1: Must declare correct capabilities during protocol negotiation [Tested by: TC-NF001-1]
- SC-NF001-2: All tool responses must conform to MCP message format [Tested by: TC-NF001-2]
- SC-NF001-3: Resource responses must follow MCP resource specification [Tested by: TC-NF001-3]
- SC-NF001-4: Sampling requests must conform to MCP sampling specification [Tested by: TC-NF001-4]
- SC-NF001-5: Elicitation requests must conform to MCP elicitation specification [Tested by: TC-NF001-5]

**Acceptance Criteria**:
- AC-NF001-1: GIVEN MCP client connection, WHEN protocol negotiation occurs, THEN correct capabilities are declared [Tested by: TC-NF001-1]
- AC-NF001-2: GIVEN tool execution, WHEN called via MCP, THEN responses conform to MCP message format [Tested by: TC-NF001-2]
- AC-NF001-3: GIVEN resource requests, WHEN accessed via MCP, THEN responses follow MCP resource specification [Tested by: TC-NF001-3]
- AC-NF001-4: GIVEN sampling requests, WHEN made via MCP, THEN requests conform to MCP sampling specification [Tested by: TC-NF001-4]
- AC-NF001-5: GIVEN elicitation requests, WHEN requesting user input via MCP, THEN requests conform to MCP elicitation specification [Tested by: TC-NF001-5]

**Test Cases**:
```robot
*** Test Cases ***

TC-NF001-1 Protocol Capability Declaration
    [Tags]    AC-NF001-1    SC-NF001-1
    [Documentation]    Test correct MCP capabilities are declared during negotiation
    Given MCP Client Attempting Connection
    When Protocol Negotiation Occurs
    Then Correct Server Capabilities Are Declared
    And Client Can Identify Available Features

TC-NF001-2 Tool Response Format Compliance
    [Tags]    AC-NF001-2    SC-NF001-2
    [Documentation]    Test all tool responses conform to MCP format
    Given Tool Execution Via MCP
    When Response Is Generated
    Then Response Conforms To MCP Message Format
    And All Required Fields Are Present

TC-NF001-3 Resource Response Specification
    [Tags]    AC-NF001-3    SC-NF001-3
    [Documentation]    Test resource responses follow MCP specification
    Given Resource Request Via MCP
    When Resource Is Accessed
    Then Response Follows MCP Resource Specification
    And Content Type Is Correctly Specified

TC-NF001-4 Sampling Request Compliance
    [Tags]    AC-NF001-4    SC-NF001-4
    [Documentation]    Test sampling requests conform to MCP specification
    Given LLM Player Decision Needed
    When Sampling Request Is Made
    Then Request Conforms To MCP Sampling Specification
    And Context Is Properly Structured

TC-NF001-5 Elicitation Request Compliance
    [Tags]    AC-NF001-5    SC-NF001-5
    [Documentation]    Test elicitation requests conform to MCP specification
    Given USER Player Input Needed
    When Elicitation Request Is Made
    Then Request Conforms To MCP Elicitation Specification
    And Options Are Properly Formatted
```

### 3.2 Performance (NF002)

#### NFR-002: Response Time
**Priority**: Medium  
**Risk**: Low  

**Description**: The system shall respond to requests within acceptable time limits.

**System Constraints**:
- SC-NF002-1: Tool execution response time must be <2 seconds for 95% of requests [Tested by: TC-NF002-1]
- SC-NF002-2: Board generation must complete within 1 second [Tested by: TC-NF002-2]
- SC-NF002-3: Guess validation must respond within 500ms [Tested by: TC-NF002-3]
- SC-NF002-4: Performance must degrade gracefully under load [Tested by: TC-NF002-4]

**Acceptance Criteria**:
- AC-NF002-1: GIVEN tool execution, WHEN processing request, THEN response time is <2 seconds for 95% of requests [Tested by: TC-NF002-1]
- AC-NF002-2: GIVEN board generation, WHEN creating new game, THEN board is generated within 1 second [Tested by: TC-NF002-2]
- AC-NF002-3: GIVEN guess processing, WHEN validating guess, THEN response is provided within 500ms [Tested by: TC-NF002-3]
- AC-NF002-4: GIVEN concurrent games, WHEN multiple games active, THEN performance degrades gracefully [Tested by: TC-NF002-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-NF002-1 Tool Response Time Performance
    [Tags]    AC-NF002-1    SC-NF002-1
    [Documentation]    Test tool execution meets response time requirements
    Given Multiple Tool Execution Requests
    When Processing 100 Requests
    Then 95% Complete Within 2 Seconds
    And Average Response Time Is Acceptable

TC-NF002-2 Board Generation Performance
    [Tags]    AC-NF002-2    SC-NF002-2
    [Documentation]    Test board generation completes within time limit
    Given New Game Creation Request
    When Board Generation Is Triggered
    Then Board Generation Completes Within 1 Second
    And All 25 Words Are Selected And Assigned

TC-NF002-3 Guess Validation Performance
    [Tags]    AC-NF002-3    SC-NF002-3
    [Documentation]    Test guess validation meets response time requirements
    Given Operative Guess Request
    When Guess Validation Is Performed
    Then Response Is Provided Within 500ms
    And Validation Is Complete And Accurate

TC-NF002-4 Concurrent Load Performance
    [Tags]    AC-NF002-4    SC-NF002-4
    [Documentation]    Test performance degradation under concurrent load
    Given Multiple Concurrent Games
    When System Load Increases
    Then Performance Degrades Gracefully
    And Response Times Remain Within Acceptable Bounds
```

### 3.3 Multi-client Support (NF003)

#### NFR-003: Client Compatibility
**Priority**: Medium  
**Risk**: Medium  

**Description**: The system shall support multiple concurrent MCP clients and games.

**System Constraints**:
- SC-NF003-1: Must handle multiple simultaneous client connections [Tested by: TC-NF003-1]
- SC-NF003-2: Game states must remain isolated between concurrent games [Tested by: TC-NF003-2]
- SC-NF003-3: Must negotiate appropriate features with different client capabilities [Tested by: TC-NF003-3]
- SC-NF003-4: Game state must be preserved and recoverable on client disconnection [Tested by: TC-NF003-4]

**Acceptance Criteria**:
- AC-NF003-1: GIVEN multiple clients, WHEN connecting simultaneously, THEN all connections are handled correctly [Tested by: TC-NF003-1]
- AC-NF003-2: GIVEN concurrent games, WHEN multiple games run, THEN game states remain isolated [Tested by: TC-NF003-2]
- AC-NF003-3: GIVEN client capabilities, WHEN different clients connect, THEN appropriate feature negotiation occurs [Tested by: TC-NF003-3]
- AC-NF003-4: GIVEN client disconnection, WHEN client drops, THEN game state is preserved and recoverable [Tested by: TC-NF003-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-NF003-1 Multiple Client Connection Handling
    [Tags]    AC-NF003-1    SC-NF003-1
    [Documentation]    Test server handles multiple simultaneous client connections
    Given Multiple MCP Clients
    When Clients Connect Simultaneously
    Then All Connections Are Handled Correctly
    And Each Client Receives Proper Protocol Negotiation

TC-NF003-2 Game State Isolation
    [Tags]    AC-NF003-2    SC-NF003-2
    [Documentation]    Test game states remain isolated between concurrent games
    Given Multiple Concurrent Games
    When Games Run Simultaneously
    Then Game States Remain Completely Isolated
    And Actions In One Game Do Not Affect Others

TC-NF003-3 Client Feature Negotiation
    [Tags]    AC-NF003-3    SC-NF003-3
    [Documentation]    Test appropriate feature negotiation with different clients
    Given Clients With Different Capabilities
    When Clients Connect To Server
    Then Appropriate Feature Negotiation Occurs
    And Each Client Gets Compatible Feature Set

TC-NF003-4 Client Disconnection Recovery
    [Tags]    AC-NF003-4    SC-NF003-4
    [Documentation]    Test game state preservation on client disconnection
    Given Active Game With Connected Client
    When Client Disconnects Unexpectedly
    Then Game State Is Preserved
    And State Is Recoverable When Client Reconnects
```

### 3.4 State Consistency (NF004)

#### NFR-004: Data Integrity
**Priority**: High  
**Risk**: High  

**Description**: The system shall maintain consistent game state throughout gameplay.

**System Constraints**:
- SC-NF004-1: Game state must remain consistent during concurrent operations [Tested by: TC-NF004-1]
- SC-NF004-2: Game state must not be corrupted during error conditions [Tested by: TC-NF004-2]
- SC-NF004-3: State integrity must be maintained during save/load operations [Tested by: TC-NF004-3]
- SC-NF004-4: Game invariants must be enforced during state validation [Tested by: TC-NF004-4]

**Acceptance Criteria**:
- AC-NF004-1: GIVEN concurrent operations, WHEN multiple actions occur, THEN game state remains consistent [Tested by: TC-NF004-1]
- AC-NF004-2: GIVEN error conditions, WHEN failures occur, THEN game state is not corrupted [Tested by: TC-NF004-2]
- AC-NF004-3: GIVEN state persistence, WHEN saving/loading games, THEN state integrity is maintained [Tested by: TC-NF004-3]
- AC-NF004-4: GIVEN state validation, WHEN checking consistency, THEN invariants are enforced [Tested by: TC-NF004-4]

**Test Cases**:
```robot
*** Test Cases ***

TC-NF004-1 Concurrent Operation Consistency
    [Tags]    AC-NF004-1    SC-NF004-1
    [Documentation]    Test game state consistency during concurrent operations
    Given Game With Multiple Active Players
    When Concurrent Actions Are Attempted
    Then Game State Remains Consistent
    And No Race Conditions Occur

TC-NF004-2 Error Condition State Protection
    [Tags]    AC-NF004-2    SC-NF004-2
    [Documentation]    Test game state protection during error conditions
    Given Active Game State
    When Error Conditions Occur
    Then Game State Is Not Corrupted
    And State Remains Valid And Recoverable

TC-NF004-3 State Persistence Integrity
    [Tags]    AC-NF004-3    SC-NF004-3
    [Documentation]    Test state integrity during save and load operations
    Given Game State To Be Persisted
    When Save And Load Operations Occur
    Then State Integrity Is Maintained
    And All Game Data Is Preserved Accurately

TC-NF004-4 Game Invariant Enforcement
    [Tags]    AC-NF004-4    SC-NF004-4
    [Documentation]    Test enforcement of game invariants during validation
    Given Game State Validation Check
    When Checking State Consistency
    Then Game Invariants Are Enforced
    And Invalid States Are Detected And Rejected
```

## 5. Constraints and Assumptions

### 5.1 Technical Constraints
The following technical constraints apply to the system implementation:

**TC-001: Platform Dependencies**
- **Constraint**: Python 3.11+ runtime environment required
- **Rationale**: Leverages modern Python features and security updates
- **Impact**: Limits deployment environments but ensures stability
- **Testability**: Version compatibility testing required

**TC-002: Integration Dependencies** 
- **Constraint**: MCP Python SDK compatibility mandatory
- **Rationale**: Core protocol implementation dependency
- **Impact**: Updates must align with SDK releases
- **Testability**: SDK integration testing required

**TC-003: Data Format Constraints**
- **Constraint**: JSON serialization for all data exchange
- **Rationale**: MCP protocol requirement and interoperability
- **Impact**: No binary data formats; potential performance considerations
- **Testability**: Data format validation testing required

**TC-004: Storage Constraints**
- **Constraint**: No external database required (in-memory for MVP)
- **Rationale**: Simplifies deployment and reduces dependencies
- **Impact**: Data persistence limited; scalability constraints for production
- **Testability**: Memory usage and concurrent access testing required

### 5.2 Business Constraints
The following business constraints define scope limitations:

**BC-001: Rule Implementation Scope**
- **Constraint**: Standard Codenames rules implementation only
- **Rationale**: Maintain game authenticity and reduce complexity
- **Impact**: No custom rules or variations supported
- **Validation**: Rule compliance verification against official Codenames rules

**BC-002: Language Support Scope**
- **Constraint**: Initial word list will be English language (extensible for internationalization)
- **Rationale**: MVP scope limitation with future expansion capability
- **Impact**: Limited initial market but architecture supports expansion
- **Validation**: Word list validation and internationalization architecture review

**BC-003: Player Capacity Constraints**
- **Constraint**: Maximum 8 players per game instance
- **Rationale**: Standard Codenames player limit and resource management
- **Impact**: Large group games not supported
- **Validation**: Player limit enforcement testing

**BC-004: Game Integrity Constraints**
- **Constraint**: All game-affecting actions must occur through structured MCP game tools only
- **Rationale**: Ensures game state consistency, rule enforcement, and proper audit trail
- **Impact**: External communication channels may exist but cannot directly modify game state
- **Validation**: Game state modification testing and audit trail verification

### 5.3 System Assumptions
The following assumptions underpin the system design:

**AS-001: Client Capability Assumptions**
- **Assumption**: MCP clients handle all UI presentation responsibilities
- **Justification**: Separation of concerns - server provides game logic, clients handle display
- **Risk Level**: Low - standard MCP architecture pattern
- **Mitigation**: Client compatibility testing and clear API documentation

**AS-002: Infrastructure Assumptions**
- **Assumption**: Network connectivity is reliable for MCP communication
- **Justification**: Standard enterprise/development environment expectation
- **Risk Level**: Medium - network issues could impact gameplay
- **Mitigation**: Timeout handling and connection recovery mechanisms

**AS-003: User Knowledge Assumptions**
- **Assumption**: USER type players understand Codenames rules independently
- **Justification**: Target audience familiar with popular board game
- **Risk Level**: Low - widely known game with simple rules
- **Mitigation**: Clear error messages and game state feedback

**AS-004: LLM Context Assumptions**
- **Assumption**: LLM players receive complete game context through MCP without prior knowledge
- **Justification**: System designed to be self-contained for AI players
- **Risk Level**: Low - system provides all necessary context
- **Mitigation**: Comprehensive context provision and response validation

## 6. Test Strategy and Acceptance Criteria

### 6.1 Test Approach Overview
This section defines the overall testing strategy aligned with ISTQB test process standards, covering test planning, design, execution, and completion criteria.

### 6.2 Test Levels and Types

#### 6.2.1 Component Testing
**Scope**: Individual game logic components
- Unit tests for game state management
- Board generation algorithm testing  
- Word validation logic testing
- Role-based filtering mechanism testing

**Entry Criteria**: Code implementation complete
**Exit Criteria**: 95% code coverage, all unit tests passing

#### 6.2.2 Integration Testing
**Scope**: MCP protocol integration and component interactions
- MCP tool registration and execution
- Sampling and elicitation integration
- Client-server communication protocols
- Game state synchronization

**Entry Criteria**: Component testing complete
**Exit Criteria**: All integration scenarios pass, protocol compliance verified

#### 6.2.3 System Testing
**Scope**: Complete game functionality end-to-end
- Complete game workflow scenarios
- Multi-player game scenarios
- Concurrent game management
- Error handling and recovery

**Entry Criteria**: Integration testing complete
**Exit Criteria**: All system requirements validated, performance criteria met

#### 6.2.4 Acceptance Testing
**Scope**: Single game MVP functionality validation
- Complete single game workflow validation
- MCP protocol integration works
- Basic error handling for invalid inputs

**Entry Criteria**: System testing complete
**Exit Criteria**: Single complete game works end-to-end

### 6.3 User Acceptance Test Scenarios

#### 6.3.1 Core Gameplay Scenarios
**UAT-001: Complete Game Workflow**
- **Objective**: Validate full game lifecycle from creation to completion
- **Scope**: Game creation, player joining, board generation, clue giving, guessing, win conditions
- **Success Criteria**: Game completes successfully with correct winner determination
- **Priority**: Critical

**UAT-002: Mixed Player Types**
- **Objective**: Validate games with both USER and LLM players
- **Scope**: Role assignment, information filtering, decision making for both player types
- **Success Criteria**: Both player types function correctly with appropriate information access
- **Priority**: High

**UAT-003: Basic Error Handling**
- **Objective**: Validate system handles basic invalid inputs without crashing
- **Scope**: Invalid clues, wrong guesses, malformed requests
- **Success Criteria**: System provides error messages and continues functioning
- **Priority**: Medium

### 6.4 Basic Performance Validation

#### 6.4.1 MVP Performance Requirements
- **Single Game Operations**: Must complete without hanging or crashing
- **Board Generation**: Must complete successfully every time
- **Response Times**: Reasonable for local development/testing (no specific targets)

### 6.5 Basic Functionality Testing

#### 6.5.1 Core Game Integrity (MVP Focus)
- **Role-based Access**: Spymasters see all colors, operatives see only revealed
- **Game Rules**: Standard Codenames rules enforced correctly
- **MCP Integration**: All game tools work as expected

### 6.6 MVP Test Completion Criteria

#### 6.6.1 MVP Exit Criteria
- Single complete game works from start to finish (create → players join → play → someone wins)
- MCP protocol integration functional for all basic game tools
- Role-based information filtering works (spymasters see card colors, operatives don't)
- System doesn't crash on basic invalid inputs
- Critical game-breaking defects resolved

#### 6.6.2 MVP Test Focus
- **Must Work**: Single game completion, MCP tools, role filtering
- **Should Work**: Basic error handling, game rule enforcement  
- **Nice to Have**: Performance optimization, edge case handling

This minimal test strategy focuses solely on proving the core MVP concept works.
