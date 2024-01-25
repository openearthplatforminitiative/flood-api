// Get the detailed flood forecast for the given coordinates and neighboring cells, between 2024-01-25 and 2024-02-03 (inclusive)
const response_loc = await fetch(
    "$endpoint_url?" + new URLSearchParams({
          lon: "33.575897", 
          lat: "-1.375532",
          include_neighbors: "true",
          start_date: "2024-01-25",
          end_date: "2024-02-03"
    })
  );
  const data_loc = await response_loc.json();
  
  // prints the minimum discharge for the first day of the forecast at the queried location
  console.log(data_loc.queried_location.features[0].properties.min_dis);

// Get the detailed flood forecast for the given bounding box without neighboring cells, covering the entire forecast duration
const response_bbox = await fetch(
    "$endpoint_url?" + new URLSearchParams({
          min_lon: "33.50", 
          max_lon: "34.55", 
          min_lat: "-1.40", 
          max_lat: "-1.30", 
    })
  );
  const data_bbox = await response_bbox.json();
  
  // prints the minimum discharge for the first day of the forecast at the first result in the queried bounding box
  console.log(data_bbox.queried_location.features[0].properties.min_dis);
