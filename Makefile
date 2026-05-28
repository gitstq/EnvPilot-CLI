# EnvPilot-CLI Makefile
# 一键构建与安装脚本

.PHONY: help install install-dev uninstall test lint format clean build upload

PYTHON := python3
PIP := pip3
PACKAGE_NAME := envpilot-cli

help:
	@echo "🚀 EnvPilot-CLI 构建脚本"
	@echo ""
	@echo "可用命令:"
	@echo "  make install      - 安装 EnvPilot-CLI"
	@echo "  make install-dev  - 安装开发依赖"
	@echo "  make uninstall    - 卸载 EnvPilot-CLI"
	@echo "  make test         - 运行测试"
	@echo "  make lint         - 代码检查"
	@echo "  make format       - 代码格式化"
	@echo "  make clean        - 清理构建文件"
	@echo "  make build        - 构建分发包"
	@echo "  make upload       - 上传到 PyPI"

install:
	@echo "📦 安装 EnvPilot-CLI..."
	$(PIP) install -e .
	@echo "✅ 安装完成! 运行 'envpilot --version' 验证"

install-dev:
	@echo "📦 安装开发依赖..."
	$(PIP) install -e ".[dev]"
	@echo "✅ 开发环境安装完成!"

uninstall:
	@echo "🗑️  卸载 EnvPilot-CLI..."
	$(PIP) uninstall -y $(PACKAGE_NAME)
	@echo "✅ 卸载完成!"

test:
	@echo "🧪 运行测试..."
	pytest tests/ -v --cov=envpilot --cov-report=term-missing

lint:
	@echo "🔍 代码检查..."
	flake8 envpilot.py --max-line-length=120
	mypy envpilot.py --ignore-missing-imports

format:
	@echo "✨ 代码格式化..."
	black envpilot.py --line-length=120

clean:
	@echo "🧹 清理构建文件..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ 清理完成!"

build: clean
	@echo "🔨 构建分发包..."
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "✅ 构建完成!"

upload: build
	@echo "📤 上传到 PyPI..."
	twine upload dist/*
	@echo "✅ 上传完成!"

# 快速测试命令
demo:
	@echo "🎬 运行演示..."
	@echo ""
	@envpilot init demo-project --desc "演示项目"
	@envpilot add demo-project API_KEY "sk-demo123456"
	@envpilot add demo-project DATABASE_URL "postgresql://localhost:5432/demo"
	@envpilot list
	@echo ""
	@echo "✅ 演示完成!"
