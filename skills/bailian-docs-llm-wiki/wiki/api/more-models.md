# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖意图理解、法律推理、深度研究、GUI交互与OCR识别等能力。这些模型在通用基座上进行了领域精调或架构增强，支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 调用，适用于高精度、低延迟、多模态等特定业务需求。

## 支持的模型/功能

| 模型名称 | 主要能力 | 适用场景 | 地域支持 | 文档引用 |
|----------|----------|----------|----------|----------|
| `tongyi-intent-detect-v3` | 意图识别与[函数调用](../concepts/function-calling.md)生成（INTENT_MODE）或纯标签分类 | 智能客服路由、Agent 工具选择、对话状态跟踪 | 华北2（北京）、新加坡、中国香港 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `farui-plus` | 法律问答、案情分析、文书生成、合同审查 | 法律咨询、司法辅助、合规审查 | 全地域（需对应地域 API Key） | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `qwen-deep-research` | 多阶段网络检索+结构化报告生成（含 ResearchPlanning/WebResearch/answer 阶段） | 行业调研、竞品分析、学术综述 | **仅华北2（北京）** | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `gui-plus` / `gui-plus-2026-02-26` | GUI 界面理解与自动化操作（支持鼠标/键盘动作调用） | 桌面自动化、RPA、无障碍交互 | 华北2（北京）、新加坡 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | 高精度图像文本提取与结构化信息抽取 | 车票/发票/合同识别、文档数字化 | 华北2（北京）、新加坡、美国（弗吉尼亚） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而其他模型如 `gui-plus` 和 `qwen-vl-ocr` 均明确列出多地域支持（含新加坡、弗吉尼亚），该限制具有排他性，不可跨地域调用。

## 关键参数

所有模型均支持以下通用参数（部分为 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)非标扩展，需通过 `extra_body` 传入）：

- `temperature`：默认 `0.01`（`qwen-vl-ocr` 默认 `0.001`），控制输出随机性；建议保持默认值以保障 OCR/意图识别等任务的确定性。
- `top_p`：默认 `0.01`（`qwen-vl-ocr` 默认 `0.001`），核采样阈值；与 `temperature` 二选一设置。
- `max_tokens`：上限由模型能力决定（如 `qwen-deep-research` 默认 `model_detailed_report` 约 6000 [Token](../concepts/token.md)；`qwen3.5-ocr` 最大 32768）。
- `stream`：布尔值，启用流式响应；`qwen-deep-research` 必须启用 `stream=True` 完成两阶段交互。
- `vl_high_resolution_images`（仅 `gui-plus`）：启用后忽略 `max_pixels`，固定像素上限 `12845056`；需置于 `extra_body`。
- `output_format`（仅 `qwen-deep-research`）：可选 `model_detailed_report`（默认）或 `model_summary_report`。
- `min_pixels` / `max_pixels`（视觉模型）：单位为像素，不同模型像素/[Token](../concepts/token.md) 换算规则不同（如 `qwen3.5-ocr`: `32×32`/[Token](../concepts/token.md)；`qwen-vl-ocr`: `28×28`/Token），详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

## 使用方式

### 基础调用前提
- 已获取并配置 API Key（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；
- 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优；
- Python SDK 用户需显式设置 `dashscope.base_http_api_url`（`qwen-deep-research`、`farui-plus` 等）或 `OpenAI(base_url=...)`（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)）。

### 模型特异性调用要点
- **意图识别**：必须在 `system` message 中声明 `Response in INTENT_MODE.`（工具调用）或指定标签字典（纯分类），响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构 —— 详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究**：严格遵循两阶段流程：① 发起研究请求 → 解析模型反问；② 将反问 + 用户澄清作为上下文再次调用。不支持单次直接生成报告。
- **GUI 自动化**：`messages.content` 必须为 `array`，包含 `image_url` 和 `text` 类型对象；工具调用需严格遵循 `<tools>` XML 块与 `<tool_call>...</tool_call>` JSON 格式。
- **OCR 提取**：`text` 字段可覆盖默认 Prompt（如车票字段提取），`image_url` 必须提供有效 URL 或 Base64 Data URL。

## 限制和注意事项

- **地域锁定**：`qwen-deep-research` 仅支持华北2（北京）地域，且必须使用该地域的 API Key；尝试在其他地域调用将失败。
- **SDK 支持差异**：
  - `qwen-deep-research` **仅支持 Python DashScope SDK**，不支持 Java SDK 或 OpenAI 兼容接口；
  - `tongyi-intent-detect-v3` 的 `dashscope CLI` 明确不支持 `understanding` 子命令，需用 Python SDK；
  - `gui-plus` 的 `enable_thinking` 参数需通过 `extra_body` 传入，非标准 OpenAI 参数。
- **输入格式强约束**：
  - GUI/OCR 模型要求 `messages[0].content` 为 `array`（含 `type: "image_url"` 对象），违反将返回 400 错误；
  - `qwen-deep-research` 第二步调用中，`assistant` message 的 `content` 必须是第一步返回的完整反问文本，否则无法进入深入研究阶段。
- **成本与限流**：`farui-plus` 明确标注输入成本为 20 元/百万 Token，且需参考 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档；`tongyi-intent-detect-v3` 提供 90 天内 100 万 Token 免费额度。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


