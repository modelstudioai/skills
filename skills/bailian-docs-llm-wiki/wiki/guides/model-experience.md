# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准化接口调用文本、视觉、语音、音视频、3D 等各类模型，无需单独配置底层服务。所有模型均遵循统一的鉴权、计费与监控机制，便于集成与管理。

## 支持的模型与功能

当前支持以下核心模型类型及对应能力：
- 文本生成（如 Qwen 系列大语言模型）  
- 视觉理解（图文理解、OCR、目标检测等）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧编辑）  
- 3D 模型生成（TriPo 3D 生成，支持 GLB 输出）  
- 语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）  
- 音乐生成（FunMusic）  
- 全模态理解与生成（Omni-Modal）  
- 向量嵌入（Embedding）与重排序（Rerank）  

> **注意**：语音合成、语音识别、语音转语音三类能力实际由阿里云 Model Studio 提供，其 API 接口规范与百炼原生模型存在差异；请务必参考 [原文标题](../../raw/model-user-guide/model-experience.md) 中的外部链接说明，并在调用前确认 endpoint 和参数格式是否兼容百炼 SDK。

## 关键参数

所有模型调用均需指定以下通用参数：
- `model`: 模型标识符（如 `qwen-max`, `wanx-v1`, `tripo-3d`），具体取值见各子文档  
- `input`: 输入数据结构，格式依模型类型而异（如文本为 `{"prompt": "..."}`，图像为 base64 或 URL）  
- `parameters`: 可选控制参数（如 `temperature`, `top_p`, `seed`, `size` 等），详见 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md) 等各子文档  
- `stream`: 布尔值，控制是否启用流式响应（仅部分模型支持）

## 使用方式

1. 在百炼控制台开通对应模型服务（部分模型需单独申请配额）  
2. 使用 SDK（Python/Java/Go）或 HTTP 直连调用 `/v1/models/{model}/invoke` 接口  
3. 构造符合模型要求的 `input` 和 `parameters`，参考各子文档示例（如 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md) 中的图像输入格式）  
4. 处理响应：同步返回 `output` 字段，流式响应按 SSE 协议解析  

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型通常 ≤ 32768 tokens，视觉类模型单图分辨率上限为 2048×2048，视频类模型单次生成时长上限为 5 秒  
- 所有模型均受账户级 QPS 与并发数限制，超出将返回 `429 Too Many Requests`  
- TriPo 3D 生成暂不支持自定义材质与物理属性，输出仅含基础网格与 UV（详见 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）  
- FunMusic 音乐生成不支持指定 BPM 或调性，仅支持风格关键词（如 `"jazz"`, `"epic"`）  
- 全模态（Omni-Modal）模型目前仅接受单图 + 单文本输入，不支持多图或多轮对话上下文

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


