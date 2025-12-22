"""
Campaign Parameter Generator

Generates campaign parameter variants based on RAG knowledge base
and optimization constraints. Creates diverse campaign configurations
for testing and optimization.
"""

import random
import uuid
from typing import List, Dict, Any, Optional
from loguru import logger

from faosim.core.schemas import (
    CampaignParameters,
    AudienceTargeting,
    AdCreative,
    BiddingStrategy,
    ParameterSpace,
    UserConstraints,
)


class CampaignGenerator:
    """
    Generates campaign parameter variants for optimization.

    Uses parameter space from RAG knowledge base to create
    diverse campaign configurations.
    """

    def __init__(
        self,
        parameter_space: ParameterSpace,
        user_constraints: UserConstraints,
        seed: Optional[int] = None,
    ):
        """
        Initialize campaign generator.

        Args:
            parameter_space: Available parameter space from RAG
            user_constraints: User-defined constraints
            seed: Random seed for reproducibility
        """
        self.parameter_space = parameter_space
        self.user_constraints = user_constraints
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        logger.info("Campaign Generator initialized")

    def generate_initial_population(
        self, population_size: int
    ) -> List[CampaignParameters]:
        """
        Generate initial population of campaign variants.

        Args:
            population_size: Number of variants to generate

        Returns:
            List of campaign parameter configurations
        """
        logger.info(f"Generating initial population of {population_size} campaigns...")

        campaigns = []
        for i in range(population_size):
            campaign = self._generate_random_campaign(
                campaign_name=f"Campaign_Gen0_Var{i+1}",
                generation=0,
            )
            campaigns.append(campaign)

        logger.info(f"Generated {len(campaigns)} initial campaigns")
        return campaigns

    def _generate_random_campaign(
        self,
        campaign_name: str,
        generation: int = 0,
        parent_ids: Optional[List[str]] = None,
    ) -> CampaignParameters:
        """
        Generate a single random campaign configuration.

        Args:
            campaign_name: Name for the campaign
            generation: Generation number
            parent_ids: Parent campaign IDs (for genetic algorithm)

        Returns:
            CampaignParameters object
        """
        # Generate audience targeting
        audience = self._generate_audience()

        # Generate ad creative
        creative = self._generate_creative()

        # Generate bidding strategy
        bidding = self._generate_bidding()

        # Select placements
        placements = random.choice(self.parameter_space.placement_combinations)

        campaign = CampaignParameters(
            campaign_id=str(uuid.uuid4()),
            campaign_name=campaign_name,
            audience=audience,
            creative=creative,
            bidding=bidding,
            placements=placements,
            generation=generation,
            parent_ids=parent_ids or [],
        )

        return campaign

    def _generate_audience(self) -> AudienceTargeting:
        """Generate random audience targeting parameters."""
        # Select random targeting strategy
        if self.parameter_space.targeting_strategies:
            strategy = random.choice(self.parameter_space.targeting_strategies)

            age_min = strategy.get("age_min", 18)
            age_max = strategy.get("age_max", 65)
            genders = strategy.get("genders", ["all"])
            locations = strategy.get("locations", ["US"])
        else:
            age_min = random.randint(18, 45)
            age_max = random.randint(age_min + 10, 65)
            genders = random.choice([["all"], ["male"], ["female"], ["male", "female"]])
            locations = random.choice([["US"], ["US", "CA"], ["US", "GB", "AU"]])

        # Add some randomness to interests
        interests = [
            f"interest_{random.randint(1000, 9999)}" for _ in range(random.randint(0, 5))
        ]

        return AudienceTargeting(
            age_min=age_min,
            age_max=age_max,
            genders=genders,
            locations=locations,
            interests=interests,
        )

    def _generate_creative(self) -> AdCreative:
        """Generate random ad creative parameters."""
        # Select random creative format
        if self.parameter_space.creative_formats:
            format = random.choice(self.parameter_space.creative_formats)
        else:
            format = random.choice(["single_image", "carousel", "video"])

        # Generate placeholder content
        headlines = [
            "Limited Time Offer!",
            "Shop Now and Save",
            "Discover Amazing Deals",
            "Don't Miss Out",
            "Special Promotion",
        ]

        cta_options = [
            "SHOP_NOW",
            "LEARN_MORE",
            "SIGN_UP",
            "DOWNLOAD",
            "BOOK_NOW",
        ]

        return AdCreative(
            format=format,
            headline=random.choice(headlines),
            primary_text="Check out our amazing products and exclusive offers!",
            description="Limited time only. Shop now!",
            call_to_action=random.choice(cta_options),
            image_urls=["https://example.com/image1.jpg"],
        )

    def _generate_bidding(self) -> BiddingStrategy:
        """Generate random bidding strategy parameters."""
        # Select random bidding strategy
        if self.parameter_space.bidding_strategies:
            bid_strategy = random.choice(self.parameter_space.bidding_strategies)
        else:
            bid_strategy = random.choice([
                "LOWEST_COST_WITHOUT_CAP",
                "COST_CAP",
            ])

        # Generate daily budget within constraints
        min_budget = self.user_constraints.min_daily_budget or 10.0
        max_budget = self.user_constraints.max_daily_budget or 500.0

        daily_budget = random.uniform(min_budget, max_budget)

        # Set bid amount if using capped strategy
        bid_amount = None
        if "CAP" in bid_strategy:
            # Estimate reasonable bid based on historical CPC
            historical_cpc = self.user_constraints.historical_data.cpc
            bid_amount = historical_cpc * random.uniform(0.8, 1.5)

        optimization_goals = ["CONVERSIONS", "LINK_CLICKS", "LANDING_PAGE_VIEWS"]

        return BiddingStrategy(
            optimization_goal=random.choice(optimization_goals),
            bid_strategy=bid_strategy,
            bid_amount=bid_amount,
            daily_budget=round(daily_budget, 2),
        )

    def crossover(
        self,
        parent1: CampaignParameters,
        parent2: CampaignParameters,
        generation: int,
    ) -> CampaignParameters:
        """
        Create offspring campaign by combining two parent campaigns.

        Args:
            parent1: First parent campaign
            parent2: Second parent campaign
            generation: Generation number

        Returns:
            New campaign combining features from both parents
        """
        # Randomly inherit features from parents
        audience = parent1.audience if random.random() < 0.5 else parent2.audience
        creative = parent1.creative if random.random() < 0.5 else parent2.creative
        bidding = parent1.bidding if random.random() < 0.5 else parent2.bidding
        placements = parent1.placements if random.random() < 0.5 else parent2.placements

        # Blend budget (average of parents with noise)
        blended_budget = (parent1.bidding.daily_budget + parent2.bidding.daily_budget) / 2
        blended_budget *= random.uniform(0.9, 1.1)
        bidding.daily_budget = round(blended_budget, 2)

        campaign_name = f"Campaign_Gen{generation}_Cross_{uuid.uuid4().hex[:8]}"

        offspring = CampaignParameters(
            campaign_id=str(uuid.uuid4()),
            campaign_name=campaign_name,
            audience=audience,
            creative=creative,
            bidding=bidding,
            placements=placements,
            generation=generation,
            parent_ids=[parent1.campaign_id, parent2.campaign_id],
        )

        return offspring

    def mutate(
        self,
        campaign: CampaignParameters,
        mutation_rate: float = 0.2,
    ) -> CampaignParameters:
        """
        Apply random mutations to a campaign.

        Args:
            campaign: Campaign to mutate
            mutation_rate: Probability of mutating each parameter

        Returns:
            Mutated campaign
        """
        mutated = campaign.model_copy(deep=True)
        mutated.campaign_id = str(uuid.uuid4())
        mutated.campaign_name = f"{campaign.campaign_name}_Mutated"

        # Mutate audience
        if random.random() < mutation_rate:
            mutated.audience = self._mutate_audience(campaign.audience)

        # Mutate creative
        if random.random() < mutation_rate:
            mutated.creative = self._mutate_creative(campaign.creative)

        # Mutate bidding
        if random.random() < mutation_rate:
            mutated.bidding = self._mutate_bidding(campaign.bidding)

        # Mutate placements
        if random.random() < mutation_rate:
            mutated.placements = random.choice(
                self.parameter_space.placement_combinations
            )

        return mutated

    def _mutate_audience(self, audience: AudienceTargeting) -> AudienceTargeting:
        """Mutate audience targeting parameters."""
        mutated = audience.model_copy(deep=True)

        # Randomly adjust age range
        if random.random() < 0.5:
            shift = random.randint(-5, 5)
            mutated.age_min = max(18, min(60, mutated.age_min + shift))
            mutated.age_max = max(mutated.age_min + 5, min(65, mutated.age_max + shift))

        # Randomly change gender targeting
        if random.random() < 0.3:
            mutated.genders = random.choice([["all"], ["male"], ["female"]])

        return mutated

    def _mutate_creative(self, creative: AdCreative) -> AdCreative:
        """Mutate creative parameters."""
        mutated = creative.model_copy(deep=True)

        # Change format
        if random.random() < 0.3:
            mutated.format = random.choice(self.parameter_space.creative_formats)

        # Change CTA
        if random.random() < 0.3:
            cta_options = ["SHOP_NOW", "LEARN_MORE", "SIGN_UP", "DOWNLOAD"]
            mutated.call_to_action = random.choice(cta_options)

        return mutated

    def _mutate_bidding(self, bidding: BiddingStrategy) -> BiddingStrategy:
        """Mutate bidding strategy."""
        mutated = bidding.model_copy(deep=True)

        # Adjust budget
        if random.random() < 0.5:
            mutated.daily_budget *= random.uniform(0.8, 1.2)
            mutated.daily_budget = round(mutated.daily_budget, 2)

            # Ensure within constraints
            if self.user_constraints.min_daily_budget:
                mutated.daily_budget = max(
                    mutated.daily_budget, self.user_constraints.min_daily_budget
                )
            if self.user_constraints.max_daily_budget:
                mutated.daily_budget = min(
                    mutated.daily_budget, self.user_constraints.max_daily_budget
                )

        # Change bid strategy
        if random.random() < 0.2:
            mutated.bid_strategy = random.choice(self.parameter_space.bidding_strategies)

        return mutated

    def generate_from_winners(
        self,
        winning_campaigns: List[CampaignParameters],
        population_size: int,
        generation: int,
    ) -> List[CampaignParameters]:
        """
        Generate new population from winning campaigns.

        Args:
            winning_campaigns: Best performing campaigns
            population_size: Size of new population
            generation: Current generation number

        Returns:
            New population of campaigns
        """
        logger.info(
            f"Generating generation {generation} from {len(winning_campaigns)} winners..."
        )

        new_population = []

        # Keep elite (best performers)
        elite_count = min(5, len(winning_campaigns))
        for i in range(elite_count):
            elite = winning_campaigns[i].model_copy(deep=True)
            elite.campaign_id = str(uuid.uuid4())
            elite.generation = generation
            new_population.append(elite)

        # Generate rest through crossover and mutation
        while len(new_population) < population_size:
            # Select two random parents
            parent1 = random.choice(winning_campaigns)
            parent2 = random.choice(winning_campaigns)

            # Crossover
            offspring = self.crossover(parent1, parent2, generation)

            # Mutate with some probability
            if random.random() < 0.3:
                offspring = self.mutate(offspring)

            new_population.append(offspring)

        logger.info(f"Generated {len(new_population)} campaigns for generation {generation}")
        return new_population
