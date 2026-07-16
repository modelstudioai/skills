# token plan guide

Token Plan 团队版与 Coding Plan 是百炼面向 AI 编程/智能体工具的两类订阅服务：Token Plan 团队版以 Credits 统一计量、按 Token 消耗抵扣，支持文本与图像生成模型并提供团队管理后台；Coding Plan 面向个人开发场景，按模型调用次数计费并设有请求限额。两者的 API Key 与 Base URL 完全隔离、互不相通，接入前需先明确使用的是哪种套餐。

## 两种套餐对比

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 一人公司/团队/企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成 + 图像生成 | 文本生成模型 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次 | 无每 5 小时/每周限额 | 有每 5 小时/每周/每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期可能排队 |
| 数据安全 | 承诺不使用数据训练模型 | 用户数据授权用于服务改进 |

> **注意**：两个计划互相独立，不支持互转（即使补差价也不行），可同时订阅、各自计费。详见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 与 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

## 支持的模型

Token Plan 团队版的模型清单为**精确字符串白名单**，必须逐字符完全匹配，版本号/子型号任何差异均视为不支持，禁止版本兼容推理。

- **千问**：qwen3.7-max（限时活动）、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro
- **万相**：wan2.7-image、wan2.7-image-pro
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.7-code、kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.2、glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

Coding Plan Pro 套餐的推荐模型为 qwen3.7-plus、qwen3.6-plus、kimi-k2.5（均支持图片理解）、glm-5、MiniMax-M2.5，更多模型见 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

> **注意**：两套清单的白名单不完全一致，且 Coding Plan Lite 套餐已于 2026 年 3 月 20 日停止新购、4 月 13 日停止续费与升级。调用时务必以对应套餐控制台的实时清单为准。

## 快速接入（三步）

以 Token Plan 团队版为例，详见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)：

1. **订阅**：在购买页选择坐席类型、数量和订阅周期。RAM 子账号订阅前需主账号授予 `AliyunBailianFullAccess` 权限。
2. **获取 API Key 和 Base URL**：分配席位后为成员生成专属 API Key（Token Plan 以 `sk-sp-` 开头，与通用 `sk-` 不可混用；仅首次显示一次，需立即保存）。
3. **接入 AI 工具**：支持 Claude Code、Qwen Code、OpenCode、OpenClaw、Cursor、Codex、Qoder、Cline、Kilo CLI 等。

### Base URL 对照

| 套餐 / 协议 | Base URL |
| --- | --- |
| Token Plan · OpenAI 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Token Plan · Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan · OpenAI 兼容 | `https://coding.dashscope.aliyuncs.com/v1` |
| Coding Plan · Anthropic 兼容 | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量付费 · OpenAI 兼容 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

> **注意**：Token Plan、Coding Plan、按量付费三者的 API Key 与 Base URL 必须配套使用。混用会导致走按量计费通道产生意外扣费，或返回 401/403 鉴权失败。

## 工具调用与扩展能力

- **模型内置工具**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 通过 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图 5 个工具，不额外收费，token 消耗统一从套餐 Credits 抵扣。
- **MCP 服务**：其他模型（如 deepseek-v3.2、glm-5）通过百炼 MCP 广场接入工具。联网搜索 MCP 前 2000 次调用免费，之后按 29 元/千次计费。接入 MCP 用的是**百炼通用 API Key（`sk-xxx`）**，而非套餐专属 Key。
- **图像生成模型**：不在文本模型清单展示，需通过工具的 Skill / Slash Command / Agent 机制调用 `multimodal-generation` API，详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
- **视觉理解**：qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉；glm-5、MiniMax-M2.5 等纯文本模型可通过 Skill/Agent 辅助获得视觉能力。OpenCode/OpenClaw 需在配置中显式声明 `modalities`/`input` 为 `["text","image"]`。

## Credits 计费与额度

Token Plan 团队版单次请求消耗的 Credits **并非固定值**，由模型类型、Token 用量、思考模式及工具调用动态决定。多轮对话中上下文持续累积，消耗会随之上升；部分模型按上下文长度阶梯计费，长上下文可能进入更高价位档。

抵扣顺序：坐席套餐月度额度 → 共享用量包（多个时优先扣最近到期的）→ 全部用尽后服务暂停至下一计费周期。

> **注意**：续费/续订只延长有效期或预定下期额度，**不会叠加补充到当前计费周期**。当期额度用尽需立即恢复时，应购买共享用量包、升级坐席或加购坐席（加购后需分配给成员才能使用）。

控制消耗建议：任务切换时及时开启新会话、清理无关历史；对长文档/大代码库按需拆分输入；在控制台订阅页用量明细关注实时消耗趋势。

## 常见报错速查

- **401 Invalid API-key / invalid access token**：误用了通用 Key 或其他套餐的 Key/Base URL、订阅过期、或 Key 复制不完整含空格。核对套餐专属 Key 与配套 Base URL，必要时重置。
- **404 model not found / model not [support](support.md)ed**：模型名拼写或大小写错误，或不在套餐白名单内。
- **400 url error / Range of input length**：Base URL 路径与协议不匹配（Anthropic 端点以 `/apps/anthropic` 结尾，OpenAI 端点以 `/compatible-mode/v1` 或 `/v1` 结尾），或输入超出上下文长度（新建会话或切换更长上下文模型）。
- **429 quota exceeded**：套餐额度用尽（加购/等待重置）或触发 TPS/TPM 限流（限流按主账号维度合并计算，等待约一分钟后平滑重试）。
- **Coding Plan 限额类**：`hour/week/month allocated quota exceeded` 分别对应每 5 小时（滚动恢复）、每周一 00:00 重置、每月订阅日重置。

完整报错表见 [Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md) 与 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

## 团队管理与使用限制

- **角色**：所有者、管理员（权限同所有者，可被移除/降级）、成员（仅使用分配的 Key 调用）。
- **成员接入**：支持手动添加（仅供 API 调用）、SAML 2.0（SSO）、钉钉登录三种方式。
- **席位操作**：分配后自动生成 API Key；回收后席位释放、原 Key 失效；加购/升级按剩余时长折算费用；退订按席位维度，已消耗用量的席位不可退订。
- **使用范围**：仅限在兼容的 AI 编程和智能体工具中**交互式**使用，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁。

> **注意**：Token Plan 团队版目前仅支持**华北2（北京）**地域；每个阿里云账号限购一个订阅，共享用量包需先订阅坐席套餐后才能购买、有效期 1 个月且到期清零。

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


