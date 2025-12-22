"""
Reusable Streamlit UI components for FAO-Sim.
"""

import streamlit as st
import tempfile
import time
from pathlib import Path
from typing import List, Optional
from loguru import logger

from faosim.core.schemas import (
    UserConstraints,
    HistoricalData,
    Goal,
    MetricType,
)
from faosim.core.orchestrator import FAOSimOrchestrator


def render_sidebar():
    """Render sidebar with app info and settings."""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/667eea/ffffff?text=FAO-Sim", width=150)
        st.markdown("---")

        st.markdown("### 📖 About")
        st.markdown("""
        **FAO-Sim** is an AI-powered system for autonomous Facebook Ads
        campaign optimization using:
        - 🧠 RAG Knowledge Base
        - 📊 TimesFM Forecasting
        - 🔄 Genetic Algorithm
        - 🎯 Multi-Objective Optimization
        """)

        st.markdown("---")

        st.markdown("### ⚙️ Settings")
        log_level = st.selectbox(
            "Log Level",
            ["INFO", "DEBUG", "WARNING", "ERROR"],
            index=0
        )

        use_existing_kb = st.checkbox(
            "Use Existing Knowledge Base",
            value=True,
            help="Use cached knowledge base if available"
        )

        st.markdown("---")

        st.markdown("### 🔗 Quick Links")
        st.markdown("[📚 Documentation](https://github.com)")
        st.markdown("[🐛 Report Issue](https://github.com)")
        st.markdown("[💡 Request Feature](https://github.com)")

        st.markdown("---")
        st.caption("FAO-Sim v0.1.0")


def render_config_form() -> Optional[UserConstraints]:
    """Render configuration input form."""
    st.markdown("### Product Information")

    col1, col2 = st.columns(2)
    with col1:
        product_cost = st.number_input(
            "Product Cost ($)",
            min_value=0.01,
            value=100.0,
            step=10.0,
            help="Cost of goods sold (COGS)"
        )
    with col2:
        selling_price = st.number_input(
            "Selling Price ($)",
            min_value=0.01,
            value=300.0,
            step=10.0,
            help="Product selling price"
        )

    st.markdown("---")
    st.markdown("### Historical Performance Data")

    col1, col2 = st.columns(2)
    with col1:
        cpm = st.number_input(
            "CPM ($)",
            min_value=0.01,
            value=15.0,
            step=1.0,
            help="Cost per 1000 impressions"
        )
        ctr = st.number_input(
            "CTR (%)",
            min_value=0.01,
            max_value=100.0,
            value=2.0,
            step=0.1,
            help="Click-through rate"
        ) / 100

    with col2:
        cpc = st.number_input(
            "CPC ($)",
            min_value=0.01,
            value=0.75,
            step=0.05,
            help="Cost per click"
        )
        cr = st.number_input(
            "Conversion Rate (%)",
            min_value=0.01,
            max_value=100.0,
            value=3.0,
            step=0.1,
            help="Conversion rate"
        ) / 100

    daily_budget = st.number_input(
        "Historical Daily Budget ($)",
        min_value=1.0,
        value=100.0,
        step=10.0,
        help="Average daily budget from historical data"
    )

    st.markdown("---")
    st.markdown("### Optimization Goal")

    col1, col2, col3 = st.columns(3)
    with col1:
        metric = st.selectbox(
            "Target Metric",
            ["ROAS", "ROI", "CPA", "CTR", "CR"],
            help="Metric to optimize for"
        )
    with col2:
        target_value = st.number_input(
            "Target Value",
            min_value=0.01,
            value=2.5 if metric in ["ROAS", "ROI"] else 0.05,
            step=0.1,
            help=f"Target value for {metric}"
        )
    with col3:
        tolerance = st.number_input(
            "Tolerance (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
            help="Acceptable deviation from target"
        ) / 100

    st.markdown("---")
    st.markdown("### Optimization Parameters")

    col1, col2 = st.columns(2)
    with col1:
        max_loops = st.slider(
            "Max Generations",
            min_value=1,
            max_value=50,
            value=10,
            help="Maximum number of optimization generations"
        )
        population_size = st.slider(
            "Population Size",
            min_value=5,
            max_value=100,
            value=20,
            help="Number of campaign variants per generation"
        )

    with col2:
        min_budget = st.number_input(
            "Min Daily Budget ($)",
            min_value=1.0,
            value=50.0,
            step=10.0
        )
        max_budget = st.number_input(
            "Max Daily Budget ($)",
            min_value=1.0,
            value=500.0,
            step=10.0
        )

    # Create UserConstraints object
    if st.button("💾 Save Configuration", type="primary"):
        try:
            historical_data = HistoricalData(
                cpm=cpm,
                ctr=ctr,
                cpc=cpc,
                cr=cr,
                daily_budget=daily_budget
            )

            goal = Goal(
                metric=metric,
                target_value=target_value,
                tolerance=tolerance
            )

            user_constraints = UserConstraints(
                product_cost=product_cost,
                selling_price=selling_price,
                historical_data=historical_data,
                goal=goal,
                max_loops=max_loops,
                population_size=population_size,
                min_daily_budget=min_budget,
                max_daily_budget=max_budget
            )

            return user_constraints

        except Exception as e:
            st.error(f"❌ Error creating configuration: {e}")
            return None

    return None


def render_knowledge_base_uploader() -> List[str]:
    """Render knowledge base file uploader."""
    st.markdown("""
    Upload advertising guides, best practices documents, or strategy PDFs.
    The system will extract optimization parameters from these documents.
    """)

    uploaded_files = st.file_uploader(
        "Upload Knowledge Base Documents",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        help="PDF, TXT, or DOCX files containing advertising best practices"
    )

    kb_file_paths = []

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

        # Save uploaded files temporarily
        for uploaded_file in uploaded_files:
            # Create temp file
            temp_dir = Path(tempfile.gettempdir()) / "faosim_kb"
            temp_dir.mkdir(exist_ok=True)

            temp_path = temp_dir / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            kb_file_paths.append(str(temp_path))

        # Show uploaded files
        with st.expander("📄 Uploaded Files"):
            for file in uploaded_files:
                st.markdown(f"- {file.name} ({file.size / 1024:.1f} KB)")

    else:
        # Offer to use example
        if st.checkbox("Use example knowledge base"):
            example_kb = Path("examples/fb_ads_guide.txt")
            if example_kb.exists():
                kb_file_paths = [str(example_kb)]
                st.info(f"✅ Using example: {example_kb.name}")

    return kb_file_paths


def render_optimization_controls(config_data: UserConstraints, kb_files: List[str]):
    """Render optimization execution controls."""

    col1, col2, col3 = st.columns(3)

    with col1:
        export_format = st.selectbox(
            "Export Format",
            ["JSON", "CSV", "Both"],
            help="Format for exporting results"
        )

    with col2:
        output_dir = st.text_input(
            "Output Directory",
            value="./output",
            help="Directory to save results"
        )

    with col3:
        st.write("")  # Spacer
        st.write("")  # Spacer

    # Run button
    if st.button("🚀 Start Optimization", type="primary", disabled=st.session_state.is_running):
        run_optimization(config_data, kb_files, output_dir, export_format.lower())

    # Status display
    if st.session_state.is_running:
        st.warning("⏳ Optimization in progress...")
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simulate progress (in real implementation, this would track actual progress)
        for i in range(100):
            time.sleep(0.1)
            progress_bar.progress(i + 1)
            status_text.text(f"Processing... {i + 1}%")


def run_optimization(
    config_data: UserConstraints,
    kb_files: List[str],
    output_dir: str,
    export_format: str
):
    """Run the optimization process."""
    st.session_state.is_running = True

    try:
        # Create progress containers
        progress_container = st.container()

        with progress_container:
            st.info("🔄 Initializing optimization...")

            # Initialize orchestrator
            orchestrator = FAOSimOrchestrator(
                user_constraints=config_data,
                knowledge_base_docs=kb_files if kb_files else None,
                use_existing_kb=True,
            )

            st.info("⚙️ Setting up modules...")
            orchestrator.setup()

            st.info("🚀 Running optimization loop...")

            # Run optimization
            result = orchestrator.run_optimization()

            st.info("💾 Exporting results...")

            # Export results
            if export_format in ["json", "both"]:
                orchestrator.export_results(result, output_dir, "json")
            if export_format in ["csv", "both"]:
                orchestrator.export_results(result, output_dir, "csv")

            # Save result to session state
            st.session_state.optimization_result = result
            st.session_state.is_running = False

            # Success message
            st.success(f"""
            ✅ **Optimization Complete!**

            - **Best ROAS**: {result.best_roas:.2f}
            - **Winning Campaigns**: {len(result.winning_campaigns)}
            - **Total Generations**: {result.total_loops}
            - **Execution Time**: {result.execution_time_seconds:.2f}s

            Results saved to: `{output_dir}`
            """)

            # Auto-switch to results tab (this would require additional logic)
            st.balloons()

    except Exception as e:
        st.session_state.is_running = False
        st.error(f"❌ Optimization failed: {e}")
        logger.exception("Optimization error")


def render_campaign_card(campaign, forecast, rank: int):
    """Render a campaign result card."""
    with st.container():
        st.markdown(f"""
        <div class="metric-card">
            <h4>#{rank} - {campaign.campaign_name}</h4>
            <p><strong>ROAS:</strong> {forecast.predicted_roas:.2f} |
               <strong>CPA:</strong> ${forecast.predicted_cpa:.2f} |
               <strong>CTR:</strong> {forecast.predicted_ctr * 100:.2f}%</p>
            <p><strong>Budget:</strong> ${campaign.bidding.daily_budget:.2f}/day |
               <strong>Placement:</strong> {', '.join(campaign.placements[:2])}</p>
        </div>
        """, unsafe_allow_html=True)
