# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、OCR文字识别及GUI界面交互等任务。这些模型在通用大模型基础上进行了领域精调与能力增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，适用于高精度、低延迟、强可控性的专业场景。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 适用场景 | 文档引用 |
|----------|------|-----------|------------|-----------|
| `farui-plus` | 法律大模型 | 法律问答、案情分析、文书生成、合同审查、RAG检索增强 | 法律咨询、司法辅助、合规审查 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策（INTENT_MODE）、多标签分类 | 智能客服、语音助手、Agent编排 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 机器翻译模型 | 多语言互译、术语干预、翻译记忆（TM）、领域提示（IT/医疗/金融等） | 技术文档本地化、跨境业务支持 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 + 网络搜索 + 报告生成）、带引用的研究报告输出 | 行业调研、竞品分析、学术辅助 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | OCR视觉模型 | 图像中文本提取、结构化信息抽取（如车票、合同、表格）、多分辨率自适应处理 | 单据识别、档案数字化、表单自动化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-*` | GUI交互模型 | 基于截图的桌面操作指令生成（鼠标/键盘/等待/终止）、支持[函数调用](../concepts/function-calling.md)与思考模式（`enable_thinking`） | RPA流程自动化、UI测试、无障碍辅助 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 模型**仅支持华北2（北京）地域且仅限 Python DashScope SDK 调用**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)；而 `tongyi-intent-detect-v3` 和 `qwen-mt-plus` 均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。该差异在[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)和[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)中均有强调，需开发者严格遵循。

## 关键参数

所有模型均支持以下通用参数（部分为非OpenAI标准参数，需通过 `extra_body` 传入）：

- `stream`: `boolean`，控制是否[流式输出](../concepts/streaming-output.md)（默认 `false`）；
- `max_tokens`: `integer`，限制输出长度（各模型取值范围不同，例如 `qwen3.5-ocr` 默认/最大为 32768，`qwen-vl-ocr` 系列为 4096）；
- `temperature` / `top_p`: 控制生成多样性（推荐保持默认值 `0.01`，二者选其一即可）；
- `repetition_penalty`: 重复惩罚（默认 `1.0`，建议勿修改）；
- `presence_penalty`: 内容重复度控制（`qwen-vl-ocr` 默认 `0.0`，`gui-plus` 默认 `1.5`）；
- `seed`: 随机种子（用于结果复现）；
- `stop`: 停止词（字符串或数组）。

**模型特有关键参数**：
- `tongyi-intent-detect-v3`: 必须在 `system` message 中声明 `Response in INTENT_MODE.` 或指定意图字典格式；
- `qwen-mt-plus`: 必须通过 `translation_options` 对象传入 `source_lang`/`target_lang`/`terms`/`tm_list`/`domains`；
- `qwen-deep-research`: 支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）；
- `qwen-vl-ocr-*` / `gui-plus-*`: 支持图像分辨率控制参数 `min_pixels`/`max_pixels`/`vl_high_resolution_images`；
- `gui-plus-*`: 支持 `enable_thinking`（仅对 `gui-plus-2026-02-26` 等混合思考模型生效，返回 `reasoning_content` 字段）。

## 使用方式

### 1. 基础前提
- 已开通百炼服务并获取对应地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；
- 推荐将 `DASHSCOPE_API_KEY` 配置至环境变量；
- 安装最新版 SDK：Python（`dashscope>=2.12.0`）或 Java（`dashscope-java-sdk`），或 OpenAI SDK（v1.0+）；
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用但性能与稳定性较低 —— 此要求在[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)和[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)中均被多次强调。

### 2. 调用示例（核心模式）
- **单轮对话**（如 `farui-plus`）：构造 `messages = [{'role': 'user', 'content': '...'}]`，调用 `Generation.call(model="farui-plus", ...)`；
- **多轮对话**：将上一轮 `response.output.choices[0].message` 追加至 `messages` 数组后继续调用；
- **[流式输出](../concepts/streaming-output.md)**：设置 `stream=True`（Python）或 `streamCall()`（Java），逐块解析响应；
- **多模态输入**（如 `qwen3.5-ocr`, `gui-plus-*`）：`messages[0].content` 为数组，包含 `{"type": "image_url", "image_url": {"url": "..."}}` 和 `{"type": "text", "text": "..."}`；
- **[函数调用](../concepts/function-calling.md)/意图识别**（如 `tongyi-intent-detect-v3`）：`system` message 必须含 `Response in INTENT_MODE.`，且需自行解析 `<tags>`/<tool_call>/`<content>` 结构化响应；
- **两阶段研究**（`qwen-deep-research`）：第一步获取模型反问内容，第二步将用户澄清回复连同初始问题、反问内容一并作为 `messages` 输入。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen-mt-plus`、`qwen-vl-ocr-*`、`gui-plus-*` 支持北京/新加坡/美国（弗吉尼亚）三地，但需使用对应地域的 API Key 和 `base_url`；
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 和 OpenAI 兼容接口，仅支持 Python DashScope SDK（见[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）；`tongyi-intent-detect-v3` 的 `dashscope CLI` 明确不支持 `understanding` 子命令（见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；
- **图像参数兼容性**：`min_pixels`/`max_pixels` 的默认值与换算逻辑因模型版本而异（如 `qwen3.5-ocr` 按 `32×32` 换算，旧版 `qwen-vl-ocr` 按 `28×28`），务必查阅对应模型文档；
- **成本与限流**：各模型按输入/输出 Token 计费（如 `farui-plus` 输入 20元/百万Token），具体限流策略参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量或密钥管理服务注入；Java SDK 中 `Generation` 对象**非线程安全**，需复用对象并自行管理同步（见[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


