# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘等核心能力。所有视频生成类 API 均采用统一[异步调用](../concepts/asynchronous-invocation.md)范式：先创建任务获取 `task_id`，再轮询查询结果，任务有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同技术路线与业务场景：

- **HappyHorse**：专注物理真实感与运动流畅性，提供[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[HappyHorse-图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[HappyHorse-参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)及[HappyHorse-视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类能力。
- **万相（WanX）**：提供全栈式视频生成能力，包含万相2.7（推荐）、万相3.0（All-in-One）及早期版本（2.1–2.6）。其中万相3.0统一支持文生、图生（首帧/首尾帧）、参考生视频等多种输入模式；万相2.7则按任务类型细分为独立 API；而早期模型（如万相2.2-animate-move、wan2.2-s2v）聚焦垂直场景如图生动作、数字人驱动等。
- **爱诗（PixVerse）**：强调多模态融合与可控性，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、视频动作模仿、视频超清等细分能力，各能力对应专用模型标识（如 `pixverse/pixverse-lipsync`）。
- **Vidu / 可灵 / MiniMax / VideoRetalk / 视频风格重绘**：Vidu 和可灵均支持文生、图生（首帧/首尾帧）、参考生视频及视频编辑；MiniMax 支持多模态参考生视频；VideoRetalk 专精于视频口型替换；视频风格重绘则提供 8 种预设艺术风格转换。

> **注意**：万相2.7系列文档明确标注“此接口为新版协议”，而[万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)等旧版文档则注明“此接口为旧版协议”。二者在请求体结构、参数命名（如 `input.prompt` vs `prompt`）及模型兼容性上存在不兼容差异，**强烈建议新项目优先选用万相2.7或万相3.0系列**。

## 关键参数

所有视频生成 API 的通用关键参数如下（具体字段依模型略有差异）：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API_KEY>`，值来自对应地域的 API Key
  - `X-DashScope-Async`: **必须设置为 `enable`**，缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”

- **请求体（Request Body）**
  - `model`: 字符串，必选。指定具体模型名称，例如：
    - HappyHorse: `happyhorse/happyhorse-t2v`
    - 万相3.0: `kling/kling-v3-omni-video-generation`
    - 爱诗文生视频: `pixverse/pixverse-v6-t2v`
    - Vidu参考生视频: `vidu/viduq3-mix_reference2video`
    - 视频风格重绘: `video-style-transform`
  - `input`: 对象，必选。内容因模型而异：
    - 文生视频：`{ "prompt": "描述文本" }`
    - 图生视频（首帧）：`{ "img_url": "https://...", "prompt": "..." }`
    - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`
    - 参考生视频：`{ "reference_urls": ["https://..."], "prompt": "..." }`
    - 口型替换：`{ "media": [{ "type": "video_url", "url": "..." }, { "type": "audio_url", "url": "..." }] }`
  - `parameters`: 对象，可选。用于控制输出规格，常见字段：
    - `resolution`: 如 `"720P"`、`"1080P"`、`"4K"` 或 `"480P"`
    - `style`: 风格重绘中为整数（0–7），Vidu 中可能为字符串
    - `fps`: 帧率，如 `15`, `30`
    - `aspect_ratio`: 宽高比，如 `"16:9"`, `"9:16"`

## 使用方式

所有视频生成 API 均遵循标准异步两步流程：

### 步骤1：创建任务
向对应地域的 Endpoint 发起 `POST` 请求：
```
POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```
其中 `{WorkspaceId}` 为业务空间 ID（控制台查看），`{region}` 如 `cn-beijing`、`ap-southeast-1`。请求体包含 `model`、`input` 等必要参数。成功响应返回 JSON，含 `task_id` 字段。

### 步骤2：轮询获取结果
使用上一步获得的 `task_id`，向任务查询接口发起 `GET` 请求：
```
GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}
```
轮询间隔建议 ≥3 秒。当响应中 `status` 为 `"SUCCESS"` 时，`output.video_url` 即为生成视频的直链；若为 `"FAILED"`，则 `output.error` 提供失败原因。

> **注意**：部分模型（如[数字人wan2.2-s2v](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)）要求前置图像检测（`wan2.2-s2v-detect`），且仅限华北2（北京）地域；而[视频风格重绘](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)的初始请求 URL 仍为 `https://dashscope.aliyuncs.com/...`，未强制要求业务空间专属域名，与其他模型不一致。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint URL、API Key **必须同属一个地域**（如华北2北京），混用将导致鉴权失败或服务报错。各文档均反复强调此前提，例如[HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)明确指出“跨地域调用将会失败”。
- **异步强制要求**：所有视频生成 API **仅支持[异步调用](../concepts/asynchronous-invocation.md)**，`X-DashScope-Async: enable` 为硬性要求，同步调用必然失败。
- **任务生命周期**：`task_id` 有效期为 **24 小时**，超时后无法查询结果，接口返回 `UNKNOWN` 状态。
- **输入资源要求**：
  - 图片/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；
  - 本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口；
  - 若使用 OSS 临时 URL（`oss://`），请求头必须添加 `X-DashScope-OssResourceResolve: enable`，否则报错 `No connection adapters were found for 'oss://...'`。
- **模型选型指引**：
  - 动态复杂场景（打斗、法术）：爱诗推荐 `c1` 系列模型；
  - 广告生成：Vidu 推荐 `viduq3-ad_reference2video`；
  - 剧情向内容：Vidu 推荐 `viduq3-drama_reference2video`；
  - 全能型首选：万相3.0（`kling-v3-omni-video-generation`）或 HappyHorse 新版。
- **计费与限流**：部分模型（如 VideoRetalk）有明确 RPS 限制（如 1 QPS）和并发任务数限制（如同时处理中任务数量为 1），详见各模型资费文档。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
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
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)


