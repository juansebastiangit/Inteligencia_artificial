import Build_Sample_copy as bs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # This import registers the 3D projection
import numpy as np

lattice_parameters = {
        "a": "6.027318(29)",
        "b": "6.027318(29)",
        "c": "4.82861(13)",
        "alpha": "90.0",
        "beta": "90.0",
        "gamma": "120.0"
    }

atomic_sites=[
        {
            "element": "CU1",
            "x": ".0",
            "y": ".0",
            "z": ".0",
            "occupancy": "1.0"
        },
        {
            "element": "C2",
            "x": ".0",
            "y": ".0",
            "z": ".4016(14)",
            "occupancy": ".5"
        },
        {
            "element": "N3",
            "x": ".0",
            "y": ".0",
            "z": ".4016(14)",
            "occupancy": ".5"
        }
    ]
symmetry_operations=[
        "+x,+y,+z",
        "-y,x-y,+z",
        "y-x,-x,+z",
        "y-x,+y,+z",
        "-y,-x,+z",
        "+x,x-y,+z",
        "-x,-y,-z",
        "+y,y-x,-z",
        "x-y,+x,-z",
        "x-y,-y,-z",
        "+y,+x,-z",
        "-x,y-x,-z",
        "+x+1/3,+y+2/3,+z+2/3",
        "-y+1/3,x-y+2/3,+z+2/3",
        "y-x+1/3,-x+2/3,+z+2/3",
        "y-x+1/3,+y+2/3,+z+2/3",
        "-y+1/3,-x+2/3,+z+2/3",
        "+x+1/3,x-y+2/3,+z+2/3",
        "-x+2/3,-y+1/3,-z+1/3",
        "+y+2/3,y-x+1/3,-z+1/3",
        "x-y+2/3,+x+1/3,-z+1/3",
        "x-y+2/3,-y+1/3,-z+1/3",
        "+y+2/3,+x+1/3,-z+1/3",
        "-x+2/3,y-x+1/3,-z+1/3",
        "+x+2/3,+y+1/3,+z+1/3",
        "-y+2/3,x-y+1/3,+z+1/3",
        "y-x+2/3,-x+1/3,+z+1/3",
        "y-x+2/3,+y+1/3,+z+1/3",
        "-y+2/3,-x+1/3,+z+1/3",
        "+x+2/3,x-y+1/3,+z+1/3",
        "-x+1/3,-y+2/3,-z+2/3",
        "+y+1/3,y-x+2/3,-z+2/3",
        "x-y+1/3,+x+2/3,-z+2/3",
        "x-y+1/3,-y+2/3,-z+2/3",
        "+y+1/3,+x+2/3,-z+2/3",
        "-x+1/3,y-x+2/3,-z+2/3"
    ]

supercell_cartesian=bs.build_sample(lattice_parameters, atomic_sites, symmetry_operations, 3)

