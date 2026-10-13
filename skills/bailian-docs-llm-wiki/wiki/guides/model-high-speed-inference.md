# model high speed inference

百炼平台提供多种面向高性能、高吞吐、低延迟场景的推理加速能力，覆盖实时高速响应（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能资源调度（智能路由）等典型模式。开发者可根据业务对 TPS、首字延迟、成本确定性、缓存命中率及模型效果的综合要求，选择最适配的方案。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景优化，支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，TPS 提升至标准 API 的 1.5~2 倍，[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM 预留）与 PTU/DTU 部署**：提供专属推理容量保障，支持 Qwen、GLM、DeepSeek、Kimi 等主流模型，包括 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-flash` 等；其中 PTU 部署明确支持长输入阶梯系数与前缀缓存折扣，[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **批量推理（Batch）**：适用于非实时场景，支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`text-embedding-v1` 等文本、多模态及向量模型，成本约为实时推理的 50%，[原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：动态匹配请求内容至最优备选模型，当前版本 `model-router-2026-0908` 支持 `qwen3.8-max`、`qwen3.7-flash`、`deepseek-v4-pro-0813`、`glm-5.2` 等 8 款模型，仅限 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用。

> **注意**：文档 2（吞吐预留）与文档 5（专属部署概述）均提及 PTU 模式，但文档 5 明确指出“预置吞吐单元（PTU）的创建与管理现已支持在「吞吐预留」页面进行”，而文档 2 的“性能模式”选项中仍保留“标准模式 / 高速模式（即 PTU 模型部署）”表述，存在术语混用风险。实际操作应以[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面为准，PTU 已统一归入吞吐预留体系。

## 关键参数

| 参数 | 说明 | 适用模式 | 备注 |
|------|------|----------|------|
| `model` | 指定模型标识符，是启用高速能力的核心开关 | 全部 | Prime 模式使用 `glm-5.2-fast-preview`；吞吐预留/PTU/DTU 使用专属 `model code`；智能路由固定为 `auto-model-xxxxxx`；Batch 中需在 JSONL `body` 内指定 |
| `stream` | 控制是否流式返回 | Prime、PTU、DTU、Token 按量 | Prime 模式下流式响应会分别推送 `delta.reasoning_content` 与 `delta.content` 字段 |
| `enable_thinking` | 开启/关闭深度思考模式 | Batch、PTU、DTU、Token 按量 | Batch 场景下即使设为 `true`，结果文件也不包含 `reasoning_content` 字段，详见[原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `input_tpm` / `output_tpm` | 预留或购买的吞吐额度（单位：kTPM） | 吞吐预留、PTU、DTU | DTU 与 PTU 均按输入/输出 TPM 分别计费，但 DTU 要求购买基准 TPM 的整数倍 |
| `response_format` | 指定响应结构（如 JSON Schema） | 智能路由 | 智能路由会自动过滤不支持该参数的备选模型，详见[原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为支持的 Prime 模型 ID（如 `glm-5.2-fast-preview`），并使用专用域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
- **吞吐预留/PTU/DTU**：在控制台创建后获取专属 `model code`，替换 API 请求中的 `model` 参数即可调用；PTU 还支持通过 `ptu_capacity` 字段在 API 中直接部署（见 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)）。
- **批量推理**：构造符合规范的 JSONL 文件（UTF-8 编码，每行一个请求对象，含 `custom_id`, `method`, `url`, `body`），通过控制台或 API 提交任务；`body` 中 `model` 和 `enable_thinking` 必须同级。
- **智能路由**：部署后获得 `auto-model-xxxxxx` code，直接用于 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用；响应头 `x-dashscope-resolved-model` 返回实际执行的模型名。
- **Token 按量部署**：仅支持 LoRA 微调模型，部署时 `plan="lora"`，`capacity` 参数必须填写但无效；调用时 `model` 为部署生成的专属模型 code。

## 限制和注意事项

- **地域与协议限制**：智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且**仅限 [OpenAI 兼容接口](../concepts/openai-compatibility.md)**，不支持 DashScope 协议或 `dashscope.aliyuncs.com` 域名；Batch 推理不支持语音输出（如 `qwen3.5-omni-plus`）。
- **缓存行为差异**：Prime 模式、PTU、DTU 均支持前缀缓存，但智能路由**不支持显式缓存参数**，仅依赖实际路由模型的隐式缓存，命中率无保障；Batch 推理结果文件不返回 `reasoning_content`，即使开启思考模式。
- **模型兼容性约束**：Batch 推理中，同一 JSONL 文件内所有请求必须使用**相同模型及 `enable_thinking` 设置**；智能路由对 `max_tokens` 参数会自动转换为 `max_completion_tokens`，因此仅路由至支持该参数的备选模型。
- **计费与扩容**：吞吐预留、PTU、DTU 均为预付费，提前终止按 1.2 倍系数结算退费；Token 按量部署不支持自助扩缩容，需人工审核申请；Batch 推理单文件上限为 50,000 请求或 500 MB。
- **权限与部署前置**：从 OSS 导入 LoRA 模型需主账号完成服务关联角色授权并为目标 Bucket 添加 `bailian-datahub-access=read` 标签；智能路由的备选模型需 RAM 用户已获对应调用权限，否则无法勾选。

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
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)


