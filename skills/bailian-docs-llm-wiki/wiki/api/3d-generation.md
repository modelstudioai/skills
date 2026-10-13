# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前通过 Tripo 模型实现端到端的快速建模。该能力适用于游戏资产、电商展示、AR/VR 内容等开发场景，输出为标准 GLB 格式文件。所有调用均通过统一的 `/v1/models/{model}/generate` 接口发起。

## 支持的模型/功能

- 当前仅支持 `tripo-1.0` 模型（对应 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档），不支持其他模型别名或历史版本。
- 支持两种输入模式：纯文本描述（text-to-3D）和单张 RGB 图像（image-to-3D）；暂不支持多视图图像、点云或网格输入。
- 输出为带纹理的 GLB 文件（二进制格式），包含 PBR 材质信息，可直接用于 Three.js、Babylon.js 等主流引擎。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object | 是 | 必须包含 `text`（string）或 `image_url`（string）字段；二者不可同时为空，也不可同时存在 |
| `seed` | integer | 否 | 随机种子，范围 [-2147483648, 2147483647]；相同 seed + 相同 input 可复现结果 |
| `resolution` | string | 否 | 可选 `"low"`（默认）、`"medium"`、`"high"`；影响生成耗时与面数，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |
| `output_format` | string | 否 | 固定为 `"glb"`，暂不支持 OBJ、STL 等其他格式 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持多轮迭代优化”，但该功能尚未上线，实际 API 不接受 `refinement_steps` 或 `previous_task_id` 等相关字段，调用将返回 `400 Bad Request`。

## 使用方式

1. 构造请求体（JSON）：
   ```json
   {
     "input": { "text": "a minimalist ceramic vase on white background" },
     "seed": 42,
     "resolution": "medium"
   }
   ```
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/models/tripo-1.0/generate`
3. 解析响应中的 `output.result_url` 字段，该 URL 为临时可下载的 GLB 文件地址（有效期 24 小时）

## 限制和注意事项

- 单次请求最大输入文本长度为 512 Unicode 字符；图像 URL 必须可公开访问且尺寸 ≤ 1024×1024 像素。
- 生成任务最长等待时间为 180 秒，超时返回 `504 Gateway Timeout`；建议客户端实现重试逻辑（指数退避）。
- GLB 文件体积通常为 2–15 MB，需确保下游服务具备足够内存解压及解析能力；部分轻量级 WebGL 库可能需预处理压缩纹理。
- 生成结果受输入语义明确性影响显著，模糊描述（如“一个好看的东西”）或含冲突约束（如“透明金属球”）将导致几何失真或材质异常——具体提示词工程建议参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


