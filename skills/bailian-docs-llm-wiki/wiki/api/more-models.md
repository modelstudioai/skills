# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、深度研究、GUI界面交互和OCR文字识别等。这些模型在特定任务上具备更强的专业能力与优化性能，开发者可根据业务需求选择调用。所有模型均支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，但部分模型存在地域、SDK 或协议限制。

## 支持的模型/功能

当前 `more models` 类别下主要包含以下四类专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式——同时输出意图与[函数调用](../concepts/function-calling.md)（需 `Response in INTENT_MODE.` 系统提示），或仅输出预定义意图标签（如 `alarm_set`）。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，专用于长周期、多阶段的研究任务（反问确认 → 研究规划 → 网络搜索 → 报告生成），**仅支持华北2（北京）地域及 DashScope Python SDK**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK。
- **GUI界面交互模型**：`gui-plus` 及其版本（如 `gui-plus-2026-02-26`），支持图文多模态输入与工具调用，适用于自动化桌面操作（如点击、输入、截图）。支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope API。
- **OCR文字识别模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20`、`qwen-vl-ocr` 等，支持高精度图像文本提取与结构化信息抽取（如车票、合同字段），支持多地域部署（华北2、新加坡、美国弗吉尼亚）。

> **注意**：文档 2 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 OpenAI 兼容接口”，而文档 3 和文档 4 均明确支持 OpenAI 兼容接口。三者在协议支持上存在明确差异，非文档矛盾，而是模型设计定位不同。

## 关键参数

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 模型名称（必填） | 全部 | 如 `"tongyi-intent-detect-v3"`、`"qwen-deep-research"`、`"gui-plus-2026-02-26"`、`"qwen3.5-ocr"` |
| `messages` | 对话上下文数组（必填） | 全部 | `gui-plus` 和 `qwen-vl-ocr` 支持 `image_url` + `text` 混合 content；`qwen-deep-research` 要求两阶段 message 结构（user → assistant → user） |
| `vl_high_resolution_images` | 控制图像像素上限策略（非 OpenAI 标准） | `gui-plus` | 需通过 `extra_body` 传入；设为 `true` 时忽略 `max_pixels`，固定上限 `12845056` |
| `output_format` | 指定研究报告格式 | `qwen-deep-research` | 取值：`model_detailed_report`（默认，~6000 Token）或 `model_summary_report`（~1500–2000 Token） |
| `min_pixels` / `max_pixels` | 图像预处理像素阈值 | `gui-plus`、`qwen-vl-ocr` | 默认值因模型而异（如 `qwen3.5-ocr` 默认 `min_pixels=3072`, `max_pixels=8388608`）；[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中详细列出了各模型对应关系 |
| `enable_thinking` | 是否返回思考过程（仅混合思考模型） | `gui-plus-2026-02-26` | 需通过 `extra_body` 传入；启用后思考内容在 `reasoning_content` 字段中 |

## 使用方式

### 域名与认证
- **统一推荐使用业务空间专属域名**（性能与稳定性更优）：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
  - 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`（仅 `qwen-vl-ocr` 系列支持）
- 所有模型均要求已[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并建议配置至环境变量 `DASHSCOPE_API_KEY`。
- SDK 安装参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### 调用方式示例
- **OpenAI 兼容接口**：适用于 `tongyi-intent-detect-v3`、`gui-plus`、`qwen-vl-ocr` 系列，`base_url` 需设为对应地域的 `compatible-mode/v1` 地址。
- **DashScope SDK**：
  - `tongyi-intent-detect-v3` 和 `gui-plus` 支持 `chat.completions.create`；
  - `qwen-deep-research` **必须使用 `Generation.call`**（非 `chat.completions`），且需手动处理流式响应中的 `phase` 字段（如 `ResearchPlanning`, `WebResearch`, `answer`）；
  - `qwen-vl-ocr` 推荐使用 OpenAI 兼容接口，DashScope SDK 调用方式未在原始文档中体现。

> **注意**：文档 1 中 dashscope CLI 的 `Understanding.call` 示例（`model='opennlu-v1'`）与当前 `tongyi-intent-detect-v3` 模型无关，属过时用法；当前意图模型**必须使用 `chat.completions.create` + `INTENT_MODE` 系统提示**。该不一致已在文档中明确标注为“dashscope CLI 暂不支持 understanding 子命令”，故不构成矛盾，但需开发者规避旧 CLI 方式。

## 限制和注意事项

- **地域限制**：
  - `qwen-deep-research` 仅支持华北2（北京）地域；
  - `qwen-vl-ocr` 系列支持华北2、新加坡、美国（弗吉尼亚）三地；
  - `tongyi-intent-detect-v3` 和 `gui-plus` 支持华北2 与新加坡（文档 1 和文档 3 均明确列出）。
- **协议与 SDK 限制**：
  - `qwen-deep-research` 不支持 OpenAI 兼容接口（文档 2 明确声明），仅 DashScope Python SDK；
  - `gui-plus` 和 `qwen-vl-ocr` 支持 OpenAI 兼容接口，但部分参数（如 `vl_high_resolution_images`, `top_k`）需放入 `extra_body`；
  - `tongyi-intent-detect-v3` 的 `INTENT_MODE` 输出格式需配合自定义 `parse_text` 函数解析 `<tags>`/<tool_call>/`<content>` 结构（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **输入输出约束**：
  - `qwen-vl-ocr` 的 `max_tokens` 上限因模型而异（`qwen3.5-ocr` 为 32768，`qwen-vl-ocr` 为 4096，超限需商务申请）；
  - `qwen-deep-research` 输出为流式多阶段响应，客户端必须按 `phase` 字段区分处理，不可简单等待 `finish_reason == "stop"`；
  - `gui-plus` 的 `system` message 中若含工具定义，需严格遵循 `<tools>` XML 标签包裹及 `<tool_call>...</tool_call>` 工具调用格式。
- **成本与配额**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；其余模型按实际 Token 消耗计费，无通用免费额度说明。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


