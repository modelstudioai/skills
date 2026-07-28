# token plan guide

Token Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，一份订阅即可在 Claude Code、Cursor、Qwen Code、Qoder、OpenClaw 等主流 AI 编程和智能体工具中使用。产品分为面向个人开发者的个人版和面向企业团队的团队版，覆盖文本生成、图像生成、视频生成等模型以及联网搜索、代码解释器等 Harness 工具。本页汇总产品定位、套餐限额、接入方式、[多模态](../concepts/multimodal.md)/Harness 扩展及常见排错要点。

> **注意**：Token Plan 目前仅支持**华北2（北京）**地域，需在百炼控制台左上角切换地域后购买使用。Coding Plan 与 Token Plan 是两个独立订阅产品，不可迁移或升级；Coding Plan Lite 已于 2026 年 3 月 20 日停止新购、4 月 13 日停止续费与升级，官方推荐迁移到 Token Plan，详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 版本与套餐

### 个人版

个人版提供 Lite / Standard / Pro 三个档位（限时价 39 / 139 / 499 元/月），采用 **5 小时 + 7 天两层固定窗口限额**（单位 Credits）：

| 档位 | 5 小时限额 | 7 天限额 | 并发 Agent |
| --- | --- | --- | --- |
| Lite | 700 Credits | 2,500 Credits | 1-2 个 |
| Standard | 3,000 Credits | 10,000 Credits | 3-4 个 |
| Pro | 12,000 Credits | 40,000 Credits | 6-8 个 |

- 任一层限额触顶即暂停服务，可等待窗口结束重置、使用额度重置功能，或购买**用量包**（100 元/2 万 Credits，不受窗口限额约束，需先有有效订阅，最多持有 5 个，有效期 1 个月）。
- 窗口自首次调用起计时，7 天限额**不是**固定日历日重置。
- 窗口内未用完的额度不结转。
- 支持升配（补差价、限额立即提升），不支持降配和退订。

详见 [概述（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

### 团队版

团队版以**席位（坐席）**为最小订阅单位，采用**月度总额度制**，无 5 小时/7 天窗口限额：

| 坐席 | 限时价 | 月度额度 |
| --- | --- | --- |
| 标准坐席 | 150 元/坐席/月 | 25,000 Credits |
| 高级坐席 | 550 元/坐席/月 | 100,000 Credits |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits |
| 共享用量包 | 5,000 元/个 | 625,000 Credits（有效期 1 个月，跨坐席共享） |

团队版额外提供：席位分配/回收、成员用量分析、SSO（SAML 2.0）/钉钉登录、**承诺不使用对话数据训练模型**、多租户隔离高峰不排队。个人版与团队版可同时购买，独立计费、额度不共享。管理操作详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)。

## 支持的模型

- **文本/推理模型**：qwen3.8-max-preview（预览版，限时 Credits 1 折；个人版另有夜间 22:00-08:00 折上折）、qwen3.7-max、qwen3.7-plus、qwen3.6-plus/flash、deepseek-v4 系列、glm-5 系列、kimi-k2.5 及以上、MiniMax-M2.5 等（团队版模型列表更全）。
- **图片生成**：qwen-image-2.0（团队版）、wan2.7-image、wan2.7-image-pro。
- **视频生成**：happyhorse-1.1-t2v / i2v / r2v。

> **注意**：个人版与团队版支持的模型列表不完全一致（例如 kimi、glm 多版本、qwen-image-2.0 仅出现在团队版列表中），且预览模型权益可能随运营调整，购买前以控制台模型列表页为准。

## 接入方式（关键配置）

三步接入：订阅套餐 → 获取 API Key → 配置 AI 工具，详见 [快速开始（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md) 与 [快速开始（团队版）](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)。

- **API Key**：Token Plan 专属 Key 以 `sk-sp-` 开头，仅在生成/重置时完整显示一次。
- **Base URL**：
  - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- **三套体系完全隔离，必须配套使用**：
  - Token Plan：`sk-sp-` Key + `token-plan.cn-beijing.maas.aliyuncs.com`
  - Coding Plan：专属 Key + `https://coding.dashscope.aliyuncs.com/v1`（或 `/apps/anthropic`）
  - 按量付费：通用 `sk-` Key + `https://dashscope.aliyuncs.com/compatible-mode/v1`

  混用会导致 401/403 鉴权失败，或走按量计费通道产生意外扣费。
- **RAM 用户**：需主账号授予 `AliyunTokenPlanReadOnlyAccess` 或 `AliyunTokenPlanFullAccess` + BSS 相关策略，并在百炼控制台账号管理中分配管理员或订阅套餐权限。

## 扩展能力

### [多模态](../concepts/multimodal.md)生成模型

图像/视频生成模型使用独立接口（`/api/v1/services/aigc/...`），不能通过文本模型的 Base URL 直接调用，需通过工具的扩展机制（Claude Code 的 Slash Command、Codex/Qwen Code/Qoder 的 Skill、OpenCode 的 Agent）以 curl 方式接入；视频生成为异步接口，流程为"提交任务 → 轮询 `/api/v1/tasks/<task_id>` → 下载视频"。完整示例见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### Harness 工具

部分 Qwen 模型内置 Harness 工具：联网搜索（web_search）、代码解释器（code_interpreter）、网页抓取（web_extractor）、文搜图（t2i_search）、图搜图（i2i_search）。当前仅 qwen3.7 / qwen3.8 系列支持原生工具调用（qwen3.7-max 不支持搜图类工具），切换模型后对话中直接提问即可自动调用，按成功调用次数从 Credits 抵扣。仅适用于 Token Plan，不适用于 Coding Plan，详见 [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

### 视觉理解

qwen3.8-max-preview、qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等模型原生支持视觉，直接传图即可；glm-5、MiniMax-M2.5、qwen3-coder 系列等纯文本模型可通过本地 Skill/Agent（转调 qwen3.7-plus）间接获得视觉能力。OpenCode 需在配置中显式声明 `modalities.input: ["text", "image"]` 才能启用视觉。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)。

### 联网搜索 MCP

除 Harness 原生搜索外，也可通过百炼 MCP 广场的联网搜索 MCP（Streamable HTTP：`https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）为 Qwen Code、Claude Code、OpenClaw、OpenCode 等工具扩展搜索能力。

> **注意**：MCP 服务鉴权使用**百炼通用 API Key（`sk-` 开头）**而非 Token Plan 专属 Key，前 2000 次调用免费，之后按 29 元/千次计费，详见 [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)。

## 使用限制与注意事项

1. **严禁 API 调用**：仅限在编程/智能体工具中交互式使用，禁止用于自动化脚本、应用后端或批量调用；违规可能导致订阅暂停或 API Key 封禁。
2. **数据授权差异**：个人版（及 Coding Plan）的输入输出会用于服务改进与模型优化；团队版承诺不使用对话数据训练模型。
3. **账号规范**：套餐/席位为个人专享，禁止共享 API Key。
4. **不支持降配**；个人版不支持退订；团队版可按席位退订（已有用量消耗的席位除外）。
5. **续费仅延长有效期**，不叠加当前周期额度；订阅到期重购或退订重购后 API Key 会变更，需在工具中重新配置。
6. **[限流](../concepts/rate-limit.md)按主账号维度计算**，RAM 子账号、[业务空间](../concepts/workspace.md)和 API Key 的调用量合并计算。

## 常见报错速查

| 报错 | 典型原因 | 处理 |
| --- | --- | --- |
| 401 InvalidApiKey / invalid access token | 混用了通用 Key、Coding Plan Key 或错误 Base URL；订阅过期 | 使用 `sk-sp-` Key + Token Plan 专属 Base URL |
| 404 model not found or not supported | 模型名拼写/大小写错误或不在支持列表 | 对照套餐支持的模型 ID（精确匹配） |
| 400 Range of input length | 输入超出上下文长度 | 新建会话或压缩上下文 |
| 400 调用图像/视频模型报错 | [多模态](../concepts/multimodal.md)模型不能走文本 Base URL | 通过 Skill/Slash Command/Agent 扩展机制接入 |
| 429 Requests rate limit exceeded | 请求过密触发[限流](../concepts/rate-limit.md) | 等待后重试、降低频率 |
| 429 Allocated quota exceeded | 个人版窗口限额或团队版月额度用尽 | 购买用量包/共享用量包，或等待额度重置 |

更多排错细节见 [常见问题（个人版）](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)、[常见问题（团队版）](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md) 以及 Coding Plan 的 [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)（含 OpenCode `thinking_budget`、Claude Code 初始化等工具级问题）。

## 与 Coding Plan 的关系

Coding Plan 是早期的编程模型订阅产品（Pro 套餐 200 元/月，按请求次数限额：每 5 小时 6,000 次 / 每周 45,000 次 / 每月 90,000 次），仅支持精确白名单内的文本模型，Base URL 为 `coding.dashscope.aliyuncs.com`，详见 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

> **注意**：Coding Plan 按"模型调用次数"计量，Token Plan 按 Credits（Token 用量）计量，两者额度机制不同、Key 与 Base URL 不互通、无法互相迁移。新用户应直接选择 Token Plan。

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)


