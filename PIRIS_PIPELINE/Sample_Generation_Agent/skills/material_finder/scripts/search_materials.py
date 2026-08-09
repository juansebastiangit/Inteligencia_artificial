import os
import json
import argparse
from typing import Optional, List
from mp_api.client import MPRester

def search_materials_project(
    api_key: str,
    formula: Optional[str] = None,
    chemsys: Optional[str] = None,
    material_ids: Optional[List[str]] = None,
    elements: Optional[List[str]] = None,
    crystal_system: Optional[str] = None,
    band_gap_min: Optional[float] = None
) -> str:
    """
    Searches the Materials Project for crystallographic data.
    """
    search_args = {
        "formula": formula,
        "chemsys": chemsys,
        "material_ids": material_ids,
        "elements": elements,
        "crystal_system": crystal_system,
        "band_gap_min": band_gap_min
    }
    
    # Filter out None values
    search_params = {k: v for k, v in search_args.items() if v is not None}

    if crystal_system:
        # Normalize crystal_system (e.g., "cubic" -> "Cubic")
        search_params['crystal_system'] = crystal_system.capitalize()

    if not search_params:
        return json.dumps({"error": "No search criteria provided."})

    try:
        # Prioritize formula/chemsys over elements
        if ("formula" in search_params or "chemsys" in search_params) and "elements" in search_params:
            del search_params["elements"]

        with MPRester(api_key=api_key) as mpr:
            results = mpr.materials.summary.search(
                **search_params,
                fields=["material_id", "formula_pretty", "symmetry.symbol", "band_gap"]
            )

            if not results:
                return json.dumps({"total_count": 0, "results": []})

            output_data = [
                {
                    "material_id": str(mat.material_id),
                    "formula_pretty": mat.formula_pretty,
                    "space_group_symbol": mat.symmetry.symbol,
                    "band_gap": f"{mat.band_gap:.2f} eV" if mat.band_gap is not None else "N/A"
                }
                for mat in results
            ]

            return json.dumps({
                "total_count": len(output_data),
                "results": output_data
            }, indent=2)

    except Exception as e:
        import traceback
        return json.dumps({
            "error": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Materials Project database.")
    parser.add_argument("--api-key", help="Materials Project API Key (can also use MP_API_KEY env var)")
    parser.add_argument("--formula", help="Chemical formula (e.g., SiO2)")
    parser.add_argument("--chemsys", help="Chemical system (e.g., Si-O)")
    parser.add_argument("--material-ids", nargs="+", help="Material IDs (e.g., mp-149 mp-19017)")
    parser.add_argument("--elements", nargs="+", help="Required elements (e.g., Li P)")
    parser.add_argument("--crystal-system", help="Crystal system (e.g., cubic)")
    parser.add_argument("--band-gap-min", type=float, help="Minimum band gap in eV")

    args = parser.parse_args()

    # Hardcode your API key here for testing if environment variables fail
    HARDCODED_API_KEY = "8PYa1oiRYmim6vVYine0YAIYMAU9g1pm" 

    api_key = args.api_key or HARDCODED_API_KEY or os.environ.get("MP_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Missing API Key. Provide via --api-key or MP_API_KEY environment variable."}))
        exit(1)

    result = search_materials_project(
        api_key=api_key,
        formula=args.formula,
        chemsys=args.chemsys,
        material_ids=args.material_ids,
        elements=args.elements,
        crystal_system=args.crystal_system,
        band_gap_min=args.band_gap_min
    )
    print(result)
