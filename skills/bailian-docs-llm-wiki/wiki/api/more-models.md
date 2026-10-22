# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，覆盖意图理解、OCR识别、深度研究和GUI自动化等场景。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于需要高精度、低延迟或结构化输出的生产环境。所有模型均需配置有效的 API Key 与对应地域的 `base_url`。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式：  
  - `INTENT_MODE`：同时输出意图标签与结构化[函数调用](../concepts/function-calling.md) JSON（需在 System Message 中声明 `Response in INTENT_MODE.` 并传入工具定义）；  
  - 纯意图分类模式：仅返回预定义标签（如 `alarm_set`），支持单 [Token](../concepts/token.md) 输出优化响应速度。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **OCR 模型**：`qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等，支持图像文本提取与结构化信息抽取（如车票字段），兼容多分辨率输入与自定义 Prompt。  
- **深度研究模型**：`qwen-deep-research`，仅限华北2（北京）地域，采用两阶段交互流程（反问确认 → 深入研究），自动执行网络搜索、内容分析与报告生成。  
- **GUI 自动化模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专用于桌面界面理解与操作，支持截图输入、工具调用（如 `computer_use`）及混合思考模式（需显式启用 `enable_thinking`）。该模型的详细接口规范见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：`qwen-deep-research` 明确声明“**仅支持华北2（北京）地域**”，且“**暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**”，而其他模型（如 `tongyi-intent-detect-v3`、`qwen3.5-ocr`、`gui-plus`）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。此为关键能力差异，不可跨模型泛化调用方式。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus` | 图像像素阈值控制缩放行为。`qwen3.5-ocr` 按 `32×32`/[Token](../concepts/token.md) 计算，`gui-plus` 默认按 `28×28`/[Token](../concepts/token.md)（即 `min_pixels=3136`）；`qwen-vl-ocr` 系列旧模型沿用 `28×28` 规则。详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。 | `qwen3.5-ocr`: `min=3072`, `max=8388608`；`gui-plus`: `min=3136`, `max=1003520`（当 `vl_high_resolution_images=false`） |
| `output_format` | `qwen-deep-research` | 指定研究报告格式：`model_detailed_report`（约6000 Token）或 `model_summary_report`（约1500–2000 Token）。 | `model_detailed_report` |
| `vl_high_resolution_images` | `gui-plus` | 启用高分辨率图像处理（上限 `12845056` 像素），此时 `max_pixels` 参数失效。 | `false` |
| `enable_thinking` | `gui-plus-2026-02-26`（仅此版本） | 开启后返回 `reasoning_content` 字段，用于调试思考链。需通过 `extra_body` 传递。 | `false` |
| `temperature` / `top_p` | 所有模型 | 控制生成多样性。二者互斥，建议仅设其一；`tongyi-intent-detect-v3` 文档未提及，应保持默认（0.01/0.001）以保障分类稳定性。 | `temperature=0.01`, `top_p=0.001`（OCR/GUI-Plus） |

## 使用方式

### 基础前提
- 已获取并配置 API Key（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；
- 根据所选地域（华北2、新加坡、美国弗吉尼亚）替换 `base_url` 中的 `{WorkspaceId}` 与域名后缀（如 `cn-beijing.maas.aliyuncs.com`）；
- 安装对应 SDK（[DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK）。

### 调用示例要点
- **意图模型**：System Message 必须包含明确指令（`Response in INTENT_MODE.` 或 `just reply with the chosen tag.`），工具/意图字典需 JSON 序列化后嵌入；解析响应需使用正则提取 `<tags>`、<tool_call>、`<content>` 三段内容。
- **OCR 模型**：`messages.content` 必须为 `array`，含 `image_url` 和可选 `text`（Prompt）；`min_pixels`/`max_pixels` 需与模型像素规则匹配。
- **深度研究模型**：必须分两步调用——第一步仅传 `user` 消息获取反问，第二步将 `user`+`assistant`（反问）+`user`（澄清）构成完整对话历史；仅支持 DashScope Python SDK 流式调用。
- **GUI-Plus 模型**：`system` 消息需严格定义工具签名与响应格式（如 `<tool_call>...</tool_call>` 包裹 JSON），`image_url` 必须为有效 URL 或 Base64；高分辨率需显式设置 `extra_body={"vl_high_resolution_images": true}`。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；OCR 与 GUI-Plus 支持多地域，但需确保 API Key 与 `base_url` 地域一致。
- **SDK 限制**：`qwen-deep-research` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Java SDK；`dashscope CLI` 当前不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **参数兼容性**：`top_k`、`repetition_penalty`、`presence_penalty` 等非 OpenAI 标准参数，在 OpenAI SDK 中必须置于 `extra_body` 对象内（如 `extra_body={"top_k": 1}`），否则被忽略。
- **成本与配额**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度；OCR 与 GUI-Plus 按实际输入/输出 Token 计费，无通用免费额度。
- **图像处理**：`qwen3.5-ocr` 与 `gui-plus` 的 `min_pixels`/`max_pixels` 单位均为**总像素数**（宽×高），非分辨率数值；错误设置可能导致图像失真或 API 报错。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


