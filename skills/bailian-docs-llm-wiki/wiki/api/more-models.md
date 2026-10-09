# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、OCR识别与GUI自动化等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持结构化输入/输出、多阶段推理、视觉-文本联合理解等能力，适用于高精度、强专业性的业务场景。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **通义法睿（`farui-plus`）**：专为法律行业设计的大模型，支持法律咨询、案情分析、文书生成、合同审查等功能，基于千问基座并融合RAG、法律Agent等技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与工具调用决策模型，支持两种模式：`INTENT_MODE`（返回[函数调用](../concepts/function-calling.md)JSON）和纯标签分类（如 `alarm_set`），适用于智能助手、对话路由等场景 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究的模型，第一阶段反问澄清需求，第二阶段执行网络搜索、信息整合与报告生成，**仅支持华北2（北京）地域及 Python SDK** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR 系列（如 `qwen3.5-ocr`, `qwen-vl-ocr-latest`）**：多模态OCR模型，支持图像文本提取、结构化信息抽取（如车票、合同关键字段），兼容 OpenAI 接口与 DashScope API。
- **GUI-Plus（`gui-plus`, `gui-plus-2026-02-26`）**：面向桌面GUI自动化的视觉-动作模型，可解析界面截图并生成鼠标/键盘操作指令（如 `left_click`, `type`），支持高分辨率图像与思考链输出。

> **注意**：文档 4 和文档 5 中对 `min_pixels` 默认值的描述存在不一致——文档 4 明确 `qwen3.5-ocr` 的 `min_pixels` 默认值为 3072，而文档 5 对 `gui-plus` 的 `min_pixels` 默认值描述为 3136，且未限定模型版本。实际调用时请以具体模型文档为准，并优先参考 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中按模型分组的像素规则。

## 关键参数

所有模型均支持以下通用参数（部分为 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)特有）：

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 必选，模型标识符，如 `"farui-plus"`、`"tongyi-intent-detect-v3"` | — |
| `messages` | array | 必选，对话消息列表，支持 `system`/`user`/`assistant` 角色及 `text`/`image_url` 内容类型 | — |
| `stream` | boolean | 是否启用流式响应 | `false` |
| `max_tokens` | integer | 输出最大 [Token](../concepts/token.md) 数，各模型上限不同（如 `qwen3.5-ocr`: 32768；`qwen-deep-research`: 依报告格式而定） | 模型特定 |
| `temperature` / `top_p` | float | 控制生成随机性，二者建议只设其一 | `0.01` |
| `seed` | integer | 随机种子，保障结果可复现 | — |

**模型特有参数**：
- `tongyi-intent-detect-v3`：需在 `system` message 中显式声明 `Response in INTENT_MODE.` 或指定意图字典格式；
- `qwen-deep-research`：支持 `output_format="model_detailed_report"`（默认）或 `"model_summary_report"`；
- `qwen3.5-ocr` / `gui-plus`：支持 `min_pixels`/`max_pixels` 控制图像缩放，且 `qwen3.5-ocr` 使用 `32×32` 像素/[Token](../concepts/token.md)，旧版 OCR 模型使用 `28×28`；
- `gui-plus-2026-02-26`：支持 `enable_thinking=true` 返回 `reasoning_content` 字段。

## 使用方式

### 基础调用流程
1. **准备环境**：安装最新版 DashScope SDK（Python/Java）或 OpenAI SDK，[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
2. **选择域名**：强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 文档中的迁移指引；
3. **构造请求**：按模型要求组织 `messages`（注意 `farui-plus` 和 `tongyi-intent-detect-v3` 对 `system` message 的格式约束），设置必要参数；
4. **处理响应**：解析 `response.output.choices[0].message.content`；流式调用需逐块消费；`qwen-deep-research` 响应含 `phase` 字段标识当前阶段（`ResearchPlanning`, `WebResearch`, `answer`）。

### 示例代码要点
- **单轮对话（法睿）**：直接传入 `system` + `user` 消息，`model="farui-plus"`；
- **意图识别（[函数调用](../concepts/function-calling.md)）**：`system` message 必须包含工具定义 JSON 和 `Response in INTENT_MODE.`，响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构；
- **深度研究（两阶段）**：第一步获取模型反问内容（`stream=True`），第二步将 `user` 初始请求、`assistant` 反问、`user` 补充回答三者拼入 `messages`；
- **OCR 图文混合**：`messages[0].content` 为数组，内含 `{"type":"image_url","image_url":{"url":"..."}}` 和 `{"type":"text","text":"..."}` 对象；
- **GUI 自动化**：`system` message 提供工具签名（`computer_use`），`user` content 包含界面截图，响应为 `Action:` 描述 + <tool_call> JSON 工具调用。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `qwen3.5-ocr`, `gui-plus`）在华北2、新加坡、美国（弗吉尼亚）等多地可用，但需匹配对应 `base_url`；
- **SDK 限制**：`qwen-deep-research` **暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅可通过 Python DashScope SDK 调用 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **限流与配额**：所有模型受百炼平台统一限流策略约束，详情见 [限流](raw/model-user-guide/get-started-with-models/rate-limit.md)；`tongyi-intent-detect-v3` 提供开通后90天内100万 [Token](../concepts/token.md) 免费额度；
- **安全与合规**：法律类模型（`farui-plus`）生成内容仅为参考模板，**不可替代专业法律意见**；OCR 与 GUI 模型处理用户上传图像时，需确保符合数据隐私法规；
- **参数兼容性**：`top_k`、`vl_high_resolution_images`、`enable_thinking` 等非 OpenAI 标准参数，在 Python SDK 中需置于 `extra_body` 字典中传递，HTTP/Node.js 调用则作为顶层参数。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


