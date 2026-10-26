# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化场景的推理加速能力，涵盖实时高速输出（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型路由等方案。所有方案均兼容 OpenAI 接口，开发者可根据业务对 TPS、延迟、确定性、成本敏感度及是否需实时响应等维度进行选型。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，TPS 提升至标准 API 的 1.5~2 倍，适用于 AI 编程助手、Agent 多步推理与实时对话。支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，能力与原版模型一致 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPM 预留）**：为指定模型锁定专属推理容量，保障高峰期服务稳定性。支持 Qwen3.x、GLM-5.x、DeepSeek-v4.x、Kimi-K2.6 等主流文本模型，以及部分视频理解模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **批量推理（Batch）**：适用于无需实时响应的大规模[异步任务](../concepts/asynchronous-task.md)（如模型评测、数据标注），成本约为实时推理的 50%。支持千问全系列（Max/Plus/Flash/Long）、多模态模型（Qwen-VL、Qwen-OMNI）及向量模型（text-embedding-vx） [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **专属部署**：含 PTU（预置吞吐）、DTU（独占吞吐）和 MU（模型单元）三种模式，提供物理/逻辑资源隔离与性能定制能力；[Token](../concepts/token.md) 按量部署仅支持 LoRA 微调模型，适用于效果验证场景 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。  
- **智能路由**：基于请求内容动态匹配最优备选模型（如 `qwen3.8-max`、`deepseek-v4-flash-0731`），支持「效果优先」与「成本优先」策略，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 7（PTU 部署）中列出的 `qwen3.7-flash-2026-07-15` 标注“联系商务经理开通”，而文档 2（吞吐预留）明确将其列为华北2（北京）支持模型，二者存在矛盾。实际可用性请以控制台实时展示为准。

## 关键参数

| 方案 | 关键参数 | 说明 |
|------|----------|------|
| **Prime 模式** | `model` | 必须使用专用 model ID（如 `glm-5.2-fast-preview`），无额外参数；接入域名需为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| **吞吐预留 / PTU / DTU** | `model`（专属 model code） | 创建后生成唯一专属 model code，API 请求中必须替换原 model ID；PTU 还需配置 `input_tpm`/`output_tpm`，DTU 需按基准 TPM 整数倍购买 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| **批量推理** | `custom_id`, `enable_thinking`, `body` | JSONL 文件中每行需含唯一 `custom_id`；`enable_thinking` 为 `body` 同级字段，不可置于 `extra_body`；结果文件不返回 `reasoning_content` 字段 |
| **智能路由** | `model`（`auto-model-xxxxxx`）, `response_format`, `max_tokens` | `model` 固定为 `auto-model-` 前缀；`max_tokens` 会自动转为 `max_completion_tokens`，仅路由至支持该参数的备选模型 |

## 使用方式

- **Prime 模式**：直接调用兼容模式 API，`model` 参数设为 Prime 专用 ID 即可，无需修改请求体或 Header。流式响应中思考内容与回答内容分别通过 `delta.reasoning_content` 和 `delta.content` 返回。  
- **吞吐预留 / PTU / DTU**：在控制台创建实例后获取专属 `model code`，替换 API 请求中的 `model` 参数；PTU/DTU 部署还支持通过 API 创建（`plan=ptu` 或 `plan=mu`），详见 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。  
- **批量推理**：准备 UTF-8 编码 JSONL 文件（单文件 ≤50,000 请求且 ≤500 MB），通过控制台或 API 提交任务；媒体 URL 必须为公网可访问地址，不支持本地路径或内网地址。  
- **智能路由**：将 `model` 替换为 `auto-model-xxxxxxxx`，其余调用方式与普通模型完全一致；响应头 `x-dashscope-resolved-model` 返回实际执行模型，响应体 `model` 字段亦为真实模型名。  

> **注意**：文档 10（API 部署指南）中示例使用 `dashscope.Generation.call` 调用已部署模型，但文档 11（我的模型）明确指出“调优后的模型部署成功后，只能使用其所在业务空间的 API-KEY 调用，且目前仅支持通过 DashScope 方式调用，不支持通过 OpenAI 兼容方式调用”。此限制未在 API 部署指南中体现，开发者需严格遵循该约束。

## 限制和注意事项

- **模型兼容性**：Prime 模式与吞吐预留均要求模型在对应地域开放支持；批量推理中 `qwen3.8-max` 在新加坡地域暂不支持纯文本输入；智能路由仅支持文本 Chat Completions，不支持图片/视频输入、Embedding、Rerank 或 Batch。  
- **缓存行为**：Prime 模式与吞吐预留支持上下文缓存，但批量推理结果文件不包含 `reasoning_content`；智能路由不支持显式缓存参数，仅依赖实际路由模型的隐式缓存机制。  
- **计费与扩容**：吞吐预留/PTU/DTU 均支持溢出策略（自动溢出至按量计费或返回 429），但 [Token](../concepts/token.md) 按量部署不支持自助扩缩容，需人工审核申请；批量推理任务提交后不可修改，超限需拆分任务。  
- **权限与地域**：智能路由仅支持 `maas.aliyuncs.com` 域名（`cn-beijing`/`ap-southeast-1`），不支持 `dashscope.aliyuncs.com`；模型导入需完成 OSS 服务关联角色授权并为目标 Bucket 添加 `bailian-datahub-access=read` 标签。  
- **性能预热**：吞吐预留实例在请求量快速拉升时需短暂预热，期间可能出现延迟波动，建议实现请求排队或重试机制。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)


