import random
FIRST_PART_NAME_GENS = [
    "Defiant",
    "Valour's",
    "Intrepid",
    "Ebon",
    "Reliable",
    "Loyal",
    "Adventures",
    "Brave",
    "Bright",
    "Honorable",
    "Gallant",
    "Steadfast",
    "Noble",
    "Mighty",
    "Fearless",
    "Courageous",
    "Daring",
    "Heroic",
    "Stalwart",
    "Resilient",
    "Valiant",
    "Fierce",
    "Indomitable",
    "Bold",
    "Unyielding"
]

SECOND_PART_NAME_GENS = [
    "Winter",
    "Star",
    "Hero",
    "Snow",
    "Leaf",
    "Bloom",
    "Trident",
    "Eagle",
    "Mountain",
    "River",
    "Forest",
    "Flame",
    "Storm",
    "Rock",
    "Ocean",
    "Thunder",
    "Blaze",
    "Sky",
    "Peak",
    "Waves",
    "Lightning",
    "Frost"
]

def get_random_name():
    return f"{FIRST_PART_NAME_GENS[random.randint(0, len(FIRST_PART_NAME_GENS))]}_{SECOND_PART_NAME_GENS[random.randint(0, len(SECOND_PART_NAME_GENS))]}"

if __name__ == "__main__":
    print(get_random_name())
