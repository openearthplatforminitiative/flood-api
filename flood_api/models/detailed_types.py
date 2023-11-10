from datetime import date
from typing import List

from pydantic import BaseModel, Field

from flood_api.models.shared_types import CustomBaseModel, Feature, FeatureCollection


class DetailedProperties(CustomBaseModel):
    issued_on: date = Field(
        ...,
        description="The date the detailed forecast was issued on.",
        json_schema_extra={"example": "2023-11-07"},
    )
    valid_for: date = Field(
        ...,
        description="The date of the 24-hour forecast period for the flood. "
        "The forecast uses the discharge expected between 00:00 and 23:59 of that day.",
        json_schema_extra={"example": "2023-12-01"},
    )
    step: int = Field(
        ...,
        ge=1,
        le=30,
        description="The time step number of the forecast data.",
        json_schema_extra={"example": 22},
    )
    p_above_2y: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of exceedance over the 2-year return period threshold.",
        json_schema_extra={"example": 0.8627450980392157},
    )
    p_above_5y: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of exceedance over the 5-year return period threshold.",
        json_schema_extra={"example": 0.29411764705882354},
    )
    p_above_20y: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of exceedance over the 20-year return period threshold.",
        json_schema_extra={"example": 0.0196078431372549},
    )
    min_dis: float = Field(
        ...,
        ge=0.0,
        description="Minimum forecasted discharge.",
        json_schema_extra={"example": 16.2890625},
    )
    Q1_dis: float = Field(
        ...,
        ge=0.0,
        description="First quartile of forecasted discharge.",
        json_schema_extra={"example": 21.83984375},
    )
    median_dis: float = Field(
        ...,
        ge=0.0,
        description="Median forecasted discharge.",
        json_schema_extra={"example": 24.87109375},
    )
    Q3_dis: float = Field(
        ...,
        ge=0.0,
        description="Third quartile of forecasted discharge.",
        json_schema_extra={"example": 27.44921875},
    )
    max_dis: float = Field(
        ...,
        ge=0.0,
        description="Maximum forecasted discharge.",
        json_schema_extra={"example": 39.64062599},
    )


class DetailedFeature(Feature):
    properties: DetailedProperties = Field(
        ...,
        description="Specific properties of the detailed forecast, including probabilities for different return periods and discharge statistics.",
    )


class DetailedFeatureCollection(FeatureCollection):
    features: List[DetailedFeature] = Field(
        ...,
        description="A collection of detailed forecasts, providing extensive forecast data including detailed probabilities and discharge information.",
    )


class DetailedResponseModel(BaseModel):
    queried_cell: DetailedFeatureCollection = Field(
        ...,
        description="A feature collection representing the queried cell's detailed forecast data.",
    )
    neighboring_cells: DetailedFeatureCollection = Field(
        ...,
        description="A feature collection representing the neighboring cells' detailed forecast data, potentially empty if there are no neighboring cells with forecast data.",
    )