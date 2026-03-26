# Flarum 2.0 语言包技术架构深度分析

> 文档版本：1.0  
> 最后更新：2026-03-27  
> 目标读者：语言包维护团队、扩展开发者

---

## 目录

1. [Flarum 2.0 扩展架构变化](#1-flarum-20-扩展架构变化)
2. [前端国际化 (i18n)](#2-前端国际化-i18n)
3. [后端国际化](#3-后端国际化)
4. [性能优化](#4-性能优化)
5. [自动化流程](#5-自动化流程)
6. [最佳实践建议](#6-最佳实践建议)

---

## 1. Flarum 2.0 扩展架构变化

### 1.1 Flarum 1.x 与 2.0 语言包机制对比

#### Flarum 1.x 架构特点

- **翻译系统集成**: 基于 Symfony Translator 和 ICU MessageFormat
- **语言包结构**: 独立的扩展包，使用 `Flarum\Extend\LanguagePack` 扩展器
- **文件组织**: 
  - 翻译文件位于 `locale/` 目录
  - 按扩展 ID 命名：`EXTENSION_ID.yml`
  - DayJS 配置使用 `locale/config.js`

#### Flarum 2.0 架构演进

**核心变化**:

| 特性 | Flarum 1.x | Flarum 2.0 |
|------|------------|------------|
| PHP 版本要求 | 7.3+ | 8.1+ |
| Laravel 组件 | 8.x | 10.x+ |
| 依赖注入容器 | 基础支持 | 完整 Service Provider 模式 |
| TypeScript 支持 | 实验性 | 官方支持 (flarum-tsconfig) |
| 前端构建 | Webpack 4 | Webpack 5+ |
| 类型定义 | 有限 | 完整的 typings 系统 |

### 1.2 Provider 模式在语言包中的应用

Flarum 2.0 采用 Laravel 风格的 Service Provider 架构，语言包可以通过以下方式注册:

```php
<?php
// extend.php - 语言包入口
return new Flarum\Extend\LanguagePack();
```

**composer.json 配置**:

```json
{
  "name": "flarum/lang-chinese-simplified",
  "description": "Simplified Chinese Language Pack for Flarum",
  "type": "flarum-extension",
  "require": {
    "flarum/core": "^2.0.0"
  },
  "extra": {
    "flarum-extension": {
      "title": "Simplified Chinese",
      "icon": {
        "name": "fas fa-language",
        "backgroundColor": "#d93025",
        "color": "#fff"
      }
    },
    "flarum-locale": {
      "code": "zh-CN",
      "title": "简体中文"
    }
  },
  "autoload": {
    "psr-4": {
      "Flarum\\Lang\\ChineseSimplified\\": "src/"
    }
  }
}
```

### 1.3 依赖注入对翻译加载的影响

**服务容器集成**:

Flarum 使用 Laravel 的服务容器进行依赖注入，翻译服务通过容器自动注入:

```php
<?php
use Flarum\Locale\Translator;
use Flarum\Settings\SettingsRepositoryInterface;

class TranslationService
{
    protected $translator;
    protected $settings;
    
    public function __construct(
        Translator $translator,
        SettingsRepositoryInterface $settings
    ) {
        $this->translator = $translator;
        $this->settings = $settings;
    }
    
    public function translate(string $key, array $params = []): string
    {
        return $this->translator->trans($key, $params);
    }
}
```

**翻译加载流程**:

1. 用户请求到达 → 检测用户语言偏好
2. 从 `SettingsRepository` 获取论坛默认语言
3. 通过容器解析 `Translator` 实例
4. 加载对应语言的 YAML 翻译文件
5. 缓存翻译结果到 `cache/translations/` 目录
6. 返回翻译后的字符串

**优先级顺序**:

```
用户首选语言 → 论坛默认语言 → 英文回退 → 翻译键 (兜底)
```

---

## 2. 前端国际化 (i18n)

### 2.1 DayJS 配置最佳实践

**语言包中的 DayJS 配置**:

```javascript
// locale/config.js
dayjs.locale('zh-cn');

// 可选：自定义 locale 配置
dayjs.updateLocale('zh-cn', {
  months: [
    '一月', '二月', '三月', '四月', '五月', '六月',
    '七月', '八月', '九月', '十月', '十一月', '十二月'
  ],
  monthsShort: ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月', '7 月', '8 月', '9 月', '10 月', '11 月', '12 月'],
  weekdays: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
  weekdaysShort: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
  weekdaysMin: ['日', '一', '二', '三', '四', '五', '六'],
  relativeTime: {
    future: '%s内',
    past: '%s前',
    s: '几秒',
    m: '1 分钟',
    mm: '%d 分钟',
    h: '1 小时',
    hh: '%d 小时',
    d: '1 天',
    dd: '%d 天',
    M: '1 个月',
    MM: '%d 个月',
    y: '1 年',
    yy: '%d 年'
  }
});
```

**在组件中使用**:

```typescript
import app from 'flarum/common/components/app';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

// 格式化时间
const formattedTime = dayjs(post.createdAt()).format('YYYY-MM-DD HH:mm');
const relativeTime = dayjs(post.createdAt()).fromNow();

// 使用翻译
const label = app.translator.trans('core.lib.time_ago', { time: relativeTime });
```

### 2.2 前端组件的翻译加载机制

**Mithril.js 组件中的翻译**:

```typescript
import app from 'flarum/common/components/app';
import Component from 'flarum/common/Component';
import Button from 'flarum/common/components/Button';

export default class DiscussionList extends Component {
  view() {
    return (
      <div className="DiscussionList">
        <h1>{app.translator.trans('core.views.discussion_list.title')}</h1>
        <Button>
          {app.translator.trans('core.views.discussion_list.compose_button')}
        </Button>
      </div>
    );
  }
}
```

**翻译键命名规范**:

```yaml
# 标准格式：vendor-extension.section.subsection.key
flarum-core:
  views:
    discussion_list:
      title: "讨论列表"
      compose_button: "新建讨论"
  lib:
    time_ago: "{time}前"
    number_separator: ","
```

**实时翻译更新**:

Flarum 前端在初始化时加载翻译，不支持运行时动态切换语言。如需切换:

1. 用户更改语言设置
2. 设置保存到服务器
3. 页面刷新/重新加载
4. 新语言包在初始化时加载

**优化方案 - 按需加载**:

```typescript
// 扩展可以注册额外的翻译文件
app.initializers.add('my-extension', (app) => {
  // 延迟加载大型翻译模块
  if (app.current.user && app.current.user.isAdmin()) {
    import('./admin-translations').then((translations) => {
      app.translator.addTranslations(translations.default);
    });
  }
});
```

### 2.3 前端翻译文件结构

```
locale/
├── config.js              # DayJS 和前端配置
├── core.yml              # 核心翻译
├── flarum-approval.yml   # 扩展翻译
├── flarum-flags.yml
├── flarum-lock.yml
├── flarum-markdown.yml
├── flarum-mentions.yml
├── flarum-statistics.yml
├── flarum-sticky.yml
├── flarum-subscriptions.yml
├── flarum-suspend.yml
├── flarum-tags.yml
└── flarum-emoji.yml
```

---

## 3. 后端国际化

### 3.1 Laravel 翻译系统的集成

Flarum 后端使用 Laravel 框架，翻译系统基于 Laravel Localization:

**翻译文件位置**:

```
# Flarum 核心
/vendor/flarum/core/locale/

# 语言包
/vendor/flarum/lang-chinese-simplified/locale/

# 扩展覆盖
/locale/vendor/{package}/{locale}/
```

**Laravel 风格翻译**:

```php
<?php
// lang/zh-CN/messages.php
return [
    'welcome' => '欢迎使用 :appname!',
    'posts_count' => '{0} 没有帖子|[1,19] 有 :count 个帖子|[20,*] 有很多帖子',
];
```

**在 PHP 中使用**:

```php
<?php
use Flarum\Locale\Translator;

class NotificationMailer
{
    protected $translator;
    
    public function __construct(Translator $translator)
    {
        $this->translator = $translator;
    }
    
    public function sendNewPostNotification($user, $post)
    {
        $subject = $this->translator->trans('core.email.new_post.subject', [
            '{discussionTitle}' => $post->discussion->title,
            '{forumTitle}' => $this->settings->get('forum_title')
        ]);
        
        $body = $this->translator->trans('core.email.new_post.body', [
            '{username}' => $post->user->display_name,
            '{content}' => $post->content,
        ]);
        
        // 发送邮件...
    }
}
```

### 3.2 验证消息的翻译处理

**Laravel 验证规则翻译**:

```yaml
# flarum-core.yml
flarum-core:
  validation:
    username:
      required: "用户名是必填项"
      taken: "该用户名已被使用"
      invalid: "用户名格式不正确"
    email:
      required: "邮箱是必填项"
      taken: "该邮箱已被注册"
      invalid: "邮箱格式不正确"
    password:
      required: "密码是必填项"
      min: "密码长度至少为 :min 位"
```

**自定义验证器**:

```php
<?php
use Illuminate\Support\Facades\Validator;
use Flarum\Locale\Translator;

class CustomValidator
{
    protected $translator;
    
    public function __construct(Translator $translator)
    {
        $this->translator = $translator;
    }
    
    public function validate(array $data)
    {
        Validator::extend('valid_discussion_title', function ($attribute, $value, $parameters, $validator) {
            if (strlen($value) < 3) {
                $validator->addReplacer('valid_discussion_title', function ($message, $attribute, $rule, $parameters) {
                    return $this->translator->trans('core.validation.discussion_title.too_short');
                });
                return false;
            }
            return true;
        });
    }
}
```

### 3.3 邮件模板的翻译支持

**邮件模板结构**:

```yaml
# core.yml - 邮件翻译
flarum-core:
  email:
    activation:
      subject: "激活您的账户 - {forumTitle}"
      body: |
        您好 {username},
        
        欢迎注册 {forumTitle}!
        
        请点击以下链接激活您的账户:
        {url}
        
        如果这不是您操作，请忽略此邮件。
        
        此致，
        {forumTitle} 团队
    
    new_post:
      subject: "新回复：{discussionTitle}"
      body: |
        您好 {recipientDisplayName},
        
        {username} 在讨论 "{discussionTitle}" 中回复了您:
        
        ---
        {content}
        ---
        
        查看讨论：{url}
    
    password_reset:
      subject: "密码重置请求 - {forumTitle}"
      body: |
        您好 {username},
        
        我们收到您的密码重置请求。
        
        请点击以下链接重置密码:
        {url}
        
        如果您没有请求重置密码，请忽略此邮件。
```

**邮件发送器实现**:

```php
<?php
use Flarum\Mail\DriverInterface;
use Flarum\Locale\Translator;
use Illuminate\Mail\Mailer;

class TranslatedMailer
{
    protected $mailer;
    protected $translator;
    
    public function __construct(Mailer $mailer, Translator $translator)
    {
        $this->mailer = $mailer;
        $this->translator = $translator;
    }
    
    public function sendEmailTemplate(string $template, array $data)
    {
        $subject = $this->translator->trans("core.email.{$template}.subject", $data);
        $body = $this->translator->trans("core.email.{$template}.body", $data);
        
        $this->mailer->send(
            'emails.plain',
            ['content' => $body],
            function ($message) use ($data, $subject) {
                $message->to($data['recipient'])
                        ->subject($subject);
            }
        );
    }
}
```

---

## 4. 性能优化

### 4.1 翻译缓存机制

**Flarum 缓存策略**:

```php
<?php
// Flarum\Locale\Translator 内部实现

class Translator
{
    protected $cache;
    protected $locale;
    protected $translations = [];
    
    public function trans(string $key, array $params = []): string
    {
        // 检查内存缓存
        if (isset($this->translations[$this->locale][$key])) {
            return $this->interpolate($this->translations[$this->locale][$key], $params);
        }
        
        // 检查文件缓存
        $cached = $this->cache->get("translations.{$this->locale}");
        if ($cached) {
            $this->translations[$this->locale] = $cached;
            return $this->interpolate($cached[$key] ?? $key, $params);
        }
        
        // 加载翻译文件
        $this->loadTranslations();
        $this->cache->set("translations.{$this->locale}", $this->translations[$this->locale]);
        
        return $this->interpolate($this->translations[$this->locale][$key] ?? $key, $params);
    }
}
```

**缓存优化建议**:

```yaml
# config.php 配置
'cache' => [
    'driver' => 'file',  // 或 redis, memcached
    'prefix' => 'flarum_',
    'ttl' => 3600,  // 翻译缓存 1 小时
],
```

**Redis 缓存实现**:

```php
<?php
use Illuminate\Redis\RedisManager;

class RedisTranslationCache
{
    protected $redis;
    
    public function __construct(RedisManager $redis)
    {
        $this->redis = $redis;
    }
    
    public function get(string $locale): ?array
    {
        $cached = $this->redis->get("flarum:translations:{$locale}");
        return $cached ? json_decode($cached, true) : null;
    }
    
    public function set(string $locale, array $translations): void
    {
        $this->redis->setex(
            "flarum:translations:{$locale}",
            3600,
            json_encode($translations)
        );
    }
    
    public function clear(string $locale = null): void
    {
        if ($locale) {
            $this->redis->del("flarum:translations:{$locale}");
        } else {
            $keys = $this->redis->keys("flarum:translations:*");
            if ($keys) {
                $this->redis->del($keys);
            }
        }
    }
}
```

### 4.2 按需加载翻译

**前端按需加载策略**:

```typescript
// src/forum/index.ts
import app from 'flarum/common/components/app';

app.initializers.add('my-extension', (app) => {
  // 基础翻译立即加载
  const coreTranslations = require('../../locale/core.yml');
  app.translator.addTranslations(coreTranslations);
  
  // 管理面板翻译延迟加载
  if (app.current.user?.can('administrate')) {
    import('../../locale/admin.yml').then((adminTranslations) => {
      app.translator.addTranslations(adminTranslations.default);
    });
  }
});
```

**后端懒加载**:

```php
<?php
// 使用生成器延迟加载大型翻译文件
class TranslationLoader
{
    public function loadLocale(string $locale): Generator
    {
        $file = __DIR__ . "/locale/{$locale}.yml";
        if (!file_exists($file)) {
            return;
        }
        
        $translations = Yaml::parseFile($file);
        foreach ($translations as $extension => $messages) {
            yield $extension => $messages;
        }
    }
}
```

### 4.3 减少翻译文件体积

**优化技巧**:

1. **移除冗余翻译**:
```yaml
# ❌ 不推荐 - 重复定义
flarum-core:
  button:
    submit: "提交"
    save: "保存"
    confirm: "确认"
  
# ✅ 推荐 - 使用参数
flarum-core:
  button:
    action: "{action}"
  # 在代码中使用
  # translator.trans('core.button.action', {action: '提交'})
```

2. **合并相似翻译**:
```yaml
# ❌ 不推荐
flarum-core:
  time:
    minute_ago: "1 分钟前"
    minutes_ago_2: "2 分钟前"
    minutes_ago_3: "3 分钟前"
    
# ✅ 推荐 - 使用 ICU 复数格式
flarum-core:
  time:
    minutes_ago: "{count} 分钟前"
```

3. **使用短键 vs 原文键**:

```yaml
# 短键 (适合小型项目)
flarum-core:
  welcome_msg: "欢迎来到论坛"
  
# 原文键 (适合大型项目，便于维护)
# locale/zh-CN.json
{
  "Welcome to the forum": "欢迎来到论坛",
  "Create a new discussion": "创建新讨论"
}
```

**文件压缩建议**:

```bash
# 构建时压缩 YAML 文件
npm run build

# 使用 webpack 进行 tree-shaking
# webpack.config.js
module.exports = {
  optimization: {
    usedExports: true,  // tree-shaking
    minimize: true,
  }
};
```

---

## 5. 自动化流程

### 5.1 翻译缺失检测脚本

**Python 检测脚本**:

```python
#!/usr/bin/env python3
"""
Flarum 语言包翻译缺失检测工具
用法：python detect_missing.py --source en --target zh-CN
"""

import yaml
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Set, Any

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """将嵌套字典展平为键值对"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def load_yaml_file(filepath: Path) -> Dict:
    """加载 YAML 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def load_json_file(filepath: Path) -> Dict:
    """加载 JSON 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f) or {}

def compare_translations(source: Dict, target: Dict) -> Dict:
    """比较源语言和目标语言的翻译"""
    source_flat = flatten_dict(source)
    target_flat = flatten_dict(target)
    
    missing = {}
    for key, value in source_flat.items():
        if key not in target_flat:
            missing[key] = value
        elif target_flat[key] == key:  # 未翻译，直接使用键
            missing[key] = value
    
    return missing

def detect_missing(source_locale: str, target_locale: str, output_format: str = 'console'):
    """检测翻译缺失"""
    locale_dir = Path('locale')
    missing_report = {}
    
    # 获取所有翻译文件
    source_files = list(locale_dir.glob(f'*.{source_locale}.yml'))
    if not source_files:
        # 尝试无语言后缀的文件 (如 core.yml)
        source_files = list(locale_dir.glob('*.yml'))
    
    for source_file in source_files:
        filename = source_file.stem
        target_file = locale_dir / f"{filename}.{target_locale}.yml"
        
        if not target_file.exists():
            missing_report[str(source_file)] = {"error": "文件不存在"}
            continue
        
        source_data = load_yaml_file(source_file)
        target_data = load_yaml_file(target_file)
        
        missing = compare_translations(source_data, target_data)
        if missing:
            missing_report[str(source_file)] = missing
    
    # 输出报告
    if output_format == 'json':
        print(json.dumps(missing_report, ensure_ascii=False, indent=2))
    elif output_format == 'console':
        total_missing = sum(len(v) for v in missing_report.values() if isinstance(v, dict) and 'error' not in v)
        print(f"\n📊 翻译缺失检测报告")
        print(f"源语言：{source_locale}")
        print(f"目标语言：{target_locale}")
        print(f"缺失翻译数：{total_missing}")
        print("=" * 50)
        
        for file, missing in missing_report.items():
            if isinstance(missing, dict) and 'error' in missing:
                print(f"\n❌ {file}: {missing['error']}")
            elif missing:
                print(f"\n⚠️  {file}:")
                for key, value in list(missing.items())[:10]:  # 只显示前 10 个
                    print(f"   - {key}: {value[:50]}...")
                if len(missing) > 10:
                    print(f"   ... 还有 {len(missing) - 10} 条缺失")
    
    return missing_report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flarum 语言包翻译缺失检测')
    parser.add_argument('--source', default='en', help='源语言 (默认：en)')
    parser.add_argument('--target', required=True, help='目标语言')
    parser.add_argument('--format', choices=['console', 'json'], default='console')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    report = detect_missing(args.source, args.target, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 报告已保存到：{args.output}")
```

**GitHub Actions 集成**:

```yaml
# .github/workflows/translation-check.yml
name: Translation Check

on:
  push:
    paths:
      - 'locale/**'
  pull_request:
    paths:
      - 'locale/**'
  schedule:
    - cron: '0 0 * * 1'  # 每周一检查

jobs:
  check-translations:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install pyyaml
    
    - name: Check translation completeness
      run: |
        python detect_missing.py --source en --target zh-CN --format json --output report.json
    
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: translation-report
        path: report.json
    
    - name: Comment on PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = JSON.parse(fs.readFileSync('report.json', 'utf8'));
          const missingCount = Object.values(report).reduce((sum, v) => 
            sum + (typeof v === 'object' && !v.error ? Object.keys(v).length : 0), 0);
          
          if (missingCount > 0) {
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `⚠️ 发现 ${missingCount} 条缺失翻译，请查看报告附件。`
            });
          }
```

### 5.2 与官方英文包同步更新流程

**同步脚本**:

```bash
#!/bin/bash
# sync-with-official.sh
# 同步官方英文翻译包

set -e

OFFICIAL_REPO="flarum/lang-english"
LOCAL_LOCALE_DIR="locale"
TEMP_DIR=$(mktemp -d)

echo "🔄 开始同步官方英文包..."

# 克隆官方仓库
git clone --depth 1 https://github.com/$OFFICIAL_REPO.git $TEMP_DIR

# 对比文件
echo "📋 对比文件差异..."
diff -rq $TEMP_DIR/locale/ $LOCAL_LOCALE_DIR/ --exclude="*.zh-CN.yml" --exclude="config.js" || true

# 更新核心翻译文件
for file in $TEMP_DIR/locale/*.yml; do
    filename=$(basename $file)
    if [ -f "$LOCAL_LOCALE_DIR/$filename" ]; then
        echo "✓ $filename 已存在"
    else
        echo "⚠️  新增文件：$filename"
        cp $file $LOCAL_LOCALE_DIR/
    fi
done

# 清理
rm -rf $TEMP_DIR

echo "✅ 同步完成"
echo "📝 请运行检测脚本检查缺失翻译：python detect_missing.py --source en --target zh-CN"
```

**自动化同步 (GitHub Actions)**:

```yaml
# .github/workflows/sync-official.yml
name: Sync with Official English Pack

on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日凌晨 2 点
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Sync official translations
      run: |
        bash sync-with-official.sh
    
    - name: Check for changes
      id: git-check
      run: |
        git diff --quiet || echo "has_changes=true" >> $GITHUB_OUTPUT
    
    - name: Create Pull Request
      if: steps.git-check.outputs.has_changes == 'true'
      uses: peter-evans/create-pull-request@v5
      with:
        commit-message: 'chore: sync with official English pack'
        branch: sync-official-${{ github.run_number }}
        title: 'Sync with official English language pack'
        body: |
          自动同步官方英文语言包。
          
          请检查：
          - 新增的翻译文件
          - 需要翻译的缺失项
          
          运行以下命令检测缺失：
          ```bash
          python detect_missing.py --source en --target zh-CN
          ```
```

### 5.3 CI/CD 集成建议

**完整的 CI/CD 流程**:

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Set up PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.2'
    
    - name: Install dependencies
      run: |
        composer install --no-interaction
        cd js && npm ci
    
    - name: Lint YAML files
      run: |
        for file in locale/*.yml; do
          python -c "import yaml; yaml.safe_load(open('$file'))" || exit 1
        done
    
    - name: Check translation completeness
      run: |
        python detect_missing.py --source en --target zh-CN --format json --output report.json
    
    - name: Build frontend
      run: |
        cd js && npm run build
    
    - name: Run tests
      run: composer test
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: |
          js/dist/
          locale/

  publish:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Get version
      id: version
      run: echo "version=$(composer show --format=json | jq -r '.version')" >> $GITHUB_OUTPUT
    
    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        tag_name: v${{ steps.version.outputs.version }}
        generate_release_notes: true
    
    - name: Publish to Packagist
      uses: dissimulate/action-packagist@master
      with:
        username: ${{ secrets.PACKAGIST_USERNAME }}
        api_token: ${{ secrets.PACKAGIST_API_TOKEN }}
```

**预提交钩子**:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 运行预提交检查..."

# 检查 YAML 语法
for file in $(git diff --cached --name-only | grep 'locale/.*\.yml$'); do
    python -c "import yaml; yaml.safe_load(open('$file'))" || {
        echo "❌ YAML 语法错误：$file"
        exit 1
    }
done

# 检查翻译完整性
if git diff --cached --name-only | grep -q 'locale/.*\.yml$'; then
    python detect_missing.py --source en --target zh-CN --format console || {
        echo "⚠️  存在缺失翻译，请补充"
        # 不阻止提交，仅警告
    }
fi

echo "✅ 预提交检查通过"
```

---

## 6. 最佳实践建议

### 6.1 翻译键命名规范

```yaml
# ✅ 推荐
flarum-extension-name:
  section:
    subsection:
      key: "翻译内容"

# ❌ 避免
flarum-extension-name:
  section_subsection_key: "翻译内容"  # 使用下划线而非嵌套
```

### 6.2 变量占位符规范

```yaml
# ✅ 推荐 - 使用花括号
flarum-core:
  greeting: "你好，{username}！"
  count: "共 {count} 条"

# ❌ 避免 - 混用格式
flarum-core:
  greeting: "你好，:username！"  # Laravel 风格
  count: "共 %count 条"  # printf 风格
```

### 6.3 复数形式处理

```yaml
# ✅ 推荐 - ICU 格式
flarum-core:
  posts_count: "{0} 暂无帖子|[1,9] :count 个帖子|[10,*] :count+ 个帖子"

# ❌ 避免 - 硬编码
flarum-core:
  post_1: "1 个帖子"
  post_2: "2 个帖子"
  post_3: "3 个帖子"
```

### 6.4 HTML 标签处理

```yaml
# ✅ 推荐 - 使用 <a> 占位符
flarum-core:
  link_text: "请查看 <a>帮助文档</a>"

# 在代码中:
translator.trans('core.link_text', [], {
  'a': <a href="/help">帮助文档</a>
})
```

### 6.5 团队协作流程

```
1. 官方英文包更新 → 触发同步脚本
2. 检测缺失翻译 → 生成报告
3. 分配翻译任务 → 团队成员认领
4. 提交翻译 → PR 审核
5. CI 检查 → 自动验证
6. 合并发布 → 更新语言包
```

---

## 附录

### A. 常用资源链接

- [Flarum 官方文档](https://docs.flarum.org/)
- [Flarum GitHub](https://github.com/flarum/framework)
- [官方英文语言包](https://github.com/flarum/lang-english)
- [Laravel 本地化文档](https://laravel.com/docs/localization)
- [DayJS 文档](https://day.js.org/)
- [ICU MessageFormat](https://unicode-org.github.io/icu/userguide/format_parse/messages/)

### B. 工具清单

| 工具 | 用途 | 链接 |
|------|------|------|
| flarum-cli | 扩展脚手架 | https://github.com/flarum/cli |
| PyYAML | YAML 解析 | https://pypi.org/project/PyYAML/ |
| flarum-tsconfig | TypeScript 配置 | https://github.com/flarum/flarum-tsconfig |

### C. 版本兼容性

| Flarum 版本 | PHP 版本 | 语言包版本 |
|-------------|----------|------------|
| 1.x | 7.3+ | ^1.0 |
| 2.0 Beta | 8.1+ | ^2.0@beta |
| 2.0 Stable | 8.1+ | ^2.0 |

---

*本文档由 Flarum 中文语言包团队维护，欢迎贡献和改进。*
