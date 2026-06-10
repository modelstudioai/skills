# token plan guide

Token Plan 团队版与 Coding Plan 是阿里云百炼推出的两类 AI 大模型订阅服务，分别面向团队协作与个人开发场景。Token Plan 以 Credits 统一计量，支持文本生成与图像生成模型，提供团队管理后台；Coding Plan 按模型调用次数计费，限定在 AI 编程工具中使用。两者均兼容主流 AI 编程与智能体工具，通过专属 API Key 与 Base URL 接入。

## 产品对比

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 一人公司 / 团队 / 企业日常办公 | 个人开发 |
| 支持模型 | 文本生成 + 图像生成 | 仅文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次 | 无每 5 小时 / 每周限额 | 每 5 小时 / 每周 / 每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 可能排队 |
| 数据安全 | 承诺不使用对话数据训练模型 | 用户数据授权用于模型优化 |
| 团队管理 | 支持席位分配、角色权限、SSO/钉钉接入 | 不支持 |
| API Key 格式 | `sk-sp-xxx`（专属） | `sk-sp-xxx`（专属） |

> **注意**：两者的 API Key 与 Base URL **互不相通**，也不与百炼通用按量计费 API Key（`sk-xxx`）混用。误用不会抵扣套餐额度，且可能导致额外按量扣费。详见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## 支持的模型

### Token Plan 团队版

模型清单为**精确字符串白名单**，必须逐字符完全匹配，禁止版本兼容推理。

| 品牌 | 模型 ID | 能力 |
| --- | --- | --- |
| 千问 | `qwen3.7-max`（限时 Credits 减半） | 推理、文本生成 |
| 千问 | `qwen3.7-plus` / `qwen3.6-plus` / `qwen3.6-flash` | 推理、视觉理解、文本生成 |
| 千问 | `qwen-image-2.0` / `qwen-image-2.0-pro` | 图像生成 |
| 万相 | `wan2.7-image` / `wan2.7-image-pro` | 图像生成 |
| DeepSeek | `deepseek-v4-pro` / `deepseek-v4-flash` / `deepseek-v3.2` | 推理、文本生成 |
| 月之暗面 | `kimi-k2.6` / `kimi-k2.5` | 推理、视觉理解、文本生成 |
| 智谱 AI | `glm-5.1` / `glm-5` | 文本生成 |
| MiniMax | `MiniMax-M2.5` | 推理、文本生成 |

### Coding Plan（Pro 套餐）

同样为精确白名单。推荐模型：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5`（均支持图片理解）、`glm-5`、`MiniMax-M2.5`。更多：`qwen3.5-plus`、`qwen3-max-2026-01-23`、`qwen3-coder-next`、`qwen3-coder-plus`、`glm-4.7`。

> **注意**：Coding Plan Lite 套餐已于 2026 年 3 月 20 日停止新购、4 月 13 日停止续费与升级。已购用户可继续使用至到期，建议升级至 Pro 套餐。详见 [Coding Plan 概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

## 套餐与定价

### Token Plan 团队版

| 坐席类型 | 价格 | 额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | ¥198/坐席/月 | 25,000 Credits/坐席/月 | 轻度使用 |
| 高级坐席 | ¥698/坐席/月 | 100,000 Credits/坐席/月 | 日常高频 |
| 尊享坐席 | ¥1,398/坐席/月 | 250,000 Credits/坐席/月 | 重度依赖 |

另有**共享用量包**：¥5,000/个，625,000 Credits/个，有效期 1 个月，跨坐席共享弹性抵扣。每个阿里云账号限购一个订阅，共享用量包可叠加购买（单次最多 1000 个）。

### Coding Plan Pro

- **价格**：¥200/月
- **用量限制**：每 5 小时 6,000 次 / 每周 45,000 次 / 每月 90,000 次
- **额度恢复**：5 小时额度滚动恢复（每分钟释放 5 小时前的用量）；周额度每周一 00:00（UTC+8）重置；月额度在订阅日重置

## 快速开始

### 步骤一：订阅

- **Token Plan 团队版**：访问 [Token Plan 购买页](https://common-buy.aliyun.com/token-plan/)，选择坐席类型和数量，主账号和 RAM 账号均可订阅。
- **Coding Plan**：访问 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan)，RAM 子账号需先在百炼工作空间授权。

### 步骤二：获取 API Key 与 Base URL

**Token Plan 团队版**：在控制台成员管理页面创建成员、分配席位后生成 API Key。

**Coding Plan**：在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) 获取专属 API Key。

**Base URL 按协议区分**：

| 套餐 | OpenAI 兼容协议 | Anthropic 兼容协议 |
| --- | --- | --- |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

> **注意**：Base URL 路径必须与工具使用的协议匹配。把 OpenAI 兼容路径配在 Anthropic 端点上（或反之）会报 `401 invalid access token` 或 `400 InvalidParameter: url error`。详见 [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

### 步骤三：接入 AI 工具

支持的编程工具包括 Claude Code、Cursor、Codex、Qwen Code、OpenCode、OpenClaw、Cline、Cherry Studio、Chatbox、Kilo CLI、Qoder、Lingma、Hermes Agent 等。具体配置请参见各工具的接入文档。

## 工具调用与扩展

### 模型内置工具（仅 Token Plan）

`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 的 Responses API 内置 5 种工具：联网搜索、代码解释器、网页抓取、以图搜图、文搜图。启用后模型自动调用，不额外收费，产生的 Token 从 Credits 抵扣。

### MCP 服务

其他模型可通过百炼 MCP 广场接入联网搜索、代码解释器等工具。需要**百炼通用 API Key**（`sk-xxx`，非套餐专属 Key）鉴权。联网搜索 MCP 前 2000 次调用免费，之后 29 元/千次。

各工具接入方式不同：Claude Code 用 `claude mcp add` 命令；OpenCode 在 `opencode.json` 配置 `mcp` 字段；Qwen Code 用 `qwen mcp add` 命令；Kilo CLI 在配置文件写入 MCP 信息。详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

### 图像生成模型接入（仅 Token Plan）

图像生成模型使用独立接口，需通过工具的 Skill / Slash Command / Agent 扩展机制接入。以 Claude Code 为例，在项目根目录创建 `.claude/commands/text-to-image.md`，通过 curl 调用 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` 端点。其他工具配置文件路径见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### 视觉理解能力（Coding Plan）

`qwen3.6-plus`、`qwen3.5-plus`、`kimi-k2.5` 原生支持视觉理解，可直接传入图片。对于 `glm-5`、`MiniMax-M2.5` 等纯文本模型，可通过添加本地 Skill/Agent 辅助获得视觉能力——配置一个以 `qwen3.6-plus` 为底层模型的 image-analyzer Skill，在主模型需要时调用。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 团队管理（Token Plan 专属）

### 角色与权限

| 角色 | 权限 |
| --- | --- |
| 拥有者 | 添加/移除成员、分配/回收席位、修改角色、查看全部用量 |
| 管理员 | 与拥有者相同，可被移除或降级 |
| 成员 | 使用分配的 API Key 和 Base URL 调用模型 |

### 成员接入方式

- **手动添加**：管理员创建成员 → 分配席位 → 系统生成 API Key → 发给成员
- **SSO（SAML 2.0）接入**：对接企业 IdP（如阿里云 IDaaS），成员用 IdP 账号登录管理平台自动加入
- **钉钉接入**：创建钉钉企业内部应用 → 获取 Client ID/Secret → 配置回调域名与通讯录权限 → 在 Token Plan 管理平台填入凭证

### 席位操作

- **分配**：成员管理页面 → 选择成员 → 分配席位 → 选择档位
- **回收**：回收后席位转为未分配，原 API Key 失效，重新分配时生成新 Key
- **用量分析**：管理平台提供近 1/7/30 天 Credits 消耗趋势、各模型用量、成员消耗明细

详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

## Credits 计费（Token Plan 专属）

单次请求消耗的 Credits 由模型类型、Token 用量（输入/缓存/输出）、思考模式及工具调用动态决定。

**抵扣顺序**：
1. 优先从坐席套餐月度额度抵扣
2. 坐席额度用尽后从共享用量包抵扣（多包优先抵扣最近到期的）
3. 全部用尽后服务暂停，可购买共享用量包或等待下一计费周期重置

**额度不累积**：坐席额度与共享用量包均按月重置，未用完清零。

## 订阅管理

在 Token Plan 控制台的**我的订阅**页面可执行：

- **加购席位**：新席位与现有订阅统一到期，按剩余时长折算
- **升级席位**：低档位升高档位，按差价补缴
- **退订席位**：已有用量消耗的席位不可退订，退款原路退回（1-3 工作日）
- **批量操作**：勾选多席位批量升级/退订
- **续费 / 自动续费**：自动续费到期前 9 天扣款
- **加购共享用量包**

## 使用限制与注意事项

1. **使用范围**：仅限在兼容的 AI 编程与智能体工具中交互式使用，**不可用于自动化脚本或应用后端**。违规可能导致订阅暂停或 API Key 封禁。
2. **账号规范**：API Key 仅限已分配席位成员本人使用，不可共享或泄露。
3. **数据安全**：Token Plan 团队版承诺不使用对话数据训练模型；Coding Plan 则将数据用于模型优化。
4. **服务地域**：Token Plan 团队版目前仅支持华北2（北京）地域。Coding Plan 不限地域，海外用户可使用国际站端点（`coding-intl.dashscope.aliyuncs.com`）。
5. **模型版本严格匹配**：模型 ID 必须精确匹配白名单，任何版本号/子型号差异均视为不支持。

## 常见报错排查

| 报错 | 原因 | 解决 |
| --- | --- | --- |
| `401 InvalidApiKey` | 未携带 API Key、用了通用 Key 或订阅过期 | 使用套餐专属 API Key，确认订阅有效 |
| `404 model 'xxx' not found` | 模型 ID 拼写错误或不在白名单 | 核对精确模型 ID，区分大小写 |
| `401 invalid access token` | Base URL 与协议不匹配 | 按工具协议选对端点 |
| `400 Range of input length` | 输入超出模型上下文长度 | 新建会话、压缩上下文或换更大窗口模型 |
| `400 max_tokens / thinking_budget` | 输出/思维链长度超上限 | 调低 `max_tokens` 或 `budgetTokens` |
| `429 quota exceeded` | 额度用尽 | 加购共享用量包或等待重置 |
| `hour/week/month allocated quota exceeded`（Coding Plan） | 对应时段请求额度用尽 | 等待额度恢复 |

更多报错详见 [Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md) 和 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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



