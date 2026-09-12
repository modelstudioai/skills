# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘等核心能力，适用于内容创作、设计辅助与自动化视觉生产等场景。所有模型均通过标准 RESTful 接口调用，支持同步响应与异步任务模式。开发者需根据具体需求选择适配的模型及参数组合。

## 支持的模型/功能

当前支持以下图像生成模型（按发布顺序与定位区分）：
- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：侧重多模态理解与可控生成，支持 [prompt](../guides/prompt.md) 中嵌入结构化指令；  
- **万相（WanXiang）**：面向高保真艺术风格生成，支持 `style` 参数精细控制流派（如 `anime`, `oil_painting`, `cyberpunk`）；  
- **Z-Image**：轻量级实时生成模型，适合低延迟场景，但不支持图生图；  
- **可灵（Kling）**：支持长宽比自定义（1:1, 4:3, 16:9, 9:16）、高分辨率输出（最高 1024×1024），并兼容 ControlNet 类扩展；  
- **Vidu**：虽以视频生成为主，但其静态帧生成能力已集成至 `/v1/images/generations` 路径，需显式指定 `model=vidu-image`；  
- **创意工具（Creative Tools）**：提供图像增强、背景移除、主体抠图等后处理能力，作为独立子模块调用。  

> **注意**：[原文标题](../../raw/model-api-reference/image-generation.md) 中列出的 Vidu 链接指向视频模型文档，实际图像生成能力需参考 [原文标题](../../raw/model-api-reference/vidu-image.md)（该文档明确说明 `vidu-image` 是独立图像模型，非 Vidu 视频模型的降维使用）。另据 [原文标题](../../raw/model-api-reference/z-image.md)，Z-Image 已于 v2.3.0 起弃用图生图功能，与早期文档描述存在偏差。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `wanx-v1`, `kling-v1`, `zimage-v2`），必须与所选模型严格匹配；  
- `prompt`: 中文或英文文本提示词，长度 ≤ 512 字符；支持部分模型的负向提示（`negative_prompt`），但 Z-Image 不支持；  
- `size`: 输出尺寸，格式为 `WIDTHxHEIGHT`（如 `1024x1024`），各模型支持范围不同（详见各模型文档）；  

可选参数：
- `n`: 生成图片数量（默认 1，最大 4）；  
- `seed`: 随机种子，用于结果复现（仅部分模型稳定支持，万相与可灵效果最佳）；  
- `style`: 仅万相与可灵支持，取值见对应模型文档枚举；  
- `image` / `mask`: 图生图或局部重绘时需 base64 编码的 PNG/JPEG 图像数据（`image` 必填，`mask` 可选）。

## 使用方式

1. 发送 `POST` 请求至 `https://dashscope.aliyuncs.com/api/v1/images/generations`；  
2. Header 中设置 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`；  
3. Body 示例（万相生成）：
```json
{
  "model": "wanx-v1",
  "prompt": "一只赛博朋克风格的机械猫坐在东京雨夜街头",
  "size": "1024x1024",
  "style": "cyberpunk",
  "n": 1
}
```
4. 同步接口返回 `output.results[]` 数组，含 `url`（临时直链，有效期 1 小时）与 `task_id`（异步任务需轮询）；  
5. 异步任务通过 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回相同结构结果。

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 512 字符，超长将被截断且不报错；  
- 所有模型均禁止生成含暴力、色情、政治敏感或侵犯版权的内容，违规请求将被拦截并记录日志；  
- Z-Image 模型不支持 `negative_prompt` 和图生图，若误传相关字段将被静默忽略；  
- 可灵（Kling）对中文 [prompt](../guides/prompt.md) 的语义解析优于英文，建议优先使用中文描述；  
- 临时 URL 有效期为 1 小时，如需长期存储，请及时下载并保存至自有对象存储。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


