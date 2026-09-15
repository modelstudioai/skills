# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准化接口调用文本、视觉、音视频、3D、语音及全模态等各类模型服务，无需单独配置底层基础设施。所有模型均通过 `model_id` 标识，并遵循一致的请求/响应结构。

## 支持的模型与功能

当前支持以下模型类型及对应能力：

- 文本生成：支持通用对话、指令遵循、代码生成等任务，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- 视觉理解：包括图像分类、OCR、图文理解等，详见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- 图片生成与编辑：支持文生图、图生图、局部重绘等，详见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- 视频生成与编辑：支持文生视频、视频扩时、关键帧控制等，详见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- 3D模型生成：集成 Tripo 模型，支持文生3D、图生3D，详见 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- 向量与重排序：提供嵌入向量生成（embedding）和检索重排序（rerank）能力，详见 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- 全模态：支持跨模态联合理解与生成（如图文音视频混合输入），详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  

> **注意**：语音合成、语音识别、语音转语音三类能力当前托管于 Model Studio 官方帮助中心，其 API 签名、鉴权方式与百炼主平台不一致，暂不支持通过 `/v1/models/{model_id}/invoke` 统一路径调用；请直接参考 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 等外部文档。音乐生成文档 [fun-music.md](../../raw/model-user-guide/model-experience/fun-music.md) 中描述的 `music_generate` 接口已下线，实际应使用 `model_id: qwen2-audio-music` 调用新版音频模型。

## 关键参数

调用模型体验统一接口（`POST /v1/models/{model_id}/invoke`）时，必需参数包括：

- `model_id`：模型唯一标识（如 `qwen2.5-plus`、`qwen-vl-plus`、`wanx-video-1.0`），必须与 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md) 等子文档中声明的 ID 严格一致  
- `input`：模型输入数据，结构因模型类型而异（如文本模型为 `{"prompt": "..."}`，视觉模型为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`（可选）：控制生成行为，常见字段包括 `temperature`、`top_p`、`max_tokens`（文本类）、`seed`（生成类）、`quality`（图像/视频类）等，具体以各子模型文档为准  

## 使用方式

1. 在控制台「模型体验」页选择目标模型，获取 `model_id`  
2. 构造 HTTP POST 请求，Header 中携带 `Authorization: Bearer <api_key>`  
3. Body 使用 JSON 格式，按模型类型填充 `input` 和 `parameters`  
4. 解析返回的 `output` 字段（结构化 JSON 或 base64 编码二进制内容）  

示例（文本生成）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/models/qwen2.5-plus/invoke \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {"prompt": "写一首关于春天的五言绝句"},
        "parameters": {"temperature": 0.7}
      }'
```

## 限制和注意事项

- 单次请求最大 `input` 大小为 16MB（视频/3D 类模型建议 ≤8MB）  
- 视频与3D生成任务默认异步执行，需轮询 `task_id` 获取结果，同步调用将返回 `400 UnsupportedOperation`  
- 所有模型均受配额与并发数限制，超出时返回 `429 Too Many Requests`；配额详情见控制台「用量管理」  
- 模型输出内容受阿里云内容安全策略约束，违规输入将被拦截并返回 `400 ContentBlocked`，具体规则参见 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md) 中的安全说明章节  
- 音频类模型（语音合成、音乐生成）暂不支持流式响应（`stream=true`），设置后将被忽略 —— 此行为与 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md) 中旧版描述矛盾，以当前 API 实际行为为准

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


