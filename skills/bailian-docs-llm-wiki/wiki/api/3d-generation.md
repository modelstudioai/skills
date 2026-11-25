# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的API能力，当前仅支持Tripo模型，适用于快速原型设计、游戏资产生成等场景。该能力以异步任务方式运行，需轮询获取生成结果。所有请求均需通过`/v1/3d/generation`端点提交。

## 支持的模型/功能

- 当前**唯一支持的模型为 Tripo**，详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 文档；
- 支持两种输入模式：纯文本描述（`prompt`）或图文混合（`prompt` + `image_url`）；
- 输出为 `.glb` 格式的通用3D模型文件，可通过标准WebGL引擎直接加载。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是 | 中文或英文提示词，建议包含物体类别、材质、视角等细节；避免抽象概念或动态动作描述 |
| `image_url` | string | 否 | JPEG/PNG格式的参考图URL（需公网可访问），与`prompt`协同提升几何一致性；若提供，`prompt`仍需描述主体语义 |
| `callback_url` | string | 否 | 异步完成回调地址（需HTTPS），平台将POST结果至该地址；未提供则需主动轮询 `/v1/3d/generation/{task_id}` |
| `seed` | integer | 否 | 随机种子，用于结果复现（范围0–4294967295） |

> **注意**：[3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持多视角渲染输出”，但当前API实际返回仅含单个`.glb`文件，该功能尚未上线，以 [Tripo](../../raw/3d-generation/tripo-api-reference.md) 的最新接口定义为准。

## 使用方式

1. 发送 `POST /v1/3d/generation` 请求，携带上述参数（`Content-Type: application/json`）；
2. 解析响应中的 `task_id` 和 `status`（通常为 `queued` 或 `running`）；
3. 轮询 `GET /v1/3d/generation/{task_id}` 直至 `status` 变为 `success`（含 `model_url`）或 `failed`；
4. 下载 `model_url` 指向的 `.glb` 文件（有效期24小时），该URL由平台OSS托管，无需鉴权。

示例请求体：
```json
{
  "prompt": "一只写实风格的陶瓷猫摆件，白色釉面，坐姿，正面视角",
  "image_url": "https://example.com/cat-ref.jpg",
  "seed": 42
}
```

## 限制和注意事项

- 单次请求最大`prompt`长度为200字符；`image_url` 图片分辨率建议 ≥ 512×512，过大可能导致超时；
- 不支持生成带骨骼动画、物理碰撞体或复杂材质贴图（如PBR多贴图集）的模型；
- 生成耗时通常为 60–180 秒，超时阈值为 300 秒，超时任务状态置为 `failed`；
- 所有输入内容须符合中国法律法规及百炼内容安全策略，禁止生成违法、暴力、色情或侵权内容——具体细则参见 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 的合规章节。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


