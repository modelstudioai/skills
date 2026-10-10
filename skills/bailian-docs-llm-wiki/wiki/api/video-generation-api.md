# video generation api

百炼平台的 Video Generation API 提供多模态视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步等核心场景。所有模型均采用统一异步调用范式，通过任务创建 + 轮询获取结果两步完成，适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同技术路线与业务需求：

- **HappyHorse**：专注物理真实感与运动流畅性，提供[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[HappyHorse-图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[HappyHorse-参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)及[HappyHorse-视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四大能力。
- **万相（WanX）**：全栈式视频生成平台，3.0版本为All-in-One统一模型；2.7版本明确区分图生/文生/参考生/编辑四类API；早期2.1–2.6版本仍可使用但功能受限。注意：[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)明确推荐优先选用wan2.7，因其支持首帧、首尾帧、视频续写三大任务，而旧版仅支持首帧。
- **爱诗（PixVerse）**：强动态表现力，支持文生、图生（首帧/首尾帧）、参考生、动作模仿、对口型、超清、视频编辑等细分能力，各子模型命名清晰（如`pixverse/pixverse-c1-it2v`表示c1系列首帧生视频）。
- **Vidu / 可灵（Kling） / MiniMax**：分别提供差异化能力矩阵，如Vidu强调广告与剧集场景优化，可灵支持主体ID复用（见[可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)），MiniMax支持尾帧输入等扩展模态。

> **注意**：文档中存在模型路径不一致问题。例如，万相2.2-s2v数字人模型的请求Endpoint为`/api/v1/services/aigc/image2video/video-synthesis`（见[数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)）），而其他主流视频模型（如HappyHorse、wan2.7、PixVerse）均使用`/api/v1/services/aigc/video-generation/video-synthesis`。开发者需严格按模型文档指定路径调用，不可混用。

## 关键参数

所有视频生成API共用以下核心参数结构：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API Key>`，Key需与模型所在地域匹配
  - `X-DashScope-Async`: 必须为 `enable`，缺失将报错“current user api does not [support](../guides/support.md) synchronous calls”

- **请求体（Request Body）**
  - `model`: 字符串，模型唯一标识（如 `wan2.7-t2v`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`）。选型需结合场景（如打斗特效选c1，通用选v6）和输出要求（分辨率、时长）。
  - `input`: 对象，内容依模型能力而异：
    - 文生视频：`prompt`（必填，UTF-8字符数限制因模型而异，Vidu上限5000，MiniMax上限7000）
    - 图生视频：`img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）
    - 参考生视频：`media`数组，含`image_url`/`video_url`/`audio_url`等类型元素
    - 视频编辑/动作迁移：需同时传入目标视频与参考素材
  - `parameters`: 可选对象，常见字段包括：
    - `resolution`: 如 `"720P"`, `"1080P"`, `"4k"`
    - `style`: 风格ID（如视频风格重绘API中`style: 0`代表日式漫画）
    - `video_fps`: 帧率（15–25）
    - `animate_emotion`: 是否优化面部表情（布尔值）

## 使用方式

API采用标准异步模式，分两步完成：

1. **创建任务**  
   向对应地域Endpoint发送`POST /api/v1/services/aigc/video-generation/video-synthesis`（数字人s2v等少数模型除外，见上文注意项），携带完整请求头与Body。成功响应返回JSON，含`task_id`（字符串）和`output.task_status`（通常为`QUEUED`或`RUNNING`）。`task_id`有效期24小时，**严禁重复提交相同请求**。

2. **轮询获取结果**  
   使用`GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`（具体URL格式见各模型文档）定期查询。建议初始间隔1s，后续逐步延长至5–10s。当`task_status`变为`SUCCESS`时，响应中`output.video_url`即为生成视频的直链（HTTPS，有效期通常24h）；若为`FAILED`，`output.error_code`与`output.error_message`提供失败原因。

> **注意**：业务空间专属域名已全面推广。[HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)等多篇文档强调，华北2（北京）与新加坡地域应优先使用`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`格式，而非旧版`https://dashscope.aliyuncs.com`，以获得更高性能与稳定性。现有域名虽兼容，但新项目务必迁移。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL、API Key三者必须属于同一地域（如华北2），跨地域调用必然失败。控制台开通模型时需确认地域，API Key也需在对应地域控制台生成。
- **输入文件约束**：所有媒体URL必须为公网可访问的HTTP/HTTPS链接；本地文件需先调用[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)接口转换；OSS链接需额外添加请求头`X-DashScope-OssResourceResolve: enable`。
- **计费与限流**：多数模型按秒计费（如数字人wan2.2-s2v为0.5元/秒），且存在RPS（每秒请求数）与并发任务数限制（如VideoRetalk同时仅1个任务运行）。详细规格见各模型文档的“资费与限流”章节。
- **任务生命周期**：`task_id`有效期24小时，超时未查询则失效；生成视频URL有效期通常也为24小时，需及时下载或转存。
- **错误处理**：除网络超时外，常见错误包括`task_status: FAILED`（模型内部失败）、`401 Unauthorized`（API Key无效或地域不匹配）、`400 Bad Request`（参数缺失或格式错误，如`X-DashScope-Async`未设为`enable`）。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
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
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


