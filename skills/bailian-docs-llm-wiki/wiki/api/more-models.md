# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括意图理解、深度研究、OCR识别和GUI交互等。这些模型在特定任务上经过优化，具备更强的专业能力与更高的执行效率，适用于需要精准语义解析、多阶段推理、图文混合理解或自动化界面操作的业务场景。

## 支持的模型/功能

- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级响应，支持双模式输出——可同时返回结构化[函数调用](../concepts/function-calling.md)信息（需 `Response in INTENT_MODE.` 系统提示），也可仅输出预定义意图标签（如 `alarm_set`）。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究（`qwen-deep-research`）**：两阶段工作流（反问确认 → 深入研究），自动规划研究路径、执行网络搜索并生成结构化报告，当前**仅支持华北2（北京）地域**，且**仅限 DashScope Python SDK 调用**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR识别（`qwen3.5-ocr`, `qwen-vl-ocr-*`）**：支持图像文本提取与结构化信息抽取（如车票、合同关键字段），兼容 OpenAI 和 DashScope 接口，支持 `min_pixels`/`max_pixels` 图像分辨率控制及[流式输出](../concepts/streaming-output.md)。
- **GUI交互（`gui-plus-*`）**：专为桌面自动化设计，接收截图+指令，输出可执行动作（如 `left_click`, `type`, `wait`），支持高分辨率图像处理（通过 `vl_high_resolution_images` 参数启用）和思考过程返回（`enable_thinking`）。

> **注意**：文档 4 中 `presence_penalty` 默认值为 `1.5`，而文档 3 中同名参数默认值为 `0.0`；二者均为 OCR 和 GUI-Plus 模型的通用采样参数，但取值不一致。实际调用时请以具体模型文档为准，GUI-Plus 应遵循文档 4 的 `1.5`，OCR 应遵循文档 3 的 `0.0`。

## 关键参数

| 参数 | 说明 | 适用模型 | 默认值 | 备注 |
|------|------|----------|--------|------|
| `min_pixels` / `max_pixels` | 图像像素阈值控制（缩放依据） | `qwen3.5-ocr`, `qwen-vl-ocr-*`, `gui-plus-*` | `3072`/`8388608`（OCR）；`3136`/`1003520`（GUI-Plus） | 单位：像素；不同模型每 Token 对应像素不同（如 `32×32` 或 `28×28`） |
| `output_format` | 深度研究报告格式 | `qwen-deep-research` | `model_detailed_report` | 可选 `model_summary_report`（约1500–2000 Token） |
| `vl_high_resolution_images` | 启用高分辨率图像处理（固定上限 `12845056` 像素） | `gui-plus-*` | `false` | 非 OpenAI 标准参数，需置于 `extra_body` 中 |
| `enable_thinking` | 返回推理过程内容（`reasoning_content` 字段） | `gui-plus-2026-02-26` | `false` | 仅该版本支持；非标准参数，需 `extra_body` 传入 |
| `stream_options.include_usage` | 流式响应末尾是否包含 token 统计 | 所有支持流式的模型 | `false` | 仅对 `stream=true` 生效 |

## 使用方式

- **域名迁移**：强烈建议使用业务空间专属域名以获得更优性能与稳定性。华北2（北京）、新加坡地域已上线，迁移路径见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **SDK 选择**：
  - `tongyi-intent-detect-v3`、`qwen3.5-ocr`、`gui-plus-*`：支持 OpenAI SDK（兼容模式）与 DashScope SDK；
  - `qwen-deep-research`：**仅支持 DashScope Python SDK**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK。
- **系统提示（System Prompt）**：
  - 意图识别需显式声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或 `just reply with the chosen tag.`（纯标签）；
  - GUI-Plus 必须提供 `<tools>` 定义与严格约定的响应格式（`Action` + `<tool_call>...<tool_call>` JSON 块）；
  - 深度研究无需特殊 system prompt，由两步 messages 序列驱动（初始 query + assistant 反问 + user 补充）。
- **输入格式**：
  - 视觉模型（OCR、GUI-Plus）要求 `messages[0].content` 为 `array`，含 `{"type": "image_url", "image_url": {"url": "..."}}` 和可选 `{"type": "text", "text": "..."}`；
  - 纯文本模型（意图识别、深度研究）使用标准字符串 `content`。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR 和 GUI-Plus 在华北2、新加坡、美国（弗吉尼亚）均可用，但 endpoint URL 需按地域替换。
- **配额与计费**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 Token 免费额度；其余模型按实际 token 消耗计费，详情参见各模型定价页。
- **流式响应解析**：OCR 和 GUI-Plus 的流式响应需客户端逐块拼接 `delta.content`；`qwen-deep-research` 的流式响应结构复杂，含 `phase`（如 `WebResearch`）、`status`（如 `streamingQueries`）等字段，需按阶段解析 `output.message.content` 与 `output.message.extra.deep_research`。
- **图像处理**：`max_tokens` 对 OCR 模型有硬性限制（如 `qwen-vl-ocr` 默认 4096，超限需商务申请）；GUI-Plus 的 `vl_high_resolution_images=true` 会忽略 `max_pixels`，强制缩放到 `12845056` 像素上限。
- **工具调用解析**：意图识别返回的 `<tags>...</tags><tool_call>[...]</tool_call><content>...</content>` 需用正则+JSON 解析（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中 `parse_text` 示例），不可直接 JSON.parse 原始响应体。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


