# token plan guide

阿里云百炼平台提供两种订阅制 AI 模型服务：**Token Plan 团队版**面向团队和企业，以 Credits 统一计量，支持文本生成与图像生成模型；**Coding Plan**面向个人开发者，按模型调用次数计费。两者均兼容主流 AI 编程和智能体工具，提供专属 API Key 和 Base URL，与百炼按量计费体系独立运作。

## Token Plan 团队版

### 产品定位

Token Plan 团队版是面向团队/企业的 AI 大模型订阅服务，核心特性包括：

- **多模型灵活切换**：支持千问、DeepSeek、月之暗面、智谱 AI、MiniMax 等品牌的文本生成与图像生成模型，通过 Credits 统一抵扣
- **团队管理**：提供管理后台，支持席位分配与回收、成员用量分析、SAML SSO 和钉钉接入
- **数据安全**：承诺不使用对话数据训练模型，多租户隔离架构
- **高峰期不排队**：多租户隔离，调用高峰期间不排队

> **注意**：Token Plan 团队版目前仅支持**华北2（北京）**地域。

### 支持的模型

Token Plan 团队版的模型列表为精确字符串白名单，必须逐字符完全匹配，不做版本兼容推理。主要支持的模型包括：

| 品牌 | 模型 ID | 模型能力 |
|------|---------|----------|
| 千问 | qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash | 推理模型、文本生成（部分支持视觉理解） |
| 千问 | qwen-image-2.0、qwen-image-2.0-pro | 图像生成 |
| 万相 | wan2.7-image、wan2.7-image-pro | 图像生成 |
| DeepSeek | deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2 | 推理模型、文本生成 |
| 月之暗面 | kimi-k2.7-code、kimi-k2.6、kimi-k2.5 | 推理模型、视觉理解、文本生成 |
| 智谱 AI | glm-5.2、glm-5.1、glm-5 | 文本生成 |
| MiniMax | MiniMax-M2.5 | 推理模型、文本生成 |

完整列表请参见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### 套餐与定价

| 坐席类型 | 价格 | 月额度 | 适用场景 |
|---------|------|--------|---------|
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits | 日常高频使用 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits | 重度依赖 AI |

另提供**共享用量包**（5,000 元/个，625,000 Credits），跨坐席共享，当坐席额度用尽时自动抵扣。

### Credits 抵扣机制

单次请求的 Credits 消耗由模型类型、输入/输出/缓存 Token 数量等因素决定。抵扣顺序为：

1. 优先从坐席套餐月度额度抵扣
2. 坐席额度用尽后从共享用量包抵扣（优先抵扣最近到期的）
3. 全部额度用尽后服务暂停，等待下一计费周期或购买补充包

### 快速接入

接入 Token Plan 团队版只需三步，详见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)：

1. **订阅套餐**：访问购买页面选择坐席类型和数量
2. **获取凭证**：管理员在管理后台创建成员并分配席位后生成 API Key
3. **配置工具**：在 AI 工具中填入 API Key 和对应协议的 Base URL

Base URL 按协议区分：

| 协议 | Base URL |
|------|----------|
| OpenAI 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

支持的工具包括 Claude Code、Cursor、Qwen Code、OpenClaw、OpenCode、Cline、Chatbox、Cherry Studio 等。

### 团队管理

Token Plan 团队版提供完整的团队管理能力，详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)：

- **角色体系**：拥有者、管理员、成员三级权限
- **成员管理**：支持手动添加（仅 API 调用）和 SSO/钉钉登录（可访问管理平台）两种方式
- **席位操作**：分配、回收、加购、升级席位，加购费用按剩余时长折算
- **用量分析**：查看 Credits 消耗趋势、模型用量和成员用量明细
- **SSO 接入**：支持标准 SAML 2.0 和钉钉两种企业身份集成方式

### 工具调用

Token Plan 团队版支持两种方式扩展模型能力，详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)：

- **模型内置工具**：qwen3.7-max/plus、qwen3.6-plus/flash 通过 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，不额外收费
- **MCP 服务**：其他模型通过百炼 MCP 广场接入工具能力（联网搜索前 2000 次免费，之后 29 元/千次）

### 接入图像生成模型

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，需通过工具的 Skill 或扩展机制接入。例如在 Claude Code 中可创建 Slash Command `.claude/commands/text-to-image.md`，通过 curl 调用多模态生成 API。详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## Coding Plan

### 产品定位

Coding Plan 面向个人开发场景，按模型调用次数计费，提供 Pro 高级套餐（200 元/月）。与 Token Plan 团队版的主要区别：

| 维度 | Token Plan 团队版 | Coding Plan |
|------|------------------|-------------|
| 适用场景 | 团队/企业 | 个人开发 |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 计费方式 | Credits（按 Token） | 按调用次数 |
| 频次限制 | 无 | 每 5 小时/每周/每月限额 |
| 数据安全 | 不用于训练 | 用户数据授权 |
| 高峰期 | 多租户隔离 | 可能排队 |

### Coding Plan 支持的模型

推荐模型：qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5。更多模型包括 qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。

Pro 套餐用量限制：每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次。额度采用滚动恢复机制，每分钟自动释放 5 小时前的额度。

### Coding Plan 接入

Coding Plan 的 API Key（格式 `sk-sp-xxx`）和 Base URL 与 Token Plan 团队版、百炼按量计费三者互不相通：

| 协议 | Base URL |
|------|----------|
| OpenAI 兼容 | `https://coding.dashscope.aliyuncs.com/v1` |
| Anthropic 兼容 | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

详见 [Coding Plan 概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 联网搜索

Coding Plan 用户可通过百炼 MCP 广场的联网搜索 MCP 服务为编程工具添加联网搜索能力。需使用百炼通用 API Key（`sk-xxx` 格式）而非 Coding Plan 专属 API Key。MCP 连接地址为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`，采用 Streamable HTTP 协议。详见 [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)。

### 视觉理解能力

Coding Plan 中 qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉理解，可直接处理图片。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过添加 Skill 或 Agent 调用视觉模型来辅助获得视觉能力。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 使用限制与注意事项

- **使用范围**：两种套餐均仅限在兼容的 AI 编程和智能体工具中交互式使用，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **API Key 隔离**：Token Plan 团队版、Coding Plan 和百炼按量计费的 API Key 和 Base URL 互不相通，误用会导致认证错误
- **账号规范**：API Key 仅限分配的成员本人使用，不可共享

## 常见错误排查

| 错误 | 常见原因 | 解决方案 |
|------|---------|---------|
| 401 InvalidApiKey | 混用了其他套餐的 API Key 或订阅过期 | 确认使用对应套餐的专属 API Key |
| 404 model not found | 模型名称拼写错误或不在支持列表中 | 检查模型 ID 是否精确匹配，区分大小写 |
| 401 invalid access token | 混用了其他套餐的 Base URL | 按协议选择正确的 Base URL 端点 |
| 429 rate limit / quota exceeded | 请求过于密集或额度用尽 | 降低频率、加购共享用量包或等待额度重置 |

完整错误码列表请参见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md) 和 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


