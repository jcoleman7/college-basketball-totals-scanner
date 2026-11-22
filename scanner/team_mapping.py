
import re
import unicodedata

# Explicit aliases for known ESPN / TeamRankings naming differences.
ALIASES = {
    "Murray State": "Murray St",
    "Ball State": "Ball St",
    "Mississippi State": "Mississippi St",
    "Florida International": "Florida Intl",
    "East Tennessee State": "E Tennessee St",
    "Georgia Southern": "Georgia So",
    "Middle Tennessee": "Middle Tenn",
    "Mount St. Mary's": "Mt St Mary's",
    "Maryland Eastern Shore": "Maryland ES",
    "SIU Edwardsville": "SIU Edward",
    "Texas A&M-Corpus Christi": "Texas A&M-CC",
    "Cal State Northridge": "CS Northridge",
    "Cal State Fullerton": "CS Fullerton",
    "Cal State Bakersfield": "CS Bakersfield",
    "Central Arkansas": "C Arkansas",
    "Central Connecticut": "C Connecticut",
    "Central Michigan": "C Michigan",
    "South Florida": "S Florida",
    "Southern Illinois": "S Illinois",
    "Southern Miss": "Southern Miss",
    "North Florida": "N Florida",
    "North Texas": "N Texas",
    "Northern Arizona": "N Arizona",
    "Northern Illinois": "N Illinois",
    "Northern Iowa": "N Iowa",
    "Northern Kentucky": "N Kentucky",
    "Western Carolina": "W Carolina",
    "Western Illinois": "W Illinois",
    "Western Michigan": "W Michigan",
    "William & Mary": "William & Mary",
    "UC Santa Barbara": "UCSB",
    "Seattle U": "Seattle",
    "UConn": "UConn",
    "UMass": "UMass",
    "UCF": "UCF",
        "Cleveland State": "Cleveland St",
    "Eastern Illinois": "E Illinois",
    "Eastern Washington": "E Washington",
    "Kennesaw State": "Kennesaw St",
    "Massachusetts": "UMass",
    "Norfolk State": "Norfolk St",
    "Ole Miss": "Mississippi",
    "West Florida": "W Florida",
        "George Washington": "G Washington",
    "Stephen F. Austin": "SF Austin",
    "Coastal Carolina": "Coastal Car",
    "Western Kentucky": "W Kentucky",
    "Eastern Kentucky": "E Kentucky",
    "South Alabama": "S Alabama",
    "East Carolina": "E Carolina",
    "Boise State": "Boise St",
    "Fresno State": "Fresno St",
    "Loyola Maryland": "Loyola MD",
    "UAlbany": "Albany",
        "East Texas A&M": "E Texas A&M",
    "Sacramento State": "Sacramento St",
    "Tarleton": "Tarleton St",
    "CSU Northridge": "CS Northridge",
    "North Texas": "N Texas",
        "Appalachian State": "App State",
        "Southeast Missouri State": "SE Missouri St",
}

MASCOTS = {
    "pride", "racers", "scarlet knights", "cougars", "fighting irish",
    "gators", "peacocks", "river hawks", "flames", "salukis",
    "red foxes", "black knights", "bisons", "boilermakers",
    "fighting illini", "blue devils", "broncs", "hurricanes",
    "49ers", "wildcats", "zips", "bison", "phoenix", "argonauts",
    "bulldogs", "knights", "mountaineers", "buccaneers", "thundering herd",
    "spartans", "yellow jackets", "matadors", "trojans", "seahawks",
    "hawks", "tigers", "bulls", "rams", "jaspers", "chippewas",
    "flyers", "falcons", "tribe", "deacons", "panthers", "commodores",
    "mavericks", "lions", "fighting hawks", "redbirds", "islanders",
    "eagles", "blue raiders", "running eagles", "demons", "rebels",
    "cowboys", "utes", "volunteers", "monarchs", "cavaliers",
    "hornets", "anteaters", "redhawks", "bobcats", "crimson tide",
    "bears", "owls", "aces", "roos", "mustangs", "colonels",
    "bearkats", "huskies", "cardinals", "red wolves", "jaguars",
    "hawks", "pirates", "lady rebels", "lopes", "broncos",
    "bears", "blue hens", "minutemen", "minutewomen", 

}


def normalize_name(name):
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.replace(".", "").replace("'", "")
    name = re.sub(r"\s+", " ", name).strip()
    return name.lower()


def teamrankings_name(espn_name, available_names):
    words = espn_name.split()

    for i in range(len(words)):
        candidate = " ".join(words[:len(words) - i]) if i else espn_name
        normalized = normalize_name(candidate)

        # Apply explicit aliases.
        for alias, target in ALIASES.items():
            if normalize_name(alias) == normalized:
                candidate = target
                break

        # Match exact normalized names only.
        for available in available_names:
            if normalize_name(available) == normalize_name(candidate):
                return available

    return None
