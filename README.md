# Instagram Automation Research Platform

A comprehensive Python platform for Instagram automation research, built for educational and defensive security analysis purposes. This project provides a structured framework for studying Instagram's API, automation patterns, and social media security research.

## 🔬 Project Overview

This platform enables researchers and developers to study Instagram automation techniques in a controlled, ethical manner. It includes session management, data extraction tools, and comprehensive testing frameworks for understanding social media automation behaviors.

## 📊 Current Status

**Version**: 0.3.0
**License**: MIT
**Python**: 3.8+

## 🏗️ Project Structure

```
instagram-automation-research/
├── core/                   # Core framework components
│   ├── automation_base.py  # Base automation classes
│   ├── session_manager.py  # Instagram session management
│   ├── content_generator.py# Content generation tools
│   ├── examples/           # Usage examples
│   ├── templates/          # HTML/CSS templates
│   └── testing/            # Testing frameworks
├── scripts/                # Automation scripts
│   ├── utilities/          # Core reusable tools (6 scripts)
│   ├── analysis/           # Research analysis tools (3 scripts)
│   └── experiments/        # Experimental scripts (40+ scripts)
├── sessions/               # Authentication session files
├── config/                 # Configuration files
│   ├── .env.example        # Environment template
│   └── requirements.txt    # Python dependencies
├── data/                   # Organized data storage
│   ├── analysis/           # Research results
│   ├── experiments/        # Experimental data
│   └── sessions/           # Session backups
├── docs/                   # Documentation
│   └── instagrapi/         # API documentation
├── reports/                # Generated reports
└── tests/                  # Test suites
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd instagram-automation-research

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r config/requirements.txt

# Install Playwright browsers
playwright install
```

### 2. Configuration

```bash
# Copy environment template
cp config/.env.example config/.env

# Edit configuration with your settings
# Note: Only use test accounts for research purposes
```

### 3. Basic Usage

```python
from core.session_manager import InstagramSessionManager
from core.automation_base import AutomationBase

# Initialize session manager
session_manager = InstagramSessionManager()

# Create session (uses test account)
client = session_manager.get_client()

# Your automation research code here
```

## 🛠️ Core Components

### Session Management
- **7-day rate limiting** protection
- **Session persistence** across runs
- **Bypass validation** methods for research
- **Multiple session support**

### Data Extraction Tools
- **Follower/Following analysis**
- **Direct message analysis**
- **Post interaction tracking**
- **Network relationship mapping**
- **Profile data extraction**

### Safety Features
- **Rate limiting** with configurable delays
- **Test account isolation**
- **Comprehensive error handling**
- **Instagram ToS compliance guidelines**
- **Privacy protection mechanisms**

## 📁 Key Script Categories

### Utility Scripts (`scripts/utilities/`)
Core reusable functionality:
- `create_session.py` - Session creation and initialization
- `dm_analyzer.py` - Direct message analysis tool
- `follower_activity_analyzer.py` - Follower activity tracking
- `follower_network_analysis.py` - Network relationship analysis
- `friend_analysis.py` - Comprehensive user analysis
- `setup.py` - Setup and configuration utility

### Analysis Scripts (`scripts/analysis/`)
Research-focused tools:
- `followers_latest_posts_smart.py` - Smart follower post analysis
- `my_followers_activity.py` - Personal follower activity analysis
- `my_followers_last_posts.py` - Last post tracking

### Experimental Scripts (`scripts/experiments/`)
40+ experimental automation scripts for various research purposes.

## 🔬 Research Applications

### Content Creator Research
- Automated post scheduling analysis
- Story template generation research
- Hashtag optimization studies
- Engagement analytics research

### Security Research
- Rate limiting behavior analysis
- Session management security
- API vulnerability research
- Automation detection studies

### Social Media Analysis
- User behavior pattern studies
- Network relationship analysis
- Trend analysis and prediction
- Algorithm interaction research

## 📊 Recent Updates (v0.3.0)

### Major Reorganization
- **Complete folder restructuring** for logical organization
- **Core framework** moved to dedicated `core/` directory
- **Script categorization** by purpose (utilities/analysis/experiments)
- **Centralized configuration** in `config/` folder

### Enhanced Session Management
- **Fixed validation bugs** in instagrapi library
- **Bypass methods** for reliable session loading
- **Rate limit detection** and proper handling
- **Session persistence** verified and working

### Data Organization
- **Structured data storage** by category
- **Report consolidation** in dedicated folder
- **Session file organization** with proper backup

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/performance/

# Run with coverage
python -m pytest --cov=core tests/
```

**Test Coverage**: 61 tests across unit, integration, and performance categories.

## ⚖️ Legal & Ethical Guidelines

### Important Disclaimers
- **Educational purposes only** - This project is for research and learning
- **Respect Instagram's ToS** - Always comply with platform terms of service
- **Use test accounts** - Never use production accounts for experimentation
- **Rate limiting respect** - Honor Instagram's rate limits and restrictions
- **Privacy protection** - Protect user data and respect privacy

### Responsible Usage
- Only use for defensive security research
- Respect user privacy and consent
- Follow academic research ethics
- Document and report findings responsibly
- Contribute back to the security community

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/research-improvement`)
3. **Make changes** with proper testing
4. **Commit changes** (`git commit -am 'Add research feature'`)
5. **Push to branch** (`git push origin feature/research-improvement`)
6. **Open Pull Request** with detailed description

### Development Setup
```bash
# Install development dependencies
pip install -r config/requirements.txt
pip install pytest pytest-cov black flake8

# Run code formatting
black core/ scripts/ tests/

# Run linting
flake8 core/ scripts/ tests/
```

## 📚 Documentation

- **API Reference**: Check `docs/instagrapi/` for complete API documentation
- **Examples**: See `core/examples/` for practical implementation examples
- **Configuration**: Review `config/.env.example` for all available settings
- **Changelog**: See `CHANGELOG.md` for detailed version history

## 🔧 Configuration Options

Key configuration parameters in `.env`:

```env
# Instagram credentials (test account only)
INSTAGRAM_USERNAME=your_test_account
INSTAGRAM_PASSWORD=your_test_password

# Session settings
SESSION_DURATION=604800  # 7 days in seconds
RATE_LIMIT_DELAY=60     # Seconds between requests

# Safety settings
MAX_REQUESTS_PER_HOUR=100
ENABLE_RATE_LIMITING=true
TEST_MODE=true
```

## 🐛 Troubleshooting

### Common Issues

**Session Validation Errors**
```python
# Use bypass method for research
client = session_manager.get_client_bypass_validation()
```

**Rate Limiting**
```python
# Increase delays in configuration
RATE_LIMIT_DELAY=120  # 2 minutes
```

**Import Errors**
```bash
# Ensure proper installation
pip install -r config/requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📈 Roadmap

### Planned Features
- **Advanced Analytics**: Machine learning-based analysis
- **Multi-Platform Support**: Extension to other social platforms
- **Cloud Deployment**: Docker containerization
- **API Gateway**: REST API for external integrations
- **Real-time Monitoring**: Live automation monitoring

### Research Areas
- **Algorithm Analysis**: Deep dive into recommendation algorithms
- **Engagement Optimization**: AI-powered content optimization
- **Trend Prediction**: ML-based trend forecasting
- **User Segmentation**: Advanced audience analysis

## 📞 Support

For questions, issues, or research collaboration:

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community help and research ideas
- **Documentation**: Check the `docs/` folder for guides
- **Email**: Contact maintainers for research collaboration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is intended for educational and research purposes only. Users are responsible for ensuring their use complies with Instagram's Terms of Service and applicable laws. The maintainers assume no responsibility for misuse of this software.

**Always use responsibly and ethically.**

---

**🔍 Research Focus**: Understanding social media automation for defensive security and educational purposes.