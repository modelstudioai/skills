# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，涵盖意图理解、OCR识别、深度研究与GUI界面交互等场景。这些模型在推理性能、领域适配性与结构化输出能力上具有显著优势，适用于需要高精度、低延迟或复杂工作流的生产环境。所有模型均支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，但部分模型存在地域、SDK 或协议限制。

## 支持的模型与核心功能

| 模型名称 | 类型 | 主要能力 | 地域支持 | SDK 限制 |
|----------|------|-----------|-----------|------------|
| `tongyi-intent-detect-v3` | 文本理解 | 意图识别（单标签）与工具调用决策（INTENT_MODE） | 华北2（北京）、新加坡、中国香港 | OpenAI SDK / DashScope SDK 均支持，[dashscope CLI 不支持 understanding 子命令](raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | 多模态（视觉） | 图像文本提取、结构化信息抽取（如车票、合同） | 华北2（北京）、新加坡、美国（弗吉尼亚） | OpenAI SDK / DashScope SDK 均支持 |
| `qwen-deep-research` | 文本生成 | 两阶段深度研究（反问确认 + 网络检索分析），支持 `model_detailed_report` 与 `model_summary_report` 输出格式 | **仅华北2（北京）** | **仅支持 Python DashScope SDK**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK，详见 [Qwen-Deep-Research API 参考](raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `gui-plus-*`（如 `gui-plus-2026-02-26`） | 多模态（GUI） | 基于截图的桌面自动化操作（鼠标/键盘/等待/终止），支持 `enable_thinking` 与 `vl_high_resolution_images` 扩展参数 | 华北2（北京）、新加坡 | OpenAI SDK / DashScope SDK 均支持 |

> **注意**：文档 3 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档 1 和文档 4 均明确支持 OpenAI 兼容接口。该限制在多篇文档中一致，无矛盾。

## 关键参数

所有模型共享部分通用参数（如 `model`, `messages`, `stream`, `max_tokens`, `temperature`, `top_p`, `seed`, `stop`），但以下参数为特定模型关键扩展：

- **图像处理类模型（`qwen3.5-ocr`, `gui-plus-*`）**：
  - `min_pixels` / `max_pixels`：控制输入图像缩放阈值，单位为像素；不同模型对应像素/Tokens 比例不同（如 `qwen3.5-ocr` 为 `32×32`/token，`qwen-vl-ocr` 旧版为 `28×28`/token）。
  - `vl_high_resolution_images`（仅 `gui-plus-*`）：启用后忽略 `max_pixels`，固定上限为 `12845056` 像素。
  - `enable_thinking`（仅 `gui-plus-2026-02-26`）：开启后返回 `reasoning_content` 字段，需通过 `extra_body` 传入。

- **意图理解模型（`tongyi-intent-detect-v3`）**：
  - 无 `max_tokens` 等生成控制参数，其输出长度由意图定义严格约束（如单字符标签模式下恒为 1 token）。
  - 依赖 `System Message` 中的显式指令（`Response in INTENT_MODE.` 或 `just reply with the chosen tag.`）触发不同行为模式。

- **深度研究模型（`qwen-deep-research`）**：
  - `output_format`：指定 `model_detailed_report`（默认，~6000 tokens）或 `model_summary_report`（~1500–2000 tokens）。
  - 无 `temperature`/`top_p` 等采样参数，因其流程由内部状态机驱动，非自由文本生成。

## 使用方式

### 1. 域名与认证
- **必须使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。旧域名 `dashscope.aliyuncs.com` 仍可用，但[官方强烈建议迁移以获得更高性能与稳定性](raw/model-api-reference/more-models/intent-detect-capability.md)。
- API Key 需通过 [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md) 流程完成，并推荐配置至环境变量 `DASHSCOPE_API_KEY`。

### 2. 调用示例要点
- **意图识别（单标签）**：`system_prompt` 必须包含意图字典与 `Just reply with the chosen tag.` 指令；响应为纯字符串（如 `"alarm_set"`）。
- **意图识别（工具调用）**：`system_prompt` 必须含工具描述 JSON 与 `Response in INTENT_MODE.`；响应需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构，参考 [意图理解能力](raw/model-api-reference/more-models/intent-detect-capability.md) 中的 `parse_text` 函数。
- **OCR 与 GUI-Plus**：`messages[0].content` 为 `array`，需混合 `type: "image_url"` 与 `type: "text"` 对象；`image_url.url` 支持 HTTP URL 或 Base64 Data URL。
- **深度研究**：必须分两步调用——先发起研究请求获取模型反问（`step1_content`），再将反问与用户澄清作为上下文二次调用；流式响应需按 `phase`（如 `ResearchPlanning`, `WebResearch`, `answer`）解析阶段状态。

## 限制和注意事项

- **地域锁定**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；`qwen3.5-ocr` 在美国（弗吉尼亚）地域可用，但 `gui-plus-*` 文档未声明该地域支持，应默认仅限北京/新加坡。
- **协议与 SDK 限制**：
  - `qwen-deep-research` 不支持 OpenAI 兼容接口，仅 DashScope Python SDK；
  - `tongyi-intent-detect-v3` 的 dashscope CLI `understanding` 子命令已废弃，必须使用 Python SDK。
- **图像参数兼容性**：`min_pixels`/`max_pixels` 的默认值与取值范围因模型版本而异（如 `qwen3.5-ocr` 与 `qwen-vl-ocr` 的像素/Tokens 比例不同），需严格参照对应模型文档，不可跨模型复用参数值。
- **输出解析要求**：`tongyi-intent-detect-v3`（INTENT_MODE）与 `qwen-deep-research` 的响应结构高度定制化，**不可直接当作标准 ChatCompletion 响应处理**；必须按文档提供的正则或 `phase` 字段进行解析。
- **成本与额度**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度，详见 [意图理解能力](raw/model-api-reference/more-models/intent-detect-capability.md)；其他模型按实际 Token 消耗计费，无统一免费额度说明。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


