---
name: material_crystallographer
description: Fetches full structural details, atomic sites, and symmetry operations for a specific Material ID.
---

# Material Crystallographer Skill

This skill allows the agent to retrieve the complete crystallographic data for a specific material once its ID (e.g., `mp-149`) is known. This data is essential for structural analysis and building larger crystal models (supercells).

### Logic
1. Identify the `material_id` from the search results or user input.
2. Execute the script using the virtual environment: `.venv\Scripts\python.exe .agent/skills/material_crystallographer/scripts/get_details.py --id [ID]`
3. Parse the JSON output.
4. Summarize the structural parameters (lattice, symmetry) for the user.
5. Retain the detailed data if the user intends to build a supercell next.

### Examples
- **Get Details for Silicon**: `.venv\Scripts\python.exe .agent/skills/material_crystallographer/scripts/get_details.py --id mp-149`
- **Get Details for ZnO**: `.venv\Scripts\python.exe .agent/skills/material_crystallographer/scripts/get_details.py --id mp-2133`

## Scripts
- [get_details.py](file:///c:/Users/Asus-PC/Desktop/.agent/skills/material_crystallographer/scripts/get_details.py)
