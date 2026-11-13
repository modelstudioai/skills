# video generation api

百炼平台的 video generation api 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。开发者可通过统一 API 接口调用不同底层模型，无需单独对接各模型服务。所有视频生成接口均基于 RESTful 设计，支持同步返回或[异步任务](../concepts/asynchronous-task.md)轮询。

## 支持的模型/功能

当前支持以下视频生成模型及对应能力：

- **HappyHorse**：支持高帧率（最高60fps）、长时长（最长8秒）文生视频，适用于动态场景生成  
- **万相**：专注中文语义理解的文生视频模型，对古风、国潮类提示词优化明显  
- **人像驱动**：输入单张人像图 + 驱动音频/文本，生成口型与表情同步的说话视频  
- **爱诗（PixVerse）**：支持 SDXL 兼容提示词，强调艺术风格控制与运镜效果  
- **可灵（Kling）**：支持 1080p 分辨率输出，具备物理运动建模能力  
- **Vidu**：百度研发模型，支持多镜头分镜生成（需指定 `scene_breaks` 参数）  
- **MiniMax**：提供轻量级 SDK 封装，适合移动端集成  

> **注意**：[原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的 MiniMax 模块在 v2.3.0 版本后已迁移至独立域名 `api.minimax.video`，旧版 `model-api-reference/video-generation-api/minimax-video-api-reference.md` 文档未同步更新，实际调用请参考 [原文标题](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md) 的最新修订注释。

## 关键参数

所有视频生成接口共用以下核心参数（部分模型支持扩展字段）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"kling"`, `"wanxiang"`, `"portrait-animation"` —— 必须与 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的名称严格一致 |
| `input` | object | 是 | 输入内容，结构因模型而异：文生视频为 `{"prompt": "..."}`；人像驱动为 `{"image_url": "...", "audio_url": "..."}` 等 |
| `parameters` | object | 否 | 模型特有参数，如 `width`, `height`, `duration`, `fps`, `seed` 等，详见各子模型文档 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation`  
3. **响应处理**：  
   - 成功时返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}` 获取结果（最长等待 5 分钟）  
   - 视频文件通过 `output.video_url` 字段返回，有效期 24 小时  
   - 错误码参考通用 AIGC 错误规范（如 `InvalidParameter`, `QuotaExceeded`）

## 限制和注意事项

- 单次请求最大输入图像尺寸为 1024×1024（人像驱动模型），文生视频提示词长度上限 512 字符  
- 所有模型默认输出格式为 MP4（H.264 编码），不支持自定义容器或编码器  
- [异步任务](../concepts/asynchronous-task.md)超时时间为 300 秒，超时后任务状态置为 `failed`，错误信息中会包含具体超时原因  
- 人像驱动模型要求输入人像图必须为正面清晰人脸（遮挡率 < 20%），否则生成质量显著下降  

> **注意**：[原文标题](../../raw/model-api-reference/video-generation-api.md) 中提及的 “Vidu 支持 4K 输出” 为历史版本描述，当前生产环境仅开放 1080p，4K 能力处于灰度阶段，需单独申请白名单权限。

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


