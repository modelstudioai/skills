# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与确定性性能的推理加速能力，覆盖实时高速响应（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型调度（智能路由）等场景。所有方案均兼容 OpenAI 接口，开发者可通过统一 API 调用，按需选择成本、性能与运维复杂度的最优平衡点。

## 支持的模型/功能

百炼为不同性能目标提供分层能力：

- **Prime 模式**：面向输出速度敏感场景（如 AI 编程助手、Agent 多步推理），通过底层优化将 TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等专用模型标识，无需额外参数，仅需指定对应 model ID 即可启用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
  
- **吞吐预留（TPM 预留）与 PTU/DTU 部署**：提供刚性容量保障。吞吐预留支持标准模式与高速模式（即 PTU），适用于流量可预估且不能接受限流的生产环境；DTU（独占吞吐）与 PTU（预置吞吐）均以输入/输出 TPM 为计量单位，底层独占 GPU 资源，支持长输入与前缀缓存优化 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。DTU 是 MU（模型单元）的继任方案，新购部署应优先选用 DTU [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

- **批量推理（Batch）**：适用于非实时场景（如模型评测、数据标注），成本约为实时推理的 50%。支持华北2（北京）和新加坡地域的千问系列（`qwen3.8-max`、`qwen3.7-plus` 等）、多模态模型（`qwen3-vl-plus`）及向量模型（`text-embedding-v3`）[批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

- **智能路由**：动态分析请求内容，在预设备选模型集中自动匹配最优模型（如 `qwen3.8-flash` 或 `glm-5.2`），兼顾效果与成本。仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与文本 Chat Completions 请求，不支持流式、Batch 或非生成类接口 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档中“PTU 预置吞吐”在控制台已统一迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面管理，专属部署页面仅提供入口。旧文档中单独描述的 PTU 页面（如 `model-deployment-modes/ptu-long-input-and-cache.md`）内容已整合，开发者应以吞吐预留文档为准。

## 关键参数

| 参数 | 说明 | 使用约束 |
|------|------|----------|
| `model` | 指定推理模型或服务标识 | Prime 模式需填 `glm-5.2-fast-preview`；吞吐预留/DTU/PTU 需填专属模型 code；智能路由固定为 `auto-model-xxxxxx`；Batch 不支持思考字段，即使设置 `enable_thinking=true`，结果文件中也不含 `reasoning_content` [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `stream` | 是否启用流式响应 | Prime 模式下[流式输出](../concepts/streaming-output.md)时，思考内容与回答内容分别通过 `delta.reasoning_content` 与 `delta.content` 推送 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |
| `enable_thinking` | 控制是否启用深度思考模式 | Batch 场景下该参数对结果文件无影响；实时 API 中需显式设置 `true`/`false`，且必须与 `model` 同级传入，不可置于 `extra_body` 中 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `input_tpm` / `output_tpm` | 吞吐预留或 DTU/PTU 的容量配额 | 创建时需为基准 TPM 的整数倍，各模型有固定基准值（如 `qwen3.7-plus-2026-05-26` 基准输入 TPM 为 1,372,000） [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md) |
| `response_format` / `max_tokens` | 智能路由的路由过滤条件 | 设置后仅路由到支持该参数的备选模型；`max_tokens` 会自动转为 `max_completion_tokens` [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |

## 使用方式

- **Prime 模式**：直接调用标准 `/v1/chat/completions` 接口，`model` 设为 `glm-5.2-fast-preview` 等 Prime 模型 ID，接入域名使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
  
- **吞吐预留/PTU/DTU**：在控制台创建预留或部署服务后，获取专属 `model code`，替换 API 请求中的 `model` 参数。例如：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"your-dedicated-model-code","messages":[{"role":"user","content":"你好"}]}'
  ```

- **批量推理**：构造符合规范的 JSONL 文件（每行一个 `POST /v1/chat/completions` 请求），通过控制台或 API 提交任务；结果文件为独立下载项，不包含 `reasoning_content` 字段 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

- **智能路由**：将 `model` 设为 `auto-model-xxxxxx`，其余参数与普通 Chat Completions 一致；响应头 `x-dashscope-resolved-model` 返回实际执行模型，计费按该模型单价结算 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

## 限制和注意事项

- **容量费用刚性计费**：吞吐预留、PTU、DTU、MU 均为预付费模式，创建成功即开始计费，与是否调用无关；即使未发起任何请求，费用也全额产生 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
  
- **模型能力一致性**：Prime 模式、吞吐预留、DTU/PTU 所支持的模型能力（如思考模式、上下文长度、缓存支持）与原版模型完全相同，但部分参数（如 GLM-5.2 的 `thinking_budget`）在特定部署下不生效 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。

- **协议与地域限制**：智能路由仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、`maas.aliyuncs.com` 域名及北京/新加坡地域；不支持 DashScope 协议、`dashscope.aliyuncs.com` 域名、图片/视频输入、Batch 或 Embedding 接口 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

- **缓存行为差异**：Prime 模式与吞吐预留支持前缀缓存并提供缓存折扣（如 `glm-5.1` 缓存命中部分按 20% 折算容量）；智能路由仅依赖实际调用模型的隐式缓存，不保障命中率，且忽略用户显式缓存参数 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **错误处理策略**：吞吐预留/PTU/DTU 在溢出时可选「自动溢出至按量计费」（默认，服务不中断）或「仅使用预留容量」（超限返回 429）；智能路由故障自动切换仅对模型不可用生效，对 429（限流）、400/403/500 等确定性错误不触发 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


