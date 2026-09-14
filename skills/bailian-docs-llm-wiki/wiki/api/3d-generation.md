# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的能力，当前由 Tripo 模型支持，适用于快速原型设计、游戏资产生成等场景。该能力通过统一的 Model API 接口调用，需指定 `model` 和 `input` 字段，并遵循特定的参数约束。详细接口规范和示例请参见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 支持的模型/功能

- 当前仅支持 `tripo-1.0` 模型（对应 Tripo 官方发布的 Tripo-3D v1.0），不支持其他 3D 生成模型。
- 支持两种输入模式：纯文本描述（text-to-3D）和单张参考图像（image-to-3D）；暂不支持多图输入或带掩码的条件控制。
- 输出为 `.glb` 格式的网格模型（含基础材质与法线），可通过 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 获取完整 MIME 类型与结构说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `"tripo-1.0"` |
| `input.prompt` | string | 是（text-to-3D） | 中文或英文提示词，长度 ≤ 200 字符；避免模糊表述（如“高质量”“逼真”） |
| `input.image_url` | string | 是（image-to-3D） | 可公开访问的 PNG/JPEG 图像 URL，分辨率建议 512×512～1024×1024；需确保主体居中、背景简洁 |
| `parameters.style` | string | 否 | 可选值：`"realistic"`（默认）、`"cartoon"`；该字段行为以 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 定义为准 |

> **注意**：原始文档中提及的 `input.negative_prompt` 字段在当前 API 版本（v2024.07）中已被移除，实际请求中传入将被忽略——请以最新 SDK 示例和 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 的参数表为准。

## 使用方式

1. 构造 POST 请求至 `/v1/models/{model}/invoke`（如 `/v1/models/tripo-1.0/invoke`）；
2. 请求体 JSON 示例（text-to-3D）：
   ```json
   {
     "model": "tripo-1.0",
     "input": {
       "prompt": "a red ceramic teapot with steam rising"
     },
     "parameters": {
       "style": "realistic"
     }
   }
   ```
3. 成功响应返回 `output.model_url`（有效期 24 小时），指向可直接下载的 `.glb` 文件；失败时返回标准错误码及 `error.message`。

## 限制和注意事项

- 单次请求最大等待时间 180 秒，超时返回 `504 Gateway Timeout`；
- 每日调用量受项目配额限制，超出后返回 `429 Too Many Requests`；
- 输入图像不得含人脸、可识别文字或版权敏感内容，否则可能触发内容安全拦截；
- 生成结果不保证拓扑一致性或可编辑性（如 Blender 导入后需手动修复法线/UV），生产环境建议人工校验；
- 模型对复杂几何（如细长杆件、薄壁结构）和透明材质支持有限，效果不稳定——具体能力边界详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


