# video generation api

百炼平台提供多种视频生成模型的 API 接口，统一采用[异步调用](../concepts/asynchronous-invocation.md)模式（创建任务 → 轮询获取结果），支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、风格重绘、口型替换、动作模仿、超分等多种能力。所有接口均需确保模型、Endpoint URL 与 API Key 严格同地域，且必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以保障稳定性与性能。

## 支持的模型/功能

当前主流视频生成模型包括：
- **万相（WanX）**：提供全系列能力，涵盖万相3.0（All-in-One 统一接口）、万相2.7（新版协议，支持首帧/首尾帧/视频续写/编辑）、以及早期 2.1–2.6 版本（旧版协议，部分已归档）。其中 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md) 是推荐首选，统一支持多输入模态与最长30秒输出。
- **HappyHorse**：专注高质量物理真实感视频，提供文生视频、图生视频（基于首帧）、参考生视频和视频编辑四类独立 API，全部基于新版协议。
- **爱诗（PixVerse）**：强调动态表现力，支持文生视频、首帧/首尾帧生视频、参考生视频、对口型、动作模仿、视频超清等细分能力，模型命名体现版本与场景（如 `pixverse/pixverse-c1-t2v`）。
- **可灵（Kling）**：支持文生/图生/参考生/视频编辑五合一的 `kling/kling-v3-omni-video-generation` 模型，并提供预设主体 ID（如雷电、魔法法阵）用于可控生成，详见 [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)。
- **Vidu**：面向专业内容生产，按能力分层提供 Turbo（快）、Pro（质）、Drama（剧）、Ad（广告）等模型变体，例如 `vidu/viduq3-drama_reference2video` 专精角色一致性与情绪表达。
- **MiniMax**：支持文生、首帧/尾帧/首尾帧生视频及多模态参考生视频，当前仅开放 `MiniMax/MiniMax-H3` 单一模型。
- **人像驱动类**：包括 VideoRetalk（口型替换）、视频风格重绘、数字人 wan2.2-s2v（需先调用图像检测 API）等垂直能力，均属独立服务线。

> **注意**：万相2.7系列（如 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)）与万相早期版本（2.1–2.6）存在协议不兼容。旧版文档中部分接口路径为 `/api/v1/services/aigc/image2video/video-synthesis`（如文档15、17、18、19），而新版统一为 `/api/v1/services/aigc/video-generation/video-synthesis`；混用将导致 404 或参数解析失败。

## 关键参数

所有视频生成 API 均需以下通用请求头：
- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，除 Vidu 文生视频文档39外，其余均明确要求；Vidu 文生视频文档39未列出 Authorization，但实际调用必需，属文档遗漏）
- `X-DashScope-Async: enable`（必选，缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：
- `model`（字符串，必选）：精确指定模型名称，如 `wanx3.0-video-generation`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video` 等，不同模型能力与输入格式强绑定。
- `input`（对象，必选）：结构因模型而异：
  - 文生视频：含 `prompt`（文本提示词，长度限制因模型而异，如 Vidu 限5000字符，MiniMax 限7000字符）。
  - 图生视频：含 `image_url`（首帧）或 `first_frame_url` + `last_frame_url`（首尾帧）。
  - 参考生视频：含 `reference_image_urls` 数组或 `video_url`。
  - 视频编辑/重绘：含 `video_url` 及指令性 `prompt` 或 `template`。
- `parameters`（对象，可选）：控制输出规格，常见字段包括：
  - `resolution`（如 `"720P"`、`"480P"`、`"4k"`）
  - `style`（风格重绘模型专用，整数索引）
  - `video_fps`（帧率，默认15–30）
  - `animate_emotion`（数字人模型专用）

> **注意**：[万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md) 明确指出：在特效模式下，`prompt` 字段会被忽略，必须通过 `template` 参数指定效果（如 `"flying"`、`"hanfu-1"`），且仅适用于 legacy 首帧/首尾帧模型，新版万相3.0 不支持该模式。

## 使用方式

1. **准备环境**：  
   - 在百炼控制台开通对应模型服务（如搜索 “PixVerse” 或 “Vidu” 并开通）；  
   - 获取并配置**同地域**的 API Key 到环境变量 `DASHSCOPE_API_KEY`；  
   - 在控制台业务空间详情页获取 `WorkspaceId`。

2. **构造请求**：  
   - 使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**禁用旧版 `dashscope.aliyuncs.com` 域名**（虽仍可用，但性能与稳定性无保障）；  
   - 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求，携带上述关键参数。

3. **轮询结果**：  
   - 成功响应返回 `task_id`（有效期24小时）；  
   - 轮询 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 获取状态（`IN_PROGRESS` / `SUCCESS` / `FAILED`）；  
   - `SUCCESS` 时，响应 `output.video_url` 为可下载的 MP4 地址。

4. **错误处理**：  
   - `401 Unauthorized`：检查 API Key 是否有效、是否与 Endpoint 同地域；  
   - `400 Bad Request`：校验 `model` 名称拼写、`input` 结构完整性（如 `prompt` 必填却为空）、`parameters` 取值范围；  
   - `429 Too Many Requests`：检查 RPS 限制（如 VideoRetalk 限1 QPS）。

## 限制和注意事项

- **地域强约束**：模型、API Key、Endpoint URL 必须完全同地域（如华北2北京），跨地域调用必然失败，此规则在所有文档（如文档1、2、3、5、7等）中反复强调。
- **异步强制性**：所有视频 API 仅支持异步，同步调用无效；`X-DashScope-Async: enable` 是硬性要求，非可选。
- **输入文件规范**：  
  - 图片：支持 JPG/PNG/WEBP/BMP，分辨率通常要求 400–7000px（如文档21）；  
  - 视频：MP4/AVI/MOV 等，时长 ≤30秒（多数模型），大小 ≤100MB（如文档25），需公网可访问 URL；  
  - 音频：WAV/MP3，时长 <20s（数字人）、<120s（VideoRetalk），需清晰人声（文档21、24）。
- **计费与配额**：  
  - VideoRetalk 按生成视频秒数计费（0.08元/秒），有1800秒免费额度（文档23）；  
  - 其他模型多按 token 或任务计费，具体见控制台定价页。
- **模型演进提示**：万相2.7+、爱诗、可灵、Vidu 均已迭代至新版协议，旧版（2.1–2.6）文档明确标注“推荐优先选用新版”，且部分旧版接口路径（如 `/image2video/`）已弃用，开发者应以新版文档为准。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


