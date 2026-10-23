# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前仅支持 Tripo-3D 模型。该能力适用于快速生成低多边形、可导出为 `.glb` 格式的通用3D资产，适用于原型设计、游戏预研和Web端轻量展示等场景。生成过程为[异步任务](../concepts/asynchronous-task.md)，需轮询获取结果。

## 支持的模型/功能

- 当前唯一支持的模型为 **Tripo-3D**，对应 API 接口为 `tripo-3d-generation`；其他3D生成模型暂未接入。
- 支持两种输入模式：纯文本描述（如 `"a red ceramic mug with handle"`）或单张RGB图像（需为正面清晰图，背景尽量简洁）。
- 输出为标准 `.glb` 文件（含几何、材质与基础光照），可通过 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 获取完整字段说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是（文本模式） | 中英文自然语言描述，建议 ≤100 字；避免模糊词（如“beautiful”、“nice”） |
| `image_url` | string | 是（图像模式） | 可公开访问的 HTTPS 图片 URL，尺寸建议 512×512 或以上，格式为 JPG/PNG |
| `resolution` | string | 否 | 可选 `"low"`（默认，约 2k 三角面）、`"medium"`（约 5k）、`"high"`（约 10k）；更高分辨率不保证稳定性，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |
| `seed` | integer | 否 | 随机种子，用于结果复现 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持多视角图像输入”，但当前 API 实际仅接受单图；该描述已过时，请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的参数定义为准。

## 使用方式

1. 发起 POST 请求至 `/v1/models/tripo-3d-generation:generate`；
2. Body 为 JSON，按输入模式选择 `prompt` 或 `image_url`（二者不可同时存在）；
3. 响应中返回 `task_id`，随后调用 `/v1/tasks/{task_id}` 轮询状态（推荐间隔 ≥3s）；
4. 状态变为 `succeeded` 后，`output.model_url` 即为可下载的 `.glb` 文件地址（有效期 24 小时）。

## 限制和注意事项

- 单次请求最大超时时间为 300 秒；生成失败时响应中 `error.code` 会明确标识原因（如 `INVALID_INPUT`、`TIMEOUT`）；
- 输入图像禁止含人脸、可识别文字、版权敏感内容（如品牌Logo），否则将被拦截并返回 `CONTENT_POLICY_VIOLATION`；
- `.glb` 输出不包含动画、骨骼或 PBR 材质高级属性，如需进一步处理，建议导入 Blender 等工具后编辑；
- 该能力暂不支持批量提交或 Webhook 回调，需自行实现轮询逻辑——详细错误码与重试建议见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


