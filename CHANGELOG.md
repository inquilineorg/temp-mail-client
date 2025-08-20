# Changelog

All notable changes to Pryvon Temp Mail will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- 🔮 **Future Enhancements**
  - Docker containerization support
  - Web-based dashboard interface
  - API rate limiting improvements
  - Enhanced message filtering and search
  - Multi-account management
  - Backup and restore functionality

---

## [2.0.0] - 2024-08-20

### 🎉 **Major Release - Professional Edition**

#### ✨ **Added**
- **🏗️ Enhanced Architecture**
  - Modular design with clean separation of concerns
  - Dedicated modules for configuration, logging, caching, and exceptions
  - Professional project structure following Python best practices

- **🚀 Professional Error Handling**
  - Custom exception classes for different error types
  - Comprehensive API error handling with status codes
  - Network retry logic with exponential backoff
  - Rate limiting and API protection mechanisms

- **💾 Intelligent Caching System**
  - TTL-based caching for domains, messages, and content
  - Automatic cache cleanup and invalidation
  - Cache statistics and monitoring capabilities
  - Configurable cache settings and policies

- **⚙️ Configuration Management**
  - Persistent configuration storage in `~/.pryvon/config.json`
  - Runtime configuration updates without restart
  - Environment-specific settings support
  - Configurable timeouts, retry policies, and preferences

- **📊 Professional Logging**
  - Structured logging with multiple levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Log rotation and file management
  - Console and file output support
  - Debug mode for troubleshooting and development

- **🔒 Enhanced Security Features**
  - Secure password input (hidden during typing)
  - Bearer token authentication with session management
  - Input validation and data sanitization
  - Secure session cleanup and logout procedures

- **🎨 Rich User Interface**
  - Beautiful console interface using Rich library
  - Professional tables, panels, and progress indicators
  - Screen management with console clearing for clean experience
  - Responsive design optimized for various terminal sizes

- **📱 Dual Interface Support**
  - Interactive console application for full-featured experience
  - Command-line interface (CLI) for automation and scripting
  - Consistent functionality across both interfaces

#### 🔧 **Changed**
- **🔄 API Client Enhancements**
  - Improved retry logic with urllib3 compatibility
  - Enhanced request handling with detailed error responses
  - Better rate limiting and API protection
  - Optimized connection pooling and session management

- **📧 Message Handling Improvements**
  - Flexible API response parsing for different structures
  - Enhanced message display with rich formatting
  - Better error handling for malformed responses
  - Improved message validation and processing

- **🎯 User Experience**
  - Professional console clearing for cleaner interface
  - Enhanced domain selection with auto-selection options
  - Better error messages with user guidance
  - Improved account management workflows

#### 🐛 **Fixed**
- **🔧 Compatibility Issues**
  - Fixed urllib3 2.0+ compatibility with retry strategies
  - Resolved API response parsing for different data structures
  - Fixed message data access issues with safe dictionary handling

- **📱 UI/UX Issues**
  - Resolved console display issues and terminal clutter
  - Fixed domain selection workflow for better user experience
  - Improved error recovery and user guidance

#### 🏷️ **Branding**
- **🎨 Complete Rebranding**
  - Changed from "Mail.tm Console Client" to "Pryvon Temp Mail"
  - Updated CLI tool name from `mailtm-cli` to `pryvon-temp-mail`
  - Changed configuration paths from `~/.mailtm/` to `~/.pryvon/`
  - Updated user agent and all branding references

#### 📚 **Documentation**
- **📖 Comprehensive README**
  - Professional modern design with badges and visual elements
  - Detailed feature documentation and architecture overview
  - Installation and usage guides with examples
  - Performance, security, and deployment information

---

## [1.0.0] - 2024-08-20

### 🎯 **Foundation Release**

#### ✨ **Added**
- **🔧 Basic API Integration**
  - Core mail.tm API client implementation
  - Account creation and management
  - Basic email operations (send, receive, delete)
  - Simple console interface

- **📧 Email Management**
  - Temporary email account creation
  - Basic message retrieval and display
  - Account login and logout functionality
  - Simple mailbox management

- **🖥️ Console Interface**
  - Basic menu-driven console application
  - Simple user input handling
  - Basic error handling and user feedback

#### 🔧 **Technical Foundation**
- **🐍 Python Implementation**
  - Python 3.8+ compatibility
  - Basic dependency management
  - Simple project structure
  - Basic error handling

---

## 📋 **Version History Summary**

| Version | Date | Release Type | Key Features |
|---------|------|--------------|--------------|
| **2.0.0** | 2024-08-20 | **Major** | Professional Edition, Enhanced Architecture, Rich UI |
| **1.0.0** | 2024-08-20 | **Foundation** | Basic API Integration, Console Interface |

---

## 🔄 **Migration Guide**

### From v1.0.0 to v2.0.0

#### **Breaking Changes**
- Configuration paths changed from `~/.mailtm/` to `~/.pryvon/`
- CLI tool renamed from `mailtm-cli` to `pryvon-temp-mail`
- Some API response handling improvements may affect custom integrations

#### **Upgrade Steps**
1. **Backup Configuration**: Copy your existing `~/.mailtm/` folder
2. **Update Installation**: Pull the latest code and reinstall dependencies
3. **Migrate Configuration**: Copy settings to new `~/.pryvon/` location
4. **Update Scripts**: Change any automation scripts to use new CLI names
5. **Test Functionality**: Verify all features work as expected

#### **New Features to Explore**
- Enhanced caching system for better performance
- Professional logging for debugging and monitoring
- Rich console interface for better user experience
- Comprehensive error handling and recovery
- Advanced configuration management

---

## 📝 **Contributing to Changelog**

When contributing to this project, please update this changelog with:

1. **New Features** - What was added
2. **Changes** - What was changed
3. **Deprecations** - What was deprecated
4. **Bug Fixes** - What was fixed
5. **Security** - Security-related changes

### **Changelog Format**
```markdown
## [Version] - YYYY-MM-DD

### ✨ Added
- New feature description

### 🔧 Changed
- Changed feature description

### 🐛 Fixed
- Bug fix description
```

---

## 📞 **Support & Questions**

For questions about specific changes or migration assistance:

- **📚 Documentation**: Check the README.md for detailed information
- **🐛 Issues**: Report bugs via [GitHub Issues](https://github.com/inquilineorg/temp-mail-client/issues)
- **💬 Discussions**: Use [GitHub Discussions](https://github.com/inquilineorg/temp-mail-client/discussions) for questions

---

*This changelog is maintained by the Pryvon Temp Mail development team.*
