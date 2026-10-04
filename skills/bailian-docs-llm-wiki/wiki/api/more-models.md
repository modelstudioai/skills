# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、GUI自动化和OCR等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持结构化输入/输出、多模态交互、工具调用等高级能力，适用于专业级AI应用开发。

## 支持的模型/功能

当前支持的专用模型包括：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、合同审查、案情分析等，基于千问基座，融合RAG、法律Agent与司法小模型技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与[函数调用](../concepts/function-calling.md)决策模型，支持两种模式：① 同时输出意图标签与工具调用JSON；② 仅输出预定义意图标签（如 `alarm_set`），可进一步压缩为单[Token](../concepts/token.md)响应以提升性能 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，首阶段反问澄清研究范围，次阶段执行网络搜索、信息整合与报告生成，支持 `model_detailed_report`（约6000 [Token](../concepts/token.md)）与 `model_summary_report`（约1500–2000 [Token](../concepts/token.md)）两种输出格式 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI-Plus（`gui-plus` 系列）**：界面交互专用多模态模型，支持图文混合输入（含 `image_url` + `text`）、高分辨率图像处理（通过 `vl_high_resolution_images` 控制）、工具调用（如 `computer_use`）及思考链输出（`enable_thinking`） [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。
- **Qwen-OCR（`qwen3.5-ocr`, `qwen-vl-ocr-*` 等）**：高精度OCR模型，支持多地域部署（华北2、新加坡、美国弗吉尼亚），可提取图像文本并按需结构化（如车票信息JSON提取），不同版本对应不同像素/Token换算规则（`28×28` 或 `32×32`） [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

> **注意**：文档4中 `gui-plus` 模型名称未明确列出具体版本，但示例代码使用 `gui-plus-2026-02-26`；而文档5中 `qwen-vl-ocr` 系列明确区分了多个版本（如 `qwen3.5-ocr`, `qwen-vl-ocr-2025-11-20`）。实际调用时请严格依据控制台或API文档确认可用模型ID，避免因版本模糊导致404错误。

## 关键参数

| 参数 | 说明 | 公共性 | 备注 |
|------|------|--------|------|
| `model` | 模型唯一标识符 | 所有模型必填 | 如 `"farui-plus"`, `"tongyi-intent-detect-v3"` |
| `messages` | 对话消息数组，含 `role`（`system`/`user`/`assistant`）与 `content` | 所有模型必填 | GUI-Plus 和 Qwen-OCR 的 `content` 为数组，支持 `text` + `image_url` 混合；法睿与意图模型为字符串；Deep-Research 要求两阶段消息构造 |
| `result_format` / `response_format` | 输出格式（如 `'message'`） | 法睿、意图模型、Deep-Research 使用 `result_format`；OCR 使用 OpenAI 兼容 `response_format` | DashScope SDK 统一用 `result_format='message'`；OpenAI SDK 不传此参数 |
| `stream` | 是否启用[流式输出](../concepts/streaming-output.md) | 所有模型支持 | 设为 `True` 时需按 SSE 协议解析数据块 |
| `max_tokens` | 最大输出长度限制 | 所有模型支持 | OCR 模型有版本相关默认值（如 `qwen3.5-ocr` 默认32768，旧版默认4096） |
| `vl_high_resolution_images` | GUI-Plus 专用：启用12845056像素上限 | 仅 GUI-Plus | 非OpenAI标准参数，Python SDK需置于 `extra_body` 中 |
| `output_format` | Deep-Research 专用：报告详略程度 | 仅 Deep-Research | 取值 `model_detailed_report`（默认）或 `model_summary_report` |

## 使用方式

### 基础前提
- 已开通百炼服务并获取有效 API Key：[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 推荐将 `DASHSCOPE_API_KEY` 配置至环境变量，降低泄露风险；
- 安装最新版 SDK：[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)（Python/Java）；
- **必须使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` —— 文档2、4、5均强调此迁移要求，旧域名虽兼容但不推荐。

### 调用示例要点
- **法睿/意图/Deep-Research**：统一使用 DashScope Python SDK 的 `Generation.call()`，设置 `model`、`messages`、`result_format='message'`；
- **GUI-Plus/OCR**：推荐 OpenAI SDK（兼容模式），`base_url` 指向业务空间专属域名，`model` 传入对应ID，`messages.content` 为图文混合数组；
- **流式调用**：
  - DashScope：`stream=True` + `incremental_output=True`（法睿）；Deep-Research 需循环读取 `responses`；
  - OpenAI：`stream=True`，客户端需处理 SSE 数据流；
- **多轮对话**：将上一轮 `response.output.choices[0].message` 追加至 `messages` 数组末尾，再发起新请求（法睿示例已展示）；
- **OCR结构化提取**：在 `messages[0].content` 的 `text` 字段中传入明确Prompt（如车票字段JSON格式要求），而非依赖默认行为。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**，其他地域调用将失败 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **SDK支持差异**：
  - Deep-Research **仅支持 Python SDK**，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；
  - 意图理解模型的 `Understanding.call()` 方法（如 `opennlu-v1`）与 `Generation.call()` 行为不同，文档2明确指出 `dashscope CLI 暂不支持 understanding 子命令`；
- **图像处理参数冲突**：GUI-Plus 与 Qwen-OCR 均有 `min_pixels`/`max_pixels`，但默认值与换算逻辑不同（OCR 分版本，GUI-Plus 固定 `min_pixels=3136`）；若混用参数需按目标模型文档校准；
- **限流与配额**：所有模型受百炼平台统一限流策略约束，详情参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；意图模型提供 **90天内100万Token免费额度**；
- **安全与合规**：法律类输出（如法睿生成的起诉书）仅为模板参考，**不构成法律意见**，实际使用须由执业律师审核；
- **错误处理**：API 返回 `status_code != 200` 或 `code` 非空时，应解析 `message` 字段定位问题（如模型不存在、token超限、地域不匹配）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


