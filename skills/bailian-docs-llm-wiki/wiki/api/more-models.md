# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，涵盖意图理解、深度研究、OCR识别与GUI自动化等场景。这些模型在推理性能、领域适配性及输出结构化程度上优于通用大模型，适用于需要高精度、低延迟或强领域约束的生产环境。所有模型均需通过业务空间专属域名调用以获得最佳稳定性与性能。

## 支持的模型与功能

当前 `more models` 类别下支持以下核心模型：

- **`tongyi-intent-detect-v3`**：毫秒级意图识别与[函数调用](../concepts/function-calling.md)决策模型，支持两种模式：  
  - `INTENT_MODE`：输出结构化工具调用 JSON（需在 system prompt 中声明 `Response in INTENT_MODE.`）；  
  - 纯标签分类模式：从预定义意图字典中返回单个标签（如 `alarm_set`），支持单 [Token](../concepts/token.md) 响应以极致提速 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **`qwen-deep-research`**：两阶段深度研究报告生成模型，仅支持华北2（北京）地域，需先由模型反问确认研究范围，再基于澄清结果执行网络搜索与分析 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。  
- **`qwen3.5-ocr` / `qwen-vl-ocr-*`**：高精度多语言 OCR 模型，支持图像文本提取、结构化信息抽取（如车票字段），可配置 `min_pixels`/`max_pixels` 控制图像分辨率适配 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。  
- **`gui-plus-*`**（如 `gui-plus-2026-02-26`）：面向桌面 GUI 自动化的视觉-语言模型，支持接收截图+指令，输出鼠标/键盘操作指令（如 `left_click`, `type`），需配合 `<tools>` 描述与 `<tool_call>` 包裹的 JSON 调用格式 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 明确指出 `qwen-deep-research` “仅支持华北2（北京）地域”，而文档 3 和文档 4 均列出新加坡、美国（弗吉尼亚）等多地域 endpoint。该模型实际不支持跨地域调用，其他文档中关于其地域兼容性的隐含表述属于过时或错误信息，开发者必须严格限定为 `cn-beijing`。

## 关键参数

| 参数 | 说明 | 公共性 | 备注 |
|------|------|--------|------|
| `model` | 模型名称（如 `tongyi-intent-detect-v3`） | 所有模型必选 | 不同模型名称不可混用 |
| `messages` | 对话消息数组，含 `role`（`system`/`user`/`assistant`）、`content`（文本或含 `image_url` 的数组） | 所有模型必选 | `gui-plus` 和 `qwen3.5-ocr` 支持多模态输入；`tongyi-intent-detect-v3` 和 `qwen-deep-research` 仅支持文本 |
| `base_url` | 必须使用业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）<br>或 DashScope SDK 的 `workspace` + `region` 配置 | 所有模型强制要求 | `{WorkspaceId}` 在控制台获取；`{region}` 如 `cn-beijing`、`ap-southeast-1`；旧域名 `dashscope.aliyuncs.com` 已不推荐 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `stream` | 是否流式响应 | 所有模型可选（默认 `false`） | `qwen-deep-research` 的两阶段流程天然依赖流式解析各 `phase` 状态 |
| `max_tokens` | 输出长度上限 | 所有模型可选 | `qwen-vl-ocr` 默认 4096，超限需商务申请；`qwen-deep-research` 默认 `model_detailed_report`（约 6000 [Token](../concepts/token.md)） |
| `vl_high_resolution_images` | GUI-Plus 专用：启用 16384 [Token](../concepts/token.md) 分辨率上限 | 仅 `gui-plus-*` 模型 | 设为 `true` 时忽略 `max_pixels`，固定上限 `12845056` 像素 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `output_format` | `qwen-deep-research` 专用：`model_detailed_report`（默认）或 `model_summary_report` | 仅该模型 | 影响报告篇幅与详略程度 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |

## 使用方式

### 1. 基础准备
- 获取并配置 API Key：[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 安装 SDK：OpenAI SDK 或 DashScope SDK（`qwen-deep-research` 仅支持 DashScope Python SDK）；
- 替换 `{WorkspaceId}` 和 `{region}`：从百炼控制台「业务空间详情」页获取 ID，并按模型要求选择地域（`qwen-deep-research` 强制 `cn-beijing`）。

### 2. 调用示例要点
- **意图识别**：System Message 必须包含 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或明确的标签列表（纯分类），并正确序列化 `tools` 或 `intent_dict`；
- **深度研究**：严格遵循两步调用：第一步传入初始主题获取反问，第二步将用户回答与历史消息（含 assistant 反问）一并传入；
- **OCR 与 GUI-Plus**：`content` 字段需为数组，内含 `{"type": "image_url", "image_url": {"url": "..."} }` 和可选 `{"type": "text", "text": "prompt"}`；`min_pixels`/`max_pixels` 需按模型规格设置（如 `qwen3.5-ocr` 默认 `min_pixels=3072`）；
- **响应解析**：`tongyi-intent-detect-v3` 返回含 `<tags>`/`<tool_call>`/`<content>` 的特殊格式，需用正则 `parse_text` 函数提取；`qwen-deep-research` 响应含 `phase` 字段，需按 `ResearchPlanning`→`WebResearch`→`answer` 流程处理。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域 endpoint 调用将失败；
- **SDK 限制**：`qwen-deep-research` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)和 Java SDK；`tongyi-intent-detect-v3` 的 DashScope CLI 不支持 `understanding` 子命令，必须用 Python SDK；
- **图像参数差异**：`qwen3.5-ocr` 与 `qwen-vl-ocr` 系列的 `min_pixels`/`max_pixels` 默认值及像素/Token 换算规则不同（`32×32` vs `28×28`），需严格对照文档配置；
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度，到期后按量计费；
- **安全与合规**：所有图像 URL 必须可公开访问（或使用 Base64 Data URL），私有内网地址无法被模型服务访问；
- **流式响应完整性**：`qwen-deep-research` 的 `finished` 字段为 `true` 时才表示完整报告生成完毕，中间 `phase` 响应（如 `KeepAlive`）不含有效内容。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


