# Token

Token 是百炼平台中用于计量和管控模型调用资源消耗的基本单位。它代表模型处理输入内容（如文本、图像描述、音频转录等）与生成输出内容时所消耗的计算资源量，是配额管理、计费统计、限流控制与性能监控的核心度量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **资源配额与限流（Token Plan）**：Token 是 Token Plan 的核心计量单位。平台通过 `tokens_per_minute`（每分钟总 token 配额）、`max_tokens_per_request`（单次请求最大输出 token 数）等参数对模型调用进行硬性或软性约束。输入 token 包含 system [prompt](../guides/prompt.md)、user message 及 tool call 参数；base64 图片/音频字符串仅计 1 token（实际解析开销由后端单独核算）。

- **用量统计与成本治理**：在「模型用量」页面，所有大语言模型（LLM）调用量均以 TotalToken 数为统计单位（图像/语音等模态按“张”“秒”等独立单位统计）。该数据延迟约 1 小时，用于计费对账，与实时监控指标严格分离。

- **监控与告警**：`TotalToken 数` 是预置告警模板支持的关键指标之一，可用于配置“模型消耗 Token 突增”类成本类告警；同时，`限流错误次数`（HTTP 429）直接反映 token 配额瓶颈，建议同步告警。

- **API 调用与 SDK 初始化**：Token 本身不参与身份认证（认证使用 `api_key` 或阿里云 AccessKey），但所有模型请求的实际 token 消耗会实时计入绑定的 Token Plan，并影响限流策略生效。SDK 调用无需手动计算 token，平台在服务端完成标准化计数（遵循 Qwen 系列 tokenizer 规则，多模态内容按平台定义的折算规则统一换算）。

- **组织级资源编排（Token Plan API）**：Token Plan API 不直接操作 token，而是通过席位（`standard`/`pro`/`max`）分配和订阅管理，间接调控成员可使用的 token 配额总量与规格，实现企业级资源隔离与生命周期管控。

## 关键参数和配置

| 参数 | 说明 | 所属模块 | 是否可配置 |
|------|------|----------|------------|
| `tokens_per_minute` | 每分钟允许消耗的总 token 数（input + output），自然分钟（UTC+0）统计，超限触发限流 | Token Plan | ✅ 控制台/API 创建计划时设置 |
| `max_tokens_per_request` | 单次请求最大输出 token 数，硬限制，超限返回 HTTP 400 | Token Plan | ✅ |
| `burst_capacity` | 突发容量（token），按秒级窗口平滑释放，非传统令牌桶 | Token Plan | ✅（进阶配置） |
| `model_fallback` | 主模型 token 配额耗尽时自动降级的备用模型（限同 family） | Token Plan | ✅ |
| `TotalToken 数` | 监控/用量页展示的累计消耗 token 总量，用于告警与对账 | 模型监控 & 用量统计 | ❌（只读） |

> ⚠️ 注意：`burst_capacity` 行为以 [Token Plan 进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 文档为准；`base64` 类二进制内容在 token 计数中仅计 1 token，真实计算负载由后端独立评估。

## 面向开发者，简洁实用

- ✅ **首次调用前**：无需手动分词或估算 token —— 平台自动完成计数，你只需关注业务逻辑。
- ✅ **调试配额问题**：若遇到 `429 Too Many Requests`，检查 `/v1/token-plan/status` 接口返回的 `remaining_tokens` 和 `rate_limit_exceeded` 字段；若遇 `400` 错误，确认 `max_tokens_per_request` 是否过小。
- ✅ **选型建议**：通用场景优先选用 `qwen3.8-plus`（均衡）；高并发低延迟场景用 `qwen3.8-flash`；复杂推理任务用 `qwen3.8-max` —— 它们的 token 效率与响应速度差异直接影响你的配额利用率。
- ✅ **安全实践**：`api_key` 仅用于模型 API 调用，**不可用于 Token Plan API**（后者强制使用阿里云 AccessKey + 签名）；避免将 key 硬编码或泄露至前端。
- ✅ **生产部署必做**：务必使用业务空间专属域名（含 `WorkspaceId`），并显式声明 `x-bailian-token-plan-id` header，否则请求将走默认 plan，可能导致配额不可控。

Token 是百炼平台资源治理的“原子单位”。理解它，就掌握了用量、成本、稳定性三者的统一标尺。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [model monitoring](../guides/model-monitoring.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)


