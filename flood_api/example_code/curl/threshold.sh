# Get the return period thresholds for the given coordinates
curl -i -X GET $api_url$api_path?lon=22.260536&lat=4.882569

# Get the return period thresholds for the given bounding box
curl -i -X GET $api_url$api_path?min_lon=22.0&max_lon=23.05&min_lat=4.764412&max_lat=5.015732