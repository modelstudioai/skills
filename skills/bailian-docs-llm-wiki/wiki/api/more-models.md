# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、机器翻译、深度研究、OCR文字识别和GUI界面交互等。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于需要高精度、低延迟或特定模态处理能力的生产级应用。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式——`INTENT_MODE`（输出结构化工具调用）和纯标签分类（如 `alarm_set`），适用于对话系统路由与[函数调用](../concepts/function-calling.md)决策。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **机器翻译模型**：`qwen-mt-plus`，支持源/目标语言自动检测、术语干预、翻译记忆（TM）及领域提示（如 IT、金融），适用于高质量批量文档翻译。
- **深度研究模型**：`qwen-deep-research`，仅支持华北2（北京）地域，采用两阶段流程（反问确认 → 深入研究），可联网检索并生成详尽研究报告，**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK**，仅限 Python DashScope SDK 调用。
- **OCR文字识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr` 等，支持图像文本提取、结构化信息抽取（如车票字段），具备 `min_pixels`/`max_pixels` 像素控制与多分辨率适配能力。
- **GUI界面交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专为桌面自动化设计，支持基于截图的鼠标/键盘操作指令生成，需配合 `<tools>` 系统提示与 `computer_use` 函数签名使用。

> **注意**：文档 3 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，但文档 4 和文档 5 的 OCR 与 GUI-Plus 均明确声明支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。该差异非矛盾，而是模型能力边界的真实体现，开发者需按模型文档选择对应 SDK。

## 关键参数

所有模型共享部分通用参数，但关键行为参数因模型而异：

| 参数 | 说明 | 适用模型 | 默认值 | 备注 |
|------|------|----------|--------|------|
| `model` | 模型名称 | 全部 | — | 必填，如 `"tongyi-intent-detect-v3"` |
| `messages` | 对话消息数组 | 全部 | — | `content` 类型依模型而异：意图模型为纯文本；OCR/GUI-Plus 支持 `image_url` + `text` 混合；`qwen-deep-research` 要求两轮 `user`/`assistant` 消息链 |
| `translation_options` | 翻译配置对象（`source_lang`, `target_lang`, `terms`, `tm_list`, `domains`） | `qwen-mt-plus` | — | 仅该模型支持，需置于 `extra_body`（Python）或顶层（Node.js/curl） |
| `output_format` | 报告格式（`model_detailed_report` / `model_summary_report`） | `qwen-deep-research` | `model_detailed_report` | 控制输出长度与详略程度 |
| `min_pixels` / `max_pixels` | 图像像素阈值（影响 OCR/GUI-Plus 输入分辨率） | `qwen3.5-ocr`, `gui-plus` | `3072` / `8388608`（OCR）；`3136` / `1003520`（GUI-Plus） | 文档 4 与文档 5 对 `max_pixels` 默认值描述一致，但文档 5 补充了 `vl_high_resolution_images` 开关对上限的影响 |
| `vl_high_resolution_images` | 启用高分辨率图像处理（固定上限 `12845056` 像素） | `gui-plus` | `false` | 非 OpenAI 标准参数，Python SDK 需置入 `extra_body` |
| `enable_thinking` | 启用思考过程输出（返回 `reasoning_content`） | `gui-plus-2026-02-26` | `false` | 仅特定版本支持，见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 4 中 `qwen3.5-ocr` 的 `max_tokens` 默认值为 `32768`，而文档 5 中 `gui-plus` 的 `max_tokens` 默认值为“模型最大输出长度”，二者未统一。实际使用时应以各模型最新文档或控制台模型详情页为准。

## 使用方式

### 基础前提
- 已在百炼控制台[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`；
- 根据地域选择业务空间专属域名（推荐）：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
  - 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`
- 安装对应 SDK：OpenAI SDK（通用）或 DashScope SDK（`qwen-deep-research` 必选）。

### 调用示例要点
- **意图理解**：必须在 `system` 消息中声明 `Response in INTENT_MODE.` 或指定标签列表，并正确构造 `tools` 或 `intent_dict` JSON 字符串；
- **机器翻译**：`translation_options` 是核心，`terms`（术语表）、`tm_list`（翻译记忆）和 `domains`（领域提示）可显著提升专业领域准确率；
- **深度研究**：严格遵循两阶段调用流程，第二步需将第一步的 `assistant` 回复作为上下文传入；
- **OCR/GUI-Plus**：`messages[0].content` 必须为数组，包含 `{"type": "image_url", "image_url": {"url": "..."} }` 及可选 `{"type": "text", "text": "..."}` 提示词；
- **流式响应**：所有模型均支持 `stream=true`，但 `qwen-deep-research` 的流式响应结构特殊（含 `phase`、`status` 字段），需按其 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 解析。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus`）支持北京、新加坡、美国（弗吉尼亚）三地；
- **SDK 限制**：`qwen-deep-research` 不支持 OpenAI 兼容接口，仅限 DashScope Python SDK；`tongyi-intent-detect-v3` 的 DashScope CLI 不支持 `understanding` 子命令，需用 Python SDK；
- **输入约束**：
  - OCR/GUI-Plus 模型对图像尺寸敏感，`min_pixels`/`max_pixels` 设置不当会导致识别失败或精度下降；
  - `qwen-vl-ocr` 系列模型 `max_tokens` 超过 4096 需商务申请，而 `qwen3.5-ocr` 默认即支持 32768；
- **输出解析**：意图模型返回的 `<tags>...</tags>`、<tool_call>`...`<tool_call>、`<content>...</content>` 结构需用正则解析；深度研究模型返回的 `phase`（如 `WebResearch`, `answer`）和 `status`（如 `streamingQueries`, `finished`）是流式处理的关键状态标识；
- **成本与额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 [Token](../concepts/token.md) 免费额度，具体计费标准见各模型文档。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


