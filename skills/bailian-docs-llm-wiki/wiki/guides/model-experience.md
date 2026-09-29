# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或控制台界面，按需选择文本、视觉、语音、音视频、3D 等各类模型服务，并灵活配置关键参数进行推理验证。所有模型均遵循统一的身份认证、计费与配额体系，详见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前支持以下核心模型类别（按模态组织）：
- **文本生成**：支持大语言模型（如 Qwen 系列）的对话、补全、摘要等任务  
- **视觉理解**：图像分类、OCR、目标检测、图文理解等  
- **图片生成与编辑**：文生图、图生图、局部重绘、风格迁移  
- **视频生成与编辑**：文生视频、图生视频、视频插帧与剪辑  
- **世界模型**：具备环境建模与决策规划能力的具身智能模型  
- **3D 模型生成**：支持文本/图像输入生成可导出的 3D 网格（参见 [TriPo 3D 生成指南](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音频生成、音乐生成  
- **全模态**：支持跨模态联合理解与生成（如图文音视频混合输入输出）  
- **向量与重排序**：文本嵌入（embedding）、语义向量检索、结果重排序  

> **注意**：语音合成与语音识别的官方文档已迁至阿里云帮助中心，[模型体验](../../raw/model-user-guide/model-experience.md) 中保留的链接为历史引用，实际使用请以 `https://help.aliyun.com/zh/model-studio/...` 为准。

## 关键参数

各模型共用以下基础参数（部分模型支持扩展参数）：
- `model`: 模型标识符（如 `qwen-max`, `wanx-v1`, `speech_16k_zh-cn`），必须指定  
- `input`: 输入内容，结构依模型类型而异（如 `{"text": "..."}` 或 `{"image_url": "..."}`）  
- `parameters`: 可选字典，常见字段包括：  
  - `temperature`: 控制生成随机性（0.0–2.0，默认 1.0）  
  - `top_p`: 核采样阈值（0.0–1.0）  
  - `max_tokens`: 输出最大 token 数  
  - `seed`: 随机种子（确保结果可复现）  
  - `stream`: 是否启用流式响应（布尔值）  

具体参数说明请参考对应子模型文档，例如 [文本生成模型](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉模型](../../raw/model-user-guide/model-experience/vision-model.md)。

## 使用方式

1. **API 调用**：通过 `POST /v1/models/{model}/invoke` 接口提交请求，需携带 `Authorization: Bearer <api_key>`  
2. **控制台体验**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入与参数 → 点击「运行」  
3. **SDK 调用**（Python 示例）：  
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = bailian_models.Client(...)
   response = client.invoke_model(
       model='qwen-max',
       input={'text': '你好'},
       parameters={'temperature': 0.7}
   )
   ```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（视频类模型为 100 MB）  
- 流式响应仅支持文本、语音合成、部分视觉模型；视频/3D/全模态模型暂不支持流式  
- 向量模型（embedding）不支持 `temperature`、`top_p` 等采样参数  
- 所有模型调用受项目级配额与速率限制约束，超限返回 `429 Too Many Requests`  
- 视频与 3D 生成类任务耗时较长，建议设置合理超时（推荐 ≥ 300 秒）  
- 多模态输入（如图文混合）需严格遵循各模型定义的 `input` schema，错误结构将导致 `400 Bad Request`  

> **注意**：[视频生成与编辑模型](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 文档中提及的“支持 GIF 输出”在 v2.3.0+ 版本中已被移除，当前仅支持 MP4；该信息尚未在原文中同步更新，请以实际 API 响应为准。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


