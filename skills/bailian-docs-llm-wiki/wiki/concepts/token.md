# Token

Token 是百炼平台对模型输入与输出内容进行标准化计量的基本单位，用于精确衡量语言模型处理文本、多模态数据（图像、音频）时的计算资源消耗。1 个 token 通常对应一个子词（subword）或字节对编码（BPE）单元，在实际调用中，其数量由模型 tokenizer 动态计算得出，而非简单按字符或字数折算。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与资源包管理**：Token 是 Token Plan 资源包的计量和抵扣单位。每次 API 调用产生的 `input_tokens` 和 `output_tokens` 总和将实时从已购 Token Plan 中扣除；余额不足时自动回退至后付费模式。
- **高吞吐推理（TPM Reservation）**：吞吐预留以 **tokens per minute（TPM）** 为单位配置，用于保障每分钟可稳定处理的 token 总量（含输入+输出），是性能隔离与 QPS 稳定性的核心度量。
- **实时流式接口（Realtime API / Omni Realtime API）**：token 是流式响应粒度的基础——服务端按 token 增量推送 `text.delta` 或 `audio.delta` 事件；`max_tokens` / `max_output_tokens` 等参数均以 token 为上限单位实施硬性截断。
- **账单分析（Billing API）**：`GetBillingOverview` 和 `GetBillingTrend` 接口直接返回 `total_tokens_used` 及按模型/项目分组的 token 消耗明细，是用量审计与成本归因的核心指标。
- **组织级配额治理（TokenPlan API）**：虽不直接暴露 token 数值，但席位（seat）分配与成员用量统计最终映射到 token 消耗行为上，支撑企业级资源分账与预算控制。

> ⚠️ 注意：Token 不是认证凭证（如 API Key 或 Bearer Token），也不等同于 HTTP 请求中的 `Authorization` 头；它纯粹是**模型计算负载的计量单位**，全程由服务端 tokenizer 自动统计，开发者无需手动拆分或估算。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 典型取值示例 |
|---------|-----------|------|----------------|
| `input_tokens` / `output_tokens` | 所有模型 API 响应体 | 每次调用实际消耗的输入/输出 token 数，返回在 `usage` 字段中 | `"usage": {"input_tokens": 127, "output_tokens": 43}` |
| `max_tokens` / `max_output_tokens` | Realtime API、Omni Realtime API | 强制截断响应长度的 token 上限（硬限制） | `2048`, `4096` |
| `tpm_reservation` | 高速推理（Model High Speed Inference） | 预留吞吐量，单位为 tokens per minute | `5000`, `10000`（须为 1000 的整数倍） |
| `X-DashScope-Token-Plan-ID` | 请求 Header | 指定本次调用优先使用的 Token Plan | `plan-abc123xyz` |
| `remaining_tokens` | Token Plan 查询接口（`/v1/token_plan/balance`） | 当前资源包剩余可用 token 数 | `124890` |

- 所有 token 计数均基于模型原生 tokenizer（如 Qwen 使用 QwenTokenizer），对中文、英文、符号、emoji、Base64 图像编码等均有统一且确定的切分逻辑；
- 多模态输入（如图像 URL、base64 编码图）会经视觉 encoder 转换为固定数量的视觉 token，计入 `input_tokens`；
- 流式响应中，每个 `text.delta` 事件携带的字符串可能对应 1~N 个 token，不可假设“1 字符 = 1 token”。

## 面向开发者，简洁实用

- ✅ **必查响应字段**：所有同步/异步模型 API 响应中，务必解析 `usage.input_tokens` 和 `usage.output_tokens`，用于本地用量监控与预算预警；
- ✅ **流式开发注意**：Realtime/Omni 接口不返回累计 token 数，需客户端自行累加 `text.delta` 事件长度（推荐用 SDK 内置计数器，避免 Unicode 边界错误）；
- ✅ **调试技巧**：若需预估 token 消耗，可调用 `/v1/tokenizer/count`（需开通权限）对 [prompt](../guides/prompt.md) 进行离线计数，结果与线上一致；
- ❌ **不要手动换算**：避免用字符数 × 系数估算 token —— 中文平均 ~1.5 字符/token，英文 ~0.75 字符/token，但受内容结构影响极大；
- ❌ **不要复用 token 值做认证**：`X-DashScope-Token-Plan-ID` 是资源包 ID，不是密钥；API 认证始终使用独立的 `Authorization: Bearer <api_key>`。

Token 是百炼平台资源计量的“原子单位”。理解它，就掌握了用量、成本、性能与配额控制的共同语言。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [billing api](../api/billing-api.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


