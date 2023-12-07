// Get the return period thresholds for the given coordinates
const response_loc = await fetch(
    "$api_url$api_path?" + new URLSearchParams({
          lon: "22.260536", 
          lat: "4.882569"
    })
  );
  const data_loc = await response_loc.json();
  
  // prints the name of the first result
  console.log(data_loc.features[0].properties.name);

// Get the return period thresholds for the given bounding box
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