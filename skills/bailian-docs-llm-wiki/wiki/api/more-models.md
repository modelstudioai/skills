# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、翻译、意图理解、深度研究、OCR识别及GUI自动化等能力。这些模型基于通义千问基座，通过领域精调、RAG增强、多阶段推理等技术优化，在特定任务上具备更高精度与效率。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持流式/非[流式输出](../concepts/streaming-output.md)、多轮对话及结构化参数控制。

## 支持的模型/功能

当前支持的专用模型包括：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、合同审查、案情分析等，上下文长度 12k [Token](../concepts/token.md) [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)；
- **Qwen-MT（`qwen-mt-plus`）**：机器翻译模型，支持术语干预、翻译记忆、领域提示等高级功能，适用于技术文档、本地化等高保真翻译场景 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)；
- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级意图识别模型，支持工具调用（`INTENT_MODE`）与纯标签分类两种模式，免费额度为开通后90天内100万[Token](../concepts/token.md) [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，支持反问确认→网络搜索→报告生成全流程，**仅限华北2（北京）地域且仅支持 Python DashScope SDK** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **Qwen-OCR（`qwen3.5-ocr`, `qwen-vl-ocr-*` 等）**：多分辨率OCR模型，支持图像像素缩放（`min_pixels`/`max_pixels`）、结构化文本提取、JSON格式输出等 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)；
- **GUI-Plus（`gui-plus-*`）**：界面交互专用模型，支持 GUI 自动化操作（如点击、输入、截图），需配合 `computer_use` 工具函数使用 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：Qwen-Deep-Research 明确声明“**仅支持 Python DashScope SDK，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**”，而其他模型（如 Qwen-MT、Qwen-OCR、GUI-Plus）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。若在 Java 环境中需调用深度研究能力，必须改用 Python 服务或等待后续 Java SDK 支持。

## 关键参数

各模型共性关键参数如下（具体取值因模型而异）：

| 参数 | 类型 | 说明 | 典型默认值 |
|------|------|------|------------|
| `model` | string | 模型标识符，必填 | `farui-plus`, `qwen-mt-plus`, `tongyi-intent-detect-v3` 等 |
| `messages` | array | 对话历史，含 `role`（`user`/`system`/`assistant`）与 `content` | — |
| `stream` | boolean | 是否启用[流式输出](../concepts/streaming-output.md) | `false` |
| `max_tokens` | integer | 输出最大 [Token](../concepts/token.md) 数 | `qwen3.5-ocr`: 32768；`tongyi-intent-detect-v3`: 1024；`qwen-deep-research`: 默认 `model_detailed_report`（约6000 Token） |
| `temperature` / `top_p` | float | 控制生成多样性，**二者建议只设其一** | `0.01`（多数模型） |
| `repetition_penalty` | float | 抑制重复输出 | `1.0`（无惩罚） |
| `seed` | integer | 随机种子，保障结果可复现 | — |

此外，视觉类模型（Qwen-OCR、GUI-Plus）特有图像参数：
- `min_pixels` / `max_pixels`：控制图像缩放阈值，单位为像素；
- `vl_high_resolution_images`（GUI-Plus）：启用高分辨率处理（固定上限 12845056 像素）；
- `image_url.url`：支持 HTTP URL 或 Base64 Data URL。

## 使用方式

### 通用前提
- 已获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 已安装对应 SDK（DashScope 或 OpenAI）[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。

### 调用示例（核心模式）
- **单轮/多轮对话**：通义法睿、意图理解等通用文本模型均支持标准 `messages` 数组传入，系统消息（`role: system`）用于设定角色与约束；
- **结构化输出**：Qwen-MT 通过 `translation_options` 字段传递 `source_lang`/`target_lang`/`terms`/`tm_list`；Qwen-OCR 在 `content` 中混合 `text` 与 `image_url`；
- **两阶段流程**：Qwen-Deep-Research 必须分步调用——先发送初始请求获取反问内容，再将用户回答与反问内容共同作为第二步输入；
- **工具调用**：意图理解模型需在 `system` 消息中声明 `Response in INTENT_MODE.` 并嵌入工具 JSON Schema；GUI-Plus 需在 `system` 中定义 `<tools>` 与响应格式规范。

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research **仅支持华北2（北京）地域**，其他地域调用将失败；
- **SDK 限制**：Qwen-Deep-Research 不支持 Java SDK 和 OpenAI 兼容接口，仅限 Python DashScope SDK；
- **成本与配额**：意图理解模型提供 90 天内 100 万 Token 免费额度，超出后按量计费；法睿、Qwen-MT 等模型按输入/输出 Token 单独计费（见各模型文档中的成本表格）；
- **[流式输出](../concepts/streaming-output.md)兼容性**：DashScope Python SDK 使用 `stream=True` + `incremental_output=True`；Java SDK 需调用 `streamCall` 接口；OpenAI SDK 直接设 `stream=True`；
- **图像处理安全**：Qwen-OCR 和 GUI-Plus 的 `image_url` 必须为公网可访问 URL 或合法 Base64，本地文件需先上传至对象存储并构造 URL；
- **参数冲突风险**：`temperature` 与 `top_p` 同时设置可能导致行为不可控，文档明确建议“**只设置其中一个值**”；
- **响应解析**：意图理解模型返回特殊 XML 标签（如 `<tags>`、<tool_call>、`<content>`），需自行正则解析；GUI-Plus 的工具调用结果也需按约定格式提取 JSON 块。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


