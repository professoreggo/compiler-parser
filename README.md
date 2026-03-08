# 🔧 Expression Compiler & Evaluator

A Python-based mini compiler with a graphical interface that processes mathematical expressions through all major compiler phases — from lexical analysis to assembly code generation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Usage](#installation--usage)
- [Pipeline](#pipeline)
- [Example Input](#example-input)
- [Limitations](#limitations)

---

## Overview

This project implements a complete compiler pipeline for simple mathematical assignment expressions (e.g., `z = x + 2 * y`). It supports both **integer** and **float** modes, and walks the input through lexical analysis, syntax parsing, semantic analysis, intermediate code generation, optimization, and finally assembly code generation — displaying results at each stage via Tkinter GUI windows.

---

## Features

- ✅ Lexical analysis with token identification and variable mapping
- ✅ Syntax analysis using the Shunting-Yard algorithm with parse tree visualization
- ✅ Semantic analysis with optional `int-to-float` type conversion tree
- ✅ Intermediate Code Generation (ICG) with temporary variable allocation
- ✅ Code optimization (redundant temporary variable elimination)
- ✅ Assembly-style code generation (`LD`, `ADD`, `SUB`, `MUL`, `DIV`, `STR`, `MOV`)
- ✅ GUI-driven with Tkinter — no command-line output required
- ✅ Supports implicit multiplication (e.g., `2 x` → `2 * x`)
- ✅ Supports exponentiation via `^` or `**`
- ✅ Supports the constant `pi`

---

## Project Structure

```
.
├── main.py                # Entry point — GUI setup and pipeline orchestration
├── lexical_analyzer.py    # Tokenization and variable identification
├── syntax_analyzer.py     # Infix-to-postfix conversion and parse tree construction
├── semantic_analyzer.py   # Type checking and tree annotation for float mode
├── ICG.py                 # Intermediate Code Generator
├── Optimizer.py           # Intermediate code optimizer
├── code_generator.py      # Assembly code generator
└── reserved_words.py      # Reserved words and special symbols definitions
```

---

## Requirements

- Python 3.x
- `tkinter` (included with most Python distributions)

No third-party packages are required.

---

## Installation & Usage

1. **Clone or download** this repository.

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **In the GUI:**
   - Enter a mathematical assignment expression in the input field (e.g., `z = x + 2 * y`)
   - Select the data type: **Integer** or **Float**
   - Click **Process**

4. Results from each compiler phase will appear in the output panel and as separate Tkinter windows.

---

## Pipeline

The expression is processed through the following stages in order:

```
User Input
    │
    ▼
1. Input Validation       — checks for '=' and valid identifier on the left-hand side
    │
    ▼
2. Math Preprocessing     — handles implicit multiplication, pi, and ^ notation
    │
    ▼
3. Lexical Analysis       — tokenizes input, maps identifiers to symbolic IDs
    │
    ▼
4. Syntax Analysis        — converts to postfix, builds a parse tree, visualizes it
    │
    ▼
5. Semantic Analysis      — type-checks and annotates the tree (int-to-float if needed)
    │
    ▼
6. ICG                    — generates three-address intermediate code with temp vars
    │
    ▼
7. Optimization           — eliminates redundant temporaries
    │
    ▼
8. Assembly Code Gen      — produces register-based assembly instructions
```

---

## Example Input

**Input:** `z = x + 2 * y` (Integer mode)

| Stage | Output |
|---|---|
| Lexical Analysis | `{'x': 'id1', 'y': 'id2', 'z': 'id3'}` |
| Syntax (Postfix) | `z id1 2 id2 * + =` |
| ICG | `temp1 = id1 + 2`, `temp2 = temp1 * id2`, `z = temp2` |
| Optimized | `temp1 = id1 + 2`, `z = temp1 * id2` |
| Assembly | `LD R2, id1` → `ADD R2, 2` → `MUL R2, id2` → `STR z, R2` |

---

## Limitations

- Only supports **single assignment statements** (one `=` per expression)
- Left-hand side must be a valid identifier (cannot be a number or reserved word)
- A variable cannot appear on both sides of the assignment (e.g., `x = x + 1` is rejected)
- No support for conditionals, loops, or multi-statement programs
- Assembly generation uses a simplified single-register (`R2`) model
