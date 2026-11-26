# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等核心场景。所有模型均采用统一异步调用范式（创建任务 → 轮询获取），适用于生产环境集成。

## 支持的模型/功能

当前平台提供三大主力视频模型家族及多个垂直能力模型：

- **HappyHorse**：专注高保真物理运动建模，支持[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[HappyHorse-图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[HappyHorse-参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[HappyHorse-视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。
- **万相（WanX）**：All-in-One 多模态视频模型，3.0 版本统一支持文生、图生（首帧/首尾帧/续写）、参考生、编辑等全链路能力；2.7 版本为推荐稳定版，明确区分新版协议；早期 2.1–2.6 版本已归档为[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)，不建议新项目接入。
- **爱诗（PixVerse）**、**可灵（Kling）**、**Vidu**、**MiniMax**：各具特色的第三方合作模型，均支持文生视频与图生视频基础能力，并在关键帧控制、主体库、音色库等维度有差异化设计（如[Kling-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)提供预置 `element_id`）。

> **注意**：万相2.7系列文档明确指出其图生视频API支持“首帧生视频、首尾帧生视频、视频续写”三大任务，而[万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)仅支持首帧生视频，二者能力范围存在显著差异，应以2.7+版本为准。

## 关键参数

所有视频生成 API 均遵循统一请求结构，核心参数如下：

- **`model`**（必填，string）：模型标识符，例如 `"wanx-v3"`、`"kling/kling-v4-omni-reference-video-generation"`、`"vidu"`。必须与所选地域开通的模型完全一致。
- **`input`**（必填，object）：输入数据容器，结构因模型类型而异：
  - 文生视频：`{"prompt": "描述文本"}`
  - 图生视频（首帧）：`{"image_url": "https://...", "prompt": "描述文本"}`
  - 图生视频（首尾帧）：`{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`（部分模型如Vidu、PixVerse支持）
  - 参考生视频：`{"reference_images": ["url1", "url2"], "prompt": "..."}` 或 `{"reference_video_url": "..."}`（依模型而定）
- **`parameters`**（可选，object）：控制生成细节，常见字段包括：
  - `size`：输出分辨率，如 `"720p"`、`"1080p"`、`"4k"`（Kling v4 不支持 4k）
  - `aspect_ratio`：宽高比，如 `"16:9"`、`"9:16"`、`"1:1"`
  - `duration`：视频时长（秒），多数模型支持 `3–15` 秒，Kling v4/v4-omni 支持 `3–30` 秒
  - `template`：仅限特定模型（如万相早期图生视频）的特效模板，详见[万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)

- **请求头（Headers）**（必填）：
  - `Content-Type: application/json`
  - `Authorization: Bearer ${DASHSCOPE_API_KEY}`
  - `X-DashScope-Async: enable`（**必须显式设置，否则报错**）

## 使用方式

API 采用标准异步模式，分两步完成：

1. **创建任务**：向对应地域的 Endpoint 发送 `POST` 请求。
   - 统一路径：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
     - `{WorkspaceId}`：业务空间 ID（控制台查看）
     - `{region}`：地域代码，如 `cn-beijing`、`ap-southeast-1`、`us-east-1` 等
   - > **注意**：部分模型（如万相数字人 `wan2.2-s2v`、声动人像 `videoretalk`、视频风格重绘）使用 `/api/v1/services/aigc/image2video/...` 路径，与主流 `/video-generation/` 路径不一致，需严格按对应文档调用。

2. **轮询结果**：使用返回的 `task_id`，向 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status == "SUCCESS"`，响应体中 `output.video_url` 即为生成视频直链。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL 和 API Key **必须属于同一地域**，跨地域调用必然失败。所有文档均强调此约束，是首要排查点。
- **域名迁移建议**：华北2（北京）和新加坡地域已启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`，强烈建议迁移。
- **时效性**：`task_id` 有效期为 **24 小时**，超时后无法查询结果，需重新提交任务。
- **输入文件要求**：
  - 所有图片/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；
  - 本地文件需先通过[临时存储空间](../../preparations/get-temporary-file-url.md)上传并获取 URL；
  - 若使用 `oss://` URL，请求头必须添加 `X-DashScope-OssResourceResolve: enable`（见[VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)）。
- **计费与配额**：不同模型计费模式不同（如 VideoRetalk 按秒后付费，万相部分模型含免费额度），具体请查阅各模型文档的“资费与限流”章节。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
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
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)


