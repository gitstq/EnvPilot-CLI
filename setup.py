#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnvPilot-CLI Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="envpilot-cli",
    version="1.0.0",
    author="EnvPilot Team",
    author_email="envpilot@example.com",
    description="轻量级终端环境变量智能管理引擎 | Lightweight Terminal Environment Variable Management Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/EnvPilot-CLI",
    py_modules=["envpilot"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 核心功能零依赖
    ],
    extras_require={
        "crypto": ["cryptography>=3.4.8"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "envpilot=envpilot:main",
        ],
    },
    keywords="environment variables, env, dotenv, cli, terminal, developer tools, productivity",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/EnvPilot-CLI/issues",
        "Source": "https://github.com/gitstq/EnvPilot-CLI",
        "Documentation": "https://github.com/gitstq/EnvPilot-CLI#readme",
    },
)
