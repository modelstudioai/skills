# token plan guide

阿里云百炼提供两种 AI 大模型订阅套餐：**Token Plan 团队版**（面向团队/企业）和 **Coding Plan**（面向个人开发者）。两者均以包月形式提供多模型访问能力，兼容主流 AI 编程与智能体工具，预算可控且无欠费风险。本文汇总两种套餐的核心差异、支持模型、接入方式、工具扩展及常见问题。

## 两种套餐对比

| 维度 | Token Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业日常办公 | 个人开发场景 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 使用频次 | 无每 5 小时/每周限额 | 每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期间可能排队 |
| 数据安全 | 承诺不使用数据训练模型 | 数据用于服务改进与模型优化 |
| 价格 | ¥198~¥1,398/坐席/月 | ¥200/月 |

详见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 和 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

## Token Plan 团队版

### 支持的模型

Token Plan 团队版支持以下模型（精确字符串白名单，不做版本兼容推理）：

- **千问**：qwen3.7-max（限时活动 Credits 消耗减半）、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro
- **万相**：wan2.7-image、wan2.7-image-pro
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

### 套餐与定价

| 坐席类型 | 价格 | 额度 | 适用场景 |
|----------|------|------|---------|
| 标准坐席 | ¥198/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | ¥698/坐席/月 | 100,000 Credits | 日常高频 |
| 尊享坐席 | ¥1,398/坐席/月 | 250,000 Credits | 重度依赖 |

另有**共享用量包**（¥5,000/个，625,000 Credits），跨坐席弹性抵扣，坐席额度用尽后自动使用。

### Credits 抵扣顺序

1. 优先从坐席套餐月度额度抵扣
2. 坐席额度用尽后从共享用量包抵扣（优先抵扣最近到期的）
3. 全部用尽后服务暂停，可加购共享用量包或等待下一计费周期

### 团队管理

管理员通过 [Token Plan 控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/token-plan) 或独立管理平台进行成员管理、席位分配/回收、用量分析。支持三种身份接入方式：手动添加、SAML SSO、钉钉登录。详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

## Coding Plan

### 支持的模型

推荐模型：qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5

更多模型：qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7

### 用量限制与恢复

- 每 5 小时 6,000 次请求（滚动恢复）
- 每周 45,000 次（每周一 00:00 UTC+8 重置）
- 每月 90,000 次（订阅日 00:00 UTC+8 重置）

> **注意**：Coding Plan Lite 基础版本已于 2026 年 3 月 20 日起停止新购，4 月 13 日起停止续费与升级。已购用户可继续使用至到期。

## 快速接入

### 步骤概览

两种套餐均为三步接入：订阅套餐 → 获取专属 API Key 和 Base URL → 配置 AI 工具。

### API Key 与 Base URL

| 套餐 | API Key 格式 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
|------|-------------|---------------------|------------------------|
| Token Plan 团队版 | 管理平台生成 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `sk-sp-xxx` | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

> **注意**：两种套餐的 API Key 和 Base URL 互不相通，与百炼按量计费的通用 API Key（`sk-xxx`）也不兼容，请勿混用。

### 兼容的 AI 工具

两种套餐均兼容：Claude Code、OpenClaw、Hermes Agent、OpenCode、Cursor、Codex、Qwen Code、QwenPaw、Cherry Studio、Chatbox、Cline、Qoder、Lingma、Kilo CLI 等。详见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

## 工具扩展

### 模型内置工具

qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 通过 Responses API 内置五种工具：联网搜索、代码解释器、网页抓取、以图搜图、文搜图。无需额外配置，不额外收费，Token 消耗从套餐 Credits 抵扣。

### MCP 服务

其他模型可通过百炼 MCP 广场接入工具能力。以联网搜索为例，需使用百炼通用 API Key（`sk-xxx`，非套餐专属 Key）调用。联网搜索 MCP 前 2,000 次免费，之后按 29 元/千次计费。各工具的 MCP 配置方式详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md) 和 [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)。

### 图像生成模型接入

Token Plan 团队版支持图像生成模型（qwen-image-2.0、wan2.7-image 等），但需通过工具的 Skill/Slash Command/Agent 扩展机制接入，无法直接通过文本模型 Base URL 调用。详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### 视觉理解能力

qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉理解，可直接处理图片输入。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过配置 Skill 或 Agent 委托视觉模型处理图片。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 使用限制与注意事项

- **仅限交互式使用**：两种套餐均仅限在兼容的 AI 编程和智能体工具中交互使用，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **API Key 不可共享**：Token Plan 团队版每个席位绑定一个成员、对应一个 API Key；Coding Plan 为订阅人专享
- **地域限制**：Token Plan 团队版目前仅支持华北2（北京）地域
- **退订规则**：Token Plan 团队版支持按席位退订（已消耗用量的席位不可退）；Coding Plan 不支持退款

## 常见报错速查

| 报错 | 原因 | 解决方案 |
|------|------|---------|
| `401 InvalidApiKey` | API Key 缺失/错误/混用 | 确认使用套餐专属 API Key，完整且无空格 |
| `404 model 'xxx' not found` | 模型名称拼写错误或不在支持列表 | 核对模型 ID，区分大小写 |
| `401 invalid access token` | 使用了错误的 Base URL | 按协议选择对应端点 |
| `400 Range of input length` | 输入超出上下文长度 | 新建会话或使用 `/compact` 压缩上下文 |
| `429 rate limit exceeded` | 请求过于密集 | 等待后重试，降低频率 |
| `429 quota exceeded` | 套餐额度用尽 | 加购共享用量包或等待额度重置 |

更多错误详见 [Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md) 和 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

## 来源文档

- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


