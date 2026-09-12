# video generation api

视频生成 API 提供多种模型能力，支持文生视频、图生视频、人像驱动动画等场景。开发者可通过统一接口调用不同后端模型，按需选择适合任务的模型。所有模型均通过百炼平台统一鉴权与计费，具体能力细节请参考各模型官方文档。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：
- **通用文生视频**：[可灵](https://help.aliyun.com/zh/model-studio/kling-api-reference)、[Vidu](https://help.aliyun.com/zh/model-studio/vidu-api-reference)、[爱诗](https://help.aliyun.com/zh/model-studio/pixverse-api-reference)  
- **图像增强/图生视频**：[万相](https://help.aliyun.com/zh/model-studio/wan-api-reference)  
- **人像驱动与口型同步**：[人像驱动](https://help.aliyun.com/zh/model-studio/portrait-animation-api-reference)  
- **轻量级视频生成**：[HappyHorse](https://help.aliyun.com/zh/model-studio/happyhorse-api-reference)、[MiniMax](https://help.aliyun.com/zh/model-studio/minimax-video-api-reference)  

> **注意**：[原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的模型链接均为外部帮助文档，实际可用模型列表以控制台「模型广场」中“视频生成”分类为准；部分链接（如 MiniMax）在控制台当前未开放公测，调用将返回 `ModelNotEnabled` 错误。

## 关键参数

所有视频生成请求共用以下核心参数（JSON body）：
- `model`: 模型标识符（如 `"kling-v1"`, `"wanx-v1"`），必须与 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中模型命名规范一致  
- `input`: 输入内容对象，结构因模型而异（如 `prompt` 字段为必填文生视频输入，`image_url` 为图生视频必需）  
- `parameters`: 可选配置，常见字段包括 `duration`（秒，支持 2–8s）、`aspect_ratio`（如 `"16:9"`）、`seed`（整数，用于复现）  
- `stream`: 布尔值，仅部分模型（如 Vidu）支持流式响应，详见各模型文档  

## 使用方式

1. 通过 HTTPS POST 请求调用 `/v1/videos/generations` 端点  
2. Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. 请求体示例（文生视频）：
```json
{
  "model": "kling-v1",
  "input": {
    "prompt": "一只橘猫在太空舱里打太极，赛博朋克风格"
  },
  "parameters": {
    "duration": 4,
    "aspect_ratio": "16:9"
  }
}
```
4. 成功响应返回 `video_url`（直链，有效期 24 小时）及 `task_id`，可用于轮询状态。详细协议格式见 [原文标题](../../raw/model-api-reference/video-generation-api.md)。

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 512 字符；图生视频输入图尺寸建议 ≥ 512×512，格式仅支持 JPG/PNG  
- 所有模型输出视频分辨率固定（如 Kling 输出 1024×576，Vidu 输出 1280×720），不支持自定义宽高  
- 人像驱动模型要求输入人脸图像清晰、正向、无遮挡；若检测失败将返回 `InvalidInput.FaceNotFound`  
- 免费额度仅限测试，生产环境需开通对应模型的商用授权，否则调用将被拒绝

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


