# Token

Token 是百炼平台中用于计量模型输入与输出文本单元的最小计费与配额单位，其本质是模型分词器（Tokenizer）对原始文本进行切分后产生的离散符号。一个 Token 可能对应一个汉字、一个英文单词、一个标点，或子词（subword）片段；具体数量取决于模型所用分词器（如 Qwen 系列使用 QwenTokenizer），而非字符数或字节数。Token 是平台进行用量统计、配额控制、计费结算和性能监控的核心度量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用配额管理（Token Plan）**：Token 是 Token Plan 的计量基础。每次请求的 `input_tokens` 与 `output_tokens` 实时计入所选 plan（如 `"team-pro"`）的总配额池，并受 `max_tokens` 单次硬限流约束。流式响应中，token 消耗仅在 final chunk 返回时统一扣减。
- **模型部署计费模式**：在 Token 按量部署（`plan=lora`）模式下，服务按实际消耗的 input/output token 总数精确计费；而 PTU（预置吞吐）和 MU（独占算力）模式虽不按 token 实时扣费，但其容量规格（如 `input_tpm`）仍以 token/分钟为单位定义吞吐能力。
- **用量监控与告警**：模型监控中的 `TotalToken 数`、`TPM`（Tokens Per Minute）、`平均单次请求调用量` 等核心指标均基于 token 统计，支持按模型、API Key、时间维度精细化分析用量趋势与异常。
- **[异步任务](asynchronous-task.md)与[多模态](multi-modal.md)处理**：图像/视频/语音类[异步任务](asynchronous-task.md)最终返回的文本结果（如 OCR 文本、语音转写内容、图生文描述）同样计入 token 消耗；[多模态](multi-modal.md)模型（如 Qwen-VL）对图像编码后的视觉 token 与文本 token 统一纳入总量统计。
- **SDK 与调试辅助**：DashScope SDK Expert 及 CLI 工具默认在响应中返回 `usage` 字段（含 `input_tokens`/`output_tokens`），开发者可直接获取 token 消耗明细，用于成本估算与 [prompt](../guides/prompt.md) 优化。

## 关键参数和配置

- `max_tokens`（请求级）：可选整数，限制单次响应最大生成 token 数，优先级高于 Token Plan 总配额，超限将截断输出并返回 `finish_reason="length"`。
- `X-Qwen-Plan`（Header）：必填字符串，指定生效的 Token Plan（如 `"personal"`、`"team-pro"`），决定本次请求从哪个配额池扣减 token。
- `enable_thinking=true`（思考模式）：启用后，模型内部推理过程产生的“思考 token”将额外计费（计入 `output_tokens`），且必须配合 `incremental_output=true` 使用。
- `stream=true`：流式调用时，`usage` 仅在最后一个 chunk 中返回完整 token 统计，中间 chunk 不触发配额扣减。
- `response_format={"type": "json_object"}`：结构化输出不改变 token 计算逻辑，但需注意：思考模式模型不支持该格式，须关闭 `enable_thinking` 才可启用。

> ⚠️ 注意：`free` plan 已下线；所有新应用默认绑定 `"personal"` plan。Token 消耗不可跨模型共享（如 `qwen-plus` 与 `qwen3-235b` 分别计费），也不跨部署模式混用（Token 按量部署的消耗不计入 PTU 配额）。

## 面向开发者，简洁实用

- ✅ **查用量**：调用后检查响应 `response.usage.input_tokens` 和 `response.usage.output_tokens`；或通过 `/v1/usage` 接口、控制台「用量中心」实时查询剩余配额。
- ✅ **控成本**：对长 [prompt](../guides/prompt.md) 场景，先用 `qwen-turbo` 或 `qwen-plus` 估算 token 数（`Generation.call(model="qwen-plus", messages=[...], top_p=0.01, max_tokens=1)`），再决定是否升级模型。
- ✅ **避踩坑**：
  - [多模态](multi-modal.md)输入中，一张高分辨率图经视觉编码可能产生数千 token，务必在测试阶段验证 `usage`；
  - 启用 `enable_thinking` 时，`output_tokens` 显著增加，建议开启 `incremental_output` 并监控首 token 延迟；
  - 使用临时文件（`oss://` URL）调用多模态模型时，需显式添加 Header `X-DashScope-OssResourceResolve: enable`，否则解析失败导致 token 计费异常。
- ✅ **调优建议**：精简 system [prompt](../guides/prompt.md)、压缩历史对话（如用 summary 替代全量 history）、禁用非必要功能（如 `tool_calls` 中未使用的工具），可直接降低 input token 消耗。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [model deployment index](../guides/model-deployment-index.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


