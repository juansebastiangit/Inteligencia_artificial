import numpy as np
import re

def build_sample(lattice_parameters,atomic_sites,symmetry_ops,sample_size):
    #Takes in the lattice parameters, atomic sites, symmetry operations, and sample size and returns a dictionary
    # with the positions of th atoms in a sample of the crystal structure and a cif file to validate the structure

    #Read in the lattice parameters and atomic sites
    a,b,c,alpha,beta,gamma = [float(lattice_parameters[key].split("(")[0]) for key in lattice_parameters.keys()]
    sites ={atomic_sites[i]["element"]:(float(atomic_sites[i]["x"].split("(")[0]),float(atomic_sites[i]["y"].split("(")[0]),float(atomic_sites[i]["z"].split("(")[0]),float(atomic_sites[i]["occupancy"].split("(")[0])) for i in range(len(atomic_sites))}

    #Defining lattice vectors
    a_vec = np.array([a, 0.0, 0.0])
    b_vec = np.array([b*np.cos(gamma), b*np.sin(gamma), 0.0])
    aux = (np.cos(alpha) - np.cos(beta)*np.cos(gamma)) / np.sin(gamma)
    c_vec = np.array([c*np.cos(beta), c*aux, c*np.sqrt(1 - np.cos(beta)**2 - aux**2)])

    def parse_symmetry_operation(sym_op):
        """Converts a symmetry operation string (e.g. "-y,x-y,+z" or "x+1/3,y+2/3,z+2/3")
        into a 3x3 transformation matrix and a 3x1 translation vector.
        """
        variables = ['x', 'y', 'z']
        # Regex to capture an optional sign, an optional number (integer, fraction, or decimal),
        # and an optional variable (x, y, or z).
        token_pattern = re.compile(r'([+-]?)(\d+(?:/\d+)?|\d*\.\d+)?([xyz])?')
        
        #split the symmetry operation into parts
        parts = sym_op.split(',')
        #Initialize the transformation matrix and translation vector
        M = np.zeros((3, 3))
        t = np.zeros(3)
        
        for i, part in enumerate(parts):
            # Remove spaces from the part
            part = part.replace(" ", "")
            # Find all the tokens in the part
            tokens = token_pattern.findall(part)
            for sign, number, var in tokens:
                # If the number is empty, set it to 1
                if sign == '' and number == '' and var == '':
                    continue
                # Evaluate the number to a float
                coeff = float(eval(number)) if number else 1.0
                # If the sign is negative, make the coefficient negative
                if sign == '-':
                    coeff = -coeff
                # Find the index of the variable (x=0, y=1, z=2)
                if var:
                    j = variables.index(var)
                    M[i, j] += coeff
                # If there is no variable, it's a translation term
                else:
                    t[i] += coeff
        # Return the transformation matrix and translation vector
        return M, t
    
    # Prepare a dictionary to hold transformed positions.
    # For each atom, the value will be a list of tuples: (x, y, z, occupancy)
    transformed_atoms = {atom: [] for atom in sites.keys()}

    # Loop over each symmetry operation.
    for op in symmetry_ops:
        M, t = parse_symmetry_operation(op)
        # Apply the current symmetry operation to every atom.
        for atom, (x, y, z, occ) in sites.items():
            original = np.array([x, y, z])
            transformed = M @ original + t
            # Store the transformed position along with the original occupancy.
            transformed_atoms[atom].append( (transformed[0], transformed[1], transformed[2], occ) )

    def remove_duplicates(positions, tol=1e-5):
        """
        Remove duplicate positions from a list of tuples (x, y, z, occupancy).
        Two positions are considered duplicates if their x, y, and z coordinates
        are within a tolerance (tol).
        """
        unique_positions = []
        for pos in positions:
            duplicate = False
            # Compare only the first three coordinates (x, y, z)
            for up in unique_positions:
                if np.allclose(pos[:3], up[:3], atol=tol) and np.isclose(pos[3], up[3], atol=tol):
                    duplicate = True
                    break
            if not duplicate:
                unique_positions.append(pos)
        return unique_positions
    
    for atom in transformed_atoms:
        transformed_atoms[atom] = remove_duplicates(transformed_atoms[atom])

    def fractional_to_cartesian(frac_coord, a, b, c):
        """
        Convert a single fractional coordinate (as a NumPy array [x, y, z])
        into Cartesian coordinates using lattice vectors a, b, c.
        """
        # The conversion: r_cart = x * a + y * b + z * c
        return frac_coord[0] * a + frac_coord[1] * b + frac_coord[2] * c

    # Dictionary to hold Cartesian coordinates
    cartesian_atoms = {atom: [] for atom in transformed_atoms.keys()}

    for atom, positions in transformed_atoms.items():
        for pos in positions:
            frac = np.array(pos[:3])
            occ = pos[3]
            cart = fractional_to_cartesian(frac, a_vec, b_vec, c_vec)
            # Save the Cartesian coordinate with occupancy.
            cartesian_atoms[atom].append( (cart[0], cart[1], cart[2], occ) )
    if sample_size == 1:
        return cartesian_atoms
    
    else:
        supercell_cartesian = {atom: [] for atom in cartesian_atoms.keys()}
        for atom, positions in cartesian_atoms.items():
            for pos in positions:
                # Convert the position to a NumPy array (for vector arithmetic).
                pos_cart = np.array(pos[:3])
                occ = pos[3]
                # Loop over replication indices along each axis.
                for i in range(sample_size):
                    for j in range(sample_size):
                        for k in range(sample_size):
                            # Compute the offset in Cartesian space.
                            offset = i * a_vec + j * b_vec + k * c_vec
                            # New Cartesian coordinate:
                            new_cart = pos_cart + offset
                            # Store the new position along with its occupancy.
                            supercell_cartesian[atom].append((new_cart[0], new_cart[1], new_cart[2], occ))

        def write_supercell_cif(filename, supercell_cartesian_atoms):

            # Compute supercell lattice vectors by multiplying the original vectors.
            a_super = sample_size * a_vec
            b_super = sample_size * b_vec
            c_super = sample_size * c_vec
            lattice_vectors = (a_super, b_super, c_super)
            
            # Compute cell lengths.
            a_len = np.linalg.norm(a_super)
            b_len = np.linalg.norm(b_super)
            c_len = np.linalg.norm(c_super)
            
            
            # Build the lattice matrix L (with columns a_super, b_super, c_super) and its inverse.
            L = np.column_stack((a_super, b_super, c_super))
            L_inv = np.linalg.inv(L)
            
            # Prepare CIF content.
            cif_lines = []
            cif_lines.append("data_supercell_structure")
            cif_lines.append(f"_cell_length_a    {a_len:.4f}")
            cif_lines.append(f"_cell_length_b    {b_len:.4f}")
            cif_lines.append(f"_cell_length_c    {c_len:.4f}")
            cif_lines.append(f"_cell_angle_alpha {alpha:.2f}")
            cif_lines.append(f"_cell_angle_beta  {beta:.2f}")
            cif_lines.append(f"_cell_angle_gamma {gamma:.2f}")
            cif_lines.append("loop_")
            cif_lines.append("  _atom_site_label")
            cif_lines.append("  _atom_site_fract_x")
            cif_lines.append("  _atom_site_fract_y")
            cif_lines.append("  _atom_site_fract_z")
            cif_lines.append("  _atom_site_occupancy")
            
            # Convert each Cartesian atom position to fractional coordinates in the supercell.
            for atom, positions in supercell_cartesian_atoms.items():
                for pos in positions:
                    cart = np.array(pos[:3])
                    occ = pos[3]
                    frac = L_inv @ cart
                    # Normalize the fractional coordinates to be in [0,1)
                    frac = frac % 1.0
                    cif_lines.append(f"  {atom}  {frac[0]:.5f}  {frac[1]:.5f}  {frac[2]:.5f}  {occ:.3f}")
            
            # Write the CIF content to file.
            with open(filename, 'w') as f:
                for line in cif_lines:
                    f.write(line + "\n")

        write_supercell_cif("supercell_structure.cif", supercell_cartesian)
        print("CIF file 'supercell_structure.cif' has been created.")

        return supercell_cartesian
    