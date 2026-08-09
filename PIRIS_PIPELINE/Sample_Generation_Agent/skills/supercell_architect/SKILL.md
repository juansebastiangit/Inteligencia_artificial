# Supercell Architect Skill

This skill generates ready-to-paste Python code for the PIRIS (Physical Regularized Information) adsorption simulation notebook. 

## Purpose
Instead of generating static data files, this skill produces a standalone Python function that handles symmetry expansion and supercell replication. This allows the user to dynamically adjust the sample size (nx, ny, nz) directly within their notebook environment.

## Definition
- **Name**: `supercell_architect`
- **Description**: Generates a PIRIS-compatible Python function for building supercells.

## Arguments
- `material_json` (string): The path to the JSON file produced by the `material_crystallographer` skill.

## Execution Logic
The skill uses the Python script `build_supercell.py` within the `.venv` environment to generate the code block.

```powershell
.venv\Scripts\python.exe .agent/skills/supercell_architect/scripts/build_supercell.py --input <material_json>
```

## Example Usage
1. Search: `material_finder --formula ZnO` -> mp-2133
2. Details: `material_crystallographer --id mp-2133` -> `zno_details.json`
3. Generate Code: `supercell_architect --material_json zno_details.json`
4. Result: A Python function `build_ZnO_sample(nx=1, ny=1, nz=1)` that returns the 6-tuple required by PIRIS.
