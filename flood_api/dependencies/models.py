from datetime import datetime
from typing import List

from pydantic import BaseModel


# Base classes
class Geometry(BaseModel):
    type: str
    coordinates: List[List[List[float]]]


class Feature(BaseModel):
    id: str
    type: str
    geometry: Geometry


class FeatureCollection(BaseModel):
    type: str
    features: List[Feature]


# Separate properties models
class SummaryProperties(BaseModel):
    issued_on: datetime
    peak_step: int
    peak_day: datetime
    peak_timing: str
    max_median_dis: float
    min_median_dis: float
    control_dis: float
    max_max_dis: float
    min_min_dis: float
    tendency: str
    max_p_above_20y: float
    max_p_above_5y: float
    max_p_above_2y: float
    intensity: str


class DetailedProperties(BaseModel):
    issued_on: datetime
    valid_time: datetime
    step: int
    p_above_2y: float
    p_above_5y: float
    p_above_20y: float
    min_dis: float
    Q1_dis: float
    median_dis: float
    Q3_dis: float
    max_dis: float


class ThresholdProperties(BaseModel):
    threshold_2y: float
    threshold_5y: float
    threshold_20y: float


# Feature extensions with specific properties
class SummaryFeature(Feature):
    properties: SummaryProperties


class DetailedFeature(Feature):
    properties: DetailedProperties


class ThresholdFeature(Feature):
    properties: ThresholdProperties


# Specific feature collections
class SummaryFeatureCollection(FeatureCollection):
    features: List[SummaryFeature]


class DetailedFeatureCollection(FeatureCollection):
    features: List[DetailedFeature]


class ThresholdFeatureCollection(FeatureCollection):
    features: List[ThresholdFeature]


# Response models for each endpoint
class SummaryResponseModel(BaseModel):
    queried_cell: SummaryFeatureCollection
    neighboring_cells: SummaryFeatureCollection


class DetailedResponseModel(BaseModel):
    queried_cell: DetailedFeatureCollection
    neighboring_cells: DetailedFeatureCollection


class ThresholdResponseModel(BaseModel):
    queried_cell: ThresholdFeatureCollection
