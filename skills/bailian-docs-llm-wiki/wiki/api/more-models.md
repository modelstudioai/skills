# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、深度研究、OCR识别与GUI自动化等。这些模型在特定任务上具备更强的性能和更优的推理效率，适用于需要高精度、低延迟或复杂[多模态](../concepts/multi-modal.md)交互的业务场景。开发者可根据具体需求选择对应模型，并遵循统一的 API 调用规范。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、智能助手工具编排等场景。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，支持两阶段交互式研究（反问确认 + 深度分析），可自动规划研究路径、执行网络搜索并生成结构化报告，**仅限华北2（北京）地域调用**。
- **OCR识别模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等版本，支持图像文本提取、结构化信息抽取（如车票、合同关键字段），兼容 OpenAI 接口与 DashScope SDK。
- **GUI自动化模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专为桌面界面交互设计，支持基于截图的鼠标/键盘操作指令生成，需配合 `computer_use` 工具函数使用。

> **注意**：文档 4 中对 `vl_high_resolution_images` 参数的默认值描述为 `false`，但其示例代码中显式传入 `True`；而文档 3 对同名参数未作说明。实际调用时请以 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 的 `max_pixels` 行为为准——该参数仅在 `vl_high_resolution_images=false` 时生效，否则像素上限固定为 `12845056`。

## 关键参数

所有模型均支持通用控制参数（部分为非 OpenAI 标准参数，需通过 `extra_body` 传入）：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `temperature` | `float` | `0.01` | 控制输出随机性，建议保持默认；与 `top_p` 二选一设置 |
| `top_p` | `float` | `0.001`（OCR）、`0.01`（GUI-Plus） | 核采样阈值，同上 |
| `max_tokens` | `integer` | 按模型而异（如 `qwen3.5-ocr`: 32768；`gui-plus`: 模型最大输出长度） | 限制响应长度，超长将被截断 |
| `min_pixels` / `max_pixels` | `integer` | OCR 模型：`3072` / `8388608`；GUI-Plus：`3136` / `1003520`（`vl_high_resolution_images=false` 时） | 图像预处理像素阈值，影响识别精度与 [Token](../concepts/token.md) 消耗 |
| `vl_high_resolution_images` | `boolean` | `false` | GUI-Plus 专用，启用后忽略 `max_pixels`，强制使用高分辨率策略 |
| `enable_thinking` | `boolean` | — | 仅 `gui-plus-2026-02-26` 支持，开启后返回 `reasoning_content` 字段 |

## 使用方式

### 域名与认证
- **必须使用业务空间专属域名**：华北2（北京）、新加坡、美国（弗吉尼亚）地域均已上线新域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 明确指出其“能够为推理请求提供卓越的性能和更高的稳定性”，强烈建议迁移。
- **API Key 配置**：需提前在百炼控制台获取，并通过环境变量（`DASHSCOPE_API_KEY`）或 SDK 初始化参数传入。

### 调用协议
- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：适用于 `tongyi-intent-detect-v3`、`qwen3.5-ocr`、`gui-plus` 等模型，`base_url` 需按地域配置为 `.../compatible-mode/v1`。
- **DashScope 原生 SDK**：`qwen-deep-research` **仅支持 DashScope Python SDK**（文档 2 明确说明“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”），且需设置 `dashscope.base_http_api_url`。
- **消息格式差异**：
  - 意图模型需在 `system` 消息中声明 `Response in INTENT_MODE.` 或指定意图字典；
  - OCR 与 GUI-Plus 模型的 `user` 消息 `content` 为数组，支持 `text` 与 `image_url` 混合输入；
  - `qwen-deep-research` 采用两阶段调用：先发起研究请求获取澄清问题，再将问题+用户回答作为上下文二次调用。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR 与 GUI-Plus 在多地域可用，但需匹配对应 `base_url` 和 API Key。
- **流式支持**：`qwen-deep-research` 仅支持流式响应（`stream=True`），其他模型可选；流式响应中需解析 `phase` 字段（如 `ResearchPlanning`、`WebResearch`）判断当前处理阶段。
- **[Token](../concepts/token.md) 成本与免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 [Token](../concepts/token.md) 免费额度，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 表格。
- **图像处理约束**：OCR 与 GUI-Plus 模型对输入图像有严格像素范围要求（如 `min_pixels=3072`），低于阈值将放大导致失真，高于 `max_pixels` 将缩小损失细节；`qwen-deep-research` 不接受图像输入。
- **工具调用解析**：意图模型返回内容含 `<tags>`、<tool_call>、`<content>` 等自定义标签，需用正则解析（文档 1 提供 `parse_text` 示例），不可直接 JSON 解析。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


