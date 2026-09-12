# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前由Tripo-3D模型支持，适用于快速生成中低复杂度的通用3D资产。该能力以API形式开放，需通过`/v1/3d/generation`端点调用，不支持实时流式响应。详细接口定义与字段说明见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 支持的模型/功能

- 当前仅支持 **Tripo-3D** 模型（v1.0），支持两种输入模态：
  - 文本到3D：输入英文提示词（如 `"a minimalist ceramic vase on a wooden table"`），输出GLB格式3D模型；
  - 图像到3D：输入单张RGB图像（JPG/PNG，≤4MB），输出对应几何重建的GLB文件。
- 不支持多视角图、视频、点云或深度图输入；也不支持编辑已有3D模型（如重拓扑、UV调整等）。更多能力边界请参考 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 包含 `type`（`text` 或 `image_url`）及对应值；`image_url` 需为公网可访问的HTTPS链接 |
| `output_format` | string | 否 | 默认 `"glb"`；暂不支持 `"obj"` 或 `"fbx"` |
| `seed` | integer | 否 | 控制生成随机性，范围 `[0, 2147483647]`；设为 `-1` 表示随机种子 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持中文提示词”，但实测仅英文提示词稳定生效；中文输入可能导致空输出或格式错误，建议始终使用英文描述。

## 使用方式

1. 构造请求体（JSON），例如文本生成：
   ```json
   {
     "input": { "type": "text", "data": "a sleek red sports car" },
     "output_format": "glb"
   }
   ```
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/3d/generation`，携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
3. 解析响应中的 `output.model_url` 字段，该URL有效期为24小时，需及时下载。

完整调用示例与错误码说明详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 限制和注意事项

- 单次请求最大等待时间 300 秒，超时返回 `504 Gateway Timeout`；
- 输入图像分辨率建议 512×512 至 1024×1024，过低（<256px）或过高（>2048px）均显著降低重建质量；
- 输出GLB文件大小通常为 2–15 MB，需确保客户端具备足够内存解压与渲染；
- 暂不支持批量提交或多任务并发（即使使用不同`seed`）；
- 所有生成内容须符合中国法律法规及百炼内容安全策略，禁止生成武器、暴力、成人相关内容。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


