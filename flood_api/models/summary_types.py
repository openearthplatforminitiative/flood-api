from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_validator

from flood_api.models.shared_types import BaseModelWithDates, Feature, FeatureCollection


class PeakTimingEnum(str, Enum):
    BLACK_BORDER = "BB"
    GRAYED_COLOR = "GC"
    GRAY_BORDER = "GB"


class TendencyEnum(str, Enum):
    UPWARD_TRIANGLE = "U"
    DOWNWARD_TRIANGLE = "D"
    CIRCLE = "C"


class IntensityEnum(str, Enum):
    PURPLE = "P"
    RED = "R"
    YELLOW = "Y"
    GREY = "G"


class SummaryProperties(BaseModelWithDates):
    # issued_on: date = Field(
    #     ...,
    #     description="The date the summary forecast was issued on.",
    #     json_schema_extra={"example": "2023-11-07"},
    # )
    peak_step: int = Field(
        ...,
        ge=1,
        le=30,
        description="The step number at which the peak occurs, ranging from 1 to 30.",
        json_schema_extra={"example": 1},
    )
    peak_day: date = Field(
        ...,
        description="The date the flood peak is forecasted to take place on, assuming UTC timezone.",
        json_schema_extra={"example": "2023-11-07"},
    )
    peak_timing: str = Field(
        ...,
        description="The timing of the flood peak indicated by border and grayed colors."
        "BB: Black border, peak forecasted within days 1-3. "
        "GC: Greyed color, peak forecasted after day 10 with <30% probability of exceeding "
        "the 2-year return period threshold in first 10 days. "
        "GB: Grey border, floods of some severity in first 10 days and peak after day 3.",
        json_schema_extra={"example": "BB"},
    )
    max_median_dis: float = Field(
        ...,
        ge=0.0,
        description="The maximum of the median discharges over the forecast horizon.",
        json_schema_extra={"example": 314.96875},
    )
    min_median_dis: float = Field(
        ...,
        ge=0.0,
        description="The minimum of the median discharges over the forecast horizon.",
        json_schema_extra={"example": 89.9921875},
    )
    control_dis: float = Field(
        ...,
        ge=0.0,
        description="The control discharge value. Currently taken to be the median discharge of the first day in forecasted.",
        json_schema_extra={"example": 314.96875},
    )
    max_max_dis: float = Field(
        ...,
        ge=0.0,
        description="The maximum of the maximum discharges over the forecast horizon.",
        json_schema_extra={"example": 340.7265625},
    )
    min_min_dis: float = Field(
        ...,
        ge=0.0,
        description="The minimum of the minimum discharges over the forecast horizon.",
        json_schema_extra={"example": 67.703125},
    )
    tendency: TendencyEnum = Field(
        ...,
        description="Flood tendency (indicated by shape) according to the evolution of flood intensity signal over the forecast horizon. "
        "U: Upward triangle, increasing trend over the next 30-days with 30-day max median exceeding initial (control) discharge by >10%. "
        "D: Downward triangle, decreasing trend over the next 30-days with 30-day max median not exceeding initial discharge by >10% and min median is >=10% below initial discharge. "
        "C: Circle, stagnant flow with no significant trend detected.",
        json_schema_extra={"example": "U"},
    )
    max_p_above_20y: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="The maximum probability of exceeding the 20-year return period threshold over the forecast horizon.",
        json_schema_extra={"example": 1.0},
    )
    max_p_above_5y: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="The maximum probability of exceeding the 5-year return period threshold over the forecast horizon.",
        json_schema_extra={"example": 1.0},
    )
    max_p_above_2y: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="The maximum probability of exceeding the 2-year return period threshold over the forecast horizon.",
        json_schema_extra={"example": 1.0},
    )
    intensity: IntensityEnum = Field(
        ...,
        description="The flood intensity (indicated by color) relating to maximum return period threshold exceedance probabilities over the forecast horizon. "
        "P: Purple, maximum 20-year exceedance probability >=30%; "
        "R: Red, maximum for 20-year <30% and 5-year >=30%; "
        "Y: Yellow, maximum for 5-year <30% and 2-year >=30%; "
        "G: Gray, no flood signal (2-year <30%).",
        json_schema_extra={"example": "P"},
    )

    @field_validator("peak_timing")
    def check_peak_timing(cls, value):
        if value not in PeakTimingEnum._member_map_.values():
            raise ValueError(
                f"peak_timing must be one of {PeakTimingEnum._member_map_.values()}"
            )
        return value

    @field_validator("tendency")
    def check_tendency(cls, value):
        if value not in TendencyEnum._member_map_.values():
            raise ValueError(
                f"tendency must be one of {TendencyEnum._member_map_.values()}"
            )
        return value

    @field_validator("intensity")
    def check_intensity(cls, value):
        if value not in IntensityEnum._member_map_.values():
            raise ValueError(
                f"intensity must be one of {IntensityEnum._member_map_.values()}"
            )
        return value


class SummaryFeature(Feature):
    properties: SummaryProperties = Field(
        ...,
        description="Specific properties of the summary forecast, including various attributes like tendency, peak step, and intensity.",
    )


class SummaryFeatureCollection(FeatureCollection):
    features: List[SummaryFeature] = Field(
        ...,
        description="A collection of summary forecasts, each containing specific forecast information for a queried location.",
    )


class SummaryResponseModel(BaseModel):
    queried_cell: SummaryFeatureCollection = Field(
        ...,
        description="A feature collection representing the queried cell's summary forecast data.",
    )
    neighboring_cells: SummaryFeatureCollection = Field(
        ...,
        description="A feature collection representing the neighboring cells' summary forecast data, potentially empty if there are no neighboring cells with forecast data.",
    )
