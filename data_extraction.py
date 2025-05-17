import re

def extract_properties(text):
    patterns = {
        "Weight": r"(\d+(\.\d+)?)(?:kg)?Weight",
        "FatFreeBodyWeight": r"(\d+(\.\d+)?)(?:kg)?Fat(?:-)?FreeMass",
        "BodyWater": r"(\d+(\.\d+)?)%BodyWater",
        "BoneMass": r"(\d+(\.\d+)?)(?:kg)?BoneMass",
        "MetabolicAge": r"(\d+(\.\d+)?)MetabolicAge",
        "BMI": r"(\d+(\.\d+)?)BMI",
        "SubcutaneousFat": r"(\d+(\.\d+)?)%SubcutaneousFat",
        "SkeletalMuscle": r"(\d+(\.\d+)?)%SkeletalMuscle",
        "Protein": r"(\d+(\.\d+)?)%Protein",
        "BodyFat": r"(\d+(\.\d+)?)%BodyFat",
        "VisceralFat": r"(\d+(\.\d+)?)VisceralFat",
        "MuscleMass": r"(\d+(\.\d+)?)(?:kg)?MuscleMass",
        "BMR": r"(\d+(\d+)?)BMR"
    }

    properties = {}

    for prop, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            properties[prop] = float(match.group(1))
        else:
            properties[prop] = None

    return properties
