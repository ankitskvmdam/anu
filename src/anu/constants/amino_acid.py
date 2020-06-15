"""Enum for amino acid."""

from enum import Enum
from typing import Dict, TypedDict


class AcidityBasicity(Enum):
    """Enum for acidity and basicity."""

    U = 3  # Neutral
    A = 1  # Acid
    B = 2  # Base


class Charge(Enum):
    """Enum for charge."""

    U = 3  # Neutral
    P = 1  # Positive
    N = 2  # Negative


class Hydropathy(Enum):
    """Enum for hydropathy."""

    HL = 1  # Hydrophilic
    HB = 2  # Hydrophobic
    M = 3  # Moderate


class AminoAcidToInt(Enum):
    """Enum for Amino Acid one letter code to integer."""

    A = 1  # Alanine
    C = 2  # Cysteine
    D = 3  # Aspartic Acid
    E = 4  # Glutamic Acid
    F = 5  # Phenylalanine
    G = 6  # Glycine
    H = 7  # Histidine
    I = 8  # Isoleucine
    K = 9  # Lysine
    L = 10  # Leucine
    M = 11  # Methionine
    N = 12  # Asparagine
    P = 13  # Proline
    Q = 14  # Glutamine
    R = 15  # Arginine
    S = 16  # Serine
    T = 17  # Threonine
    V = 18  # Valine
    W = 19  # Tryptophan
    Y = 20  # Tyrosine


class AminoAcidProperty(TypedDict):
    """Dictionary shape for Amino acid."""

    code = int
    hydropathy = int
    hydropathy_index = float
    acidity_basicity = int
    mass = float
    isoelectric_point = float
    charge = int


amino_acid: Dict[str, AminoAcidProperty] = {
    "A": {
        "code": AminoAcidToInt["A"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": 1.8,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 89.09,
        "isoelectric_point": 6.00,
        "charge": Charge["U"].value,
    },
    "C": {
        "code": AminoAcidToInt["C"].value,
        "hydropathy": Hydropathy["M"].value,
        "hydropathy_index": 2.5,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 121.16,
        "isoelectric_point": 5.02,
        "charge": Charge["U"].value,
    },
    "D": {
        "code": AminoAcidToInt["D"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -3.5,
        "acidity_basicity": AcidityBasicity["A"].value,
        "mass": 133.10,
        "isoelectric_point": 2.77,
        "charge": Charge["N"].value,
    },
    "E": {
        "code": AminoAcidToInt["E"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -3.5,
        "acidity_basicity": AcidityBasicity["A"].value,
        "mass": 147.13,
        "isoelectric_point": 3.22,
        "charge": Charge["N"].value,
    },
    "F": {
        "code": AminoAcidToInt["F"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": 2.8,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 165.19,
        "isoelectric_point": 5.44,
        "charge": Charge["U"].value,
    },
    "G": {
        "code": AminoAcidToInt["G"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": -0.4,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 75.07,
        "isoelectric_point": 5.97,
        "charge": Charge["U"].value,
    },
    "H": {
        "code": AminoAcidToInt["H"].value,
        "hydropathy": Hydropathy["M"].value,
        "hydropathy_index": -3.2,
        "acidity_basicity": AcidityBasicity["B"].value,
        "mass": 155.16,
        "isoelectric_point": 7.47,
        "charge": Charge["P"].value,
    },
    "I": {
        "code": AminoAcidToInt["I"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": 4.5,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 131.8,
        "isoelectric_point": 5.94,
        "charge": Charge["U"].value,
    },
    "K": {
        "code": AminoAcidToInt["K"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -3.9,
        "acidity_basicity": AcidityBasicity["B"].value,
        "mass": 146.19,
        "isoelectric_point": 9.59,
        "charge": Charge["P"].value,
    },
    "L": {
        "code": AminoAcidToInt["L"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": 3.8,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 131.18,
        "isoelectric_point": 5.98,
        "charge": Charge["U"].value,
    },
    "M": {
        "code": AminoAcidToInt["M"].value,
        "hydropathy": Hydropathy["M"].value,
        "hydropathy_index": 1.9,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 149.21,
        "isoelectric_point": 5.74,
        "charge": Charge["U"].value,
    },
    "N": {
        "code": AminoAcidToInt["N"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -3.5,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 132.12,
        "isoelectric_point": 5.41,
        "charge": Charge["U"].value,
    },
    "P": {
        "code": AminoAcidToInt["P"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": -1.6,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 115.13,
        "isoelectric_point": 6.30,
        "charge": Charge["U"].value,
    },
    "Q": {
        "code": AminoAcidToInt["Q"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -3.5,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 146.15,
        "isoelectric_point": 5.65,
        "charge": Charge["N"].value,
    },
    "R": {
        "code": AminoAcidToInt["R"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -4.5,
        "acidity_basicity": AcidityBasicity["B"].value,
        "mass": 174.20,
        "isoelectric_point": 11.15,
        "charge": Charge["P"].value,
    },
    "S": {
        "code": AminoAcidToInt["S"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -0.8,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 165.09,
        "isoelectric_point": 5.68,
        "charge": Charge["U"].value,
    },
    "T": {
        "code": AminoAcidToInt["T"].value,
        "hydropathy": Hydropathy["HL"].value,
        "hydropathy_index": -0.7,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 119.12,
        "isoelectric_point": 5.64,
        "charge": Charge["U"].value,
    },
    "V": {
        "code": AminoAcidToInt["V"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": 4.2,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 117.15,
        "isoelectric_point": 5.96,
        "charge": Charge["U"].value,
    },
    "W": {
        "code": AminoAcidToInt["W"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": -0.9,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 204.23,
        "isoelectric_point": 5.89,
        "charge": Charge["U"].value,
    },
    "Y": {
        "code": AminoAcidToInt["Y"].value,
        "hydropathy": Hydropathy["HB"].value,
        "hydropathy_index": -1.3,
        "acidity_basicity": AcidityBasicity["U"].value,
        "mass": 181.19,
        "isoelectric_point": 5.66,
        "charge": Charge["U"].value,
    },
}
