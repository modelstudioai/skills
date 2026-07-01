# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼推出的 AI 大模型订阅服务，包含面向团队的 [Token](../concepts/token.md) Plan 团队版和面向个人开发者的 Coding Plan 两种形态。两者均以固定月费模式提供多模型访问能力，兼容主流 AI 编程与智能体工具，通过专属 [API Key](../concepts/api-key.md) 和 Base URL 接入使用。

## 产品形态对比

| 维度 | [Token](../concepts/token.md) Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 定位 | 企业团队协作 | 个人开发者 |
| 计量方式 | Credits 统一计量 | 请求次数限额 |
| 席位管理 | 支持（管理员分配/回收） | 不支持 |
| 数据安全承诺 | 不用于模型训练 | 数据可用于服务改进 |
| 价格 | 198-1398 元/坐席/月 | 200 元/月 |

## Token Plan 团队版

### 支持的模型

团队版支持千问、万相、DeepSeek、月之暗面、智谱 AI、MiniMax 等品牌的模型，覆盖推理、文本生成、视觉理解、图像生成等能力。模型 ID 为精确字符串白名单，必须逐字符完全匹配，详见[Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

主要模型包括：
- **千问**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0 等
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.7-code、kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.2、glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

### 套餐与定价

| 坐席类型 | 价格 | 额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits/月 | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits/月 | 日常高频 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits/月 | 重度依赖 |

另有共享用量包（5,000 元/625,000 Credits）供跨坐席弹性使用。Credits 抵扣顺序为：坐席月度额度 > 共享用量包（近到期优先）> 额度用尽暂停服务。

### 团队管理

管理员可在 Token Plan 控制台或管理平台中完成成员管理、席位分配、用量监控。支持手动添加成员和通过 SAML SSO / 钉钉登录自动加入两种方式，详见[团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

角色分为拥有者、管理员（完整管理权限）和成员（仅使用 [API Key](../concepts/api-key.md) 调用模型）。

### 接入方式

1. 订阅套餐并获取 [API Key](../concepts/api-key.md)（格式 `sk-sp-xxx`）
2. 选择协议对应的 Base URL：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. 在 AI 工具中配置接入

> **注意**：Token Plan 团队版目前仅支持华北2（北京）地域。

## Coding Plan

### 支持的模型

Coding Plan Pro 套餐支持 qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5 等模型。模型 ID 同样为精确白名单匹配，详见[Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 套餐与限额

Pro 高级套餐 200 元/月，用量限制：
- 每 5 小时 6,000 次请求（滚动恢复）
- 每周 45,000 次请求（周一重置）
- 每月 90,000 次请求（订阅日重置）

### 接入方式

1. 获取 Coding Plan 专属 API Key（格式 `sk-sp-xxx`）
2. 选择 Base URL：
   - OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

> **注意**：Coding Plan 专属 API Key/Base URL 与百炼按量[计费](../concepts/billing.md)的 API Key（`sk-xxx`）/Base URL（`https://dashscope.aliyuncs.com/...`）不互通，混用会导致额外扣费或 403 报错。

## 兼容的 AI 工具

两种套餐均兼容以下主流工具：Claude Code、OpenClaw、Hermes Agent、OpenCode、Cursor、Codex、Qwen Code、QwenPaw、Cherry Studio、Chatbox、Cline、Qoder、Lingma、Kilo CLI 等。

## 工具调用与 MCP 扩展

### 内置工具（仅团队版 qwen3 系列）

qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图 5 个工具，通过 Responses API 直接调用，不额外收费。

### MCP 服务接入

其他模型通过百炼 MCP 广场的服务扩展能力。以联网搜索为例，在 MCP 广场开通后获取 Streamable HTTP Endpoint，在工具中添加配置即可使用。详见[工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

> **注意**：MCP 服务使用百炼通用 API Key（格式 `sk-xxx`），与套餐专属 API Key（`sk-sp-xxx`）不同，两者不可混淆。

## 图像生成模型接入

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入。例如在 Claude Code 中创建 `.claude/commands/text-to-image.md` 实现文生图功能，详见[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## 视觉理解能力

qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉理解，可直接处理图片输入。对于纯文本模型（glm-5、MiniMax-M2.5 等），可通过添加本地 Skill 委托视觉模型处理图片。

## 使用限制与注意事项

- 两种套餐均仅限在 AI 编程/智能体工具中交互式使用，禁止用于自动化脚本或应用后端
- API Key 仅限本人使用，不可共享或公开
- 违规使用可能导致订阅暂停或 API Key 封禁
- Coding Plan Lite 套餐已于 2026 年 3 月停止新购，4 月停止续费

## 常见问题

**已购买套餐仍被扣费**：检查是否误用了百炼通用 API Key 和 Base URL，应使用套餐专属的 `sk-sp-` 开头 Key 和对应 Base URL。

**model 'xxx' is not [support](support.md)ed**：模型名称必须精确匹配白名单，区分大小写，不可做版本兼容推理。

**额度用尽**：Token Plan 团队版可购买共享用量包补充；Coding Plan 需等待额度恢复周期。

**无法连接 MCP 服务**：确认已开通/升级至 Streamable HTTP 协议，检查 Endpoint URL 和 API Key 是否正确。

更多问题详见[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

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


