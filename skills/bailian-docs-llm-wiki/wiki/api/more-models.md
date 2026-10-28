# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型（[more](more.md) models），覆盖意图理解、机器翻译、深度研究、OCR文字识别和GUI界面交互等场景。这些模型在对应领域具备更强的专业能力与优化性能，适用于需要高精度、低延迟或复杂多模态处理的业务需求。所有模型均支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，推荐使用业务空间专属域名以获得更优稳定性与推理性能。

## 支持的模型/功能

当前可用的专用模型包括：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两类模式：  
  - `INTENT_MODE`：同时输出结构化[函数调用](../concepts/function-calling.md)（含工具名与参数）；  
  - 纯意图分类模式：从预定义标签集中返回单个意图标识符（如 `alarm_set`）。  
  详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

- **机器翻译模型**：`qwen-mt-plus`，支持源语言自动检测、术语干预、翻译记忆（TM）及领域提示（如 IT、金融），适用于高质量专业文档翻译。

- **深度研究模型**：`qwen-deep-research`，仅支持华北2（北京）地域，采用两阶段工作流（反问确认 → 深入研究），可联网检索并生成详尽研究报告（`model_detailed_report`）或摘要报告（`model_summary_report`）。该模型**仅支持 DashScope Python SDK**，不兼容 OpenAI 接口或 Java SDK —— 此限制在 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中明确说明。

- **OCR 文字识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr` 等，支持图像文本提取、结构化信息抽取（如车票字段），并提供 `min_pixels`/`max_pixels` 图像分辨率控制参数。

- **GUI 交互模型**：`gui-plus`（含 `gui-plus-2026-02-26`），专为桌面自动化设计，支持基于截图的鼠标键盘操作指令生成，需配合 `<tools>` 系统提示与 `computer_use` [函数调用](../concepts/function-calling.md)规范使用。

> **注意**：文档 4（Qwen-OCR）中 `min_pixels` 默认值描述为“3136（即 `4×28×28`）”，而文档 5（GUI-Plus）中同参数默认值亦写为“3136”，但文档 4 同时指出 `qwen3.5-ocr` 的像素单位为 `32×32`，其最小值应为 `3072（3×32×32）`。实际调用时请以模型文档页脚的 [模型选型](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr#0573ce495fnnf) 或最新控制台说明为准。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `translation_options` | `qwen-mt-plus` | 必填对象，含 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）、`domains`（领域提示）等子字段。 |
| `output_format` | `qwen-deep-research` | 可选值：`model_detailed_report`（默认，约6000 [Token](../concepts/token.md)）或 `model_summary_report`（约1500–2000 [Token](../concepts/token.md)）。 |
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus` | 控制图像输入分辨率，单位为像素；不同模型对应不同像素/[Token](../concepts/token.md) 换算规则（如 `qwen3.5-ocr`: `32×32`/Token）。 |
| `vl_high_resolution_images` | `gui-plus` | 布尔值，启用后忽略 `max_pixels`，固定上限为 `12845056` 像素。 |
| `enable_thinking` | `gui-plus-2026-02-26` | 仅该版本支持；启用后返回 `reasoning_content` 字段，用于调试思考链。 |

## 使用方式

### 域名与认证
- **统一推荐域名格式**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如 `cn-beijing`, `ap-southeast-1`, `us-east-1`），替代旧版 `dashscope.aliyuncs.com`。  
- **前置依赖**：必须已[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并安装对应 SDK（[DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK）。

### 调用示例要点
- **意图识别**：System Message 中必须显式声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)模式）或 `just reply with the chosen tag.`（纯意图模式）。
- **OCR 与 GUI-Plus**：`messages.content` 为数组，需混合 `text` 和 `image_url` 类型元素；`image_url.url` 支持公网 URL 或 Base64 Data URL。
- **Qwen-Deep-Research**：必须分两步调用（反问确认 + 深入研究），且第二步需将第一步的 `assistant` 回复作为历史消息传入。
- **流式响应**：所有模型均支持 `stream=true`，但 `qwen-deep-research` 的响应结构含 `phase` 字段（如 `ResearchPlanning`, `WebResearch`, `answer`），需按阶段解析。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen-mt-plus` 和 `qwen3.5-ocr` 支持北京、新加坡、美国（弗吉尼亚）三地；`gui-plus` 当前仅列北京地域 endpoint，实际部署请以控制台为准。
- **SDK 限制**：`qwen-deep-research` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅可通过 DashScope Python SDK 调用；`dashscope CLI` 不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **输出长度**：`qwen-vl-ocr` 的 `max_tokens` 默认上限为 4096；若需提升至 4097–8192，须联系商务经理申请，并提供主账号ID、图像类型、QPS等信息。
- **参数兼容性**：`top_k`、`vl_high_resolution_images`、`enable_thinking` 等非 OpenAI 标准参数，在 Python SDK 中需置于 `extra_body` 对象内传递；Node.js/HTTP 调用则作为顶层参数。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100 万 Token 免费额度（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)），其他模型未在原始文档中声明免费策略。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


