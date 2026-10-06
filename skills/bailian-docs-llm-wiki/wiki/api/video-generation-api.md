# video generation api

百炼平台的 video generation api 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。开发者可通过统一 API 接口调用不同底层模型，无需单独对接各模型服务。所有模型均通过 `POST /v1/videos/generations` 端点接入，遵循标准 OpenAI 兼容请求/响应格式。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：
- **文生视频（Text-to-Video）**：[可灵](raw/model-api-reference/video-generation-api/kling-api-reference.md)、[Vidu](raw/model-api-reference/video-generation-api/vidu-api-reference.md)、[爱诗](raw/model-api-reference/video-generation-api/pixverse-api-reference.md)  
- **图生视频（Image-to-Video）**：[万相](raw/model-api-reference/video-generation-api/wan-api-reference.md)、[HappyHorse](raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)  
- **人像驱动（Portrait Animation）**：[人像驱动](raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)  
- **多模态视频生成（含语音驱动）**：[MiniMax](raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)  

> **注意**：[原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的模型列表为最新官方支持清单；部分旧版文档（如早期 `wan-api-reference.md`）提及的 `--style=anime` 参数已在 v2.3+ 版本中移除，请以 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference.md) 的最新参数说明为准。

## 关键参数

所有请求共用以下核心字段（JSON body）：
- `model`（必填）：字符串，取值为模型标识符，如 `"kling-v1.0"`、`"wanx-v2"`、`"portrait-animation"`  
- `prompt`（必填）：描述性文本，长度 ≤ 512 字符（[原文标题](../../raw/model-api-reference/video-generation-api.md) 明确限制）  
- `size`（可选）：输出分辨率，格式为 `"WxH"`，如 `"1024x576"`；各模型支持范围不同，详见对应子文档  
- `duration`（可选）：视频时长（秒），仅部分模型支持（如 `kling` 支持 `2` 或 `4`，`vidu` 仅支持 `3`）  
- `seed`（可选）：整数，用于结果复现  

## 使用方式

1. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/videos/generations`  
2. 设置 Header：`Authorization: Bearer YOUR_API_KEY`，`Content-Type: application/json`  
3. Body 示例（以可灵为例）：
```json
{
  "model": "kling-v1.0",
  "prompt": "一只金毛犬在雪地中奔跑，阳光明媚",
  "size": "1024x576",
  "duration": 4
}
```
4. 响应返回 `id` 和 `status`；需轮询 `GET /v1/videos/{id}` 获取最终视频 URL（详见各模型子文档的 polling 机制说明）

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 512 字符，超长将被截断（[原文标题](../../raw/model-api-reference/video-generation-api.md) 明确说明）  
- 视频生成任务最长排队等待时间 10 分钟，超时返回 `status: expired`  
- 所有模型均**不支持**输入视频文件或帧序列；仅接受文本或单张图像（base64 或 URL）作为输入源  
- `portrait-animation` 模型要求输入图像必须为人脸正向清晰照，侧脸/遮挡/低光照会导致失败率显著上升  
- 各模型对 `negative_prompt` 的支持不一致：`kling` 和 `vidu` 完全忽略该字段，而 `minimax-video` 支持但需显式启用 `enable_negative_prompt: true`

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


