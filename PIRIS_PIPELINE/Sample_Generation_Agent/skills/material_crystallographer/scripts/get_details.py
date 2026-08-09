import os
import json
import argparse
from mp_api.client import MPRester

def get_material_details(api_key: str, material_id: str) -> str:
    """
    Retrieves full, detailed crystallographic data for a specific material_id.
    """
    try:
        with MPRester(api_key=api_key) as mpr:
            # Fetch the material document. We use summary search for the specific ID.
            # We explicitly request the fields we need.
            results = mpr.summary.search(
                material_ids=[material_id],
                fields=["material_id", "formula_pretty", "structure", "symmetry", "band_gap"]
            )
            
            if not results:
                return json.dumps({"error": f"No material found with ID {material_id}"})
            
            material_doc = results[0]
            structure = material_doc.structure
            
            # Extract lattice parameters
            lat = structure.lattice
            unit_cell_params = {
                "a": lat.a, "b": lat.b, "c": lat.c,
                "alpha": lat.alpha, "beta": lat.beta, "gamma": lat.gamma
            }
            unit_cell_str = f"a={lat.a:.3f}, b={lat.b:.3f}, c={lat.c:.3f}, alpha={lat.alpha:.2f}, beta={lat.beta:.2f}, gamma={lat.gamma:.2f}"

            # Extract atomic sites
            # Note: specie is often a specialized object, cast to string for JSON
            atomic_sites = [
                {"element": str(site.specie), "x": site.a, "y": site.b, "z": site.c, "occupancy": 1.0} 
                for site in structure.sites
            ]

            # Extract symmetry info and operations
            # Symmetry operations are generated using SpacegroupAnalyzer for completeness
            from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
            sga = SpacegroupAnalyzer(structure)
            
            sym_ops = []
            # Get the symmetry operations as standard "x,y,z" strings
            for op in sga.get_space_group_operations():
                sym_ops.append(op.as_xyz_str())

            detailed_data = {
                "material_id": str(material_id),
                "formula": material_doc.formula_pretty,
                "unit_cell": unit_cell_str,
                "unit_cell_params": unit_cell_params,
                "atomic_sites": atomic_sites,
                "symmetry": {
                    "symbol": material_doc.symmetry.symbol,
                    "number": material_doc.symmetry.number
                },
                "band_gap": f"{material_doc.band_gap:.2f} eV" if material_doc.band_gap is not None else "N/A",
                "symmetry_operations": sym_ops
            }
            
            return json.dumps(detailed_data, indent=2)

    except Exception as e:
        import traceback
        return json.dumps({
            "error": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get material details from Materials Project.")
    parser.add_argument("--api-key", help="Materials Project API Key")
    parser.add_argument("--id", required=True, help="Material ID (e.g., mp-149)")

    args = parser.parse_args()

    HARDCODED_API_KEY = "8PYa1oiRYmim6vVYine0YAIYMAU9g1pm"
    api_key = args.api_key or os.environ.get("MP_API_KEY") or HARDCODED_API_KEY

    if not api_key:
        print(json.dumps({"error": "Missing API Key."}))
        exit(1)

    print(get_material_details(api_key, args.id))
