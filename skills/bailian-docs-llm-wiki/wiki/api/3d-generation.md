# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，当前通过集成Tripo-3D模型实现端到端的轻量级3D资产生成。该能力适用于快速原型设计、游戏素材预研及AIGC内容生产等场景，输出为标准GLB格式文件。详细接口定义与调用规范请参考 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 支持的模型/功能

- 当前仅支持 **Tripo-3D** 模型（v1.0），支持两种输入模态：
  - 文本描述生成（text-to-3D）
  - 单张图像生成（image-to-3D，需提供正面视角清晰图）
- 输出为单个 `.glb` 文件（二进制格式），包含网格、材质和基础光照信息，不支持动画或骨骼绑定。
- 该模型能力由 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 文档明确限定，暂无其他3D生成模型接入计划。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 输入对象，含 `text`（string）或 `image_url`（string）字段，二者不可同时为空；`text` 长度 ≤ 200 字符，`image_url` 需为公网可访问的PNG/JPEG链接 |
| `resolution` | string | 否 | 可选值：`low`（512×512，默认）、`medium`（1024×1024）、`high`（2048×2048）；分辨率越高，生成耗时越长，但高分辨率对细节提升有限，建议优先使用 `medium` |
| `seed` | integer | 否 | 随机种子（0–4294967295），用于结果复现；若未指定，服务端随机生成 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中未明确 `resolution` 的默认值，但实测行为与平台统一默认策略一致（`low`），此行为以实际API响应为准。

## 使用方式

1. 调用 `POST /v1/models/tripo-3d:generate` 接口；
2. 请求体为 JSON，结构示例如下：
```json
{
  "input": {
    "text": "a minimalist ceramic vase on white background"
  },
  "resolution": "medium",
  "seed": 42
}
```
3. 成功响应返回 `output.glb_url`（有效期24小时），需及时下载保存；
4. 错误码 `400` 表示输入校验失败（如文本超长、图片URL不可达），`500` 表示模型内部异常，重试前应检查输入合规性。完整错误码说明见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 限制和注意事项

- 单次请求最大等待时间 180 秒，超时将返回 `504 Gateway Timeout`；
- 不支持批量生成，每次请求仅生成一个GLB文件；
- 输入图像需为正交/近正交视角，侧视、俯视或含复杂背景的图像会导致几何失真；
- GLB文件不包含PBR材质贴图（如roughness/metallic），仅含基础baseColor；如需高级渲染，需后处理导入Blender等工具；
- 生成内容受Tripo模型版权约束，商用前须确认 [Tripo-3D模型生成](https://help.aliyun.com/zh/model-studio/tripo-3d-generation-api-reference) 官方许可条款。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)



