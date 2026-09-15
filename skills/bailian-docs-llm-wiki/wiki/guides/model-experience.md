# model experience

`model experience` 是百炼平台为开发者提供的统一模型调用入口，支持多模态模型的快速体验与集成。通过该能力，开发者可无需单独申请模型权限，直接在控制台或 SDK 中发起推理请求。所有模型均遵循统一的 API 协议与鉴权机制，适用于原型验证、A/B 测试及轻量级生产场景。

## 支持的模型与功能

当前支持以下模型类别（按模态组织）：
- **文本生成**：包括通义千问系列（Qwen）、代码补全、摘要、翻译等 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解**：支持图像分类、OCR、图文理解等任务 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- **图像生成与编辑**：文生图、图生图、局部重绘、风格迁移等 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- **视频生成与编辑**：短时长视频生成、帧插值、视频描述等 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- **3D 模型生成**：基于文本生成可导出的 `.glb` 格式 3D 模型 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- **语音与音乐**：语音合成（TTS）、语音识别（ASR）、语音转语音（TTS2TTS）、音乐生成（FunMusic），其中 ASR/TTS/TTS2TTS 文档托管于阿里云帮助中心，**注意**：[语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 和 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 的最新参数与错误码已与百炼统一 SDK 不一致，建议优先参考 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 中的通用错误处理规范。  
- **全模态**：支持文本+图像+音频混合输入的联合推理 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  
- **向量与重排序**：文本嵌入（embedding）、语义相似度计算、检索重排序（rerank） [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展字段）：
- `model`: 必填，模型标识符（如 `qwen-max`, `qwen-vl-plus`, `wanx-video-1.0`），具体取值见各子文档  
- `input`: 必填，结构化输入，格式依模型类型而异（如文本模型为 `{"prompt": "..."}`，视觉模型为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`: 可选，控制生成行为（`temperature`, `top_p`, `max_tokens`, `seed` 等），**注意**：不同模型对同名参数的实际影响范围存在差异，例如 `max_tokens` 在视频模型中表示帧数上限而非 token 数，详见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  

## 使用方式

1. **控制台体验**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入 → 点击运行  
2. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，需携带 `Authorization: Bearer <api_key>`  
3. **SDK 调用**（推荐）：  
   ```python
   from alibabacloud_bailian20231229 import models as bailian_models
   client = BailianClient(...)
   response = client.invoke_model(
       model="qwen-max",
       input={"prompt": "你好"},
       parameters={"temperature": 0.7}
   )
   ```

## 限制和注意事项

- 免费额度仅限新用户首月，后续按调用量计费；单次请求最大输入长度因模型而异（文本模型默认 32k tokens，视觉模型图像分辨率上限 1536×1536）  
- 视频与 3D 模型生成任务为异步模式，需轮询 `GET /v1/jobs/{job_id}` 获取结果  
- 所有模型均不支持自定义 LoRA 或微调权重加载；若需私有化部署，请参阅 [模型体验](../../raw/model-user-guide/model-experience.md) 中的“企业版能力”章节（该章节目前仅限白名单客户访问）  
- **注意**：原始文档中列出的 [音乐生成](raw/model-user-guide/model-experience/fun-music.md) 当前已下线，实际可用模型请以控制台实时列表为准，避免硬编码模型 ID。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


