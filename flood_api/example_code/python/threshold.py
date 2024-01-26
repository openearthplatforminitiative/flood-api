from httpx import Client

with Client() as client:
    # Get the return period thresholds for the given coordinates
    response_loc = client.get(
        url="$endpoint_url", params={"lon": 33.575897, "lat": -1.375532}
    )

    data_loc = response_loc.json()

    # prints the return period thresholds for the queried location
    print(data_loc["queried_location"]["features"][0]["properties"]["threshold_2y"])

    # Get the return period thresholds for the given bounding box
    response_bbox = client.get(
        url="$endpoint_url",
        params={
            "min_lon": 33.50,
            "max_lon": 34.55,
            "min_lat": -1.40,
            "max_lat": -1.30,
        },
    )

    data_bbox = response_bbox.json()

    # prints the return period thresholds for the first result in the queried bounding box
    print(data_bbox["queried_location"]["features"][0]["properties"]["threshold_2y"])
