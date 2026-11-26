# Token

Token 是百炼平台中用于计量模型输入与输出文本单元的基本单位，是模型推理成本核算、资源配额控制与性能监控的核心度量基础。一个 Token 通常对应一个子词（subword）或标点符号，在中文场景下平均约等于 1.5–2 个汉字，具体切分由模型所用 tokenizer 决定。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 订阅服务**：Token 不作为直接计费单位，而是底层计量依据——Credits 消耗量由实际 `input_tokens`、`output_tokens` 及缓存命中、工具调用等因子加权计算得出。开发者无需手动统计 Token 数，但需理解其对 Credits 消耗的影响（例如长上下文、多轮工具调用会显著增加 Token 总量，从而提升 Credits 扣减）。

- **按量计费（test-1）**：Token 是精确计费的直接依据。调用 `/v1/chat/completions` 等接口后，系统自动解析请求中的 `input_tokens` 和响应中的 `output_tokens`，按模型单价（元/千 Token）实时计费。该数值可在账单明细、用量监控和 OpenAPI 返回头（如 `X-DashScope-Usage: {"input_tokens":128,"output_tokens":64}`）中获取。

- **模型监控（[model monitoring](../guides/model-monitoring.md)）**：Token 消耗是核心可观测指标之一，监控页展示「总 Token 数」（`input_tokens + output_tokens`），用于分析服务负载、识别异常请求（如超长 prompt）、评估成本趋势。注意：该统计不含系统提示词（system prompt）和工具调用内部开销，仅覆盖用户显式传入内容与模型生成结果。

- **多模态能力（图像/语音/视频生成等）**：Token 概念不直接适用。此类服务采用独立计费模型（如“每次生成”或“每秒音频”），但其 API 请求体中仍可能包含文本描述（caption、prompt），这部分文本会被 tokenizer 处理并计入 `input_tokens`（影响 Token Plan Credits 或按量费用），需在调试时关注。

- **API 鉴权与路由**：Token 本身不参与鉴权，但 API Key 类型（`sk-sp-` vs `sk-`）决定了 Token 的归属通道——`sk-sp-` Key 的调用走 Token Plan Credits 通道，`sk-` Key 的调用走按量或 Harness 通道，二者 Token 计量逻辑隔离，不可混用。

- **开发调试与优化**：开发者可通过 SDK 的 `response.usage` 字段（OpenAI 兼容格式）或响应头 `X-DashScope-Usage` 获取本次调用的精确 Token 数，用于：
  - 估算成本（结合模型单价）
  - 优化 prompt 长度与结构
  - 判断是否触发限流（TPM/RPM 基于 Token 速率）
  - 调试缓存效果（缓存命中时 `input_tokens` 仍计费，`output_tokens` 显著减少）

## 关键参数和配置

- `input_tokens` / `output_tokens`：只读字段，由服务端 tokenizer 自动计算，不可手动设置。在 [OpenAI 兼容接口](openai-compatible-interface.md)中通过 `response.usage` 返回；在 DashScope 原生接口中通过响应头 `X-DashScope-Usage` 返回（JSON 格式字符串）。

- `max_tokens`：请求参数，用于限制模型最大生成长度（即 `output_tokens` 上限）。设置过小可能导致截断，过大则增加延迟与费用。建议根据业务需求合理设定，避免盲目设为 `8192`。

- `thinking.budget_tokens` / `thinking_budget`：Anthropic/OpenAI 兼容参数，**Token Plan 当前不支持**（`auto` 模型及多数指定模型均忽略该参数）。如需控制推理深度，请改用 `max_tokens` 或模型专属参数（如 Qwen 的 `max_new_tokens`）。

- 缓存相关：百炼支持响应缓存（需开启），缓存命中时 `output_tokens` 按实际返回内容计费，但 `input_tokens` 仍全额计费——这是设计行为，非 bug。

## 面向开发者，简洁实用

- ✅ **必查**：每次调试模型调用后，务必检查 `X-DashScope-Usage` 响应头或 `response.usage`，确认 Token 数是否符合预期。异常高的 `input_tokens` 往往意味着 prompt 中混入了冗余日志、注释或未清理的 base64 图片数据。

- ✅ **必配**：在生产环境，为所有 `chat/completions` 请求显式设置 `max_tokens`，防止失控生成导致 Token 暴增与费用飙升。

- ⚠️ **禁用**：不要尝试用 `sk-` Key 调用 Token Plan 模型（如 `qwen4-max`），或用 `sk-sp-` Key 调用 Harness 工具（如 `EnhancedSearch/mcp`）——将返回 `401 Unauthorized` 或 `429 insufficient_quota`，且无法抵扣任何额度。

- 🛑 **严禁**：将 `sk-sp-` API Key 用于自动化脚本、定时任务或高并发批量调用。Token Plan 明确禁止生产级自动化使用，违者将被暂停订阅。

- 💡 **技巧**：想快速估算 Token 数？用百炼控制台「模型调试」页粘贴文本，点击「计算 Token」即可实时查看（基于当前模型 tokenizer）。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan personal](../guides/token-plan-personal.md)
- [token plan team edition](../guides/token-plan-team-edition.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [token plan best practice](../guides/token-plan-best-practice.md)


