# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型（[more](more.md) models），覆盖意图理解、机器翻译、深度研究、OCR文字识别和GUI界面交互等场景。这些模型在各自领域具备优化的架构与能力，支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，适用于需要高精度、低延迟或结构化输出的生产级应用。

## 支持的模型/功能

当前可用的专用模型包括：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式：  
  - `INTENT_MODE`：同时输出意图标签与结构化[函数调用](../concepts/function-calling.md)（含工具名与参数）；  
  - 纯意图分类模式：仅返回预定义意图标签（如 `alarm_set`），支持单 [Token](../concepts/token.md) 响应以提升速度。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **机器翻译模型**：`qwen-mt-plus`，支持源/目标语言指定、术语干预、翻译记忆（TM）和领域提示，适用于技术文档、本地化等高保真场景。  
- **深度研究模型**：`qwen-deep-research`，采用两阶段工作流（反问确认 → 深入研究），自动规划研究路径、执行网络搜索并生成结构化报告，**仅支持华北2（北京）地域及 DashScope Python SDK**。  
- **OCR模型**：`qwen3.5-ocr`、`qwen-vl-ocr` 等，支持多分辨率图像输入（通过 `min_pixels`/`max_pixels` 控制）、文本提取与结构化信息抽取（如车票字段）。  
- **GUI交互模型**：`gui-plus` 及其版本（如 `gui-plus-2026-02-26`），专为桌面自动化设计，可解析截图、生成鼠标/键盘操作指令，并支持 `enable_thinking` 开启推理过程输出。

> **注意**：文档 3 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档 4 和文档 5 的 OCR 与 GUI-Plus 模型均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。该差异需严格遵循，不可混用调用方式。

## 关键参数

所有模型共享部分通用参数（如 `model`, `messages`, `stream`, `max_tokens`, `temperature`, `top_p`），但以下参数为专用模型关键配置：

- **意图模型**：依赖 `System Message` 中的固定指令（如 `Response in INTENT_MODE.`）触发功能模式；工具列表或意图字典需 JSON 序列化后嵌入 system [prompt](../guides/prompt.md)。  
- **翻译模型**：必须通过 `extra_body.translation_options`（OpenAI）或顶层 `translation_options`（Node.js/curl）传入 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` 等字段。  
- **OCR 与 GUI-Plus 模型**：图像输入需使用 `content` 数组，其中 `type: "image_url"` + `image_url.url` 为必选；`min_pixels`/`max_pixels` 控制图像缩放（单位：像素），不同模型对应像素/[Token](../concepts/token.md) 比例不同（如 `qwen3.5-ocr` 为 `32×32`/[Token](../concepts/token.md)）。  
- **GUI-Plus 模型**：`vl_high_resolution_images` 控制图像上限策略（`true` 时忽略 `max_pixels`，固定为 `12845056` 像素）；`enable_thinking` 为非标准参数，须置于 `extra_body` 中。  
- **深度研究模型**：无 `extra_body` 或 `translation_options` 等扩展字段；需按两阶段构造 `messages`（第一步仅 user，第二步含 user+assistant+user），且 `output_format` 参数控制报告详略（`model_detailed_report` 或 `model_summary_report`）。

## 使用方式

### 基础前提
- 已获取并配置 API Key（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
- 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中的迁移说明。

### 调用方式选择
- **OpenAI 兼容接口**：适用于 `tongyi-intent-detect-v3`, `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus-*`；需设置 `base_url` 为对应地域的专属域名，并通过 `extra_body`（Python）或顶层字段（Node.js/curl）传递模型特有参数。  
- **DashScope SDK**：`qwen-deep-research` **强制要求**使用 DashScope Python SDK（`dashscope.Generation.call`），不支持 OpenAI 接口；其他模型亦可选用 DashScope SDK（如 `dashscope.Client.chat.completions.create`）。  
- **CLI 工具**：文档 1 明确说明 “dashscope CLI 暂不支持 understanding 子命令”，因此意图模型等无法通过 CLI 调用。

### 示例流程（OCR 结构化提取）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.jpg"}},
            {"type": "text", "text": "提取发票号码、金额、日期，JSON格式输出"}
        ]
    }]
)
print(completion.choices[0].message.content)
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen-mt-plus`、OCR、GUI-Plus 支持北京、新加坡、美国（弗吉尼亚）三地，但各地区 API Key 不互通。  
- **SDK 限制**：`qwen-deep-research` 不支持 OpenAI 兼容接口或 Java SDK；OCR 与 GUI-Plus 的 `top_k`, `repetition_penalty`, `presence_penalty` 等参数在 OpenAI SDK 中需放入 `extra_body`，而在 HTTP/curl 中为顶层参数。  
- **图像处理**：OCR 与 GUI-Plus 模型对 `min_pixels`/`max_pixels` 的默认值与范围定义不一致（如文档 4 中 `qwen3.5-ocr` 默认 `min_pixels=3072`，文档 5 中 `gui-plus` 默认 `min_pixels=3136`），需按具体模型文档配置。  
- **输出解析**：意图模型响应为自定义 XML 格式（`<tags>`/<tool_call>/`<content>`），需自行实现 `parse_text` 函数提取 `tool_call`；深度研究模型响应为流式 JSON，需按 `phase` 字段（如 `answer`, `WebResearch`）解析不同阶段内容。  
- **成本与配额**：`tongyi-intent-detect-v3` 提供 90 天内 100 万 Token 免费额度（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)），其他模型按实际用量计费，无统一免费额度说明。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


