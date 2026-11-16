# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署细节。它支持同步推理、流式响应、批量请求及多模态协同调用，是构建 AI 应用的核心交互入口。详细设计目标见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

`model experience` 覆盖以下五大能力类别，每类对应独立的模型族与专用接口规范：

- **文本生成**：支持大语言模型（LLM）的补全、对话、工具调用等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成**：涵盖图像生成、编辑、理解及视频生成，输入支持 URL、base64 或 multipart 二进制，参见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：包括 TTS、ASR、音色克隆与音频理解，需注意采样率与格式约束，参考 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：提供嵌入（embedding）与重排序（rerank）两类低延迟向量操作，适用于 RAG 场景，见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态**：支持跨模态联合输入（如图文混合 prompt），目前仅限指定模型，具体能力以 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档为准  

> **注意**：`omni-modal` 类别中部分模型要求 `input` 字段必须为 JSON 对象数组（而非字符串），而 `text-generation-model` 仍接受纯字符串；该不一致已在 v2.3.0 后统一为对象数组格式，旧文档未同步更新。

## 关键参数

所有调用共用以下核心参数（HTTP Header 或 JSON Body 中）：

- `model`: 必填，模型 ID（如 `qwen2.5-7b-instruct`），须在控制台已启用且配额充足  
- `input`: 必填，结构化输入，格式依模型类型而异（见上节各子文档）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`），**非所有模型均支持全部参数**，具体支持列表以各子文档为准  
- `stream`: 布尔值，启用流式响应（仅部分文本/语音模型支持）  

`parameters` 的默认值与取值范围因模型而异，例如 `temperature` 在 `text-generation-model` 中默认为 `0.8`，但在 `embedding-rerank-model` 中被忽略——详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 与 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 的参数对照表。

## 使用方式

1. **认证**：通过 `Authorization: Bearer <api_key>` 请求头传入有效 API Key  
2. **端点**：统一使用 `POST /v1/models/{model}/invoke`（同步）或 `/v1/models/{model}/invoke-stream`（流式）  
3. **请求体**：`Content-Type: application/json`，`input` 和 `parameters` 为 JSON 对象  
4. **响应**：成功时返回 `200 OK`，结构含 `output`（结果）、`usage`（token/计费信息）、`request_id`（用于问题追踪）  

示例（文本生成）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/v1/models/qwen2.5-7b-instruct/invoke" \
  -H "Authorization: Bearer sk-xxx" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {"messages": [{"role":"user","content":"你好"}]},
        "parameters": {"temperature": 0.5}
      }'
```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（视觉/视频类模型实际限制更低，见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)）  
- 流式响应仅支持 `text-generation-model` 和 `speech-and-audio` 中的 TTS 模型，其他类型调用 `invoke-stream` 将返回 `400 Bad Request`  
- 全模态调用（`omni-modal`）暂不支持 `stream=true`，且 `input` 中若含图像 URL，必须为 HTTPS 且可公开访问  
- 所有模型调用均受账户级 QPS 与并发数限制，超出将返回 `429 Too Many Requests`；实时配额状态需通过 `/v1/status` 查询  

> **注意**：原始文档 [模型调用](../../raw/model-user-guide/model-experience.md) 中未明确说明视觉类模型对 `input.image.url` 的域名白名单要求，但生产环境实际强制校验（仅允许 `aliyuncs.com`、`qiniu.com` 及已备案 CDN 域名），该限制已在最新 SDK 中默认启用。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


