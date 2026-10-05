# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的API能力，当前仅支持Tripo-3D模型生成服务。该能力适用于快速原型设计、游戏资产预研及AIGC内容生产等场景，输出为标准GLB格式文件。

## 支持的模型/功能

- 当前唯一支持的模型为 **Tripo-3D**，支持文本到3D（text-to-3D）和图像到3D（image-to-3D）两种模态输入；  
- 输出为单个 `.glb` 文件（二进制GL Transmission Format），包含完整几何、材质与基础光照信息；  
- 不支持点云、网格编辑、多视角重建或视频输入。详细接口定义见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是（text-to-3D） | 中英文自然语言描述，建议≤100字符，避免模糊修饰词（如“精美”“高质量”） |
| `image_url` | string | 是（image-to-3D） | 可访问的公网图片URL（支持PNG/JPEG），宽高比建议1:1，分辨率≥512×512 |
| `negative_prompt` | string | 否 | 禁止生成的内容描述（如“text, logo, background”），效果弱于[prompt](../guides/prompt.md)，详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md) |
| `seed` | integer | 否 | 随机种子，用于结果复现（范围0–4294967295） |

> **注意**：`image_url` 参数在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确要求HTTPS协议，而旧版文档未强调此约束，以该API参考为准。

## 使用方式

1. 调用 `POST /v1/3d/generation` 接口；  
2. 请求体为JSON，按输入模态选择 `prompt` 或 `image_url`（二者不可同时为空，也不可同时提供）；  
3. 响应返回 `task_id`，需轮询 `GET /v1/3d/generation/{task_id}` 获取状态；  
4. `status == "succeeded"` 时，`output.model_url` 即为可下载的GLB文件直链（有效期24小时）。完整调用流程参见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 限制和注意事项

- 单次请求最大超时时间为300秒，平均生成耗时约120–240秒；  
- 每日免费额度为5次，超出后按量计费（见控制台配额管理）；  
- 输入图像若含显著透视畸变、遮挡或低对比度，易导致几何失真；文本提示中避免使用品牌名、人物肖像等可能触发内容安全拦截的词汇；  
- GLB文件不包含动画、骨骼或PBR材质贴图（如roughness/metallic），如需进一步处理，建议导入Blender等工具后手动增强。更多约束说明请查阅 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


