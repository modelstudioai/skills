# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署细节。它支持同步推理、流式响应、批量请求及上下文管理，适用于从原型验证到生产部署的全周期场景。所有能力均通过 `/v1/models/{model_id}/invoke` 统一端点暴露。

## 支持的模型与功能

当前 `model experience` 覆盖以下模态能力：
- **文本生成**：支持大语言模型（LLM）的补全、对话、[函数调用](../concepts/function-calling.md)等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)；
- **视觉生成**：包括图像生成、编辑、理解及视频生成，详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)；
- **语音处理**：涵盖语音转文字（ASR）、文字转语音（TTS）及音频理解，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)；
- **向量服务**：提供嵌入（embedding）与重排序（rerank）两类向量模型，详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)；
- **全模态模型**：支持多模态输入（如图文混合）与跨模态推理，详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)。

> **注意**：部分旧版文档中提及的 `multimodal` 模型标识已统一归入 `omni-modal` 分类，[全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档为最新权威说明，此前分散在 `multimodal-vision` 等路径下的内容已过时。

## 关键参数

所有调用共用以下核心参数（JSON body）：
- `model_id`：必需，平台注册的模型唯一标识（如 `qwen2.5-7b-chat`）；
- `input`：必需，结构化输入，格式依模型类型而异（如文本模型为 `{"messages": [...]}`，图像模型为 `{"image_url": "..."}`）；
- `parameters`：可选，控制生成行为，通用字段包括 `temperature`、`top_p`、`max_tokens`；模态特有字段（如 `seed` 用于图像生成）见对应子文档；
- `stream`：布尔值，启用流式响应（仅部分模型支持，需查阅具体模型文档确认）。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头；
2. **端点**：`POST https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke`；
3. **示例（文本）**：
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen2.5-7b-chat",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.7}
         }' \
     https://dashscope.aliyuncs.com/v1/models/qwen2.5-7b-chat/invoke
   ```
   其他模态的 `input` 构造方式请严格参照 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 等原始文档定义。

## 限制和注意事项

- 单次请求最大 `input` 大小为 16 MB（图像/视频需压缩后上传）；
- 流式响应（`stream=true`）仅对文本与部分语音模型生效，[语音](../../raw/model-user-guide/model-experience/speech-and-audio.md) 文档明确列出支持 `stream` 的 ASR/TTS 模型；
- 向量模型（embedding/rerank）不支持 `temperature`、`top_p` 等采样参数，传入将被忽略；
- 模型 ID 区分大小写且严格匹配注册名，错误 ID 将返回 `404 Model Not Found`，建议通过 `/v1/models` 列表接口动态获取可用 ID。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


