# model experience

`model experience` 是百炼平台统一的模型调用入口，提供标准化的 API 接口与 SDK 封装，支持多模态模型的一致性体验。开发者可通过单一接口接入文本、视觉、语音、音视频、3D、世界模型等能力，无需为每类模型单独适配协议。所有模型均遵循统一的请求/响应结构和错误码体系，详见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前支持以下核心能力类别（按模态组织）：

- **文本生成**：包括大语言模型（LLM）的对话、补全、摘要、代码生成等  
- **视觉理解**：图文理解、OCR、目标检测、图像分类等  
- **图片生成与编辑**：文生图、图生图、局部重绘、风格迁移  
- **视频生成与编辑**：文生视频、图生视频、视频插帧与剪辑  
- **世界模型**：具备环境感知、推理与动作规划能力的具身智能模型  
- **3D模型生成**：支持 TriPO 等框架的文本/图像到 3D 网格生成  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（TTS2TTS）、音频生成、音乐生成  
- **全模态**：支持跨文本、图像、音频、视频的联合理解与生成  
- **向量与重排序**：文本嵌入（embedding）、多粒度语义向量、检索重排序（rerank）  

> **注意**：语音合成与语音识别的官方文档分别指向阿里云帮助中心外部链接（如 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis)），其参数命名与错误码与百炼内部统一规范存在差异；实际调用时请优先以 [模型体验](../../raw/model-user-guide/model-experience.md) 中定义的 `model_id` 和 `input` 结构为准，避免直接套用帮助中心示例。

## 关键参数

所有模型调用共用以下顶层参数（部分为可选）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | ✅ | 模型唯一标识，如 `qwen-max`, `wanx-v1`, `speech-tts-16k-zh-cn`；完整列表见 [模型体验](../../raw/model-user-guide/model-experience.md) |
| `input` | object | ✅ | 模型输入数据，结构因模态而异（如文本模型为 `{ "prompt": "..." }`，视觉模型为 `{ "image_url": "...", "text": "..." }`） |
| `parameters` | object | ❌ | 模型级超参，如 `temperature`, `top_p`, `max_tokens`（文本）、`seed`, `steps`（图像）等 |
| `enable_streaming` | boolean | ❌ | 是否启用流式响应（仅部分模型支持） |

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/{service_type}/completions` 发送 POST 请求（`service_type` 根据模型类型自动映射，如 `text-generation`、`image-generation`）  
2. **SDK 调用**（推荐）：使用 `dashscope` Python SDK 或 `@alibabacloud/dashscope-nodejs-sdk`，传入 `model_id` 即可自动路由：
   ```python
   from dashscope import Generation
   resp = Generation.call(model='qwen-max', input={'prompt': '你好'})
   ```
3. **控制台调试**：在百炼控制台「模型体验」页选择模型，填写 `input` 和 `parameters` 后实时测试  

详细输入格式与示例请参考各子能力文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 Base64 图片、音频等二进制内容）  
- 流式响应仅支持文本生成、部分语音合成及全模态模型；图像/视频生成不支持流式  
- `model_id` 区分大小写且严格匹配，不可混用旧版 ID（如 `qwen-plus` ≠ `qwen-plus-0919`）  
- 音频/视频类模型对输入时长有限制（如语音合成单次 ≤ 300 字符，视频生成单次 ≤ 5 秒）  
- 所有模型调用均受百炼配额与 QPS 限制，超出将返回 `429 Too Many Requests`  

> **注意**：原始文档中列出的 `tripo-3d-generation-guide.md` 当前已归档，新项目应使用 `tripo-3d-v1` 模型 ID 并参考最新 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) 文档，旧版参数（如 `mesh_format`）已被 `output_format` 替代。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


