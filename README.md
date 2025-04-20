⸻

✅ Zone [4.1] Outcome Inference
• Outcomes are automatically inferred based on modifier and trigger combinations.
• Rendered in the syntax tree as:

└── Outcome: Outcome inferred from % MODIFIER -> TRIGGER

⸻

Graphviz Export with Styling
• Nodes are colored based on function:
• lightblue for :^: ports
• lightgrey for standard declarations
• Labels show % Modifier, -> Trigger, and [Outcome]
• Run export:

```bash
python barrelman_lexer.py example.bman --dot
dot -Tpng barrelman_tree.dot -o tree.png
```

⸻

CLI Tool for .bman Files
• Usage:

```bash
python barrelman_lexer.py your_file.bman
python barrelman_lexer.py your_file.bman --dot
```

⸻

### HIERARCHICAL NESTING PORT STRUCTURE

1. First New Line String
2. First Nesting Port
3. ^ Hierarchical Modifier Port that connects the above String
4. Beginning of Second New Line String, Connecting through ([2]) First Nesting Port
5. Beginning of Second Nesting Port, Connecting ([1], [2], [3], [4]) all nesting strings.

```
---------------------------------------------------
STRUCTURE WITH BAR CONNECTING VISUAL REPRESENTATION
---------------------------------------------------

1234
::
│:^:
││ │
││::
││::
:^:
││
│::
│::

`::` = NESTING STRING
`:^:` = NESTING PORT
`│` = VISUAL BAR REPRESENTATION FOR CONNECTION POINTS
```

```
-------------
ACTUAL SYNTAX
-------------
1234
::
 :^:
  ::
  ::
:^:
 ::
 ::

-----------------------------
# ACTUAL SYNTAX FUNCTIONALITY
-----------------------------
:: THREAT // AWAKENING CANDIDATE RACE % [2]
 :^: RACE[2] // STATUS % CRITICAL -> PLANETARY SYSTEM FAILURE [SELF-INITIATED]
  :: RACE[2] // AWAKENING % DENIED
  :: RACE[2] // DANGER LEVEL % ABSOLUTE -> INTERGALACTIC TRAVEL ACHIEVED
:^: INTENT // SPECIES PRESERVATION % ANY MEANS NECESSARY
 :: TARGET ACQUISITION // EARTH BIOSPHERE % HABITABLE MATCH
 :: EARTH STATUS // SELECTED FOR RECLAMATION
```
