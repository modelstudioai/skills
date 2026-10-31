# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化的推理加速能力，涵盖实时高速响应（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型调度（智能路由）。所有方案均兼容 OpenAI 接口，开发者可通过统一 API 调用，按需选择性能、确定性与成本的最优平衡点。

## 支持的模型/功能

百炼支持以下四类高并发/高性能推理模式，覆盖不同业务场景：

- **Prime 模式**：针对输出速度敏感场景（如 AI 编程助手、Agent 多步推理），提供标准 API 1.5~2 倍 TPS 提升。支持模型包括 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等，能力与原版模型一致，[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM 预留）**：为指定模型锁定专属推理容量（kTPM），确保高峰期不受公共限流影响。支持 Qwen、GLM、DeepSeek、Kimi 等主流模型，含标准模式与高速模式（即 PTU）选项，[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **专属部署（PTU/DTU/MU）**：提供资源隔离的独占部署方案。PTU（预置吞吐）适用于高吞吐稳定场景；DTU（独占吞吐）与 MU（模型单元）支持微调模型与自定义性能指标；Token 按量部署仅限 LoRA 微调模型，不使用不计费。
- **智能路由**：通过 `auto-model-xxxx` 动态匹配备选模型集（如 `qwen3.8-flash`、`deepseek-v4-flash-0731`、`glm-5.2`），按「效果优先」或「成本优先」策略自动路由请求，[原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 2 与文档 5 对“PTU”的归属描述存在差异——文档 2 将 PTU 明确归入吞吐预留体系并指出“预置吞吐单元（PTU）的创建与管理现已支持在「吞吐预留」页面进行”，而文档 5 在“部署模式”小节中仍将 PTU 列为独立部署路径。实际生产应以 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档为准，PTU 是吞吐预留的一种性能模式（见其“性能模式”参数），非独立部署入口。

## 关键参数

| 参数 | 说明 | 使用位置 | 注意事项 |
|------|------|----------|----------|
| `model` | 指定推理模型标识符 | 所有 API 请求体 | Prime 模式需传 `glm-5.2-fast-preview` 等专用 ID；吞吐预留/专属部署需替换为专属 `model code`；智能路由固定为 `auto-model-xxxx` |
| `stream` | 是否启用流式响应 | `/chat/completions` 请求体 | Prime 模式下流式返回 `delta.reasoning_content` 与 `delta.content` 分离字段；Batch 场景不返回 `reasoning_content` 字段 |
| `enable_thinking` | 控制是否开启深度思考模式 | `/chat/completions` 请求体（部分模型支持） | Batch 场景下即使设为 `true`，结果文件也不含 `reasoning_content`；实时 API 可获取完整思考过程，详见 [深度思考](../../raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md) |
| `input_tpm` / `output_tpm` | 吞吐预留或 PTU/DTU 的容量配额（单位：kTPM） | 吞吐预留创建页、API 部署参数 | 容量费用与是否调用无关，创建即开始计费；溢出策略可选「自动溢出至按量」或「仅预留容量返回 429」 |
| `response_format` | 指定响应结构（如 JSON Schema） | 智能路由请求体 | 智能路由会实时过滤不支持该参数的备选模型，若无兼容模型则报错 |

## 使用方式

### 1. Prime 模式
- **接入域名**：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`
- **调用示例**：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```

### 2. 吞吐预留 & 专属部署
- 创建后获取专属 `model code`，替换请求中的 `model` 参数。
- **API 示例（PTU 部署）**：
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{
      "name": "my_qwen_flash",
      "model_name": "qwen-flash-2025-07-28",
      "plan": "ptu",
      "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}
    }'
  ```

### 3. 批量推理（Batch）
- 上传 JSONL 文件（每行一个请求），异步处理，成本降低 50%。
- **JSONL 格式要求**：
  ```json
  {"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-max","messages":[{"role":"user","content":"你好"}]}}
  ```
- 支持模型详见 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)，单文件 ≤50,000 请求且 ≤500 MB。

### 4. 智能路由
- 使用 `auto-model-xxxx` 发起标准 OpenAI 兼容请求。
- **关键约束**：仅支持 `maas.aliyuncs.com` 域名、文本 Chat Completions、北京/新加坡地域；不支持 `stop`、`temperature`、`top_p` 等采样参数。

## 限制和注意事项

- **计费一致性**：所有模式均按输入/输出 token 计费（视频模型按秒），但吞吐预留/PTU/DTU 为预付费容量包，容量费用与调用量无关，未使用亦全额计费；Batch 为异步按量，成本减半。
- **缓存行为差异**：
  - Prime 模式与吞吐预留支持上下文缓存（`cached_tokens` 统计），但智能路由**不保障缓存命中率**，因请求可能被路由至不同模型；
  - Batch 结果文件不包含 `reasoning_content`，即使启用思考模式。
- **模型兼容性限制**：
  - Token 按量部署**仅支持 LoRA 微调模型**，且必须通过 API 部署（`plan=lora`），不支持全参微调模型；
  - 智能路由**不支持图片/视频输入、Embedding/Rerank、Batch、工具调用等非 Chat Completions 接口**；
  - DTU/PTU 部署对长输入（>32K）应用阶梯系数与缓存折扣，具体规则见 [PTU 长输入与前缀缓存](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)。
- **故障处理**：智能路由内置故障自动切换（仅对 5xx/网络异常生效），429 或 4xx 错误直接透出，不重试；切换后仅计最终成功模型费用。

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


