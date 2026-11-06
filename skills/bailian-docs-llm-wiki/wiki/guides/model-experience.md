# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型调用均通过 `/v1/models/{model_id}/invoke` 端点发起，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义为平台核心交互范式。

## 支持的模型与功能

当前 `model experience` 支持以下模态模型的标准化调用：

- **文本生成模型**：如 Qwen-Max、Qwen-Plus，支持 prompt 补全、[函数调用](../concepts/function-calling.md)（tool calling）、多轮对话上下文管理  
- **视觉模型**：包括图像生成（如 Wanx）、图像理解（如 Qwen-VL）、视频理解（如 Qwen2-VL），详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音模型**：涵盖语音转文字（ASR）、文字转语音（TTS）、语音识别与合成联合任务  
- **向量模型**：支持 embedding 生成与重排序（rerank），适用于检索增强场景  
- **全模态模型**：如 Qwen2.5-Omni，可统一处理文本、图像、音频输入并生成跨模态响应，其能力边界见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：语音模型的 TTS 接口默认不启用流式响应，而文本生成模型的 `stream: true` 可稳定生效；此行为差异未在 [模型调用](../../raw/model-user-guide/model-experience.md) 中明确说明，实际以各子文档为准。

## 关键参数

所有调用共用以下顶层参数（位于 JSON 请求体）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object | 是 | 模态特定输入结构，例如文本模型为 `{ "messages": [...] }`，视觉模型为 `{ "image_url": "...", "prompt": "..." }` |
| `parameters` | object | 否 | 模型推理参数，如 `temperature`、`top_p`、`max_tokens`；部分参数（如 `seed`）仅对特定模型生效 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流（仅文本、部分全模态模型完全支持） |

参数兼容性需参考具体模型文档，例如 embedding 模型不接受 `temperature`，且 `input` 结构为 `{ "input": ["..."] }` ——该约定在 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档中明确定义。

## 使用方式

1. **构造请求**：HTTP POST 到 `https://dashscope.aliyuncs.com/api/v1/models/{model_id}/invoke`  
2. **设置 Header**：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
3. **发送 Body**：按目标模型类型组织 `input` 字段（参见对应子文档结构）  
4. **处理响应**：成功时返回 `200`，`output` 字段含结果；流式响应需按 SSE 协议解析 `data:` 行  

示例（文本生成）：
```json
{
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7},
  "stream": false
}
```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 Base64 编码图像/音频）；超限将返回 `400 Bad Request`  
- 全模态模型对多图/长视频输入有额外 token 限制，具体阈值见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  
- `model_id` 必须为平台注册的合法 ID（如 `qwen-max`），不支持直接传入自定义模型路径  
- [异步任务](../concepts/asynchronous-task.md)（如长视频理解）暂未纳入 `model experience` 统一接口，需调用独立异步 API —— 此缺口在 [模型调用](../../raw/model-user-guide/model-experience.md) 中未作提示，开发者需主动查阅各模态子文档

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


