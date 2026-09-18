# 3d generation

百炼平台提供基于文本或图像输入生成三维网格模型（.glb 格式）的 API 能力，适用于快速原型设计、游戏资产创建和电商可视化等场景。当前仅支持 Tripo 模型，通过异步任务方式返回结果，需轮询获取生成状态与下载链接。该能力处于公测阶段，接口行为与参数可能随模型迭代调整。

## 支持的模型/功能

- 当前唯一支持的模型为 **Tripo-3D**，支持两种输入模式：
  - 文本到 3D（text-to-3D）：根据自然语言描述生成三维模型；
  - 图像到 3D（image-to-3D）：以单张正面视角图像（如 PNG/JPEG）为输入生成带纹理的网格。
- 功能细节与模型能力边界详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 包含 `text`（字符串）或 `image_url`（字符串）字段，二者不可同时为空；若同时提供，以 `image_url` 优先 |
| `output_format` | string | 否 | 目前仅支持 `"glb"`（默认值），不支持 `"obj"` 或 `"fbx"` |
| `seed` | integer | 否 | 随机种子（0–4294967295），用于结果可复现；未指定时服务端自动生成 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持多视角图像输入”，但最新 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确限定仅接受**单张正面图像**，多视角输入暂未开放，以后者为准。

## 使用方式

1. 发起异步请求：`POST /v1/models/tripo-3d:generate`，传入 `input` 等参数；
2. 解析响应中的 `task_id`；
3. 轮询 `GET /v1/tasks/{task_id}` 获取状态（`status: "succeeded"` 表示完成）；
4. 成功后从 `output.model_url` 下载 `.glb` 文件（有效期 24 小时）。

完整调用示例与错误码说明见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- 输入图像分辨率建议 512×512 至 1024×1024，过低（<384px）或过高（>2048px）可能导致生成失败或失真；
- 文本提示词长度上限为 200 字符，避免使用模糊描述（如“好看”“高质量”），推荐具体形状、材质、风格关键词（如“low-poly red ceramic mug with handle”）；
- 单次请求最大等待时间为 300 秒，超时任务将被终止，需检查 `status` 是否为 `"failed"` 并关注 `error_code`；
- 生成结果不含物理属性（如碰撞体、骨骼），如需进一步编辑，请导入 Blender 或 Unity 等 DCC 工具处理。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


