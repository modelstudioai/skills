# token plan guide

百炼平台提供两种订阅制 AI 模型服务：**Token Plan 团队版**面向团队/企业，以 Credits 统一计量，支持文本和图像生成模型；**Coding Plan** 面向个人开发者，按模型调用次数计费，仅支持文本生成模型。两者均兼容主流 AI 编程和智能体工具，通过专属 API Key + Base URL 接入。

## 产品对比

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 团队/企业日常办公 | 个人开发 |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 频次限制 | 无每 5 小时/每周限额 | 每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次 |
| 高峰期表现 | 多租户隔离，不排队 | 可能排队 |
| 数据安全 | 承诺不用于模型训练 | 数据用于服务改进与模型优化 |

详细区别参见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## Token Plan 团队版

### 支持的模型

模型 ID 为精确字符串白名单，必须逐字符完全匹配：

| 品牌 | 模型 ID | 能力 |
| --- | --- | --- |
| 千问 | qwen3.7-max | 推理、文本生成 |
| 千问 | qwen3.7-plus | 推理、视觉理解、文本生成 |
| 千问 | qwen3.6-plus / qwen3.6-flash | 推理、视觉理解、文本生成 |
| 千问 | qwen-image-2.0 / qwen-image-2.0-pro | 图像生成 |
| 万相 | wan2.7-image / wan2.7-image-pro | 图像生成 |
| DeepSeek | deepseek-v4-pro / deepseek-v4-flash / deepseek-v3.2 | 推理、文本生成 |
| 月之暗面 | kimi-k2.6 / kimi-k2.5 | 推理、视觉理解、文本生成 |
| 智谱 AI | glm-5.1 / glm-5 | 文本生成 |
| MiniMax | MiniMax-M2.5 | 推理、文本生成 |

### 套餐与定价

| 坐席类型 | 价格 | 月额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits | 日常高频 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits | 重度依赖 |

另有共享用量包（5,000 元/625,000 Credits），跨坐席弹性抵扣。抵扣顺序：坐席月度额度 → 共享用量包（优先最近到期） → 用尽暂停。

完整定价及订阅管理参见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### 接入方式

1. 订阅套餐后在管理后台为成员分配席位并生成 API Key
2. 根据工具协议选择 Base URL：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. 在 AI 工具中配置 API Key 和 Base URL

快速上手参见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

### 团队管理

Token Plan 团队版提供完整的团队管理能力：

- **角色体系**：拥有者、管理员、成员三级权限
- **成员接入**：支持手动添加、SAML SSO、钉钉三种方式
- **席位操作**：分配、回收、升级，回收后可重新分配给其他成员
- **用量分析**：按成员、按模型查看 Credits 消耗趋势

详细操作参见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

### 工具调用

Token Plan 团队版支持两种工具扩展方式：

- **模型内置工具**（qwen3.7-max / qwen3.7-plus / qwen3.6-plus / qwen3.6-flash）：通过 Responses API 直接使用联网搜索、代码解释器、网页抓取、以图搜图、文搜图，不额外收费
- **MCP 服务**：其他模型通过百炼 MCP 广场接入（联网搜索前 2000 次免费，之后 29 元/千次）

MCP 服务需要百炼通用 API Key（sk-xxx 格式），与 Token Plan 专属 API Key（sk-sp-xxx）不同。配置方法参见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

### 接入图像生成模型

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，无法通过文本模型 Base URL 直接调用，需通过工具的 Skill 或扩展机制接入。例如在 Claude Code 中通过 Slash Command 调用 multimodal-generation API。详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## Coding Plan

### 支持的模型

推荐模型：qwen3.7-plus（视觉）、qwen3.6-plus（视觉）、kimi-k2.5（视觉）、glm-5、MiniMax-M2.5

更多模型：qwen3.5-plus（视觉）、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7

> **注意**：Coding Plan 的模型白名单与 Token Plan 团队版不同，两者支持的模型列表需分别核对，不可互相推断。

### 套餐与限额

Pro 高级套餐 200 元/月，限额：每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次。每 5 小时额度滚动恢复，每周额度周一重置，每月额度在订阅日重置。

> **注意**：Lite 套餐已于 2026 年 3 月 20 日停止新购，4 月 13 日停止续费与升级。

### 接入方式

1. 在 Coding Plan 页面获取专属 API Key（sk-sp-xxx 格式）
2. Base URL：
   - OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

### 视觉理解

qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉，可直接传入图片。其他纯文本模型可通过添加本地 Skill/Agent 调用视觉模型实现间接视觉能力。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

### 联网搜索

通过百炼 MCP 广场的联网搜索 MCP 服务为编程工具添加实时信息检索能力。需使用百炼通用 API Key（sk-xxx），Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。详见 [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)。

## 使用限制与注意事项

- **使用范围**：两套服务均仅限在兼容的 AI 编程和智能体工具中交互式使用，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **API Key 隔离**：Token Plan 团队版、Coding Plan、百炼按量计费三者的 API Key 和 Base URL 互不相通，请勿混用
- **地域限制**：Token Plan 团队版目前仅支持华北2（北京）地域
- **退订规则**：Token Plan 支持按席位退订（已消耗用量的不可退）；Coding Plan 不支持退款

## 常见错误排查

| 错误 | 常见原因 | 解决方案 |
| --- | --- | --- |
| 401 InvalidApiKey | 混用了其他套餐的 API Key | 使用对应套餐专属 API Key |
| 404 model not found | 模型名称拼写错误或不在白名单 | 严格匹配模型 ID，区分大小写 |
| 429 rate limit / quota exceeded | 额度耗尽或请求过密 | 等待额度恢复或加购用量包 |
| 400 Range of input length | 输入超出上下文长度 | 新建会话或使用 /compact 压缩上下文 |

完整错误码列表参见 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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


