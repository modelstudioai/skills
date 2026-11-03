# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型（[more](more.md) models），覆盖意图理解、机器翻译、深度研究、OCR文字识别和GUI界面交互等场景。这些模型通过统一的 API 接口调用，支持 OpenAI 兼容模式与 DashScope SDK，适用于需要高精度、低延迟或结构化输出的生产级应用。

## 支持的模型/功能

当前支持的专用模型包括：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式：  
  - `INTENT_MODE`：同时输出意图标签与结构化[函数调用](../concepts/function-calling.md)（含工具名与参数）；  
  - 纯意图分类模式：仅返回预定义标签（如 `alarm_set`），支持单 [Token](../concepts/token.md) 响应以提升速度。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **机器翻译模型**：`qwen-mt-plus`，支持源/目标语言自动检测、术语干预、翻译记忆（TM）及领域提示（如 IT、金融），适用于专业文档本地化。  
- **深度研究模型**：`qwen-deep-research`，仅限华北2（北京）地域，采用两阶段工作流（反问确认 → 深入研究），支持网络搜索与参考溯源，输出详尽报告或摘要。注意该模型**仅支持 DashScope Python SDK，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**。  
- **OCR模型**：`qwen3.5-ocr`、`qwen-vl-ocr` 等，支持多分辨率图像输入（通过 `min_pixels`/`max_pixels` 控制）、结构化文本提取（如车票信息 JSON 输出）及 Prompt 引导识别。  
- **GUI交互模型**：`gui-plus` 及其版本（如 `gui-plus-2026-02-26`），专为桌面自动化设计，可解析截图并生成鼠标/键盘操作指令（如 `left_click`, `type`），需配合 `<tools>` 系统提示与 `<tool_call>` 格式响应。  

> **注意**：文档 3 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”，而文档 4 和文档 5 的 OCR 与 GUI-Plus 均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。三者在接口兼容性上存在明确差异，开发者须按模型选择对应 SDK。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|--------|-----------|------|---------|
| `translation_options` | `qwen-mt-plus` | 必填对象，含 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）、`domains`（领域） | `{"source_lang": "Chinese", "target_lang": "English", "terms": [{"source":"生物传感器","target":"biological sensor"}]}` |
| `output_format` | `qwen-deep-research` | 控制报告格式：`model_detailed_report`（默认，~6000 [Token](../concepts/token.md)）或 `model_summary_report`（~1500–2000 [Token](../concepts/token.md)） | `"model_summary_report"` |
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus` | 图像像素阈值控制（单位：像素）。`qwen3.5-ocr` 默认 `min_pixels=3072`（3×32×32），`max_pixels=8388608`（8192×32×32）；`gui-plus` 默认 `min_pixels=3136`，`max_pixels` 受 `vl_high_resolution_images` 影响 | `{"min_pixels": 3072, "max_pixels": 8388608}` |
| `vl_high_resolution_images` | `gui-plus` | 布尔值，启用后忽略 `max_pixels`，强制将图像缩放至 12845056 像素上限（16384 Token） | `true` |
| `enable_thinking` | `gui-plus-2026-02-26` | 仅该混合思考模型支持，开启后返回 `reasoning_content` 字段 | `true` |

## 使用方式

### 域名与认证
所有模型均推荐使用业务空间专属域名以获得更高性能与稳定性：  
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`  
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`  
- 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`  
其中 `{WorkspaceId}` 为控制台「业务空间详情」中查看的 ID。API Key 需已配置至环境变量 `DASHSCOPE_API_KEY`，详见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 调用示例要点
- **意图理解**：System Message 中必须包含 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或 `just reply with the chosen tag.`（纯意图），且工具/意图字典需 JSON 序列化后嵌入。  
- **Qwen-MT**：`translation_options` 必须作为 `extra_body`（Python SDK）或顶层参数（Node.js/curl）传入。  
- **Qwen-Deep-Research**：严格遵循两阶段流程——先发起初始请求获取模型反问，再将反问内容作为 `assistant` 消息与用户澄清一并提交。  
- **OCR / GUI-Plus**：`messages.content` 为数组，需同时包含 `image_url`（含 `url` 字段）与 `text`（Prompt）对象；`image_url` 支持 HTTP URL 或 Base64 Data URL。  

### SDK 限制
- `qwen-deep-research` 仅支持 DashScope Python SDK（`dashscope.Generation.call`），不支持 OpenAI SDK 或 DashScope Java SDK。  
- `tongyi-intent-detect-v3` 的 DashScope CLI 不支持 `understanding` 子命令，需用 Python SDK，参见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus`）支持北京、新加坡、美国（弗吉尼亚）多地域。  
- **OCR 输出长度**：`qwen-vl-ocr` 默认 `max_tokens=4096`，若需提升至 4097–8192，须联系商务经理申请，并提供主账号ID、图像类型、QPS等信息。  
- **GUI-Plus 分辨率策略**：当 `vl_high_resolution_images=true` 时，`max_pixels` 参数失效，图像将被强制缩放至 12845056 像素上限。  
- **响应解析**：意图理解模型返回 `<tags>...</tags><tool_call>[...]<tool_call><content>...</content>` 结构，需用正则+JSON 解析（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中 `parse_text` 函数示例）。  
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度，具体计费规则参见 [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#977b13081ab56)。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


