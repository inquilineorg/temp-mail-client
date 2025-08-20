# Mail.tm Console Client - Professional Edition

A **commercial-grade** console application that integrates with the mail.tm API to provide enterprise-level temporary email management functionality.

## 🚀 Features

### Core Functionality
- **Account Management**
  - Create new temporary email accounts with validation
  - Secure login/logout with enhanced error handling
  - Account deletion with confirmation safeguards
  - Real-time account statistics and quota monitoring

- **Email Operations**
  - Check mailbox with intelligent caching
  - Refresh mailbox for latest messages
  - View full message content with rich formatting
  - Mark messages as read/unread
  - Delete individual messages with confirmation
  - Support for HTML and text message formats

### Professional Features
- **Advanced Caching System**
  - Intelligent TTL-based caching for domains and messages
  - Configurable cache settings and cleanup
  - Cache statistics and monitoring
  - Automatic cache invalidation

- **Enterprise-Grade Error Handling**
  - Custom exception classes for different error types
  - Comprehensive API error handling with status codes
  - Network retry logic with exponential backoff
  - Rate limiting and API protection

- **Configuration Management**
  - Persistent configuration storage
  - Runtime configuration updates
  - Environment-specific settings
  - Configurable timeouts and retry policies

- **Professional Logging**
  - Structured logging with multiple levels
  - Log rotation and file management
  - Console and file output
  - Debug mode for troubleshooting

- **Security Features**
  - Secure password input (hidden during typing)
  - Bearer token authentication
  - Session management and cleanup
  - Input validation and sanitization

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Install
```bash
# Clone the repository
git clone <repository-url>
cd temp-mail-client

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Interactive Console Application
```bash
# Start the full-featured console application
python console_app.py
```

### Command Line Interface (CLI)
```bash
# Create a new account
python cli.py create --auto-login

# Login to existing account
python cli.py login user@domain.com

# List messages
python cli.py list --limit 20 --unread-only

# View specific message
python cli.py view <message_id>

# Refresh mailbox
python cli.py refresh

# Show statistics
python cli.py stats

# Get help
python cli.py --help
```

### CLI Examples
```bash
# Create account with custom credentials
python cli.py create -u myuser -d example.com -p mypassword123

# Quick account creation with auto-login
python cli.py create --auto-login

# View only unread messages
python cli.py list --unread-only

# Check available domains
python cli.py domains

# Clear cache
python cli.py clear-cache
```

## 🏗️ Architecture

### Module Structure
```
temp-mail-client/
├── config.py          # Configuration management
├── logger.py          # Professional logging system
├── cache.py           # Intelligent caching system
├── exceptions.py      # Custom exception classes
├── mailtm_client.py   # Core API client
├── console_app.py     # Interactive console application
├── cli.py            # Command-line interface
├── example_usage.py   # Usage examples
└── requirements.txt   # Dependencies
```

### Key Components
- **ConfigManager**: Handles application configuration with persistence
- **Cache**: TTL-based caching system with automatic cleanup
- **Logger**: Professional logging with rotation and multiple outputs
- **MailTMClient**: Enhanced API client with retry logic and error handling
- **ConsoleApp**: Rich interactive interface with signal handling
- **CLI**: Click-based command-line interface for automation

## ⚙️ Configuration

### Configuration Options
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

### Environment Variables
```bash
export MAILTM_LOG_LEVEL=DEBUG
export MAILTM_CACHE_ENABLED=false
export MAILTM_API_TIMEOUT=60
```

## 🔧 Development

### Running Tests
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Code Quality
- Type hints throughout the codebase
- Comprehensive error handling
- Professional logging and monitoring
- Clean architecture with separation of concerns

## 📊 Performance Features

### Caching Strategy
- **Domain Cache**: 1 hour TTL for available domains
- **Message Cache**: 5 minutes TTL for mailbox contents
- **Message Content Cache**: 30 minutes TTL for full messages
- **Automatic Cleanup**: Expired entries are automatically removed

### API Optimization
- **Rate Limiting**: 100ms minimum between requests
- **Retry Logic**: Exponential backoff for failed requests
- **Connection Pooling**: Reusable HTTP sessions
- **Request Batching**: Efficient message retrieval

## 🚨 Error Handling

### Exception Types
- `AuthenticationError`: Login/authentication failures
- `AccountNotFoundError`: Account doesn't exist
- `InvalidCredentialsError`: Wrong password/username
- `APIError`: API-specific errors with status codes
- `NetworkError`: Connection and timeout issues
- `RateLimitError`: API rate limit exceeded
- `ValidationError`: Input validation failures

### Error Recovery
- Automatic retry for transient failures
- Graceful degradation for non-critical errors
- User-friendly error messages
- Comprehensive error logging

## 🔒 Security Features

### Authentication
- Secure password input (hidden during typing)
- Bearer token management
- Automatic session cleanup
- Secure logout procedures

### Data Protection
- No sensitive data in logs
- Secure cache management
- Input validation and sanitization
- Safe error message handling

## 📈 Monitoring & Observability

### Metrics Available
- API request counts
- Cache hit/miss ratios
- Account quota usage
- Message processing statistics
- Error rates and types

### Logging Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General operational information
- **WARNING**: Warning messages
- **ERROR**: Error conditions
- **CRITICAL**: Critical system failures

## 🚀 Production Deployment

### System Requirements
- **Memory**: 128MB RAM minimum
- **Storage**: 50MB disk space
- **Network**: Internet connection for API access
- **OS**: Linux, macOS, Windows

### Deployment Options
- **Standalone**: Run directly on target system
- **Container**: Docker container deployment
- **Virtual Environment**: Isolated Python environment
- **System-wide**: Install via pip

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive error handling
- Write clear documentation
- Add appropriate logging

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub
- **Discussions**: Use GitHub Discussions for questions

### Troubleshooting
- Enable debug logging: `python cli.py --debug`
- Check cache status: `python cli.py stats`
- Clear cache: `python cli.py clear-cache`
- Verify configuration: Check `~/.mailtm/config.json`

## 🔄 Version History

### v2.0.0 - Professional Edition
- ✨ Enhanced error handling and custom exceptions
- 🚀 Intelligent caching system with TTL
- ⚙️ Configuration management and persistence
- 📊 Professional logging with rotation
- 🔒 Enhanced security and validation
- 🎨 Improved UI with Rich library
- 📱 Command-line interface for automation
- 🏗️ Clean architecture and modular design

### v1.0.0 - Basic Edition
- Basic mail.tm API integration
- Simple console interface
- Account management features
- Basic email operations

---

**Built with ❤️ for professional temporary email management**
