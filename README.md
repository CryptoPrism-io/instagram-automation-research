# Instagram Automation Research 🔬

> **A comprehensive testing and research platform for Instagram automation, content generation, and analytics**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Instagram API](https://img.shields.io/badge/Instagram-Private%20API-E4405F)](https://www.instagram.com/)
[![Version 0.3.0](https://img.shields.io/badge/version-0.3.0-green.svg)](CHANGELOG.md)

This repository serves as a dedicated testing and research environment for Instagram automation capabilities, completely separate from production systems. It provides safe experimentation, comprehensive documentation, and practical examples for various use cases.

## 🆕 What's New in v0.3.0 (September 21, 2025)

### 📁 **Complete Repository Reorganization**
- **Logical Folder Structure** - Everything organized by purpose and category
- **Core Framework** - Production-ready code in dedicated `core/` folder
- **Separated Experiments** - One-time scripts isolated from reusable utilities
- **Session Management** - Dedicated `sessions/` folder for session files
- **Clean Configuration** - All config files in `config/` folder

### 🔧 **Session Management Improvements**
- **Fixed Session Validation Bug** - Resolved false "session expired" errors
- **Bypass Method Added** - `get_client_bypass_validation()` for reliable session loading
- **Session Never Expires** - Confirmed session persistence works correctly
- **Rate Limit Handling** - Proper detection and handling of Instagram rate limits

### 🗂️ **New Folder Structure**
```
├── core/                   # Core framework and production code
├── sessions/              # Session files and authentication data
├── config/                # Configuration files (.env, requirements.txt)
├── scripts/
│   ├── utilities/         # Reusable utility scripts
│   ├── analysis/          # Analysis and research scripts
│   └── experiments/       # One-time experimental scripts
├── data/
│   ├── analysis/          # Analysis results and reports
│   ├── experiments/       # Experimental data and results
│   └── sessions/          # Session-related data
├── docs/                  # Documentation and guides
├── tests/                 # Test files and test data
└── reports/               # Generated reports and findings
```

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/your-username/instagram-automation-research.git
cd instagram-automation-research
pip install -r config/requirements.txt
```

### 2. Configuration
```bash
# Copy and configure environment variables
cp config/.env.example config/.env
# Edit config/.env with your Instagram credentials
```

### 3. Create Session
```python
# Run session creation utility
python scripts/utilities/create_session.py
```

### 4. Basic Usage
```python
from core.core.session_manager import InstagramSessionManager
from core.core.automation_base import AutomationBase

# Initialize session manager
session_manager = InstagramSessionManager(session_file="sessions/instagram_session.json")
client = session_manager.get_client_bypass_validation()

# Use automation features
automation = AutomationBase(client)
```

## 📊 Features & Capabilities

### 🔐 **Session Management**
- **Persistent Sessions** - Maintain authentication across restarts
- **Rate Limiting Protection** - 7-day intervals prevent account restrictions
- **Session Validation Bypass** - Reliable session loading without false expiration errors
- **Multiple Session Support** - Manage multiple accounts safely

### 🔍 **Analysis & Research**
- **Follower Network Analysis** - Extract and analyze follower/following relationships
- **DM Conversation Analysis** - Analyze direct message patterns and insights
- **Profile Deep Analysis** - Comprehensive user data extraction
- **Activity Monitoring** - Track user posting patterns and engagement

### 🛠️ **Utility Scripts**
Located in `scripts/utilities/`:
- `create_session.py` - Session creation and initialization
- `dm_analyzer.py` - Direct message analysis tool
- `follower_activity_analyzer.py` - Follower activity tracking
- `follower_network_analysis.py` - Network relationship analysis
- `friend_analysis.py` - Comprehensive friend/follower analysis

### 🔬 **Analysis Scripts**
Located in `scripts/analysis/`:
- `followers_latest_posts_smart.py` - Smart follower post analysis
- `my_followers_activity.py` - Personal follower activity analysis
- `my_followers_last_posts.py` - Last post tracking for followers

### 🧪 **Experimental Scripts**
Located in `scripts/experiments/`:
- Various unfollow automation scripts
- Session testing and validation tools
- User-specific analysis experiments
- API method testing utilities

## 📁 File Organization

### Core Framework (`core/`)
```
core/
├── __init__.py              # Package initialization
├── automation_base.py       # Base automation functionality
├── content_generator.py     # Content creation utilities
├── session_manager.py       # Session management (enhanced with bypass method)
└── examples/               # Example implementations
```

### Configuration (`config/`)
```
config/
├── .env                    # Environment variables (not in git)
├── .env.example           # Environment template
└── requirements.txt       # Python dependencies
```

### Sessions (`sessions/`)
```
sessions/
└── instagram_session.json # Active session file
```

### Data Organization (`data/`)
```
data/
├── analysis/              # Analysis results and insights
├── experiments/           # Experimental data and results
└── sessions/             # Session-related data and backups
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Comprehensive API tests
python tests/test_instagrapi_comprehensive.py
```

### Test Results
- **61 Total Tests** across multiple categories
- **Unit Tests** - Core functionality validation
- **Integration Tests** - Real API interaction testing
- **Performance Tests** - Rate limiting and efficiency testing

## 🛡️ Security & Best Practices

### Account Protection
- **7-Day Rate Limiting** - Prevents account restrictions
- **Session Persistence** - Reduces login frequency
- **Error Handling** - Graceful handling of API restrictions
- **Backup Systems** - Multiple extraction methods for reliability

### Configuration Security
- **Environment Variables** - Credentials stored securely
- **Session Files** - Isolated in dedicated folder
- **Git Ignore** - Sensitive files excluded from version control

## 📚 Documentation

### Core Documentation
- [API Documentation](docs/instagrapi/) - Comprehensive API guides
- [Best Practices](docs/instagrapi/best-practices.md) - Security and efficiency guidelines
- [Test Reports](reports/) - Detailed testing and analysis reports

### Generated Reports
Located in `reports/`:
- `COMPREHENSIVE_TEST_REPORT.md` - Complete testing documentation
- `INSTAGRAPI_TEST_REPORT.md` - API functionality validation
- `CLAUDE.md` - Development and research notes

## 🔄 Recent Changes & Improvements

### Session Management Fixes
- **Resolved "Session Expired" Bug** - Fixed false expiration errors in instagrapi
- **Added Bypass Method** - `get_client_bypass_validation()` for reliable session access
- **Confirmed Session Persistence** - Sessions work correctly and don't actually expire

### Repository Reorganization
- **Logical Structure** - Files organized by purpose and usage frequency
- **Core vs Experimental** - Clear separation between production code and experiments
- **Configuration Centralization** - All config files in dedicated folder
- **Session Isolation** - Session files in dedicated, secure location

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make changes** following the established folder structure
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open Pull Request**

## ⚠️ Disclaimer

This project is for **research and educational purposes only**. Always comply with Instagram's Terms of Service and applicable laws. Use responsibly and respect rate limits to avoid account restrictions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [instagrapi](https://github.com/adw0rd/instagrapi) - Instagram Private API wrapper
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api) - Official Instagram API

---

**Version 0.3.0** - Repository reorganized and session management enhanced - September 21, 2025