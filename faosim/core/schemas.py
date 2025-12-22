"""
Data schemas for FAO-Sim system using Pydantic v2.
Defines input/output data structures for campaign optimization.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class MetricType(str, Enum):
    """Supported optimization metrics."""
    ROAS = "ROAS"
    ROI = "ROI"
    CPA = "CPA"
    CTR = "CTR"
    CR = "CR"


class HistoricalData(BaseModel):
    """Historical campaign performance data for forecasting."""

    cpm: float = Field(..., gt=0, description="Cost per 1000 impressions")
    ctr: float = Field(..., gt=0, le=1, description="Click-through rate (0-1)")
    cpc: float = Field(..., gt=0, description="Cost per click")
    cr: float = Field(..., gt=0, le=1, description="Conversion rate (0-1)")
    daily_budget: float = Field(..., gt=0, description="Daily budget in currency")
    impressions: Optional[int] = Field(None, description="Total impressions")
    clicks: Optional[int] = Field(None, description="Total clicks")
    conversions: Optional[int] = Field(None, description="Total conversions")

    @field_validator('ctr', 'cr')
    @classmethod
    def validate_percentage(cls, v: float) -> float:
        """Ensure percentage values are between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError(f"Value must be between 0 and 1, got {v}")
        return v


class Goal(BaseModel):
    """Optimization goal and target metrics."""

    metric: MetricType = Field(..., description="Target metric to optimize")
    target_value: float = Field(..., gt=0, description="Target value for the metric")
    tolerance: float = Field(0.1, ge=0, le=1, description="Acceptable tolerance (0-1)")

    class Config:
        use_enum_values = True


class UserConstraints(BaseModel):
    """User-defined constraints and input data."""

    product_cost: float = Field(..., gt=0, description="Product cost (COGS)")
    selling_price: float = Field(..., gt=0, description="Product selling price")
    historical_data: HistoricalData = Field(..., description="Historical performance data")
    goal: Goal = Field(..., description="Optimization goal")
    max_loops: int = Field(10, gt=0, le=100, description="Maximum optimization loops")
    population_size: int = Field(20, gt=0, le=100, description="Campaign variants per generation")
    min_daily_budget: Optional[float] = Field(None, gt=0, description="Minimum daily budget")
    max_daily_budget: Optional[float] = Field(None, gt=0, description="Maximum daily budget")

    @field_validator('selling_price')
    @classmethod
    def validate_pricing(cls, v: float, info) -> float:
        """Ensure selling price is greater than product cost."""
        if 'product_cost' in info.data and v <= info.data['product_cost']:
            raise ValueError("Selling price must be greater than product cost")
        return v


class AudienceTargeting(BaseModel):
    """Audience targeting parameters."""

    age_min: int = Field(18, ge=13, le=65)
    age_max: int = Field(65, ge=13, le=65)
    genders: List[Literal["male", "female", "all"]] = Field(default=["all"])
    locations: List[str] = Field(default=["US"], description="Country codes")
    interests: List[str] = Field(default=[], description="Interest IDs or keywords")
    behaviors: List[str] = Field(default=[], description="Behavior targeting")
    custom_audiences: List[str] = Field(default=[], description="Custom audience IDs")
    lookalike_audiences: List[str] = Field(default=[], description="Lookalike audience IDs")

    @field_validator('age_max')
    @classmethod
    def validate_age_range(cls, v: int, info) -> int:
        """Ensure age_max >= age_min."""
        if 'age_min' in info.data and v < info.data['age_min']:
            raise ValueError("age_max must be >= age_min")
        return v


class AdCreative(BaseModel):
    """Ad creative configuration."""

    format: Literal["single_image", "carousel", "video", "collection"] = Field(
        "single_image", description="Ad format"
    )
    headline: str = Field("", max_length=255)
    primary_text: str = Field("", max_length=2200)
    description: str = Field("", max_length=255)
    call_to_action: Literal[
        "SHOP_NOW", "LEARN_MORE", "SIGN_UP", "DOWNLOAD", "BOOK_NOW", "CONTACT_US"
    ] = Field("SHOP_NOW")
    image_urls: List[str] = Field(default=[], description="Image URLs")
    video_url: Optional[str] = Field(None, description="Video URL")


class BiddingStrategy(BaseModel):
    """Bidding and optimization strategy."""

    optimization_goal: Literal[
        "CONVERSIONS", "LINK_CLICKS", "IMPRESSIONS", "REACH", "LANDING_PAGE_VIEWS"
    ] = Field("CONVERSIONS")
    bid_strategy: Literal[
        "LOWEST_COST_WITHOUT_CAP",
        "LOWEST_COST_WITH_BID_CAP",
        "COST_CAP",
        "LOWEST_COST_WITH_MIN_ROAS"
    ] = Field("LOWEST_COST_WITHOUT_CAP")
    bid_amount: Optional[float] = Field(None, gt=0, description="Bid cap or cost cap")
    daily_budget: float = Field(..., gt=0)


class CampaignParameters(BaseModel):
    """Complete campaign configuration parameters."""

    campaign_id: Optional[str] = Field(None, description="Unique campaign identifier")
    campaign_name: str = Field(..., description="Campaign name")
    audience: AudienceTargeting = Field(default_factory=AudienceTargeting)
    creative: AdCreative = Field(default_factory=AdCreative)
    bidding: BiddingStrategy = Field(..., description="Bidding strategy")
    placements: List[Literal[
        "facebook_feed", "instagram_feed", "facebook_stories",
        "instagram_stories", "messenger", "audience_network"
    ]] = Field(default=["facebook_feed", "instagram_feed"])
    schedule_start: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    schedule_end: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")

    # Metadata for tracking
    generation: int = Field(0, description="Generation number in optimization loop")
    parent_ids: List[str] = Field(default=[], description="Parent campaign IDs")


class ForecastMetrics(BaseModel):
    """Forecasted performance metrics."""

    predicted_cpm: float = Field(..., gt=0)
    predicted_ctr: float = Field(..., gt=0, le=1)
    predicted_cpc: float = Field(..., gt=0)
    predicted_cr: float = Field(..., gt=0, le=1)
    predicted_cpa: float = Field(..., gt=0)
    predicted_roas: float = Field(..., ge=0)
    predicted_roi: float = Field(...)

    # Confidence intervals
    cpm_confidence_low: Optional[float] = None
    cpm_confidence_high: Optional[float] = None
    confidence_score: float = Field(0.0, ge=0, le=1, description="Forecast confidence")


class ForecastResult(BaseModel):
    """Result of forecasting simulation."""

    campaign_params: CampaignParameters
    forecast_metrics: ForecastMetrics
    is_winner: bool = Field(False, description="Meets target criteria")
    score: float = Field(0.0, description="Overall fitness score")
    notes: str = Field("", description="Additional notes or warnings")


class OptimizationResult(BaseModel):
    """Final optimization results."""

    winning_campaigns: List[ForecastResult] = Field(default=[])
    failed_campaigns: List[ForecastResult] = Field(default=[])
    total_loops: int = Field(0)
    best_roas: float = Field(0.0)
    best_campaign: Optional[CampaignParameters] = None
    convergence_history: List[Dict[str, Any]] = Field(default=[])
    execution_time_seconds: float = Field(0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "winning_campaigns": [],
                "failed_campaigns": [],
                "total_loops": 10,
                "best_roas": 2.5,
                "execution_time_seconds": 123.45
            }
        }


class KnowledgeBaseDocument(BaseModel):
    """Document structure for RAG knowledge base."""

    doc_id: str
    content: str
    metadata: Dict[str, Any] = Field(default={})
    category: Optional[str] = None
    embeddings: Optional[List[float]] = None


class ParameterSpace(BaseModel):
    """Defines the searchable parameter space from RAG."""

    targeting_strategies: List[Dict[str, Any]] = Field(default=[])
    creative_formats: List[str] = Field(default=[])
    bidding_strategies: List[str] = Field(default=[])
    placement_combinations: List[List[str]] = Field(default=[])
    budget_ranges: Dict[str, float] = Field(default={})

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy access."""
        return self.model_dump()
