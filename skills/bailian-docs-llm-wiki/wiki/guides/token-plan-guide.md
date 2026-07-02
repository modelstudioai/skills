# token plan guide

百炼平台提供两种订阅制 AI 模型服务：[Token](../concepts/token.md) Plan 团队版（面向团队/企业，按 Credits 计量）和 Coding Plan（面向个人开发者，按请求次数计量）。两者均兼容主流 AI 编程与智能体工具，提供专属 [API Key](../concepts/api-key.md) 和 Base URL，与百炼按量[计费](../concepts/billing.md)体系完全隔离。

## [Token](../concepts/token.md) Plan 团队版与 Coding Plan 对比

| 维度 | [Token](../concepts/token.md) Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业日常办公 | 个人开发场景 |
| [计费](../concepts/billing.md)方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数（每 5 小时/每周/每月限额） |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期间可能排队 |
| 数据安全 | 承诺不用数据训练模型 | 数据用于服务改进与模型优化 |
| 价格 | 标准坐席 198 元/月起 | 200 元/月 |

详细对比见[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## Token Plan 团队版

### 支持的模型

Token Plan 团队版采用精确字符串白名单，必须逐字符完全匹配，不做版本兼容推理。当前支持的模型包括：

- **千问**：qwen3.7-max（限时活动，Credits 消耗减半）、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash
- **图像生成**：qwen-image-2.0、qwen-image-2.0-pro、wan2.7-image、wan2.7-image-pro
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.7-code、kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.2、glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

完整模型列表和能力说明见[Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### 套餐与定价

| 坐席类型 | 价格 | 月度额度 | 适用场景 |
|----------|------|----------|----------|
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits | 日常高频使用 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits | 重度依赖 AI |

另可加购共享用量包（5,000 元/个，625,000 Credits），跨坐席共享，有效期 1 个月。

### Credits 抵扣顺序

1. 优先从坐席套餐月度额度抵扣
2. 坐席额度用尽后从共享用量包抵扣（多个包时优先抵扣最近到期的）
3. 全部用尽后服务暂停，直到下一[计费](../concepts/billing.md)周期或购买共享用量包

### 快速接入

三步完成接入：

1. **订阅套餐**：访问 [Token Plan 购买页](https://common-buy.aliyun.com/token-plan/)选择坐席类型和数量
2. **获取凭证**：管理员在团队管理后台创建成员、分配席位后获取 [API Key](../concepts/api-key.md)；根据工具协议选择 Base URL：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. **配置工具**：在 Claude Code、Cursor、Qwen Code 等工具中填入 [API Key](../concepts/api-key.md) 和 Base URL

详细步骤见[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

> **注意**：Token Plan 团队版目前仅支持华北2（北京）地域。

### 团队管理

Token Plan 团队版提供完整的团队管理能力，包括成员管理、席位分配/回收、用量分析。支持手动添加成员、SAML SSO 和钉钉三种接入方式。

角色权限分为三级：

- **所有者**：完整管理权限
- **管理员**：与所有者权限相同，由所有者授予
- **成员**：仅使用分配的 API Key 调用模型

RAM 用户使用前需由主账号授予 `AliyunTokenPlanReadOnlyAccess` 或 `AliyunTokenPlanFullAccess` 策略。详见[团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

### 工具调用

Token Plan 团队版支持两种工具调用方式：

- **模型内置工具**（qwen3.7-max/plus、qwen3.6-plus/flash）：通过 Responses API 直接使用联网搜索、代码解释器、网页抓取、以图搜图、文搜图，不额外收费
- **MCP 服务**（其他模型）：通过百炼 MCP 广场接入。联网搜索 MCP 前 2000 次免费，之后 29 元/千次

> **注意**：MCP 服务使用百炼通用 API Key（sk-xxx 格式），与 Token Plan 专属 API Key（sk-sp-xxx 格式）不同，请勿混用。

详见[工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

### 接入图像生成模型

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，需通过 AI 工具的 Skill 或扩展机制接入。以 Claude Code 为例，可创建 `.claude/commands/text-to-image.md` Slash Command，调用 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` 端点生成图片。详见[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## Coding Plan

### 套餐与模型

Coding Plan 提供 Pro 高级套餐（200 元/月），支持的模型包括：

- **推荐**：qwen3.7-plus（视觉）、qwen3.6-plus（视觉）、kimi-k2.5（视觉）、glm-5、MiniMax-M2.5
- **更多**：qwen3.5-plus（视觉）、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7

> **注意**：Lite 套餐已于 2026 年 3 月 20 日停止新购，4 月 13 日停止续费与升级。

用量限制为每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次请求。每 5 小时额度采用滚动恢复机制。

详见[Coding Plan 概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 接入方式

1. 订阅后在 Coding Plan 页面获取专属 API Key（sk-sp-xxx 格式）
2. 配置 Base URL：
   - OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

### 视觉理解能力

qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉理解。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过 Skill/Agent 机制调用视觉模型辅助处理图片。详见[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 使用限制与注意事项

- **使用范围**：两种套餐均仅限在兼容的 AI 编程和智能体工具中交互式使用，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **API Key 隔离**：Token Plan 团队版、Coding Plan、百炼按量计费三者的 API Key 和 Base URL 互不相通，混用会导致报错或额外扣费
- **退订规则**：Token Plan 团队版支持按席位退订（已有用量消耗的不可退），Coding Plan 不支持退款
- **数据安全**：Token Plan 团队版承诺不使用对话数据训练模型；Coding Plan 的数据会用于服务改进

## 常见报错速查

| 报错 | 原因 | 解决方案 |
|------|------|----------|
| 401 InvalidApiKey | API Key 错误或混用 | 确认使用对应套餐的专属 API Key |
| 404 model not found | 模型名称拼写错误或不在支持列表 | 检查模型 ID 是否完全匹配白名单 |
| 401 invalid access token | Base URL 与套餐不匹配 | 使用对应套餐的专属 Base URL |
| 429 rate limit | 请求过于密集或额度用尽 | 降低频率或等待额度恢复/加购用量包 |
| 400 input length exceeded | 输入超出上下文长度 | 新建会话或使用 `/compact` 压缩上下文 |

完整报错列表见[Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)和[Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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


