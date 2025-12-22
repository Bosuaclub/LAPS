# FAO-Sim Web UI Guide

## 🚀 Quick Start

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Launch Web UI**:
```bash
python run_ui.py
```

Or directly with Streamlit:
```bash
streamlit run faosim/ui/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📖 User Interface Overview

### Main Dashboard

The FAO-Sim Web UI consists of 4 main tabs:

#### 1. ⚙️ Configuration Tab

Configure your campaign optimization parameters using three methods:

**A. Form Input** (Recommended for beginners)
- Fill in product cost and selling price
- Enter historical performance data (CPM, CTR, CPC, CR)
- Set optimization goals (ROAS, ROI, CPA, etc.)
- Configure optimization parameters (generations, population size)
- Set budget constraints

**B. Upload JSON**
- Upload a pre-configured JSON file
- Useful for repeating optimizations
- See `examples/user_constraints_example.json` for format

**C. Load Example**
- Loads example configuration automatically
- Great for testing the system

**Knowledge Base Upload**:
- Upload PDF, TXT, or DOCX files containing advertising guides
- System extracts best practices and strategies
- Or use the example knowledge base included

#### 2. 🚀 Run Optimization Tab

Execute the optimization process:

1. **Configuration Summary**: Review your settings before running
2. **Export Options**: Choose JSON, CSV, or both
3. **Output Directory**: Specify where to save results
4. **Start Button**: Click to begin optimization
5. **Progress Tracking**: Real-time progress updates

The optimization process:
- Initializes RAG knowledge base
- Generates initial campaign population
- Runs genetic algorithm optimization
- Evaluates campaigns against goals
- Exports winning campaigns

#### 3. 📊 Results Tab

View optimization results:

**Key Metrics**:
- Best ROAS achieved
- Number of winning campaigns
- Total generations completed
- Execution time

**Best Campaign Details**:
- Complete configuration of top performer
- Targeting parameters
- Budget and bidding strategy
- Placements

**Winning Campaigns Table**:
- Top 20 campaigns ranked by performance
- Sortable and filterable
- Download options (JSON, CSV)

**Performance Distribution**:
- ROAS distribution histogram
- CPA distribution histogram
- Visual analysis of results

#### 4. 📈 Analytics Tab

In-depth performance analysis:

**Convergence Chart**:
- Best ROAS over generations
- Average ROAS trend
- Number of winners per generation
- Visual convergence tracking

**Convergence Statistics**:
- Initial vs Final ROAS
- Percentage improvement
- Total winners across generations

**Top Campaigns Comparison**:
- **ROAS Comparison**: Bar chart of top campaigns
- **Budget vs Performance**: Scatter plot showing relationship
- **All Metrics**: Radar chart for multi-dimensional comparison

## 📝 Step-by-Step Workflow

### First Time Setup

1. **Launch the app**:
   ```bash
   python run_ui.py
   ```

2. **Navigate to Configuration tab**

3. **Fill in your data**:
   - Product Cost: Your COGS (e.g., $100)
   - Selling Price: Your product price (e.g., $300)
   - Historical CPM: Your average CPM (e.g., $15)
   - Historical CTR: Your average CTR (e.g., 2%)
   - Historical CPC: Your average CPC (e.g., $0.75)
   - Historical CR: Your conversion rate (e.g., 3%)

4. **Set your goal**:
   - Target Metric: ROAS (recommended)
   - Target Value: 2.5 (means $2.50 revenue per $1 ad spend)
   - Tolerance: 10% (acceptable deviation)

5. **Configure optimization**:
   - Max Generations: 10 (balance speed vs quality)
   - Population Size: 20 (number of variants per generation)
   - Budget Range: Min $50, Max $500

6. **Upload knowledge base** (optional but recommended):
   - Click "Use example knowledge base" checkbox
   - Or upload your own advertising guides

7. **Save configuration**

### Running Optimization

1. **Go to Run Optimization tab**

2. **Review summary** of your configuration

3. **Choose export format**:
   - JSON: For programmatic access
   - CSV: For Excel/spreadsheet analysis
   - Both: Get both formats

4. **Click "Start Optimization"**

5. **Wait for completion** (typically 1-5 minutes)

6. **View success message** with key results

### Analyzing Results

1. **Go to Results tab** to see:
   - Key performance metrics
   - Best campaign configuration
   - Top winning campaigns table
   - Performance distributions

2. **Download results**:
   - Click "Download JSON" for full data
   - Click "Download CSV" for spreadsheet
   - Click "Download Full Results" for complete output

3. **Go to Analytics tab** for:
   - Convergence visualization
   - Campaign comparisons
   - Performance trends

## 🎨 UI Features

### Sidebar

- **About Section**: Quick overview of FAO-Sim
- **Settings**:
  - Log Level: Control verbosity
  - Use Existing KB: Cache knowledge base
- **Quick Links**: Documentation and support

### Interactive Elements

- **Collapsible Sections**: Click to expand/collapse
- **Tooltips**: Hover over (?) icons for help
- **Real-time Updates**: Progress tracking during optimization
- **Responsive Design**: Works on desktop and tablet

### Visualizations

All charts are interactive:
- **Hover**: See detailed values
- **Zoom**: Click and drag to zoom
- **Pan**: Shift+drag to pan
- **Download**: Click camera icon to save as PNG

## 📊 Understanding the Metrics

### Performance Metrics

**ROAS (Return on Ad Spend)**:
- Revenue / Ad Spend
- Example: ROAS of 2.5 = $2.50 revenue per $1 spent
- Target: 2.0+ is good, 3.0+ is excellent

**CPA (Cost Per Acquisition)**:
- Cost to acquire one customer
- Lower is better
- Should be less than your profit margin

**CTR (Click-Through Rate)**:
- Clicks / Impressions
- Measures ad engagement
- Industry average: 1-2%

**CR (Conversion Rate)**:
- Conversions / Clicks
- Measures landing page effectiveness
- Industry average: 2-5%

### Optimization Metrics

**Score**:
- Overall fitness score combining multiple factors
- Higher is better
- Used for ranking campaigns

**Generation**:
- Iteration number in genetic algorithm
- Each generation improves on previous
- Convergence typically in 5-15 generations

**Winners**:
- Campaigns meeting target criteria
- More winners = better optimization

## 🔧 Troubleshooting

### Common Issues

**"No winning campaigns found"**:
- Your target might be too aggressive
- Lower target value or increase tolerance
- Check historical data accuracy

**"Optimization taking too long"**:
- Reduce max generations (try 5-7)
- Reduce population size (try 10-15)
- Use simpler knowledge base

**"Error loading configuration"**:
- Check all required fields are filled
- Ensure selling price > product cost
- Verify percentages are 0-100 (not 0-1)

**"Knowledge base error"**:
- Check file format (PDF, TXT, DOCX)
- Ensure files aren't corrupted
- Try using example knowledge base first

### Performance Tips

**For faster optimization**:
- Use existing knowledge base (check the box)
- Reduce population size to 10-15
- Reduce max generations to 5-7
- Use smaller knowledge base files

**For better results**:
- Provide accurate historical data
- Use comprehensive knowledge base
- Increase population size to 30-50
- Increase max generations to 15-20
- Run multiple optimizations with different seeds

## 📁 Output Files

After optimization, find results in your output directory:

```
output/
├── optimization_results.json      # Complete results
├── winning_campaigns.json         # Top campaigns (JSON)
├── winning_campaigns.csv          # Top campaigns (CSV)
└── convergence_history.json       # Generation-by-generation data
```

### Using Results

**Import to Facebook Ads Manager**:
1. Download winning_campaigns.json
2. Use Facebook's bulk import tool
3. Adjust any platform-specific settings
4. Review before launching

**Spreadsheet Analysis**:
1. Download winning_campaigns.csv
2. Open in Excel/Google Sheets
3. Create pivot tables
4. Analyze performance patterns

## 🎯 Best Practices

### Data Input

✅ **Do**:
- Use recent historical data (last 30-90 days)
- Verify data accuracy before inputting
- Include seasonal adjustments if needed
- Document your data sources

❌ **Don't**:
- Use very old historical data (>6 months)
- Mix data from different product categories
- Include outlier campaigns in averages

### Optimization Settings

✅ **Do**:
- Start with default settings (10 generations, 20 population)
- Adjust target based on industry benchmarks
- Use 10-20% tolerance for flexibility
- Test with example first

❌ **Don't**:
- Set unrealistic targets (ROAS > 10.0)
- Use population size < 10 or > 100
- Set tolerance too tight (< 5%)

### Knowledge Base

✅ **Do**:
- Use comprehensive advertising guides
- Include multiple source documents
- Update knowledge base regularly
- Use industry-specific materials

❌ **Don't**:
- Upload unrelated documents
- Use very old strategies (>2 years)
- Mix B2B and B2C strategies

## 🆘 Getting Help

**In-App Help**:
- Hover over (?) icons for tooltips
- Check sidebar for quick links
- View example configurations

**Documentation**:
- README.md: Project overview
- ARCHITECTURE.md: Technical details
- This guide: UI-specific help

**Support**:
- GitHub Issues: Report bugs
- Discussions: Ask questions
- Examples: Learn by doing

## 🚀 Advanced Usage

### Batch Processing

Run multiple optimizations with different parameters:
1. Save first configuration
2. Run optimization
3. Download results
4. Modify configuration
5. Run again
6. Compare results

### Custom Knowledge Base

Create your own knowledge base:
1. Document your successful campaigns
2. Include targeting strategies
3. Add creative best practices
4. Save as PDF or TXT
5. Upload to FAO-Sim

### API Integration

For programmatic access:
```python
from faosim.core.orchestrator import FAOSimOrchestrator

# Use results from UI
orchestrator = FAOSimOrchestrator(...)
result = orchestrator.run_optimization()
```

## 📱 Mobile Access

The UI is responsive but works best on:
- Desktop: Full experience
- Tablet: Most features work
- Mobile: View results only (not recommended for configuration)

## 🎓 Tutorial Videos

Coming soon:
- Getting Started (5 min)
- First Optimization (10 min)
- Advanced Features (15 min)
- Case Studies (20 min)

## 📊 Sample Workflows

### E-commerce Store

1. Input product cost: $50
2. Selling price: $150
3. Target ROAS: 3.0
4. Historical data from last month
5. Upload e-commerce best practices
6. Run with 15 generations
7. Export top 5 campaigns
8. Test in Facebook Ads Manager

### Lead Generation

1. Input lead value: $100
2. Target CPA: $25
3. Historical conversion data
4. Upload lead gen guides
5. Run with 20 population size
6. Focus on campaigns with best CR
7. Scale winning campaigns

---

**Need more help?** Check our [GitHub repository](https://github.com) or [open an issue](https://github.com/issues).

**Version**: 1.0.0
**Last Updated**: 2025-12-22
