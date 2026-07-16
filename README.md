# Gmail Daily Summary Skill

自动获取 Gmail 未读邮件并生成分类中文摘要报告的 AI Agent Skill。

## 这是什么

一个轻量级 AI Agent Skill，自动抓取你 Gmail 收件箱中过去 24 小时的未读邮件，将其整理为结构化的中文摘要报告 —— 重要事项置顶、资讯归类、营销过滤，支持多语言邮件自动翻译。

## 解决的问题

- **信息过载**：几十上百封邮件压缩成一页分类摘要
- **跨语言障碍**：德语、英语、法语邮件自动翻译为中文
- **优先级盲区**：账单、安全告警、工作匹配等"需要行动"的邮件自动置顶
- **定时复盘**：配合每日定时任务，24 小时窗口设计保证不重不漏

## 跨 Agent 兼容性

此 Skill 面向**任何支持 `SKILL.md` 格式且提供 Gmail MCP 工具的 AI Agent 平台**：

| 平台 | 兼容性 | 说明 |
|------|--------|------|
| **WorkBuddy** | 原生支持 | 通过 Gmail MCP connector 获取邮件 |
| **Claude Code** | 兼容 | 需要安装 Gmail MCP server |
| **Codex** | 兼容 | 需要配置 Gmail MCP |
| **Cursor** | 兼容 | 需要配置 Gmail MCP |
| **其他 Agent** | 兼容 | 仅依赖 `gmail_search_messages` 工具 + Python 3 标准库 |

## 安装

### 方式一：让 Agent 安装（推荐）

```
帮我安装 gmail-daily-summary skill: https://github.com/stephninja028-creator/gmail-daily-summary-skill
```

### 方式二：手动安装

```bash
mkdir -p ~/.workbuddy/skills/gmail-daily-summary
git clone https://github.com/stephninja028-creator/gmail-daily-summary-skill.git ~/.workbuddy/skills/gmail-daily-summary
```

### 前置条件

- Python 3（仅用标准库，无需 `pip install`）
- 已配置 Gmail MCP connector 或同等的 `gmail_search_messages` 工具

## 使用方法

### 手动触发

对 Agent 说：

```
总结我过去 24 小时的 Gmail 未读邮件
```

### 每日定时任务

配置 Automation 每天固定时间自动运行，提示词：

```
使用 gmail-daily-summary skill，总结我过去 24 小时的 Gmail 未读邮件
```

## 输出示例

```markdown
## 每日未读邮件摘要
报告生成时间：2026-07-16 08:00 (UTC)
覆盖区间：2026-07-15 08:00 至 2026-07-16 08:00

过去 24 小时共有 **12 封未读邮件**。

### 一、需要留意的邮件

**security@github.com**: [Security] New sign-in to your account
- We noticed a new sign-in to your account from Berlin, Germany...

### 二、行业资讯与订阅

- **swyx@substack.com**: Latent Space #142 — Latest AI Engineering News

### 三、其他邮件

- promo@shop.com: Summer Sale 50% off — 可忽略
```

## 工作原理

```
用户触发 "总结邮件"
        │
        ▼
Agent 调用 gmail_search_messages 工具 ──→ 获取 24h 未读邮件 JSON
        │
        ▼
Agent 执行 scripts/generate_summary.py ──→ 关键词分类 + 结构化
        │
        ▼
Agent 对输出润色 + 外语翻译 ──→ 最终中文摘要交付用户
```

**设计哲学**：薄脚本 + Agent 编排。脚本只做确定性的数据整理和关键词分类，不调 API、不内置 LLM。翻译和润色交给上层 Agent 完成。

## 项目结构

```
├── SKILL.md                        # Skill 清单（入口文件，Agent 首先读取）
└── scripts/
    └── generate_summary.py         # 邮件分类脚本（纯标准库，73 行）
```

## 分类逻辑

| 类别 | 匹配关键词 |
|------|-----------|
| **需要留意** | `security`, `alert`, `job`, `invoice`, `order`, `bill`, `urgent`, `安全`, `职位`, `订单`, `账单` |
| **行业资讯** | `substack`, `newsletter`, `news`, `digest` |
| **其他** | 其余所有 |

当前使用纯关键词启发式分类，未来可由 LLM 增强分类准确度。

## 注意事项

- 脚本不直接调用 Gmail API —— 依赖 Agent 平台的 `gmail_search_messages` 工具获取数据
- 脚本本身不做翻译 —— 外语邮件翻译由上层 Agent/LLM 完成
- 24 小时窗口基于 Agent 运行时的系统时间计算，确保定时任务无缝覆盖
- 仅需 Python 3 标准库，无第三方依赖

## License

MIT
