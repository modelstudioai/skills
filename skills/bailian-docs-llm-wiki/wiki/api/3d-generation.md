# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的API能力，当前仅支持Tripo模型，适用于快速原型设计、游戏资产生成等场景。该能力为异步接口，需轮询获取生成结果。所有请求均需通过`/v1/3d/generation`端点发起。

## 支持的模型/功能

- 当前**唯一支持的模型为 Tripo**，详见 [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)  
- 支持两种输入模式：纯文本描述（text-to-3D）和单张参考图+可选文本提示（image-to-3D）  
- 输出格式为 `.glb`（GL Transmission Format），兼容主流渲染引擎与WebGL查看器  
- 不支持多视角图、视频、点云或网格编辑等高级3D操作——该限制在 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中明确说明

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 包含 `text`（string）或 `image_url`（string）字段；二者不可同时为空，但可共存 |
| `image_url` | string | 否 | 公开可访问的JPEG/PNG图片URL，尺寸建议 ≥512×512，宽高比应接近1:1 |
| `text` | string | 否 | 中英文描述，长度 ≤200 字符；若仅传`image_url`，模型将自动理解图像内容 |
| `callback_url` | string | 否 | 异步完成后的HTTP回调地址（需支持POST，带`X-Event-Type: generation.completed`头） |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 未声明`callback_url`的鉴权要求，但实际调用中该URL必须能被百炼服务端公网访问且返回2xx状态码，否则回调失败且无重试机制。

## 使用方式

1. 发送 `POST /v1/3d/generation` 请求，携带JSON body（含`input`等参数）  
2. 接收响应中的 `task_id`（字符串），用于后续轮询或回调验证  
3. 轮询 `GET /v1/3d/generation/{task_id}` 获取状态（`pending`/`success`/`failed`）；成功时返回`result.glb_url`（有效期24小时）  
4. 下载GLB文件并校验SHA256（响应中提供`result.file_hash`）  

完整请求示例与错误码说明见 [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)。

## 限制和注意事项

- 单次请求最大等待时间：180秒；超时后任务自动终止，状态为`failed`  
- 每个`task_id`最多轮询50次，建议间隔≥2秒  
- 输入图像禁止包含人脸、身份证件、水印或受版权保护的3D资产；违反将导致`failed`且不计费返还  
- GLB文件默认为简化拓扑（约5k–50k面片），如需更高精度，需联系技术支持开通白名单——此能力尚未在公开文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 中披露，属内部灰度功能

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


