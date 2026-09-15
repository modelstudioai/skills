# 3d generation

百炼平台提供基于文本或图像输入的3D模型生成能力，支持快速产出可用于渲染、AR/VR或下游3D编辑的网格模型。当前能力由Tripo系列模型提供，通过统一API接口调用，适用于原型设计、游戏资产生成等技术场景。详细接口定义与行为规范请参考 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 支持的模型/功能

- 当前仅支持 `tripo-1.0` 模型（对应 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档），暂不支持多模态输入（如图+文联合提示）或可控拓扑生成。
- 功能包括：文本到3D（text-to-3D）、单张图像到3D（image-to-3D），输出为 `.glb` 格式网格文件（含基础材质与UV）。
- 不支持点云、体素或SDF等中间表示输出；所有生成结果均为三角面片网格。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是 | 中文或英文描述性文本，建议≤100字符；避免模糊词（如“精美”“高质量”）；[3D模型生成](../../raw/model-api-reference/3d-generation.md) 明确要求首句需为对象主体描述（如“一只陶瓷猫”）。 |
| `input_image` | string (base64 或 URL) | 否 | 仅 image-to-3D 场景使用；图像需为正向清晰物体照，背景简洁；宽高比建议 1:1，分辨率不低于 512×512。 |
| `output_format` | string | 否 | 默认 `"glb"`；暂不支持 `"obj"` 或 `"stl"`（参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)）。 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中提及“支持 `seed` 参数控制随机性”，但实测及 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 均未声明该字段，当前API忽略 `seed`，视为不支持确定性生成。

## 使用方式

1. 调用 `/v1/models/tripo-1.0/generate` POST 接口；
2. 请求体为 JSON，包含 `prompt`（或 `input_image`）及其他可选参数；
3. 响应中 `result.url` 指向临时可下载的 `.glb` 文件（有效期 24 小时）；
4. 完整请求示例与错误码说明详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- 单次请求最大超时 300 秒；生成耗时通常为 60–180 秒，复杂提示可能失败；
- 输入文本禁止含政治、暴力、成人内容；图像禁止含人脸或可识别个人信息（违反将触发静默拒绝）；
- 输出模型无物理属性（如质量、碰撞体），不可直接用于Unity/Unreal物理模拟；
- 免费试用额度限 5 次/日；商用需开通对应模型配额。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


