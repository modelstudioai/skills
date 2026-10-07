# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准 API 或 SDK 快速集成。其核心目标是降低模型使用门槛，同时保留对关键推理行为的精细控制。所有能力均基于 [模型体验](../../raw/model-user-guide/model-experience.md) 文档所定义的能力矩阵实现。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别（按模态组织）：

- **文本生成**：支持大语言模型（LLM）的对话、补全、摘要等任务  
- **视觉理解**：图文理解、OCR、图像描述生成  
- **图像生成与编辑**：文生图、图生图、局部重绘、尺寸适配  
- **视频生成与编辑**：文生视频、视频扩时、关键帧编辑  
- **世界模型**：具备环境建模与动态推理能力的具身智能模型  
- **3D 模型生成**：支持 TriPo 等 3D 生成模型，输出 GLB/OBJ 格式  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（TTS2TTS）、通用音频生成、音乐生成（含 [Fun Music](../../raw/model-user-guide/model-experience/fun-music.md)）  
- **全模态**：支持跨文本、图像、音频、视频的联合理解与生成  
- **向量与重排序**：嵌入（embedding）模型与语义重排序（rerank）模型  

> **注意**：语音合成与语音识别的官方文档已迁移至阿里云帮助中心（如 [https://help.aliyun.com/zh/model-studio/speech-synthesis](https://help.aliyun.com/zh/model-studio/speech-synthesis)），但 `model experience` 接口仍保持兼容；实际调用时请以 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的路径为准，避免直接依赖外部链接。

## 关键参数

所有模型调用共用以下基础参数（部分模型支持扩展参数）：

- `model`: 模型标识符（如 `qwen-vl-plus`、`wanx-video`、`funmusic-1.0`），必须与 [模型体验](../../raw/model-user-guide/model-experience.md) 中各子文档声明的合法值一致  
- `input`: 输入结构体，格式依模型类型而异（如文本生成为 `{"prompt": "..."}`，视觉理解为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`: 可选字典，常见字段包括：  
  - `temperature`（float, 0.0–2.0）  
  - `top_p`（float, 0.0–1.0）  
  - `max_tokens`（int, 仅文本类模型）  
  - `seed`（int, 控制确定性）  
  - `stream`（bool, 是否启用流式响应）  

具体参数约束详见各子模型文档，例如 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md) 对 `input` 结构有显著差异。

## 使用方式

1. **API 调用**：向 `/v1/models/{model}/invoke` 发送 POST 请求，`Content-Type: application/json`，携带 `input` 与 `parameters` 字段  
2. **SDK 调用**（Python）：
   ```python
   from aliyunsdkcore.client import AcsClient
   from aliyunsdkbailian.request.v20240719 import InvokeModelRequest

   req = InvokeModelRequest.InvokeModelRequest()
   req.set_model_id("qwen-vl-plus")
   req.set_input({"image_url": "...", "prompt": "描述这张图"})
   req.set_parameters({"temperature": 0.7})
   ```

3. **批量调用**：不支持原生批量，需自行并发封装；单次请求最大 `input` 大小为 16 MB（视频类模型上限为 512 MB）

## 限制和注意事项

- 单账号默认 QPS 限制为 5，可通过工单申请提升  
- 视频与 3D 模型生成任务默认超时时间为 300 秒，不可修改  
- 所有模型输入中的 URL 必须可公开访问且支持 `HEAD` 请求；内网或鉴权 URL 将失败  
- `model experience` 不提供模型微调入口，微调需通过 [模型训练](../../raw/model-user-guide/model-training.md) 模块完成  
- 音频类模型（如 Fun Music）暂不支持 `stream=True`，该限制已在 [Fun Music](../../raw/model-user-guide/model-experience/fun-music.md) 文档中明确说明

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


