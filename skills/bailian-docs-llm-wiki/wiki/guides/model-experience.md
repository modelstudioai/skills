# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或 Web 控制台直接调用各类预置模型，无需自行部署或管理底层基础设施。所有模型均经过平台统一封装，提供一致的请求格式、鉴权机制与错误码体系。

## 支持的模型与功能

当前支持以下核心模型类别（按模态与任务划分）：

- **文本生成**：包括通用大语言模型（如 Qwen 系列）、代码生成、结构化输出等  
- **视觉理解**：图文理解、OCR、目标检测、图像分类等 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)  
- **图片生成与编辑**：文生图、图生图、局部重绘、风格迁移等 [原文标题](../../raw/model-user-guide/model-experience/image-model.md)  
- **视频生成与编辑**：短视频生成、关键帧控制、时序编辑等 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- **世界模型**：具备环境建模与推理能力的具身智能模型  
- **3D 模型生成**：支持文本/图像输入生成可导出的 3D 网格（TriPo 模型）  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音频生成、音乐生成（FunMusic）  
- **全模态**：支持跨文本、图像、音频、视频的联合理解与生成 [原文标题](../../raw/model-user-guide/model-experience/omni-modal.md)  
- **向量与重排序**：嵌入（Embedding）模型、语义重排序（Rerank）模型  

> **注意**：语音合成与语音识别的官方文档目前托管在 help.aliyun.com，其参数命名与错误码定义与百炼平台内其他模型存在不一致（例如 `voice` vs `speaker`），建议优先参考 [原文标题](../../raw/model-user-guide/model-experience/audio-generation.md) 中的统一参数映射表。

## 关键参数

所有模型调用共用以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID（如 `qwen-max`, `wanx-v1`, `funmusic-1.0`） |
| `input` | object | 是 | 输入内容，结构依模型类型而异（如 `text`, `image_url`, `audio_url`） |
| `parameters` | object | 否 | 模型特有超参（如 `temperature`, `top_p`, `seed`, `style`） |
| `enable_streaming` | boolean | 否 | 是否启用流式响应（仅部分文本/语音模型支持） |

具体参数约束请查阅各子模型文档，例如视觉理解模型对 `image_url` 的格式与尺寸有明确限制。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>`  
2. **Web 控制台**：进入「模型体验」页，选择模型 → 填写输入 → 点击运行 → 查看结果与 Token 统计  
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.20.0+），自动处理鉴权、重试与流式解析  

示例（Python）：
```python
from dashscope import Generation

resp = Generation.call(
    model='qwen-max',
    input={'messages': [{'role': 'user', 'content': '你好'}]},
    parameters={'temperature': 0.8}
)
```

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型默认 32K tokens，视觉/视频类模型受文件大小（≤100MB）与分辨率（如图像 ≤4096×4096）双重限制  
- 免费额度仅适用于指定模型（如 `qwen-turbo`, `wanx-v1`），高级模型（如 `qwen-max`, `funmusic-1.0`）需开通后付费或使用配额包  
- 所有模型均不支持自定义 LoRA 或微调权重上传；若需定制化能力，请使用「模型训练」模块  
- 视频与 3D 模型生成任务为异步执行，需轮询 `GET /v1/tasks/{task_id}` 获取状态，详见 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


