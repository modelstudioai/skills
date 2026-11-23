# video generation api

百炼平台的 Video Generation API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，由 HappyHorse、万相（WanX）、爱诗（PixVerse）、可灵（Kling）、Vidu、MiniMax 等多个模型系列支持。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生成时长 3–30 秒、分辨率最高达 4K 的高质量视频。开发者需严格保证模型、Endpoint URL 与 API Key 同地域部署。

## 支持的模型/功能

当前平台提供以下主流视频生成能力：

- **文生视频（Text-to-Video）**：输入文本提示词生成视频，如 `wan2.7-text2video`、`pixverse/pixverse-v6-max-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v4-video-generation`。
- **图生视频（Image-to-Video）**：
  - 基于首帧：如 `happyhorse-text-to-video-api-reference`、`wan2.7-image-to-video`、`pixverse/pixverse-v6-max-it2v`；
  - 基于首尾帧：如 `wan2.2-first-and-last-frame`、`vidu/viduq3-pro_start-end2video`、`pixverse/pixverse-c1-kf2v`；
  - 视频特效模式（仅限万相旧版）：通过 `template` 参数指定预设动态效果，详见 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。
- **参考生视频（Reference-to-Video）**：支持多图/视频/音频输入，融合角色与场景，如 `happyhorse-reference-to-video-api-reference`、`wan2.7-video-to-video`、`pixverse/pixverse-v6-r2v-omni`、`vidu/viduq3-ad_reference2video`。
- **视频编辑类**：
  - 视频编辑（指令驱动）：如 `wan2.7-videoedit`、`kling/kling-v4-omni-reference-video-generation`；
  - 视频对口型（Lip-sync）：如 `pixverse/pixverse-lipsync`；
  - 动作模仿：如 `pixverse/pixverse-motioncontrol`；
  - 视频超清：如 `pixverse/pixverse-upscale`；
  - 风格重绘：如 `video-style-transform`；
  - 视频换人/图生动作：如 `wan2.2-animate-mix`、`wan2.2-animate-move`；
  - 数字人驱动：如 `wan2.2-s2v`（需先调用 `wan2.2-s2v-detect` 图像检测）。

> **注意**：万相 2.7 及以上版本已统一协议，而万相 2.1–2.6 系列（如 `wanx2.1-i2v-turbo`）使用旧版接口路径 `/api/v1/services/aigc/image2video/...`，与新版 `/api/v1/services/aigc/video-generation/...` 不兼容。实际调用前请确认模型版本与文档匹配，参见 [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。

## 关键参数

所有视频生成请求均需以下通用参数：

- **请求头（Headers）**：
  - `Content-Type: application/json`（必选）；
  - `Authorization: Bearer <API_KEY>`（必选，除部分纯前端或特定模型外）；
  - `X-DashScope-Async: enable`（**必选**，所有 HTTP 调用均强制异步；缺失将报错 `"current user api does not support synchronous calls"`）。

- **请求体（Body）**：
  - `model`（必选）：模型全名，如 `wan2.7-text2video`、`pixverse/pixverse-v6-max-t2v`、`vidu/viduq3-pro_text2video`；
  - `input`（必选）：结构化输入对象，内容依模型类型而异：
    - 文生视频：`{ "prompt": "..." }`；
    - 图生视频：`{ "img_url": "...", "prompt": "..." }` 或 `{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`；
    - 参考生视频：`{ "reference_images": [...], "prompt": "..." }`；
    - 视频编辑/对口型等：`{ "media": [{ "type": "video_url", "url": "..." }, ...] }`；
  - `parameters`（可选）：控制输出规格，常见字段包括：
    - `resolution`（如 `"720P"`、`"1080P"`、`"4k"`）；
    - `style`（风格重绘中为整数索引）；
    - `video_fps`（帧率，默认 15–30）；
    - `template`（万相特效专用，如 `"flying"`）。

## 使用方式

1. **准备环境**：  
   - 开通对应模型服务（如在[模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通）；  
   - 获取所属地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并配置至环境变量 `DASHSCOPE_API_KEY`；  
   - 获取业务空间 ID（WorkspaceId），见[业务空间详情页](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

2. **发起异步任务**：  
   向对应地域 Endpoint 发送 `POST` 请求（示例为北京）：  
   ```bash
   curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "X-DashScope-Async: enable" \
     -d '{
           "model": "wan2.7-text2video",
           "input": { "prompt": "一只橘猫在秋日公园奔跑" }
         }'
   ```  
   成功响应返回 `task_id`（有效期 24 小时）。

3. **轮询获取结果**：  
   使用 `task_id` 向任务查询接口轮询（URL 格式：`https://{WorkspaceId}.<region>.maas.aliyuncs.com/api/v1/tasks/{task_id}`），直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：数字人 `wan2.2-s2v` 和视频换人 `wan2.2-animate-mix` 等部分模型使用 `/api/v1/services/aigc/image2video/...` 路径，而非 `/video-generation/...`，且必须使用华北2（北京）专属域名（不支持 WorkspaceId 形式）。详见 [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint URL 与 API Key **必须同属一个地域**（如北京、新加坡、东京等），跨地域调用必然失败。业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）为推荐方案，旧域名（`dashscope.aliyuncs.com`）仍可用但性能较低。
- **异步时效性**：任务最长等待时间约 5–10 分钟（万相 2.1 编辑模型可达 10 分钟），`task_id` 有效期固定为 24 小时。
- **输入约束**：
  - 图片/视频 URL 必须公网可访问，含中文字符需 URL 编码；
  - 本地文件需先调用 [临时文件上传接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 获取有效 URL；
  - OSS 链接（`oss://`）需额外添加请求头 `X-DashScope-OssResourceResolve: enable`。
- **模型兼容性**：  
  - `X-DashScope-Async: enable` 为所有视频 API 的硬性要求，无例外；  
  - 万相 2.7+ 与 HappyHorse/PixVerse/Kling/Vidu 等新模型统一使用 `/video-generation/video-synthesis` 路径；  
  - 万相 2.1–2.6、数字人、视频换人、图生动作等旧模型使用 `/image2video/...` 路径，且部分仅支持北京地域。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
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
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)


