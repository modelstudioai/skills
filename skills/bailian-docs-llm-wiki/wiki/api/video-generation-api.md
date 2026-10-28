# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑及风格化等核心能力。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。开发者需确保模型、Endpoint URL 与 API Key 严格同地域部署。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同精度、时长与多模态能力需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑四类任务。
- **万相（WanX）**：全场景覆盖型模型家族，其中 **万相3.0** 为 All-in-One 统一模型，原生支持文生、图生（首帧/首尾帧）、参考生视频及视频编辑；**万相2.7** 系列则按能力拆分为独立 API（如 `wan2.7-videoedit`），推荐优先选用 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。
- **爱诗（PixVerse）**：强动态表现力模型，支持文生、图生（首帧/首尾帧）、参考生视频、视频对口型、动作模仿、超清增强等细分能力，各子模型（如 `pixverse-v6-t2v`、`pixverse-lipsync`）需按场景精确选型。
- **可灵（Kling）、Vidu、MiniMax**：分别提供差异化能力矩阵，例如可灵 `kling-v3-omni-video-generation` 支持五合一任务，Vidu 提供广告级 `viduq3-ad_reference2video` 和剧集级 `viduq3-drama_reference2video` 模型，MiniMax 则支持尾帧驱动等特殊输入模式。

> **注意**：万相2.1–2.6 等早期模型（如 `wanx2.1-i2v-turbo`）已明确标记为旧版协议，文档中多次强调“推荐优先选用”万相2.7或3.0，且其 Endpoint 路径存在不一致（如文档16中部分旧版使用 `/api/v1/services/aigc/image2video/video-synthesis`，而新版统一为 `/api/v1/services/aigc/video-generation/video-synthesis`），实际调用应以新版路径为准。

## 关键参数

所有视频生成 API 共享以下核心参数规范：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API_KEY>`，需与模型地域匹配
  - `X-DashScope-Async`: 必须设置为 `enable`，缺失将报错 `"current user api does not support synchronous calls"`

- **请求体（Request Body）**
  - `model`: 字符串，必需。具体值依模型而定（如 `wan3-video-generation`、`vidu/viduq3-pro_text2video`、`pixverse/pixverse-c1-t2v`）
  - `input`: 对象，必需。结构因任务类型差异显著：
    - 文生视频：含 `prompt`（文本提示词，长度上限依模型而异，Vidu 为 5000 字符，MiniMax 为 7000 字符）
    - 图生视频：含 `img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧），部分模型（如万相2.7）支持 `template` 特效参数
    - 参考生视频：含 `media` 数组，可混合传入图片、视频、音频 URL
    - 视频编辑/风格化：含 `video_url` 及 `parameters.style`（如视频风格重绘 API 的 `style: 0` 表示日式漫画）

- **地域与 WorkspaceId**
  - 所有 HTTP 请求 URL 均需替换 `{WorkspaceId}` 为真实业务空间 ID，详见 [业务空间详情页面](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)
  - 地域列表完整覆盖北京、新加坡、东京、法兰克福、弗吉尼亚、中国香港等，但部分旧版文档（如文档16）仅列出北京/新加坡，新文档（如文档8）已补全全部六地

## 使用方式

标准调用流程为两步异步操作，耗时通常为 1–5 分钟：

1. **创建任务**  
   向对应地域的 Endpoint 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求，携带上述关键参数。成功后返回 JSON 响应，含唯一 `task_id`（有效期 24 小时）。

2. **轮询获取结果**  
   使用 `task_id` 向 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态。当 `status` 为 `SUCCESS` 时，响应中 `output.video_url` 即为生成视频的直链（HTTPS，有效期 24 小时）。

> **注意**：数字人 `wan2.2-s2v` 模型为特例，需先调用图像检测接口 `POST /api/v1/services/aigc/image2video/face-detect` 验证输入图片合规性，再提交生成任务，详见 [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint URL、API Key 必须属于同一地域，跨地域调用必然失败。文档中反复强调此要求（如文档2、文档4、文档6等），是首要排查点。
- **异步强制约束**：所有视频 API 仅支持异步，`X-DashScope-Async: enable` 为硬性要求，同步调用将直接报错。
- **输入资源要求**：
  - 图片/视频 URL 必须为公网可访问的 HTTPS/HTTP 链接；本地文件需先通过 [临时存储空间 API](raw/model-api-reference/more-about-models/get-temporary-file-url.md) 获取有效 URL
  - 视频格式支持 MP4/AVI/MOV 等主流封装，但 Vidu 首尾帧模型明确要求“单边尺寸不小于 256 像素”，而万相数字人模型要求图像分辨率在 [400, 7000] 像素区间
- **任务管理**：`task_id` 有效期严格为 24 小时，超时后无法查询；禁止重复创建相同任务，应复用已有 `task_id` 轮询。
- **模型演进策略**：万相、爱诗等系列持续迭代，旧版模型（如万相2.1–2.6、爱诗v5.6）虽仍可用，但文档明确建议升级至 v6 或更高版本以获得更优效果与功能支持。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


