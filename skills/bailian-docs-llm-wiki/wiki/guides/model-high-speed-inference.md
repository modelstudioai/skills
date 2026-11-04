# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与确定性性能的推理加速能力，核心包括吞吐预留（TPM）、PTU/DTU 专属部署、Prime 模式及批量推理。这些方案在容量保障强度、计费粒度、资源隔离级别和接入复杂度上形成梯度覆盖，开发者可根据流量可预测性、SLA 要求、成本敏感度及模型定制程度选择最适配路径。

## 支持的模型/功能

百炼支持以下四类高并发/高性能推理模式，对应不同模型覆盖范围：

- **吞吐预留（TPM）与 PTU 部署**：面向标准预置模型，提供专属 TPM 容量保障。支持 Qwen3.8-Max、Qwen3.7-Flash-2026-07-15、GLM-5.3、DeepSeek-v4-Pro、Kimi-K2.6 等主流模型；其中 [kimi-k3.1-pro](raw/model-user-guide/support/model-studio-model-list/model-list-text-generation/kimi-k3-1-pro.md) 仅支持按天预付费的标准模式 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **DTU（独占吞吐）与 MU（模型单元）部署**：支持基础模型与 LoRA 微调模型，提供物理级 GPU 隔离。DTU 已成为新发布大模型（如 qwen3.5-397b-a17b、glm-5.2）的首选部署方式，MU 则用于历史模型兼容 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **Prime 模式**：为输出速度敏感场景（如 AI 编程助手、Agent 多步推理）设计，TPS 提升至标准 API 的 1.5~2 倍，当前仅支持 GLM 系列（`glm-5.3-prime`、`glm-5.2-fast-preview`）及 Wan3.0 视频生成模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **批量推理（Batch）**：适用于异步、非实时场景（如模型评测、数据标注），成本约为实时推理的 50%。支持 Qwen3.8-Max、Qwen3.7-Plus、Qwen-VL-Plus、text-embedding-v3 等文本、多模态及向量模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

> **注意**：文档中 `qwen3.7-flash-2026-07-15` 在吞吐预留文档中标注“联系商务经理开通”，但在 PTU 文档价格表中直接列出，存在开通条件不一致问题，实际使用前请以控制台可选列表为准。

## 关键参数

各模式的核心配置参数如下：

| 模式 | 关键参数 | 说明 |
|------|----------|------|
| 吞吐预留 / PTU | `input_tpm`, `output_tpm`, `performance_mode`（标准/高速） | 输入/输出吞吐量单位为 kTPM（1,000 tokens/min）；`performance_mode=高速` 即 PTU，TPS 提升 1.5~2 倍 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| DTU | `input_tpm`, `output_tpm`（基准倍数） | 购买需为基准 TPM 的整数倍，各模型有固定基准值（如 `qwen3.7-plus-2026-05-26` 基准输入为 1,372,000 TPM） [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md) |
| MU | `deploy_spec`（如 `MU1`）、`capacity`、`rpm_limit`, `tpm_limit` | `capacity` 表示副本数；`rpm_limit`/`tpm_limit` 为可选限流参数，仅 MU 模式支持自定义 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md) |
| Prime | 无显式参数，仅需指定专用 model code（如 `glm-5.2-fast-preview`） | 接入域名必须为 `maas.aliyuncs.com`，不可用 `dashscope.aliyuncs.com` [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |
| 批量推理 | `enable_thinking`（顶层参数）、`custom_id` | `enable_thinking` 必须置于 JSONL 每行 `body` 的同级，不可嵌套于 `extra_body`；结果文件不返回 `reasoning_content` 字段 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |

## 使用方式

所有高并发模式均通过替换 API 请求中的 `model` 参数实现接入，无需修改请求结构：

- **吞吐预留 / PTU / DTU / MU**：部署成功后获取专属 `model code`（如 `tpu-qwen3.8-max-abc123`），在 `chat.completions.create(model="...")` 中直接使用。代码示例如下：
  ```python
  response = client.chat.completions.create(
      model="tpu-qwen3.8-max-abc123",  # 替换为专属 model code
      messages=[{"role": "user", "content": "你好"}]
  )
  ```
- **Prime 模式**：直接使用 Prime 专用 model code（如 `glm-5.2-fast-preview`），并确保 base_url 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
- **批量推理**：通过 `/v1/batches` 接口提交 JSONL 文件，**不使用常规 `/v1/chat/completions` 端点**。JSONL 每行必须含 `custom_id`、`method="POST"`、`url="/v1/chat/completions"` 及符合 OpenAI 格式的 `body` [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：使用 `auto-model-xxxxxx` 格式 model code，仅支持 `maas.aliyuncs.com` 域名与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，响应头 `x-dashscope-resolved-model` 返回实际执行模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：吞吐预留实例创建后即开始计费，与是否调用无关；且短时间内请求量快速拉升时，系统需短暂预热，预热期间可能出现延迟波动，建议客户端实现请求排队或重试机制 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **计费刚性**：吞吐预留、PTU、DTU、MU 均为预付费模式，费用按购买量一次性支付，即使零调用也不减免；其中 DTU/MU 提前退订按 1.2 倍日单价结算退费 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
- **模型兼容性**：Token 按量部署**仅支持 LoRA 微调模型**，不支持全参微调或原生预置模型；批量推理中 `qwen3.5-omni-plus` 不支持语音输出，且思考模式结果字段被裁剪 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **协议与域名限制**：智能路由与 Prime 模式**均强制要求使用 `maas.aliyuncs.com` 域名**，不可使用 `dashscope.aliyuncs.com`；且智能路由仅支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，不支持 DashScope 协议、流式响应中的部分参数（如 `top_p`, `temperature`）及非文本输入 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **缓存行为差异**：吞吐预留中 GLM-5.2 的 `thinking_budget` 参数在调用时不生效；而 Prime 模式下 `glm-5.2-fast-preview` 默认返回 `reasoning_content` 字段，流式响应需分别处理 `delta.reasoning_content` 和 `delta.content` [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)


