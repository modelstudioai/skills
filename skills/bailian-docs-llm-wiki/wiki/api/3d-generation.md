# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前通过 Tripo 模型实现端到端的快速建模。该能力适用于原型设计、游戏资产预研、电商展示等开发场景，输出为标准 GLB 格式文件。所有调用均通过统一的 `/v1/models/{model_id}/generate` 接口发起。

## 支持的模型/功能

- 当前仅支持 `tripo-1.0` 模型（对应 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档），不支持多模型并行或自定义模型替换。
- 支持两种输入模式：纯文本描述（text-to-3D）和单张参考图+文本提示（image+text-to-3D）；暂不支持多图输入或视频输入。
- 输出为单个 `.glb` 文件（含几何、材质与基础光照），不提供 OBJ/FBX 等其他格式导出选项，亦不支持网格编辑或UV重拓扑等后处理。

## 关键参数

- `prompt`（必填，string）：中文或英文描述，建议控制在 200 字符内，避免模糊修饰词（如“精美”“高质量”）；具体约束见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- `image_url`（可选，string）：公网可访问的 JPG/PNG 图像 URL；若提供，将覆盖 prompt 的部分语义，但不会完全忽略 prompt 文本。
- `seed`（可选，integer）：用于结果复现，范围 0–4294967295；未指定时服务端随机生成。
- `output_format`（固定为 `"glb"`，不可修改）。

## 使用方式

1. 调用 `POST /v1/models/tripo-1.0/generate`，Body 为 JSON 格式，例如：
   ```json
   {
     "prompt": "a minimalist ceramic vase, white matte finish, studio lighting",
     "image_url": "https://example.com/ref.jpg",
     "seed": 42
   }
   ```
2. 接口返回 `task_id`，需轮询 `GET /v1/tasks/{task_id}` 获取状态；成功时 `result.url` 指向临时可下载的 GLB 文件（有效期 24 小时）。
3. 全流程示例代码及错误码说明详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 限制和注意事项

- 单次请求最大等待时间 180 秒，超时返回 `TASK_TIMEOUT` 错误；生成失败时无重试机制，需客户端重发。
- 输入图像分辨率建议 512×512 至 1024×1024，过低（<256px）或过高（>2048px）可能导致纹理失真或拒绝处理。
- > **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中提及的 `style` 参数已在 v2.3.0 API 版本中移除，实际调用时传入将被静默忽略，请勿依赖该字段。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


