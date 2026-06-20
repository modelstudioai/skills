# token plan guide

百炼平台提供两种订阅制 AI 模型服务：Token Plan 团队版（面向团队/企业，按 Credits 计量）和 Coding Plan（面向个人开发者，按调用次数计量）。两者均兼容主流 AI 编程与智能体工具，通过专属 API Key 和 Base URL 接入，支持文本生成模型，Token Plan 团队版还额外支持图像生成模型。

## Token Plan 团队版与 Coding Plan 对比

| 维度 | Token Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 频次限制 | 无每 5 小时/每周限额 | 每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次（Pro） |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期可能排队 |
| 数据安全 | 承诺不用于模型训练 | 数据授权用于服务改进 |

详见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 和 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

## 支持的模型

### Token Plan 团队版

模型名称为精确字符串白名单，必须逐字符完全匹配。

| 品牌 | 模型 ID | 能力 |
|------|---------|------|
| 千问 | qwen3.7-max | 推理、文本生成 |
| 千问 | qwen3.7-plus | 推理、视觉理解、文本生成 |
| 千问 | qwen3.6-plus / qwen3.6-flash | 推理、视觉理解、文本生成 |
| 千问 | qwen-image-2.0 / qwen-image-2.0-pro | 图像生成 |
| 万相 | wan2.7-image / wan2.7-image-pro | 图像生成 |
| DeepSeek | deepseek-v4-pro / deepseek-v4-flash / deepseek-v3.2 | 推理、文本生成 |
| 月之暗面 | kimi-k2.7-code / kimi-k2.6 / kimi-k2.5 | 推理、视觉理解、文本生成 |
| 智谱 AI | glm-5.2 / glm-5.1 / glm-5 | 文本生成 |
| MiniMax | MiniMax-M2.5 | 推理、文本生成 |

### Coding Plan（Pro 套餐）

推荐模型：qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5。更多模型：qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。

> **注意**：Token Plan 团队版与 Coding Plan 支持的模型列表不同。例如 Token Plan 团队版支持 deepseek 系列和图像生成模型，而 Coding Plan 不支持；Coding Plan 支持 qwen3-coder-next/plus，而 Token Plan 团队版不支持。请以各自文档中的精确白名单为准。

## 套餐与定价

### Token Plan 团队版

| 坐席类型 | 价格 | 月额度 | 适用场景 |
|----------|------|--------|----------|
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits | 日常高频使用 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits | 重度依赖 AI |

另提供共享用量包（5,000 元/个，625,000 Credits），跨坐席共享，坐席额度用尽后自动抵扣。

### Coding Plan

Pro 套餐 200 元/月，限量抢购，每日 09:30 补充名额。

> **注意**：Coding Plan Lite 套餐已于 2026 年 3 月 20 日停止新购，4 月 13 日停止续费与升级。已购用户可用至到期。

## 快速开始

### Token Plan 团队版接入流程

1. 在 [购买页面](https://common-buy.aliyun.com/token-plan/) 选择坐席类型、数量和订阅周期
2. 管理员在控制台创建成员、分配席位，获取 API Key
3. 根据 AI 工具选择对应 Base URL 并配置

Base URL 如下：

- **OpenAI 兼容**：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **Anthropic 兼容**：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

### Coding Plan 接入流程

1. 在 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan) 订阅套餐
2. 在 Coding Plan 页面获取专属 API Key（`sk-sp-xxx` 格式）
3. 配置 Base URL 并接入工具

Base URL 如下：

- **OpenAI 兼容**：`https://coding.dashscope.aliyuncs.com/v1`
- **Anthropic 兼容**：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

> **注意**：Token Plan 团队版、Coding Plan 和百炼按量计费三者的 API Key 和 Base URL 互不相通，请勿混用。误用会导致 401/403 错误或意外扣费。

两种套餐均兼容 Claude Code、OpenClaw、Hermes Agent、OpenCode、Cursor、Codex、Qwen Code、QwenPaw、Cherry Studio、Chatbox、Cline、Qoder、Lingma、Kilo CLI 等工具。详细接入步骤见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

## Credits 计费机制（Token Plan 团队版）

单次消耗由模型类型、输入/缓存/输出 Token 用量等决定。以 qwen3.6-plus 为例，一次包含约 8,349 输入 token、40,794 缓存 token、573 输出 token 的请求约消耗 3.18 Credits。

抵扣顺序：坐席月度额度 → 共享用量包（优先抵扣最近到期的） → 额度用尽则服务暂停。

## 团队管理（Token Plan 团队版）

Token Plan 团队版提供完整的团队管理能力，包括：

- **角色权限**：拥有者、管理员（完整管理权限）、成员（仅 API 调用）
- **成员管理**：手动添加（仅供 API 调用）或通过 SSO/钉钉登录（成员可登录管理平台）
- **席位操作**：分配、回收、加购、升级席位
- **用量分析**：查看 Credits 消耗趋势、各模型和成员用量

企业可通过 SAML 2.0 对接 IdP（如阿里云 IDaaS）或钉钉实现单点登录。详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

## 工具调用

### 模型内置工具（Token Plan 团队版）

qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 通过 Responses API 内置以下工具，无需额外配置，不额外收费：

- 联网搜索、代码解释器、网页抓取、以图搜图、文搜图

### MCP 服务

其他模型可通过百炼 MCP 广场接入工具能力。以联网搜索为例：

1. 在 MCP 广场开通联网搜索服务（前 2,000 次免费，之后 29 元/千次）
2. 获取百炼通用 API Key（`sk-xxx` 格式，非套餐专属 Key）
3. 在 AI 工具中添加 MCP 配置，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`

详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md) 和 [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)。

## 图像生成模型接入

Token Plan 团队版支持 qwen-image-2.0、wan2.7-image 等图像生成模型，需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入，无法通过文本模型的 Base URL 直接调用。具体方法见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## 视觉理解能力

部分模型（qwen3.6-plus、qwen3.5-plus、kimi-k2.5）原生支持视觉理解，可直接处理图片输入。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过添加 Skill 或 Agent 调用视觉模型来获得图片理解能力。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 使用限制与注意事项

- **使用范围**：仅限在兼容的 AI 编程和智能体工具中交互式使用，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **API Key 规范**：每人独立 API Key，不可共享或公开泄露
- **服务地域**：Token Plan 团队版目前仅支持华北2（北京）地域
- **退订**：Token Plan 团队版支持按席位退订（已有用量消耗的不可退），Coding Plan 不支持退款
- **数据安全**：Token Plan 团队版承诺不使用对话数据训练模型；Coding Plan 使用数据用于服务改进

## 常见报错

| 报错 | 原因 | 解决方案 |
|------|------|----------|
| 401 InvalidApiKey | API Key 错误或混用 | 确认使用对应套餐的专属 API Key |
| 404 model not found | 模型名称错误或不在支持列表 | 核对模型 ID 精确拼写，确认套餐支持 |
| 401 invalid access token | 混用了其他套餐的 Base URL | 使用正确的 Base URL |
| 429 rate limit | 请求过于密集 | 降低频率，等待后重试 |
| 429 quota exceeded | 额度用尽 | 加购共享用量包或等待下一周期 |
| 400 Range of input length | 输入超出上下文长度 | 新建会话或压缩上下文 |

详见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)


