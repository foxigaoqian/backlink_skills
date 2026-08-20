# Backlink Skills — Browser-first Quick Start

这个 fork 的推荐入口是：

```text
$backlink-submitter
```

适合从一个项目 URL 直接开始，例如：

```text
$backlink-submitter
给 https://dearpassengerscrew.com/ 做外链。
第一批最多 10 个，免费优先，不付费，不做互链，不冒充官方。
普通网站表单用浏览器执行；有官方 API 才走 API；遇到 CAPTCHA、登录、邮箱验证时暂停让我处理。
每个结果写入 campaign record，不要把打开表单当作提交成功。
```

## 正确执行架构

```text
项目 URL
  ↓
识别网站类型与身份边界
  ↓
从 Free-backlink-list.md + 当前研究筛候选
  ↓
质量筛选（第一批 ≤ 10）
  ↓
执行路由
  ├─ 官方 API / CLI / Connector → 程序化执行
  ├─ 普通网站表单 → Codex Browser / connected browser
  └─ CAPTCHA / 登录 / 邮箱验证 → 用户接管
  ↓
记录 submitted / awaiting approval / published / blocked / unknown
  ↓
下一批
```

## 不再使用的方式

普通第三方网站表单不要再使用：

- GitHub Actions + `requests`/`urllib` 模拟提交
- 为每个目录单独写 HTML parser
- 猜隐藏字段和 POST endpoint
- 网站改版后继续盲目重试旧脚本

这些方式只在目标网站明确提供并支持程序化接口时才有意义。

## 为什么 Browser-first

目录站经常依赖 JavaScript、Cookie、CSRF/session、反机器人逻辑、动态字段、挑战页面或浏览器里的真实登录状态。GitHub Runner / 普通 HTTP 客户端拿到的页面可能和用户浏览器看到的完全不同。

因此：

- 浏览器页面是普通表单路线的事实来源；
- API 文档是程序化路线的事实来源；
- CAPTCHA、OTP 和邮件验证是正常人工接管点，不是需要绕过的障碍。

## Campaign 记录

每个站一个文件：

```text
campaigns/<domain>.md
```

默认记录：

- 项目身份
- 标题 / 描述 / URL / 分类
- 候选渠道
- 执行 surface（browser / API / handoff）
- 成本 / 互链要求
- 当前状态
- 公开 listing URL
- 下一步

不要把密码、Cookie、OTP、恢复码、session ID、magic link 写进仓库。

## Skill 选择

- `$backlink-submitter`：默认入口，从项目 URL 开始，适合游戏站、工具站、SaaS、内容站等。
- `$submit-product-directories-v2-quality`：需要严格质量门槛、授权矩阵和审计时用。
- `$submit-product-directories-v1-batch`：已经有大量合格 URL，主要需要批量队列、去重和断点恢复时用。

普通网站表单无论进入哪个 Skill，都遵守 Browser-first 规则。
