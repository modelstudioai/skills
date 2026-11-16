# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，包括意图理解、深度研究、OCR文字识别和GUI界面交互等。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持多地域部署与业务空间专属域名，适用于需要高精度、低延迟或复杂多模态处理的生产场景。开发者需根据任务类型选择对应模型，并注意各模型在地域支持、调用方式和参数约束上的差异。

## 支持的模型/功能

当前 `more models` 类别下主要包含以下四类专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级用户意图识别，可输出结构化[函数调用](../concepts/function-calling.md)指令或离散意图标签，适用于智能客服、Agent 工具路由等场景。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，支持两阶段交互式研究（反问确认 + 深度分析），自动规划研究路径、执行网络搜索并生成结构化报告，**仅支持华北2（北京）地域**，且**仅可通过 DashScope Python SDK 调用**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR 文字识别模型**：`qwen3.5-ocr`、`qwen-vl-ocr-*` 等，支持图像中文字提取与结构化信息抽取（如车票、合同字段），兼容 OpenAI 和 DashScope 接口，支持多地域（华北2、新加坡、美国弗吉尼亚）。
- **GUI 界面交互模型**：`gui-plus-*`（如 `gui-plus-2026-02-26`），专为桌面 GUI 自动化设计，可解析截图、生成鼠标键盘操作指令，需配合 `computer_use` 工具函数使用。

> **注意**：文档 4 中 `vl_high_resolution_images` 参数说明存在自引用错误——其描述中两次引用了自身路径 `raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md`，该链接无效，应以实际模型规格文档为准。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus-*` | 图像预处理像素阈值。`qwen3.5-ocr`：`min_pixels=3072`, `max_pixels=8388608`；`gui-plus-*`：`min_pixels=3136`，`max_pixels` 受 `vl_high_resolution_images` 控制 | 见上表 |
| `output_format` | `qwen-deep-research` | 报告格式：`model_detailed_report`（约6000 Token）或 `model_summary_report`（约1500–2000 Token） | `model_detailed_report` |
| `vl_high_resolution_images` | `gui-plus-*` | 启用高分辨率图像处理（固定上限 12845056 像素），设为 `true` 时忽略 `max_pixels` | `false` |
| `enable_thinking` | `gui-plus-2026-02-26`（仅混合思考模型） | 开启后返回 `reasoning_content` 字段，用于调试推理过程 | `false` |
| `stream` / `stream_options.include_usage` | 全部支持流式的模型 | 流式响应控制；`include_usage=true` 可在最后一个数据块获取 token 消耗 | `false` |

> **注意**：`qwen-deep-research` 的 `messages` 结构为两阶段必需：第一步仅含 `user` 消息；第二步必须包含 `user`（原始请求）、`assistant`（模型反问）、`user`（用户澄清）三元组，否则无法进入深入研究阶段。

## 使用方式

### 域名与认证
- **强制迁移建议**：华北2（北京）、新加坡地域用户应使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优，旧域名 `dashscope.aliyuncs.com` 仍可用但非推荐路径 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **API Key 配置**：所有模型均需已[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置。

### 调用方式差异
- `tongyi-intent-detect-v3`：支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope SDK，需严格设置 `System Message` 触发 `INTENT_MODE` 或意图分类模式。
- `qwen-deep-research`：**仅支持 DashScope Python SDK**，且必须使用 `dashscope.Generation.call()`（非 `chat.completions.create`），不支持 OpenAI 接口。
- `qwen3.5-ocr` 与 `gui-plus-*`：均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）和 DashScope SDK，`content` 字段需为 `array` 类型，支持 `text` 与 `image_url` 混合输入。

### 典型调用流程示例
- **意图识别（[函数调用](../concepts/function-calling.md)）**：`system_prompt` 包含工具定义 + `Response in INTENT_MODE.`，解析响应需用正则提取 `<tags>`、<tool_call>、`<content>` 三段内容。
- **深度研究**：先发起初始请求获取反问内容 → 提取 `step1_content` → 构造三轮 `messages`（user/assistant/user）发起第二步调用。
- **OCR 提取**：`content` 数组中同时传入 `image_url`（含 `url`、`min_pixels`、`max_pixels`）和 `text`（定制 Prompt），避免默认提示语干扰结构化输出。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen3.5-ocr` 和 `gui-plus-*` 支持华北2、新加坡、美国弗吉尼亚三地；意图模型未限定地域，但推荐使用专属域名。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 与 OpenAI 兼容接口；`dashscope CLI` 当前不支持 `understanding` 子命令，意图识别需用 Python SDK [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **输出长度限制**：
  - `qwen-vl-ocr`（旧版）：`max_tokens` 默认 4096，超限需商务申请；
  - `qwen3.5-ocr`：`max_tokens` 默认 32768；
  - `gui-plus-*`：`max_tokens` 默认为模型最大输出长度，参见官方模型选型页。
- **图像处理**：`min_pixels`/`max_pixels` 单位为总像素（宽×高），不同模型每 Token 对应像素不同（`qwen3.5-ocr`: 32×32；旧版 OCR: 28×28），需按公式换算配置值。
- **Token 成本**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


