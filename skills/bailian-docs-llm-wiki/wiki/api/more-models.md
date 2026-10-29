# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、机器翻译、深度研究、OCR文字提取和GUI界面交互等。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于需要高精度、低延迟或特定模态处理能力的生产场景。所有模型均需配置有效的 API Key 与 WorkspaceId，并推荐使用新域名以获得更优性能与稳定性。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式——`INTENT_MODE`（输出结构化[函数调用](../concepts/function-calling.md)）和纯标签分类（如 `alarm_set`），适用于智能助手、对话路由等场景。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **机器翻译模型**：`qwen-mt-plus`，支持源/目标语言指定、术语干预、翻译记忆（TM）及领域提示，适用于技术文档、本地化等专业翻译任务。详情见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **深度研究模型**：`qwen-deep-research`，仅支持华北2（北京）地域，采用两阶段工作流（反问确认 → 深入研究），可联网检索并生成详尽研究报告。注意该模型**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅限 DashScope Python SDK 调用。详情见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR文字提取模型**：`qwen3.5-ocr`、`qwen-vl-ocr` 等，支持图像输入（URL 或 Base64）、像素阈值控制（`min_pixels`/`max_pixels`）及结构化 Prompt 提取（如车票字段）。详情见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI界面交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专为桌面自动化设计，支持工具调用（如 `computer_use`）、高分辨率图像处理（通过 `vl_high_resolution_images` 控制）及可选思考链输出（`enable_thinking`）。详情见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：`qwen-deep-research` 明确声明“仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus`）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。此为关键差异，不可混用调用方式。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `model` | 全部 | 必填，模型名称（如 `"tongyi-intent-detect-v3"`） | — |
| `base_url` | OpenAI 兼容调用 | 地域专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；北京、新加坡、美国弗吉尼亚等地域均支持 | — |
| `translation_options` | `qwen-mt-plus` | JSON 对象，含 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）、`domains`（领域）等 | — |
| `output_format` | `qwen-deep-research` | 取值 `model_detailed_report`（默认）或 `model_summary_report` | `model_detailed_report` |
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`、`gui-plus` | 图像预处理像素阈值；单位为像素，不同模型每 [Token](../concepts/token.md) 对应像素不同（如 `qwen3.5-ocr` 为 `32×32`） | `qwen3.5-ocr`: 3072 / 8388608；`gui-plus`: 3136 / 1003520（`vl_high_resolution_images=false`） |
| `vl_high_resolution_images` | `gui-plus` | 布尔值，启用后忽略 `max_pixels`，固定上限为 12845056 像素 | `false` |
| `enable_thinking` | `gui-plus-2026-02-26` | 布尔值，启用后返回 `reasoning_content` 字段；需通过 `extra_body` 传入 | `false` |

## 使用方式

### 通用前提
- 已在百炼控制台创建业务空间并获取对应地域的 API Key；
- 在环境变量中配置 `DASHSCOPE_API_KEY`；
- 安装对应 SDK（[DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK）；
- 将 `{WorkspaceId}` 替换为实际业务空间 ID（可在控制台「业务空间详情」页查看）。

### 调用示例要点
- **意图识别**：必须在 `system` 消息中声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或指定标签列表（纯分类），且工具/意图字典需 JSON 序列化后嵌入 [prompt](../guides/prompt.md)；
- **机器翻译**：`translation_options` 需作为 `extra_body`（Python SDK）或顶层参数（Node.js/curl）传入；
- **深度研究**：必须执行两步调用——先发起研究请求获取澄清问题，再将问题+用户回答组合为第二轮 `messages`（含 `user`+`assistant`+`user`）；
- **OCR 与 GUI-Plus**：`messages.content` 为数组，需同时包含 `image_url` 和 `text`（Prompt）对象；`image_url.url` 支持公网 URL 或 Base64 Data URL。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`）支持北京、新加坡、美国（弗吉尼亚）三地；
- **接口兼容性**：`qwen-deep-research` 不支持 OpenAI 兼容接口，仅 DashScope Python SDK；其余模型均支持 OpenAI 兼容与 DashScope 原生双接口；
- **图像参数差异**：`qwen3.5-ocr` 与 `gui-plus` 的 `min_pixels`/`max_pixels` 默认值及单位逻辑一致，但 `gui-plus` 新增 `vl_high_resolution_images` 开关，其行为与 `max_pixels` 冲突，启用后后者失效；
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 [Token](../concepts/token.md) 免费额度，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
- **流式响应**：`qwen-deep-research` 返回结构化 `phase` 字段（如 `ResearchPlanning`、`WebResearch`），客户端需按 `phase` 和 `status` 解析阶段状态；`qwen3.5-ocr` 和 `gui-plus` 的流式响应则遵循标准 OpenAI SSE 格式，`stream_options.include_usage` 控制是否在末块返回 token 统计。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


