# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的身份认证、配额管理和计费机制。

## 支持的模型与功能

当前支持以下模型类别及对应能力：

- 文本生成（如 Qwen 系列）  
- 视觉理解（图文理解、OCR、目标检测等）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（短视频生成、时序编辑）  
- 世界模型（具身智能、环境建模与推理）  
- 3D 模型生成（TriPo 等结构化输出）  
- 语音合成（TTS）、音频生成、音乐生成  
- 语音识别（ASR）、语音转语音（S2S）  
- 全模态模型（跨文本/图像/音频/视频联合理解与生成）  
- 向量嵌入与重排序（embedding/rerank）  

详细能力说明请参见 [模型体验](../../raw/model-user-guide/model-experience.md)。各子类模型的具体输入输出格式、示例及最佳实践，见其对应文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 关键参数

调用模型体验接口时，通用关键参数包括：

- `model`: 模型 ID（如 `qwen-max`, `qwen-vl-plus`, `wanx-video`），必须与所选模型类型匹配；  
- `input`: 输入内容，结构依模型而异（如 `{"prompt": "..."}` 或 `{"image_url": "...", "text": "..."}`）；  
- `parameters`: 可选配置，常见字段有 `temperature`, `top_p`, `max_tokens`, `seed`（部分模型支持）；  
- `stream`: 布尔值，控制是否启用流式响应（仅部分文本/语音模型支持）；  
- `enable_search`: 仅适用于支持联网搜索的模型（如 `qwen-max` 的增强版），默认 `false`。

> **注意**：`parameters.seed` 在视觉生成类模型（如图片/视频）中为必填项以保证结果可复现，但在文本生成中为可选；该差异在 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md) 中明确要求，而 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 文档未作强制说明，实际调用时建议显式设置以提升一致性。

## 使用方式

1. **控制台体验**：登录百炼控制台 → 进入「模型体验」页 → 选择模型 → 填写输入并提交 → 查看响应与 Token 统计；  
2. **API 调用**：使用 `POST /api/v1/services/aigc/{service}/models/{model}/invoke` 接口，需携带 `Authorization: Bearer <access_token>`；  
3. **SDK 集成**：推荐使用 `alibabacloud_bailian20231229` Python SDK，调用 `Client.invoke_model()` 方法，传入 `service`, `model`, `input`, `parameters` 字典；  
4. **批量测试**：支持上传 JSONL 文件进行批量请求，结果按行返回（详见 [模型体验](../../raw/model-user-guide/model-experience.md) 中的「批量调用」章节）。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型上限为 32768 tokens（Qwen 系列），视觉类模型图像分辨率不超过 1536×1536 像素；  
- 视频生成任务最长支持 8 秒输出，且不支持自定义帧率；  
- 所有语音/音频类模型暂不支持跨区域调用（即调用地域须与模型部署地域一致）；  
- 全模态模型（`omni-*`）目前仅开放白名单试用，需单独申请权限；  
- 向量模型（`embedding`）输出维度固定为 1024，不支持自定义；重排序模型仅接受最多 100 个候选文本，超出将被截断。

> **注意**：[语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 和 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 的官方帮助文档已迁至阿里云 Model Studio 独立站点，其参数命名（如 `voice` vs `speaker`）与百炼平台模型体验 API 不完全兼容，建议优先参考 [模型体验](../../raw/model-user-guide/model-experience.md) 中的映射说明。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


