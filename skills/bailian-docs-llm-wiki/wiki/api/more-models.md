# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、OCR文字识别及GUI界面交互等任务。这些模型在通用大模型基础上进行了领域精调或架构增强，具备更强的专业能力与更优的推理性能。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用，所有模型均支持业务空间专属域名以提升稳定性与延迟表现。

## 支持的模型/功能

- **通义法睿（`farui-plus`）**：法律行业专用模型，支持法律咨询、案情分析、文书生成、合同审查等，上下文长度 12k Token，最大输出 2k Token [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级意图识别模型，支持 `INTENT_MODE` 下的工具调用解析或纯标签分类，上下文长度 8,192 Token，提供 100 万 Token 免费额度（开通后 90 天内）[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示（如 IT、金融），兼容多地域（北京/新加坡/弗吉尼亚）[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，支持反问确认 → 网络搜索 → 报告生成全流程，**仅限华北2（北京）地域**，且**仅支持 Python DashScope SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatibility.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`, `qwen-vl-ocr-*`）**：多模态 OCR 模型，支持图像文本提取、结构化信息抽取（如车票、合同），支持 `min_pixels`/`max_pixels` 图像分辨率控制及[流式输出](../concepts/streaming.md) [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（`gui-plus`, `gui-plus-2026-02-26`）**：界面自动化交互模型，支持基于截图的 GUI 操作指令生成（如点击、输入、等待），需配合 `computer_use` 工具函数使用 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 4 明确指出 Qwen-Deep-Research “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)”，而文档 1 中 `farui-plus` 的 Java SDK 示例代码存在明显截断（末尾为 `System.out.println(JsonUtils.toJson(me`），且未说明该模型是否支持 Java SDK。因此，**`farui-plus` 的 Java SDK 支持状态存疑，建议优先使用 Python SDK**。

## 关键参数

所有模型均支持以下通用参数（部分为非 OpenAI 标准参数，需通过 `extra_body` 传入）：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `temperature` | float | `0.01` | 控制生成多样性；建议保持默认，避免与 `top_p` 同时设置 |
| `top_p` | float | `0.001`（OCR）或 `0.01`（GUI-Plus） | 核采样阈值；同上，二者择一即可 |
| `max_tokens` | int | 因模型而异（如 `qwen3.5-ocr`: 32768；`qwen-vl-ocr`: 4096） | 输出长度上限；OCR 类模型超限需申请配额 |
| `stream` | bool | `false` | 是否启用[流式输出](../concepts/streaming.md)；流式响应需客户端逐块解析 |
| `seed` | int | — | 随机种子，保障结果可复现 |
| `stop` | string/array | — | 指定停止词，用于安全或格式控制 |

**模型特有参数**：
- **Qwen-MT**：`translation_options`（含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains`）；
- **Qwen-OCR / GUI-Plus**：`min_pixels`/`max_pixels`（图像像素阈值），其中 `qwen3.5-ocr` 默认 `min_pixels=3072`，`qwen-vl-ocr` 系列默认 `3136`；
- **GUI-Plus**：`vl_high_resolution_images`（启用高分辨率处理）、`enable_thinking`（仅 `gui-plus-2026-02-26` 支持）；
- **意图理解**：必须通过 `system` message 设置 `Response in INTENT_MODE.` 或意图标签列表，否则无法触发对应模式。

## 使用方式

1. **环境准备**：  
   - 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
   - 安装最新版 DashScope SDK（Python/Java）或 OpenAI SDK [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；  
   - **强制使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，旧域名已不推荐 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

2. **调用示例（核心模式）**：  
   - **单轮对话（法睿）**：构造 `messages = [{'role': 'user', 'content': '...'}]`，调用 `dashscope.Generation.call(model='farui-plus', ...)`；  
   - **意图识别（工具调用）**：`system` message 必须包含 `Response in INTENT_MODE.` 和工具 JSON 描述；响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构；  
   - **OCR 提取**：`messages` 中 `content` 为 `[{type: 'image_url', image_url: {url: '...'}}, {type: 'text', text: '...'}]`；  
   - **深度研究**：严格分两步——先发初始请求获反问内容，再将用户澄清 + 反问内容 + 新指令组合为三元组 `messages` 发起第二步调用；  
   - **GUI 自动化**：`system` message 提供 `computer_use` 工具定义，`user` message 传截图 + 文本指令，响应为 `Action` + `<tool_call>{...}<tool_call>` 格式 JSON。

3. **[流式输出](../concepts/streaming.md)**：  
   - DashScope SDK：设置 `stream=True`（Python）或 `streamCall()`（Java）；  
   - OpenAI SDK：设置 `stream=True`，并迭代 `completion` 流；  
   - 注意：Qwen-Deep-Research 的流式响应含 `phase` 字段（如 `ResearchPlanning`, `WebResearch`, `answer`），需按阶段解析 `content` 与 `extra.deep_research`。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus`）支持多地域，但需匹配对应 WorkspaceId 与 API Key [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **SDK 限制**：`qwen-deep-research` 明确不支持 Java SDK 与 OpenAI 兼容接口；`tongyi-intent-detect-v3` 的 dashscope CLI 不支持 `understanding` 子命令，需用 Python SDK [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **图像参数差异**：`qwen3.5-ocr` 与 `qwen-vl-ocr` 系列的 `min_pixels`/`max_pixels` 默认值及像素/Token 换算比例不同（32×32 vs 28×28），务必按模型文档配置，否则可能触发错误缩放 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **成本与限流**：`farui-plus` 输入/输出成本分别为 20 元/百万 Token；所有模型受统一限流策略约束，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档。
- **安全与合规**：法律类模型（如 `farui-plus`）生成内容仅为参考模板，实际使用需经专业律师审核；OCR/GUI 模型处理敏感图像前应脱敏。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


