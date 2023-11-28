from typing import List

from pydantic import BaseModel, Field

from flood_api.models.shared_types import Feature, FeatureCollection


class ThresholdProperties(BaseModel):
    threshold_2y: float = Field(
        ...,
        description="The 2-year return period threshold in m^3/s.",
        ge=0.0,
        json_schema_extra={"example": 17.34925885},
    )
    threshold_5y: float = Field(
        ...,
        description="The 5-year return period threshold in m^3/s.",
        ge=0.0,
        json_schema_extra={"example": 19.26002567},
    )
    threshold_20y: float = Field(
        ...,
        description="The 20-year return period threshold in m^3/s.",
        ge=0.0,
        json_schema_extra={"example": 30.15522911},
    )


class ThresholdFeature(Feature):
    properties: ThresholdProperties = Field(
        ...,
        description="Properties defining flood thresholds for various return periods, used to categorize flood risk.",
    )


class ThresholdFeatureCollection(FeatureCollection):
    features: List[ThresholdFeature] = Field(
        ...,
        description="A collection of threshold features, each outlining the specific discharge thresholds associated with different return period flood risks.",
    )


class ThresholdResponseModel(BaseModel):
    queried_data: ThresholdFeatureCollection = Field(
        ...,
        description="A feature collection representing the queried location's threshold data for flood risk analysis.",
    )
