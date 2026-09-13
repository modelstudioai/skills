# video generation api

视频生成 API 提供多种模型能力，支持文生视频、图生视频、人像驱动动画等场景。开发者可通过统一接口调用不同后端模型，按需选择适合任务的模型。所有模型均通过百炼平台统一鉴权与计费，具体能力边界和输入要求需结合各模型文档确认。

## 支持的模型/功能

当前支持以下视频生成模型：
- **HappyHorse**：面向通用文生视频任务，支持 4s 短视频生成 [原文标题](../../raw/model-api-reference/video-generation-api.md)  
- **万相**：侧重艺术风格视频生成，支持中文提示词优化与多风格控制 [原文标题](../../raw/model-api-reference/video-generation-api.md)  
- **人像驱动**：基于单张人像图与语音/文本驱动生成口型同步动画，适用于数字人场景 [原文标题](../../raw/model-api-reference/video-generation-api.md)  
- **爱诗（PixVerse）**：强调高动态帧率与电影感运镜，支持 16:9/9:16 多比例输出  
- **可灵（Kling）**：支持长时序一致性建模，最长可生成 120 帧（约 4 秒）视频  
- **Vidu**：国产自研大模型，对中文语义理解强，支持复杂动作描述  
- **MiniMax**：提供轻量级 SDK 接入方式，适合移动端集成  

> **注意**：原始文档中未明确标注各模型的输入分辨率、帧率、最大时长等技术规格，实际使用前请务必查阅对应模型的独立 API 文档（如 [Vidu API 文档](https://help.aliyun.com/zh/model-studio/vidu-api-reference)），避免因参数超限导致请求失败。

## 关键参数

通用必填参数包括：
- `model`: 模型标识符（如 `"kling-v1"`, `"vidu-1.0"`），必须与[原文标题](../../raw/model-api-reference/video-generation-api.md)所列名称严格一致  
- `input`: 输入内容对象，结构依模型而异（如 `text` 字段用于文生视频，`image_url` + `audio_url` 用于人像驱动）  
- `parameters`: 可选配置项，常见字段有 `duration`（秒）、`aspect_ratio`（如 `"16:9"`）、`seed`（整数，用于结果复现）  

部分模型（如万相、爱诗）支持 `style_preset` 参数指定预设风格；人像驱动模型强制要求 `voice_cloning_enabled: false` 或提供合规授权凭证。

## 使用方式

1. 通过百炼控制台开通对应模型的 API 权限  
2. 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation`  
3. 在 Header 中携带 `Authorization: Bearer ${API_KEY}` 和 `Content-Type: application/json`  
4. Body 示例（以 HappyHorse 为例）：
```json
{
  "model": "happyhorse-v1",
  "input": {"text": "一只橘猫在秋日森林中跳跃"},
  "parameters": {"duration": 4, "aspect_ratio": "16:9"}
}
```

## 限制和注意事项

- 所有模型均限制单次请求最大 `duration` ≤ 4 秒（Vidu 与 Kling 当前实测上限为 4.08 秒，超出将截断）  
- 图片输入需为公网可访问 URL，且格式为 JPG/PNG，尺寸建议 ≥ 512×512；人像驱动模型要求人脸区域占比 ≥ 30%  
- 视频生成不支持实时流式响应，返回为 `video_url`（有效期 24 小时）及元数据  
- 禁止生成含暴力、政治敏感、成人内容的视频；违反将触发自动拦截并计入违规调用次数  
- 各模型的计费粒度不同（如按 token、按秒或按请求），详情见[原文标题](../../raw/model-api-reference/video-generation-api.md)中的资费说明章节

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


