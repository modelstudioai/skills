# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前仅支持 Tripo 模型，通过统一 API 接口调用。该功能适用于快速生成中低复杂度的通用3D资产，输出为 GLB 格式，可直接用于WebGL、Unity等引擎。详细接口定义与行为规范请参考 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 支持的模型/功能

- 当前**唯一支持的模型**为 `tripo-1.0`（对应 Tripo 官方 v1.0 版本），无其他3D生成模型上线。
- 支持两种输入模式：  
  - **文本到3D**：输入英文 [prompt](../guides/prompt.md)（中文暂不支持语义理解，需翻译为英文）；  
  - **图像到3D**：输入单张 RGB 图像（JPG/PNG，建议正视角、背景简洁）。  
- 输出为标准 GLB 文件（含几何、材质、基础光照信息），不含动画或骨骼。

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持多视角图像输入”，但实际 API 仅接受单图；该描述已过时，以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的正式参数说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object | 是 | 包含 `type`（`text` 或 `image_url`）及对应字段；`image_url` 需为公网可访问 HTTPS 地址 |
| `prompt` | string | `type=text` 时必填 | 英文描述，长度 ≤ 200 字符；避免模糊词（如“beautiful”、“high quality”） |
| `image_url` | string | `type=image` 时必填 | 图片分辨率建议 512×512 ~ 1024×1024，宽高比应接近 1:1 |
| `seed` | integer | 否 | 控制生成随机性，范围 0–4294967295；设为 `-1` 表示随机种子 |

完整参数约束与默认值详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用方式

1. 调用 `POST /v1/models/tripo-1.0/generate`（需携带 `Authorization: Bearer <api_key>`）；
2. 请求体为 JSON，结构如下：
   ```json
   {
     "input": {
       "type": "text",
       "prompt": "a red ceramic mug on a wooden table"
     }
   }
   ```
3. 成功响应返回 `task_id`；轮询 `GET /v1/tasks/{task_id}` 获取状态，`status=success` 时 `output.glb_url` 即为可下载 GLB 文件地址（有效期 24 小时）。

## 限制和注意事项

- **输入限制**：不支持中文 [prompt](../guides/prompt.md)；图像 URL 必须可被百炼服务端直连（禁止私有网络、需绕过防盗链）；
- **输出限制**：单次生成耗时约 60–180 秒；GLB 文件大小上限 15 MB；不支持导出 OBJ/FBX 等格式；
- **内容安全**：生成内容受百炼内容策略约束，含暴力、成人、政治敏感等元素的输入将被拒绝；
- **调试建议**：首次集成时务必使用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 提供的示例 [prompt](../guides/prompt.md) 和 image_url 进行验证。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


