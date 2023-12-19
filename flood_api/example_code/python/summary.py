from httpx import Client

with Client() as client:
    # Get the summary flood forecast for the given coordinates and neighboring cells
    response_loc = client.get(
        url="$endpoint_url",
        params={"lon": 22.260536, "lat": 4.882569, "include_neighbors": "true"},
    )

    data_loc = response_loc.json()

    # prints the name of the first result
    print(data_loc["features"][0]["properties"]["name"])

    # Get the summary flood forecast for the given bounding box without neighboring cells
    response_bbox = client.get(
        url="$endpoint_url",
        params={
            "min_lon": 22.0,
            "max_lon": 23.05,
            "min_lat": 4.764412,
            "max_lat": 5.015732,
        },
    )

    data_bbox = response_bbox.json()

    # prints the name of the first result
    print(data_bbox["features"][0]["properties"]["name"])
