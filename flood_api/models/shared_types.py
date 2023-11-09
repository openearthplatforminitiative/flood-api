from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from flood_api.settings import settings

GLOFAS_RESOLUTION = settings.glofas_resolution


class GeometryType(str, Enum):
    POLYGON = "Polygon"


class Geometry(BaseModel):
    type: GeometryType = Field(
        ...,
        description="The nature of the geometry type, which is 'Polygon' for this model.",
        json_schema_extra={"example": "Polygon"},
    )
    coordinates: List[List[List[float]]] = Field(
        ...,
        description=f"Coordinates for the Polygon geometry type, defined according to a {GLOFAS_RESOLUTION}-degree resolution grid. "
        "Each polygon's coordinates are provided as an array of points, with each point specifying its "
        "longitude and latitude in decimal degrees. The array forms a closed linear ring that defines the "
        "polygon's boundary, with the first and last point being identical to close the ring.",
        json_schema_extra={
            "example": [
                [
                    [51.95, 16.95],
                    [51.95, 17.0],
                    [52.0, 17.0],
                    [52.0, 16.95],
                    [51.95, 16.95],
                ]
            ]
        },
    )


class Feature(BaseModel):
    id: str = Field(..., description="A unique identifier for the feature.")
    type: str = Field(
        ...,
        description="The type of the feature, typically 'Feature' for GeoJSON objects.",
        json_schema_extra={"example": "Feature"},
    )
    geometry: Geometry = Field(
        ...,
        description="The geometric details of the feature, including its type and coordinates.",
    )


class FeatureCollection(BaseModel):
    type: str = Field(
        description="The type of the collection, typically 'FeatureCollection' for a group of features.",
    )
    features: List[Feature] = Field(
        ...,
        description="A list of feature objects, each containing its unique identifier, type, and geometry.",
    )
