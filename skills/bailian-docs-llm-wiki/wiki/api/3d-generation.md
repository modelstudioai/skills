# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的API能力，当前仅支持Tripo-3D模型生成服务。该能力适用于快速构建原型、游戏资产预研及AIGC内容生产等场景，输出为GLB格式文件。详细接口规范与调用示例请参考 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 支持的模型/功能

- 当前唯一支持的模型为 **Tripo-3D**，支持两种输入模态：
  - 文本到3D（text-to-3D）：根据自然语言描述生成三维网格；
  - 图像到3D（image-to-3D）：以单张RGB图像为输入生成带纹理的3D模型。
- 不支持多视角图像输入、视频输入或点云输入；所有生成任务均默认返回带PBR材质的GLB文件（含mesh、texture、material信息）。
- 更多模型能力演进可关注 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中的版本更新说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 输入对象，必须包含 `type`（`text` 或 `image_url`）及对应字段（`text` 或 `image_url`） |
| `resolution` | string | 否 | 可选值：`low`（512³）、`medium`（1024³）、`high`（2048³）；默认 `medium`；注意高分辨率将显著增加生成耗时与费用 |
| `output_format` | string | 否 | 当前仅支持 `glb`，不可修改 |
| `seed` | integer | 否 | 随机种子，用于结果可复现；若未指定则服务端自动生成 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中曾提及支持 `obj` 格式输出，但该字段已废弃，实际调用中设置 `output_format=“obj”` 将被忽略并静默降级为 `glb`。

## 使用方式

1. 调用 `POST /v1/models/tripo-3d:generate` 接口；
2. 请求体需为 JSON，结构符合上述参数要求；
3. 成功响应返回 `status: "success"` 及 `output.model_url`（有效期24小时的直链）；
4. 建议在客户端校验 `model_url` 的HTTP状态码（200）及Content-Type（`model/gltf-binary`）后再加载渲染；
5. 完整请求/响应示例见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 限制和注意事项

- 单次请求最大输入文本长度为 200 字符；图像URL需为公网可访问的HTTPS链接，尺寸建议 ≥ 512×512，宽高比应接近1:1；
- 每个API Key每分钟限流 5 次（burst=10），超出将返回 `429 Too Many Requests`；
- 生成结果不保证物理精度或拓扑一致性（如非流形边、自交面），下游应用需自行做几何验证；
- 生成任务最长等待时间为 180 秒，超时后任务终止，`model_url` 不可用；
- 所有生成内容受阿里云《AIGC内容安全规范》约束，禁止生成违法、侵权或高危3D模型（如武器、人脸生物特征等）。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


