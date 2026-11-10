# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、机器翻译、深度研究、OCR文字提取和GUI界面交互等。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于需要高精度、低延迟或强领域适配能力的生产级应用。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式——`INTENT_MODE`（输出结构化[函数调用](../concepts/function-calling.md)）和纯意图分类（返回预定义标签），适用于智能客服、Agent 工具路由等场景。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **机器翻译模型**：`qwen-mt-plus`，支持源/目标语言自动识别、术语干预、翻译记忆（TM）及领域提示，适用于技术文档、本地化流水线等专业翻译任务。
- **深度研究模型**：`qwen-deep-research`，仅支持华北2（北京）地域，采用两阶段工作流（反问确认 → 深入研究），可联网检索并生成详尽研究报告，但**暂不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅可通过 DashScope Python SDK 调用。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR 文字提取模型**：`qwen3.5-ocr`、`qwen-vl-ocr` 等系列，支持图像输入（URL 或 Base64）、像素阈值控制（`min_pixels`/`max_pixels`）、结构化 Prompt 提取（如车票字段），适用于票据、合同、文档等非结构化图像解析。
- **GUI 界面交互模型**：`gui-plus` 及其版本（如 `gui-plus-2026-02-26`），专为桌面自动化设计，支持截图理解 + [工具调用](../concepts/tool-calling.md)（如 `computer_use`），需配合系统消息中声明工具签名使用。参见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus`）在文档 2、4、5 中均明确列出新加坡、美国（弗吉尼亚）等多地域支持。该差异非矛盾，而是模型能力本身的地域部署限制，开发者需按模型文档选择对应地域的 API Key 和 endpoint。

## 关键参数

所有模型共享部分通用参数，但行为与默认值存在差异，需特别注意：

| 参数 | 说明 | 默认值/约束 | 文档依据 |
|------|------|-------------|----------|
| `base_url` | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用但**不推荐** | 各地域格式固定，`{WorkspaceId}` 需从控制台获取 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 均强调迁移必要性 |
| `model` | 模型名称，严格区分大小写与版本后缀（如 `qwen3.5-ocr` ≠ `qwen-vl-ocr`） | 无默认值，必填 | 所有文档均列为 `string`（必选） |
| `messages.content` | 对于多模态模型（OCR、GUI-Plus），`content` 为数组，含 `text` 和 `image_url` 对象；`image_url.url` 支持 HTTP URL 或 `data:image/...;base64,...` | `text` 字段若未提供，OCR 模型默认使用 `"Please output only the text content..."` | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)、[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `min_pixels` / `max_pixels` | 图像预处理像素阈值，单位为总像素数；不同模型每 [Token](../concepts/token.md) 对应像素不同（`32×32` 或 `28×28`），直接影响 [Token](../concepts/token.md) 计费与识别精度 | `qwen3.5-ocr`: min=3072, max=8388608；`gui-plus`: min=3136, max 默认 1003520（`vl_high_resolution_images=false`） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)、[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `output_format` | 仅 `qwen-deep-research` 支持，控制报告详略程度 | `model_detailed_report`（默认，~6000 [Token](../concepts/token.md)）或 `model_summary_report`（~1500–2000 Token） | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `translation_options` | 仅 `qwen-mt-plus` 支持，为嵌套对象，含 `source_lang`、`target_lang`、`terms`、`tm_list`、`domains` 等字段 | `source_lang="auto"`，`target_lang` 必填 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |

## 使用方式

### 通用前提
- 已在百炼控制台[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并设为环境变量 `DASHSCOPE_API_KEY`；
- 安装对应 SDK：OpenAI SDK（用于兼容接口）或 DashScope SDK（用于原生接口）；
- 替换 `{WorkspaceId}` 为实际业务空间 ID（控制台 > 业务空间详情页）；
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），避免性能与稳定性风险。

### 模型调用示例要点
- **意图理解**：System Message 必须包含 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或 `just reply with the chosen tag.`（纯意图），且需显式注入工具定义或意图字典（JSON 格式）。
- **机器翻译**：`translation_options` 需作为 `extra_body`（Python OpenAI SDK）或顶层参数（Node.js/HTTP）传入，不可置于 `messages` 内。
- **深度研究**：严格遵循两阶段流程——先调用获取模型反问（`step1_content`），再将初始 query、反问内容、用户澄清组合为 `messages` 进行第二步调用；仅 DashScope Python SDK 支持。
- **OCR 与 GUI-Plus**：`messages` 中 `content` 为数组，`image_url` 和 `text` 顺序无关，但 `text` 用于指定提取指令（如 `"提取发票号码..."`），否则使用默认 Prompt。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；`qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus` 支持北京、新加坡、美国（弗吉尼亚）三地，但各地区 API Key 不互通。
- **接口限制**：`qwen-deep-research` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅 DashScope Python SDK 可用；`tongyi-intent-detect-v3` 的 DashScope CLI 也不支持 `understanding` 子命令，需用 Python SDK。
- **图像参数差异**：`qwen3.5-ocr` 与 `gui-plus` 的 `min_pixels`/`max_pixels` 默认值与计算逻辑一致（均基于 `32×32` 或 `28×28`），但 `gui-plus` 新增 `vl_high_resolution_images` 开关，启用后 `max_pixels` 失效，强制使用 12845056 像素上限。
- **输出解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 响应需用正则解析 `<tags>`、<tool_call>、`<content>` 三段式结构，官方提供 `parse_text()` 示例函数；`qwen-deep-research` 响应为流式 JSON，需按 `phase`（如 `answer`、`WebResearch`）和 `status` 字段判断阶段状态。
- **Token 成本敏感项**：OCR 模型的 `min_pixels`/`max_pixels` 直接影响图像 Token 数（`总像素 / (32×32)` 或 `/ (28×28)`），进而影响计费；深度研究报告的 `output_format` 选项显著影响输出长度（6000 vs 1500 Token），需按需选择。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


