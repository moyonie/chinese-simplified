# 更新日志

所有重要的项目变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [2.0.0] - 2026-03-27

### ✅ 已修复
- 更新 description，移除"有 BUG，暂时不可用"标注
- 优化 config.js，添加 `weekStart: 1`（周一作为周起始日）
- 优化 config.js，添加序数格式配置
- 补充 lib/api/ref 模块翻译

### 📝 已添加
- CHANGELOG.md 更新日志文件
- .gitignore 文件

### 🔄 已更新
- 翻译完整性达到 92%+
- 完全兼容 Flarum 2.0.0-beta.8

---

## [2.0.0-beta] - 2026-03-26

### ✨ 新增
- 完整支持 Flarum 2.0.0-beta.8
- 翻译核心模块（forum/admin/validation/lib/date/error）
- 翻译官方扩展（approval/emoji/flags/likes/lock/mentions/subscriptions/sticky/suspend/tags）
- 翻译 Flarum 2.0 新增功能（messages/realtime/extension-manager）

### 🔧 技术
- 使用 Flarum 2.0 正确的 extend.php API
- 配置 locale code 为 zh-Hans
- 添加 icon.svg 图标
- 确保所有文件为 UTF-8 编码

---

## 版本说明

### 版本号规则
- **主版本号**：跟随 Flarum 主版本（如 Flarum 2.0 → 2.x.x）
- **次版本号**：重大功能更新或翻译大幅补充
- **修订号**：bug 修复、翻译修正、小改进

### 符号说明
- ✨ 新增功能
- 🐛 Bug 修复
- ✅ 已修复
- 📝 文档更新
- 🔄 更新/改进
- 🔧 技术变更
- ⚡ 性能优化
