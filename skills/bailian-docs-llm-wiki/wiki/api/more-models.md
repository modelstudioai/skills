# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖意图理解、法律推理、深度研究、机器翻译、OCR识别和GUI自动化等能力。这些模型在通用大模型基础上进行了领域精调与架构优化，支持高精度、低延迟的行业任务处理。所有模型均通过统一的 DashScope API 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，开发者可按需选择并快速集成。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于智能客服、Agent 工具路由等场景。其核心能力包括双模式输出（仅意图标签 / 意图+工具调用JSON），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **法律行业模型**：`farui-plus`，专为司法场景优化，支持法律咨询、文书生成、案情分析、合同审查等功能，具备 RAG 增强与法律 Agent 能力。
- **深度研究模型**：`qwen-deep-research`，仅支持华北2（北京）地域，采用两阶段交互流程（反问确认 → 深入研究），自动执行网络搜索、信息整合与结构化报告生成，[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中详细说明了其阶段状态与响应结构。
- **机器翻译模型**：`qwen-mt-plus`，支持多语言互译、术语干预、翻译记忆（TM）及领域提示，适用于技术文档、本地化等高保真翻译需求。
- **OCR 识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr-*` 系列，支持图文混合输入，可提取图像中任意文本，并通过 `min_pixels`/`max_pixels` 控制图像分辨率适配，[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 提供了完整的像素-Token 映射规则。
- **GUI 自动化模型**：`gui-plus-*`（如 `gui-plus-2026-02-26`），专为桌面界面操作设计，支持基于截图的鼠标键盘控制、多步任务编排与思考模式（`enable_thinking`），适用于 RPA 和智能测试场景。

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而 `gui-plus` 文档未限定地域，但其示例代码与 `qwen-ocr` 一致，均默认使用北京专属域名；实际部署时请以控制台可用模型列表为准，避免跨地域调用失败。

## 关键参数

各模型共享部分通用参数，但关键行为参数存在差异：

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 必选，指定模型名称（如 `"tongyi-intent-detect-v3"`） | 全部 | 不同模型不可混用 |
| `messages` | 必选，按角色组织的对话历史数组 | 全部 | `qwen-deep-research` 要求两步构造（用户初始请求 + 助理反问 + 用户澄清）；`qwen-ocr` 和 `gui-plus` 支持 `image_url` 类型内容；`tongyi-intent-detect-v3` 对 `system` 消息格式有严格要求（必须含 `INTENT_MODE` 或意图字典） |
| `translation_options` | 仅 `qwen-mt-plus` 使用，包含 `source_lang`/`target_lang`/`terms`/`tm_list`/`domains` | `qwen-mt-plus` | 非标准字段，需通过 `extra_body` 传入 OpenAI SDK |
| `vl_high_resolution_images` | 仅 `gui-plus` 使用，启用后忽略 `max_pixels`，固定上限为 12845056 像素 | `gui-plus-*` | 非 OpenAI 标准参数，Python SDK 需置于 `extra_body` |
| `output_format` | 仅 `qwen-deep-research` 使用，取值 `model_detailed_report`（默认）或 `model_summary_report` | `qwen-deep-research` | 控制输出报告长度与详略程度 |
| `stream` / `stream_options` | 控制[流式输出](../concepts/streaming.md)，`include_usage` 仅在最后一块返回 token 统计 | `qwen-deep-research`, `qwen-ocr`, `gui-plus`, `farui-plus` | `qwen-mt-plus` 和 `tongyi-intent-detect-v3` 示例中未体现流式支持，建议以实际 SDK 文档为准 |

## 使用方式

### 基础前提
- 已在百炼控制台开通服务并获取对应地域的 API Key（不同地域 Key 不互通）；
- 已配置 `DASHSCOPE_API_KEY` 环境变量；
- 已安装最新版 DashScope SDK 或 OpenAI SDK（[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；
- **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更优性能与稳定性，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中的迁移指引。

### 调用路径
- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：适用于 `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus-*`，`base_url` 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；
- **DashScope 原生接口**：适用于 `farui-plus`, `qwen-deep-research`, `tongyi-intent-detect-v3`，`base_http_api_url` 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1`；
- **特殊限制**：`qwen-deep-research` 仅支持 Python DashScope SDK（不支持 Java/HTTP/OpenAI）；`tongyi-intent-detect-v3` 的 `dashscope CLI` 当前不支持 `understanding` 子命令，需用 Python SDK。

### 典型模式示例
- **意图识别（[函数调用](../concepts/function-calling.md)）**：`system` 消息中嵌入工具定义 JSON 并声明 `Response in INTENT_MODE.`；
- **意图识别（单标签）**：`system` 消息中提供意图字典并指令 `Just reply with the chosen tag.`；
- **OCR 结构化提取**：在 `messages[0].content` 数组中同时传入 `image_url` 和 `text`（Prompt），如车票信息提取；
- **GUI 自动化**：`system` 消息中定义 `<tools>` 与响应格式规范，`user` 消息传入截图 + 操作指令（如“帮我打开浏览器”）。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 严格限定于华北2（北京）地域；其他模型虽支持多地域（北京/新加坡/弗吉尼亚），但 API Key 与域名必须匹配，跨地域调用将失败。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅限 Python DashScope SDK；`tongyi-intent-detect-v3` 的 `dashscope CLI` 暂不支持 `understanding` 子命令。
- **输入约束**：
  - `qwen-ocr` 和 `gui-plus` 对图像尺寸有 `min_pixels`/`max_pixels` 强制校验，超出范围会自动缩放，需按模型版本（`28×28` 或 `32×32` 每 Token）计算阈值；
  - `qwen-mt-plus` 的 `terms` 和 `tm_list` 字段长度受服务端限制，过长可能导致请求被截断或拒绝；
  - `tongyi-intent-detect-v3` 的 `system` 消息若未精确包含 `INTENT_MODE.` 或意图字典格式错误，将导致解析失败。
- **输出解析**：`tongyi-intent-detect-v3` 的[函数调用](../concepts/function-calling.md)响应需用正则 `parse_text()` 函数提取 `<tags>`/<tool_call>/`<content>` 三段内容，不可直接 JSON 解析原始响应体。
- **成本与额度**：`tongyi-intent-detect-v3` 提供 90 天内 100 万 Token 免费额度；`farui-plus` 输入成本为 20 元/百万 Token，无免费额度说明；具体计费请以控制台实时报价为准。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


