# model high speed inference

百炼平台提供多种面向高性能、低延迟与高吞吐场景的推理加速能力，覆盖异步批量处理、实时高速[流式输出](../concepts/streaming-output.md)、专属资源保障及智能动态调度四大范式。开发者可根据业务对延迟敏感度、流量稳定性、成本弹性及模型效果确定性等维度，选择最适合的方案。

## 支持的模型/功能

百炼支持的高速推理能力按使用模式划分为四类，各模式支持的模型存在差异，需结合地域与具体版本确认：

- **批量推理（Batch）**：适用于非实时、高吞吐离线任务，支持文本生成、多模态（图像/视频理解、OCR、全模态）、向量嵌入等模型。华北2（北京）与新加坡地域均支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等系列，以及 `qwen3-vl-plus`、`qwen-vl-ocr`、`qwen3.5-omni-plus` 等多模态模型；向量模型支持 `text-embedding-v1` 至 `v4` 及 `qwen3.7-text-embedding` 系列 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **Prime 模式**：面向实时流式场景（如编程助手、Agent 多步推理），通过优化推理引擎提升 TPS 至标准 API 的 1.5~2 倍。当前仅支持 GLM 系列（如 `glm-5.2-fast-preview`、`glm-5.3-prime`）与 Wan 视频生成模型（如 `wan3.0-video-prime`），不支持千问系列模型 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM Reservation）与专属部署（PTU/DTU）**：通过预置专属资源保障稳定吞吐与低延迟。支持 Qwen3、GLM、DeepSeek、Kimi 等主流模型，包括 `qwen3.8-max`、`qwen3.7-plus-2026-05-26`、`glm-5.2`、`deepseek-v4-flash` 等；其中 DTU 还支持自定义 LoRA 微调模型部署 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **智能路由（Smart Routing）**：动态匹配请求内容至最优备选模型，仅支持文本 Chat Completions 接口，备选集包含 `qwen3.8-flash`、`qwen3.7-plus`、`qwen3.7-max`、`deepseek-v4-flash-0731`、`glm-5.2` 等，不支持多模态、Embedding 或 Batch [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 2（Prime 模式）明确指出其“不支持千问系列模型”，而文档 1（批量推理）和文档 3（吞吐预留）均列出大量千问模型。这表明 Prime 模式是 GLM/Wan 专属加速通道，与千问模型的高速能力（如 PTU/DTU）属于正交方案，开发者不可混淆调用。

## 关键参数

不同高速模式的关键控制参数如下：

- **批量推理**：核心参数为 `custom_id`（必填唯一标识）、`enable_thinking`（顶层 body 参数，控制思考模式开关，`qwen3.8`/`qwen3.7` 系列默认开启）、`thinking_budget`（思考 token 预算）。注意：结果文件中**不返回** `reasoning_content` 字段，需实时 API 获取 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **Prime 模式**：无额外参数，仅需将 `model` 设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`），并使用专用域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。响应中 `usage.completion_tokens_details.reasoning_tokens` 明确统计思考消耗。
- **吞吐预留 / PTU / DTU**：关键参数为 `input_tpm` 与 `output_tpm`（PTU/DTU 计费与容量单位）、`plan: "ptu"` 或 `"mu"`（API 部署时指定）、`overflow_strategy`（溢出策略：`auto_overflow` 或 `only_reserved`）。DTU 模式下 `rpm_limit` 和 `tpm_limit` 为可选配置项。
- **智能路由**：关键参数为 `enable_thinking`（影响模型筛选）、`max_tokens`（自动转为 `max_completion_tokens` 并过滤不支持模型）、`response_format` 等。以下参数**禁止使用**：`top_p`, `temperature`, `n`, `stop`, `tool_choice`, `logprobs`, `thinking_budget` [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

## 使用方式

- **批量推理**：构造 UTF-8 编码 JSONL 文件，每行一个含 `custom_id`, `method`, `url`, `body` 的对象；`body` 格式与 `/v1/chat/completions` 或 `/v1/embeddings` 一致。上传后异步处理，结果通过控制台或 API 下载 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **Prime 模式**：直接使用 OpenAI 兼容 SDK 或 curl，`model` 参数设为 Prime 模型 ID，`base_url` 指向 `maas.aliyuncs.com` 域名。流式响应中需分别处理 `delta.reasoning_content` 与 `delta.content`。
- **吞吐预留 / PTU / DTU**：
  - 控制台：在[吞吐预留](https://bailian.console.aliyun.com/cn-beijing/model/tpm-reservation)页创建，获取专属 `model code` 后替换 API 中的 `model` 参数。
  - API：使用 `/api/v1/deployments` 接口，`plan` 设为 `"ptu"` 并传入 `ptu_capacity`，或设为 `"mu"` 并传入 `deploy_spec` 等参数 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。
- **智能路由**：创建后获得 `auto-model-xxxxxx` code，调用时仅需将 `model` 替换为此 code，其余参数与普通模型完全一致，零代码改造 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

## 限制和注意事项

- **功能边界**：批量推理不返回思考过程；Prime 模式不支持千问模型；智能路由**不支持**多模态输入、Embedding/Rerank、Batch、`tool_call` 等非 Chat Completions 场景；[Token](../concepts/token.md) 按量部署**仅支持 LoRA 微调模型**，且一个月不使用将自动释放 [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)。
- **地域与协议约束**：智能路由仅支持北京与新加坡地域，且**必须使用 `maas.aliyuncs.com` 域名与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)**，不支持 `dashscope.aliyuncs.com`；批量推理的媒体 URL 必须为公网可访问地址，不支持本地路径或内网地址 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **计费与资源**：吞吐预留、PTU、DTU 均为**预付费模式，创建即开始计费，与是否调用无关**；溢出策略为 `auto_overflow` 时，超量请求降级为按量计费并返回 `x-dashscope-ptu-overflow:true` Header；DTU/MU 提前退订按 1.2 倍系数结算 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **模型兼容性**：多模态模型（如 `qwen3-vl-plus`）在批量推理中 `content` 字段必须为数组格式，且同一请求中媒体 URL 类型需一致（全图片/全视频）；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 来源文档

- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)


