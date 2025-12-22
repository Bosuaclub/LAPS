"""
Streamlit Web UI for FAO-Sim

A comprehensive web interface for Facebook Ads campaign optimization.
"""

import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime

from faosim.core.schemas import (
    UserConstraints,
    HistoricalData,
    Goal,
)
from faosim.core.orchestrator import FAOSimOrchestrator
from faosim.ui.components import (
    render_sidebar,
    render_config_form,
    render_knowledge_base_uploader,
    render_optimization_controls,
)
from faosim.ui.visualizations import (
    render_results_dashboard,
    render_convergence_chart,
    render_metrics_comparison,
)


# Page configuration
st.set_page_config(
    page_title="FAO-Sim - FB Ads Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "optimization_result" not in st.session_state:
        st.session_state.optimization_result = None
    if "is_running" not in st.session_state:
        st.session_state.is_running = False
    if "uploaded_kb_files" not in st.session_state:
        st.session_state.uploaded_kb_files = []
    if "config_data" not in st.session_state:
        st.session_state.config_data = None


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">🎯 FAO-Sim Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**FB Ads Autonomous Optimization & Simulation Lab**")
    st.markdown("---")

    # Sidebar
    render_sidebar()

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚙️ Configuration",
        "🚀 Run Optimization",
        "📊 Results",
        "📈 Analytics"
    ])

    # Tab 1: Configuration
    with tab1:
        st.header("Campaign Configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 Input Method")
            input_method = st.radio(
                "Choose how to provide configuration:",
                ["Form Input", "Upload JSON", "Load Example"],
                help="Select your preferred method to configure optimization parameters"
            )

            if input_method == "Form Input":
                user_constraints = render_config_form()
                if user_constraints:
                    st.session_state.config_data = user_constraints
                    st.success("✅ Configuration saved!")

            elif input_method == "Upload JSON":
                uploaded_file = st.file_uploader(
                    "Upload configuration JSON",
                    type=["json"],
                    help="Upload a JSON file with your campaign constraints"
                )
                if uploaded_file:
                    try:
                        config_data = json.load(uploaded_file)
                        user_constraints = UserConstraints(**config_data)
                        st.session_state.config_data = user_constraints
                        st.success("✅ Configuration loaded successfully!")
                        st.json(config_data)
                    except Exception as e:
                        st.error(f"❌ Error loading config: {e}")

            else:  # Load Example
                st.info("Loading example configuration...")
                example_path = Path("examples/user_constraints_example.json")
                if example_path.exists():
                    with open(example_path, "r") as f:
                        config_data = json.load(f)
                    user_constraints = UserConstraints(**config_data)
                    st.session_state.config_data = user_constraints
                    st.success("✅ Example configuration loaded!")
                    st.json(config_data)
                else:
                    st.warning("⚠️ Example file not found. Please use Form Input.")

        with col2:
            st.subheader("📚 Knowledge Base")
            uploaded_kb_files = render_knowledge_base_uploader()
            if uploaded_kb_files:
                st.session_state.uploaded_kb_files = uploaded_kb_files

    # Tab 2: Run Optimization
    with tab2:
        st.header("Run Campaign Optimization")

        if st.session_state.config_data is None:
            st.warning("⚠️ Please configure your campaign parameters in the Configuration tab first.")
        else:
            # Display current configuration summary
            st.subheader("📋 Configuration Summary")
            config = st.session_state.config_data

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Product Cost", f"${config.product_cost:.2f}")
            with col2:
                st.metric("Selling Price", f"${config.selling_price:.2f}")
            with col3:
                st.metric("Target ROAS", f"{config.goal.target_value:.2f}")
            with col4:
                st.metric("Max Loops", config.max_loops)

            st.markdown("---")

            # Optimization controls
            render_optimization_controls(
                config_data=st.session_state.config_data,
                kb_files=st.session_state.uploaded_kb_files
            )

    # Tab 3: Results
    with tab3:
        st.header("Optimization Results")

        if st.session_state.optimization_result is None:
            st.info("💡 Run an optimization to see results here.")
        else:
            render_results_dashboard(st.session_state.optimization_result)

    # Tab 4: Analytics
    with tab4:
        st.header("Performance Analytics")

        if st.session_state.optimization_result is None:
            st.info("💡 Run an optimization to see analytics here.")
        else:
            result = st.session_state.optimization_result

            # Convergence chart
            st.subheader("📈 Convergence History")
            render_convergence_chart(result.convergence_history)

            st.markdown("---")

            # Metrics comparison
            st.subheader("📊 Top Campaigns Comparison")
            if result.winning_campaigns:
                render_metrics_comparison(result.winning_campaigns[:10])


if __name__ == "__main__":
    main()
