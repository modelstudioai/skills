# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，覆盖意图理解、GUI自动化、深度研究和OCR等场景。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持精细化参数控制与多模态输入。开发者需根据业务需求选择对应模型，并注意地域、域名与 SDK 兼容性限制。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由与工具编排。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **GUI交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专为桌面 GUI 自动化设计，支持图像+文本多模态输入与动作指令生成，适用于 RPA 场景。
- **深度研究模型**：`qwen-deep-research`，支持两阶段研究流程（反问确认 → 深度分析），自动执行网络搜索、信息整合与结构化报告生成。
- **OCR模型**：`qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等，支持高精度文本提取与结构化字段抽取，适配文档、票据、截图等多种图像类型。

> **注意**：`qwen-deep-research` 明确声明“**仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**”[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)，而其他模型（如 `tongyi-intent-detect-v3`、`gui-plus`、`qwen3.5-ocr`）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。该差异构成关键兼容性约束，不可忽略。

## 关键参数

各模型共享部分通用参数，但存在重要差异：

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `vl_high_resolution_images` | 控制图像像素上限策略（固定 12845056 或由 `max_pixels` 决定） | `gui-plus` | 非 OpenAI 标准参数，Python SDK 中需置于 `extra_body` |
| `output_format` | 指定研究报告格式（`model_detailed_report` / `model_summary_report`） | `qwen-deep-research` | 仅 DashScope SDK 支持 |
| `min_pixels` / `max_pixels` | 图像预处理像素阈值，单位像素；不同 OCR 模型对应不同 Token 像素比（`32×32` 或 `28×28`） | `qwen3.5-ocr`, `qwen-vl-ocr-*` | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中明确定义了各模型取值范围 |
| `enable_thinking` | 开启混合思考模式，返回 `reasoning_content` 字段 | `gui-plus-2026-02-26` | 仅该版本支持，非全局参数 |
| `temperature` / `top_p` | 控制生成多样性；默认值普遍设为 `0.01`（OCR）或 `0.01`（intent） | 全部 | 文档均强调“建议只设置其中一个” |

## 使用方式

### 域名与认证
所有模型均推荐使用**业务空间专属域名**以获得更优性能与稳定性：
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`（仅 OCR 支持）

`{WorkspaceId}` 需从百炼控制台【业务空间详情】页获取。API Key 必须已配置至环境变量（`DASHSCOPE_API_KEY`）或显式传入 SDK。

### 调用示例要点
- **意图识别**：必须在 `system` 消息中声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或指定意图字典（纯标签输出），并正确构造 `tools` 或 `intent_dict` JSON 结构。
- **GUI-Plus**：`messages.content` 必须为数组，含 `image_url` 和 `text` 对象；`image_url` 中可直接嵌入 `min_pixels`/`max_pixels`。
- **Qwen-Deep-Research**：严格遵循**两阶段流程**——先发初始请求获取澄清问题，再将用户回答与历史消息一并提交进行深度分析。
- **OCR**：`user` 消息 `content` 数组中，`image_url` 对象可携带 `min_pixels`/`max_pixels`，`text` 对象用于传递自定义 Prompt（否则使用默认提取指令）。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**，其他地域调用将失败 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **SDK 限制**：`qwen-deep-research` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Java SDK；`tongyi-intent-detect-v3` 的 DashScope CLI 不支持 `understanding` 子命令，需用 Python SDK。
- **流式响应解析**：`tongyi-intent-detect-v3` 的响应需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构；`qwen-deep-research` 的流式响应含 `phase`（如 `ResearchPlanning`、`WebResearch`）与 `status` 字段，需按阶段处理。
- **OCR 图像尺寸**：`max_pixels` 默认值因模型而异（如 `qwen3.5-ocr` 为 `8388608`，`qwen-vl-ocr` 为 `6422528`），超限需申请提升，且 `qwen-vl-ocr` 输出长度 >4096 需商务审批。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内 100万 Token 免费额度，有效期明确标注于 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 表格中。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


