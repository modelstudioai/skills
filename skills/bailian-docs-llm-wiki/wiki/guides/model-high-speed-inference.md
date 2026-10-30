# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化的推理加速能力，覆盖实时高速响应（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型调度（智能路由）四大技术路径。所有方案均兼容 OpenAI 接口，开发者可通过统一 API 调用，按需选择性能、确定性与成本的最优平衡点。

## 支持的模型/功能

百炼为不同场景提供分层加速能力：

- **Prime 模式**：面向输出速度敏感场景（如 AI 编程助手、Agent 多步推理），通过底层优化将 TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，能力与原版模型完全一致，无需额外参数，仅需指定对应 model ID 即可启用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
  
- **吞吐预留（TPM 预留）与 PTU/DTU 部署**：提供专属推理容量保障。吞吐预留支持 Qwen3.8-Max、GLM-5.2、DeepSeek-v4 系列等主流模型；PTU 部署进一步强化性能档位（标准/高速模式），支持长输入与前缀缓存；DTU 则面向独占算力与微调模型部署，支持 qwen3.5-397b-a17b、glm-5.2 等大模型规格 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。> **注意**：文档 2 与文档 5 均提及“PTU 高速模式”，但文档 5 明确指出“性能模式”选项包含“标准模式（与标准 API 相同 TPS）/ 高速模式（即 PTU 模型部署，相比标准 API 有 1.5～2 倍 TPS 提升）”，而文档 2 未明确该模式是否等同于 Prime 模式。二者定位不同：Prime 是轻量级 API 层加速，PTU 是资源层预置，不可混用。

- **批量推理（Batch）**：适用于非实时场景（如模型评测、数据标注），成本约为实时推理的 50%。支持千问全系列（Max/Plus/Flash/Long）、多模态（qwen3-vl-plus）、向量模型（text-embedding-v3/v4）等，单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

- **智能路由**：动态匹配请求内容与备选模型集，实现效果与成本的自动权衡。当前版本 `model-router-20260908` 支持 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813` 等 11 个文本生成模型，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用。

## 关键参数

| 参数 | 说明 | 适用场景 |
|------|------|----------|
| `model` | 必填。取值为：<br>- Prime 模型 ID（如 `glm-5.2-fast-preview`）<br>- 吞吐预留/PTU/DTU 生成的专属 model code<br>- 智能路由 model-code（如 `auto-model-abcd1234`）<br>- Batch 输入文件中各请求的 model 字段 | 全部加速方式 |
| `stream` | 控制响应格式。流式调用时，Prime 模式需显式解析 `delta.reasoning_content` 与 `delta.content` 字段 | Prime、PTU、DTU、智能路由 |
| `enable_thinking` | 控制思考模式开关。Batch 场景下即使设为 `true`，结果文件也不返回 `reasoning_content` 字段，仅实时 API 支持完整思考输出 | Prime、PTU、DTU、智能路由、Batch（仅影响计费，不返回字段） |
| `response_format`, `max_tokens` 等 | 智能路由会实时过滤不支持这些参数的备选模型；`max_tokens` 将被自动转换为 `max_completion_tokens` | 智能路由（仅部分参数受支持） |
| `custom_id` | Batch 必填字段，用于结果匹配。单文件内必须唯一，最长 256 字符 | 批量推理 |

## 使用方式

- **Prime 模式**：直接使用专属 model ID 发起标准 `/chat/completions` 请求，接入域名固定为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`。示例：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```

- **吞吐预留 / PTU / DTU**：创建成功后获取专属 `model code`，替换请求中的 `model` 参数即可。PTU 和 DTU 还支持在 API 中配置 `rpm_limit`、`tpm_limit` 等限流参数（仅 DTU/MU 模式支持）[API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。

- **批量推理**：构造 UTF-8 编码 JSONL 文件（每行一个含 `custom_id`、`method`、`url`、`body` 的对象），通过控制台或 API 提交任务。`body` 内需与 `/v1/chat/completions` 接口规范一致，且同一文件内所有请求必须使用相同模型与 `enable_thinking` 设置。

- **智能路由**：使用 `auto-model-xxxxxx` model code 发起 OpenAI 兼容请求，域名必须为 `maas.aliyuncs.com`。响应头 `x-dashscope-resolved-model` 返回实际执行模型，便于监控与调试。

## 限制和注意事项

- **模型兼容性限制**：Prime 模式仅支持明确列出的模型（如 `glm-5.2-fast-preview`），不支持任意模型开启；Batch 不支持语音输出，且 `qwen3.8-max` 在新加坡地域暂不支持纯文本输入；智能路由**不支持图片/视频输入、Embedding/Rerank、Batch、工具调用（`tool_choice`）、`logprobs`、`temperature` 等 10 余项参数**，设置即报错。

- **容量与计费约束**：吞吐预留、PTU、DTU 均为预付费模式，**创建成功即开始计费，与是否调用无关**；DTU/MU 的首月退订按日单价 1.2 倍结算；Batch 结果文件不包含 `reasoning_content`，如需思考过程请改用实时 API。

- **地域与协议限制**：智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，且**仅限 `maas.aliyuncs.com` 域名与 OpenAI 兼容协议**，不支持 `dashscope.aliyuncs.com` 或 DashScope 协议。

- **缓存行为差异**：Prime 模式支持缓存（见计费表中“缓存命中”单价）；PTU 支持前缀缓存并应用阶梯系数；智能路由仅依赖实际路由模型的隐式缓存，不保障命中率，且忽略用户传入的显式缓存参数。

- **故障处理机制**：智能路由内置故障自动切换，但**对 429（限流）、400/403/404/500 等确定性错误不触发切换**，错误直接透出；PTU/DTU 溢出策略可选「自动溢出至按量」或「仅预留容量返回 429」，需按业务中断容忍度谨慎选择。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


