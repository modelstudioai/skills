# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、深度研究、OCR识别与GUI自动化等。这些模型在特定任务上经过优化，具备更强的专业能力与更高的执行效率，适用于需要精准语义解析、多步推理、图文理解或界面交互的业务场景。

## 支持的模型/功能

当前 `more models` 类别下支持以下核心模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、工具编排等场景。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，支持两阶段研究流程（反问确认 + 深度分析），可联网检索并生成结构化研究报告，**仅限华北2（北京）地域调用**，且**仅支持 DashScope Python SDK**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr-*` 等，支持高精度图文提取与结构化信息抽取，兼容 OpenAI 接口与 DashScope API，覆盖华北2（北京）、新加坡、美国（弗吉尼亚）三地 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI自动化模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专用于桌面界面理解与操作指令生成，支持带思考链（`enable_thinking`）和高分辨率图像处理（`vl_high_resolution_images`）。

> **注意**：文档 4 中对 `max_pixels` 的默认值描述存在矛盾——其正文称“默认值为1003520”，但参数表格中又注明“默认值和最大值和 [vl_high_resolution_images](raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 的取值有关”，而该链接实际指向自身（路径错误）。应以实际 SDK 行为和控制台文档为准，建议显式传入 `max_pixels` 或启用 `vl_high_resolution_images=True` 明确控制分辨率策略。

## 关键参数

| 参数 | 适用模型 | 说明 | 备注 |
|--------|-----------|------|------|
| `model` | 全部 | 必填，指定模型名称（如 `"tongyi-intent-detect-v3"`） | — |
| `messages` | 全部 | 必填，按角色（`system`/`user`/`assistant`）组织的对话历史 | OCR 与 GUI-Plus 支持 `image_url` 类型内容 |
| `output_format` | `qwen-deep-research` | 可选，取值 `model_detailed_report`（默认）或 `model_summary_report` | 仅 DashScope SDK 支持 |
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus` | 控制输入图像缩放边界，单位为像素 | 像素→[Token](../concepts/token.md) 转换规则因模型而异（如 `32×32`/`28×28`） |
| `vl_high_resolution_images` | `gui-plus` | 布尔值，启用后忽略 `max_pixels`，固定上限为 `12845056` 像素 | 非 OpenAI 标准参数，需通过 `extra_body` 传入 |
| `enable_thinking` | `gui-plus-2026-02-26` | 布尔值，开启后返回 `reasoning_content` 字段 | 仅混合思考模型支持 |

## 使用方式

### 通用前提
- 已获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 在控制台「业务空间详情」页获取；
- 各地域 endpoint 示例：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

### 调用示例要点
- **意图识别**：需在 `system` 消息中声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)模式）或指定意图字典（标签模式）；
- **深度研究**：必须分两步调用（第一步获取反问，第二步传入反问+用户澄清），且仅 DashScope SDK 支持流式响应；
- **OCR / GUI-Plus**：`user` 消息 `content` 为数组，包含 `{"type": "image_url", "image_url": {"url": "..."} }` 和可选 `{"type": "text", "text": "prompt"}`；
- **[流式输出](../concepts/streaming-output.md)**：设置 `stream=true`，OCR 模型支持 `stream_options.include_usage=true` 获取末块 [Token](../concepts/token.md) 统计。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`tongyi-intent-detect-v3` 和 `qwen3.5-ocr` 支持多地域，但需匹配对应 `base_url` 和 `region` 配置。
- **SDK 限制**：`qwen-deep-research` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Java SDK**；`dashscope CLI` 当前不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **图像参数差异**：`qwen3.5-ocr` 与 `qwen-vl-ocr` 系列的 `min_pixels`/`max_pixels` 默认值及像素-[Token](../concepts/token.md) 换算规则不同，务必按模型文档核对（如 `qwen3.5-ocr` 默认 `min_pixels=3072`，对应 `3×32×32`）。
- **输出解析**：意图模型返回含 `<tags>`/<tool_call>/`<content>` 的特殊格式，需用正则+JSON 解析（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中 `parse_text` 示例）。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 Token 免费额度，详见对应文档注释链接。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


