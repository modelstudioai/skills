# video generation api

百炼平台视频生成 API 提供统一的异步调用入口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、风格重绘及数字人/动作迁移等多模态任务。接口采用“创建任务获取 `task_id` -> 轮询获取结果”的标准异步模式，全面覆盖万相 (Wan)、HappyHorse、可灵 (Kling)、Vidu、PixVerse 等主流模型家族。

## 支持的模型与核心功能

平台将视频生成能力按任务类型划分为以下几类，开发者可根据业务场景按需选用：

* **文生视频 (T2V)**：仅通过文本提示词生成视频。主流模型如 `happyhorse-1.0-t2v`、`wan2.7-t2v-*`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`、`pixverse/*` 均支持此能力，部分模型内置多镜头叙事控制。详见 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)。
* **图生视频 (I2V)**：基于单张首帧或首尾帧图像生成平滑过渡视频。支持 `first_frame` 控制起始状态，部分模型（如 Vidu、Kling、PixVerse）支持 `last_frame` 约束结束状态。
* **参考生视频 (R2V) 与视频编辑**：支持传入多张参考图、视频或音频，进行角色一致性生成、局部替换、指令风格迁移或口型替换。万相 2.7 及 Kling 等模型提供统一的多模态输入结构。详见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)。
* **专属垂类模型**：包含数字人播报（`wan2.2-s2v`、`emo-v1`、`liveportrait`）、动作迁移（`wan2.2-animate-move/mix`、`animate-anyone`）、表情包生成（`emoji`）及视频风格重绘（`video-style-transform`）等。

> **注意**：万相系列模型已进行协议迭代。**万相 2.7 及新版协议**已统一 `media` 字段结构，支持音频驱动与多模态混合输入；而 **万相 2.1~2.6 旧版协议**使用 `img_url`、`reference_urls` 或独立 function 字段，参数结构不兼容。新项目请优先选用 2.7 及以上版本，详见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)。

## 关键参数说明

调用时需严格遵循 JSON 格式，核心参数分为请求头与请求体两部分：

### 请求头 (Headers)
| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `Content-Type` | string | 是 | 固定为 `application/json` |
| `Authorization` | string | 是 | 格式为 `Bearer {DASHSCOPE_API_KEY}`，需完成 [[api-key配置]] |
| `X-DashScope-Async` | string | 是 | **必须设置为 `enable`**，HTTP 请求仅支持异步模式 |

### 请求体 (Request Body)
| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `model` | string | 是 | 模型标识符，如 `wan2.7-i2v-2026-04-25`、`happyhorse-1.0-t2v` 等，需与所选地域严格匹配 |
| `input` | object | 是 | 包含业务输入数据。`[[prompt|prompt]]` (string) 为文本描述，通常限制 5000 字符内；`media` (array) 用于传入图像/视频/音频的 URL 及类型 (`type`: `first_frame`/`video`/`reference_image`/`driving_audio` 等) |
| `parameters` | object | 否 | 控制输出规格。常见字段：<br>`resolution`/`size`: 分辨率 (如 `720P`, `1280*720`)<br>`duration`: 时长 (秒，通常 5~15)<br>`ratio`/`aspect_ratio`: 画幅比例<br>`watermark`: 是否添加水印<br>`[[prompt|prompt]]_extend`: 是否开启智能提示词优化 |

## 标准调用流程

视频生成属于高耗时任务（通常 1~5 分钟），必须采用异步轮询机制。建议在生产环境通过 [[dashscope-sdk]] 封装重试逻辑，或使用 HTTP 客户端实现。

### 步骤 1：创建任务
向任务下发接口发送 `POST` 请求，成功响应将返回 `task_id`。
* **通用 Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
* **旧版人像/动作 Endpoint**：部分专用模型使用 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

### 步骤 2：轮询获取结果
使用 `task_id` 轮询任务状态。
`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
当响应状态为 `SUCCEEDED` 时，从 `output.video_url`（或对应输出字段）获取结果。轮询实现可参考 [[异步任务轮询]] 最佳实践。

> **注意**：`task_id` 有效期为 **24 小时**。任务创建后请勿重复下发相同请求，应直接通过 `task_id` 轮询。超时或失败任务将返回 `FAILED` 及 `code`/`message` 错误码，需结合日志排查参数合规性或模型负载情况。

## 限制与注意事项

1. **地域强一致性**：模型、Endpoint URL 与 API Key 必须属于同一地域（如北京、新加坡、美西弗吉尼亚、法兰克福）。跨地域混用将直接触发鉴权失败或 404 报错。
2. **媒体资源要求**：所有传入的图像/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接，部分接口支持 Base64 编码（如旧版万相首尾帧），但推荐使用对象存储 OSS 或临时直传链接以提升解析成功率。
3. **并发与限流**：不同模型共享账号级 QPS/RPS 限制及排队队列。高优业务建议配置专属部署实例或查阅对应模型的 [[限流与计费]] 规则。部分模型（如 EMO、AnimateAnyone）要求前置调用 `-detect` 模型进行图像合规校验，校验不通过将阻断视频生成。
4. **画幅与时长约束**：分辨率、画幅比例与时长存在强耦合关系。例如 `480P` 通常不支持 `16:9`，部分模型最长仅支持 5 秒基础输出，超长视频需依赖续写或分镜拼接功能。具体映射关系以各模型参数说明为准。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-image-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/emoji-quick-start.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-image-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)

