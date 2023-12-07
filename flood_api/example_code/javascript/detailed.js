// Get the detailed flood forecast for the given coordinates with neighboring cells, between 2023-12-01 and 2023-12-07 (inclusive)
const response_loc = await fetch(
    "$api_url$api_path?" + new URLSearchParams({
          lon: "22.260536", 
          lat: "4.882569",
          include_neighbors: "true",
          start_date: "2023-12-01",
          end_date: "2023-12-07"
    })
  );
  const data_loc = await response_loc.json();
  
  // prints the name of the first result
  console.log(data_loc.features[0].properties.name);

// Get the detailed flood forecast for the given bounding box without neighboring cells, covering the entire forecast duration
const response_bbox = await fetch(
    "$api_url$api_path?" + new URLSearchParams({
          min_lon: "22.0", 
          max_lon: "23.05", 
          min_lat: "4.764412", 
          max_lat: "5.015732", 
    })
  );
  const data_bbox = await response_bbox.json();
  
  // prints the name of the first result
  console.log(data_bbox.features[0].properties.name);