# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、深度研究、GUI界面交互和OCR文字识别等。这些模型在特定任务上具备更强的专业能力与优化性能，开发者可根据业务需求选择调用。所有模型均支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，但部分模型存在地域、SDK 或协议限制。

## 支持的模型/功能

当前 `more models` 类别下主要包含以下四类专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式——同时输出意图与[函数调用](../concepts/function-calling.md)（需 `Response in INTENT_MODE.` 系统指令），或仅输出预定义意图标签（如 `alarm_set`）。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，专用于长周期、多阶段的研究任务（反问确认 → 研究规划 → 网络搜索 → 报告生成），仅支持华北2（北京）地域及 DashScope Python SDK，**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI界面交互模型**：`gui-plus-*`（如 `gui-plus-2026-02-26`），支持图文多模态输入与工具调用，适用于自动化桌面操作（如点击、输入、截图）。支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope SDK。详见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。
- **OCR文字识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr-*` 等，专精于图像中文本内容的高精度提取，支持自定义 Prompt 提取结构化字段（如车票信息）。支持 OpenAI 兼容接口与 DashScope SDK。详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

> **注意**：文档 2 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 OpenAI 兼容接口”，而文档 3 和文档 4 均明确支持 OpenAI 兼容接口。该限制在文档 1 中未提及，属关键差异，开发者务必遵守。

## 关键参数

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 模型名称（必填） | 全部 | 如 `"tongyi-intent-detect-v3"`、`"qwen-deep-research"`、`"gui-plus-2026-02-26"`、`"qwen3.5-ocr"` |
| `messages` | 对话消息数组（必填） | 全部 | `system`/`user`/`assistant` 角色需严格匹配；GUI-Plus 与 Qwen-OCR 的 `user.content` 为数组（支持 `text` + `image_url`）；`qwen-deep-research` 要求两步调用（含 `assistant` 消息作为历史） |
| `vl_high_resolution_images` | 图像高分辨率开关（非 OpenAI 标准） | GUI-Plus | 仅 Python SDK 通过 `extra_body` 传入；设为 `true` 时 `max_pixels` 失效，上限固定为 `12845056` |
| `min_pixels` / `max_pixels` | 图像像素阈值（单位：像素） | GUI-Plus、Qwen-OCR | 默认值与范围因模型而异：`qwen3.5-ocr` 使用 `32×32` 像素/Token，`qwen-vl-ocr` 使用 `28×28`；详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `output_format` | 研究报告格式 | `qwen-deep-research` | 可选 `model_detailed_report`（默认，~6000 Token）或 `model_summary_report`（~1500–2000 Token） |
| `enable_thinking` | 是否开启思考模式（非 OpenAI 标准） | GUI-Plus（仅混合思考模型） | Python SDK 需通过 `extra_body` 传入；开启后返回 `reasoning_content` 字段 |

## 使用方式

### 通用前提
- 已[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并配置至环境变量 `DASHSCOPE_API_KEY`；
- 已安装对应 SDK（[DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK）；
- **必须使用业务空间专属域名**（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 在控制台“业务空间详情”中查看；旧域名（如 `dashscope.aliyuncs.com`）仍可用，但性能与稳定性较低 —— 此迁移建议在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中均被强调。

### 调用示例要点
- **意图理解**：系统消息中必须显式声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)模式）或 `just reply with the chosen tag.`（纯意图模式）；响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构。
- **深度研究**：必须分两步调用：第一步仅 `user` 消息发起请求，捕获模型反问；第二步将 `user` 初始消息、`assistant` 反问、`user` 补充澄清三者按序传入 `messages`。
- **GUI-Plus / Qwen-OCR**：`user.content` 必须为数组，内含 `{"type": "image_url", "image_url": {"url": "..."}}` 和可选 `{"type": "text", "text": "..."}`；图像 URL 支持公网地址或 Base64 Data URL。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**；GUI-Plus 和 Qwen-OCR 支持华北2（北京）、新加坡、美国（弗吉尼亚）三地，但各地区 `base_url` 和 `endpoint` 不同，需严格匹配（见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)）。
- **SDK 限制**：`qwen-deep-research` 不支持 OpenAI 兼容接口与 Java SDK；`tongyi-intent-detect-v3` 的 `dashscope CLI` 不支持 `understanding` 子命令，需用 Python SDK（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **图像参数冲突**：文档 3 中 `vl_high_resolution_images` 的说明存在自引用错误 —— 其链接指向自身（`raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md`），应为笔误，实际逻辑以文档正文为准。
- **OCR 输出长度**：`qwen-vl-ocr` 默认最大输出 `4096` tokens；若需 `4097–8192`，须联系商务经理申请，并提供主账号ID、图像类型、QPS等信息（见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)）。
- **Token 成本与免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 Token 免费额度（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；其他模型未在原始文档中声明免费额度，需按实际用量计费。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


