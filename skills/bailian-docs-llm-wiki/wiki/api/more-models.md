# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，涵盖意图理解、机器翻译、深度研究、OCR文字识别和GUI界面交互等场景。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，兼顾性能、稳定性与成本效率。开发者可根据具体任务需求选择对应模型，并按规范配置参数与输入格式。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解**：`tongyi-intent-detect-v3`，支持两类模式：  
  - `INTENT_MODE`：同时输出结构化[函数调用](../concepts/function-calling.md)（含工具名与参数），适用于 Agent 工具编排；  
  - 纯意图分类模式：从预定义标签集中返回单个意图标识符（如 `alarm_set`），支持单 [Token](../concepts/token.md) 响应以提升吞吐。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **机器翻译**：`qwen-mt-plus`，支持源/目标语言自动检测与显式指定、术语干预、翻译记忆（TM）、领域提示等高级能力，覆盖中英等主流语种。  
- **深度研究**：`qwen-deep-research`，仅限华北2（北京）地域，采用两阶段工作流（反问确认 → 深入研究），支持网络搜索、参考溯源与多格式报告生成（`model_detailed_report` / `model_summary_report`）。  
- **OCR文字识别**：`qwen3.5-ocr`、`qwen-vl-ocr` 等系列模型，支持图像文本提取、结构化信息抽取（如车票字段），并提供 `min_pixels` / `max_pixels` 图像分辨率控制。  
- **GUI界面交互**：`gui-plus` 及其版本（如 `gui-plus-2026-02-26`），专为桌面自动化设计，可解析截图、生成鼠标键盘操作指令（`computer_use` 函数），支持高分辨率图像处理与混合思考模式（`enable_thinking`）。

> **注意**：文档 3 明确指出 `Qwen-Deep-Research` “仅支持华北2（北京）地域”，而文档 2 和文档 4 中列出的美国（弗吉尼亚）地域 endpoint 并未在文档 3 中被提及或验证，因此 `qwen-deep-research` **不支持美国（弗吉尼亚）地域**，该地域 endpoint 对此模型无效。

## 关键参数

各模型共性关键参数如下（部分为 OpenAI 标准参数，部分为百炼扩展参数）：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | — | 必填。模型名称，如 `tongyi-intent-detect-v3`、`qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26`、`qwen-deep-research`。 |
| `messages` | array | — | 必填。消息数组，结构依模型而异：<br>- 意图模型需在 `system` 消息中嵌入 `Response in INTENT_MODE.` 或意图字典；<br>- OCR/GUI 模型支持 `image_url` + `text` 多模态输入；<br>- `qwen-deep-research` 要求第二步传入 `assistant` 消息作为历史澄清。 |
| `base_url` | string | — | 必填（SDK 调用）。必须使用业务空间专属域名，例如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。旧域名 `dashscope.aliyuncs.com` 已不推荐。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。 |
| `extra_body` | object | — | 非标准参数容器。用于传递模型特有参数：<br>- `qwen-mt-plus`: `{"translation_options": {...}}`；<br>- `gui-plus`: `{"vl_high_resolution_images": true, "enable_thinking": true}`；<br>- `qwen3.5-ocr`: `{"top_k": 5}`。 |
| `stream` | boolean | `false` | 控制响应方式。`true` 时需按 SSE 协议逐块解析（`qwen-deep-research` 强制流式）。 |
| `max_tokens` | integer | 按模型而定 | 输出长度上限。OCR 模型默认 4096（`qwen-vl-ocr`）或 32768（`qwen3.5-ocr`）；GUI 模型默认为模型最大输出长度。 |
| `temperature` / `top_p` | float | `0.01` / `0.001` (意图), `0.01` / `0.01` (GUI) | 控制生成多样性。二者互斥，建议仅设其一。OCR 文档明确建议保持默认值。 |

## 使用方式

### 通用前提
- 已在百炼控制台创建业务空间并获取对应地域的 API Key；
- 已将 API Key 配置至环境变量 `DASHSCOPE_API_KEY`；
- 已安装对应 SDK（[DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI Python/Node.js SDK）。

### 调用路径差异
- **意图模型 (`tongyi-intent-detect-v3`) 与翻译模型 (`qwen-mt-plus`)、OCR (`qwen3.5-ocr`)、GUI (`gui-plus`) 模型**：均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）与 DashScope SDK（`chat.completions.create`）。
- **深度研究模型 (`qwen-deep-research`)**：**仅支持 DashScope Python SDK 的 `Generation.call` 接口**，不支持 OpenAI 兼容模式，且必须使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1` endpoint。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

### 输入构造要点
- **意图识别**：System Message 必须包含 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或明确的意图字典（纯分类），且 `tools` 或 `intent_dict` 需 JSON 序列化后注入。
- **OCR/GUI**：`messages[0].content` 为数组，内含 `{"type": "image_url", "image_url": {"url": "..."}, "min_pixels": ..., "max_pixels": ...}` 与 `{"type": "text", "text": "prompt"}` 两项。
- **深度研究**：第一步仅传 `user` 消息；第二步需按顺序传入 `user`（原始问题）、`assistant`（模型反问）、`user`（用户澄清）三元组。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen-mt-plus` 和 `qwen3.5-ocr` 支持北京、新加坡、美国（弗吉尼亚）三地，但需使用对应地域的 API Key 与 `base_url`。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；`dashscope CLI` 当前不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **OCR 分辨率约束**：`min_pixels` 和 `max_pixels` 的默认值与取值范围因模型版本而异（如 `qwen3.5-ocr` 与 `qwen-vl-ocr` 的像素/[Token](../concepts/token.md) 比不同），务必查阅对应模型文档确认。
- **GUI 模型特殊参数**：`vl_high_resolution_images=true` 时，`max_pixels` 参数失效，图像将被强制缩放到 `12845056` 像素上限；`enable_thinking=true` 时，思考内容通过 `reasoning_content` 字段返回，非 `message.content`。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 [Token](../concepts/token.md) 免费额度，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


