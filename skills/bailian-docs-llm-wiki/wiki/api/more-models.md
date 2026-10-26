# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，覆盖意图理解、深度研究、OCR文字识别和GUI界面交互等场景。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，兼顾性能、稳定性与成本效率。开发者可根据具体任务需求选择对应模型，并按规范配置参数与消息结构。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、工具编排等场景。该模型提供两种模式：`INTENT_MODE`（输出结构化工具调用）与纯标签分类（输出预定义意图 ID），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，专用于长周期、多阶段的研究任务，支持自动反问澄清、网络搜索、研究报告生成（详版/摘要版），**仅限华北2（北京）地域使用**，且**仅支持 Python DashScope SDK 调用**，不兼容 OpenAI 接口 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR 文字识别模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等版本，支持图像文本提取、结构化信息抽取（如车票、合同关键字段），兼容 OpenAI 和 DashScope 两种调用方式，支持 `min_pixels`/`max_pixels` 图像分辨率控制。
- **GUI 界面交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），面向桌面自动化任务，可解析 UI 截图并生成鼠标键盘操作指令（如 `left_click`、`type`），需配合 `<tools>` 声明与 `<tool_call>` 标签格式化输出。

> **注意**：文档 4 中对 `vl_high_resolution_images` 参数的默认值描述为 `false`，但其 `max_pixels` 默认值（1003520）与 `vl_high_resolution_images=true` 时的固定上限（12845056）存在显著差异；而文档 3 中 OCR 模型的 `min_pixels`/`max_pixels` 默认值均基于明确像素计算（如 3072、8388608）。二者参数设计逻辑一致，但 GUI-Plus 文档未说明 `vl_high_resolution_images=false` 时 `max_pixels` 的实际生效机制，建议以实测为准或参考 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 的像素计算规则。

## 关键参数

所有模型均支持通用 LLM 参数（如 `temperature`、`top_p`、`max_tokens`、`stop`），但部分参数为非 OpenAI 标准，需通过 `extra_body`（Python SDK）或顶层字段（HTTP/curl）传入：

- **图像处理相关**：
  - `min_pixels` / `max_pixels`：控制输入图像缩放阈值，单位为像素。不同模型像素/[Token](../concepts/token.md) 换算不同（如 `qwen3.5-ocr` 为 `32×32`/[Token](../concepts/token.md)，`qwen-vl-ocr` 为 `28×28`/[Token](../concepts/token.md)）。
  - `vl_high_resolution_images`（仅 GUI-Plus）：启用高分辨率策略，此时 `max_pixels` 失效，图像被强制缩至 12845056 像素上限。
- **输出控制**：
  - `output_format`（仅 `qwen-deep-research`）：取值 `model_detailed_report`（默认，~6000 Token）或 `model_summary_report`（~1500–2000 Token）。
  - `enable_thinking`（仅 `gui-plus-2026-02-26`）：开启后返回 `reasoning_content` 字段，用于调试思考链。
- **流式响应**：
  - `stream`：布尔值，启用[流式输出](../concepts/streaming-output.md)。
  - `stream_options.include_usage`：在最后一个数据块中返回 `usage`（输入/输出 Token 数）。

## 使用方式

### 基础准备
- 获取并配置 API Key（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- **强烈建议迁移至业务空间专属域名**（华北2/新加坡地域），以获得更高性能与稳定性：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（`{WorkspaceId}` 在控制台业务空间详情页查看）。

### 调用示例（核心差异）
- **意图识别**：必须设置 System Message，明确声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或 `just reply with the chosen tag.`（纯标签），并注入工具定义或意图字典。
- **深度研究**：采用两阶段调用：第一阶段发送初始研究主题，解析模型反问内容；第二阶段将用户澄清回复连同历史消息一并提交，触发深度分析。
- **OCR / GUI-Plus**：`messages.content` 必须为数组，包含 `image_url`（含 `url` 字段）与可选 `text`（Prompt），`role` 固定为 `user`；GUI-Plus 还需在 System Message 中声明 `<tools>` 与 `<tool_call>` 输出格式。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR 与 GUI-Plus 支持华北2、新加坡、美国（弗吉尼亚）三地，但各地区 endpoint 不同，需严格匹配 `base_url`。
- **SDK 限制**：
  - `qwen-deep-research` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Java SDK**，仅 Python DashScope SDK 可用。
  - `dashscope CLI` 当前不支持 `understanding` 子命令，意图识别需用 Python SDK（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **图像参数冲突**：OCR 文档明确区分了不同模型的 `min_pixels`/`max_pixels` 默认值与换算逻辑，而 GUI-Plus 文档中 `vl_high_resolution_images` 的行为描述存在模糊性（如 `max_pixels` 在 `false` 时是否完全生效），实际使用应优先验证。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度，其他模型未在原始文档中提及免费政策。
- **响应解析**：意图识别返回含 `<tags>`、<tool_call>、`<content>` 的定制化 XML 结构，需用正则+JSON 解析（如 `parse_text` 函数）；深度研究返回多阶段 `phase`（如 `WebResearch`、`answer`），需按 `status` 和 `finished` 字段判断流式进度。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


