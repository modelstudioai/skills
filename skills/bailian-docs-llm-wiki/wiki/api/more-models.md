# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，包括深度研究、意图理解、OCR 文字识别和 GUI 界面交互等。这些模型通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，支持多地域部署与精细化参数控制，适用于需要高精度、强领域适配性的生产场景。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **Qwen-Deep-Research**：面向复杂研究任务的两阶段模型，支持反问确认 → 深入研究流程，自动执行网络搜索、研究规划与报告生成，输出含参考文献的结构化报告。仅支持华北2（北京）地域，且**仅可通过 Python DashScope SDK 调用**，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **tongyi-intent-detect-v3**：毫秒级意图识别模型，支持两种模式：① 同时输出意图标签与[函数调用](../concepts/function-calling.md) JSON（需在 system prompt 中声明 `Response in INTENT_MODE.`）；② 仅输出预定义意图标签（需指定 `just reply with the chosen tag`）。支持多地域，推荐使用业务空间专属域名以提升稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-OCR 系列（如 `qwen3.5-ocr`, `qwen-vl-ocr`）**：专用于图像文字提取与结构化信息抽取，支持多分辨率图像输入（通过 `min_pixels`/`max_pixels` 控制），兼容 OpenAI 接口与 DashScope API，支持流式与非[流式输出](../concepts/streaming.md) [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（如 `gui-plus-2026-02-26`）**：面向桌面 GUI 自动化任务的视觉-语言模型，支持基于截图的鼠标/键盘操作指令生成（如 `left_click`, `type`, `wait`），需配合 `<tools>` 描述与 `<tool_call>` 标签格式返回[函数调用](../concepts/function-calling.md) [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 与文档 3 均提及“建议迁移至业务空间专属域名”，但文档 2 明确列出新加坡、中国香港地域，而文档 3 仅列出华北2（北京）、新加坡地域，未提中国香港。实际部署时请以控制台中业务空间详情页显示的可用地域为准。

## 关键参数

所有模型均支持通用 LLM 参数（如 `temperature`, `top_p`, `max_tokens`, `stop`, `seed`），但部分参数为模型特有或行为差异显著：

- **`output_format`**（仅 Qwen-Deep-Research）：控制报告详略程度，可选 `model_detailed_report`（默认，~6000 Token）或 `model_summary_report`（~1500–2000 Token）。
- **`min_pixels` / `max_pixels`**（Qwen-OCR 与 GUI-Plus）：控制图像预处理缩放阈值。注意不同模型像素/Token 换算规则不同：
  - `qwen3.5-ocr` / `qwen-vl-ocr-2025-11-20`：每 Token = `32×32` 像素；
  - `qwen-vl-ocr` 及更早版本：每 Token = `28×28` 像素 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **`vl_high_resolution_images`**（仅 GUI-Plus）：布尔开关，启用后忽略 `max_pixels`，强制将图像缩放到固定上限 `12845056` 像素（对应 16384 Token）。
- **`enable_thinking`**（仅 GUI-Plus 混合思考模型）：启用后返回 `reasoning_content` 字段，用于调试推理链路。
- **`phase` / `status` 字段**（仅 Qwen-Deep-Research 响应体）：用于识别当前执行阶段（`ResearchPlanning`, `WebResearch`, `answer`, `KeepAlive`），客户端需据此解析流式响应 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

## 使用方式

### 地域与端点配置
所有模型均需使用业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），其中 `{WorkspaceId}` 从控制台获取。地域映射如下：
- 华北2（北京）：`cn-beijing`
- 新加坡：`ap-southeast-1`
- 美国（弗吉尼亚）：`us-east-1`

> **注意**：Qwen-Deep-Research **强制要求华北2（北京）地域**，且必须配置 `dashscope.base_http_api_url`（Python SDK）或 `base_url`（OpenAI SDK），否则调用失败 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

### SDK 调用示例（通用模式）
- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：设置 `base_url` 为对应地域专属地址，`model` 传入模型名（如 `"qwen3.5-ocr"`），`messages` 中 `content` 为数组（支持 `text` + `image_url` 混合）。
- **DashScope SDK**：
  - Qwen-Deep-Research：使用 `dashscope.Generation.call()`，**不可用 `chat.completions.create()`**；
  - 其他模型（intent-detect, OCR, GUI-Plus）：使用 `client.chat.completions.create()`，并传入 `workspace` 和 `region` 参数。

### 输入构造要点
- **Qwen-Deep-Research**：严格两步调用。第一步仅 `user` 消息；第二步需包含原始 `user` 消息、`assistant` 的反问内容、用户对反问的回答（新 `user` 消息）。
- **tongyi-intent-detect-v3**：system message 必须明确指定输出模式（`INTENT_MODE` 或 `just reply with the chosen tag`），且工具/意图列表需 JSON 序列化后嵌入 prompt。
- **OCR / GUI-Plus**：`messages[0].content` 必须为数组，每个元素含 `type`（`text` 或 `image_url`），`image_url.url` 支持公网 URL 或 Base64 Data URL。

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research 仅支持华北2（北京）地域；其他模型虽支持多地域，但免费额度、延迟与稳定性因地域而异，生产环境务必使用业务空间专属域名。
- **SDK 限制**：Qwen-Deep-Research **不支持 Java SDK 与 OpenAI 兼容接口**，仅支持 Python DashScope SDK；GUI-Plus 与 OCR 模型推荐使用 OpenAI 兼容接口或 DashScope Python SDK，dashscope CLI 不支持 understanding 子命令 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **输入约束**：
  - Qwen-Deep-Research：`messages` 中 `assistant` 消息仅在第二步有效，且 `content` 必须为模型第一步返回的完整反问文本。
  - OCR / GUI-Plus：`image_url.url` 若为本地文件，需先上传至 OSS 或转换为 Base64；`min_pixels`/`max_pixels` 必须满足模型规定的取值范围，越界将导致 400 错误。
- **输出解析**：Qwen-Deep-Research 流式响应中 `phase` 和 `status` 字段是状态机关键，客户端需按 `typing`/`streamingQueries`/`finished` 等状态做差异化处理；tongyi-intent-detect-v3 的[函数调用](../concepts/function-calling.md)结果需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **成本与额度**：tongyi-intent-detect-v3 提供 90 天内 100 万 Token 免费额度；Qwen-OCR 与 GUI-Plus 按实际输入/输出 Token 计费，`max_tokens` 设置过高会增加成本且无实际收益。

## 来源文档

- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


