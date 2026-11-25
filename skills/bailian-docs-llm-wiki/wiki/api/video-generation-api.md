# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、对口型、动作模仿、超清增强等核心场景。所有模型均采用统一异步调用范式（创建任务 → 轮询获取），适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同能力边界与演进阶段：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：支持全栈视频能力，包括 3.0 版本（All-in-One，统一接口支持文/图/参考/编辑）、2.7 版本（多模态输入升级）及早期 2.1–2.6 版本（功能分立）。需注意：[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确推荐优先选用 wan2.7 替代旧版。
- **爱诗（PixVerse）**：提供文生视频、首帧/首尾帧生视频、参考生视频、对口型、动作模仿、视频超清六类能力，全部面向华北2（北京）地域 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **可灵（Kling）与 Vidu**：Kling 支持 v3/v4 多代模型，v4 系列新增关键帧（首/中/尾）任意组合与官方主体库；Vidu 则聚焦文生、首帧、首尾帧、参考生四类标准能力。

> **注意**：部分模型存在路径不一致问题。例如，万相2.2-animate-move（图生动作）和 videoretalk（口型替换）等专用模型使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而绝大多数通用视频生成模型（如 HappyHorse、wan3、pixverse、vidu）均使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者需严格按模型文档选择 endpoint，不可混用。

## 关键参数

所有视频生成 API 均遵循统一请求结构，核心参数如下：

- **请求头（Headers）**：
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选，需与模型地域匹配）
  - `X-DashScope-Async: enable`（必选，异步模式强制启用）

- **请求体（Body）**：
  - `model`: 字符串，指定模型标识（如 `"happyhorse-text-to-video"`、`"wan3"`、`"pixverse-text-to-video"`、`"kling/kling-v4-omni-reference-video-generation"`）
  - `input`: 对象，根据任务类型动态变化：
    - 文生视频：`{"prompt": "描述文本"}`
    - 图生视频（首帧）：`{"image_url": "...", "prompt": "..."}`  
    - 图生视频（首尾帧）：`{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`  
    - 参考生视频：`{"reference_urls": ["..."], "prompt": "..."}`（支持图片或视频 URL 数组）
  - `parameters`: 可选对象，用于控制输出（如 `{"aspect_ratio": "16:9", "duration": 5}`）

- **地域与 WorkspaceId**：所有 endpoint URL 中的 `{WorkspaceId}` 必须替换为实际业务空间 ID，且该空间、模型、API Key 必须同属一个地域（如华北2（北京）或新加坡）。

## 使用方式

API 采用标准两步异步流程：

1. **创建任务**：发送 `POST` 请求至对应地域的 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），携带完整请求体。成功后返回 JSON，含 `task_id` 字段。
2. **轮询结果**：使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 定期查询（建议间隔 ≥5 秒），直至 `status` 变为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频直链。

> **注意**：`task_id` 有效期为 24 小时，且**严禁重复提交相同任务**。轮询是唯一获取结果的方式，同步调用不被支持。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须严格同地域（如北京模型 + 北京 URL + 北京 API Key），跨地域调用必然失败，此规则在 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 等多篇文档中反复强调。
- **域名迁移建议**：华北2（北京）与新加坡地域已启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`，强烈建议迁移。
- **输入文件要求**：图像/视频/音频需通过公网 HTTP(S) URL 或阿里云临时存储 OSS URL（需额外添加 `X-DashScope-OssResourceResolve: enable` 请求头）传入，不支持本地路径。
- **时效性**：单任务处理时间通常为 1–5 分钟（部分复杂任务如视频编辑可达 10 分钟），请合理设计客户端超时与重试逻辑。
- **模型兼容性**：万相系列存在明确版本迭代关系。例如，[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 指出其支持“首帧/首尾帧/视频续写”三大任务，而旧版仅支持首帧，开发者应优先选用新版协议。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)


