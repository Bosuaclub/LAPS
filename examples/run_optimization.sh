#!/bin/bash

# Example script to run FAO-Sim optimization

# Make sure virtual environment is activated
# source venv/bin/activate

# Set environment variables (or use .env file)
export OPENAI_API_KEY="your_openai_api_key_here"

# Create output directory
mkdir -p output

# Run optimization
python -m faosim.cli \
  --config examples/user_constraints_example.json \
  --knowledge-base examples/fb_ads_guide.txt \
  --output-dir ./output \
  --export-format both \
  --log-level INFO \
  --log-file logs/faosim.log

echo "Optimization complete! Check ./output directory for results."
