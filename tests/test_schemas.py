"""
Tests for data schemas.
"""

import pytest
from pydantic import ValidationError

from faosim.core.schemas import (
    HistoricalData,
    Goal,
    UserConstraints,
    AudienceTargeting,
    AdCreative,
    BiddingStrategy,
    CampaignParameters,
)


def test_historical_data_valid():
    """Test valid historical data creation."""
    data = HistoricalData(
        cpm=15.0,
        ctr=0.02,
        cpc=0.75,
        cr=0.03,
        daily_budget=100.0
    )
    assert data.cpm == 15.0
    assert data.ctr == 0.02


def test_historical_data_invalid_ctr():
    """Test invalid CTR (out of range)."""
    with pytest.raises(ValidationError):
        HistoricalData(
            cpm=15.0,
            ctr=1.5,  # Invalid: > 1.0
            cpc=0.75,
            cr=0.03,
            daily_budget=100.0
        )


def test_goal_creation():
    """Test goal creation."""
    goal = Goal(
        metric="ROAS",
        target_value=2.5,
        tolerance=0.1
    )
    assert goal.metric == "ROAS"
    assert goal.target_value == 2.5


def test_user_constraints_valid():
    """Test valid user constraints."""
    historical_data = HistoricalData(
        cpm=15.0,
        ctr=0.02,
        cpc=0.75,
        cr=0.03,
        daily_budget=100.0
    )

    goal = Goal(
        metric="ROAS",
        target_value=2.5,
        tolerance=0.1
    )

    constraints = UserConstraints(
        product_cost=100.0,
        selling_price=300.0,
        historical_data=historical_data,
        goal=goal,
        max_loops=10,
        population_size=20
    )

    assert constraints.product_cost == 100.0
    assert constraints.selling_price == 300.0


def test_user_constraints_invalid_pricing():
    """Test invalid pricing (selling price <= product cost)."""
    historical_data = HistoricalData(
        cpm=15.0,
        ctr=0.02,
        cpc=0.75,
        cr=0.03,
        daily_budget=100.0
    )

    goal = Goal(
        metric="ROAS",
        target_value=2.5
    )

    with pytest.raises(ValidationError):
        UserConstraints(
            product_cost=300.0,
            selling_price=100.0,  # Invalid: < product_cost
            historical_data=historical_data,
            goal=goal
        )


def test_audience_targeting():
    """Test audience targeting creation."""
    audience = AudienceTargeting(
        age_min=25,
        age_max=45,
        genders=["all"],
        locations=["US", "CA"]
    )
    assert audience.age_min == 25
    assert audience.age_max == 45


def test_campaign_parameters():
    """Test full campaign parameters creation."""
    audience = AudienceTargeting(age_min=18, age_max=65)
    creative = AdCreative(format="single_image", headline="Test Ad")
    bidding = BiddingStrategy(
        optimization_goal="CONVERSIONS",
        bid_strategy="LOWEST_COST_WITHOUT_CAP",
        daily_budget=100.0
    )

    campaign = CampaignParameters(
        campaign_name="Test Campaign",
        audience=audience,
        creative=creative,
        bidding=bidding
    )

    assert campaign.campaign_name == "Test Campaign"
    assert campaign.bidding.daily_budget == 100.0
