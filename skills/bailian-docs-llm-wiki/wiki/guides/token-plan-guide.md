# token plan guide

百炼平台提供两种 AI 大模型订阅套餐：Token Plan 团队版和 Coding Plan，分别面向团队/企业和个人开发者。两者均以预付费模式整合多种主流模型，兼容 Claude Code、Cursor、Qwen Code 等 AI 编程与智能体工具，通过专属 API Key 和 Base URL 接入使用。

## 套餐对比

| 维度 | Token Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 频次限制 | 无每 5 小时/每周限额 | 每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期间可能排队 |
| 数据安全 | 承诺不使用数据训练模型 | 数据使用授权 |

详细对比见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## Token Plan 团队版

### 支持的模型

Token Plan 团队版支持以下精确版本（必须逐字符完全匹配，不做版本兼容推理）：

- **千问**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro
- **万相**：wan2.7-image、wan2.7-image-pro
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

其中 qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、kimi-k2.6、kimi-k2.5 支持视觉理解；qwen-image-2.0 等为图像生成模型。详见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### 套餐与定价

提供三个坐席档位：

| 坐席类型 | 价格 | 月度额度 | 适用场景 |
|----------|------|----------|----------|
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits | 日常高频使用 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits | 重度依赖 AI 的核心开发者 |

另提供共享用量包（5,000 元/个，625,000 Credits），跨坐席弹性抵扣，有效期 1 个月。

### Credits 计费与抵扣

单次消耗的 Credits 由模型类型、输入/缓存/输出 Token 用量共同决定。抵扣顺序：坐席月度额度 > 共享用量包（优先到期最近的） > 全部用尽后服务暂停。

### 快速接入

1. 在 [Token Plan 购买页面](https://common-buy.aliyun.com/token-plan/) 订阅坐席
2. 在管理后台创建成员、分配席位，获取专属 API Key
3. 配置 Base URL 接入 AI 工具：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

详细步骤见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

> **注意**：Token Plan 团队版目前仅支持华北2（北京）地域。

### 团队管理

Token Plan 团队版提供完整的团队管理能力，包括：

- **角色体系**：拥有者、管理员、成员三级权限
- **成员管理**：手动添加（仅 API 调用）或通过 SSO/钉钉登录（可访问管理平台）
- **席位操作**：分配、回收、升级席位；每个席位绑定一个成员和一个 API Key，不可共享
- **用量分析**：查看 Credits 消耗趋势、各模型和成员的消耗明细

企业可通过 SAML 2.0 对接 IdP（如阿里云 IDaaS）或钉钉实现统一身份接入。详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

## Coding Plan

### 支持的模型

Pro 套餐支持：qwen3.7-plus、qwen3.6-plus、qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、kimi-k2.5、glm-5、glm-4.7、MiniMax-M2.5。

> **注意**：Coding Plan Lite 套餐已于 2026 年 3 月 20 日起停止新购，4 月 13 日起停止续费与升级。已购用户可继续使用至到期。

### 定价与额度

Pro 套餐 200 元/月，额度限制：每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次。每 5 小时额度为滚动恢复机制（每分钟释放 5 小时前的消耗），每周额度于周一 00:00 重置。

### 快速接入

1. 在 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan) 订阅
2. 获取专属 API Key（`sk-sp-xxx` 格式）和 Base URL：
   - OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
3. 在 AI 工具中配置接入

详见 [Coding Plan 概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

> **注意**：Token Plan 团队版、Coding Plan 和百炼按量计费三者的 API Key 和 Base URL 互不相通，请勿混用。误用会导致 401/403 错误或意外扣费。

## 工具调用与扩展能力

### 模型内置工具

qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 通过 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，不额外收费，Token 消耗从套餐 Credits 中抵扣。

### MCP 服务

其他模型可通过百炼 MCP 广场接入工具能力（如联网搜索 MCP），需使用百炼通用 API Key（`sk-xxx` 格式）鉴权。联网搜索 MCP 前 2,000 次调用免费，之后按 29 元/千次计费。详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

### 图像生成模型

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，需通过工具的 Skill 或扩展机制接入。例如在 Claude Code 中可创建 Slash Command 调用文生图 API。详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### 视觉理解

qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉理解，可直接处理图片输入。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过添加 Skill 委托视觉模型处理图片。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 使用限制与注意事项

- **使用范围**：仅限在兼容的 AI 编程和智能体工具中交互式使用，不可用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **账号规范**：API Key 仅限分配成员本人使用，不可共享或公开泄露
- **数据安全**：Token Plan 团队版承诺不使用对话数据训练模型；Coding Plan 的数据使用授权详见服务协议
- **退订**：Token Plan 团队版支持按席位退订（已有消耗的不可退），Coding Plan 不支持退款
- **服务地域**：Token Plan 团队版目前仅在华北2（北京）地域提供服务

## 常见错误排查

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 401 InvalidApiKey | 误用其他套餐的 API Key 或 Key 过期 | 使用对应套餐的专属 API Key |
| 404 model not found | 模型名称拼写错误或不在套餐支持列表 | 确认模型 ID 完全匹配，区分大小写 |
| 429 rate limit | 请求过于密集 | 降低频率，等待额度恢复 |
| 400 input length | 输入超出模型上下文长度 | 新建会话或使用 `/compact` 压缩上下文 |
| Connection error | Base URL 拼写错误或网络异常 | 检查域名拼写和网络连接 |

更多错误码和解决方案见 [Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md) 和 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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



