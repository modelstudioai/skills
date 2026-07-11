# token plan guide

Token Plan 团队版与 Coding Plan 是百炼平台面向 AI 编程/智能体场景的两类订阅制套餐：前者以 Credits 按 Token 消耗计量、面向团队协作，后者按模型调用次数计量、面向个人开发者。两者均提供专属 API Key 与 Base URL，兼容 OpenAI / Anthropic 接口标准，可接入 Claude Code、Qwen Code、OpenClaw、Cursor 等主流工具。本文汇总两类套餐的模型支持、接入方式、计费规则及常见问题。

## Token Plan 团队版 vs. Coding Plan

两者是相互独立的订阅计划，不支持互转（即使补差价也不行），可同时订阅、各自独立计费。核心差异见下表（详见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)）：

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 团队/企业日常办公 | 个人开发 |
| 支持模型 | 文本生成 + 图像生成 | 文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次限制 | 无 5 小时/每周限额 | 有 5 小时/每周/每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期可能排队 |
| 数据安全 | 承诺不用于模型训练 | 输入/输出用于服务改进与模型优化 |
| API Key 前缀 | `sk-sp-` | `sk-sp-` |

> **注意**：两类套餐的 Base URL 不同（Token Plan 为 `token-plan.cn-beijing.maas.aliyuncs.com`，Coding Plan 为 `coding.dashscope.aliyuncs.com`），且与百炼按量付费（`dashscope.aliyuncs.com` + `sk-` 通用 Key）三者完全隔离，必须配套使用，混用会导致意外扣费或 401/403 鉴权失败。

## 支持的模型

模型清单为**精确字符串白名单**，必须逐字符完全匹配，版本号/子型号任何差异均视为不支持，禁止做版本兼容推理。

- **Token Plan 团队版**：涵盖千问（qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0/-pro）、万相（wan2.7-image/-pro）、DeepSeek（deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2）、月之暗面（kimi-k2.7-code、kimi-k2.6、kimi-k2.5）、智谱（glm-5.2/5.1/5）、MiniMax（MiniMax-M2.5）。完整清单与能力标签见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **Coding Plan（Pro 套餐）**：推荐 qwen3.7-plus、qwen3.6-plus、kimi-k2.5（均支持图片理解）、glm-5、MiniMax-M2.5；更多模型包括 qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。详见 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

> **注意**：Coding Plan Lite 基础套餐已于 2026 年 3 月 20 日停止新购、4 月 13 日停止续费与升级，已购用户可用至到期，新用户请选择 Pro 套餐。

## 快速接入（三步）

以 Token Plan 团队版为例：

1. **订阅**：在购买页选择坐席类型、数量和订阅周期。RAM 子账号订阅前需主账号授予 `AliyunBailianFullAccess` 权限。
2. **获取 API Key 与 Base URL**：管理员在成员管理页为账号分配席位后生成 API Key（`sk-sp-` 开头，仅首次显示一次，务必立即保存）。按工具协议选择端点：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. **接入 AI 工具**：支持 OpenClaw、Claude Code、OpenCode、Cursor、Codex、Qwen Code、Cline、Qoder、Lingma、Kilo CLI 等。完整步骤见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

Coding Plan 的 Base URL 为 `https://coding.dashscope.aliyuncs.com/v1`（OpenAI 兼容）或 `https://coding.dashscope.aliyuncs.com/apps/anthropic`（Anthropic 兼容）。

## 团队管理（Token Plan 团队版）

Token Plan 团队版提供管理后台，支持三类角色：所有者、管理员、成员。RAM 用户使用前需授予 `AliyunTokenPlanReadOnlyAccess` 或 `AliyunTokenPlanFullAccess` 系统策略，并在百炼账号管理页分配相应权限。

- **成员接入方式**：手动添加（仅供 API 调用，不能登录管理平台）或通过 SAML 2.0 / 钉钉 SSO 登录（成员可自管席位与 API Key）。
- **席位操作**：分配 / 回收 / 加购 / 升级。席位是最小订阅单位，一个席位绑定一个成员、对应一个 API Key，不可共享。加购与升级均按剩余时长折算费用。
- **用量分析**：所有者可查看近 1/7/30 天的 Credits 消耗趋势、各模型用量及成员消耗明细。

SAML/钉钉的完整配置流程（含阿里云 IDaaS 示例）见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

## 工具调用与扩展能力

- **模型内置工具**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 的 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，模型按需自动调用。内置工具不额外收费，token 消耗统一从 Credits 抵扣。
- **MCP 服务**：其他模型（如 deepseek-v3.2、glm-5）通过百炼 MCP 广场接入。联网搜索 MCP 全部用户前 2000 次免费，之后按 29 元/千次计费。接入 MCP 使用的是**百炼通用 API Key（`sk-` 开头）**，与套餐专属 Key 不同。

> **注意**：联网搜索 MCP 已从旧版 SSE 协议升级为 Streamable HTTP 协议，正确 Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`；若地址以 `/sse` 结尾说明仍是旧版，需在 MCP 广场取消开通后重新开通完成升级。

### 图像生成与视觉理解

- **图像生成模型**（qwen-image-2.0、wan2.7-image 等）使用独立接口，无法通过文本模型 Base URL 直接调用，需借助工具的 Skill / Slash Command / Agent 扩展机制接入。以 Claude Code 为例，可创建 `.claude/commands/text-to-image.md` 调用文生图 API，详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
- **视觉理解**：Coding Plan 中 qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉，直接切换模型即可；glm-5、MiniMax-M2.5 等纯文本模型需通过本地 Skill/Agent 辅助获得视觉能力，详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 计费与额度

- **Token Plan 团队版**：单次消耗的 Credits 由模型类型、Token 用量、思考模式、工具调用等动态决定。抵扣顺序为：坐席月度额度 → 共享用量包（优先抵扣最近到期的）→ 全部用尽后服务暂停。坐席额度按订阅月重置且不累积；共享用量包有效期 1 个月，到期未用自动清零。
- **Coding Plan**：按模型调用次数扣额度（简单任务约 5-10 次，复杂任务 10-30+ 次）。每 5 小时额度滚动恢复、每周一 00:00 重置、每月按订阅日重置。

> **注意**：Token Plan 团队版续费**不会**叠加补充至当前计费周期，仅延长有效期或预定下一周期额度。当前周期额度用尽需立即恢复时，应购买共享用量包、升级坐席或加购坐席。

## 限制与注意事项

1. **使用范围**：两类套餐均仅限在兼容的 AI 编程/智能体工具中**交互式**使用，禁止用于自动化脚本、应用后端或非交互式批量调用，违规可能导致订阅暂停或 API Key 封禁。
2. **账号规范**：API Key 仅限本人使用，不可共享或公开。API Key 仅在生成/重置时完整显示一次，丢失后需重置（原 Key 立即失效）。
3. **服务地域**：Token Plan 团队版目前仅支持华北2（北京）地域；Coding Plan 不限制使用地域，海外用户可正常使用。
4. **退款**：Token Plan 团队版支持按席位退订（已消耗用量的席位不可退订），退款 1-3 个工作日原路退回；Coding Plan **不支持退款**。
5. **限购**：每个阿里云账号限购一个 Token Plan 订阅；共享用量包需先订阅坐席套餐后才能购买，单次最多 1000 个。
6. **常见报错**：401 多为误用 Key/Base URL 或订阅过期；404/400 model not found 多为模型名拼写或不在白名单；429 多为额度耗尽或触发限流（限流按主账号维度合并计算）。排查详情见 [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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


