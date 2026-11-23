# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，涵盖深度研究、意图理解、GUI交互与OCR文字提取等场景。这些模型在架构设计、输入输出协议和调用流程上具有显著差异，开发者需根据业务需求选择对应模型，并严格遵循其地域、SDK 和参数约束。

## 支持的模型/功能

当前 `more models` 类别下包含以下四类专用模型：

- **Qwen-Deep-Research**：支持两阶段研究流程（反问确认 → 深入分析），自动执行网络搜索、研究规划与报告生成，适用于需要结构化深度分析的场景。[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **tongyi-intent-detect-v3**：毫秒级意图识别模型，支持两种模式：① 同时输出意图标签与[函数调用](../concepts/function-calling.md) JSON（需 `INTENT_MODE` 系统提示）；② 仅输出单一意图标签（需显式声明 tag 列表）。[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **GUI-Plus**：专用于桌面 GUI 自动化交互的多模态模型，支持图像+文本输入，可调用 `computer_use` 工具执行鼠标/键盘操作、截图与状态判断。[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)  
- **Qwen-OCR 系列**（如 `qwen3.5-ocr`, `qwen-vl-ocr-2025-11-20`）：高精度 OCR 模型，支持自定义 Prompt 提取结构化文本（如车票、合同字段），并兼容不同分辨率图像预处理策略。[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)

> **注意**：文档 2 中提及的 `tongyi-intent-detect-v3` 在“支持的模型”表格中列出最大输出为 1,024 Token，但其实际响应为纯标签（如 `alarm_set`）或短 JSON（如 `[{"name": "get_current_weather", ...}]`），远低于该上限；该数值应理解为协议层面允许的最大响应长度，而非典型使用场景下的输出规模。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `model` | 全部 | 必填，精确指定模型名称（如 `"qwen-deep-research"`, `"tongyi-intent-detect-v3"`） | — |
| `messages` | 全部 | 必填，按对话顺序组织的 message 数组；各模型对 `role`（`user`/`system`/`assistant`）和 `content` 结构要求不同 | — |
| `vl_high_resolution_images` | GUI-Plus | 控制图像像素上限策略（`true` 时固定为 12845056 像素） | `false` |
| `output_format` | Qwen-Deep-Research | 指定报告格式：`model_detailed_report`（约 6000 Token）或 `model_summary_report`（约 1500–2000 Token） | `model_detailed_report` |
| `max_tokens` | Qwen-OCR、GUI-Plus | 限制输出长度；Qwen-OCR 不同版本默认值不同（如 `qwen3.5-ocr`: 32768；`qwen-vl-ocr`: 4096） | 见各模型文档 |
| `temperature` / `top_p` | GUI-Plus、Qwen-OCR | 控制生成多样性；二者互斥，建议只设其一 | `0.01` / `0.001`（OCR）、`0.01`（GUI-Plus） |

> **注意**：`top_k`、`repetition_penalty`、`presence_penalty` 等采样参数在 GUI-Plus 和 Qwen-OCR 文档中均有定义，但文档 2（意图模型）未提及——表明 `tongyi-intent-detect-v3` 当前不支持这些参数，调用时传入将被忽略。

## 使用方式

### 地域与端点
所有模型**仅支持华北2（北京）地域**（Qwen-Deep-Research 明确限定；其余三篇文档均推荐迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，且未提及其他地域可用性）。必须使用业务空间专属域名：
- SDK 配置 `base_url` 或 `workspace` + `region="cn-beijing"`
- HTTP 请求 endpoint 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`

### SDK 与接口
- **Qwen-Deep-Research**：**仅支持 Python DashScope SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **tongyi-intent-detect-v3**、**GUI-Plus**、**Qwen-OCR**：同时支持 **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)** 与 **DashScope SDK**（Python/Node.js）。  
- **流式调用**：Qwen-Deep-Research、GUI-Plus、Qwen-OCR 均支持 `stream=true`；意图模型未明确说明，实践中不推荐流式（因其响应极短）。

### 典型调用模式
- **Qwen-Deep-Research**：严格两步调用——先发初始 query 获取 `assistant` 反问内容，再将 user query + assistant 反问 + user 回答拼入第二步 `messages`。  
- **tongyi-intent-detect-v3**：必须设置 `system` message，内容需包含工具定义（`INTENT_MODE`）或意图字典（`just reply with the chosen tag`）。  
- **GUI-Plus / Qwen-OCR**：`messages[0].content` 为 `array`，含 `text` 和/或 `image_url` 对象；`image_url` 内可带 `min_pixels`/`max_pixels`。

## 限制和注意事项

- **地域强约束**：Qwen-Deep-Research 明确要求华北2（北京）地域；其他模型虽未写“仅支持”，但所有文档均将 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 作为首选/唯一示例域名，且无任何其他地域的 endpoint 示例或配置说明，**实际生产环境应默认仅在北京地域可用**。  
- **SDK 限制**：Qwen-Deep-Research 不支持 OpenAI 接口，若强行使用 OpenAI SDK 调用将失败；意图模型、GUI-Plus、Qwen-OCR 均明确支持 OpenAI 兼容模式。  
- **参数兼容性**：`enable_thinking`、`vl_high_resolution_images`、`top_k` 等为非 OpenAI 标准参数，通过 DashScope SDK 需置于 `extra_body`，通过 OpenAI SDK 或 HTTP 需作为顶层参数传递。  
- **图像处理差异**：GUI-Plus 与 Qwen-OCR 的 `min_pixels`/`max_pixels` 单位均为**总像素数**，但计算基准不同（GUI-Plus 文档未说明像素/Token 比例；Qwen-OCR 明确区分 `32×32` 与 `28×28`）。直接复用参数值可能导致图像缩放异常。  
- **免费额度**：仅 `tongyi-intent-detect-v3` 文档明确列出 100 万 Token 免费额度（有效期 90 天）；其他模型未提及其免费策略，需查阅控制台或计费文档。

## 来源文档

- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


