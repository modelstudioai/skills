# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的标准化接入与管理。通过该能力，开发者可基于统一 API 接口调用不同模态的模型服务，无需为每类模型单独适配协议或鉴权逻辑。所有模型均遵循平台统一的请求/响应格式、错误码体系与计费规则。

## 支持的模型与功能

当前支持以下 12 类模型能力，覆盖文本、视觉、语音、音视频、3D、世界建模及向量处理等场景：

- 文本生成（[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)）  
- 视觉理解（[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)）  
- 图片生成与编辑（[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)）  
- 视频生成与编辑（[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)）  
- 世界模型（[世界模型](../../raw/model-user-guide/model-experience/world-model.md)）  
- 3D 模型生成（[3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）  
- 语音合成（[语音合成](../../raw/model-user-guide/model-experience/speech-synthesis.md)）  
- 音频生成（[音频生成](../../raw/model-user-guide/model-experience/audio-generation.md)）  
- 语音识别（[语音识别](../../raw/model-user-guide/model-experience/speech-recognition.md)）  
- 语音转语音（[语音转语音](../../raw/model-user-guide/model-experience/speech-to-speech.md)）  
- 全模态（[全模态](../../raw/model-user-guide/model-experience/omni-modal.md)）  
- 向量与重排序（[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)）

> **注意**：`world-model` 当前仅限白名单用户调用，其输入 schema 与通用文本模型不兼容，需显式指定 `model_type: "world"`；相关细节请以 [世界模型](../../raw/model-user-guide/model-experience/world-model.md) 文档为准，而非通用模型参数说明。

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展字段）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`, `qwen-vl-plus`, `wanx-video-1.0` 等，具体列表见各子文档 |
| `input` | object | 是 | 模型输入数据，结构因模态而异（如 `text`、`image_url`、`audio_url`、`messages` 等） |
| `parameters` | object | 否 | 模型推理参数，如 `temperature`, `top_p`, `max_output_tokens`；**非所有模型均支持全部参数**，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和对应模态文档 |

## 使用方式

1. 调用 `POST /v1/models/{model}/invoke`（推荐）或通用入口 `POST /v1/model-experience/invoke`  
2. 在请求头中携带 `Authorization: Bearer <api_key>`  
3. 请求体为 JSON，包含 `model`、`input` 和可选 `parameters` 字段  
4. 响应统一返回 `output` 字段（结构依模型而定）和 `request_id`

示例（文本生成）：
```json
{
  "model": "qwen-max",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```

## 限制和注意事项

- 单次请求最大 `input` 大小：文本 ≤ 1MB，图像 ≤ 20MB，视频 ≤ 500MB，音频 ≤ 100MB  
- 所有模型均受账户配额与速率限制约束，超限返回 `429 Too Many Requests`  
- `embedding-rerank-model` 不支持流式响应，且 `input` 中 `texts` 字段最多 64 项（[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)）  
- 视频/3D/世界模型等高资源消耗类型默认关闭自动重试，客户端需自行实现幂等与重试逻辑  
- **重要**：`speech-to-speech` 模型暂不支持 `stream=true`，启用将导致 400 错误 —— 此限制未在 [语音转语音](../../raw/model-user-guide/model-experience/speech-to-speech.md) 文档中明确说明，但已在线上环境强制执行。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


