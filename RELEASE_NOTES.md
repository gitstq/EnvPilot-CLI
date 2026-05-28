# EnvPilot-CLI v1.0.0 Release Notes

## 🎉 首次发布 | Initial Release

**发布日期**: 2026-05-28

## ✨ 新特性 | New Features

### 核心功能 | Core Features
- 🎯 **零依赖设计** - 仅使用Python标准库，单文件可运行
- 📁 **多配置管理** - 支持无限数量的项目环境变量配置
- 🔐 **安全存储** - SQLite本地数据库存储，数据不出本机
- ⚡ **快速激活** - 一键导出.env文件，即时生效
- 📥 **智能导入** - 自动解析现有.env文件，无缝迁移
- 🎨 **彩色界面** - 美观的终端输出，提升使用体验

### 命令列表 | Commands
- `envpilot init` - 初始化项目配置
- `envpilot list` - 列出所有配置
- `envpilot show` - 查看配置详情
- `envpilot add` - 添加环境变量
- `envpilot remove` - 移除环境变量
- `envpilot activate` - 激活配置（导出.env）
- `envpilot import` - 从.env文件导入
- `envpilot export` - 导出配置
- `envpilot delete` - 删除配置
- `envpilot shell` - 生成Shell加载脚本

## 🔧 技术细节 | Technical Details

- **Python版本**: 3.8+
- **依赖**: 零依赖（核心功能）
- **数据库**: SQLite3
- **存储位置**: `~/.envpilot/`

## 📦 安装方式 | Installation

### 方式一：直接下载 | Direct Download
```bash
curl -o envpilot.py https://raw.githubusercontent.com/gitstq/EnvPilot-CLI/main/envpilot.py
chmod +x envpilot.py
python3 envpilot.py --version
```

### 方式二：pip安装 | pip Install
```bash
pip install envpilot-cli
```

### 方式三：源码安装 | Source Install
```bash
git clone https://github.com/gitstq/EnvPilot-CLI.git
cd EnvPilot-CLI
make install
```

## 🚀 快速开始 | Quick Start

```bash
# 初始化配置
envpilot init myproject --desc "My Project"

# 添加环境变量
envpilot add myproject API_KEY "sk-your-api-key"

# 激活配置
envpilot activate myproject

# 加载环境变量
source .env
```

## 📝 文档 | Documentation

- [简体中文](https://github.com/gitstq/EnvPilot-CLI#简体中文)
- [繁體中文](https://github.com/gitstq/EnvPilot-CLI#繁體中文)
- [English](https://github.com/gitstq/EnvPilot-CLI#english)

## 🔮 未来计划 | Future Plans

- [ ] v1.1.0 - 加密功能支持
- [ ] v1.2.0 - 环境变量模板系统
- [ ] v1.3.0 - Git集成同步功能
- [ ] v2.0.0 - TUI图形界面

## 🤝 贡献 | Contributing

欢迎提交Issue和Pull Request！

## 📄 协议 | License

MIT License

---

**Made with ❤️ by EnvPilot Team**
