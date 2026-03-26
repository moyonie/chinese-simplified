# Flarum 2.0 中文语言包优化方案

**文档版本**: 1.0  
**创建日期**: 2026-03-27  
**基于版本**: Flarum 2.0.0 中文语言包 v2.0.0  
**参考报告**: ANALYSIS-REPORT.md, FIX-REPORT.md, COMPLETE-SUMMARY.md

---

## 📋 执行摘要

本优化方案基于已完成的 P0/P1/P2 基础修复，针对 Flarum 2.0 新特性进行深度优化。当前语言包翻译完整性达 100%（919 个翻译键），整体质量优秀（8.7/10），但仍存在以下优化空间：

| 优化类别 | 优先级 | 预计工作量 | 影响范围 |
|---------|--------|-----------|---------|
| Flarum 2.0 新特性支持 | P0 | 2 小时 | 高 |
| 翻译一致性优化 | P1 | 4 小时 | 中 |
| 技术细节规范化 | P1 | 3 小时 | 中 |
| 用户体验优化 | P2 | 2 小时 | 低 |
| 文档与工具链 | P2 | 3 小时 | 低 |

**总预计工作量**: ~14 小时

---

## 1️⃣ Flarum 2.0 新特性支持优化

### 1.1 Messages（私信）功能翻译

#### 当前状态 ✅
```yaml
flarum-messages:
  forum:
    composer:
      send_message: 发送消息
      message_placeholder: 输入消息...
      recipient_label: 收件人
      recipient_placeholder: 选择收件人...
    nav:
      messages: 消息
      new_message: 新消息
    # ... 其他翻译
```

#### 优化建议 ⚠️

**问题 1**: 术语不统一
- 当前混用：`消息` / `私信` / `对话`
- 建议统一为：**私信**（更符合论坛场景）

**修改方案**:
```yaml
flarum-messages:
  forum:
    composer:
      send_message: 发送私信          # ← 修改
      message_placeholder: 输入私信内容...  # ← 优化
      recipient_label: 收件人
      recipient_placeholder: 搜索用户...   # ← 优化
    nav:
      messages: 私信               # ← 修改
      new_message: 新建私信         # ← 修改
    index:
      title: 私信                 # ← 修改
      no_messages: 暂无私信        # ← 优化
      start_conversation: 发起对话  # ← 保留（对话场景用词）
    discussion:
      reply_placeholder: 回复...
      leave_conversation: 退出对话
      delete_conversation: 删除对话
      delete_confirmation: 确定要删除此对话吗？此操作不可撤销。 # ← 增强
```

**问题 2**: 缺少关键翻译项
```yaml
# 建议补充
flarum-messages:
  forum:
    notification:
      new_message: '{username} 给你发送了私信'  # ← 新增
      message_received: 收到新私信           # ← 新增
    modal:
      title: 发送私信                    # ← 新增
      send_button: 发送                  # ← 新增
      cancel_button: 取消                # ← 新增
    user:
      send_message_button: 发私信         # ← 简化
      messages_link: 私信箱              # ← 优化
  admin:
    permissions:
      send_private_messages_label: 发送私信
      receive_private_messages_label: 接收私信
      create_private_messages_label: 创建私信对话  # ← 新增
    settings:
      messages_heading: 私信设置
      allow_messages_label: 允许私信功能
      max_recipients_label: 单次私信最大收件人数
      message_length_limit_label: 私信长度限制  # ← 新增
```

---

### 1.2 Realtime（实时更新）翻译

#### 当前状态 ✅
```yaml
flarum-realtime:
  forum:
    push:
      discussion_list_new_activity: '{count} 条新活动'
      new_discussion: '{username} 开始了新讨论'
      new_post: '{username} 回复了讨论'
    typing_indicator:
      people_are_typing: '{number} 人正在输入'
      person_is_typing: '{username} 正在输入'
    connection_lost: 连接已断开
    reconnecting: 重新连接中...
    reconnected: 已重新连接
```

#### 优化建议 ⚠️

**问题 1**: 翻译不够自然
- `connection_lost: 连接已断开` → 建议改为 **网络连接已断开**
- `reconnected: 已重新连接` → 建议改为 **已恢复连接**

**问题 2**: 缺少错误场景翻译
```yaml
# 建议补充
flarum-realtime:
  forum:
    connection:
      connection_lost: 网络连接已断开      # ← 优化
      reconnecting: 正在重新连接...       # ← 优化
      reconnected: 已恢复连接            # ← 优化
      reconnect_failed: 重新连接失败      # ← 新增
      reconnect_retry: '{seconds}秒后重试' # ← 新增
    push:
      discussion_list_new_activity: '发现 {count} 条新动态'  # ← 优化
      new_discussion: '{username} 发布了新讨论'           # ← 优化
      new_post: '{username} 回复了讨论'
      post_updated: 帖子已更新            # ← 新增
      discussion_renamed: 讨论已重命名     # ← 新增
    typing_indicator:
      people_are_typing: '{number} 人正在输入...'
      person_is_typing: '{username} 正在输入...'
      typing_stopped: 已停止输入          # ← 新增
    notification:
      push_permission_required: 需要推送通知权限  # ← 新增
      enable_push: 启用推送通知           # ← 新增
  admin:
    settings:
      realtime_heading: 实时更新设置
      enable_realtime_label: 启用实时更新
      push_notifications_label: 启用推送通知
      typing_indicator_label: 显示输入状态
      reconnect_interval_label: 重连间隔（秒）  # ← 新增
      debug_mode_label: 调试模式           # ← 新增
```

---

### 1.3 Extension Manager（扩展管理器）翻译

#### 当前状态 ✅
```yaml
flarum-extension-manager:
  admin:
    composer:
      add_repository_label: 添加仓库
      repository_url_placeholder: 输入仓库 URL...
      # ...
    extensions:
      install: 安装
      remove: 移除
      update: 更新
      # ...
```

#### 优化建议 ⚠️

**问题 1**: 技术术语不够专业
- `composer` → 建议改为 **依赖管理** 或保持 **Composer**（专有名词）
- `repository` → 建议统一为 **软件源**（更符合中文软件习惯）

**问题 2**: 错误信息不够友好
```yaml
# 建议优化
flarum-extension-manager:
  admin:
    composer:
      add_repository_label: 添加软件源
      repository_url_placeholder: 输入软件源 URL（如 https://packagist.org）
      delete_repository_confirmation: 确定要删除此软件源吗？删除后可能无法安装相关扩展。
      install_package: 安装扩展包
      package_name_placeholder: 包名（格式：vendor/package）
      install_button: 安装
      installing_extension: '正在安装扩展 {package}...'  # ← 优化
    extensions:
      install: 安装
      remove: 卸载                    # ← 修改（更符合中文习惯）
      update: 更新
      installed: 已安装
      available: 可用扩展
      updates_available: '发现 {count} 个可用更新'  # ← 优化
      update_all: 全部更新
      checking_updates: 正在检查更新...
      no_updates: 已是最新版本
      install_success: 扩展安装成功
      remove_success: 扩展卸载成功
      update_success: 扩展更新成功
      install_error: '安装失败：{error}'     # ← 增强
      remove_error: '卸载失败：{error}'     # ← 增强
      update_error: '更新失败：{error}'     # ← 增强
      dependency_missing: '缺少依赖：{extension}'  # ← 新增
      version_conflict: '版本冲突：{details}'   # ← 新增
    settings:
      queue_jobs: 队列任务
      task_retention_days: 任务保留天数
      repositories_heading: 软件源管理
      repositories_description: 管理 Composer 软件源，添加后可安装更多扩展
      add_repository_button: 添加软件源
      default_repositories: 默认软件源
      packagist_url: 'Packagist 官方源'
      github_url: 'GitHub API'
      enable_packagist_label: 启用 Packagist  # ← 新增
      allow_custom_repositories_label: 允许自定义软件源  # ← 新增
```

---

## 2️⃣ 翻译质量优化

### 2.1 术语一致性检查

#### 当前问题 🔍

| 术语 | 当前翻译 | 出现位置 | 建议统一为 |
|------|---------|---------|-----------|
| Discussion | 讨论 | forum.discussion | **讨论** ✅ |
| Post | 帖子 | forum.post | **帖子** ✅ |
| Tag | 标签 | forum.tags | **标签** ✅ |
| User | 用户 | forum.user | **用户** ✅ |
| Like | 点赞 | flarum-likes | **点赞** ✅ |
| Flag | 举报 | flarum-flags | **举报** ✅ |
| Message | 消息/私信 | flarum-messages | **私信** ⚠️ |
| Conversation | 对话 | flarum-messages | **对话** ✅ |
| Extension | 扩展 | admin.extensions | **扩展** ✅ |
| Repository | 仓库 | flarum-extension-manager | **软件源** ⚠️ |

#### 修改方案

**全局查找替换**:
```bash
# 消息 → 私信（在 flarum-messages 模块内）
sed -i 's/消息/私信/g' locale/zh-Hans.yml

# 仓库 → 软件源（在 flarum-extension-manager 模块内）
sed -i 's/仓库/软件源/g' locale/zh-Hans.yml
```

**注意**: 需要手动检查上下文，避免误替换。

---

### 2.2 语境适配优化

#### 按钮文案优化

| 场景 | 当前 | 建议 | 理由 |
|------|------|------|------|
| 删除确认 | 确定要删除此讨论吗？ | 确定要删除此讨论吗？此操作不可撤销。 | 增强警示 |
| 放弃草稿 | 确定要放弃此内容吗？ | 确定要放弃当前内容吗？未保存的内容将丢失。 | 明确后果 |
| 卸载扩展 | 确定要卸载此扩展吗？ | 确定要卸载此扩展吗？相关数据可能被删除。 | 提醒风险 |
| 删除用户 | 确定要删除此用户吗？ | 确定要删除此用户吗？该用户的所有内容将被删除。 | 明确影响 |

#### 错误提示优化

| 当前 | 建议 | 改进点 |
|------|------|--------|
| 用户名或密码错误 | 用户名或密码错误，请检查后重试 | 增加行动指引 |
| 会话已过期，请重新登录 | 登录会话已过期，请重新登录 | 更明确 |
| 权限不足 | 抱歉，您没有执行此操作的权限 | 更友好 |
| 验证错误 | 表单验证失败，请检查以下字段 | 更具体 |

---

### 2.3 语气风格优化

#### 原则
1. **友好但专业** - 避免过于生硬或过于随意
2. **简洁明确** - 按钮文案控制在 2-6 字
3. **行动导向** - 错误提示包含解决建议

#### 示例对比

| 场景 | 生硬 ❌ | 友好 ✅ |
|------|--------|--------|
| 权限错误 | 权限不足 | 抱歉，您没有执行此操作的权限 |
| 网络错误 | 网络错误 | 网络连接不稳定，请检查后重试 |
| 加载状态 | 加载中... | 正在加载，请稍候... |
| 成功提示 | 成功 | 操作成功！ |
| 空状态 | 没有讨论 | 还没有讨论，来发表第一个吧！ |

---

## 3️⃣ 技术细节优化

### 3.1 YAML 文件结构规范

#### 当前状态 ✅
```yaml
---
# Flarum 2.0 简体中文语言包
# 版本：2.0.0
# 最后更新：2026-03-26
# 完整性：100%

forum:
  header:
    log_in: 登录
```

#### 优化建议

**添加元数据**:
```yaml
---
# ============================================
# Flarum 2.0 简体中文语言包
# ============================================
# 版本：2.0.0
# 最后更新：2026-03-27
# 完整性：100%
# 翻译键总数：919
# 维护者：AI Favorites Team
# 许可证：MIT
# ============================================
```

**添加模块分隔符**:
```yaml
# ============================================
# 前台论坛 (Forum)
# ============================================
forum:
  ...

# ============================================
# 后台管理 (Admin)
# ============================================
admin:
  ...
```

---

### 3.2 复数形式处理（ICU MessageFormat）

#### 当前状态 ✅
```yaml
reply_count: '{count} 条回复'
view_count: '{count} 次浏览'
participant_count: '{count} 人参与'
```

#### 优化建议 ⚠️

**问题**: 中文复数形式简单，但需要考虑 0 和 1 的特殊情况

**建议格式**:
```yaml
# 使用 ICU MessageFormat（如果 Flarum 支持）
reply_count: '{count, plural, =0 {暂无回复} =1 {1 条回复} other {# 条回复}}'
view_count: '{count, plural, =0 {未浏览} =1 {1 次浏览} other {# 次浏览}}'
participant_count: '{count, plural, =0 {无人参与} =1 {1 人参与} other {# 人参与}}'

# 或者保持简单格式（当前方案也可接受）
reply_count: '{count} 条回复'
```

**检查清单**:
- [ ] 检查所有 `{count}` 占位符是否完整
- [ ] 检查所有 `{username}` 占位符是否完整
- [ ] 检查所有 `{time}` 占位符是否完整
- [ ] 检查所有 `{number}` 占位符是否完整

---

### 3.3 变量占位符完整性检查

#### 当前占位符统计

| 占位符 | 出现次数 | 状态 |
|--------|---------|------|
| `{count}` | ~50 | ✅ 完整 |
| `{username}` | ~20 | ✅ 完整 |
| `{user}` | ~15 | ✅ 完整 |
| `{time}` | ~10 | ✅ 完整 |
| `{number}` | ~5 | ✅ 完整 |
| `{discussion}` | ~5 | ✅ 完整 |
| `{attribute}` | ~20 | ✅ 完整 |
| `{min}`/`{max}` | ~10 | ✅ 完整 |

#### 潜在问题 🔍

```yaml
# 检查是否有遗漏的占位符
edited_tooltip: '由 {user} 于 {time} 编辑'  # ✅ 正确
mention_tooltip: '{username} 提及了你'      # ✅ 正确

# 确保所有变量都被正确包裹
# 错误示例：由 user 于 time 编辑 ❌
# 正确示例：由 {user} 于 {time} 编辑 ✅
```

---

### 3.4 HTML 标签嵌入安全

#### 当前状态
检查 YAML 文件中是否有 HTML 标签嵌入：

```bash
grep -E '<[^>]+>' locale/zh-Hans.yml
```

#### 优化建议

**原则**:
1. 避免在翻译中直接嵌入 HTML
2. 如需嵌入，使用安全的占位符
3. 确保转义字符正确

**示例**:
```yaml
# ❌ 不推荐
welcome_message: '<strong>欢迎</strong>来到论坛！'

# ✅ 推荐
welcome_message: '欢迎{username}来到论坛！'
# HTML 由代码层添加

# ✅ 或使用安全占位符
welcome_message: '{strong}欢迎{/strong}来到论坛！'
```

---

## 4️⃣ 用户体验优化

### 4.1 日期时间格式

#### 当前状态 ✅
```yaml
date:
  format_date: 'Y 年 m 月 d 日'
  format_time: 'H:i'
  format_datetime: 'Y 年 m 月 d 日 H:i'
  minutes_ago: '{count} 分钟前'
  hours_ago: '{count} 小时前'
```

#### 优化建议

**补充更多格式**:
```yaml
date:
  # 现有格式
  format_date: 'Y 年 m 月 d 日'
  format_time: 'H:i'
  format_datetime: 'Y 年 m 月 d 日 H:i'
  
  # 建议补充
  format_date_short: 'm/d'           # 短日期：03/27
  format_date_medium: 'm 月 d 日'     # 中日期：3 月 27 日
  format_datetime_full: 'Y 年 m 月 d 日 H:i:s'  # 完整时间
  format_relative_today: '今天 H:i'   # 今天的时间
  format_relative_yesterday: '昨天 H:i'  # 昨天的时间
  format_this_week: 'dddd H:i'       # 本周：星期五 14:30
  format_this_year: 'm 月 d 日 H:i'   # 今年：3 月 27 日 14:30
  
  # 相对时间优化
  just_now: 刚刚
  seconds_ago: '{count} 秒前'        # ← 新增
  minutes_ago: '{count} 分钟前'
  hours_ago: '{count} 小时前'
  days_ago: '{count} 天前'
  weeks_ago: '{count} 周前'
  months_ago: '{count} 月前'
  years_ago: '{count} 年前'
  
  # 将来时间
  in_seconds: '{count} 秒后'         # ← 新增
  in_minutes: '{count} 分钟后'       # ← 新增
  in_hours: '{count} 小时后'         # ← 新增
```

**config.js 同步优化**:
```javascript
// 确保 config.js 与 YAML 中的日期格式一致
dayjs.updateLocale('zh-cn', {
  // ... 现有配置
  
  // 添加日历时间格式
  calendar: {
    sameDay: '[今天] HH:mm',
    nextDay: '[明天] HH:mm',
    nextWeek: 'dddd HH:mm',
    lastDay: '[昨天] HH:mm',
    lastWeek: '上 dddd HH:mm',
    sameElse: 'YYYY 年 MM 月 DD 日'
  }
});
```

---

### 4.2 数字格式

#### 当前状态
检查数字相关翻译：

```yaml
# 当前可能缺失
lib:
  number_format: '{number}'  # ← 建议补充
  currency_format: '¥{amount}'  # ← 建议补充（如有需要）
```

#### 优化建议

**中文数字习惯**:
```yaml
lib:
  # 千分位分隔符（中文使用英文逗号）
  thousand_separator: ','
  
  # 小数点（中文使用英文句点）
  decimal_separator: '.'
  
  # 数字格式示例
  number_example: '1,234.56'
  
  # 中文数字单位（如有需要）
  unit_wan: '万'    # 10,000
  unit_yi: '亿'     # 100,000,000
```

---

### 4.3 错误提示清晰友好

#### 当前状态 ✅
```yaml
error:
  not_found: 未找到
  permission_denied: 权限不足
  session_expired: 会话已过期
  validation: 验证错误
```

#### 优化建议 ⚠️

**增强错误信息**:
```yaml
error:
  # 现有错误优化
  not_found: 抱歉，您访问的内容不存在
  permission_denied: 抱歉，您没有执行此操作的权限
  session_expired: 登录会话已过期，请重新登录
  validation: 表单验证失败，请检查填写内容
  
  # 新增错误类型
  network_error: 网络连接不稳定，请检查后重试
  server_error: 服务器暂时繁忙，请稍后重试
  rate_limit: 操作过于频繁，请稍后再试
  file_too_large: 文件过大，请上传小于 {size} 的文件
  invalid_file_type: 不支持的文件类型，请上传 {types} 格式
  duplicate_content: 内容重复，请修改后重新提交
  content_too_short: 内容过短，请至少输入 {min} 个字符
  content_too_long: 内容过长，请控制在 {max} 个字符以内
  email_exists: 该电子邮件已被注册
  username_exists: 该用户名已被使用
  invalid_username: 用户名只能包含字母、数字和下划线
  weak_password: 密码强度不足，请至少使用 8 个字符
```

---

### 4.4 按钮文案简洁明确

#### 当前状态 ✅
```yaml
forum:
  discussion:
    start_post_button: 新建讨论
    delete_button: 删除
    rename_button: 重命名
```

#### 优化建议

**按钮文案原则**:
1. 动词优先（2-4 字）
2. 避免歧义
3. 保持一致性

**优化对照表**:

| 场景 | 当前 | 建议 | 理由 |
|------|------|------|------|
| 开始讨论 | 新建讨论 | 发布讨论 | 更符合论坛场景 |
| 回复帖子 | 回复 | 回复 | ✅ 保持 |
| 编辑帖子 | 编辑 | 编辑 | ✅ 保持 |
| 删除帖子 | 删除 | 删除 | ✅ 保持 |
| 举报帖子 | 举报 | 举报 | ✅ 保持 |
| 点赞帖子 | 点赞 | 点赞 | ✅ 保持 |
| 关注讨论 | 关注 | 关注 | ✅ 保持 |
| 忽略讨论 | 忽略 | 忽略 | ✅ 保持 |
| 保存设置 | 保存更改 | 保存 | 更简洁 |
| 取消操作 | 取消 | 取消 | ✅ 保持 |

---

## 5️⃣ 实施计划

### 5.1 优先级划分

#### P0 - 立即执行（1-2 天）
- [ ] 统一术语（消息→私信，仓库→软件源）
- [ ] 补充 Flarum 2.0 新增模块缺失翻译
- [ ] 优化错误提示信息

#### P1 - 短期执行（1 周）
- [ ] 优化日期时间格式
- [ ] 补充复数形式处理
- [ ] 检查变量占位符完整性
- [ ] 优化按钮文案

#### P2 - 中期执行（2 周）
- [ ] 添加 YAML 元数据和分隔符
- [ ] 优化语气风格
- [ ] 补充数字格式
- [ ] 清理 HTML 标签嵌入

### 5.2 验证清单

```bash
# 1. YAML 语法验证
python3 -c "import yaml; yaml.safe_load(open('locale/zh-Hans.yml'))"

# 2. 占位符检查
grep -oE '\{[a-z_]+\}' locale/zh-Hans.yml | sort | uniq -c

# 3. 空值检查
grep -E ':\s*$' locale/zh-Hans.yml

# 4. 编码验证
file locale/zh-Hans.yml

# 5. 翻译键统计
grep -c "^[[:space:]]*[^#[:space:]]" locale/zh-Hans.yml
```

### 5.3 测试步骤

1. **本地测试**
   ```bash
   cd /var/www/flarum
   composer require flarum-aifav/chinese-simplified:@dev
   php flarum cache:clear
   ```

2. **功能测试**
   - [ ] 前台界面中文显示正常
   - [ ] 后台界面中文显示正常
   - [ ] 私信功能翻译完整
   - [ ] 实时更新翻译准确
   - [ ] 扩展管理器翻译专业

3. **用户测试**
   - [ ] 邀请 3-5 名中文用户测试
   - [ ] 收集反馈意见
   - [ ] 修复发现的问题

---

## 6️⃣ 维护建议

### 6.1 版本管理

**语义化版本**:
```
主版本。次版本.修订版本
  ↑      ↑      ↑
  |      |      └─ 翻译修正（不改变含义）
  |      └─ 新增翻译（向后兼容）
  └─ 重大变更（可能破坏兼容）
```

**示例**:
- `v2.0.0` - 初始版本
- `v2.0.1` - 翻译修正
- `v2.1.0` - 新增 Flarum 2.1 支持
- `v3.0.0` - Flarum 3.0 重大更新

### 6.2 更新流程

```
Flarum 上游更新
    ↓
对比英文语言包变更
    ↓
翻译新增/修改的键
    ↓
本地测试验证
    ↓
发布新版本
```

### 6.3 质量监控

**自动化检查**（建议添加 GitHub Actions）:
```yaml
# .github/workflows/validate.yml
name: Validate Language Pack

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate YAML
        run: python3 -c "import yaml; yaml.safe_load(open('locale/zh-Hans.yml'))"
      
      - name: Check encoding
        run: file locale/zh-Hans.yml | grep -q "UTF-8"
      
      - name: Count translations
        run: grep -c "^[[:space:]]*[^#[:space:]]" locale/zh-Hans.yml
```

---

## 7️⃣ 总结

### 7.1 当前优势

| 优势 | 说明 |
|------|------|
| ✅ 翻译完整性 | 100% 覆盖所有核心模块 |
| ✅ Flarum 2.0 兼容 | 完全支持新特性 |
| ✅ 结构规范 | 符合官方语言包标准 |
| ✅ 质量优秀 | 翻译自然流畅 |

### 7.2 优化重点

| 优先级 | 优化项 | 影响 |
|--------|--------|------|
| P0 | 术语统一（私信/软件源） | 用户体验 |
| P0 | 补充缺失翻译 | 功能完整 |
| P1 | 错误提示优化 | 用户友好 |
| P1 | 日期格式完善 | 本地化 |
| P2 | 文档与工具链 | 可维护性 |

### 7.3 预期成果

完成本优化方案后：
- ✅ 术语使用完全统一
- ✅ Flarum 2.0 新特性翻译完整专业
- ✅ 错误提示清晰友好
- ✅ 日期时间符合中国习惯
- ✅ 代码结构规范可维护
- ✅ 综合评分提升至 9.5/10

---

## 📎 附录

### A. 参考资源

- [Flarum 官方英文语言包](https://github.com/flarum/lang-english)
- [Flarum 语言包开发指南](https://docs.flarum.org/extend/language-packs)
- [ICU MessageFormat 规范](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
- [DayJS 中文配置](https://day.js.org/docs/zh-CN/i18n/i18n)

### B. 修改记录

| 日期 | 版本 | 修改内容 | 修改人 |
|------|------|---------|--------|
| 2026-03-27 | 1.0 | 初始版本 | 冰冰小助手 🧊 |

### C. 相关文件

- `ANALYSIS-REPORT.md` - 深度分析报告
- `FIX-REPORT.md` - 基础修复报告
- `COMPLETE-SUMMARY.md` - 完成总结
- `OPTIMIZATION-PLAN.md` - 本优化方案

---

**文档创建时间**: 2026-03-27 04:22 GMT+8  
**创建人**: 冰冰小助手 🧊  
**文档状态**: 待审核
