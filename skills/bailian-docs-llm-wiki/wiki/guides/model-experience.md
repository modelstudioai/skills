# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型调用均通过 `/v1/models/{model_id}/invoke` 端点发起，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义了基础路由与通用行为。

## 支持的模型与功能

当前 `model experience` 支持以下模态模型的标准化调用：

- **文本生成**：如 Qwen-Max、Qwen-Plus，支持 completion、chat、function calling；详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成与理解**：包括图像生成（如 WanX）、多图推理、视频摘要等；详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音处理**：ASR、TTS、语音转文字、音色克隆等；详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：嵌入（embedding）与重排序（rerank），统一使用 `input` 字段传入文本列表；详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态模型**：单次请求可混合文本、图像、音频输入（需 base64 或 URL），输出结构化 JSON；详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  

> **注意**：部分旧版文档（如早期 `text-generation-model.md` 中描述的 `messages` 字段嵌套格式）与当前 `model experience` v2.1+ 的扁平化 `input` 结构不兼容；请以 [模型调用](../../raw/model-user-guide/model-experience.md) 中定义的最新 request schema 为准。

## 关键参数

所有调用共用以下核心字段（位于 JSON body）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object \| string \| array | 是 | 模态相关输入：文本为 string 或 `{ "messages": [...] }`；图像/音频为 `{"image_url": "...", "text": "..."}` 等结构；向量模型为 string[] |
| `parameters` | object | 否 | 模型级超参，如 `temperature`, `top_p`, `max_tokens`（文本）、`n`（rerank）等，各模态支持项见对应子文档 |
| `enable_streaming` | boolean | 否 | 设为 `true` 启用 SSE 流式响应（仅文本、语音 TTS、部分全模态模型支持） |

`model_id` 需在路径中显式指定（如 `qwen-max`, `wanx-v1`），不可省略。

## 使用方式

1. **构造请求**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/models/qwen-max/invoke" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.7}
         }'
   ```

2. **解析响应**：  
   成功时返回 `200 OK`，结构统一为 `{ "output": { ... }, "usage": { ... } }`；错误时返回标准 `code` 与 `message`（如 `InvalidParameter.InputFormat`）。详细状态码与字段含义见 [模型调用](../../raw/model-user-guide/model-experience.md)。

3. **流式处理**（启用 `enable_streaming=true`）：  
   响应头含 `Content-Type: text/event-stream`，每行以 `data:` 开头，需按 SSE 协议解析；注意客户端需设置足够长的超时（建议 ≥ 300s）。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 **16 MB**（含 base64 图像/音频）；超过将返回 `RequestEntityTooLarge` 错误。
- 全模态模型对多模态输入顺序与数量有严格校验（如最多 4 张图 + 1 段音频），违反时返回 `InvalidInput.MultiModalConstraint`。
- 向量模型（embedding/rerank）**不支持** `parameters.temperature` 等采样参数，若传入将被静默忽略 —— 此行为与 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档中“参数透传”描述存在偏差，实际以运行时行为为准。
- 所有模型调用均受配额与并发数限制，具体阈值取决于用户等级与模型类型，实时配额可通过 `/v1/quotas` 查询。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


