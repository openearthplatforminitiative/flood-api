# Get the summary flood forecast for the given coordinates and neighboring cells
curl -i -X GET $endpoint_url?lon=22.260536&lat=4.882569&include_neighbors=true

# Get the summary flood forecast for the given bounding box without neighboring cells
curl -i -X GET $endpoint_url?min_lon=22.0&max_lon=23.05&min_lat=4.764412&max_lat=5.015732
