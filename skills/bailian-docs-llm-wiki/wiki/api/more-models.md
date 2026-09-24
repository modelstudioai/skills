# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、OCR识别与GUI自动化等方向。这些模型在通用大模型基座上经过领域精调与能力增强，支持结构化输入/输出、多模态交互及工具调用等高级功能，适用于专业级AI应用开发。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **通义法睿（`farui-plus`）**：法律行业专用大模型，支持法律咨询、文书生成、案情分析、合同审查等，基于千问基座，融合RAG、法律Agent与司法小模型技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与[函数调用](../concepts/function-calling.md)决策模型，支持两种模式：`INTENT_MODE`（输出结构化工具调用）和纯标签分类（如 `alarm_set`），适用于智能助手与自动化工作流。
- **Qwen-MT（`qwen-mt-plus`）**：高性能机器翻译模型，支持术语干预、翻译[记忆](../concepts/memory.md)（TM）、领域提示（如 IT、金融）等企业级翻译能力 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，先反问澄清需求，再执行网络搜索、信息整合与报告生成，仅支持华北2（北京）地域及 Python DashScope SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`, `qwen-vl-ocr-*`）**：多分辨率视觉语言OCR模型，支持图像文本提取、结构化信息抽取（如车票、合同字段），兼容 OpenAI 接口与 DashScope API。
- **GUI-Plus（`gui-plus`, `gui-plus-2026-02-26`）**：界面交互专用模型，可解析截图并生成鼠标/键盘操作指令（如 `left_click`, `type`），支持高分辨率图像与混合思考模式。

> **注意**：文档 4 明确指出 Qwen-Deep-Research “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”，而文档 1 中法睿模型的 Java SDK 示例代码存在截断（末尾为 `System.out.println(JsonUtils.toJson(me`），且未说明是否完全支持该模型。实际开发中请以 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 的明确限制为准。

## 关键参数

各模型共性参数遵循 OpenAI 兼容规范，但部分参数为百炼扩展：

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 模型标识符，如 `"farui-plus"`、`"qwen-mt-plus"` | 全部 | 必填 |
| `messages` | 对话历史数组，支持 `system`/`user`/`assistant` 角色及多模态 `image_url` + `text` 混合内容 | 法睿、意图、Qwen-MT、Qwen-OCR、GUI-Plus | `qwen-deep-research` 仅支持 `user` 和 `assistant` 消息，且第二步需传入第一步的 `assistant` 回复 |
| `stream` / `stream_options` | 控制[流式输出](../concepts/streaming-output.md)；`include_usage` 可在最后一块返回 token 消耗 | 法睿、Qwen-OCR、GUI-Plus 等 | `qwen-deep-research` 默认流式，`qwen-mt-plus` 也支持流式 |
| `translation_options` | Qwen-MT 专用对象，含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` | 仅 `qwen-mt-plus` | 非标准 OpenAI 字段，需置于 `extra_body`（Python SDK）或顶层（HTTP/curl） |
| `vl_high_resolution_images` | GUI-Plus 专用布尔开关，启用后忽略 `max_pixels`，固定像素上限为 `12845056` | 仅 `gui-plus-*` | 需通过 `extra_body` 传递 |
| `output_format` | Qwen-Deep-Research 专用，取值 `model_detailed_report`（默认）或 `model_summary_report` | 仅 `qwen-deep-research` | 影响输出长度与详略程度 |

## 使用方式

### 基础调用流程
1. **配置环境**：获取业务空间 ID 与对应地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)），推荐配置至环境变量 `DASHSCOPE_API_KEY`；
2. **选择域名**：强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
3. **构造请求**：
   - OpenAI SDK：设置 `base_url` 为专属域名，调用 `client.chat.completions.create()`；
   - DashScope SDK：设置 `dashscope.base_http_api_url`，调用 `Generation.call()`；
   - HTTP/curl：直接向 `POST {base_url}/compatible-mode/v1/chat/completions` 或 `/api/v1/services/aigc/text-generation/generation` 发送 JSON 请求。

### 典型场景示例
- **法律文书生成（法睿）**：使用 `system` 消息设定角色，`user` 消息提交需求（如“生成起诉书”），支持多轮对话追加约束（如“利率4%”）；
- **意图+工具调用（意图模型）**：`system` 消息中必须包含 `Response in INTENT_MODE.` 及完整工具 JSON Schema，响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构；
- **精准翻译（Qwen-MT）**：通过 `translation_options.terms` 强制术语映射，`translation_options.tm_list` 复用历史译文，`translation_options.domains` 指定领域提升专业性；
- **GUI 自动化（GUI-Plus）**：`user` 消息中同时传入截图（`image_url`）与文本指令（`text`），`system` 消息定义可用工具与输出格式规则。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen-mt-plus`、`qwen-ocr`、`gui-plus` 在北京、新加坡、弗吉尼亚等多地可用，但 API Key 与域名需严格匹配地域；
- **SDK 支持差异**：
  - `qwen-deep-research` 仅支持 Python DashScope SDK，Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)不可用；
  - `tongyi-intent-detect-v3` 的 DashScope CLI 不支持 `understanding` 子命令，须用 Python SDK；
- **输入/输出约束**：
  - OCR 与 GUI-Plus 模型对图像尺寸有 `min_pixels`/`max_pixels` 限制，不同模型版本对应像素/[Token](../concepts/token.md) 比例不同（如 `qwen3.5-ocr` 为 `32×32`，旧版为 `28×28`）；
  - `qwen-vl-ocr` 系列 `max_tokens` 默认为 4096，如需提高至 4097–8192，须联系商务经理申请；
- **成本与限流**：各模型按输入/输出 [Token](../concepts/token.md) 计费（如 `farui-plus` 输入 20元/百万 [Token](../concepts/token.md)），具体限流策略参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档；
- **安全实践**：API Key 务必配置到环境变量，避免硬编码；生产环境应启用请求签名与 IP 白名单。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


