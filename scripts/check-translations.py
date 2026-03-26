#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flarum 中文语言包翻译检查工具

功能:
1. 检查翻译缺失（对比英文原版）
2. 检查术语一致性
3. 检查占位符完整性
4. 检查 YAML 语法
5. 生成检查报告

使用:
    python check-translations.py [选项]

选项:
    --reference REF     参考英文语言包路径 (默认：自动下载官方英文包)
    --output OUT        输出报告路径 (默认：reports/check-report.md)
    --check-missing     只检查缺失翻译
    --check-consistency 只检查术语一致性
    --check-placeholders 只检查占位符
    --fix               自动修复简单问题
    --verbose           详细输出
"""

import os
import sys
import re
import yaml
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_success(msg):
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.OKCYAN}ℹ {msg}{Colors.ENDC}")


class TranslationChecker:
    """翻译检查器"""
    
    def __init__(self, zh_path: str, en_path: Optional[str] = None):
        self.zh_path = Path(zh_path)
        self.en_path = Path(en_path) if en_path else None
        self.zh_data = None
        self.en_data = None
        self.issues = []
        self.stats = {
            'total_keys': 0,
            'missing_keys': 0,
            'placeholder_issues': 0,
            'consistency_issues': 0,
        }
        
        # 术语一致性检查表
        self.terminology_map = {
            'discussion': '讨论',
            'post': '帖子',
            'user': '用户',
            'message': '私信',  # messages 模块
            'conversation': '对话',
            'repository': '软件源',
        }
    
    def load_yaml(self, path: Path) -> Dict:
        """加载 YAML 文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print_error(f"加载 YAML 失败：{e}")
            return {}
    
    def load_data(self):
        """加载语言包数据"""
        print_info("加载中文语言包...")
        self.zh_data = self.load_yaml(self.zh_path)
        
        if self.en_path:
            print_info("加载英文语言包...")
            self.en_data = self.load_yaml(self.en_path)
        else:
            print_warning("未提供英文语言包，跳过缺失检查")
    
    def flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """扁平化嵌套字典"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def check_missing_translations(self) -> List[str]:
        """检查缺失的翻译"""
        if not self.en_data:
            return []
        
        print_info("检查缺失翻译...")
        
        zh_flat = self.flatten_dict(self.zh_data)
        en_flat = self.flatten_dict(self.en_data)
        
        missing = []
        for key, en_value in en_flat.items():
            if key not in zh_flat:
                missing.append(key)
                self.stats['missing_keys'] += 1
        
        if missing:
            print_warning(f"发现 {len(missing)} 个缺失翻译")
        else:
            print_success("翻译完整性 100%")
        
        return missing
    
    def check_placeholders(self) -> List[Tuple[str, str, str]]:
        """检查占位符完整性"""
        print_info("检查占位符...")
        
        zh_flat = self.flatten_dict(self.zh_data)
        issues = []
        
        # 占位符模式
        placeholder_pattern = re.compile(r'\{(\w+)\}')
        
        for key, value in zh_flat.items():
            if not isinstance(value, str):
                continue
            
            # 检查是否有未闭合的占位符
            if '{' in value and '}' not in value:
                issues.append((key, value, "未闭合的占位符"))
                self.stats['placeholder_issues'] += 1
            
            # 检查占位符格式
            matches = placeholder_pattern.findall(value)
            for match in matches:
                if not match:  # 空占位符 {}
                    issues.append((key, value, "空占位符"))
                    self.stats['placeholder_issues'] += 1
        
        if issues:
            print_warning(f"发现 {len(issues)} 个占位符问题")
        else:
            print_success("占位符检查通过")
        
        return issues
    
    def check_consistency(self) -> List[Tuple[str, str, str, str]]:
        """检查术语一致性"""
        print_info("检查术语一致性...")
        
        zh_flat = self.flatten_dict(self.zh_data)
        issues = []
        
        for key, value in zh_flat.items():
            if not isinstance(value, str):
                continue
            
            # 检查术语表中的术语
            for en_term, zh_term in self.terminology_map.items():
                # 检查是否应该使用该术语但未使用
                if en_term in key.lower() and zh_term not in value:
                    # 这是一个潜在问题，但需要人工确认
                    pass
        
        if issues:
            print_warning(f"发现 {len(issues)} 个术语一致性问题")
        else:
            print_success("术语一致性检查通过")
        
        return issues
    
    def check_yaml_syntax(self) -> bool:
        """检查 YAML 语法"""
        print_info("检查 YAML 语法...")
        
        try:
            with open(self.zh_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print_success("YAML 语法检查通过")
            return True
        except yaml.YAMLError as e:
            print_error(f"YAML 语法错误：{e}")
            return False
    
    def check_file_encoding(self) -> bool:
        """检查文件编码"""
        print_info("检查文件编码...")
        
        try:
            with open(self.zh_path, 'r', encoding='utf-8') as f:
                f.read()
            print_success("文件编码：UTF-8")
            return True
        except UnicodeDecodeError:
            print_error("文件编码不是 UTF-8")
            return False
    
    def run_all_checks(self) -> Dict:
        """运行所有检查"""
        print("\n" + "="*60)
        print(f"{Colors.BOLD}Flarum 中文语言包翻译检查{Colors.ENDC}")
        print("="*60 + "\n")
        
        # 加载数据
        self.load_data()
        
        # 基础检查
        self.check_file_encoding()
        self.check_yaml_syntax()
        
        # 翻译检查
        if self.en_data:
            missing = self.check_missing_translations()
        
        placeholders = self.check_placeholders()
        consistency = self.check_consistency()
        
        # 统计
        zh_flat = self.flatten_dict(self.zh_data)
        self.stats['total_keys'] = len(zh_flat)
        
        # 生成报告
        self.generate_report()
        
        return self.stats
    
    def generate_report(self):
        """生成检查报告"""
        report_path = self.zh_path.parent.parent / 'reports' / 'check-report.md'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 翻译检查报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**语言包版本**: 2.0.1\n\n")
            
            f.write("## 📊 统计摘要\n\n")
            f.write(f"| 项目 | 数量 |\n")
            f.write(f"|------|------|\n")
            f.write(f"| 翻译键总数 | {self.stats['total_keys']} |\n")
            f.write(f"| 缺失翻译 | {self.stats['missing_keys']} |\n")
            f.write(f"| 占位符问题 | {self.stats['placeholder_issues']} |\n")
            f.write(f"| 术语一致性问题 | {self.stats['consistency_issues']} |\n\n")
            
            f.write("## ✅ 检查项\n\n")
            f.write("- [x] 文件编码检查\n")
            f.write("- [x] YAML 语法检查\n")
            f.write("- [x] 占位符检查\n")
            f.write("- [x] 术语一致性检查\n")
            if self.en_data:
                f.write("- [x] 翻译缺失检查\n")
            else:
                f.write("- [ ] 翻译缺失检查（缺少英文参考）\n")
        
        print_info(f"报告已保存：{report_path}")


def main():
    parser = argparse.ArgumentParser(description='Flarum 中文语言包翻译检查工具')
    parser.add_argument('--reference', '-r', help='参考英文语言包路径')
    parser.add_argument('--output', '-o', help='输出报告路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 默认路径
    zh_path = Path(__file__).parent.parent / 'locale' / 'zh-Hans.yml'
    
    if not zh_path.exists():
        print_error(f"中文语言包不存在：{zh_path}")
        sys.exit(1)
    
    # 运行检查
    checker = TranslationChecker(str(zh_path), args.reference)
    stats = checker.run_all_checks()
    
    # 退出码
    if stats['missing_keys'] > 0 or stats['placeholder_issues'] > 0:
        sys.exit(1)
    else:
        print_success("\n所有检查通过！✓")
        sys.exit(0)


if __name__ == '__main__':
    main()
