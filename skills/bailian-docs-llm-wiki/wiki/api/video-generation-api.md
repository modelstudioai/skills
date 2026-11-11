# video generation api

百炼平台提供多种视频生成模型的统一 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑及专业场景（如数字人、口型替换、风格重绘等）共十余类能力。所有视频生成任务均采用异步调用模式，需通过“创建任务 → 轮询查询”两步完成，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域。

## 支持的模型/功能

当前主流视频生成模型按能力矩阵可分为三类：

- **全能型多模态模型**：  
  - `wan3`（万相3.0）支持文生、图生（首帧/首尾帧）、参考生视频一体化调用，最长生成 30 秒、30fps 视频 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；  
  - `kling/kling-v3-omni-video-generation`（可灵）覆盖文生、图生、参考生、视频编辑全链路；  
  - `vidu/viduq3-*` 系列（Vidu）提供广告、剧集、通用等细分参考生视频模型。

- **垂直场景专用模型**：  
  - 数字人：`wan2.2-s2v`（单图+音频生成说话/唱歌视频），需先调用 `wan2.2-s2v-detect` 图像合规检测 [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)；  
  - 口型替换：`videoretalk`（人物视频+音频驱动口型同步）、`pixverse/pixverse-lipsync`（爱诗对口型）；  
  - 动作迁移：`wan2.2-animate-move`（图生动作）、`pixverse/pixverse-motioncontrol`（爱诗动作模仿）；  
  - 风格重绘：`video-style-transform`（8种预设艺术风格）。

- **轻量/特效向模型**：  
  - 万相早期模型（2.1–2.6）支持视频特效模板（如 `flying`、`hanfu-1`），仅需首帧图像 + `template` 参数，无需提示词 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)；  
  - HappyHorse 系列（文生/图生/参考生/编辑）强调物理真实与运动流畅性。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相2.1–2.6早期模型（如 `wanx2.1-i2v-turbo`）使用不同协议和参数结构，不可混用；前者要求 `X-DashScope-Async: enable`，后者部分旧版接口（如 `legacy-image-to-video-by-first-and-last-frame-api-reference.md`）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，存在路径不一致风险。

## 关键参数

所有视频生成 API 均需以下**请求头（Headers）**：

- `Content-Type: application/json`（必选）  
- `Authorization: Bearer <API_KEY>`（必选，除部分纯前端调用场景外）  
- `X-DashScope-Async: enable`（**必选**，缺失将报错 `"current user api does not support synchronous calls"`）

**请求体（Request Body）核心字段**：

- `model`（string，必选）：模型标识符，如 `wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`；  
- `input`（object，必选）：根据模型类型结构化输入：  
  - 文生视频：`{ "prompt": "..." }`；  
  - 图生视频（首帧）：`{ "img_url": "https://...", "prompt": "..." }`；  
  - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`；  
  - 参考生视频：`{ "reference_urls": ["..."], "prompt": "..." }`；  
  - 数字人：`{ "image_url": "...", "audio_url": "..." }`；  
- `parameters`（object，可选）：控制输出规格，常见字段包括：  
  - `resolution`：`"480P"`/`"720P"`/`"1080P"`/`"4k"`；  
  - `style`：风格重绘模型中指定风格 ID（0–7）；  
  - `video_fps`：帧率（15–25）；  
  - `animate_emotion`：是否优化面部表情（布尔值）。

## 使用方式

1. **准备环境**：  
   - 在[百炼控制台](https://bailian.console.aliyun.com)开通对应模型服务；  
   - 获取所属地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并配置至环境变量 `DASHSCOPE_API_KEY`；  
   - 获取业务空间 ID（WorkspaceId），见[业务空间详情页](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

2. **创建任务（POST）**：  
   ```bash
   curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer sk-xxx' \
     -H 'X-DashScope-Async: enable' \
     -d '{
           "model": "wan2.7-videoedit",
           "input": { "prompt": "为人物换上酷闪的衣服" },
           "parameters": { "resolution": "720P" }
         }'
   ```
   成功响应返回 `{"task_id": "xxx"}`，有效期 24 小时。

3. **轮询结果（GET）**：  
   使用 `task_id` 查询：  
   ```bash
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
     -H 'Authorization: Bearer sk-xxx'
   ```
   当 `output.video_url` 字段非空且 `status` 为 `"SUCCESS"` 时，任务完成。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败，且不同地域的 API Key 不可复用；  
- **异步强制要求**：所有视频 API 仅支持异步，同步调用会返回明确错误；  
- **输入资源要求**：  
  - 图片/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 [临时URL上传接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；  
  - 若使用 OSS 临时链接（`oss://` 前缀），必须在请求头添加 `X-DashScope-OssResourceResolve: enable`，否则报错 `No connection adapters were found for 'oss://...'`；  
- **计费与配额**：  
  - 任务创建即计费（即使检测不通过，如 `wan2.2-s2v-detect`）；  
  - 免费额度详见各模型文档（如 `videoretalk` 提供 1800 秒免费额度）；  
- **模型兼容性**：  
  > **注意**：`HappyHorse` 和 `MiniMax` 模型目前**仅支持华北2（北京）地域**，其文档明确标注“仅适用于北京地域”，而 `wan3`、`Vidu` 等模型已支持新加坡、东京、法兰克福等多地域，开发者选型时需核对 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md) 中的 Endpoint 列表。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
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
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


