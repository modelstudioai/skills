# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，包括意图理解、深度研究、OCR文字识别和GUI界面交互等。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于高精度、低延迟、多模态等专业场景。开发者需根据任务类型选择对应模型，并注意各模型在地域支持、调用方式和参数约束上的差异。

## 支持的模型/功能

当前 `more models` 类别下主要包含以下四类专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级用户意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、智能助手决策等场景。该模型提供两种输出模式：带工具调用的结构化响应（需 `Response in INTENT_MODE.` 系统指令）和纯标签分类响应（需显式定义意图字典）[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，专用于长周期、多阶段的研究任务，支持自动反问澄清、网络搜索、研究规划与报告生成。**仅支持华北2（北京）地域**，且**仅可通过 Python DashScope SDK 调用**，不支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md) [原文标题](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR 文字识别模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr` 等系列，支持图像中文字提取与结构化信息抽取（如车票、合同关键字段）。支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)与 DashScope API，覆盖华北2（北京）、新加坡、美国（弗吉尼亚）三地 [原文标题](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI 界面交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），面向桌面自动化任务，可解析 UI 截图并生成鼠标/键盘操作指令（如点击、输入、等待）。支持 `vl_high_resolution_images` 等专用参数以适配高分辨率截图需求 [原文标题](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)”，而文档 3 和文档 4 均明确支持 OpenAI 兼容接口。若开发者尝试用 OpenAI SDK 调用 `qwen-deep-research`，将失败——此为模型能力边界，非文档错误。

## 关键参数

所有模型均支持通用 LLM 参数（如 `temperature`、`top_p`、`max_tokens`、`stop`），但部分模型引入了任务专属参数：

- **图像处理类模型（OCR、GUI-Plus）**：
  - `min_pixels` / `max_pixels`：控制输入图像缩放阈值，单位为像素；不同模型对应像素/Tokens 比例不同（如 `qwen3.5-ocr` 为 `32×32`/token，`qwen-vl-ocr` 为 `28×28`/token）。
  - `vl_high_resolution_images`（仅 GUI-Plus）：布尔开关，启用后忽略 `max_pixels`，强制使用固定上限 `12845056` 像素。
  - `enable_thinking`（仅 GUI-Plus）：控制是否返回 `reasoning_content` 字段，需通过 `extra_body` 传入。

- **意图理解模型**：
  - 无额外参数，但**系统消息（system prompt）格式严格决定输出行为**：含 `Response in INTENT_MODE.` 触发工具调用格式；含 `choose one tag from the tag list` 触发纯标签输出。

- **深度研究模型**：
  - `output_format`：指定报告格式，可选 `model_detailed_report`（默认，约6000 Token）或 `model_summary_report`（约1500–2000 Token）。

## 使用方式

### 基础前提
- 已获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`。
- 根据地域选择**业务空间专属域名**（强烈建议迁移）：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（见[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。

### 调用路径
| 模型类型             | OpenAI 兼容接口 | DashScope SDK | 备注 |
|----------------------|-----------------|----------------|------|
| `tongyi-intent-detect-v3` | ✅              | ✅             | —    |
| `qwen-deep-research`       | ❌              | ✅（Python only） | 文档 2 明确限制 |
| `qwen3.5-ocr` / `gui-plus` | ✅              | ✅             | —    |

### 典型调用示例
- **意图识别（工具调用）**：`system` 消息中必须包含工具定义 JSON 和 `Response in INTENT_MODE.` 指令，响应需用正则 `parse_text()` 解析 `<tags>`/<tool_call>/`<content>` 结构。
- **深度研究**：必须执行**两阶段调用**——第一阶段获取模型反问，第二阶段将反问+用户澄清作为上下文再次请求。
- **OCR/GUI-Plus 图像输入**：`messages.content` 必须为数组，内含 `{"type": "image_url", "image_url": {"url": "..."} }` 和可选 `{"type": "text", "text": "prompt"}` 对象。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR 和 GUI-Plus 模型支持多地域，但需匹配对应 `base_url` 和 API Key 地域。
- **SDK 限制**：`qwen-deep-research` 不支持 OpenAI SDK 或 HTTP 直接调用，仅限 Python DashScope SDK；`dashscope CLI` 当前不支持 `understanding` 子命令（见[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **图像参数冲突**：GUI-Plus 的 `max_pixels` 在 `vl_high_resolution_images=true` 时被忽略，而 OCR 模型无此行为——二者不可混用参数逻辑。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 Token 免费额度，其他模型未在原始文档中声明免费额度。
- **流式响应差异**：`qwen-deep-research` 响应体含 `phase`（如 `ResearchPlanning`, `WebResearch`）和 `status` 字段，用于跟踪研究阶段；OCR/GUI-Plus 流式响应仅遵循标准 OpenAI `delta` 格式，无阶段语义。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


