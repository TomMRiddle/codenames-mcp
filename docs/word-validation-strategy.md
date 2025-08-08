# Word Validation Strategy for Codenames MCP Server

## Overview
Since we're accepting words from user input or LLM sampling instead of using pre-validated Codenames word sets, we need validation to ensure game rules are followed.

## Research Findings
- Official Codenames contains 200 cards with 400 codenames (double-sided)
- Example official words: "beach", "whale", "water", "ocean", "disease", "Germany", "carrot"
- Official game uses curated word sets that are pre-tested and balanced
- We should avoid over-engineering validation rules without seeing actual official word lists

## MVP Validation Rules (Simplified)

### Technical Requirements
1. **Exactly 25 words** - No more, no less
2. **No duplicates** - Each word must be unique (case-insensitive)
3. **No empty/invalid strings** - Basic string validation
4. **Basic profanity filter** - Content appropriateness for family-friendly gameplay

### Validation Tools to Implement
- `validate_word_list(words)` - Complete validation with detailed error reporting
- `validate_single_word(word)` - Check individual word against all rules
- `check_word_duplicates(words)` - Find exact duplicates (case-insensitive)
- `sanitize_word_input(word)` - Clean and normalize word input

### LLM Sampling Context for Word Generation
When requesting words via sampling, include context like:
- "Generate 25 diverse, single words suitable for a word association game"
- "Include a mix of nouns, adjectives, and concepts that can have multiple meanings"
- "Avoid offensive content and ensure words are family-friendly"
- "Words should be suitable for players aged 10+"

## Philosophy
- **Use empirical validation** based on gameplay testing rather than rigid assumptions
- **Keep validation minimal for MVP** - focus on technical requirements
- **Let gameplay quality emerge** through testing and LLM training
- **Avoid reverse-engineering** official Codenames criteria without data

## Future Considerations
- Could add word complexity analysis (syllable count, reading level)
- Could implement semantic similarity checks to avoid too many related words
- Could add custom word difficulty settings
- Could learn from successful games to improve word selection

## Resources for Implementation
- `game://rules/word-requirements` - Technical validation criteria
- `game://validation/common-errors` - Typical validation failures and fixes
- `game://validation/profanity-filter` - Content filtering patterns

---
*Document created: August 8, 2025*
*Status: Design phase - implementation pending*
