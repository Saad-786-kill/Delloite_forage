import json
from datetime import datetime

# Convert from Format 1 (data-1.json)
def convertFromFormat1(jsonObject):
    location_parts = jsonObject["location"].split("/")

    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],  # already in milliseconds
        "country": location_parts[0],
        "city": location_parts[1],
        "area": location_parts[2],
        "factory": location_parts[3],
        "section": location_parts[4],
        "operationStatus": jsonObject["operationStatus"],
        "temperature": jsonObject["temp"]
    }


# Convert from Format 2 (data-2.json)
def convertFromFormat2(jsonObject):
    from datetime import datetime, timezone

    # Handle timestamp safely
    time_key = "time" if "time" in jsonObject else "timestamp"

    dt = datetime.strptime(jsonObject[time_key], "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    timestamp_ms = int(dt.timestamp() * 1000)

    # Handle location safely
    if "location" in jsonObject:
        if isinstance(jsonObject["location"], dict):
            loc = jsonObject["location"]
            country = loc["country"]
            city = loc["city"]
            area = loc["area"]
            factory = loc["factory"]
            section = loc["section"]
        else:
            parts = jsonObject["location"].split("/")
            country, city, area, factory, section = parts
    else:
        # Already flattened
        country = jsonObject["country"]
        city = jsonObject["city"]
        area = jsonObject["area"]
        factory = jsonObject["factory"]
        section = jsonObject["section"]

    return {
        "deviceID": jsonObject.get("device", {}).get("id", jsonObject.get("deviceID")),
        "deviceType": jsonObject.get("device", {}).get("type", jsonObject.get("deviceType")),
        "timestamp": timestamp_ms,
        "country": country,
        "city": city,
        "area": area,
        "factory": factory,
        "section": section,
        "operationStatus": jsonObject.get("data", {}).get("status", jsonObject.get("operationStatus")),
        "temperature": jsonObject.get("data", {}).get("temperature", jsonObject.get("temperature"))
    }

# ---------------- DO NOT MODIFY BELOW ---------------- #

def main():
    with open('data-1.json', encoding='utf-8') as f1, \
     open('data-2.json', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    result = []
    result.append(convertFromFormat1(data1))
    result.append(convertFromFormat2(data2))

    with open('data-result.json', 'w') as fout:
        json.dump(result, fout, indent=2)

    print("Transformation complete. Check data-result.json")


if __name__ == "__main__":
    main()