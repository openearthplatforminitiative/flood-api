from httpx import Client

with Client() as client:
    # Get the summary flood forecast for the given coordinates and neighboring cells
    response_loc = client.get(
        url="$endpoint_url",
        params={"lon": 33.575897, "lat": -1.375532, "include_neighbors": "true"},
    )

    data_loc = response_loc.json()

    # prints the peak day for the queried location
    print(data_loc["queried_location"]["features"][0]["properties"]["peak_day"])

    # Get the summary flood forecast for the given bounding box without neighboring cells
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

    # prints the peak day for the first result in the queried bounding box
    print(data_bbox["queried_location"]["features"][0]["properties"]["peak_day"])
