import random
FIRST_PART_NAME_GENS = [
    "Defiant", "Valour's", "Intrepid", "Ebon", "Reliable", "Loyal",
    "Adventures", "Brave", "Bright", "Honorable", "Gallant", "Steadfast",
    "Noble", "Mighty", "Fearless", "Courageous", "Daring", "Heroic",
    "Stalwart", "Resilient", "Valiant", "Fierce", "Indomitable", "Bold",
    "Unyielding", "Vigilant", "Unbreakable", "Sovereign", "Revered", "Proud",
    "Persevering", "Invincible", "Guardian", "Fortified", "Eternal",
    "Determined", "Commanding", "Boundless", "Awe-inspiring", "Ancestral",
    "Immutable", "Venerable", "Zealous", "Warrior's", "Primeval", "Majestic",
    "Infallible", "Harmonious", "Empyrean", "Dauntless"
]

SECOND_PART_NAME_GENS = [
    "Winter", "Star", "Hero", "Snow", "Leaf", "Bloom", "Trident", "Eagle",
    "Mountain", "River", "Forest", "Flame", "Storm", "Rock", "Ocean",
    "Thunder", "Blaze", "Sky", "Peak", "Waves", "Lightning", "Frost", "Glacier",
    "Horizon", "Crest", "Vortex", "Gale", "Canyon", "Serpent", "Phoenix", "Tide",
    "Wildfire", "Vale", "Summit", "Ridge", "Prairie", "Nebula", "Meadow", "Labyrinth",
    "Crusade", "Expanse", "Abyss", "Celestial", "Dragon", "Inferno", "Jungle", "Quartz",
    "Realm", "Zephyr"
]


def get_random_name():
    return f"{FIRST_PART_NAME_GENS[random.randint(0, len(FIRST_PART_NAME_GENS)-1)]}_{SECOND_PART_NAME_GENS[random.randint(0, len(SECOND_PART_NAME_GENS)-1)]}"

if __name__ == "__main__":
    print(get_random_name())
