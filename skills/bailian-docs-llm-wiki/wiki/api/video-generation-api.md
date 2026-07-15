# video generation api

阿里云百炼平台聚合了多家厂商的视频生成模型（万相 Wan、HappyHorse、爱诗 PixVerse、Vidu、可灵 Kling 以及一系列人像驱动模型），统一通过 DashScope 网关的 `video-synthesis` 接口对外提供服务。所有视频生成任务均耗时较长（通常 1-5 分钟），因此 API 统一采用**异步调用**：先「创建任务」拿到 `task_id`，再「轮询查询」获取结果视频 URL。

## 支持的模型与功能

按厂商与任务类型划分，主要能力包括：

- **万相 Wan（推荐）**：wan2.7 系列支持文生视频、图生视频（首帧/首尾帧/视频续写）、参考生视频、视频编辑；另有 wan2.2-animate-move（图生动作）、wan2.2-animate-mix（视频换人）、wan2.2-s2v（数字人）等专用模型。参见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 与 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **HappyHorse**：happyhorse-1.1 系列覆盖文生视频（`-t2v`）、图生视频（`-i2v`）、参考生视频（`-r2v`），以及 happyhorse-1.0-video-edit 视频编辑。
- **爱诗 PixVerse**：pixverse-c1 / v6 / v5.6 系列支持文生视频、图生视频（首帧/首尾帧）、参考生视频，需先在控制台开通 PixVerse 服务。
- **Vidu**：viduq2 / viduq3 系列支持文生视频、图生视频（首帧/首尾帧）、参考生视频（含广告、短剧等场景模型）。
- **可灵 Kling**：kling-v3 系列单一接口即可完成文生视频、图生视频、参考生视频与视频编辑，支持智能分镜（`multi_shot`）。
- **人像/专项模型**：AnimateAnyone（图生舞蹈）、EMO（图生唱演）、LivePortrait（图生播报）、Emoji（表情包）、VideoRetalk（口型替换）、video-style-transform（视频风格重绘）。这些模型多为「检测 + 生成」两段式流程，详见 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。

## 接口与调用流程

绝大多数模型的任务下发地址为：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

调用要点：

- **必须开启异步**：请求头需带 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。
- **鉴权与内容类型**：`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`。
- **两步流程**：创建任务返回 `task_id`（有效期 24 小时），随后用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 轮询。请勿重复创建任务。

> **注意**：部分模型（如 wan2.2-animate-move、wan2.2-animate-mix、wan2.2-s2v 以及旧版 wan2.2-kf2v 首尾帧）使用的是 `.../aigc/image2video/video-synthesis` 路径，而非通用的 `.../aigc/video-generation/video-synthesis`。接入前请以对应模型文档为准，参见 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。

## 关键参数

请求体主要由 `model`、`input`、`parameters` 三部分组成：

- `model`：模型名称（如 `wan2.7-t2v-2026-06-12`、`pixverse/pixverse-c1-t2v`、`vidu/viduq3-turbo_text2video`、`kling/kling-v3-video-generation`）。
- `input.prompt`：文本提示词，用于描述画面与镜头。多镜头一般通过在 `prompt` 中用时间戳/分镜自然语言描述实现。
- `input.media`：新版协议中承载多模态素材，元素含 `type`（`first_frame` / `last_frame` / `image_url` / `image` / `reference_image` / `video` 等）与 `url`；参考生视频可附 `reference_voice` 音色。
- `parameters`：常见有 `resolution`（如 `480P`/`720P`/`1080P`）、`size`（如 `1280*720`）、`duration`（秒）、`ratio`/`aspect_ratio`、`audio`、`watermark`、`prompt_extend` 等。不同模型支持的字段差异较大。

## 限制与注意事项

- **地域一致性**：模型、Endpoint URL 与 API Key 必须属于**同一地域**，跨地域调用会失败。华北2（北京）与新加坡地域拥有各自独立的 API Key 与请求地址，不可混用。
- **专属域名**：百炼为华北2（北京）、新加坡地域推出业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`、`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`），推荐迁移以获得更高性能与稳定性，原有 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 域名仍可用。
- **地域可用性不一致**：万相、HappyHorse 系列提供北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）等多地域；而 PixVerse、Vidu、Kling、数字人 wan2.2-s2v 及各类人像模型目前**仅支持华北2（北京）地域**，且需使用该地域 API Key。参见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

> **注意**：万相视频存在新旧两套协议。wan2.7 走**新版协议**，功能更全（首尾帧、视频续写、多模态），官方**推荐优先选用**；wan2.6 及更早（wan2.5 / wan2.2 / wanx2.1）走**旧版协议**，仅支持子集功能（如旧版图生视频仅支持首帧）。若沿用旧模型请参考 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)。

- **两段式模型**：数字人（wan2.2-s2v）、EMO、LivePortrait、AnimateAnyone、Emoji 等需先调用对应 `-detect` 检测接口确认输入图片合规，再调用生成接口，部分模型还需先生成动作模板。
- **计费与限流**：多为后付费按视频时长（元/秒）或按张计费，且「同时处理中任务数量」通常限制为 1（排队执行），下发接口有 RPS/QPS 限制，接入前请核对各模型的限流与免费额度。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


