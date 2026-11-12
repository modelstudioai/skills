# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的API能力，当前仅支持Tripo模型。该能力适用于快速原型设计、游戏资产生成等场景，输出为GLB格式网格文件。所有请求需通过`/v1/3d/generation`端点发起，采用异步工作流（提交→轮询→获取结果）。

## 支持的模型/功能

- 当前唯一支持的模型是 [Tripo](raw/model-api-reference/3d-generation/tripo-api-reference.md)，由Tripo AI提供，支持文本到3D（text-to-3D）和图像到3D（image-to-3D）两种模式。
- 输出为标准GLB（glTF Binary）格式，包含完整几何、材质与基础光照信息，可直接导入Blender、Unity或Three.js等主流引擎。
- 不支持多视角输入、视频输入或物理属性编辑；相关能力请参考 [Tripo](raw/model-api-reference/3d-generation/tripo-api-reference.md) 官方文档说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是（text-to-3D） | 中英文自然语言描述，建议≤100字符，避免模糊修饰词（如“精美”“高质量”） |
| `image_url` | string | 是（image-to-3D） | 可访问的PNG/JPEG公网URL，分辨率建议512×512或更高，宽高比应接近1:1 |
| `seed` | integer | 否 | 随机种子，用于结果复现；若未指定，服务端自动生成 |
| `output_format` | string | 否 | 当前仅支持`glb`，默认值即`glb`，其他值将被忽略 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 未明确说明`image_url`是否支持私有OSS签名URL，但实测中仅接受公开可直连的HTTP(S) URL；若需内网或鉴权资源，请先做临时公开代理——该限制在 [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md) 文档中亦未澄清，建议以实际调用反馈为准。

## 使用方式

1. **提交任务**：`POST /v1/3d/generation`，传入`prompt`或`image_url`（不可同时为空，也不可同时提供）；
2. **轮询状态**：使用返回的`task_id`调用`GET /v1/3d/generation/{task_id}`，检查`status`字段（`queued`/`processing`/`success`/`failed`）；
3. **获取结果**：`status == "success"`时，从响应`result.glb_url`下载GLB文件（有效期24小时）；
4. 全流程示例代码见 [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md) 中的cURL与Python片段。

## 限制和注意事项

- 单次请求最大超时600秒，任务队列等待时间通常<30秒，但高峰时段可能延长；
- 每个GLB文件大小上限为20MB，超出将导致`failed`状态并返回`output_too_large`错误码；
- 输入图像若含过多纹理噪声、严重遮挡或非单物体构图，生成质量显著下降——此现象在 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中未预警，但[Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md) 的最佳实践章节已明确建议使用干净白底单物图；
- 不支持批量提交；如需并发生成，请自行控制QPS ≤ 5（超过将触发限流，返回429）。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


