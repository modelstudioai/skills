# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、机器翻译、深度研究、OCR文字识别和GUI界面交互等能力。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于需要高精度、低延迟或特定领域适配的生产级应用。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、智能助手决策等场景。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **机器翻译模型**：`qwen-mt-plus`，支持多语言互译、术语干预、翻译记忆与领域提示，适用于技术文档、本地化内容等专业翻译任务。
- **深度研究模型**：`qwen-deep-research`，仅限华北2（北京）地域，采用两阶段流程（反问确认 → 深入研究），自动规划研究路径、执行网络搜索并生成结构化报告。注意该模型**暂不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Java SDK**，仅可通过 Python DashScope SDK 调用。
- **OCR文字识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr-*` 等，支持图像文本提取、结构化信息抽取（如车票、合同字段），兼容多分辨率输入与自定义 Prompt。
- **GUI界面交互模型**：`gui-plus` 及其版本（如 `gui-plus-2026-02-26`），专为桌面自动化设计，可解析界面截图、生成鼠标键盘操作指令，支持 `vl_high_resolution_images` 与 `enable_thinking` 等增强参数。

> **注意**：文档 4（Qwen-OCR）中 `min_pixels` 默认值标注为 `32 * 32 * 3 = 3072`（对应 `qwen3.5-ocr`），而文档 5（GUI-Plus）中同名参数默认值写为 `3136` 且未限定模型版本。实际调用时请严格按目标模型文档确认——`qwen3.5-ocr` 必须使用 `3072`，`qwen-vl-ocr` 系列应使用 `3136`。该差异已在 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中明确区分。

## 关键参数

所有模型均支持通用 LLM 参数（如 `temperature`、`top_p`、`max_tokens`、`stop`），但部分参数为模型特有或非 OpenAI 标准：

- **`translation_options`**（`qwen-mt-plus`）：必传对象，含 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）、`domains`（领域提示）等子字段。
- **`output_format`**（`qwen-deep-research`）：可选值为 `model_detailed_report`（默认，约6000 Token）或 `model_summary_report`（约1500–2000 Token）。
- **`min_pixels` / `max_pixels`**（`qwen3.5-ocr`, `gui-plus`）：控制图像预处理缩放，单位为像素；不同模型的像素/Token 换算关系不同（如 `qwen3.5-ocr` 为 `32×32`/Token，`qwen-vl-ocr` 为 `28×28`/Token），详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **`vl_high_resolution_images`**（`gui-plus`）：布尔值，启用后忽略 `max_pixels`，强制将图像像素上限设为 `12845056`。
- **`enable_thinking`**（`gui-plus-2026-02-26`）：启用后返回 `reasoning_content` 字段，需通过 `extra_body` 传入（Python SDK）。

## 使用方式

### 基础前提
- 已在百炼控制台创建业务空间并获取对应地域的 API Key；
- 配置环境变量 `DASHSCOPE_API_KEY`；
- 安装对应 SDK（[DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK）。

### 域名与端点
**强烈建议迁移至业务空间专属域名**（性能与稳定性更优）：
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为业务空间 ID，可在控制台「业务空间详情」页查看。旧域名（如 `dashscope.aliyuncs.com`）仍可用，但不推荐用于生产环境。

### 调用示例要点
- **意图识别**：必须在 `system` message 中声明 `Response in INTENT_MODE.` 并注入工具定义（JSON 格式），响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构。
- **机器翻译**：`translation_options` 必须作为 `extra_body`（OpenAI SDK）或顶层参数（HTTP/curl）传入。
- **深度研究**：严格遵循两阶段流程（先反问、再深入），第二步需将第一步的 `assistant` 回复作为历史消息传入。
- **OCR 与 GUI-Plus**：`messages.content` 为数组，需混合 `text` 和 `image_url` 对象；`image_url.url` 支持公网 URL 或 Base64 Data URL。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`）支持北京、新加坡、美国（弗吉尼亚）三地。
- **SDK 限制**：`qwen-deep-research` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；`dashscope CLI` 当前不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **输出长度**：`qwen-vl-ocr` 的 `max_tokens` 默认为 4096，如需提升至 4097–8192，须联系商务经理申请，并提供主账号ID、图像类型、QPS等信息。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 Token 免费额度，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 表格。
- **流式响应**：所有模型均支持 `stream=true`，但 `qwen-deep-research` 的流式响应包含多阶段状态（`ResearchPlanning`/`WebResearch`/`answer`），客户端需解析 `output.message.phase` 字段以区分阶段。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


