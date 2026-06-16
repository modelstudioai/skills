# token plan guide

百炼平台提供两种 AI 大模型订阅套餐：**Token Plan 团队版**和 **Coding Plan**。Token Plan 团队版面向团队/企业场景，以 Credits 统一计量，支持文本生成与图像生成模型，提供团队管理后台和数据安全保障；Coding Plan 面向个人开发场景，按模型调用次数计费。两者的 API Key 和 Base URL 互不相通，不可混用。

## 套餐对比

| 维度 | Token Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业日常办公 | 个人开发 |
| 支持模型 | 文本生成 + 图像生成 | 文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 频次限制 | 无每 5 小时/每周限额 | 每 5 小时/每周/每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 可能排队 |
| 数据安全 | 承诺不使用数据训练模型 | 用户数据授权 |

详细对比见[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## Token Plan 团队版

### 支持的模型

Token Plan 团队版支持以下品牌和模型（必须精确匹配模型 ID）：

- **千问**：qwen3.7-max（限时活动）、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro
- **万相**：wan2.7-image、wan2.7-image-pro
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

其中 qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、kimi-k2.6、kimi-k2.5 支持视觉理解。qwen-image-2.0、qwen-image-2.0-pro、wan2.7-image、wan2.7-image-pro 为图像生成模型。

### 套餐与定价

| 坐席类型 | 价格 | 月额度 | 适用场景 |
|----------|------|--------|----------|
| 标准坐席 | ¥198/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | ¥698/坐席/月 | 100,000 Credits | 日常高频使用 |
| 尊享坐席 | ¥1,398/坐席/月 | 250,000 Credits | 重度依赖 AI |

另提供**共享用量包**（¥5,000/个，625,000 Credits），跨坐席共享，有效期 1 个月。共享用量包需先订阅坐席套餐后才能购买。

### 快速开始

1. **订阅**：访问 [Token Plan 团队版购买页面](https://common-buy.aliyun.com/token-plan/) 选择坐席类型和数量。
2. **获取凭证**：在管理后台创建成员、分配席位后获取 API Key。Base URL 根据协议选择：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. **接入工具**：在 Claude Code、Cursor、OpenCode、Qwen Code 等工具中配置上述 API Key 和 Base URL。

完整步骤见[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

### Credits 计费机制

单次请求消耗的 Credits 由模型类型、输入/缓存/输出 Token 数量共同决定。抵扣顺序为：坐席套餐月度额度 → 共享用量包（优先最近到期的） → 全部用尽后服务暂停。

以 qwen3.6-plus 为例，一次包含约 8,349 输入 tokens、40,794 缓存 tokens、573 输出 tokens 的请求大约消耗 3.18 Credits。

### 团队管理

Token Plan 团队版提供完整的团队管理能力，包括：

- **角色体系**：拥有者、管理员、成员三级角色，权限逐级递减
- **成员管理**：支持手动添加、SAML SSO 接入、钉钉接入三种方式
- **席位操作**：分配、回收、升级席位；每个席位绑定一个成员和一个 API Key
- **用量分析**：在管理平台查看 Credits 消耗趋势、各模型用量、成员消耗明细

详细操作见[团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

### 工具调用

Token Plan 团队版支持两种方式扩展工具能力：

- **模型内置工具**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 通过 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，不额外收费。
- **MCP 服务**：其他模型可通过百炼 MCP 广场接入工具，如联网搜索 MCP（前 2000 次免费，之后 29 元/千次）。

接入 MCP 需要百炼通用 API Key（sk-xxx 格式），与 Token Plan 专属 API Key（sk-sp-xxx 格式）不同。配置方式因工具而异，详见[工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

### 接入图像生成模型

Token Plan 团队版支持图像生成模型（qwen-image-2.0、wan2.7-image 等），需通过工具的 Skill 或扩展机制接入，无法直接通过文本模型的 Base URL 调用。以 Claude Code 为例，可创建 `.claude/commands/text-to-image.md` Slash Command 调用图像生成 API。详见[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## Coding Plan

### 套餐详情

Coding Plan 当前仅提供 **Pro 高级套餐**（¥200/月），Lite 基础套餐已于 2026 年 3 月 20 日起停止新购。

Pro 套餐支持的模型：qwen3.7-plus（视觉）、qwen3.6-plus（视觉）、kimi-k2.5（视觉）、glm-5、MiniMax-M2.5、qwen3.5-plus（视觉）、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。

用量限制：每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次。额度按滚动方式恢复（5 小时额度每分钟自动释放对应时间点的消耗）。

> **注意**：Coding Plan 使用期间，模型输入和生成内容将用于服务改进与模型优化，这与 Token Plan 团队版的数据安全承诺不同。

### 快速开始

1. 访问 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan) 订阅套餐。
2. 在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) 获取专属 API Key（sk-sp-xxx 格式）和 Base URL：
   - OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
3. 在 AI 编程工具中配置。

详见[Coding Plan 概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 视觉理解能力

qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉理解，可直接处理图片。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过添加 Skill/Agent 委托视觉模型处理图片。详见[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

### 联网搜索

Coding Plan 支持通过百炼 MCP 广场的联网搜索 MCP 为编程工具添加联网搜索能力。需使用百炼通用 API Key（sk-xxx，非 Coding Plan 专属 Key）。在 Claude Code、Qwen Code、OpenCode 等工具中均可通过配置 MCP 服务接入。详见[联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)。

## 使用限制与注意事项

- **使用范围**：两种套餐均仅限在兼容的 AI 编程和智能体工具中交互式使用，不可用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁。
- **API Key 规范**：仅限分配的成员本人使用，不可共享或公开。
- **服务地域**：Token Plan 团队版目前仅支持华北2（北京）地域。
- **Key 不互通**：Token Plan 团队版、Coding Plan、百炼按量计费三者的 API Key 和 Base URL 互不相通。

## 常见错误排查

| 错误 | 常见原因 | 解决方案 |
|------|----------|----------|
| 401 InvalidApiKey | 混用了其他套餐的 API Key 或订阅过期 | 确认使用对应套餐专属 API Key |
| 404 model not found | 模型名称拼写错误或不在支持列表 | 核对模型 ID，区分大小写 |
| 429 rate limit / quota exceeded | 额度用尽或请求过密 | 等待额度恢复或购买共享用量包 |
| Connection error | Base URL 域名拼写错误 | 检查域名和网络连接 |

更多错误码及解决方案见[Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)和[Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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


