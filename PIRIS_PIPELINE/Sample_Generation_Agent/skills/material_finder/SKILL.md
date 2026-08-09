---
name: material_finder
description: Searches the Materials Project database for crystallographic data based on formula, elements, or properties.
---

# Material Finder Skill

This skill allows the agent to query the Materials Project API to find materials matching specific criteria.

## Prerequisite
- `mp-api` python package installed: `pip install mp-api`
- `MP_API_KEY` set in environment variables.

## How to use
Run the `search_materials.py` script with the desired filter flags.

### Logic
1. Identify the user's search criteria (formula, elements, crystal system, etc.).
2. Execute the script using the virtual environment: `.venv\Scripts\python.exe .agent/skills/material_finder/scripts/search_materials.py [FLAGS]`
3. Parse the JSON output.
4. Summarize the results for the user. Do not show raw JSON.

### Examples
- **By Formula**: `.venv\Scripts\python.exe .agent/skills/material_finder/scripts/search_materials.py --formula SiO2`
- **By Elements**: `.venv\Scripts\python.exe .agent/skills/material_finder/scripts/search_materials.py --elements Li P`
- **With Band Gap**: `.venv\Scripts\python.exe .agent/skills/material_finder/scripts/search_materials.py --formula GaN --band-gap-min 2.0`
- **By Crystal System**: `.venv\Scripts\python.exe .agent/skills/material_finder/scripts/search_materials.py --crystal-system cubic --elements Fe O`

## Scripts
- [search_materials.py](file:///c:/Users/Asus-PC/Desktop/.agent/skills/material_finder/scripts/search_materials.py)
