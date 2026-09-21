# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或 Web 控制台直接调用各类预置模型，无需自行部署或管理底层推理服务。所有模型均经过平台统一封装，提供一致的请求格式、鉴权机制与错误码体系。

## 支持的模型与功能

当前支持以下模型类别及对应能力：

- **文本生成**：通用对话、长文本续写、指令遵循等，详见 [模型体验](../../raw/model-user-guide/model-experience.md)  
- **视觉理解**：图像分类、OCR、图文问答等多任务理解能力  
- **图片生成与编辑**：文生图、图生图、局部重绘等，相关参数与示例见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- **视频生成与编辑**：支持短视频生成、帧插值与基础剪辑  
- **世界模型**：具备环境建模与动态推理能力，适用于仿真与决策场景  
- **3D 模型生成**：通过文本或草图生成可导出的 3D 网格，参考 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- **语音与音频处理**：涵盖语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音乐生成及通用音频生成  
- **全模态**：支持文本、图像、音频、视频等多模态输入联合推理  
- **向量与重排序**：提供嵌入（embedding）与检索重排序（rerank）两类基础模型服务  

> **注意**：语音合成与语音识别的官方文档分别托管在 help.aliyun.com，其 API 接口路径、认证方式与百炼统一 SDK 存在差异；实际集成时请以 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的百炼封装接口为准，避免直接调用 help.aliyun.com 的旧版 endpoint。

## 关键参数

所有模型调用均需指定 `model`（模型标识符）与 `input`（输入数据结构）。通用关键参数包括：

- `model`: 必填，如 `qwen-max`, `wanx-v1`, `speech-tts-16k-zh-cn` 等，具体取值见各子文档  
- `input`: 结构依模型类型而异（如文本模型为 `{"prompt": "..."}`，视觉模型为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`），部分模型支持专属参数（如图像模型的 `size`, `style`）  
- `stream`: 布尔值，启用流式响应（仅部分模型支持）

参数细节与默认值请查阅对应模型的子文档，例如 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 中明确列出了 `detail` 和 `quality` 参数的合法范围。

## 使用方式

1. **API 调用**：使用百炼 SDK（Python/Java/Go）或直接发送 HTTP POST 请求至 `/v1/models/{model}/invoke`  
2. **Web 控制台**：登录百炼控制台 →「模型体验」页 → 选择模型 → 输入内容 → 实时调试  
3. **批量测试**：通过 `/v1/batch/invoke` 提交 JSONL 格式任务列表（需开通权限）  

所有方式均复用同一套鉴权逻辑（`Authorization: Bearer <api_key>`），且返回结构标准化（含 `output`, `usage`, `request_id` 字段）。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型通常上限为 32K tokens，视觉类模型图像分辨率建议 ≤ 1536×1536 像素  
- 视频与 3D 模型暂不支持流式响应，且生成耗时较长（秒级至分钟级），需合理设置客户端超时  
- 音频类模型（如 TTS、ASR）的输入/输出格式严格限定为 PCM/WAV（16-bit, 16kHz），不支持 MP3 直接上传  
- 全模态模型对输入模态组合有约束（如不支持同时传入视频 + 音频 + 3D 网格），具体兼容性见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档  
- 向量模型（embedding/rerank）仅接受文本输入，不支持图像或音频嵌入 —— 此限制与部分早期内部文档描述不符，请以 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 为准

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


