# Pryvon Temp Mail 🚀

> **Professional-Grade Temporary Email Management Solution**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/inquilineorg/temp-mail-client)

---

<div align="center">

**Enterprise-Ready Temporary Email Management with Professional UI**

*Built for developers, teams, and production environments*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🔧 Features](#-features) • [📱 Demo](#-demo)

</div>

---

## ✨ Overview

**Pryvon Temp Mail** is a sophisticated, production-ready console application that transforms the basic mail.tm API wrapper into an enterprise-grade temporary email management solution. Built with modern Python practices, it provides a professional interface for managing temporary email accounts with enterprise-level reliability.

### 🎯 **Key Benefits**

- **🏢 Production Ready** - Built for enterprise use with comprehensive error handling
- **🎨 Professional UI** - Rich console interface with clean, modern design
- **⚡ High Performance** - Intelligent caching and optimized API interactions
- **🔒 Enterprise Security** - Secure authentication and data protection
- **📱 Dual Interface** - Both interactive console and CLI for automation

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip package manager
- **Internet connection** for mail.tm API access

### Installation

```bash
# Clone the repository
git clone https://github.com/inquilineorg/temp-mail-client.git
cd temp-mail-client

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### First Run

```bash
# Start the interactive console
python console_app.py

# Or use the CLI for quick operations
python cli.py --help
```

---

## 🎮 Demo

### Interactive Console
![Console Demo](https://via.placeholder.com/800x400/2d3748/ffffff?text=Pryvon+Temp+Mail+Console)

### Command Line Interface
```bash
# Create account with auto-login
python cli.py create --auto-login

# Check messages
python cli.py list --limit 10

# View statistics
python cli.py stats
```

---

## 🔧 Features

### 🏗️ **Core Architecture**
| Feature | Description | Status |
|---------|-------------|---------|
| **Modular Design** | Clean separation of concerns with dedicated modules | ✅ Complete |
| **Configuration Management** | Persistent settings with runtime updates | ✅ Complete |
| **Professional Logging** | Structured logging with rotation and multiple outputs | ✅ Complete |
| **Intelligent Caching** | TTL-based caching with automatic cleanup | ✅ Complete |

### 📧 **Email Management**
| Feature | Description | Status |
|---------|-------------|---------|
| **Account Creation** | Automated temporary email account generation | ✅ Complete |
| **Secure Authentication** | Bearer token-based login with session management | ✅ Complete |
| **Message Retrieval** | Intelligent mailbox management with caching | ✅ Complete |
| **Content Viewing** | Rich message display with HTML/text support | ✅ Complete |

### 🎨 **User Experience**
| Feature | Description | Status |
|---------|-------------|---------|
| **Rich Console UI** | Beautiful tables, panels, and progress indicators | ✅ Complete |
| **Screen Management** | Professional console clearing and transitions | ✅ Complete |
| **Error Handling** | Comprehensive error recovery with user guidance | ✅ Complete |
| **Responsive Design** | Optimized for various terminal sizes | ✅ Complete |

---

## 📖 Documentation

### Interactive Console

The main application provides a full-featured interactive experience:

```bash
python console_app.py
```

**Main Menu Options:**
- **📧 Check Mailbox** - View all messages with rich formatting
- **🔄 Refresh Mailbox** - Get latest messages with real-time updates
- **📝 View Message** - Read full message content with attachments
- **👁️ Mark as Read** - Manage message read status
- **🗑️ Delete Message** - Remove unwanted messages
- **📊 Account Statistics** - Monitor quota usage and performance
- **⚙️ Settings** - Configure application preferences
- **❌ Account Management** - Delete accounts with safeguards

### Command Line Interface

For automation and scripting:

```bash
# Account Management
python cli.py create --auto-login          # Create new account
python cli.py login user@domain.com        # Login to existing account
python cli.py logout                       # Secure logout

# Message Operations
python cli.py list --limit 20              # List recent messages
python cli.py list --unread-only           # Show unread messages
python cli.py view <message_id>            # View specific message
python cli.py mark_read <message_id>       # Mark message as read
python cli.py delete <message_id>          # Delete message

# System Operations
python cli.py refresh                       # Refresh mailbox
python cli.py stats                         # Show account statistics
python cli.py domains                       # List available domains
python cli.py clear-cache                   # Clear cached data
```

---

## 🏗️ Architecture

### Module Structure
```
pryvon-temp-mail/
├── 📁 Core Modules
│   ├── mailtm_client.py      # Enhanced API client
│   ├── console_app.py        # Interactive console
│   └── cli.py               # Command-line interface
├── 📁 Infrastructure
│   ├── config.py             # Configuration management
│   ├── logger.py             # Professional logging
│   ├── cache.py              # Intelligent caching
│   └── exceptions.py         # Custom exception classes
├── 📁 Documentation
│   ├── README.md             # This file
│   └── example_usage.py      # Usage examples
└── 📁 Configuration
    ├── requirements.txt      # Dependencies
    └── .gitignore           # Git exclusions
```

### Technology Stack
- **🐍 Python 3.8+** - Core runtime
- **📡 Requests** - HTTP client with retry logic
- **🎨 Rich** - Beautiful terminal UI components
- **⚙️ Click** - Professional CLI framework
- **💾 JSON** - Configuration and cache storage

---

## ⚙️ Configuration

### Environment Variables
```bash
export PRYVON_LOG_LEVEL=DEBUG
export PRYVON_CACHE_ENABLED=false
export PRYVON_API_TIMEOUT=60
```

### Configuration File
```json
{
  "api_base_url": "https://api.mail.tm",
  "api_timeout": 30,
  "max_retries": 3,
  "refresh_interval": 30,
  "max_messages_display": 100,
  "auto_refresh": true,
  "cache_enabled": true,
  "cache_ttl": 300,
  "log_level": "INFO"
}
```

---

## 📊 Performance

### Caching Strategy
- **🌐 Domains**: 1 hour TTL (rarely change)
- **📧 Messages**: 5 minutes TTL (frequently updated)
- **📄 Content**: 30 minutes TTL (stable content)
- **🧹 Auto-cleanup**: Expired entries automatically removed

### API Optimization
- **⚡ Rate Limiting**: 100ms minimum between requests
- **🔄 Retry Logic**: Exponential backoff for failures
- **🔗 Connection Pooling**: Reusable HTTP sessions
- **📦 Request Batching**: Efficient message retrieval

---

## 🔒 Security

### Authentication
- **🔑 Secure Input**: Hidden password entry
- **🎫 Token Management**: Bearer token authentication
- **🔄 Session Cleanup**: Automatic resource management
- **🚪 Secure Logout**: Complete session termination

### Data Protection
- **📝 No Sensitive Logs**: Credentials never logged
- **💾 Secure Cache**: Encrypted storage for sensitive data
- **✅ Input Validation**: Comprehensive data sanitization
- **🛡️ Error Safety**: Safe error message handling

---

## 🚨 Error Handling

### Exception Types
| Exception | Description | Recovery |
|-----------|-------------|----------|
| `AuthenticationError` | Login/authentication failures | Re-authentication required |
| `APIError` | API-specific errors with status codes | Automatic retry with backoff |
| `NetworkError` | Connection and timeout issues | Graceful degradation |
| `RateLimitError` | API rate limit exceeded | Automatic throttling |
| `ValidationError` | Input validation failures | User guidance provided |

### Error Recovery
- **🔄 Automatic Retry**: Transient failures handled gracefully
- **📱 User Guidance**: Clear error messages with solutions
- **📊 Comprehensive Logging**: Full error context for debugging
- **🛡️ Graceful Degradation**: Non-critical errors don't crash the app

---

## 📈 Monitoring & Observability

### Metrics Available
- **📊 API Request Counts** - Performance monitoring
- **💾 Cache Hit/Miss Ratios** - Efficiency tracking
- **📧 Message Processing Stats** - Throughput analysis
- **⚠️ Error Rates** - Reliability monitoring

### Logging Levels
- **🐛 DEBUG**: Detailed debugging information
- **ℹ️ INFO**: General operational information
- **⚠️ WARNING**: Warning messages
- **❌ ERROR**: Error conditions
- **🚨 CRITICAL**: Critical system failures

---

## 🚀 Deployment

### System Requirements
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Memory** | 128MB RAM | 256MB RAM |
| **Storage** | 50MB disk | 100MB disk |
| **Network** | Internet connection | Stable broadband |
| **OS** | Linux, macOS, Windows | Modern Linux distribution |

### Deployment Options
- **🖥️ Standalone**: Direct execution on target system
- **🐳 Container**: Docker container deployment
- **🔧 Virtual Environment**: Isolated Python environment
- **📦 System-wide**: Installation via pip

---

## 🤝 Contributing

### Development Setup
1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** thoroughly
6. **Submit** a pull request

### Code Standards
- **🐍 PEP 8** - Python style guidelines
- **📝 Type Hints** - All functions documented
- **✅ Error Handling** - Comprehensive exception management
- **📚 Documentation** - Clear inline documentation
- **🧪 Testing** - Unit tests for new features

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### Getting Help
- **📚 Documentation**: Check this README and inline code comments
- **🐛 Issues**: Report bugs via [GitHub Issues](https://github.com/inquilineorg/temp-mail-client/issues)
- **💬 Discussions**: Use [GitHub Discussions](https://github.com/inquilineorg/temp-mail-client/discussions) for questions

### Troubleshooting
```bash
# Enable debug logging
python cli.py --debug

# Check cache status
python cli.py stats

# Clear cache
python cli.py clear-cache

# Verify configuration
cat ~/.pryvon/config.json
```

---

## 🔄 Version History

### v2.0.0 - Professional Edition 🏆
- ✨ **Enhanced Architecture** - Modular design with clean separation
- 🚀 **Professional Error Handling** - Custom exceptions with recovery
- 💾 **Intelligent Caching** - TTL-based system with auto-cleanup
- ⚙️ **Configuration Management** - Persistent settings with runtime updates
- 📊 **Professional Logging** - Structured logging with rotation
- 🔒 **Enhanced Security** - Input validation and secure sessions
- 🎨 **Rich UI** - Beautiful console interface with Rich library
- 📱 **Dual Interface** - Both console and CLI for flexibility

### v1.0.0 - Foundation
- 🔧 Basic mail.tm API integration
- 📧 Simple email management
- 🖥️ Basic console interface

---

<div align="center">

**Built with ❤️ for professional temporary email management**

*Pryvon Temp Mail - Where Professional Meets Temporary*

[🏠 Home](https://github.com/inquilineorg/temp-mail-client) • [📖 Docs](https://github.com/inquilineorg/temp-mail-client#-documentation) • [🚀 Quick Start](https://github.com/inquilineorg/temp-mail-client#-quick-start)

</div>
