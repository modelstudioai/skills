# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前通过 Tripo 模型实现端到端的快速建模。该能力适用于原型设计、游戏资产生成、电商展示等场景，输出为标准 glTF 2.0 格式（含 `.glb` 文件）。所有请求均需通过 `/v1/models/3d-generation:generate` 接口调用。

## 支持的模型/功能

- 当前仅支持 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 一种模型，不支持多模型切换或自定义模型部署。
- 支持两种输入模式：纯文本描述（text-to-3d）和单张参考图+文本提示（image+text-to-3d）。
- 输出包含 `.glb` 二进制文件及元数据（如生成耗时、mesh面数统计），详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 文档说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是 | 中文或英文提示词，建议 ≤ 100 字符；避免模糊表述（如“好看”“高质量”） |
| `image_url` | string | 否 | JPEG/PNG 格式图片的公网可访问 URL；若提供，将覆盖 `prompt` 的几何主导权 |
| `seed` | integer | 否 | 随机种子，范围 0–4294967295；相同 seed + [prompt](../guides/prompt.md) 下结果可复现 |
| `output_format` | string | 否 | 默认 `"glb"`；暂不支持 `"gltf"` 或 `"obj"` |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及支持 `style` 参数，但实测该字段已被忽略，实际行为以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档为准，该参数已废弃。

## 使用方式

1. 构造 JSON 请求体（示例）：
```json
{
  "prompt": "一只卡通风格的蓝色陶瓷咖啡杯，带手柄，表面有波浪纹",
  "image_url": "https://example.com/ref.jpg",
  "seed": 42
}
```
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/models/3d-generation:generate`，携带 `Authorization: Bearer <api_key>`。
3. 轮询 `operation_id` 获取异步结果（最长等待 180 秒），成功响应中 `output.model_url` 即为可下载的 `.glb` 地址。

## 限制和注意事项

- 单次请求最大超时 120 秒；生成失败时返回 `error.code = "InvalidArgument"` 或 `"InternalError"`。
- 输入图片分辨率建议 512×512 至 1024×1024；过高分辨率可能导致裁剪或失真，具体约束见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- 不支持生成含动画、骨骼、材质贴图（如 PBR textures）的复杂资产；`.glb` 中仅含基础 mesh 和嵌入的 base-color texture。
- 免费试用额度有限，超出后需开通按量付费；计费单位为“每次成功生成”，无论输出大小。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


