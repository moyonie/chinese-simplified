# 第三方插件翻译

本目录包含 Flarum 第三方插件的中文翻译文件。

## 目录结构

```
third-party/
├── fof/                          # FriendsOfFlarum 系列插件
│   ├── fof-best-answer.yml       # 最佳回答
│   ├── fof-byobu.yml             # 私密对话
│   ├── fof-drafts.yml            # 草稿箱
│   ├── fof-filter.yml            # 内容过滤
│   ├── fof-links.yml             # 链接管理
│   ├── fof-polls.yml             # 投票功能
│   ├── fof-sitemap.yml           # SEO 站点地图
│   ├── fof-spamblock.yml         # 反垃圾邮件
│   └── fof-user-directory.yml    # 用户目录
├── v17development/               # v17development 系列插件
└── ianm/                         # IanM 系列插件
```

## 文件命名规则

翻译文件名必须与插件 ID 完全匹配：

| 插件包名 | 翻译文件名 |
|---------|-----------|
| `fof/best-answer` | `fof-best-answer.yml` |
| `fof/byobu` | `fof-byobu.yml` |
| `v17development/flarum-seo` | `v17development-flarum-seo.yml` |

**规则**：插件包名中的 `/` 替换为 `-`

## 已翻译插件（P0 优先级）

### FriendsOfFlarum (FoF) 系列

| 插件 | 状态 | 翻译数 |
|------|------|--------|
| fof-best-answer | ✅ 完成 | 58 行 |
| fof-byobu | ✅ 完成 | 59 行 |
| fof-drafts | ✅ 完成 | 46 行 |
| fof-filter | ✅ 完成 | 57 行 |
| fof-links | ✅ 完成 | 53 行 |
| fof-polls | ✅ 完成 | 94 行 |
| fof-sitemap | ✅ 完成 | 42 行 |
| fof-spamblock | ✅ 完成 | 65 行 |
| fof-user-directory | ✅ 完成 | 76 行 |

**总计**: 9 个插件，550 行翻译

## 待翻译插件（P1-P3 优先级）

### P1 - 热门
- [ ] fof-analytics - 统计分析
- [ ] fof-auth-discord - Discord 登录
- [ ] fof-badges - 用户徽章
- [ ] fof-ban-ips - IP 封禁
- [ ] fof-console - 控制台命令
- [ ] fof-custom-footer - 自定义页脚
- [ ] fof-default-group - 默认用户组
- [ ] fof-discussion-views - 浏览数统计
- [ ] fof-doorman - 邀请码注册
- [ ] fof-nightmode - 夜间模式

### P2 - 常用
- [ ] fof-cookies - Cookie 同意
- [ ] fof-formatting - 格式增强
- [ ] fof-impersonate - 用户模拟
- [ ] fof-oauth - OAuth 认证
- [ ] fof-pwa - PWA 支持
- [ ] fof-react-actions - 快速操作
- [ ] fof-recaptcha - 验证码
- [ ] fof-share-discussion - 分享功能
- [ ] fof-subscribed - 订阅标签页
- [ ] fof-terms - 服务条款

### P3 - 其他
- [ ] v17development-flarum-seo - SEO 优化
- [ ] v17development-flarum-user-tags - 用户标签
- [ ] matteocontrini-flarum-imgur-upload - Imgur 图片上传
- [ ] ianm-html-head - HTML 头部管理
- [ ] ianm-syndication - RSS 订阅
- [ ] ianm-twofactor - 两步验证
- [ ] clarkwinkelmann 系列插件

## 添加新插件翻译

### 步骤 1: 确认插件 ID

```bash
composer show fof/byobu | grep name
# 输出：name : fof/byobu
```

### 步骤 2: 创建翻译文件

```bash
# 在对应厂商目录下创建文件
touch locale/third-party/fof/fof-byobu.yml
```

### 步骤 3: 参考英文翻译

查看插件的英文翻译文件：
```bash
cat vendor/fof/byobu/locale/en.yml
```

### 步骤 4: 创建中文翻译

```yaml
fof-byobu:
  admin:
    permissions:
      start_byobu: 发起私密对话
  forum:
    composer:
      byobu_title: 私密对话标题
```

### 步骤 5: 提交

```bash
git add locale/third-party/fof/fof-byobu.yml
git commit -m "feat: 添加 fof/byobu 中文翻译"
git push
```

## 使用说明

用户安装中文语言包后，Flarum 会自动加载这些翻译文件：

```bash
composer require flarum-aifav/chinese-simplified
```

然后在管理面板启用简体中文即可。

## 维护

- 定期检查第三方插件更新
- 插件新增翻译键时及时补充
- 保持术语与官方翻译一致
- 参考 `../GLOSSARY.md` 术语表

---

**最后更新**: 2026-03-27  
**维护者**: AI Favorites Team
