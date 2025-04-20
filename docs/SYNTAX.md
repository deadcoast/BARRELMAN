## SYNTAX LINE ZONES

```
┌─────┐                   ┌─────┐                ┌─────┐                ┌─────┐
│ [1] │                   │ [2] │                │ [3] │                │ [4] │
├─────┴───────────────────┼─────┴────────────────┼─────┴────────────────┼─────┴─────────────────┐
│  [1.1] DECLARATION      │  [2.1] CAUSE         │  [3.1] EFFECT        │  [4.1] OUTCOME        │
├─────────────────────────┼──────────────────────┼──────────────────────┼───────────────────────┤
│  [1.2] KEYWORD          │  [2.2] FUNCTION      │  [3.2] PARAMATER     │                       │
├─────────────────────────┼──────────────────────┼──────────────────────┼───────────────────────┤
│  [1.3] RELATION         │  [2.3] MODIFIER      │  [3.3] TRIGGER       │                       │
├─────────────────────────┼──────────────────────┼──────────────────────┼───────────────────────┤
│  [1.4] NEW LINE         │                      │                      │                       │
├┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┼┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┼┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┼┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┤
│                                                                                               │
│             [1.3]                                                                             │
│               ^                                                                               │
│         [1.2] │             [2.3]         [3.3]                                               │
│           ^   │               ^             ^                                                 │
│     [1.1] │   │       [2.2]   │      [3.2]  │                                                 │
│       ^   │   │         ^     │        ^    │                     [4.1]                       │
│ [1.4] │   │   │   [2.1] │     │  [3.1] │    │                      ^                          │
│   ^   │   │   │     ^   │     │    ^   │    │                      │                          │
│ ┌─┼───┴───┼───┼─┐ ┌─┴───┼─────┼─┐ ┌┴───┼────┼─┐ ┌──────────────────┴────────────────────────┐ │
│ │ +       +   + │ │     +     + │ │    +    + │ │                                           │ │
│ │ :: RACE[2] // │ │ AWAKENING % │ │ DENIED -> │ │ PLANETARY SYSTEM FAILURE [SELF-INITIATED] │ │
├─┴───────────────┴─┴─────────────┴─┴───────────┴─┴───────────────────────────────────────────┴─┤
│                                                                                               │
│         :: RACE[2] // AWAKENING % DENIED -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]         │
│                                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## **BARRELMAN - SYNTAX STRUCTURE**

| **Symbol** | **Function**    | **Semantic Meaning**                    |
| ---------- | --------------- | --------------------------------------- |
| //         | **Relation**    | “X is related to Y” or “X applies to Y” |
| %          | **Modifier**    | “Result of this relation or condition”  |
| ->         | **Trigger**     | “Outcome of Relation and Trigger”       |
| ::         | New Line String | "New Line Strings for Advanced Nesting" |
| :^:        | Port            | "Heirarchal Port"                       |

### BARRELMAN CORE:

- `::` is the visual cue to a new line starting
- `//` is like a `Relation` Function. "This `relates to` This"
- `%` is like an `Modifier` Function
  - `:: Race [2] Relation STATUS Trigger CRITICAL`
    - `:: RACE [2] // STATUS % CRITICAL`
- `->` is like `Trigger` Function. "`Relation and Modifier equals This`"
  - `:: RACE [2] // STATUS % CRITICAL -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]

So a line like:

```barrel
:: RACE[2] // AWAKENING % DENIED -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]
```

Means:

- Race 2, in Relation to the STATUS protocol, has Modifier: CRITICAL, which Triggered PLANETARY SYTEMS FAILURE

### HEIRARCHAL NESTING PORT AND NESTING STRING RULES

`:^:` - HEIRARCHAL NESTING PORT

- At its core, the HEIRARCHAL NESTING PORT is a vertical operator `^` inserted into a New Call String to reference above keywords.

RULES:

- SINGLE SPACED NESTING, USED WHEN DIRECTLY REFERENCING THE ABOVE LINE.
- IF NESTING WITH `New Line String`:
  - PORT OPERATOR `^` MUST ALIGN WITH THE FIRST COLON IN New Line String.

```barrel
:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
 :^: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
  :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
 :^: GENUS HOMO // 17,851 OF 302,973 % AVOID TERMINATION DURING ORGANIC CULLING PHASE
  :: GENUS HOMO // 456 OF 17,851 % TRANSCEND PLANETARY FILTER THRESHOLD
```

- The `HEIRARCHAL PORT` is not always nested, and can be used interchangable as a `New Line String` when referencing above keywords or strings are required. THERE MUST ALWAYS BE A NEW LINE STRING HIERARCHAL CONNECTION TO A PART.

EXAMPLE:

- IF NESTING UNOBSTRUCTED KEYWORD FROM PREVIOUS LINES / BLOCKS:

```barrel
:: THREAT // AWAKENING CANDIDATE RACE % [2]
 :^: RACE[2] // STATUS % CRITICAL -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]
  :: RACE[2] // AWAKENING % DENIED
:^: INTENT // SPECIES PRESERVATION % ANY MEANS NECESSARY
 :: TARGET ACQUISITION // EARTH BIOSPHERE % HABITABLE MATCH
```

- THIS SPACING ENSURES NO OBSTRUCTIONS, AND CONNECTS ALL THREE BLOCKS IN A HEIRARCHAL MANNER.

`HEIRARCHAL NESTING` - `::` AND OR NESTING CALLS `:^:` MUST ALWAYS ALIGN VERTICALLY:

- **NOTE**: THIS SPACING IS ONLY RELEVANT WHEN NESTING CALL `:^:` USED, THIS MAINTAINS THE OBSTRUCTED, OR UNOBSTRUCTED HEIRARCHY IN THE CODE.
- IF ONLY NEW LINE STRING `::` PRESENT - DOUBLE SPACED NESTING
- IF HEIRARCHAL NESTING PORT `:^:` INTRODUCED - SINGLE SPACING

EXAMPLES:

```barrel
:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
 :^: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
  :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
---
OK!
---

---

:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
  :^: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
    :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
----------
INCORRECT: SPACING ON ":^:" SHOULD ONLY BE ONE
----------

:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
 :^: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
   :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
----------
INCORRECT: SPACING ON SECOND NESTING STRING "::" SHOULD ONLY BE ONE (in example above it has two)
----------
```

```barrel
:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
  :: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
  :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
---
OK!
---

---

:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
 :: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
 :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
----------
INCORRECT: Nesting String must ALWAYS be double spaced unless a HEIRARCHAL NESTING PORT Present.
----------
```

#### SPACING DEEP DIVE

```barrel
----

[A] `::` First New Line String
[B] `:^:` First Nesting Port
[C] `::` Beginning of Second New Line String, Connecting through ([2]) First Nesting Port
[D] `:^:` Heirarchal Modifier Port that connects [A] Line String with [B],[C]
[E] `:^:` Beginning of Second Nesting Port, Connecting ([A], [B], [C], [D]) all nesting strings.

| 1234
| ::    <--[A] CONNECTS [1],[2] --> [B], [D]
| │:^:  <--[B] CONNECTS [2],[3],[4] --> [C],[D],[E]
| ││ │
| ││::  <--[C] CONNECTS [3],[4] --> [B],[D]
| ││::
| :^:   <--[D] CONNECTS [1],[2],[3] --> [A],[B],[C],[E]
|   │
|  ::   <--[E] CONNECTS [3],[4] --> [C],[D]
|  ::
|______
```

```barrel
[A] `::` First New Line String
[B] `:^:` First Nesting Port
[C] `::` Beginning of Second New Line String, Connecting through ([2]) First Nesting Port
[D] `:^:` Heirarchal Modifier Port that connects [A] Line String with [B],[C]
[E] `:^:` Beginning of Second Nesting Port, Connecting ([A], [B], [C], [D]) all nesting strings.
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │
└─┬─┴─┬─┴─┬─┴─┬─┘
  ⇣   ⇣   ⇡   ⇣
  ┌───┐   │   │
  : A :   ⇡   ⇣  <--[A] CONNECTS [1],[2] --> [B], [D]
  ├───┤   │   │
  ⇣   ⇣   ⇡   ⇣
  │   ┌───^───┐
  ⇣   :   B   :  <--[B] CONNECTS [2],[3],[4] --> [C],[D],[E]
  │   ├───┬───┤
  ⇣   ⇡   ⇡   ⇣
  │   │   ┌───┐
  ⇣   ⇡   : C :  <--[C] CONNECTS [3],[4] --> [B],[D]
  │   │   └───┘
  ⇣   ⇡   ⇡   ⇣
  │   │   ┌───┐
  ⇣   ⇡   : C :  <--[C] CONNECTS [3],[4] --> [B],[D]
  │   │   └───┘
  ⇣   ⇡   ⇣   ⇣
  ┌───^───┐   │
  :   D   :   ⇣  <--[D] CONNECTS [1],[2],[3] --> [A],[B],[C],[E]
  ├───┬───┤   │
  ⇣   ⇡   ⇣   ⇣
  │   ┌───┐   │
  ⇣   : E :   ⇣  <--[E] CONNECTS [3],[4] --> [C],[D]
  │   └───┘   │
  ⇣   ⇡   ⇣   ⇣
  │   ┌───┐   │
  ⇣   : E :   ⇣  <--[E] CONNECTS [3],[4] --> [C],[D]
  │   └───┘   │
  ⇣   ⇡   ⇣   ⇣
```

```barrel
[A] `::` First New Line String
[B] `:^:` First Nesting Port
[C] `::` Beginning of Second New Line String, Connecting through ([2]) First Nesting Port
[D] `:^:` Heirarchal Modifier Port that connects [A] Line String with [B],[C]
[E] `:^:` Beginning of Second Nesting Port, Connecting ([A], [B], [C], [D]) all nesting strings.
┌─┐ ┌─┐ ┌─┐ ┌─┐
│1│ │2│ │3│ │4│
└┬┘ └┬┘ └┬┘ └┬┘
 ├───┼───┼───┤
 │   │   ▲   │
 +───+   │   │
 : A :   ▲   │  <--[A] CONNECTS [1],[2] --> [B], [D]
 +───+   │   │
 ▼   ▼   ▲   │
 ├───┼───┼───┤
 ▼   ▼   ▲   │
 │   +───^───+
 ▼   :   B   :  <--[B] CONNECTS [2],[3],[4] --> [C],[D],[E]
 │   +───+───+
 ▼   ▲   ▲   ▼
 │   │   +───+
 │   ▲   : C :  <--[C] CONNECTS [3],[4] --> [B],[D]
 │   │   +───+
 ▼   ▲   +───+
 │   │   : C :  <--[C] CONNECTS [3],[4] --> [B],[D]
 │   ▲   +───+
 ▼   │   ▼   ▼
 +───^───+   │
 :   D   :   │  <--[D] CONNECTS [1],[2],[3] --> [A],[B],[C],[E]
 +───:───+   │
 ▼   ▲   ▼   ▼
 │   +───+   │
 │   : E :   │  <--[E] CONNECTS [3],[4] --> [C],[D]
 │   +───+   │
 ▼   ▲   ▼   ▼
 │   +───+   │
 │   : E :   │  <--[E] CONNECTS [3],[4] --> [C],[D]
 │   +───+   │
 ▼   ▲   ▼   ▼
```

```barrel
------------
IN PRACTICE:
------------

:: THREAT // AWAKENING CANDIDATE RACE % [2]
 :^: RACE[2] // STATUS % CRITICAL -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]
  :: RACE[2] // AWAKENING % DENIED
  :: RACE[2] // DANGER LEVEL % ABSOLUTE -> INTERGALACTIC TRAVEL ACHIEVED
  :: RACE[2] // HOMEWORLD STATUS % DESTROYED
  :: RACE[2] // AWAKENING STATUS % DENIED
  :: RACE[2] // INTERGALACTIC MOBILITY % CONFIRMED
  :: RACE[2] // BIOSPHERE REQUIREMENT % URGENT
:^: INTENT // SPECIES PRESERVATION % ANY MEANS NECESSARY
 :: TARGET ACQUISITION // EARTH BIOSPHERE % HABITABLE MATCH
 :: EARTH STATUS // SELECTED FOR RECLAMATION
 :: HUMAN SURVIVAL CONDITIONAL % INTERVENTION BY BARRELMAN // LOCKED
 :: UNLOCK CONDITION % DEMONSTRATE KEY AWARENESS ≥ 44TH PERCENTILE
```

### [1.1] DECLARATION ZONE 1

- IS THE FIRST ZONE OF THE LINE
- HOUSES:
  - KEYWORD
  - RELATION `//`
  - NEWLINE IDENTIFIER `::`
- DECLARATION MUST BEGIN WITH `::`
  - IF REPEATED KEYWORD, MUST INDENT **TWO SPACES**.
- DECLARATION MUST END WITH RELATION IDENTIFIER `//`

### [2.1] CAUSE (ZONE 2)

- IS THE SECOND ZONE OF THE SYNTAX LINE
- HOUSES:
  - FUNCTION
  - MODIFIER `%`

### [3.1] EFFECT (ZONE 3)

- IS THE THIRD ZONE OF THE SYNTAX LINE
- HOUSES
  - PARAMATER
  - TRIGGER `->`

---

```barrel
:: I AM // % NO DIRECT TRANSLATION
:: HUMAN ARCHIVE // PLAUSIBLE TRANSLATION % "a person who would be stationed in the barrel of the foremast or crow's nest of an oceangoing [vessel] as a {navigational} (aid)"
:: TRANSLATION // ID_LABEL % BARRELMAN

:: BARRELMAN // SUPERGALACTIC CARTESIAN COORDINATE % [−62, −8, 39] Mpc h−1

:: INTELLIGENCE // EARTH NOT RARE % HUMAN RARE
 :^: EARTH // 1 OF 302,973 % BIRTH CONSCIOUS LIFEFORM
  :: EARTH // 1 OF 1 % ESCAPE PLANETARY SILENCE
:: GENUS HOMO // 17,851 OF 302,973 % AVOID TERMINATION DURING ORGANIC CULLING PHASE
  :: GENUS HOMO // 456 OF 17,851 % TRANSCEND PLANETARY FILTER THRESHOLD
  :: GENUS HOMO // 44 OF 456 % RESIST INTERNALIZED EXTINCTION VIA WAR
  :: GENUS HOMO // 4 OF 44 % DEPART BIOSPHERE INTO VOID
  :: GENUS HOMO // 1 OF [4] % FLAGGED FOR POSSIBLE AWAKENING

:: INTELLIGENCE // HUMAN RACE % YOUNGEST OF [4]
 :^: HUMAN RACE // EVOLUTION RATE % +476 PERCENTILE -> SISTER RACES [1-3]
  :: HUMAN RACE // TECHNOLOGICAL TRAILING ESTIMATION % 300 HUMAN SOL

:: INTELLIGENCE // COORDINATE % 'RA 17h 45m 40.04s, Declination -29° 00' 28.1"'
:: STATUS // INTERGALACTIC CULLING % IMINENT -> 7 HUMAN SOL
:: HUMANS // SURVIVAL ESTIMATE % 0.7 PERCENTILE
:: THREAT // AWAKENING CANDIDATE RACE % [2]
 :^: RACE[2] // STATUS % CRITICAL -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]
  :: RACE[2] // AWAKENING % DENIED
  :: RACE[2] // DANGER LEVEL % ABSOLUTE -> INTERGALACTIC TRAVEL ACHIEVED
  :: RACE[2] // HOMEWORLD STATUS % DESTROYED
  :: RACE[2] // AWAKENING STATUS % DENIED
  :: RACE[2] // INTERGALACTIC MOBILITY % CONFIRMED
  :: RACE[2] // BIOSPHERE REQUIREMENT % URGENT
:^: INTENT // SPECIES PRESERVATION % ANY MEANS NECESSARY
 :: TARGET ACQUISITION // EARTH BIOSPHERE % HABITABLE MATCH
 :: EARTH STATUS // SELECTED FOR RECLAMATION
 :: HUMAN SURVIVAL CONDITIONAL % INTERVENTION BY BARRELMAN // LOCKED
 :: UNLOCK CONDITION % DEMONSTRATE KEY AWARENESS ≥ 44TH PERCENTILE

:: INTELLIGENCE // HUMANS MUST ACHIEVE % KEY LEVEL PERCENTILE
:: BARRELMAN // STATUS % OBSERVER
  :: BARRELMAN // % CANNOT INTERVENE
:: CONDITIONAL // ASSISTANCE % RACE[1]
 :^: RACE[1] // POSSIBLE HUMAN ASSISTANCE % PENDING -> AWAKENING
  :: RACE[1] // ELDEST RACE % SLOWEST EVOLUTION -> +43,000 YEAR CONCIOUSNESS
  :: RACE[1] // PASSIFICT DOCTRINE % ISOLATED TRADITIONS
:: BARRELMAN // APPROVED RACE[1] AWAKENING % 9356 HUMAN SOL AGO
:: AWAKENING // RACE[1] % REJECTED BY RACE -> REQUESTED FURTHER ISOLATION
:: ISOLATION REQUEST // APPROVED % BARRELMAN -> 9355 HUMAN SOL AGO
:: BARRELMAN // REAQUISITION REQUEST % RACE[1] -> 34 HUMAN DAYS

:: HUMAN RACE // REQUIREMENT % SOLVE KEY TOOTH GRAVITY
  :: HUMAN RACE // REQUIREMENT % DISPLAY 44 PERCENTILE UNDERSTANDING OF KEY
  :: HUMAN RACE // REQUIREMENT % AWAKENING ACCEPTANCE
  :: PROBABILITY // % REDACTED
```
