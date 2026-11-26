# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，覆盖意图理解、深度研究、OCR文字识别和GUI界面交互等场景。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持精细化参数控制与多阶段工作流，适用于需要高精度、强领域适配能力的生产级应用。所有模型均需使用业务空间专属域名以获得最佳性能与稳定性。

## 支持的模型/功能

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式：  
  - `INTENT_MODE`：同时输出结构化工具调用指令（含函数名与 JSON 参数），适用于 Agent 工具编排；  
  - 纯标签模式：从预定义意图字典中单选一个语义标签，适用于轻量级分类任务。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **深度研究模型**：`qwen-deep-research`，专用于长周期、多步骤的研究型任务，具备反问确认、研究规划、网络搜索与报告生成四阶段能力，**仅支持华北2（北京）地域**，且**当前仅可通过 DashScope Python SDK 调用**（不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK）[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。  
- **OCR 模型**：`qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20`、`qwen-vl-ocr` 等，支持图像文本提取与结构化信息抽取（如车票字段），兼容 OpenAI 和 DashScope 接口，支持多地域（华北2、新加坡、美国弗吉尼亚）。  
- **GUI 交互模型**：`gui-plus`，面向桌面自动化任务，可解析截图并生成鼠标/键盘操作指令（如 `left_click`, `type`, `wait`），支持 `enable_thinking` 开启推理过程返回 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 明确指出 `qwen-deep-research` “仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档 3 和文档 4 均列出新加坡、美国弗吉尼亚等多地域支持。该模型的地域与 SDK 限制是明确且唯一的，其他模型的多地域描述与此不冲突。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `qwen-vl-ocr-*`, `gui-plus` | 图像预处理像素阈值。`qwen3.5-ocr` 等新模型按 `32×32`/token 计算，旧模型按 `28×28`/token；`gui-plus` 的 `max_pixels` 行为受 `vl_high_resolution_images` 控制 | `qwen3.5-ocr`: 3072 / 8388608；`gui-plus`: 3136 / 1003520（`vl_high_resolution_images=False`） |
| `output_format` | `qwen-deep-research` | 报告输出格式：`model_detailed_report`（约6000 [Token](../concepts/token.md)）或 `model_summary_report`（约1500–2000 [Token](../concepts/token.md)） | `model_detailed_report` |
| `enable_thinking` | `gui-plus`（仅 `gui-plus-2026-02-26`） | 是否返回推理过程内容至 `reasoning_content` 字段 | `false` |
| `temperature` / `top_p` | 所有模型（除 `tongyi-intent-detect-v3` 在 `INTENT_MODE` 下建议保持默认） | 控制生成多样性；二者互斥，**建议只设置其一**；`tongyi-intent-detect-v3` 在纯标签模式下对温度敏感，应谨慎调整 | `temperature=0.01`, `top_p=0.001`（OCR/GUI）；`tongyi-intent-detect-v3` 未显式声明，但示例中未设置，视为不生效 |

## 使用方式

- **域名与认证**：所有模型**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。`{WorkspaceId}` 需从控制台业务空间详情页获取。API Key 需已配置至环境变量（`DASHSCOPE_API_KEY`）或 SDK 初始化参数中。  
- **SDK 选择**：  
  - `tongyi-intent-detect-v3` 和 OCR/GUI 模型：支持 OpenAI SDK（通过 `base_url`）与 DashScope SDK；  
  - `qwen-deep-research`：**仅支持 DashScope Python SDK**，且需显式设置 `dashscope.base_http_api_url`（非 `base_url`）[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。  
- **输入格式差异**：  
  - 意图模型：依赖 System Message 中的固定指令（`Response in INTENT_MODE.` 或 `just reply with the chosen tag.`）；  
  - OCR/GUI 模型：`messages[0].content` 必须为 `array`，内含 `text` 和/或 `image_url` 对象；  
  - 深度研究模型：采用两阶段调用：第一阶段传入初始主题获取澄清问题，第二阶段将用户回答与问题一并作为上下文传入。  

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 严格限定于华北2（北京）地域，跨地域调用将失败；OCR 与 GUI 模型支持多地域，但需匹配对应 `base_url` 和 `region`。  
- **参数兼容性**：`top_k`、`repetition_penalty`、`presence_penalty`、`seed`、`stop` 等为非 OpenAI 标准参数，在 OpenAI SDK 中必须通过 `extra_body` 传入（Python）或作为顶层参数（HTTP/curl），否则被忽略。  
- **输出解析**：`tongyi-intent-detect-v3` 在 `INTENT_MODE` 下返回特殊格式（`<tags>`/<tool_call>/`<content>`），**必须使用文档提供的 `parse_text` 函数解析**，不可直接 JSON 解析原始响应体。  
- **成本与配额**：`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（开通后 90 天有效）；`qwen-deep-research` 无免费额度说明，按实际 token 消耗计费；OCR/GUI 模型计费策略需查阅对应定价页。  
- **功能弃用**：文档 1 中提及的 `dashscope CLI understanding` 子命令已明确标注“暂不支持”，开发者应使用 Python SDK 示例代码替代。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


