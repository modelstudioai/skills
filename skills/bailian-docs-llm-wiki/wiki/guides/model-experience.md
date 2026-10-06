# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或控制台界面调用各类生成式与理解型模型，无需单独配置底层资源。所有模型均遵循统一的鉴权、计费与限流机制，详见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前支持以下核心模型类型及对应能力：

- **文本生成**：支持大语言模型（如 Qwen 系列）的对话、补全、摘要等任务  
- **视觉理解**：图文多模态理解（VLM），支持 OCR、图像描述、细粒度识别等  
- **图片生成与编辑**：文生图（SD、Flux、Qwen-VL）、图生图、局部重绘  
- **视频生成与编辑**：短时长视频生成（≤8s）、关键帧插值、提示词驱动剪辑  
- **世界模型**：具身智能场景下的环境建模与动作规划（需申请白名单）  
- **3D 模型生成**：基于文本生成可导出的 `.glb` 格式 3D 资产（参见 [TriPo 3D 生成指南](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音乐生成（FunMusic）、通用音频生成  
- **向量与重排序**：文本嵌入（embedding）与跨文档相关性重排序（rerank）  
- **全模态**：支持文本、图像、音频、视频混合输入的联合推理（参见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)）

> **注意**：语音合成与语音识别的官方文档已迁移至 help.aliyun.com，其 API 接口路径、参数命名与百炼平台内嵌 SDK 不完全一致；实际集成时请以 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的 `model_id` 和 `endpoint` 为准，避免直接复用 help 文档中的旧版示例。

## 关键参数

所有模型调用均需指定以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，例如 `qwen-max`, `wanx-v1`, `funmusic-v1`；完整列表见 [模型体验](../../raw/model-user-guide/model-experience.md) |
| `input` | object | 是 | 输入数据结构，格式依模型类型而异（如文本模型为 `{ "prompt": "..." }`，视觉模型为 `{ "image_url": "...", "prompt": "..." }`） |
| `parameters` | object | 否 | 可选超参，如 `temperature`, `top_p`, `max_tokens`, `seed` 等；各模型支持项不同，详见对应子文档（如 [文本生成模型](../../raw/model-user-guide/model-experience/text-generation-model.md)） |

## 使用方式

1. **API 调用**：通过 `POST /v1/models/{model_id}/invoke` 发起请求，使用 Bearer [Token](../concepts/token.md) 鉴权  
2. **SDK 调用**：推荐使用 `alibabacloud-bailian20231219` Python/Java SDK，自动处理 endpoint 路由与参数序列化  
3. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写 input → 实时查看响应与 token 消耗  

所有方式均共享同一套配额与计费逻辑，调试结果可直接用于生产环境。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型默认 `32768` tokens，视觉类模型图像分辨率上限 `1536×1536` 像素（超限将自动缩放）  
- 视频生成模型暂不支持自定义帧率或分辨率，输出固定为 `512×512@24fps`  
- 3D 生成任务最长等待时间 120 秒，超时返回 `504 Gateway Timeout`  
- 全模态模型（`omni-v1`）暂不支持流式响应，必须等待全部模态输入处理完成才返回结果  
- 所有模型均禁止用于生成违法、侵权、歧视性或高风险内容；违规调用将触发自动熔断并通知管理员  

> **注意**：[语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 与 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 的 help.aliyun.com 文档未同步百炼平台的最新参数（如 `voice_type` 已弃用，改用 `speaker`），请以 [模型体验](../../raw/model-user-guide/model-experience.md) 及其子文档为准。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


