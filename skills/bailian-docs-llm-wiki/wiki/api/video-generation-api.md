# video generation api

百炼平台视频生成 API 提供文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、视频换人、图生动作、数字人、肖像动态视频（唱演/播报/口型替换/表情包）以及视频风格重绘等多类异步生成能力，覆盖万相（Wan/HappyHorse/wanx）、爱诗（PixVerse）、Vidu、可灵（Kling）等多家模型。所有接口均采用「创建任务获取 task_id → 轮询查询结果」的[异步调用](../concepts/async-invocation.md)模式，task_id 有效期 24 小时。

## 调用模式与通用约定

视频生成任务耗时较长（通常 1–5 分钟，万相2.1 视频编辑约 5–10 分钟），因此 HTTP 接口统一采用[异步调用](../concepts/async-invocation.md)，流程固定为两步：

1. **创建任务**：向 `POST /api/v1/services/aigc/video-generation/video-synthesis`（部分模型走 `image2video/video-synthesis`）提交请求，获取 `task_id`。
2. **轮询结果**：`GET /api/v1/tasks/{task_id}` 拉取任务状态，直到拿到视频 URL。**请勿重复创建任务**，直接轮询即可。

通用要求：

- **同地域约束**：模型、Endpoint URL、[API Key](../concepts/api-key.md) 必须属于同一地域，跨地域调用会失败。
- **请求头**：必填 `Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`X-DashScope-Async: enable`。缺少异步头会报错 `current user api does not support synchronous calls`。
- **专属域名**：华北2（北京）建议从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡建议从 `dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，`{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID。
- 美国弗吉尼亚、德国法兰克福地域提供 `dashscope-us.aliyuncs.com`、`{WorkspaceId}.eu-central-1.maas.aliyuncs.com` 等域名。
- 初学者可先使用 [Postman 快速上手](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

> **注意**：万相图生动作、视频换人、数字人 s2v 等模型走的是 `/api/v1/services/aigc/image2video/video-synthesis` 路径，与万相2.7 文生/图生/参考生/编辑的 `/video-generation/video-synthesis` 不同；调用前请核对模型对应文档。

## 支持的模型与功能矩阵

### 万相系列（HappyHorse / Wan / wanx）

HappyHorse 是万相新一代视频生成模型，支持[多模态](../concepts/multimodal.md)输入，覆盖文生、图生（首帧）、参考生、视频编辑，详见 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md) 与 [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。

- `happyhorse-1.1-t2v` 文生视频
- `happyhorse-1.1-i2v` 图生视频（基于首帧）
- `happyhorse-1.1-r2v` 参考生视频（多图像，支持 `[Image N]` 标记描述主体）
- `happyhorse-1.0-video-edit` 视频编辑（指令 + 参考图）

万相2.7 系列为**新版协议**，接口 `model` 字段示例：`wan2.7-t2v`、`wan2.7-i2v-2026-04-25`、`wan2.7-r2v`、`wan2.7-videoedit`。图生视频支持首帧生视频、首尾帧生视频、视频续写三大任务，支持文本/图像/音频/视频[多模态](../concepts/multimodal.md)输入，参考生视频可保持角色形象与音色一致性，详见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 与 [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)。

旧版协议模型（wan2.6/2.5/2.2/wanx2.1）仍可用但**推荐优先选用 wan2.7**：

- `wan2.6-i2v-flash` / `wan2.6-t2v` / `wan2.6-r2v-flash`：旧版图生/文生/参考生，支持 `shot_type: multi` 多镜头叙事。
- `wan2.2-kf2v-flash`：首尾帧生视频（旧版，走 `image2video/video-synthesis`）。
- `wanx2.1-vace-plus`：万相2.1 视频编辑统一模型，通过 `input.function` 切换 `image_reference`/`video_repainting` 等任务。
- 动作/换人/数字人：`wan2.2-animate-move`（图生动作，`wan-std`/`wan-pro`）、`wan2.2-animate-mix`（视频换人）、`wan2.2-s2v` + `wan2.2-s2v-detect`（数字人，单图+音频，支持肖像/全身/半身）。

### 爱诗 PixVerse 系列

仅适用于华北2（北京），需先在控制台搜索 PixVerse 开通。模型名以 `pixverse/` 前缀调用，支持文生、图生（首帧）、首尾帧、参考生视频：

- `pixverse/pixverse-c1-t2v`、`pixverse/pixverse-v6-t2v`、`pixverse/pixverse-v5.6-t2v`（文生）
- `pixverse/pixverse-c1-it2v` 等（图生）
- `pixverse/pixverse-c1-kf2v`、`pixverse/pixverse-v6-kf2v`（首尾帧）
- `pixverse/pixverse-c1-r2v`（参考生，支持 `ref_name` 设置主体名称）

详见 [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md) 与 [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)。

### Vidu 系列

仅适用于华北2（北京），需开通 Vidu 模型。模型名以 `vidu/` 前缀调用：

- 文生：`vidu/viduq3-pro_text2video`、`vidu/viduq3-turbo_text2video`、`vidu/viduq2_text2video`
- 图生（首帧）：`vidu/viduq3-pro_img2video`、`vidu/viduq3-turbo_img2video`、`vidu/viduq2-pro_img2video` 等
- 首尾帧：`vidu/viduq3-pro_start-end2video`、`vidu/viduq3-turbo_start-end2video` 等
- 参考生：`vidu/viduq3-mix_reference2video`、`vidu/viduq2-pro_reference2video`（参考图像+视频）

详见 [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md) 与 [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)。

### 可灵 Kling 系列

仅适用于华北2（北京），需开通可灵 AI。模型名以 `kling/` 前缀调用，支持文生、图生（首帧/首尾帧）、参考生、视频编辑，以及智能分镜（`multi_shot: true`、`shot_type: customize` + `multi_prompt`）：

- `kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`

详见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

### 肖像动态与风格重绘

人物肖像类模型通常需先调用 `-detect` 检测图像合规再生成视频，仅支持华北2（北京）：

- **舞动人像 AnimateAnyone**：`animate-anyone-detect-gen2` → `animate-anyone-template-gen2`（动作模板）→ `animate-anyone-gen2`（生成）。支持后付费与独立部署。
- **悦动人像 EMO**：`emo-detect-v1` → `emo-v1`，图生唱演视频，按画幅[计费](../concepts/billing.md)（1:1 0.08元/秒，3:4 0.16元/秒）。
- **灵动人像 LivePortrait**：`liveportrait-detect` → `liveportrait`，轻量快速播报视频，0.02元/秒。
- **声动人像 VideoRetalk**：`videoretalk`，视频口型替换，0.08元/秒。
- **表情包 Emoji**：先检测后生成，传入预设模板 `driven_id`（如 `mengwa_kaixin`）。
- **视频风格重绘**：`video-style-transform`，8 种预设风格（日式漫画/美式漫画/3D卡通/国风水墨等），参数 `style` 取 0–7。

## 关键参数说明

请求体结构统一为 `{model, input, parameters}`：

- `model`（必选）：模型名称，注意新版/旧版协议不混用（如 `wan2.7-*` 仅走新版接口，`wan2.6-*`/`wanx2.1-*` 走旧版）。
- `input.prompt`（必选/可选）：文本提示词，多数模型支持中英文，字符上限约 5000，超出自动截断。万相2.7 文生视频通过自然语言描述控制单/多镜头，`shot_type` 不生效；旧版需显式 `shot_type: "multi"` + `prompt_extend: true`。
- `input.media`：[多模态](../concepts/multimodal.md)素材数组，每项 `{type, url}`。常见 `type`：`first_frame`、`last_frame`、`image`、`image_url`、`video`、`reference_image`、`reference_video`。万相2.7 参考生可附加 `reference_voice` 指定音色。
- `input.reference_urls`（旧版万相参考生）：直接传图像/视频 URL 列表。
- `input.first_frame_url` / `last_frame_url`（万相2.2 旧版首尾帧）：支持 Base64 字符串。
- `input.function`（wanx2.1-vace-plus）：切换任务类型，如 `image_reference`、`video_repainting`。
- `parameters`：通用项含 `resolution`（`480P`/`540P`/`720P`）、`size`（如 `1280*720`、`1024*576`）、`ratio`/`aspect_ratio`（`16:9` 等）、`duration`（秒，常见 5/15）、`watermark`（bool）、`prompt_extend`（bool，智能改写提示词）、`audio`（bool，是否生成音频）、`mode`（`wan-std`/`wan-pro`/`std` 等，区分标准/专业模式）、`style`（视频风格重绘 0–7）、`video_fps`。

> **注意**：不同模型对 `size` 与 `resolution` 的支持存在差异。PixVerse/Vidu 多用 `size`（如 `1280*720`），万相多用 `resolution`（如 `720P`）；可灵使用 `aspect_ratio`。同一模型族内不同版本（如 PixVerse c1/v6/v5.6）参数也可能不同，请以各模型文档为准。

## 使用方式

### 文生视频示例（万相2.7）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-t2v",
    "input": {
        "prompt": "一段侦探追查故事。第1个镜头[0-3秒] 全景：雨夜的纽约街头..."
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

### 参考生视频示例（万相2.7，多主体+音色）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-r2v",
    "input": {
        "prompt": "视频1抱着图3，在图4的椅子上弹奏...",
        "media": [
            {"type": "reference_image", "url": "...", "reference_voice": "...mp3"},
            {"type": "reference_video", "url": "...mp4"}
        ]
    }
}'
```

### 查询任务结果

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

新加坡地域查询需将 base_url 替换为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`。

### 数字人 s2v 调用顺序

1. `wan2.2-s2v-detect` 传入图片 URL 检测合规（0.004元/张）。
2. 检测通过后 `wan2.2-s2v` 传入图片 URL 与音频 URL 提交任务（480P 0.5元/秒，720P 0.9元/秒），轮询获取结果。

## 限制与注意事项

- **地域与限流**：人物肖像类模型（EMO/LivePortrait/VideoRetalk/Emoji/AnimateAnyone/wan2.2-s2v）多数仅支持华北2（北京），且「同时处理中任务数量」普遍为 1，任务会排队。任务下发接口 QPS 限制通常为 5。
- **[计费](../concepts/billing.md)**：多数模型按生成视频时长（秒）[计费](../concepts/billing.md)。万相图生动作/视频换人区分 `wan-std`/`wan-pro` 两档；EMO 按画幅分价；VideoRetalk 0.08元/秒；LivePortrait 0.02元/秒。独立部署模型（如 `animate-anyone-deployment`、`emo-deployment`）按算力单元预付费，调用仅收部署费用。
- **免费额度**：各模型提供有限免费额度（如检测模型 200 张、生成模型 1800 秒等），详见[免费额度说明](https://help.aliyun.com/zh/model-studio/new-free-quota)。
- **新旧协议不兼容**：万相2.7 接口为**新版协议**，仅支持 wan2.7 模型；旧版接口支持 wan2.6 及早期模型，二者 `model` 不可混用。
- **多镜头**：万相2.7 通过 [prompt](../guides/prompt.md) 自然语言控制分镜，无需 `shot_type`；旧版万相需 `shot_type: "multi"` + `prompt_extend: true`；PixVerse c1 在 [prompt](../guides/prompt.md) 中描述多镜头，不支持 `shot_type`；可灵用 `multi_shot: true` + `multi_prompt`。
- **视频编辑**：万相2.7 视频编辑支持纯指令编辑与指令+参考图编辑（局部替换）；wanx2.1-vace-plus 通过 `function` 字段切换任务；HappyHorse 视频编辑为 `happyhorse-1.0-video-edit`。
- **异步头必填**：缺少 `X-DashScope-Async: enable` 会直接报错。
- **task_id 有效期**：24 小时，过期查询会返回 `UNKNOWN` 状态。

> **注意**：本文涵盖的 31 篇文档中，万相2.7 系列明确标注「推荐优先选用」，旧版（2.1–2.6）文档仅作兼容参考；如遇旧版模型下线或参数变更，以控制台模型市场与最新版 API 文档为准。

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





