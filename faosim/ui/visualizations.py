"""
Visualization components for FAO-Sim results.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import json

from faosim.core.schemas import OptimizationResult, ForecastResult


def render_results_dashboard(result: OptimizationResult):
    """Render complete results dashboard."""

    # Key metrics at the top
    st.subheader("🎯 Key Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Best ROAS",
            f"{result.best_roas:.2f}",
            help="Best Return on Ad Spend achieved"
        )

    with col2:
        st.metric(
            "Winning Campaigns",
            len(result.winning_campaigns),
            help="Number of campaigns meeting target criteria"
        )

    with col3:
        st.metric(
            "Total Generations",
            result.total_loops,
            help="Number of optimization generations completed"
        )

    with col4:
        st.metric(
            "Execution Time",
            f"{result.execution_time_seconds:.1f}s",
            help="Total optimization time"
        )

    st.markdown("---")

    # Best campaign details
    if result.best_campaign:
        st.subheader("🏆 Best Campaign Configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Campaign Details**")
            st.markdown(f"- **Name**: {result.best_campaign.campaign_name}")
            st.markdown(f"- **Daily Budget**: ${result.best_campaign.bidding.daily_budget:.2f}")
            st.markdown(f"- **Bid Strategy**: {result.best_campaign.bidding.bid_strategy}")
            st.markdown(f"- **Optimization Goal**: {result.best_campaign.bidding.optimization_goal}")

        with col2:
            st.markdown("**Targeting**")
            st.markdown(f"- **Age Range**: {result.best_campaign.audience.age_min}-{result.best_campaign.audience.age_max}")
            st.markdown(f"- **Genders**: {', '.join(result.best_campaign.audience.genders)}")
            st.markdown(f"- **Locations**: {', '.join(result.best_campaign.audience.locations)}")
            st.markdown(f"- **Placements**: {', '.join(result.best_campaign.placements)}")

    st.markdown("---")

    # Winning campaigns table
    st.subheader("✅ Top Winning Campaigns")

    if result.winning_campaigns:
        # Prepare data for table
        campaigns_data = []
        for i, forecast_result in enumerate(result.winning_campaigns[:20], 1):
            campaign = forecast_result.campaign_params
            forecast = forecast_result.forecast_metrics

            campaigns_data.append({
                "Rank": i,
                "Campaign": campaign.campaign_name,
                "ROAS": f"{forecast.predicted_roas:.2f}",
                "CPA": f"${forecast.predicted_cpa:.2f}",
                "CTR": f"{forecast.predicted_ctr * 100:.2f}%",
                "CR": f"{forecast.predicted_cr * 100:.2f}%",
                "Budget": f"${campaign.bidding.daily_budget:.2f}",
                "Score": f"{forecast_result.score:.4f}",
            })

        df = pd.DataFrame(campaigns_data)
        st.dataframe(df, use_container_width=True)

        # Download buttons
        render_download_buttons(result)

    else:
        st.warning("No winning campaigns found. Try adjusting your target criteria.")

    st.markdown("---")

    # Distribution charts
    st.subheader("📊 Performance Distribution")

    if result.winning_campaigns:
        col1, col2 = st.columns(2)

        with col1:
            # ROAS distribution
            roas_values = [w.forecast_metrics.predicted_roas for w in result.winning_campaigns]
            fig_roas = go.Figure(data=[go.Histogram(
                x=roas_values,
                nbinsx=20,
                marker_color='#667eea'
            )])
            fig_roas.update_layout(
                title="ROAS Distribution",
                xaxis_title="ROAS",
                yaxis_title="Count",
                showlegend=False
            )
            st.plotly_chart(fig_roas, use_container_width=True)

        with col2:
            # CPA distribution
            cpa_values = [w.forecast_metrics.predicted_cpa for w in result.winning_campaigns]
            fig_cpa = go.Figure(data=[go.Histogram(
                x=cpa_values,
                nbinsx=20,
                marker_color='#764ba2'
            )])
            fig_cpa.update_layout(
                title="CPA Distribution",
                xaxis_title="CPA ($)",
                yaxis_title="Count",
                showlegend=False
            )
            st.plotly_chart(fig_cpa, use_container_width=True)


def render_convergence_chart(convergence_history: List[Dict[str, Any]]):
    """Render convergence history chart."""

    if not convergence_history:
        st.warning("No convergence data available.")
        return

    # Prepare data
    df = pd.DataFrame(convergence_history)

    # Create dual-axis chart
    fig = go.Figure()

    # Best ROAS line
    fig.add_trace(go.Scatter(
        x=df['generation'],
        y=df['best_roas'],
        mode='lines+markers',
        name='Best ROAS',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))

    # Average ROAS line
    fig.add_trace(go.Scatter(
        x=df['generation'],
        y=df['avg_roas'],
        mode='lines+markers',
        name='Avg ROAS',
        line=dict(color='#764ba2', width=2, dash='dash'),
        marker=dict(size=6)
    ))

    # Winners bar (secondary y-axis)
    fig.add_trace(go.Bar(
        x=df['generation'],
        y=df['winners'],
        name='Winners',
        marker_color='rgba(102, 126, 234, 0.3)',
        yaxis='y2'
    ))

    # Update layout
    fig.update_layout(
        title="Optimization Convergence Over Generations",
        xaxis_title="Generation",
        yaxis_title="ROAS",
        yaxis2=dict(
            title="Number of Winners",
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Initial ROAS",
            f"{df['best_roas'].iloc[0]:.2f}",
            help="ROAS in first generation"
        )

    with col2:
        st.metric(
            "Final ROAS",
            f"{df['best_roas'].iloc[-1]:.2f}",
            delta=f"{df['best_roas'].iloc[-1] - df['best_roas'].iloc[0]:.2f}",
            help="ROAS in last generation"
        )

    with col3:
        st.metric(
            "Improvement",
            f"{((df['best_roas'].iloc[-1] / df['best_roas'].iloc[0]) - 1) * 100:.1f}%",
            help="Percentage improvement"
        )

    with col4:
        st.metric(
            "Total Winners",
            df['winners'].sum(),
            help="Total winning campaigns across all generations"
        )


def render_metrics_comparison(campaigns: List[ForecastResult]):
    """Render comparison of top campaigns."""

    # Prepare data
    data = []
    for i, result in enumerate(campaigns[:10], 1):
        campaign = result.campaign_params
        forecast = result.forecast_metrics

        data.append({
            "Campaign": f"#{i}",
            "ROAS": forecast.predicted_roas,
            "CPA": forecast.predicted_cpa,
            "CTR": forecast.predicted_ctr * 100,
            "CR": forecast.predicted_cr * 100,
            "Budget": campaign.bidding.daily_budget,
            "Score": result.score,
        })

    df = pd.DataFrame(data)

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["ROAS Comparison", "Budget vs Performance", "All Metrics"])

    with tab1:
        # ROAS bar chart
        fig = px.bar(
            df,
            x="Campaign",
            y="ROAS",
            color="ROAS",
            color_continuous_scale="Viridis",
            title="ROAS Comparison Across Top Campaigns"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Scatter: Budget vs ROAS
        fig = px.scatter(
            df,
            x="Budget",
            y="ROAS",
            size="Score",
            color="Campaign",
            title="Daily Budget vs ROAS",
            labels={"Budget": "Daily Budget ($)", "ROAS": "Return on Ad Spend"}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Radar chart for all metrics
        fig = go.Figure()

        for i, row in df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row['ROAS'], row['CTR'], row['CR'], row['Score'] * 10],
                theta=['ROAS', 'CTR (%)', 'CR (%)', 'Score (x10)'],
                fill='toself',
                name=row['Campaign']
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title="Multi-Metric Comparison",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)


def render_download_buttons(result: OptimizationResult):
    """Render download buttons for results."""
    col1, col2, col3 = st.columns(3)

    # Prepare data
    winning_data = []
    for w in result.winning_campaigns:
        winning_data.append({
            "campaign_id": w.campaign_params.campaign_id,
            "campaign_name": w.campaign_params.campaign_name,
            "predicted_roas": w.forecast_metrics.predicted_roas,
            "predicted_cpa": w.forecast_metrics.predicted_cpa,
            "predicted_ctr": w.forecast_metrics.predicted_ctr,
            "predicted_cr": w.forecast_metrics.predicted_cr,
            "daily_budget": w.campaign_params.bidding.daily_budget,
            "bid_strategy": w.campaign_params.bidding.bid_strategy,
            "score": w.score,
        })

    with col1:
        # Download JSON
        json_str = json.dumps(winning_data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="winning_campaigns.json",
            mime="application/json"
        )

    with col2:
        # Download CSV
        df = pd.DataFrame(winning_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="winning_campaigns.csv",
            mime="text/csv"
        )

    with col3:
        # Download full results
        full_data = result.model_dump()
        json_str = json.dumps(full_data, indent=2, default=str)
        st.download_button(
            label="📥 Download Full Results",
            data=json_str,
            file_name="optimization_results.json",
            mime="application/json"
        )


def render_campaign_detail_modal(campaign, forecast):
    """Render detailed view of a campaign."""
    with st.expander(f"📋 {campaign.campaign_name}"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Performance**")
            st.markdown(f"- ROAS: {forecast.predicted_roas:.2f}")
            st.markdown(f"- CPA: ${forecast.predicted_cpa:.2f}")
            st.markdown(f"- CTR: {forecast.predicted_ctr * 100:.2f}%")
            st.markdown(f"- CR: {forecast.predicted_cr * 100:.2f}%")

        with col2:
            st.markdown("**Targeting**")
            st.markdown(f"- Age: {campaign.audience.age_min}-{campaign.audience.age_max}")
            st.markdown(f"- Gender: {', '.join(campaign.audience.genders)}")
            st.markdown(f"- Locations: {', '.join(campaign.audience.locations[:3])}")

        with col3:
            st.markdown("**Budget & Bidding**")
            st.markdown(f"- Daily Budget: ${campaign.bidding.daily_budget:.2f}")
            st.markdown(f"- Bid Strategy: {campaign.bidding.bid_strategy}")
            st.markdown(f"- Goal: {campaign.bidding.optimization_goal}")

        st.markdown("**Placements**")
        st.markdown(f"{', '.join(campaign.placements)}")
