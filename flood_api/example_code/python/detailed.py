from httpx import Client

with Client() as client:
    # Get the detailed flood forecast for the given coordinates and neighboring cells, between 2024-01-25 and 2024-02-03 (inclusive)
    response_loc = client.get(
        url="$endpoint_url",
        params={
            "lon": 33.575897,
            "lat": -1.375532,
            "include_neighbors": "true",
            "start_date": "2024-01-25",
            "end_date": "2024-02-03",
        },
    )

    data_loc = response_loc.json()

    # prints the minimum discharge for the first day of the forecast at the queried location
    print(data_loc["queried_location"]["features"][0]["properties"]["min_dis"])

    # Get the detailed flood forecast for the given bounding box without neighboring cells, covering the entire forecast duration
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

    # prints the minimum discharge for the first day of the forecast at the first result in the queried bounding box
    print(data_bbox["queried_location"]["features"][0]["properties"]["min_dis"])
