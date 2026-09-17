# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、OCR文字识别及GUI界面交互等任务。这些模型在通用大模型基础上进行了领域精调与能力增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，适用于高精度、低延迟、强可控性的生产级场景。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 适用场景 | 文档引用 |
|----------|------|-----------|------------|-----------|
| `farui-plus` | 法律专用大模型 | 法律问答、案情推理、文书生成、合同审查、RAG检索增强 | 法律咨询、司法辅助、合规审查 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策（INTENT_MODE）、多标签分类 | 智能客服路由、Agent编排、语音助手前端解析 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 机器翻译模型 | 多语言互译、术语干预、翻译记忆（TM）、领域提示（IT/金融/医疗等） | 技术文档本地化、跨境业务沟通、多语种内容生成 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 → 网络搜索 → 报告生成）、引用溯源、结构化输出 | 行业分析、竞品调研、学术预研、政策解读 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | 多模态OCR模型 | 图像文本提取、结构化信息抽取（如车票/发票/合同）、支持min_pixels/max_pixels分辨率控制 | 单据识别、证照处理、文档数字化、RPA流程自动化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus` / `gui-plus-2026-02-26` | GUI交互模型 | 基于截图的桌面操作指令生成（鼠标/键盘/等待/终止）、支持vl_high_resolution_images与enable_thinking | 自动化测试、GUI流程录制回放、无障碍辅助、智能RPA | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确说明“仅支持华北2（北京）地域”且“仅支持 Python DashScope SDK”，而其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`）均明确支持北京、新加坡、美国（弗吉尼亚）多地域；该不一致需在调用前严格校验地域配置，避免因地域不匹配导致404错误。

## 关键参数

所有模型共享以下通用参数（部分为OpenAI兼容接口标准参数，部分为DashScope扩展参数）：

- **`model`**（必选）：模型标识符，如 `"farui-plus"`、`"qwen-mt-plus"`。
- **`messages`**（必选）：对话消息数组，每条消息含 `role`（`system`/`user`/`assistant`）和 `content`；OCR与GUI模型支持 `image_url` 类型内容。
- **`stream`**（可选，默认 `false`）：启用[流式输出](../concepts/streaming-output.md)，适用于长响应或实时渲染场景。
- **`max_tokens`**（可选）：限制输出长度。各模型上限不同：`farui-plus` 为2k，`qwen3.5-ocr` 为32768，`qwen-deep-research` 默认 `model_detailed_report` 约6000 [Token](../concepts/token.md)。
- **`temperature` / `top_p`**（可选）：控制生成随机性，默认值普遍较低（如 `0.01`），建议仅在创意类任务中调整。
- **`seed`**（可选）：设置随机种子以保证结果可复现。

**模型特有参数**：
- `qwen-mt-plus`：通过 `extra_body.translation_options` 传入 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains`。
- `qwen-deep-research`：支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）。
- `qwen3.5-ocr` / `gui-plus`：支持 `min_pixels` / `max_pixels` 控制图像分辨率，且 `gui-plus` 额外支持 `vl_high_resolution_images` 和 `enable_thinking`。
- `tongyi-intent-detect-v3`：依赖特定 `system` message 格式（含 `Response in INTENT_MODE.` 或意图字典），否则无法触发意图解析逻辑。

## 使用方式

### 基础调用流程
1. **准备环境**：获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`），安装对应 SDK（[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）。
2. **选择域名**：强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性 —— 此要求在[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)和[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)中均被强调。
3. **构造请求**：按模型要求组织 `messages`，补充必要参数（如 OCR 的 `image_url`、MT 的 `translation_options`）。
4. **发起调用**：使用 DashScope SDK 的 `Generation.call()` 或 OpenAI SDK 的 `chat.completions.create()`。

### 示例模式
- **单轮对话**（如 `farui-plus`）：直接传入 `system` + `user` 消息，适合一次性任务（如生成起诉书）。
- **多轮对话**（如 `farui-plus`）：将上一轮 `assistant` 响应追加至 `messages`，再发新 `user` 消息，实现上下文延续。
- **[流式输出](../concepts/streaming-output.md)**（如 `farui-plus`, `qwen-deep-research`）：设置 `stream=True`，逐块读取响应，降低端到端延迟。
- **两阶段交互**（仅 `qwen-deep-research`）：第一步获取模型反问，第二步将反问+用户澄清作为新 `messages` 提交，触发深度研究。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（`qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus`）虽支持多地域，但各地区 API Key 不互通，需分别申请。
- **SDK支持差异**：
  - `qwen-deep-research` 明确不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅限 Python DashScope SDK；
  - `tongyi-intent-detect-v3` 的 `dashscope CLI` 明确不支持 `understanding` 子命令，必须使用 Python SDK；
  - `gui-plus` 的 `enable_thinking` 参数需通过 `extra_body` 传递（Python SDK），非顶层参数。
- **输入约束**：
  - OCR 模型对图像像素有硬性要求（如 `qwen3.5-ocr` `min_pixels=3072`, `max_pixels=8388608`），超限将触发缩放，影响识别精度；
  - `tongyi-intent-detect-v3` 的 `system` message 必须包含 `Response in INTENT_MODE.` 才能触发[函数调用](../concepts/function-calling.md)解析，否则返回普通文本。
- **成本与限流**：各模型计费单位为 [Token](../concepts/token.md)（见各文档“模型概览”表格），且受统一[限流策略](../../raw/model-user-guide/get-started-with-models/rate-limit.md)约束，高频调用需提前评估配额。
- **输出解析**：`tongyi-intent-detect-v3` 的响应需用正则解析 `<tags>` / `<tool_call>` / `<content>` 结构；`qwen-deep-research` 响应含多阶段 `phase` 字段（如 `ResearchPlanning`, `WebResearch`），客户端需按 `phase` 和 `status` 判断当前处理状态。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


