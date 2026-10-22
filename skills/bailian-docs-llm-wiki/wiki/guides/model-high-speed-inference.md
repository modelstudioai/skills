# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化场景的推理加速能力，涵盖实时高速输出（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型路由四大技术路径。所有方案均基于 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 实现，开发者可按业务负载特征（如流量稳定性、实时性要求、成本敏感度）选择组合使用。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，TPS 提升至标准 API 的 1.5~2 倍 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留与 PTU/DTU 部署**：提供专属推理容量，支持 Qwen、GLM、DeepSeek、Kimi 等主流模型。其中吞吐预留覆盖 `Qwen3.8-Max`、`GLM-5.2`、`DeepSeek-v4-Pro` 等；PTU 部署支持 `qwen3.8-max`、`deepseek-v4-flash` 等长输入优化模型；DTU 支持 `qwen3.7-plus-2026-05-26`、`glm-5.2` 等高性能规格 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **批量推理（Batch）**：适用于非实时场景，支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`text-embedding-v1` 等文本、多模态及向量模型，单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **智能路由**：通过 `auto-model-xxxxxx` 统一入口自动匹配最优模型，当前备选集包含 `qwen3.8-max`、`qwen3.7-flash`、`deepseek-v4-pro-0813`、`glm-5.2` 等，仅限北京与新加坡地域 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  

> **注意**：文档 2（吞吐预留）与文档 5（PTU 部署）对同一模型（如 `glm-5.2`）的 TPM 单价描述存在差异（文档 2 未列具体数值，文档 5 明确华北2为 ¥28.8/10K TPM 输入），实际计费以控制台实时价格为准；文档 5 中“PTU 支持长输入阶梯系数”与文档 2 中“性能模式含标准/高速两档”的表述逻辑一致，但文档 2 将“高速模式”直接等同于 PTU 模型部署，而文档 6 明确指出“PTU 的创建与管理现已支持在「吞吐预留」页面进行”，表明二者已统一为同一能力，建议以[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)为权威入口。

## 关键参数

| 参数 | 说明 | 示例值 | 生效范围 |
|------|------|--------|----------|
| `model` | 指定推理模型标识符，是启用高速能力的核心参数 | `"glm-5.2-fast-preview"`（Prime）、`"your-dedicated-model-code"`（吞吐预留）、`"auto-model-abcd1234"`（智能路由） | 所有方案 |
| `stream` | 控制响应[流式输出](../concepts/streaming-output.md)，Prime 模式下思考内容需通过 `delta.reasoning_content` 单独解析 | `true` | Prime、实时 API |
| `enable_thinking` | 显式开关思考模式，Batch 场景下即使设为 `true`，结果文件也不含 `reasoning_content` 字段 | `true` / `false` | Prime、PTU、Batch（仅影响计费，不返回字段） |
| `input_tpm` / `output_tpm` | 吞吐预留或 PTU 部署中预置的每分钟 [Token](../concepts/token.md) 吞吐量 | `10000`, `1000` | 吞吐预留、PTU |
| `max_completion_tokens` | 智能路由下，该参数用于过滤不支持的备选模型 | `512` | 智能路由 |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为 Prime 专用 ID（如 `glm-5.2-fast-preview`），并使用 `maas.aliyuncs.com` 域名调用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留/PTU/DTU**：创建后获取专属 `model code`，替换 API 请求中的 `model` 参数即可调用；PTU 还支持长输入阶梯系数与缓存折扣，需结合模型特性配置 [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)。  
- **批量推理**：构造 JSONL 文件（每行一个请求，含 `custom_id`、`method`、`url`、`body`），通过控制台或 Batch API 提交任务；媒体 URL 必须公网可访问 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **智能路由**：使用 `auto-model-xxxxxx` 作为 `model`，调用方式与普通模型完全一致；响应头 `x-dashscope-resolved-model` 返回实际执行模型，便于验证路由效果 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  

## 限制和注意事项

- **模型兼容性**：Prime 模式与吞吐预留均要求模型本身支持对应能力，例如 `glm-5.2-fast-preview` 仅在 Prime 模式下可用，而 `glm-5.2` 标准版不可用于 Prime；Batch 不支持语音输出，且 `qwen3.5-omni-plus` 等模型在 Batch 下不返回思考内容。  
- **协议与地域限制**：智能路由仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及 `maas.aliyuncs.com` 域名，不支持 DashScope 协议；所有高速方案目前仅限华北2（北京）与新加坡地域。  
- **缓存行为差异**：Prime 模式与吞吐预留均继承原模型的缓存逻辑，但智能路由因动态选模，无法保障缓存命中率；Batch 推理结果文件不包含 `reasoning_content`，如需思考过程必须使用实时 API 调用。  
- **预热与限流**：吞吐预留实例在请求量快速拉升时需短暂预热，期间可能出现延迟波动，建议实现请求排队或重试机制；超出预留容量时，若溢出策略为“仅使用预留容量”，将直接返回 HTTP 429 错误。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)


