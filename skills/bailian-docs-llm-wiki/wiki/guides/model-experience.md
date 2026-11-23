# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型调用均通过 `/v1/models/{model_id}/invoke` 端点发起，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义了基础路由与通用行为。

## 支持的模型与功能

当前 `model experience` 支持以下模态模型的标准化调用：

- **文本生成**：如 Qwen-Max、Qwen-Plus，支持 completion、chat、function calling；详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成与理解**：包括图像生成（如 WanX）、多图推理、视频摘要等；详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音处理**：ASR、TTS、语音转写与合成；详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量与排序**：嵌入（embedding）与重排序（rerank）模型，输入为文本列表，输出为向量或打分；详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态模型**：单次请求可混合文本、图像、音频输入（如 Qwen-VL-Max），需按 schema 组织 `messages`；详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：部分旧版文档（如 `raw/model-user-guide/legacy-api.md`）仍提及 `/v1/completions` 路由，该路径已废弃，请以 [模型调用](../../raw/model-user-guide/model-experience.md) 中定义的 `/v1/models/{model_id}/invoke` 为准。

## 关键参数

所有调用共用以下核心参数（JSON body）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID（如 `qwen-max`），非 display name |
| `input` | object | 是 | 模态相关输入结构，格式依模型类型而异（见各子文档） |
| `parameters` | object | 否 | 模型级超参，如 `temperature`（文本）、`top_p`、`max_tokens`；语音模型使用 `sample_rate`、`language` 等 |
| `stream` | boolean | 否 | `true` 时启用 SSE 流式响应（仅文本/全模态支持） |

`input` 结构严格区分模态：
- 文本类：`{"messages": [...]}` 或 `{"prompt": "..."}`  
- 视觉类：`{"input": {"image_url": "...", "text": "..."}}`  
- 全模态：`{"messages": [{"role": "user", "content": [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": "..."}]}]}`  

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：POST 到 `https://dashscope.aliyuncs.com/api/v1/models/{model_id}/invoke`  
3. **响应**：成功时返回 `200 OK`，结构统一为 `{ "output": { ... }, "usage": { ... } }`；错误时返回标准 `4xx/5xx` 及 `code`/`message` 字段  

示例（文本生成）：
```bash
curl -X POST \
  -H "Authorization: Bearer sk-xxx" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen-max",
        "input": {"messages": [{"role": "user", "content": "你好"}]},
        "parameters": {"temperature": 0.8}
      }' \
  https://dashscope.aliyuncs.com/api/v1/models/qwen-max/invoke
```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 Base64 图像/音频）；超过将返回 `400 Bad Request`  
- 流式响应（`stream=true`）仅对文本生成与全模态模型生效；视觉/语音/向量类模型不支持流式，强制忽略该参数  
- 向量模型（embedding/rerank）**不接受** `parameters.temperature` 等采样参数，传入将被静默丢弃 —— 此行为与 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档一致，但与部分 SDK 示例代码矛盾，请以该文档为准  
- 模型 ID 区分大小写且必须精确匹配控制台「模型服务」页所列 ID；别名（如 `qwen-plus` vs `qwen-plus-0919`）不可混用  

> **注意**：全模态模型的 `messages` 中 `content` 数组内元素顺序影响解析优先级，图像 URL 必须为公网可访问地址（内网或私有 OSS 需预签名），详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 的输入约束章节。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


