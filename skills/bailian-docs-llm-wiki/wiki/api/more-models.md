# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、OCR、深度研究和GUI交互等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持更精准的任务执行与更高性能的推理体验。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，需注意地域限制、域名迁移及参数兼容性。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **通义法睿（`farui-plus`）**：法律行业专用大模型，支持法律咨询、文书生成、案情分析、合同审查等功能，基于千问基座融合RAG、法律Agent与司法小模型技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与工具调用决策模型，支持两种模式：`INTENT_MODE`（输出[函数调用](../concepts/function-calling.md)JSON）与纯标签分类（如 `alarm_set`），适用于智能助手、自动化工作流等场景 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-OCR 系列（如 `qwen3.5-ocr`, `qwen-vl-ocr-latest`）**：多版本视觉语言OCR模型，专为高精度文本提取优化，支持图像像素缩放控制（`min_pixels`/`max_pixels`）、结构化Prompt引导输出 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，仅支持华北2（北京）地域，通过反问确认→网络搜索→报告生成流程完成复杂主题分析，输出含引用来源的详尽研究报告 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI-Plus（`gui-plus`, `gui-plus-2026-02-26`）**：界面交互专用模型，支持结合截图与自然语言指令执行GUI操作（如点击、输入、等待），需配合`computer_use`工具函数使用 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：`qwen-deep-research` 明确声明“**仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**”，而其他模型（如 `farui-plus`, `tongyi-intent-detect-v3`, `qwen3.5-ocr`, `gui-plus`）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。此为关键兼容性差异，不可跨模型假设接口一致性。

## 关键参数

所有模型共享部分通用参数，但具体取值与行为存在模型特异性：

| 参数 | 说明 | 共同默认值 | 模型特异性说明 |
|------|------|-------------|----------------|
| `model` | 模型标识符 | — | 必填；各模型名称见上表，如 `farui-plus`、`tongyi-intent-detect-v3` |
| `messages` | 对话消息数组 | — | `role` 必须为 `system`/`user`/`assistant`；`content` 类型因模型而异（`farui-plus` 仅文本；`qwen3.5-ocr` 和 `gui-plus` 支持 `image_url` + `text` 混合） |
| `stream` | 是否[流式输出](../concepts/streaming-output.md) | `false` | `farui-plus`、`qwen-deep-research`、`gui-plus` 均支持；`qwen-deep-research` 的流式响应含 `phase` 字段标识研究阶段 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `max_tokens` | 最大输出长度 | 因模型而异 | `farui-plus`: 2k；`tongyi-intent-detect-v3`: 1,024；`qwen3.5-ocr`: 32768；`qwen-deep-research`: 默认 `model_detailed_report` 约6000 Token；`gui-plus`: 同模型最大输出长度 |
| `temperature` / `top_p` | 生成多样性控制 | `0.01`（多数模型） | `tongyi-intent-detect-v3` 文档未指定默认值，但 `qwen3.5-ocr` 和 `gui-plus` 明确为 `0.01`；建议优先使用 `top_p` 并保持默认值以保障意图/OCR结果稳定性 |
| `vl_high_resolution_images` | GUI-Plus 图像分辨率开关 | `false` | **仅 `gui-plus` 支持**；启用后忽略 `max_pixels`，固定上限为 12845056 像素 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `output_format` | 报告格式 | `model_detailed_report` | **仅 `qwen-deep-research` 支持**；可选 `model_summary_report` 生成精简版 |

## 使用方式

### 1. 域名与环境配置
- **必须迁移至业务空间专属域名**：华北2（北京）、新加坡、美国（弗吉尼亚）地域均提供新域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），文档 2、3、5 均强调其“卓越性能和更高稳定性”，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但**强烈建议迁移**。
- **API Key 配置**：所有模型均要求 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐配置至环境变量 `DASHSCOPE_API_KEY` 以降低泄露风险。

### 2. SDK 调用示例（通用流程）
```python
import os
import dashscope
# 设置业务空间专属域名（以北京为例）
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 构造 messages（示例：farui-plus 单轮对话）
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}
]

response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="farui-plus",  # 替换为目标模型名
    messages=messages,
    result_format="message"
)
print(response.output.choices[0].message.content)
```

### 3. 模型特有调用要点
- **意图理解（`tongyi-intent-detect-v3`）**：System Message 必须包含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯标签），且需注入工具定义或意图字典 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **OCR（`qwen3.5-ocr`）**：`messages[0]["content"]` 必须为 `list`，内含 `{"type": "image_url", "image_url": {"url": "..."}, "min_pixels": ..., "max_pixels": ...}` 和 `{"type": "text", "text": "Prompt..."}` 两项 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **深度研究（`qwen-deep-research`）**：必须执行**两步调用**——第一步获取模型反问，第二步将反问内容作为 `assistant` 消息传入，再附上用户澄清（如“关注个性化学习”） [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI-Plus（`gui-plus`）**：System Message 需完整定义 `<tools>` 和响应格式规则（如 `Action:` + `<tool_call>...<tool_call>`），且 `messages[0]["content"]` 同样需为 `image_url` + `text` 混合列表 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**，其他模型（如 `farui-plus`, `tongyi-intent-detect-v3`, `qwen3.5-ocr`, `gui-plus`）在华北2、新加坡、美国（弗吉尼亚）等多地可用，但需使用对应地域的 `WorkspaceId` 和 API Key。
- **SDK 支持范围**：
  - `qwen-deep-research`：**仅 Python DashScope SDK**，不支持 Java SDK 或 OpenAI 兼容接口。
  - `tongyi-intent-detect-v3`：DashScope SDK 和 OpenAI 兼容接口均支持，但 `dashscope CLI` 明确不支持 `understanding` 子命令。
  - 其他模型：Python/Java SDK 及 OpenAI 兼容接口均支持（文档 1 的 Java 示例完整，文档 3/5 的 OpenAI 示例完整）。
- **成本与限流**：`farui-plus` 在文档中明确列出输入/输出成本（20元/百万Token），并指引至 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档；`tongyi-intent-detect-v3` 提供 100万Token 免费额度（90天有效期）。**各模型成本与限流策略独立，需分别查阅对应文档**。
- **参数兼容性警告**：`top_k`、`repetition_penalty`、`presence_penalty`、`seed` 等参数在 `qwen3.5-ocr` 和 `gui-plus` 文档中被标记为“非OpenAI标准参数”，通过 Python SDK 调用时**必须放入 `extra_body` 字典**，否则将被忽略。此为易错点，务必检查 SDK 调用方式。
- **响应解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 响应需用正则表达式解析 `<tags>`/<tool_call>/`<content>` 结构；`qwen-deep-research` 的流式响应需按 `phase` 字段（`ResearchPlanning`/`WebResearch`/`answer`）区分处理逻辑；`farui-plus` 和 `gui-plus` 的标准 `message` 格式可直接读取 `content`。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


