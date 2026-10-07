# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、GUI交互和OCR识别等方向。这些模型在通用基座上进行了领域精调或架构增强，支持结构化输入/输出、多模态处理、工具调用等高级能力，适用于对专业性、准确性和响应效率有明确要求的开发者场景。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **通义法睿（`farui-plus`）**：法律行业专用模型，支持法律咨询、文书生成、案情分析、合同审查等功能，基于千问基座并融合RAG、法律Agent与司法小模型技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与[函数调用](../concepts/function-calling.md)决策模型，支持两种模式：`INTENT_MODE`（输出工具调用JSON）与纯标签分类（如 `alarm_set`），适用于智能助手、对话路由等场景 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究的模型，第一阶段反问澄清需求，第二阶段执行网络检索、规划与报告生成，仅支持华北2（北京）地域及 Python SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI-Plus（`gui-plus` 系列）**：界面交互专用多模态模型，支持图文混合输入与工具调用（如 `computer_use`），可解析桌面截图并生成鼠标/键盘操作指令，适用于自动化UI测试与RPA场景 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。
- **Qwen-OCR（`qwen3.5-ocr`, `qwen-vl-ocr-*` 等）**：高精度OCR模型，支持多分辨率图像输入与自定义Prompt提取结构化文本（如车票、合同关键字段），不同版本对应不同像素/[Token](../concepts/token.md)换算规则 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

> **注意**：文档4中 `GUI-Plus` 的 `vl_high_resolution_images` 参数说明存在不一致——其描述称“当为 `True` 时 `max_pixels` 无效”，但文档5中同名参数在 `Qwen-OCR` 中未提及该行为；实际使用应以各模型独立文档为准，不可跨模型复用参数语义。

## 关键参数

所有模型均支持以下通用参数（部分为OpenAI兼容接口特有）：

- `model`：必填，模型标识符（如 `"farui-plus"`、`"tongyi-intent-detect-v3"`）。
- `messages`：必填，按角色（`system`/`user`/`assistant`）组织的对话数组；`user` 消息内容支持 `text` 或 `image_url` 类型（视觉模型必需）。
- `stream`：布尔值，默认 `false`；设为 `true` 启用流式响应，需客户端逐块解析。
- `max_tokens`：整数，限制输出长度；各模型默认值不同（如 `qwen3.5-ocr` 为32768，`qwen-vl-ocr` 系列为4096）。
- `temperature` / `top_p`：控制输出随机性，建议二者仅选其一配置；OCR与意图模型默认值较低（0.01 / 0.001），强调确定性。
- `seed`：整数，用于结果复现。
- `stop`：字符串或数组，指定生成终止词。

视觉模型（GUI-Plus、Qwen-OCR）特有参数：
- `min_pixels` / `max_pixels`：控制图像预处理分辨率，单位为像素；不同模型版本对应不同像素/[Token](../concepts/token.md)换算系数（如 `qwen3.5-ocr` 为 `32×32`，旧版为 `28×28`）[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- `vl_high_resolution_images`：仅 GUI-Plus 支持，启用后固定像素上限为 `12845056`，忽略 `max_pixels` 设置。
- `enable_thinking`：仅 GUI-Plus 混合思考模型支持，开启后返回 `reasoning_content` 字段。

## 使用方式

### 基础调用流程
1. **准备环境**：安装最新版 DashScope SDK（Python/Java）或 OpenAI SDK，并配置 `DASHSCOPE_API_KEY` 到环境变量 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
2. **选择域名**：强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
3. **构造请求**：按模型要求组织 `messages`，注意角色顺序与内容格式（如意图模型需 `Response in INTENT_MODE.` 系统提示）。
4. **发起调用**：通过 SDK 或 curl 发送请求，处理响应中的 `output.choices[0].message.content` 或流式数据块。

### 典型代码片段
- **法睿单轮调用（Python）**：
  ```python
  import dashscope
  response = dashscope.Generation.call(
      model="farui-plus",
      messages=[{"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}],
      result_format='message'
  )
  ```
- **意图识别（OpenAI兼容）**：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  response = client.chat.completions.create(
      model="tongyi-intent-detect-v3",
      messages=[{"role": "system", "content": "Response in INTENT_MODE.\nYou may call tools: [...]"}, 
                {"role": "user", "content": "杭州天气"}]
  )
  ```
- **Qwen-Deep-Research 两阶段调用（Python）**：需先获取模型反问内容，再将其作为 `assistant` 消息传入第二轮请求 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `gui-plus`, `qwen-vl-ocr`）在华北2、新加坡、美国（弗吉尼亚）等地域可用，需匹配对应 `base_url` 和 `API Key`。
- **SDK支持差异**：
  - `qwen-deep-research` 仅支持 Python SDK，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
  - `dashscope CLI` 当前不支持 `understanding` 子命令，意图识别等任务需使用 Python SDK [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **输入约束**：
  - 视觉模型图像 URL 必须可公开访问，或使用 Base64 Data URL；本地文件需先上传至 OSS 并构造有效 URL。
  - `tongyi-intent-detect-v3` 的免费额度为开通后90天内100万[Token](../concepts/token.md)，超限后按量计费 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **输出解析**：意图模型返回内容含 `<tags>`/<tool_call>/`<content>` XML 标签，需自行解析；推荐使用文档2中提供的 `parse_text` 函数提取 `tool_call` 数组。
- **限流策略**：所有模型受统一限流规则约束，具体请参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


