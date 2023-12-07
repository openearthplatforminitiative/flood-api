from httpx import Client

with Client() as client:
    # Get the return period thresholds for the given coordinates
    response_loc = client.get(
        url="$api_url$api_path", params={"lon": 22.260536, "lat": 4.882569}
    )

    data_loc = response_loc.json()

    # prints the name of the first result
    print(data_loc["features"][0]["properties"]["name"])

    # Get the return period thresholds for the given bounding box
    response_bbox = client.get(
        url="$api_url$api_path",
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
