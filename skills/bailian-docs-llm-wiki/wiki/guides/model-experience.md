# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义/混合）的差异。所有模型能力均通过 `model experience` 接入，支持同步推理、流式响应、批量处理及异步任务等通用交互模式。其设计目标是降低多模态模型集成复杂度，提升跨模型迁移与灰度验证效率。

## 支持的模型与功能

`model experience` 覆盖以下核心模态能力，每类均对应独立的子文档说明：
- 文本生成：包括大语言模型（LLM）的对话、补全、结构化输出等，详见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)；
- 视觉生成：支持图像生成、编辑、视频生成及理解任务，详见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)；
- 语音与音频：涵盖 TTS、ASR、音色克隆及音频理解，详见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)；
- 向量服务：提供嵌入（embedding）与重排序（rerank）两类向量模型，适用于检索增强场景；
- 全模态（Omni-modal）：支持跨文本、图像、语音的联合理解与生成，需显式指定 `input_type` 和 `output_type`。

> **注意**：原始文档中列出的 `model-experience/omni-modal.md` 子路径尚未在 `raw/` 目录下实际存在，当前仅支持通过 `model_type=omni` + 显式 multi-input 格式调用，具体格式请参考 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md) 中的“全模态调用示例”章节（截至 2024-06-15 版本）。

## 关键参数

所有请求共用以下顶层参数（非模态特有参数）：
- `model_id`: 必填，模型唯一标识（如 `qwen-max`, `wanx-v1`），可在控制台模型市场或 `/v1/models` 接口获取；
- `parameters`: 可选对象，包含 `temperature`, `top_p`, `max_tokens` 等通用采样参数；
- `stream`: 布尔值，启用流式响应（仅部分模型支持，需查阅对应子文档）；
- `request_id`: 可选，用于链路追踪与问题定位；
- `extra`: 任意键值对，用于透传业务上下文（不参与模型计算）。

模态特有参数（如 `image_url`, `audio_format`, `input_documents`）均置于 `input` 字段内，结构由模型类型决定。

## 使用方式

1. **HTTP 调用**：向 `POST /v1/model/experience` 发送 JSON 请求，`Content-Type: application/json`；
2. **SDK 调用**：使用 `bailian-sdk` 的 `ModelExperienceClient.invoke()` 方法（Python/Java/Go 均支持）；
3. **批量处理**：通过 `/v1/model/experience/batch` 提交任务列表，返回 `job_id`，再轮询 `/v1/jobs/{job_id}` 获取结果；
4. **异步任务**：设置 `async=true`，响应中返回 `task_id`，后续通过 `/v1/tasks/{task_id}` 查询状态。

所有调用均需携带 `Authorization: Bearer <api_key>`，且 `model_id` 必须已授权给当前 AccessKey。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 编码图像/音频）；
- 流式响应仅支持文本与部分语音模型，视觉生成类暂不支持流式（参见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)）；
- 全模态模型不支持 `stream=true`，且 `max_tokens` 限制为 2048；
- 若请求中 `model_id` 未在当前项目中启用，将返回 `403 Forbidden`，而非 `404 Not Found`；
- 所有模型调用默认启用输入内容安全过滤（可选关闭，但需单独申请白名单）。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


