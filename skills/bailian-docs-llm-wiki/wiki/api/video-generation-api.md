# video generation api

百炼平台提供多套视频生成异步 API，覆盖文生视频、图生视频、参考生视频、视频编辑、关键帧生视频、数字人、动作生成、风格转换等场景。底层模型包括万相（Wan）系列、HappyHorse、Pixverse、Vidu、Kling、AnimateAnyone、LivePortrait、EMO、Emoji 等。所有接口均采用「创建任务 → 轮询获取」的[异步调用](../concepts/async-invocation.md)模式，单次请求耗时通常在 1–5 分钟。

## 调用模式

视频生成任务耗时较长，API 统一采用[异步调用](../concepts/async-invocation.md)，流程分两步：

1. **创建任务**：`POST /api/v1/services/aigc/video-generation/video-synthesis`（不同模型 endpoint 路径略有差异），携带 `X-DashScope-Async: enable` 头，返回 `task_id`。
2. **轮询获取**：`GET /api/v1/tasks/{task_id}`，根据 `output.task_status`（`PENDING` / `RUNNING` / `SUCCEEDED` / `FAILED` / `CANCELED`）判断结果，成功后从 `output.video_url` 取视频地址。

### 地域与域名

- 必须保证模型、Endpoint URL、[API Key](../concepts/api-key.md) 属于**同一地域**，跨地域调用会失败。
- 华北2（北京）、新加坡地域推荐使用[业务空间](../concepts/workspace.md)专属域名以获得更好性能与稳定性：
  - 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- `{WorkspaceId}` 在百炼控制台「[业务空间](../concepts/workspace.md)详情」页查看，旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 仍可用。

### 鉴权

统一使用 `Authorization: Bearer $DASHSCOPE_API_KEY`，[API Key](../concepts/api-key.md) 通过环境变量配置。详见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## 模型与能力总览

### 万相（Wan）系列

万相 2.7 系列为当前主力模型，能力最全，详见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。

| 能力 | 模型 / function | 说明 |
| --- | --- | --- |
| 文生视频 | `wan2.7-t2v-plus` | 文本直接生成视频 |
| 图生视频（首帧） | `wan2.7-i2v-plus` | 输入首帧图片 + 文本 |
| 参考生视频 | `wan2.7-vace-plus` 的 `image_reference` / `video_reference` | 多参考图/视频驱动 |
| 视频编辑 | `wan2.7-vace-plus` 的 `video_repainting` / `first_last_frame_i2v` 等 | 视频重绘、首尾帧等 |
| 图生动作 | `wan-animate-move` | 让静态人物图做出指定动作 |
| 数字人（S2V） | `wan-s2v` | 音频/文本驱动数字人 |

万相 2.7 视频编辑支持 `function` 字段切换子能力：`image_reference`、`video_reference`、`video_repainting`、`first_last_frame_i2v`、`style_transfer` 等。VACE 还提供旧版 `wanx2.1-vace-plus` 模型。调用示例与参数细节见 [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)。

### HappyHorse

HappyHorse 提供图生视频（首帧）、文生视频、参考生视频、视频编辑四类接口，模型名以 `happyhorse-*` 形式指定。其图生视频以首帧图片 + 文本引导生成物理真实、运动流畅的视频，详见 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。

### Pixverse

支持文生视频、图生视频、参考生视频、关键帧生视频（keyframe-to-video，通过关键帧序列控制镜头）。适合需要多关键帧控制的场景，详见 [Pixverse-关键帧生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-keyframe-to-video-api-reference.md)。

### Vidu

提供文生视频、图生视频、参考生视频、关键帧生视频，模型名为 `vidu-*` 系列。

### Kling

提供 `kling-*` 系列视频生成接口，支持文生/图生视频。

### 数字人 / 动作 / 表情类

- **AnimateAnyone**：静态人物图生成动作视频，适合服装展示、舞蹈等。
- **LivePortrait**：人像表情驱动，基于参考图 + 驱动视频/音频。
- **EMO**：音频驱动人物口型与表情，生成唱歌/说话视频。
- **VideoRetalk**：视频换口型，对已有视频中的人物做口型替换。
- **Emoji**：生成动态表情（emoji）视频。

### 风格转换

`video-style-transform` 接口对输入视频做风格化转换（如动漫、油画等）。

## 关键参数

通用参数结构（以万相 VACE 为例）：

```json
{
  "model": "wan2.7-vace-plus",
  "input": {
    "function": "image_reference",
    "prompt": "文本描述",
    "ref_images_url": ["https://..."]
  },
  "parameters": {
    "prompt_extend": true,
    "obj_or_bg": ["obj", "bg"],
    "size": "1280*720"
  }
}
```

- `model`：必填，指定模型名。
- `input.function`：VACE 等多能力模型必填，用于选择子能力。
- `input.prompt`：文本描述，多数接口必填；建议启用 `prompt_extend` 由模型扩写增强画面表现。
- `input.img_url` / `ref_images_url` / `video_url`：图生/参考类接口必填，需为可公网访问的 URL。
- `parameters.size`：分辨率，常见 `1280*720`、`960*960`、`1080*1920` 等；不同模型支持的尺寸集合不同。
- `parameters.duration`：视频时长（秒），各模型支持范围不同，通常 5–10 秒。
- `parameters.seed`：随机种子，可复现结果。

> **注意**：不同模型对 `size`、`duration`、参考图数量上限的支持不一致，调用前请以对应模型 API 参考文档为准，避免因参数越界导致 `InvalidParameter` 报错。

## 使用方式

### OpenAI 兼容 SDK

部分模型（如万相 2.7）支持通过 OpenAI Python / Java SDK 调用，base_url 指向百炼 endpoint，`model` 字段填对应模型名，`response_format` 等视频类参数按文档设置。视频任务同样为异步，需轮询。

### HTTP / curl

最通用的方式，所有模型均支持。典型 curl（图生视频）：

```bash
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "wan2.7-i2v-plus",
    "input": {"prompt": "...", "img_url": "https://..."},
    "parameters": {"size": "1280*720", "duration": 5}
  }'
```

### 异步轮询

```bash
curl -X GET "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

成功响应中 `output.video_url` 为视频下载地址，有效期通常为 24 小时，请及时下载或转存。

## 限制与注意事项

- **异步与超时**：单任务 1–5 分钟，建议轮询间隔 1–5 秒，设置合理超时与重试。
- **输入资源**：图片/视频 URL 必须可公网访问；建议使用百炼同地域 OSS 或公网 CDN，避免因网络不通导致 `InputDownloadError`。
- **地域一致性**：模型、endpoint、[API Key](../concepts/api-key.md) 必须同地域。
- **内容安全**：所有请求经过内容安全审核，违规内容会被拒绝；输入文本与图片均会校验。
- **配额与计费**：按生成视频时长（秒）或次数计费，不同模型单价不同；高并发请关注 QPS 配额，必要时提工单申请。
- **legacy 接口**：文档中 `legacy-*` 系列（如 `legacy-wan-text-to-video`、`legacy-wanx-vace`）为旧版接口，建议迁移至万相 2.7 新接口以获得更好效果与稳定性。
- **数字人合规**：数字人/换脸/口型替换类能力（S2V、AnimateAnyone、EMO、VideoRetalk、LivePortrait）涉及肖像权，使用前须确认素材授权，平台对生成内容加水印并做合规审计。

> **注意**：`wanx2.1-vace-plus`（VACE 旧版）与 `wan2.7-vace-plus`（新版）的 `function` 取值与参数略有差异，迁移时不要直接套用旧参数，需对照新版文档调整。

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








