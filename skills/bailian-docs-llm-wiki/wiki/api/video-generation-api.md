# video generation api

视频生成 API 提供多种模型能力，支持文本到视频、图像到视频、人像驱动动画等生成任务。开发者可通过统一接口调用不同后端模型，按需选择适合业务场景的模型。所有模型均通过百炼平台统一鉴权与计费，无需单独申请接入。

## 支持的模型/功能

当前支持以下视频生成模型及对应能力：
- **HappyHorse**：面向通用场景的文生视频模型，支持 4s/8s 短视频生成  
- **万相**：侧重艺术风格化视频生成，支持多风格 [prompt](../guides/prompt.md) 控制  
- **人像驱动**：基于单张人像图+音频/文本驱动生成口型同步视频，适用于数字人场景  
- **爱诗（PixVerse）**：强调高动态细节与运镜表现，适合创意短视频  
- **可灵（Kling）**：支持长时序一致性建模，输出最长可达 120 帧（约 4 秒）  
- **Vidu**：国产自研大模型，支持中文 [prompt](../guides/prompt.md) 优先优化，对本土文化元素理解更优  
- **MiniMax**：提供低延迟推理选项，适合实时交互类应用  

各模型能力细节请参阅 [视频生成 (raw/model-api-reference/video-generation-api.md)](../../raw/model-api-reference/video-generation-api.md)。

## 关键参数

所有视频生成请求共用以下核心参数（`POST /v1/videos/generations`）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"kling"`, `"vidu"`, `"portrait-animation"`，必须与 [视频生成 (raw/model-api-reference/video-generation-api.md)](../../raw/model-api-reference/video-generation-api.md) 中列出的模型名严格一致 |
| `input` | object | 是 | 输入内容，结构依模型而异：文生视频为 `{ "prompt": "..." }`；人像驱动为 `{ "image_url": "...", "audio_url": "..." }` |
| `parameters.duration` | number | 否 | 视频时长（秒），默认值因模型而异（如 Kling 默认 4，Vidu 默认 2），详见 [视频生成 (raw/model-api-reference/video-generation-api.md)](../../raw/model-api-reference/video-generation-api.md) |

> **注意**：部分旧文档中将 `parameters.fps` 列为可选参数，但自 v2.3.0 起该字段已废弃，实际输出帧率由模型固定，不可覆盖。

## 使用方式

1. 构造 JSON 请求体，指定 `model` 和 `input`；
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/videos/generations`；
3. 解析响应中的 `output.video_url` 获取直链（有效期 24 小时）或 `output.task_id` 异步轮询结果。

示例（Kling 文生视频）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/videos/generations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "kling",
        "input": { "prompt": "一只橘猫在秋日森林中跳跃" },
        "parameters": { "duration": 4 }
      }'
```

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 512 字符（Vidu 为 384 字符）；  
- 人像驱动模型要求 `image_url` 图片分辨率 ≥ 512×512，且人脸占比 ≥ 30%；  
- 所有视频输出格式为 MP4（H.264 编码），分辨率统一为 720p（1280×720），暂不支持自定义宽高比；  
- 免费试用额度仅限 `kling` 和 `vidu` 模型，其他模型需开通对应服务；  
- 生成失败时响应中 `error.code` 可能为 `InvalidInput.ImageResolution` 或 `UnsupportedModel`，建议先校验输入与模型兼容性。

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)



