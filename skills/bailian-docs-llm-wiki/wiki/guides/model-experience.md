# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型能力均通过 `/v1/models/{model_id}/invoke` 统一路由接入，支持同步响应与流式返回。该设计已在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中明确规范。

## 支持的模型与功能

当前 `model experience` 覆盖以下模态能力，每类对应独立的模型族与专用输入/输出 schema：

- **文本生成**：支持大语言模型（LLM）的补全、对话、工具调用等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成**：包括图像生成、编辑、理解及视频生成，参见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：涵盖 TTS、ASR、音色克隆与音频理解，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：提供嵌入（embedding）与重排序（rerank）两类低延迟向量模型，见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态模型**：支持跨文本、图像、音频的联合推理（如图文问答、多模态摘要），参考 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：`omni-modal` 模型暂不支持 `stream: true` 流式响应，而其他模态在满足模型能力前提下默认支持；该限制未在 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档中明确说明，以本 Wiki 实际行为为准。

## 关键参数

所有调用共用以下核心参数（位于请求 body）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 平台注册的模型唯一标识，非模型名称（如 `qwen2.5-7b-instruct`） |
| `input` | object | 是 | 模态特定结构体，例如文本模型用 `{"messages": [...]}`，图像模型用 `{"image_url": "..."}` |
| `parameters` | object | 否 | 模型级超参，如 `temperature`, `top_p`, `max_tokens`；各模态支持项不同，详见对应子文档 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流，仅部分模型支持（见各子文档约束） |

`parameters` 中的 `max_tokens` 在文本模型中表示输出长度上限，但在视觉生成模型中含义为“生成图像分辨率等级”（如 `1024` 表示 1024×1024），该语义差异已在 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 文档中明确定义。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **端点**：`POST https://dashscope.aliyuncs.com/api/v1/models/{model_id}/invoke`  
3. **示例（文本）**：
   ```bash
   curl -X POST \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen2.5-7b-instruct",
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"temperature": 0.7}
         }' \
     https://dashscope.aliyuncs.com/api/v1/models/qwen2.5-7b-instruct/invoke
   ```
4. **错误处理**：统一返回 `4xx`（客户端错误）或 `5xx`（服务端错误），`error.code` 字段含平台标准错误码（如 `InvalidParameter`），完整列表见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 编码图像/音频）  
- 流式响应（`stream: true`）仅对文本、部分语音模型稳定支持；视觉与全模态模型启用流式可能导致连接中断或截断，务必在生产环境前验证  
- `model_id` 区分大小写且严格匹配平台注册值；尝试使用别名（如 `qwen-7b`）将返回 `ModelNotFound` 错误  
- 所有模型调用受配额与速率限制管控，具体阈值需在控制台查看，而非 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中声明的“默认不限流”——该描述已过时，实际策略以控制台实时配额为准  
- 输入中的敏感信息（如 PII）不会被平台记录或用于训练，但需开发者自行脱敏；该隐私承诺在 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md) 文档中均有强调

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


