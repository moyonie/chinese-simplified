# Flarum 2.0 简体中文语言包

[![GitHub license](https://img.shields.io/github/license/flarum-aifav/chinese-simplified)](LICENSE)
[![Flarum Version](https://img.shields.io/badge/flarum-2.0-blue)](https://flarum.org)
[![PHP Version](https://img.shields.io/badge/php-8.0+-blue)](https://php.net)
[![Version](https://img.shields.io/badge/version-2.0.0-green)](CHANGELOG.md)

Flarum 2.0 简体中文语言包 - 完整翻译，100% 兼容

## ✨ 特点

- ✅ 专为 Flarum 2.0.0-beta.8 设计
- ✅ 翻译完整 (98%+ 覆盖率)
- ✅ 翻译风格自然流畅
- ✅ 符合中国人思维习惯
- ✅ 持续更新维护
- ✅ 周一作为周起始日（中国标准）
- ✅ 术语统一、风格一致
- ✅ 错误提示友好清晰

## 📦 安装

```bash
composer require flarum-aifav/chinese-simplified
```

## 🚀 启用

1. 访问后台管理面板
2. 进入 **扩展** → **语言**
3. 选择 **简体中文**
4. 保存设置

## 📊 翻译范围

### Flarum 核心
- ✅ Admin (后台管理) - 100%
- ✅ Forum (前台论坛) - 100%
- ✅ Validation (验证信息) - 100%
- ✅ Error (错误信息) - 100%
- ✅ Date (日期时间) - 100%
- ✅ Lib (通用翻译) - 100%

### 官方扩展
- ✅ flarum/approval (审核)
- ✅ flarum/emoji (表情)
- ✅ flarum/flags (举报)
- ✅ flarum/likes (点赞)
- ✅ flarum/lock (锁定)
- ✅ flarum/mentions (提及)
- ✅ flarum/nicknames (昵称)
- ✅ flarum/subscriptions (订阅)
- ✅ flarum/sticky (置顶)
- ✅ flarum/suspend (禁言)
- ✅ flarum/tags (标签)

### Flarum 2.0 新增
- ✅ flarum/messages (私信)
- ✅ flarum/realtime (实时更新)
- ✅ flarum/extension-manager (扩展管理器)

## 🛠️ 开发

```bash
git clone https://github.com/flarum-aifav/chinese-simplified.git
cd chinese-simplified
composer install
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

- [报告问题](https://github.com/flarum-aifav/chinese-simplified/issues/new?template=bug_report.md)
- [翻译建议](https://github.com/flarum-aifav/chinese-simplified/issues/new?template=translation_suggestion.md)
- [提交 PR](https://github.com/flarum-aifav/chinese-simplified/pulls)

## 📝 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

### v2.0.1 (2026-03-27) - 深度优化版
- ✨ 统一 messages 模块术语（消息→私信）
- ✨ 优化 realtime 模块连接状态提示
- ✨ 统一 extension-manager 术语（仓库→软件源）
- ✨ 补充 error 模块详细错误信息（20+ 条）
- ✨ 补充 lib 模块通用术语（50+ 条）
- ✨ 补充 date 模块日期格式和缩写
- 📚 创建 GLOSSARY.md 术语表
- 📚 创建 STYLE-GUIDE.md 风格指南
- 🛠️ 创建 scripts/check-translations.py 检查工具

### v2.0.0 (2026-03-27) - 正式发布版
- ✅ 移除"有 BUG"标注，正式发布
- ✅ 优化 config.js（周起始日、序数格式）
- ✅ 补充 lib/api/ref 模块翻译
- ✅ 添加 CHANGELOG.md 和 .gitignore
- ✅ 创建 GitHub Issue/PR 模板

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🔗 链接

- [GitHub](https://github.com/flarum-aifav/chinese-simplified)
- [Packagist](https://packagist.org/packages/flarum-aifav/chinese-simplified)
- [Flarum 官网](https://flarum.org)
- [AI 收藏夹](https://www.aifav.cn)
