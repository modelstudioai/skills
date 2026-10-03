# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的API能力，当前仅支持Tripo系列模型。该能力适用于快速原型设计、游戏资产预研及AIGC工作流集成等场景。所有请求需通过标准REST API调用，返回GLB格式的网格模型及元数据。

## 支持的模型/功能

- 当前唯一支持的模型为 `tripo-1.0`（详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)）  
- 支持两种输入模式：纯文本描述（text-to-3D）和单张RGB图像（image-to-3D）  
- 输出为标准GLB文件（含纹理与PBR材质），附带JSON元数据（如bbox尺寸、生成耗时、mesh统计信息）  
- 不支持多视角图、点云、视频或深度图输入；[3D模型生成](../../raw/model-api-reference/3d-generation.md) 明确指出“仅接受单图或单文本”，与Tripo官方文档一致  

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object | 是 | 必须包含 `type`（`text` 或 `image_url`）及对应字段；`image_url` 需为公网可访问的HTTPS链接，支持JPG/PNG，最大5MB |
| `prompt` | string | `type=text` 时必填 | 英文自然语言描述，建议≤100字符；中文提示词将被自动翻译（见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)） |
| `negative_prompt` | string | 否 | 英文负向提示，用于抑制特定特征（如"low poly", "watermark"） |
| `seed` | integer | 否 | 控制生成随机性，范围0–4294967295；设为-1表示随机 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中示例使用 `image` 字段传base64，但实际API仅接受 `image_url`；该处为过时示例，以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的参数定义为准。

## 使用方式

1. 发送 `POST /v1/models/tripo-1.0:generate` 请求  
2. Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. Body 示例（text-to-3D）：
```json
{
  "input": {
    "type": "text",
    "prompt": "a minimalist ceramic vase on white background"
  },
  "negative_prompt": "text, logo, watermark"
}
```
4. 成功响应返回 `status=success` 及 `output.glb_url`（有效期24小时）

## 限制和注意事项

- 单次请求超时：180秒；生成失败时返回 `status=failed` 及 `error_code`（如 `INPUT_INVALID`, `MODEL_TIMEOUT`）  
- 每日配额按项目级API Key计费，具体额度见控制台配额管理页  
- GLB文件默认分辨率约512×512纹理，不支持自定义面数或LOD；高精度需求需后处理（如Blender重拓扑）  
- 输入图像若含显著透视畸变、遮挡或低对比度，可能导致几何失真——此限制在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“常见问题”章节有明确说明

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


