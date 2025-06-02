import requests

def fetch_cafes(city="Heidelberg"):
    query = f"""
    [out:json];
    area["name"="{city}"]->.searchArea;
    node["amenity"="cafe"](area.searchArea);
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})
    data = response.json()

    cafes = []
    for el in data["elements"]:
        cafes.append({
            "Cafe Name": el["tags"].get("name", "Unnamed Cafe"),
            "lat": el["lat"],
            "lon": el["lon"]
        })

    return cafes
