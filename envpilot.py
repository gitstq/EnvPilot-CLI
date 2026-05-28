#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnvPilot-CLI - 轻量级终端环境变量智能管理引擎
Lightweight Terminal Environment Variable Intelligent Management Engine

Author: EnvPilot Team
Version: 1.0.0
License: MIT
"""

import os
import sys
import json
import sqlite3
import argparse
import getpass
import hashlib
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# 版本信息
__version__ = "1.0.0"
__author__ = "EnvPilot Team"

# 常量定义
APP_NAME = "EnvPilot"
CONFIG_DIR = Path.home() / ".envpilot"
DB_PATH = CONFIG_DIR / "envpilot.db"
TEMPLATE_DIR = CONFIG_DIR / "templates"

# 颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# 图标
ICONS = {
    "success": "✓",
    "error": "✗",
    "warning": "⚠",
    "info": "ℹ",
    "folder": "📁",
    "file": "📄",
    "key": "🔑",
    "lock": "🔒",
    "unlock": "🔓",
    "rocket": "🚀",
    "gear": "⚙️",
}


def print_colored(text: str, color: str = Colors.ENDC, bold: bool = False):
    """打印彩色文本"""
    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Colors.ENDC}")


def print_banner():
    """打印应用横幅"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {Colors.BOLD}🚀 EnvPilot-CLI{Colors.ENDC}{Colors.CYAN} - 轻量级终端环境变量智能管理引擎{Colors.ENDC}{Colors.CYAN}        ║
║                                                              ║
║   Version: {__version__}                                          ║
║   Author:  {__author__}                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print(banner)


@dataclass
class EnvProfile:
    """环境变量配置文件"""
    id: int
    name: str
    project_path: str
    description: str
    created_at: str
    updated_at: str
    is_encrypted: bool = False
    variables: Dict[str, str] = None
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = {}


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建配置文件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                project_path TEXT NOT NULL,
                description TEXT,
                created_at TEXT,
                updated_at TEXT,
                is_encrypted INTEGER DEFAULT 0
            )
        ''')
        
        # 创建环境变量表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS env_variables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER,
                key TEXT NOT NULL,
                value TEXT,
                is_sensitive INTEGER DEFAULT 0,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建模板表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                variables TEXT,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_profile(self, name: str, project_path: str, description: str = "") -> int:
        """添加配置文件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO profiles (name, project_path, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, project_path, description, now, now))
        
        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return profile_id
    
    def get_profile(self, name: str) -> Optional[EnvProfile]:
        """获取配置文件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM profiles WHERE name = ?', (name,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        profile = EnvProfile(
            id=row[0],
            name=row[1],
            project_path=row[2],
            description=row[3],
            created_at=row[4],
            updated_at=row[5],
            is_encrypted=bool(row[6])
        )
        
        # 获取变量
        cursor.execute('SELECT key, value, is_sensitive FROM env_variables WHERE profile_id = ?', (profile.id,))
        for var_row in cursor.fetchall():
            profile.variables[var_row[0]] = var_row[1]
        
        conn.close()
        return profile
    
    def list_profiles(self) -> List[EnvProfile]:
        """列出所有配置文件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM profiles ORDER BY updated_at DESC')
        profiles = []
        
        for row in cursor.fetchall():
            profile = EnvProfile(
                id=row[0],
                name=row[1],
                project_path=row[2],
                description=row[3],
                created_at=row[4],
                updated_at=row[5],
                is_encrypted=bool(row[6])
            )
            profiles.append(profile)
        
        conn.close()
        return profiles
    
    def delete_profile(self, name: str) -> bool:
        """删除配置文件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM profiles WHERE name = ?', (name,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return deleted
    
    def add_variable(self, profile_id: int, key: str, value: str, is_sensitive: bool = False):
        """添加环境变量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO env_variables (profile_id, key, value, is_sensitive)
            VALUES (?, ?, ?, ?)
        ''', (profile_id, key, value, int(is_sensitive)))
        
        # 更新配置文件时间
        now = datetime.now().isoformat()
        cursor.execute('UPDATE profiles SET updated_at = ? WHERE id = ?', (now, profile_id))
        
        conn.commit()
        conn.close()
    
    def delete_variable(self, profile_id: int, key: str):
        """删除环境变量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM env_variables WHERE profile_id = ? AND key = ?', (profile_id, key))
        
        now = datetime.now().isoformat()
        cursor.execute('UPDATE profiles SET updated_at = ? WHERE id = ?', (now, profile_id))
        
        conn.commit()
        conn.close()


class EnvFileManager:
    """.env文件管理器"""
    
    @staticmethod
    def parse_env_file(file_path: Path) -> Dict[str, str]:
        """解析.env文件"""
        variables = {}
        
        if not file_path.exists():
            return variables
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    variables[key] = value
        
        return variables
    
    @staticmethod
    def write_env_file(file_path: Path, variables: Dict[str, str], backup: bool = True):
        """写入.env文件"""
        if backup and file_path.exists():
            backup_path = file_path.with_suffix('.env.backup')
            backup_path.write_text(file_path.read_text(), encoding='utf-8')
        
        lines = []
        for key, value in sorted(variables.items()):
            # 如果值包含空格或特殊字符，使用引号
            if ' ' in value or any(c in value for c in '#$"\''):
                value = f'"{value}"'
            lines.append(f"{key}={value}")
        
        file_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    
    @staticmethod
    def detect_env_files(project_path: Path) -> List[Path]:
        """检测项目中的.env文件"""
        env_files = []
        patterns = ['.env', '.env.*', '*.env']
        
        for pattern in patterns:
            env_files.extend(project_path.glob(pattern))
        
        return sorted(set(env_files))


class EnvPilot:
    """EnvPilot主类"""
    
    def __init__(self):
        self.db = DatabaseManager(DB_PATH)
        self.env_manager = EnvFileManager()
        TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    
    def init_profile(self, name: str, project_path: str = ".", description: str = ""):
        """初始化配置文件"""
        project_path = Path(project_path).resolve()
        
        if not project_path.exists():
            print_colored(f"{ICONS['error']} 项目路径不存在: {project_path}", Colors.FAIL)
            return False
        
        # 检查是否已存在
        existing = self.db.get_profile(name)
        if existing:
            print_colored(f"{ICONS['error']} 配置文件 '{name}' 已存在", Colors.FAIL)
            return False
        
        # 创建配置文件
        profile_id = self.db.add_profile(name, str(project_path), description)
        
        # 自动导入现有的.env文件
        env_files = self.env_manager.detect_env_files(project_path)
        imported_count = 0
        
        for env_file in env_files:
            variables = self.env_manager.parse_env_file(env_file)
            for key, value in variables.items():
                is_sensitive = any(s in key.lower() for s in ['key', 'secret', 'password', 'token', 'api'])
                self.db.add_variable(profile_id, key, value, is_sensitive)
                imported_count += 1
        
        print_colored(f"{ICONS['success']} 配置文件 '{name}' 创建成功", Colors.GREEN, bold=True)
        print_colored(f"   项目路径: {project_path}", Colors.CYAN)
        print_colored(f"   导入变量: {imported_count} 个", Colors.CYAN)
        if env_files:
            print_colored(f"   源文件: {', '.join(f.name for f in env_files)}", Colors.CYAN)
        
        return True
    
    def list_profiles(self):
        """列出所有配置文件"""
        profiles = self.db.list_profiles()
        
        if not profiles:
            print_colored(f"{ICONS['info']} 暂无配置文件，使用 'envpilot init <name>' 创建", Colors.WARNING)
            return
        
        print_colored(f"\n{ICONS['folder']} 配置文件列表 ({len(profiles)}个):", Colors.HEADER, bold=True)
        print_colored("-" * 70, Colors.CYAN)
        
        for profile in profiles:
            lock_icon = ICONS['lock'] if profile.is_encrypted else ICONS['unlock']
            print_colored(f"\n  {lock_icon} {Colors.BOLD}{profile.name}{Colors.ENDC}", Colors.GREEN)
            print_colored(f"     路径: {profile.project_path}", Colors.CYAN)
            if profile.description:
                print_colored(f"     描述: {profile.description}", Colors.CYAN)
            print_colored(f"     更新: {profile.updated_at[:19]}", Colors.CYAN)
    
    def show_profile(self, name: str, show_values: bool = False):
        """显示配置文件详情"""
        profile = self.db.get_profile(name)
        
        if not profile:
            print_colored(f"{ICONS['error']} 配置文件 '{name}' 不存在", Colors.FAIL)
            return
        
        print_colored(f"\n{ICONS['file']} 配置文件: {Colors.BOLD}{profile.name}{Colors.ENDC}", Colors.HEADER, bold=True)
        print_colored(f"   项目路径: {profile.project_path}", Colors.CYAN)
        print_colored(f"   描述: {profile.description or '无'}", Colors.CYAN)
        print_colored(f"   创建时间: {profile.created_at[:19]}", Colors.CYAN)
        print_colored(f"   更新时间: {profile.updated_at[:19]}", Colors.CYAN)
        
        if profile.variables:
            print_colored(f"\n   {ICONS['key']} 环境变量 ({len(profile.variables)}个):", Colors.HEADER)
            print_colored("   " + "-" * 50, Colors.CYAN)
            
            for key in sorted(profile.variables.keys()):
                value = profile.variables[key]
                if not show_values and any(s in key.lower() for s in ['key', 'secret', 'password', 'token', 'api']):
                    display_value = "*" * min(len(value), 20)
                else:
                    display_value = value[:50] + "..." if len(value) > 50 else value
                print_colored(f"   {key}={display_value}", Colors.CYAN)
        else:
            print_colored(f"\n   {ICONS['info']} 暂无环境变量", Colors.WARNING)
    
    def add_variable(self, profile_name: str, key: str, value: str):
        """添加环境变量"""
        profile = self.db.get_profile(profile_name)
        
        if not profile:
            print_colored(f"{ICONS['error']} 配置文件 '{profile_name}' 不存在", Colors.FAIL)
            return False
        
        is_sensitive = any(s in key.lower() for s in ['key', 'secret', 'password', 'token', 'api'])
        self.db.add_variable(profile.id, key, value, is_sensitive)
        
        print_colored(f"{ICONS['success']} 环境变量添加成功", Colors.GREEN)
        print_colored(f"   {key}={value if not is_sensitive else '*' * min(len(value), 10)}", Colors.CYAN)
        return True
    
    def remove_variable(self, profile_name: str, key: str):
        """移除环境变量"""
        profile = self.db.get_profile(profile_name)
        
        if not profile:
            print_colored(f"{ICONS['error']} 配置文件 '{profile_name}' 不存在", Colors.FAIL)
            return False
        
        if key not in profile.variables:
            print_colored(f"{ICONS['error']} 环境变量 '{key}' 不存在", Colors.FAIL)
            return False
        
        self.db.delete_variable(profile.id, key)
        print_colored(f"{ICONS['success']} 环境变量 '{key}' 已移除", Colors.GREEN)
        return True
    
    def activate_profile(self, name: str, export_file: str = ".env"):
        """激活配置文件（导出到.env文件）"""
        profile = self.db.get_profile(name)
        
        if not profile:
            print_colored(f"{ICONS['error']} 配置文件 '{name}' 不存在", Colors.FAIL)
            return False
        
        project_path = Path(profile.project_path)
        env_file = project_path / export_file
        
        self.env_manager.write_env_file(env_file, profile.variables)
        
        print_colored(f"{ICONS['rocket']} 配置文件 '{name}' 已激活", Colors.GREEN, bold=True)
        print_colored(f"   导出路径: {env_file}", Colors.CYAN)
        print_colored(f"   变量数量: {len(profile.variables)}", Colors.CYAN)
        print_colored(f"\n{ICONS['info']} 提示: 运行 'source {env_file}' 加载环境变量", Colors.WARNING)
        return True
    
    def import_env(self, name: str, env_file: str, description: str = ""):
        """从.env文件导入"""
        env_path = Path(env_file)
        
        if not env_path.exists():
            print_colored(f"{ICONS['error']} 文件不存在: {env_file}", Colors.FAIL)
            return False
        
        project_path = env_path.parent.resolve()
        
        # 创建配置文件
        profile_id = self.db.add_profile(name, str(project_path), description)
        
        # 导入变量
        variables = self.env_manager.parse_env_file(env_path)
        for key, value in variables.items():
            is_sensitive = any(s in key.lower() for s in ['key', 'secret', 'password', 'token', 'api'])
            self.db.add_variable(profile_id, key, value, is_sensitive)
        
        print_colored(f"{ICONS['success']} 成功导入配置文件 '{name}'", Colors.GREEN, bold=True)
        print_colored(f"   源文件: {env_path}", Colors.CYAN)
        print_colored(f"   导入变量: {len(variables)} 个", Colors.CYAN)
        return True
    
    def export_profile(self, name: str, output_file: str):
        """导出配置文件到.env文件"""
        profile = self.db.get_profile(name)
        
        if not profile:
            print_colored(f"{ICONS['error']} 配置文件 '{name}' 不存在", Colors.FAIL)
            return False
        
        output_path = Path(output_file)
        self.env_manager.write_env_file(output_path, profile.variables, backup=False)
        
        print_colored(f"{ICONS['success']} 配置文件已导出", Colors.GREEN)
        print_colored(f"   目标文件: {output_path}", Colors.CYAN)
        return True
    
    def delete_profile(self, name: str, force: bool = False):
        """删除配置文件"""
        if not force:
            confirm = input(f"确认删除配置文件 '{name}'? [y/N]: ")
            if confirm.lower() != 'y':
                print_colored(f"{ICONS['info']} 已取消删除", Colors.WARNING)
                return False
        
        if self.db.delete_profile(name):
            print_colored(f"{ICONS['success']} 配置文件 '{name}' 已删除", Colors.GREEN)
            return True
        else:
            print_colored(f"{ICONS['error']} 配置文件 '{name}' 不存在", Colors.FAIL)
            return False
    
    def generate_shell_script(self, name: str) -> str:
        """生成Shell脚本用于加载环境变量"""
        profile = self.db.get_profile(name)
        
        if not profile:
            return ""
        
        lines = ["#!/bin/bash", f"# EnvPilot generated script for profile: {name}", ""]
        
        for key, value in profile.variables.items():
            escaped_value = value.replace('"', '\\"')
            lines.append(f'export {key}="{escaped_value}"')
        
        lines.append("")
        success_icon = ICONS["success"]
        lines.append(f'echo "{success_icon} Environment variables loaded from profile: {name}"')
        
        return '\n'.join(lines)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        prog='envpilot',
        description='EnvPilot-CLI - 轻量级终端环境变量智能管理引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  envpilot init myproject                    # 初始化配置文件
  envpilot list                              # 列出所有配置
  envpilot show myproject                    # 查看配置详情
  envpilot add myproject KEY value           # 添加环境变量
  envpilot activate myproject                # 激活配置（导出.env）
  envpilot import myproject .env             # 从.env文件导入
  envpilot delete myproject                  # 删除配置
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化配置文件')
    init_parser.add_argument('name', help='配置文件名称')
    init_parser.add_argument('--path', '-p', default='.', help='项目路径 (默认: 当前目录)')
    init_parser.add_argument('--desc', '-d', default='', help='配置描述')
    
    # list 命令
    subparsers.add_parser('list', help='列出所有配置文件')
    
    # show 命令
    show_parser = subparsers.add_parser('show', help='显示配置文件详情')
    show_parser.add_argument('name', help='配置文件名称')
    show_parser.add_argument('--values', '-v', action='store_true', help='显示敏感变量值')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加环境变量')
    add_parser.add_argument('profile', help='配置文件名称')
    add_parser.add_argument('key', help='变量名')
    add_parser.add_argument('value', help='变量值')
    
    # remove 命令
    remove_parser = subparsers.add_parser('remove', help='移除环境变量')
    remove_parser.add_argument('profile', help='配置文件名称')
    remove_parser.add_argument('key', help='变量名')
    
    # activate 命令
    activate_parser = subparsers.add_parser('activate', help='激活配置文件')
    activate_parser.add_argument('name', help='配置文件名称')
    activate_parser.add_argument('--output', '-o', default='.env', help='输出文件名')
    
    # import 命令
    import_parser = subparsers.add_parser('import', help='从.env文件导入')
    import_parser.add_argument('name', help='配置文件名称')
    import_parser.add_argument('file', help='.env文件路径')
    import_parser.add_argument('--desc', '-d', default='', help='配置描述')
    
    # export 命令
    export_parser = subparsers.add_parser('export', help='导出配置文件')
    export_parser.add_argument('name', help='配置文件名称')
    export_parser.add_argument('file', help='输出文件路径')
    
    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除配置文件')
    delete_parser.add_argument('name', help='配置文件名称')
    delete_parser.add_argument('--force', '-f', action='store_true', help='强制删除')
    
    # shell 命令
    shell_parser = subparsers.add_parser('shell', help='生成Shell加载脚本')
    shell_parser.add_argument('name', help='配置文件名称')
    
    args = parser.parse_args()
    
    # 打印横幅
    if args.command != 'shell':
        print_banner()
    
    # 初始化 EnvPilot
    pilot = EnvPilot()
    
    # 执行命令
    if args.command == 'init':
        pilot.init_profile(args.name, args.path, args.desc)
    
    elif args.command == 'list':
        pilot.list_profiles()
    
    elif args.command == 'show':
        pilot.show_profile(args.name, args.values)
    
    elif args.command == 'add':
        pilot.add_variable(args.profile, args.key, args.value)
    
    elif args.command == 'remove':
        pilot.remove_variable(args.profile, args.key)
    
    elif args.command == 'activate':
        pilot.activate_profile(args.name, args.output)
    
    elif args.command == 'import':
        pilot.import_env(args.name, args.file, args.desc)
    
    elif args.command == 'export':
        pilot.export_profile(args.name, args.file)
    
    elif args.command == 'delete':
        pilot.delete_profile(args.name, args.force)
    
    elif args.command == 'shell':
        script = pilot.generate_shell_script(args.name)
        if script:
            print(script)
        else:
            print(f"Profile '{args.name}' not found", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
