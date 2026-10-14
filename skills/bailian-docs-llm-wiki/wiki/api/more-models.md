# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，覆盖意图理解、深度研究、OCR文字识别与GUI界面交互等场景。这些模型均基于通义千问系列，通过统一 API 接口调用，支持 OpenAI 兼容模式与 DashScope SDK 两种方式，适用于需要高精度、低延迟或结构化输出的生产级应用。所有模型均需配合业务空间专属域名使用以获得最佳性能。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、工具编排等场景。该模型提供两种工作模式：`INTENT_MODE`（输出结构化工具调用）与纯标签分类（输出预定义意图 ID）。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，专为长周期、多阶段研究任务设计，支持自动反问澄清、网络搜索、研究规划与报告生成。**仅限华北2（北京）地域可用**，且**仅支持 DashScope Python SDK 调用**，不兼容 OpenAI 接口。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR 模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等多个版本，支持图像文本提取、结构化信息抽取（如车票、合同关键字段），兼容 OpenAI 和 DashScope 接口，支持多地域部署（华北2、新加坡、美国弗吉尼亚）。
- **GUI 交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），面向桌面自动化任务，可解析 UI 截图并生成鼠标/键盘操作指令，支持 `vl_high_resolution_images` 等视觉增强参数。

> **注意**：文档 4 中对 `max_pixels` 的默认值描述存在矛盾——其正文称“默认值为1003520”，但随后又说明“当 `vl_high_resolution_images` 为 False 时：默认值为1003520”，而文档 3 对 OCR 模型的同类参数明确给出分模型默认值（如 `qwen3.5-ocr` 默认 8388608）。由于 GUI-Plus 并非 OCR 模型，其 `max_pixels` 语义与 OCR 不同，此处应以文档 4 为准；但开发者需注意该参数实际生效逻辑依赖于 `vl_high_resolution_images` 开关状态。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus` | 控制输入图像缩放阈值（单位：像素）。OCR 模型按 `32×32` 或 `28×28` [Token](../concepts/token.md) 像素比换算；GUI-Plus 模型默认值为 1003520（`vl_high_resolution_images=False` 时）。 | OCR: `3072`/`8388608`；GUI-Plus: `1003520` |
| `output_format` | `qwen-deep-research` | 指定研究报告格式：`model_detailed_report`（约 6000 [Token](../concepts/token.md)）或 `model_summary_report`（约 1500–2000 [Token](../concepts/token.md)）。 | `model_detailed_report` |
| `vl_high_resolution_images` | `gui-plus` | 启用高分辨率图像处理（固定上限 12845056 像素），启用后忽略 `max_pixels` 设置。 | `false` |
| `enable_thinking` | `gui-plus-2026-02-26`（仅混合思考版） | 开启后返回 `reasoning_content` 字段，用于调试推理链。需通过 `extra_body` 传入。 | `false` |
| `stream` + `stream_options.include_usage` | 全部支持流式的模型 | 流式响应中是否在最后一块返回 `usage`（含 `input_tokens`/`output_tokens`）。 | `false` |

## 使用方式

### 域名与认证
所有模型**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。`{WorkspaceId}` 在百炼控制台「业务空间详情」页获取。API Key 需已配置至环境变量 `DASHSCOPE_API_KEY`，并安装对应 SDK（[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）。

### 调用示例（通用流程）
1. **构造 `messages`**：
   - OCR / GUI-Plus：`content` 为 `[{type: "image_url", image_url: {url: "..."}}, {type: "text", text: "prompt"}]`
   - 意图识别：System Message 必须包含 `Response in INTENT_MODE.` 或明确的标签列表指令
   - 深度研究：需两步调用——先发初始请求获反问，再将反问+用户澄清作为上下文二次请求
2. **指定 `model` 名称**（如 `"qwen3.5-ocr"`）
3. **设置 `base_url`**（OpenAI SDK）或 `dashscope.base_http_api_url`（DashScope SDK）
4. **发起请求**（注意：`qwen-deep-research` 仅支持 DashScope Python SDK）

完整代码示例请参考 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 与 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中的 Python/OpenAI 片段。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR 与 GUI-Plus 支持华北2、新加坡、美国弗吉尼亚三地，但各地区 endpoint 不同，需显式配置。
- **接口兼容性**：`qwen-deep-research` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，仅 DashScope Python SDK 可用；其余模型均支持 OpenAI 兼容模式。
- **流式支持差异**：`qwen-deep-research` 响应含多阶段 `phase` 字段（如 `ResearchPlanning`, `WebResearch`），客户端需解析 `output.message.phase` 判断当前阶段；OCR 与 GUI-Plus 的流式响应结构与标准 OpenAI 兼容。
- **Token 成本与免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度；其他模型按实际用量计费，具体成本见各模型文档。
- **图像处理限制**：OCR 模型对超大图像（如 >30000×32×32 像素）需申请提额；GUI-Plus 的 `vl_high_resolution_images=True` 时，图像将强制缩放到 12845056 像素以内，可能影响细粒度控件识别精度。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


