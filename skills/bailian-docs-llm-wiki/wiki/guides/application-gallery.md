# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、法律、金融、客服、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼模型服务构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- `通义拍照解题辅导` 基于 Qwen-VL 多模态模型 + 教育领域微调；
- `通义听悟Agent` 依赖 ASR + LLM + TTS 全链路 pipeline，底层调用 `qwen-audio` 系列模型；
- `千问联网检索Agent` 集成 `qwen-max` 与实时网页抓取模块，支持动态知识注入。

完整能力列表及对应模型详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。部分应用（如 `伶鹊CCAI-语音对话机器人`）还提供可配置的意图识别引擎和对话状态跟踪器，其接口规范在 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md) 中明确定义。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tongyi-farui`），可在控制台应用详情页获取；
- `input`：JSON 格式输入体，结构因应用而异（如 `tongyi-dianjin` 要求 `{"stock_code": "600519", "period": "quarterly"}`）；
- `timeout`：最大执行时长（单位：秒），默认 60，上限 300；
- `stream`：布尔值，仅部分应用（如 `ui-agent`、`tingwu-agent`）支持流式响应。

参数约束与示例详见各子文档，例如 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 明确要求 `input` 必须包含 `screenshot_base64` 字段。

## 使用方式

1. **控制台方式**：进入「应用广场」页面，点击目标应用 → 「立即体验」或「接入应用」获取 SDK 示例；
2. **API 方式**：调用 `POST /v1/applications/{app_id}/invoke`，需携带 `Authorization: Bearer <api_key>`；
3. **SDK 方式**：使用 `dashscope` Python SDK（v1.18.0+）：
   ```python
   from dashscope import Application
   resp = Application.call(app_id='tongyi-farui', input={'query': '合同违约金如何约定？'})
   ```

> **注意**：部分文档（如 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md)）仍引用已下线的 `qwen-plus-v1` 模型，实际运行时自动降级为 `qwen-max`，请以控制台显示的当前生效模型为准。

## 限制和注意事项

- 所有应用共享账户级 QPS 与总调用量配额，超出后返回 `429 Too Many Requests`；
- 输入内容长度受底层模型限制（如 `qwen-turbo` 应用单次输入 ≤ 8K tokens），超长文本将被截断且**不触发警告**；
- 非官方应用（如用户自建应用）不在此广场目录中，不可通过 `/applications/{app_id}/invoke` 直接调用；
- 多模态类应用（如 `multimodal-products`、`tongyi-translate`）对图片/音频格式、大小有严格要求，具体见 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md)。

> **注意**：`web-search-agent` 的联网能力依赖外部搜索引擎接口，在中国大陆地区默认使用百度搜索；若需切换为 Google，请联系技术支持开通白名单——该说明未在 [通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 中体现，但已在最新版 API 文档中更新。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


