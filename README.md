<div align="center">

# 🚀 EnvPilot-CLI

**轻量级终端环境变量智能管理引擎**

*Lightweight Terminal Environment Variable Intelligent Management Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/gitstq/EnvPilot-CLI/releases)
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-brightgreen.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**EnvPilot-CLI** 是一款专为开发者打造的轻量级终端环境变量管理工具。在现代软件开发中，我们经常需要在多个项目之间切换，每个项目都有不同的环境变量配置（API密钥、数据库连接、服务端点等）。手动管理这些 `.env` 文件既繁琐又容易出错。

EnvPilot-CLI 解决了这一痛点，提供：
- 📦 **多项目配置隔离** - 为每个项目创建独立的环境变量配置
- ⚡ **一键切换激活** - 快速在不同项目环境之间切换
- 🔒 **敏感信息保护** - 自动识别并隐藏敏感变量
- 🎯 **零依赖设计** - 仅使用Python标准库，单文件可运行
- 🌈 **彩色终端界面** - 美观易用的命令行交互体验

**灵感来源**：在日常开发中，我们注意到开发者经常需要：
- 在多个客户的项目之间切换，每个项目都有不同的API密钥
- 管理开发、测试、生产环境的差异化配置
- 安全地共享项目配置而不泄露敏感信息

EnvPilot-CLI 正是为解决这些实际问题而生。

### ✨ 核心特性

| 特性 | 描述 | 图标 |
|------|------|------|
| **🎯 零依赖** | 仅使用Python标准库，无需安装额外依赖 | ⭐⭐⭐⭐⭐ |
| **📁 多配置管理** | 支持无限数量的项目配置，轻松切换 | ⭐⭐⭐⭐⭐ |
| **🔐 安全存储** | SQLite数据库存储，自动识别敏感变量 | ⭐⭐⭐⭐⭐ |
| **⚡ 快速激活** | 一键导出.env文件，即时生效 | ⭐⭐⭐⭐⭐ |
| **📥 智能导入** | 自动解析现有.env文件，无缝迁移 | ⭐⭐⭐⭐⭐ |
| **🎨 彩色界面** | 美观的终端输出，提升使用体验 | ⭐⭐⭐⭐ |
| **🔍 变量查看** | 支持显示/隐藏敏感变量值 | ⭐⭐⭐⭐ |
| **📤 灵活导出** | 支持导出到任意路径的.env文件 | ⭐⭐⭐⭐ |

### 🚀 快速开始

#### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Linux / macOS / Windows (WSL)

#### 安装步骤

**方式一：直接下载使用（推荐）**

```bash
# 下载单文件版本
curl -o envpilot.py https://raw.githubusercontent.com/gitstq/EnvPilot-CLI/main/envpilot.py

# 赋予执行权限
chmod +x envpilot.py

# 运行
python3 envpilot.py --version
```

**方式二：通过 pip 安装**

```bash
pip install envpilot-cli
```

**方式三：从源码安装**

```bash
git clone https://github.com/gitstq/EnvPilot-CLI.git
cd EnvPilot-CLI
make install
```

#### 快速启动

```bash
# 1. 初始化项目配置
envpilot init myproject --desc "我的项目"

# 2. 添加环境变量
envpilot add myproject API_KEY "sk-your-api-key"
envpilot add myproject DATABASE_URL "postgresql://localhost:5432/mydb"

# 3. 查看配置
envpilot show myproject

# 4. 激活配置（导出到 .env）
envpilot activate myproject

# 5. 加载环境变量
source .env
```

### 📖 详细使用指南

#### 命令列表

```bash
# 配置管理
envpilot init <name> [--path <path>] [--desc <description>]   # 初始化配置
envpilot list                                                    # 列出所有配置
envpilot show <name> [--values]                                  # 查看配置详情
envpilot delete <name> [--force]                                 # 删除配置

# 变量管理
envpilot add <profile> <key> <value>                             # 添加变量
envpilot remove <profile> <key>                                  # 移除变量

# 导入导出
envpilot import <name> <file> [--desc <description>]             # 从.env导入
envpilot activate <name> [--output <file>]                       # 激活配置
envpilot export <name> <file>                                    # 导出配置

# 生成Shell脚本
envpilot shell <name>                                            # 生成加载脚本
```

#### 典型使用场景

**场景一：多项目开发**

```bash
# 为每个项目创建配置
envpilot init project-a --path ~/projects/project-a
envpilot init project-b --path ~/projects/project-b

# 添加各自的环境变量
envpilot add project-a API_KEY "key-for-a"
envpilot add project-b API_KEY "key-for-b"

# 切换到项目A时
envpilot activate project-a
source .env

# 切换到项目B时
envpilot activate project-b
source .env
```

**场景二：多环境管理**

```bash
# 为同一项目创建不同环境配置
envpilot init myapp-dev --desc "开发环境"
envpilot init myapp-prod --desc "生产环境"

# 开发环境
envpilot add myapp-dev DEBUG "true"
envpilot add myapp-dev DATABASE_URL "postgresql://localhost/dev"

# 生产环境
envpilot add myapp-prod DEBUG "false"
envpilot add myapp-prod DATABASE_URL "postgresql://prod-server/prod"

# 部署时切换到生产环境
envpilot activate myapp-prod
```

**场景三：团队协作**

```bash
# 导出配置分享给团队（不含敏感值）
envpilot export myproject .env.example

# 团队成员导入模板
envpilot import myproject .env.example

# 然后各自添加敏感信息
envpilot add myproject API_KEY "个人密钥"
```

### 💡 设计思路与迭代规划

#### 设计理念

1. **简洁至上**：核心功能零依赖，降低使用门槛
2. **安全第一**：本地SQLite存储，数据不出本机
3. **开发者友好**：符合直觉的命令设计，学习成本低
4. **可扩展性**：模块化架构，易于添加新功能

#### 技术选型原因

- **Python 3.8+**: 广泛支持，标准库功能丰富
- **SQLite**: 轻量级本地数据库，无需额外服务
- **argparse**: 标准库CLI框架，无需第三方依赖

#### 后续迭代计划

- [ ] **v1.1.0** - 添加加密功能（可选依赖 cryptography）
- [ ] **v1.2.0** - 支持环境变量模板系统
- [ ] **v1.3.0** - 添加配置同步功能（Git集成）
- [ ] **v2.0.0** - TUI图形界面（使用 rich/textual）

#### 社区贡献方向

- 支持更多环境变量文件格式（YAML, TOML）
- 添加配置验证功能
- 集成主流CI/CD平台
- 多语言文档完善

### 📦 打包与部署指南

#### 构建分发包

```bash
# 安装构建依赖
pip install build twine

# 构建
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

#### 本地安装

```bash
# 从源码安装
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"
```

#### 兼容环境

| 操作系统 | Python版本 | 支持状态 |
|---------|-----------|---------|
| Ubuntu 20.04+ | 3.8-3.12 | ✅ 完全支持 |
| macOS 11+ | 3.8-3.12 | ✅ 完全支持 |
| Windows 10+ | 3.8-3.12 | ✅ WSL支持 |
| CentOS 8+ | 3.8-3.12 | ✅ 完全支持 |

### 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

**提交规范**：
- `feat:` 新增功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

**Issue 反馈规则**：
1. 描述问题时请提供复现步骤
2. 附上错误日志和系统环境信息
3. 如果是功能建议，请说明使用场景

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

**EnvPilot-CLI** 是一款專為開發者打造的輕量級終端環境變數管理工具。在現代軟體開發中，我們經常需要在多個專案之間切換，每個專案都有不同的環境變數配置（API金鑰、資料庫連線、服務端點等）。手動管理這些 `.env` 檔案既繁瑣又容易出錯。

EnvPilot-CLI 解決了這一痛點，提供：
- 📦 **多專案配置隔離** - 為每個專案建立獨立的環境變數配置
- ⚡ **一鍵切換啟用** - 快速在不同專案環境之間切換
- 🔒 **敏感資訊保護** - 自動識別並隱藏敏感變數
- 🎯 **零依賴設計** - 僅使用Python標準庫，單檔案可執行
- 🌈 **彩色終端介面** - 美觀易用的命令列互動體驗

### ✨ 核心特性

| 特性 | 描述 | 圖示 |
|------|------|------|
| **🎯 零依賴** | 僅使用Python標準庫，無需安裝額外依賴 | ⭐⭐⭐⭐⭐ |
| **📁 多配置管理** | 支援無限數量的專案配置，輕鬆切換 | ⭐⭐⭐⭐⭐ |
| **🔐 安全儲存** | SQLite資料庫儲存，自動識別敏感變數 | ⭐⭐⭐⭐⭐ |
| **⚡ 快速啟用** | 一鍵匯出.env檔案，即時生效 | ⭐⭐⭐⭐⭐ |
| **📥 智慧匯入** | 自動解析現有.env檔案，無縫遷移 | ⭐⭐⭐⭐⭐ |

### 🚀 快速開始

#### 安裝步驟

```bash
# 方式一：直接下載
curl -o envpilot.py https://raw.githubusercontent.com/gitstq/EnvPilot-CLI/main/envpilot.py
chmod +x envpilot.py

# 方式二：pip安裝
pip install envpilot-cli
```

#### 快速啟動

```bash
# 初始化專案配置
envpilot init myproject --desc "我的專案"

# 添加環境變數
envpilot add myproject API_KEY "sk-your-api-key"

# 啟用配置
envpilot activate myproject
source .env
```

### 📖 詳細使用指南

請參考[简体中文](#简体中文)部分的完整文檔。

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

**EnvPilot-CLI** is a lightweight terminal environment variable management tool designed for developers. In modern software development, we often need to switch between multiple projects, each with different environment variable configurations (API keys, database connections, service endpoints, etc.). Manually managing these `.env` files is tedious and error-prone.

EnvPilot-CLI solves this pain point by providing:
- 📦 **Multi-project isolation** - Create independent environment variable configs for each project
- ⚡ **One-click activation** - Quickly switch between different project environments
- 🔒 **Sensitive data protection** - Automatically identify and mask sensitive variables
- 🎯 **Zero dependencies** - Uses only Python standard library, single-file executable
- 🌈 **Colorful terminal UI** - Beautiful and easy-to-use command-line interface

**Inspiration**: In daily development, we noticed developers often need to:
- Switch between multiple client projects, each with different API keys
- Manage differentiated configurations for dev, test, and production environments
- Securely share project configurations without exposing sensitive information

EnvPilot-CLI was born to solve these real-world problems.

### ✨ Core Features

| Feature | Description | Rating |
|---------|-------------|--------|
| **🎯 Zero Dependencies** | Uses only Python standard library, no extra dependencies needed | ⭐⭐⭐⭐⭐ |
| **📁 Multi-config Management** | Support unlimited project configs, easy switching | ⭐⭐⭐⭐⭐ |
| **🔐 Secure Storage** | SQLite database storage, auto-identify sensitive variables | ⭐⭐⭐⭐⭐ |
| **⚡ Quick Activation** | One-click export to .env file, instant effect | ⭐⭐⭐⭐⭐ |
| **📥 Smart Import** | Auto-parse existing .env files, seamless migration | ⭐⭐⭐⭐⭐ |
| **🎨 Colorful Interface** | Beautiful terminal output, enhanced user experience | ⭐⭐⭐⭐ |
| **🔍 Variable Viewing** | Support show/hide sensitive variable values | ⭐⭐⭐⭐ |
| **📤 Flexible Export** | Export to .env file at any path | ⭐⭐⭐⭐ |

### 🚀 Quick Start

#### Requirements

- **Python**: 3.8 or higher
- **OS**: Linux / macOS / Windows (WSL)

#### Installation

**Option 1: Direct Download (Recommended)**

```bash
# Download single-file version
curl -o envpilot.py https://raw.githubusercontent.com/gitstq/EnvPilot-CLI/main/envpilot.py

# Make executable
chmod +x envpilot.py

# Run
python3 envpilot.py --version
```

**Option 2: Install via pip**

```bash
pip install envpilot-cli
```

**Option 3: Install from source**

```bash
git clone https://github.com/gitstq/EnvPilot-CLI.git
cd EnvPilot-CLI
make install
```

#### Quick Start

```bash
# 1. Initialize project config
envpilot init myproject --desc "My Project"

# 2. Add environment variables
envpilot add myproject API_KEY "sk-your-api-key"
envpilot add myproject DATABASE_URL "postgresql://localhost:5432/mydb"

# 3. View config
envpilot show myproject

# 4. Activate config (export to .env)
envpilot activate myproject

# 5. Load environment variables
source .env
```

### 📖 Detailed Usage Guide

#### Command Reference

```bash
# Config management
envpilot init <name> [--path <path>] [--desc <description>]   # Initialize config
envpilot list                                                    # List all configs
envpilot show <name> [--values]                                  # Show config details
envpilot delete <name> [--force]                                 # Delete config

# Variable management
envpilot add <profile> <key> <value>                             # Add variable
envpilot remove <profile> <key>                                  # Remove variable

# Import/Export
envpilot import <name> <file> [--desc <description>]             # Import from .env
envpilot activate <name> [--output <file>]                       # Activate config
envpilot export <name> <file>                                    # Export config

# Generate shell script
envpilot shell <name>                                            # Generate load script
```

#### Typical Use Cases

**Case 1: Multi-project Development**

```bash
# Create config for each project
envpilot init project-a --path ~/projects/project-a
envpilot init project-b --path ~/projects/project-b

# Add respective environment variables
envpilot add project-a API_KEY "key-for-a"
envpilot add project-b API_KEY "key-for-b"

# When switching to project A
envpilot activate project-a
source .env

# When switching to project B
envpilot activate project-b
source .env
```

**Case 2: Multi-environment Management**

```bash
# Create different environment configs for same project
envpilot init myapp-dev --desc "Development environment"
envpilot init myapp-prod --desc "Production environment"

# Development environment
envpilot add myapp-dev DEBUG "true"
envpilot add myapp-dev DATABASE_URL "postgresql://localhost/dev"

# Production environment
envpilot add myapp-prod DEBUG "false"
envpilot add myapp-prod DATABASE_URL "postgresql://prod-server/prod"

# Switch to production when deploying
envpilot activate myapp-prod
```

**Case 3: Team Collaboration**

```bash
# Export config to share with team (without sensitive values)
envpilot export myproject .env.example

# Team member imports template
envpilot import myproject .env.example

# Then add personal sensitive info
envpilot add myproject API_KEY "personal-key"
```

### 💡 Design Philosophy & Roadmap

#### Design Principles

1. **Simplicity First**: Core features with zero dependencies, low barrier to entry
2. **Security First**: Local SQLite storage, data never leaves your machine
3. **Developer Friendly**: Intuitive command design, low learning curve
4. **Extensibility**: Modular architecture, easy to add new features

#### Technology Choices

- **Python 3.8+**: Widely supported, rich standard library
- **SQLite**: Lightweight local database, no additional services needed
- **argparse**: Standard library CLI framework, no third-party dependencies

#### Roadmap

- [ ] **v1.1.0** - Add encryption support (optional cryptography dependency)
- [ ] **v1.2.0** - Support environment variable template system
- [ ] **v1.3.0** - Add config sync feature (Git integration)
- [ ] **v2.0.0** - TUI graphical interface (using rich/textual)

#### Community Contributions

- Support more environment variable file formats (YAML, TOML)
- Add config validation features
- Integrate with mainstream CI/CD platforms
- Improve multilingual documentation

### 📦 Packaging & Deployment Guide

#### Build Distribution Package

```bash
# Install build dependencies
pip install build twine

# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

#### Local Installation

```bash
# Install from source
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

#### Compatibility

| Operating System | Python Version | Support Status |
|-----------------|----------------|----------------|
| Ubuntu 20.04+ | 3.8-3.12 | ✅ Fully Supported |
| macOS 11+ | 3.8-3.12 | ✅ Fully Supported |
| Windows 10+ | 3.8-3.12 | ✅ WSL Supported |
| CentOS 8+ | 3.8-3.12 | ✅ Fully Supported |

### 🤝 Contributing Guidelines

Issues and Pull Requests are welcome!

**Commit Convention**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Testing related

**Issue Reporting Rules**:
1. Provide reproduction steps when describing issues
2. Attach error logs and system environment info
3. For feature suggestions, explain the use case

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by EnvPilot Team**

[⭐ Star us on GitHub](https://github.com/gitstq/EnvPilot-CLI) | [🐛 Report Issue](https://github.com/gitstq/EnvPilot-CLI/issues) | [💡 Feature Request](https://github.com/gitstq/EnvPilot-CLI/issues)

</div>
