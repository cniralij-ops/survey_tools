import sys
import csv
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim

# --- Haversine formula ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# --- Load Survey Data ---
def load_survey_data(filename):
    surveys = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            surveys.append({
                "survey_no": row["survey_no"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"])
            })
    return surveys

# --- Layered Search ---
def layered_search(village_center, target_survey, survey_points, layers=[1, 3, 5, 10]):
    for radius in layers:
        for s in survey_points:
            if s["survey_no"] == target_survey:
                dist = haversine(village_center[0], village_center[1], s["lat"], s["lon"])
                if dist <= radius:
                    return s, radius
    return None, None

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 find_survey.py \"VillageName\" SurveyNumber")
        sys.exit(1)

    village_name = sys.argv[1]          # first argument
    target_survey = sys.argv[2]         # second argument (survey number)

    geolocator = Nominatim(user_agent="survey_locator")
    location = geolocator.geocode(village_name + ", Gujarat, India")
    if not location:
        print("Village not found in geocoding.")
        sys.exit(1)

    village_center = (location.latitude, location.longitude)
    print(f"Village center: {village_center}")

    survey_points = load_survey_data("survey_latlon01gandhinagar.csv")

    result, used_radius = layered_search(village_center, target_survey, survey_points)

    if result:
        print(f"✅ Found survey {target_survey} within {used_radius} km")
        print(f"Lat: {result['lat']}, Lon: {result['lon']}")
    else:
        print("❌ Survey not found within given layers")

