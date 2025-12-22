# 🎨 FAO-Sim Web UI

Beautiful, interactive web interface for Facebook Ads campaign optimization.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 Interactive Dashboard
- **4 Main Tabs**: Configuration, Optimization, Results, Analytics
- **Real-time Progress**: Watch optimization happen live
- **Beautiful Charts**: Powered by Plotly for interactive visualizations
- **Responsive Design**: Works on desktop and tablets

### 📊 Visualization
- **Convergence Charts**: Track ROAS improvement over generations
- **Performance Distributions**: Histogram analysis of metrics
- **Campaign Comparisons**: Side-by-side analysis of top performers
- **Multi-metric Radar**: Compare campaigns across all dimensions

### 💾 Export & Download
- **Multiple Formats**: JSON, CSV, or both
- **One-Click Download**: Get results instantly
- **Full Results Export**: Complete optimization data
- **Ready for Ads Manager**: Import directly to Facebook

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Launch Web UI

```bash
python run_ui.py
```

Or directly:
```bash
streamlit run faosim/ui/app.py
```

### 4. Open Browser

The app will automatically open at: `http://localhost:8501`

## 📖 Quick Tutorial

### Step 1: Configure Campaign
1. Go to **Configuration** tab
2. Choose input method:
   - **Form Input**: Fill in the form (easiest)
   - **Upload JSON**: Use existing config
   - **Load Example**: Start with sample data
3. Enter your product costs and prices
4. Input historical performance data
5. Set your optimization goal (e.g., ROAS 2.5)
6. Configure parameters (generations, population size)
7. Click **Save Configuration**

### Step 2: Add Knowledge Base
1. Upload advertising guides (PDF/TXT/DOCX)
2. Or check "Use example knowledge base"
3. System extracts 100+ optimization parameters

### Step 3: Run Optimization
1. Go to **Run Optimization** tab
2. Review your configuration summary
3. Choose export format
4. Set output directory
5. Click **Start Optimization**
6. Watch real-time progress

### Step 4: View Results
1. Go to **Results** tab
2. See key metrics at a glance
3. Review best campaign details
4. Browse winning campaigns table
5. Download results (JSON/CSV)

### Step 5: Analyze Performance
1. Go to **Analytics** tab
2. View convergence over generations
3. Compare top campaigns
4. Analyze performance distributions

## 🎨 UI Components

### Configuration Tab
```
┌─────────────────────────────────────┐
│  Input Method Selection             │
│  ┌───────┬───────┬───────┐         │
│  │ Form  │ JSON  │Example│         │
│  └───────┴───────┴───────┘         │
│                                     │
│  Product Information                │
│  ├─ Product Cost: $___             │
│  └─ Selling Price: $___            │
│                                     │
│  Historical Performance             │
│  ├─ CPM, CTR, CPC, CR              │
│  └─ Daily Budget                   │
│                                     │
│  Optimization Goal                  │
│  ├─ Metric (ROAS/ROI/CPA)          │
│  └─ Target Value                   │
│                                     │
│  [Save Configuration]               │
└─────────────────────────────────────┘
```

### Results Tab
```
┌─────────────────────────────────────┐
│  📊 Key Metrics                     │
│  ┌────┐┌────┐┌────┐┌────┐         │
│  │ROAS││Wins││Gens││Time│         │
│  └────┘└────┘└────┘└────┘         │
│                                     │
│  🏆 Best Campaign                   │
│  ├─ Configuration Details           │
│  └─ Performance Forecast            │
│                                     │
│  ✅ Winning Campaigns               │
│  ┌──────────────────────────┐      │
│  │ Rank │ Name │ ROAS │ CPA │      │
│  ├──────┼──────┼──────┼─────┤      │
│  │  1   │ ... │ 3.21 │ $85 │      │
│  └──────────────────────────┘      │
│                                     │
│  [Download JSON] [Download CSV]     │
└─────────────────────────────────────┘
```

### Analytics Tab
```
┌─────────────────────────────────────┐
│  📈 Convergence Chart               │
│  ┌─────────────────────────┐        │
│  │     Best ROAS ──────    │        │
│  │     Avg ROAS ------     │        │
│  │     Winners ████████    │        │
│  └─────────────────────────┘        │
│                                     │
│  📊 Campaign Comparison             │
│  ┌───────┬──────────┬──────┐       │
│  │ ROAS  │ Budget   │ All  │       │
│  │ Chart │ vs Perf  │Metrics│      │
│  └───────┴──────────┴──────┘       │
└─────────────────────────────────────┘
```

## 🎯 Use Cases

### E-commerce Store
Perfect for optimizing product ads:
- Input product COGS and price
- Historical campaign data
- Target ROAS (e.g., 3.0)
- Get winning campaign configs
- Scale best performers

### Lead Generation
Optimize for cost per lead:
- Set lead value
- Target CPA
- Historical conversion data
- Focus on high CR campaigns
- Export to Ads Manager

### Brand Awareness
Maximize reach efficiently:
- Target low CPM
- High CTR campaigns
- Broad audience testing
- Placement optimization

## 🔧 Customization

### Theming

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Port Configuration

Change default port (8501):
```bash
streamlit run faosim/ui/app.py --server.port=8502
```

### Server Settings

For remote access:
```bash
streamlit run faosim/ui/app.py \
  --server.address=0.0.0.0 \
  --server.port=8501
```

## 📊 Example Workflow

### Complete Optimization Flow

```bash
# 1. Launch UI
python run_ui.py

# 2. In Browser:
#    - Configure: Product $100, Selling $300
#    - Goal: ROAS 2.5
#    - Upload knowledge base
#    - Save config

# 3. Run Optimization:
#    - 10 generations
#    - 20 population size
#    - Start optimization
#    - Wait ~2 minutes

# 4. View Results:
#    - Best ROAS: 3.21
#    - 15 winning campaigns
#    - Download JSON

# 5. Import to Facebook:
#    - Load JSON in Ads Manager
#    - Launch campaigns
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run faosim/ui/app.py --server.port=8502
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Slow Performance
- Reduce population size to 10-15
- Decrease max generations to 5-7
- Use existing knowledge base
- Close other browser tabs

### Charts Not Loading
- Update Plotly: `pip install plotly --upgrade`
- Clear browser cache
- Try different browser (Chrome recommended)

## 📚 Documentation

- **Full Guide**: [docs/WEB_UI_GUIDE.md](docs/WEB_UI_GUIDE.md)
- **Main README**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

## 🎓 Learning Resources

### Video Tutorials (Coming Soon)
- [ ] Quick Start (5 min)
- [ ] Configuration Deep Dive (10 min)
- [ ] Understanding Results (10 min)
- [ ] Advanced Analytics (15 min)

### Sample Datasets
- `examples/user_constraints_example.json` - Basic config
- `examples/fb_ads_guide.txt` - Knowledge base
- `examples/quick_start.py` - Programmatic usage

## 🤝 Contributing

We welcome UI improvements!

**Ideas**:
- Additional chart types
- Dark mode theme
- Mobile optimization
- Campaign comparison tool
- A/B testing interface
- Multi-account support

## 📝 Changelog

### Version 1.0.0 (2025-12-22)
- ✨ Initial release
- 🎨 4-tab interface
- 📊 Plotly visualizations
- 💾 JSON/CSV export
- 📈 Real-time progress
- 🎯 Interactive configuration

## 🔗 Links

- **GitHub**: [Repository](https://github.com)
- **Documentation**: [Full Docs](docs/)
- **Issues**: [Report Bug](https://github.com/issues)
- **Discussions**: [Community](https://github.com/discussions)

## ⭐ Show Your Support

If you find FAO-Sim useful, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🎨 Contribute to UI

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

**Built with ❤️ using Streamlit and Plotly**

**Version**: 1.0.0
**Last Updated**: 2025-12-22
