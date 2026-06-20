# video generation api

百炼平台提供多系列视频生成模型的 API 接入，涵盖文生视频、图生视频、参考生视频、视频编辑、人像动画等多种能力。所有视频生成 API 均采用**异步调用**模式（创建任务 -> 轮询获取结果），统一通过 DashScope 端点访问。

## 支持的模型与能力概览

平台目前提供以下主要模型系列，各系列支持的功能有所差异：

| 模型系列 | 文生视频 | 图生视频 | 参考生视频 | 视频编辑 | 其他能力 |
|---------|---------|---------|-----------|---------|---------|
| **万相2.7**（推荐） | wan2.7-t2v | wan2.7-i2v | wan2.7-r2v | wan2.7-videoedit | 多镜头叙事、首尾帧、视频续写 |
| **HappyHorse** | happyhorse-1.0-t2v | happyhorse-1.0-i2v | happyhorse-1.0-r2v | happyhorse-1.0-video-edit | — |
| **爱诗 PixVerse** | pixverse/pixverse-c1-t2v | pixverse/pixverse-c1-it2v | pixverse/pixverse-c1-r2v | — | 首尾帧生视频 |
| **可灵 Kling** | kling/kling-v3-video-generation | 同模型 | 同模型 | 同模型 | 文/图/首尾帧/参考/编辑统一模型 |
| **Vidu** | vidu/viduq3-turbo_text2video | vidu/viduq3-pro_img2video | vidu/viduq3-mix_reference2video | — | 首尾帧生视频 |

此外还有面向人像动画的专用模型：

| 模型 | 功能 | 输入 |
|------|------|------|
| **wan2.2-s2v**（数字人） | 生成说话/唱歌/表演视频 | 单张图片 + 音频 |
| **wan2.2-animate-move**（图生动作） | 动作迁移 | 人物图片 + 参考视频 |
| **wan2.2-animate-mix**（视频换人） | 视频角色替换 | 人物图片 + 参考视频 |
| **AnimateAnyone**（舞动人像） | 舞蹈视频生成 | 人物图片 + 动作模板 |
| **EMO**（悦动人像） | 唱演视频生成 | 人物肖像 + 音频 |
| **LivePortrait**（灵动人像） | 播报视频生成 | 人物肖像 + 音频 |
| **VideoRetalk**（声动人像） | 视频口型替换 | 人物视频 + 音频 |
| **video-style-transform** | 视频风格重绘（8种预设风格） | 视频 + 风格参数 |
| **Emoji**（表情包） | 表情包视频 | 人物肖像 + 预设模板 |

> **注意**：爱诗 PixVerse、可灵 Kling、Vidu 属于第三方模型，使用前需在百炼控制台搜索对应模型并单击"立即开通"完成授权。

## 统一调用流程

所有视频生成 API 均采用异步模式，分两步完成：

### 步骤1：创建任务

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

必需的请求头：

- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（必须设置，否则请求将报错）

请求体基本结构：

```json
{
  "model": "<模型名称>",
  "input": {
    "prompt": "描述文本",
    "media": [...]
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5
  }
}
```

成功后返回 `task_id`，有效期 24 小时。详细参数因模型而异，请参考各模型的 API 文档，例如 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 和 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

> **注意**：部分模型（如图生动作 wan2.2-animate-move、视频换人 wan2.2-animate-mix）使用的端点路径为 `/api/v1/services/aigc/image2video/video-synthesis`，与通用视频生成端点不同。

### 步骤2：查询结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
Authorization: Bearer $DASHSCOPE_API_KEY
```

轮询直到任务状态变为 `SUCCEEDED` 或 `FAILED`。请勿重复创建任务，使用同一 `task_id` 轮询即可。

## 关键参数说明

各模型的通用参数包括：

- **resolution**：输出分辨率，常见选项为 `480P`、`720P`、`1080P`（不同模型支持的分辨率不同）
- **ratio**：画面比例，如 `16:9`、`9:16`、`1:1` 等
- **duration**：视频时长（秒），通常支持 5 秒或更长（万相2.7 支持最长 15 秒多镜头叙事）
- **[prompt](../guides/prompt.md)_extend**：是否启用提示词扩写（万相2.7 支持）
- **watermark**：是否添加水印（万相2.7 支持）

万相2.7 的图生视频 API 通过 `media` 数组中的 `type` 字段区分任务类型：`first_frame`（首帧生视频）、`last_frame`（尾帧）、`video`（视频续写）。详见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 多地域支持

视频生成 API 支持多个地域端点，调用时必须确保**模型、Endpoint URL 和 API Key 属于同一地域**，跨地域调用将失败：

| 地域 | Endpoint |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

> **注意**：并非所有模型都支持全部地域。人像动画类模型（AnimateAnyone、EMO、LivePortrait、VideoRetalk、Emoji、video-style-transform）目前仅支持华北2（北京）地域。部分第三方模型（PixVerse、Vidu）也仅支持北京地域。

## 人像动画类模型的调用流程

数字人（wan2.2-s2v）、AnimateAnyone、EMO 等人像动画模型通常需要**先调用图像检测接口**确认输入图片合规，再提交视频生成任务。例如数字人的流程为：

1. 调用 `wan2.2-s2v-detect` 检测图片是否符合要求
2. 检测通过后，调用 `wan2.2-s2v` 提交视频生成任务

图生动作和视频换人模型（wan2.2-animate-move、wan2.2-animate-mix）提供标准模式（`wan-std`）和专业模式（`wan-pro`）两种服务模式，可通过 `service_mode` 参数切换，两者在画质效果和计费上有所不同。详见 [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)。

## 旧版模型

万相 2.1~2.6 版本的视频生成模型仍可使用，但推荐迁移至 wan2.7 系列。旧版模型包括 wan2.6-t2v、wan2.6-i2v-flash、wan2.2-kf2v-flash、wanx2.1-vace-plus、wan2.6-r2v-flash 等，其 API 参数结构与新版有差异，详见各旧版 API 参考文档（如 [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)）。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)


