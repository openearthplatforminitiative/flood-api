# Get the detailed flood forecast for the given coordinates with neighboring cells, between 2023-12-01 and 2023-12-07 (inclusive)
curl -i -X GET $api_url$api_path?lon=22.260536&lat=4.882569&include_neighbors=true&start_date=2023-12-01&end_date=2023-12-07

# Get the detailed flood forecast for the given bounding box without neighboring cells, covering the entire forecast duration
curl -i -X GET $api_url$api_path?min_lon=22.0&max_lon=23.05&min_lat=4.764412&max_lat=5.015732