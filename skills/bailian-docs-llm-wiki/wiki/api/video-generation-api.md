# video generation api

百炼视频生成 API 将文本、图像、视频、音频等多模态输入加工为视频，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人/人像动画等场景。所有视频任务均为异步调用，统一遵循"创建任务 → 轮询获取结果"两步流程；不同模型族（万相、HappyHorse、可灵、爱诗、Vidu 等）在 endpoint、协议版本、参数命名上存在差异。

## 调用模型

视频生成任务耗时较长（通常 1–5 分钟），API 采用异步方式，所有模型都遵循同一交互模式：

1. **创建任务**：向 `POST /api/v1/services/aigc/video-generation/video-synthesis`（或部分人像动画模型的 `/api/v1/services/aigc/image2video/video-synthesis`）发送请求，请求头必须包含 `X-DashScope-Async: enable`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`，响应返回 `task_id`。
2. **轮询获取**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询结果。`task_id` 有效期 24 小时，过期后任务状态返回 `UNKNOWN`。请勿重复创建任务，轮询即可。

任务状态包含 `PENDING`、`SUCCEEDED`、`FAILED` 等；新手指引可参考 [Postman 快速调用](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。完整创建/查询示例见 [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)。

## 地域与域名

模型、Endpoint URL、API Key 必须属于**同一地域**，跨地域调用将失败。各模型族支持的域名略有不同：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（HappyHorse 等 maas 域名）或 `https://dashscope.aliyuncs.com`（wan2.7 新版协议、可灵、爱诗、Vidu 等）。
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，官方建议从旧域名 `https://dashscope-intl.aliyuncs.com` 迁移至该[业务空间](../concepts/workspace.md)专属域名以获得更佳性能与稳定性。
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com`。
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com`。

`{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台"[业务空间](../concepts/workspace.md)详情"页查看，详见 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。

> **注意**：可灵、视频风格重绘等模型仅适用于"中国内地（北京）"地域，必须使用该地域的 API Key。

## 模型族与能力

| 模型族 | 代表 model 值 | 主要能力 |
| --- | --- | --- |
| 万相 2.7（新版协议） | `wan2.7-i2v-2026-04-25`、`wan2.7-t2v`、`wan2.7-r2v`、`wan2.7-videoedit` | 多模态输入，首帧/首尾帧生视频、视频续写、参考生视频、指令编辑、视频迁移 |
| 万相 2.1–2.6（legacy） | `wan2.6-i2v-flash`、`wan2.6-r2v-flash`、`wan2.2-kf2v-flash`、`wan2.6-t2v`、`wanx2.1-vace-plus` | 仅支持首帧生视频等单一任务，老协议 |
| 万相人像 | `wan2.2-animate-move`（图生动作）、`wan2.2-s2v`（数字人）、`wan2.2-animate-mix`（视频换人） | 人物图片 + 参考视频/音频，生成动作/说话/换人视频 |
| HappyHorse | `happyhorse-1.1-t2v`、`happyhorse-1.1-i2v`、`happyhorse-1.1-r2v`、`happyhorse-1.0-video-edit` | 文生/图生/参考生/视频编辑，物理真实、运动流畅 |
| 可灵 | `kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation` | 文生视频、图生视频、首尾帧、参考生视频、视频编辑，支持智能分镜 |
| 爱诗 PixVerse | `pixverse/pixverse-c1-t2v`、`pixverse-c1-it2v`、`pixverse-c1-kf2v`、`pixverse-c1-r2v` | 文生、图生首帧、图生首尾帧、参考生视频 |
| Vidu | `vidu/viduq3-turbo_text2video`、`viduq3-turbo_start-end2video`、`viduq3-pro_img2video`、`viduq3-mix_reference2video` | 文生、首尾帧、图生首帧、参考生视频 |
| 人像动画类 | `emo`、`animateanyone`、`liveportrait`、`videoretalk`、`emoji`、`video-style-transform` | 唱演、舞蹈、播报、口型替换、表情包、风格重绘 |

万相 2.7 是当前推荐的新版协议，[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 明确指出新版接口仅支持 wan2.7 模型，原 wan2.6 及早期模型走 legacy 协议。HappyHorse 系列的 endpoint 走 maas 域名并支持北京、新加坡、美国、德国四地域。

## 请求结构

请求体统一为 `{"model", "input", "parameters"}` 三段式，但字段命名因模型族而异：

- **万相 2.7 / HappyHorse**：`input.prompt` + `input.media`（数组，元素含 `type` 如 `first_frame`/`last_frame`/`reference_image`/`reference_video`/`video` 与 `url`，部分还支持 `reference_voice`）；`parameters` 含 `resolution`（如 `720P`）、`ratio`（如 `16:9`）、`duration`（秒）、`prompt_extend`、`watermark`。
- **万相人像（animate-move / animate-mix）**：使用 `input.image_url`、`input.video_url`、`input.watermark`，`parameters.mode` 取 `wan-std` 或 `wan-pro`，endpoint 为 `image2video/video-synthesis`。
- **万相数字人 s2v**：`input.image_url` + `input.audio_url`，`parameters.style`（如 `speech`）。
- **可灵**：`parameters` 用 `mode`（`std`/`pro`）、`aspect_ratio`、`duration`、`audio`、`watermark`；智能分镜通过 `input.multi_shot=true`、`shot_type="customize"`、`input.multi_prompt` 数组配置。
- **爱诗 / Vidu**：参数命名接近万相（`resolution`、`duration`、`watermark`），具体取值范围以各文档为准。

> **注意**：万相 2.7 文生视频的镜头结构通过 `prompt` 自然语言控制（如"第1个镜头[0-3秒] 全景：…"），**不要**配置 `shot_type` 参数，配置也不会生效。可灵则相反，分镜通过 `shot_type`/`multi_prompt` 显式配置。

## 典型示例

万相 2.7 文生视频（多镜头叙事）：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-t2v",
    "input": {
        "prompt": "第1个镜头[0-3秒] 全景：雨夜街头。第2个镜头[3-6秒] 中景：人物进入建筑。"
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "16:9",
        "prompt_extend": true,
        "watermark": true,
        "duration": 15
    }
}'
```

HappyHorse 图生视频（首帧），完整地域/参数说明见 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)：

```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "happyhorse-1.1-i2v",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "media": [{"type": "first_frame", "url": "https://example.com/first.png"}]
    },
    "parameters": {"resolution": "720P"}
}'
```

## 限制与注意事项

- **异步必选头**：缺少 `X-DashScope-Async: enable` 会报错 `current user api does not support synchronous`。
- **任务有效期**：`task_id` 仅 24 小时有效，过期查询返回 `UNKNOWN`；请勿重复创建任务，直接轮询。
- **地域隔离**：北京与新加坡拥有独立 API Key 与请求地址，不可混用；跨地域调用导致鉴权失败。
- **协议版本**：wan2.7 新版协议接口与 legacy（2.1–2.6）协议不互通，模型与接口必须匹配，详见 [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)。
- **服务开通**：可灵、视频风格重绘等模型需在百炼控制台模型卡片单击"立即开通"并完成授权后才能调用。
- **人像画幅**：数字人 `wan2.2-s2v` 不限画幅，支持肖像、半身、全身及卡通形象；悦动人像 EMO 更适合人物特写/肖像。如需全身或大半身视频，推荐 s2v；追求性价比可选 EMO，对比见 [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)。
- **计费模式**：`wan2.2-animate-move`、`wan2.2-animate-mix` 提供 `wan-std`（标准）与 `wan-pro`（专业）两种模式，画质与计费不同。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)


