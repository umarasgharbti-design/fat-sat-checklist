# checklist_data.py
# Defines the FAT and SAT checklist structures used by app.py

FAT_STRUCTURE = {
    "FAT Protocols": [
        "Drawing",
        "Dimensions",
        "Machine drawing with utilities",
    ],
    "Nameplate": ["Nameplate"],
    "Toolkit": ["Toolkit"],
    "Manual": [
        "Technical documents",
        "Operational documents",
        "Maintenance documents",
        "Installation documents",
    ],
    "Drawings": [
        "Electrical drawings",
        "P&ID",
        "Pneumatic drawings",
    ],
    "Backups": [
        "HMI backup",
        "PLC backup",
    ],
    "Certificates": [
        "Material certificates",
        "Instrument calibration certificate",
        "OEL certificate",
    ],
    "Validation Certificates": [
        "IQ",
        "OQ",
    ],
    "Alarm List": ["Alarm list"],
}

# Extra certificate item, added only if the machine has LEF / laminar flow installed
HEPA_CERTIFICATE_ITEM = "HEPA certificates"
HEPA_SECTION = "Certificates"

# Items unique to SAT, on top of everything in FAT_STRUCTURE
SAT_EXTRA_STRUCTURE = {
    "Site Activities": [
        "Machine placement",
        "Hard file documentation provided",
        "Receiving confirmation",
    ],
}


def get_structure(test_type: str, has_lef: bool = False) -> dict:
    """
    Returns the full checklist structure for the given test type.
    test_type: "FAT" or "SAT"
    has_lef: whether to include the HEPA certificate item
    """
    structure = {section: items.copy() for section, items in FAT_STRUCTURE.items()}

    if has_lef:
        structure[HEPA_SECTION] = structure[HEPA_SECTION] + [HEPA_CERTIFICATE_ITEM]

    if test_type == "SAT":
        structure.update(SAT_EXTRA_STRUCTURE)

    return structure
