# image generation

百炼平台提供多种图像生成模型与工具，支持文生图、图生图、图像编辑等任务，适用于不同精度、风格和性能需求的场景。所有图像生成能力均通过统一 API 接口调用，开发者可按需选择模型并配置参数。详细模型能力与接口规范请参考 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)。

## 支持的模型/功能

当前支持以下图像生成模型与功能模块：
- **基础文生图模型**：千问（Qwen-VL 系列图像生成能力）、万相（WanX）、Z-Image、可灵（Kling）、Vidu  
- **创意工具集**：包括图像扩图、局部重绘、风格迁移、分辨率增强等图像编辑能力，详见 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)  
- **[多模态](../concepts/multi-modal.md)协同**：部分模型（如千问）支持图文混合输入，实现条件化生成；万相与 Z-Image 侧重高保真商业级出图，而可灵与 Vidu 更适合动态构图与视频帧级一致性生成  

> **注意**：Vidu 当前仅支持视频生成，其静态图像生成能力已下线；实际调用图像生成接口时，请勿指定 `model=vidu`，该信息与 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md) 中的模型列表存在不一致，以 API 文档最新枚举值为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx`, `zimage`, `kling`；不支持 `vidu` 图像模式 |
| `prompt` | string | 是 | 中文或英文提示词，建议长度 ≤ 500 字符，避免歧义描述 |
| `size` | string | 否 | 输出尺寸，格式为 `WxH`，如 `"1024x1024"`；各模型支持范围不同，详见对应模型文档 |
| `n` | integer | 否 | 生成图片数量，默认为 1，最大为 4 |
| `seed` | integer | 否 | 随机种子，用于结果复现（部分模型支持） |

## 使用方式

1. 调用 `/v1/images/generations` POST 接口  
2. 在请求体中传入 JSON 格式参数（含 `model`, `prompt` 等）  
3. 设置 `Authorization: Bearer <api_key>` 请求头  
4. 解析响应中的 `data[0].url` 获取图片直链（有效期 1 小时）  

完整请求示例与错误码说明见 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)。

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 500 字符；超长将被截断且不报错  
- 所有生成图片默认禁止包含人脸（含模糊/抽象人脸），如需合规人脸生成，须单独申请白名单权限  
- 免费调用量受账户等级限制；生产环境请配置配额告警与降级逻辑  
- 图像版权归属用户，但不得用于训练其他模型或反向工程  
- 模型输出可能受内容安全策略拦截，返回 `error.code = "content_blocked"` 时需检查 [prompt](../guides/prompt.md) 合规性

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


