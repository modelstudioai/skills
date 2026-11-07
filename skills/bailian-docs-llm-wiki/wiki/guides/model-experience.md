# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署细节。它支持同步推理、流式响应、批量请求及多模态联合调用，适用于从原型验证到生产部署的全周期场景。所有能力均通过 `/v1/models/{model_id}/invoke` 统一端点接入。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别，每类对应独立的子文档说明：
- 文本生成：支持 LLM 推理、[函数调用](../concepts/function-calling.md)、工具集成，详见 [模型调用](../../raw/model-user-guide/model-experience.md) 中的[文本](../../raw/model-user-guide/model-experience/text-generation-model.md)子页；
- 视觉生成：包括图像生成、编辑、视频生成等，能力边界与输入约束见 [模型调用](../../raw/model-user-guide/model-experience.md) 中的[视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)子页；
- 语音处理：涵盖 TTS、ASR、语音转写与音色克隆，具体支持模型列表与采样率要求参见 [模型调用](../../raw/model-user-guide/model-experience.md) 中的[语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)子页；
- 向量服务：提供嵌入（embedding）与重排序（rerank）两类低延迟向量模型，其 token 计费规则与维度兼容性见 [模型调用](../../raw/model-user-guide/model-experience.md) 中的[向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)子页；
- 全模态（Omni-modal）：实验性支持跨模态联合理解与生成，目前仅限白名单模型，详细协议与 payload 结构请参考 [模型调用](../../raw/model-user-guide/model-experience.md) 中的[全模态](../../raw/model-user-guide/model-experience/omni-modal.md)子页。

> **注意**：全模态接口的 `input_format` 字段在 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档中定义为 `"multi"`，但最新 SDK v2.3.0 已默认使用 `"auto"` 并自动推导格式；实际调用应以 SDK 行为为准，文档尚未同步更新。

## 关键参数

所有模型调用共用以下核心参数（部分参数在特定模型类型中为必填或禁用）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 平台分配的唯一模型标识符，非模型名称；可在控制台「模型管理」页获取 |
| `input` | object | 是 | 模型输入数据，结构因模型类型而异（如文本为 `{"prompt": "..."}`，图像为 `{"image_url": "..."}`）；详见各子文档示例 |
| `parameters` | object | 否 | 模型超参，如 `temperature`, `top_p`, `max_tokens` 等；**不支持跨模型类型通用**，需按 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 等子文档分别配置 |
| `stream` | boolean | 否 | 是否启用流式响应；仅对文本生成与部分语音模型生效，视觉/向量模型强制忽略 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头；
2. **端点**：`POST https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke`；
3. **请求体**：JSON 格式，必须包含 `input` 字段，`parameters` 为可选对象；
4. **响应**：成功时返回 `200 OK`，结构统一为 `{ "output": { ... }, "usage": { ... } }`；错误码遵循 RFC 7807，详见 [模型调用](../../raw/model-user-guide/model-experience.md) 总览页。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 编码图像/音频）；
- 流式响应仅支持 `text/event-stream` MIME type，客户端需正确处理 SSE 协议；
- 向量模型（embedding/rerank）**不支持** `parameters` 字段，传入将被静默忽略；
- 全模态模型暂不支持并发请求（`concurrency_limit=1`），超限请求将返回 `429 Too Many Requests`；
- 所有模型调用均按实际消耗 token 或单位计费，**非按请求次数**；token 计算逻辑依模型类型不同，请严格参照对应子文档（如 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 中的 embedding 长度计费规则）。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


