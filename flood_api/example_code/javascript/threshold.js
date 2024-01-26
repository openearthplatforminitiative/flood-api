// Get the return period thresholds for the given coordinates
const response_loc = await fetch(
    "$endpoint_url?" + new URLSearchParams({
          lon: "33.575897", 
          lat: "-1.375532",
    })
  );
  const data_loc = await response_loc.json();
  
  // prints the return period thresholds for the queried location
  console.log(data_loc.queried_location.features[0].properties.threshold_2y);

// Get the return period thresholds for the given bounding box
const response_bbox = await fetch(
    "$endpoint_url?" + new URLSearchParams({
          min_lon: "33.50", 
          max_lon: "34.55", 
          min_lat: "-1.40", 
          max_lat: "-1.30",
    })
  );
  const data_bbox = await response_bbox.json();
  
  // prints the return period thresholds for the first result in the queried bounding box
  console.log(data_bbox.queried_location.features[0].properties.threshold_2y);
