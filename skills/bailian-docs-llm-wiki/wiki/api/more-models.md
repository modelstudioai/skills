# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，包括机器翻译（Qwen-MT）、意图理解（tongyi-intent-detect-v3）、深度研究（Qwen-Deep-Research）、OCR识别（Qwen-OCR）和界面交互（GUI-Plus）。这些模型通过统一的 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或 DashScope SDK 调用，支持多地域部署与精细化参数控制，适用于对准确性、领域适配性或交互能力有强需求的生产场景。

## 支持的模型/功能

- **Qwen-MT**：专用于高质量机器翻译，支持源/目标语言自动检测、术语干预、翻译记忆（TM）和领域提示（如 IT、金融等），[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **tongyi-intent-detect-v3**：毫秒级意图识别模型，支持两种模式：① 输出结构化[函数调用](../concepts/function-calling.md)（`INTENT_MODE`），② 仅输出预定义意图标签（可简化为单 [Token](../concepts/token.md) 提升性能），[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research**：两阶段研究型模型（反问确认 → 深入分析），支持联网检索、引用溯源与多格式报告生成（`model_detailed_report` / `model_summary_report`），**仅限华北2（北京）地域且仅支持 DashScope Python SDK**，[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR**（含 `qwen3.5-ocr` 等）：支持图像文本提取与结构化信息抽取（如车票、合同），兼容多分辨率输入（`min_pixels`/`max_pixels` 控制缩放），支持[流式输出](../concepts/streaming-output.md)与 [Token](../concepts/token.md) 统计，[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus**：面向桌面 GUI 自动化任务的视觉-语言模型，支持工具调用（如 `computer_use`）、高分辨率图像处理（`vl_high_resolution_images`）及可选思考链（`enable_thinking`），[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 4 和文档 5 中关于 `max_pixels` 默认值的描述存在不一致。文档 4（Qwen-OCR）明确说明 `qwen-vl-ocr` 及之前模型的 `min_pixels` 默认值为 `3136`（即 `4×28×28`），而文档 5（GUI-Plus）在 `min_pixels` 描述中重复该值但未区分模型版本；同时文档 5 对 `max_pixels` 的默认值描述依赖于 `vl_high_resolution_images` 开关状态，而文档 4 则按模型版本给出具体数值（如 `qwen3.5-ocr` 默认 `8388608`）。实际使用时请以各模型对应文档为准，并优先参考最新模型（如 `qwen3.5-ocr`）的参数说明。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例/默认值 |
|------|----------|------|-------------|
| `base_url` | 所有 OpenAI 兼容模型 | 必须使用业务空间专属域名，地域决定 endpoint：<br>北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`<br>美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 在控制台「业务空间详情」获取 |
| `translation_options` | Qwen-MT | 包含 `source_lang`, `target_lang`, `terms`（术语表）, `tm_list`（翻译记忆）, `domains`（领域提示） | `{"source_lang": "Chinese", "target_lang": "English", "terms": [{"source":"生物传感器","target":"biological sensor"}]}` |
| `output_format` | Qwen-Deep-Research | 控制报告详略程度 | `"model_detailed_report"`（默认，~6000 [Token](../concepts/token.md)）或 `"model_summary_report"`（~1500–2000 Token） |
| `min_pixels` / `max_pixels` | Qwen-OCR, GUI-Plus | 图像预处理像素阈值，单位为像素；不同模型每 Token 对应像素不同（如 `qwen3.5-ocr`: `32×32`） | `qwen3.5-ocr`: `min_pixels=3072`, `max_pixels=8388608` |
| `vl_high_resolution_images` | GUI-Plus | 启用后忽略 `max_pixels`，固定上限为 `12845056` 像素 | `true` 或 `false`（默认） |
| `enable_thinking` | GUI-Plus（仅 `gui-plus-2026-02-26`） | 开启后返回 `reasoning_content` 字段 | `true`（需置于 `extra_body`） |

## 使用方式

- **认证与初始化**：所有模型均需 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置；OpenAI SDK 需显式传入 `base_url`，DashScope SDK 需设置 `workspace` 和 `region`。
- **请求构造**：
  - Qwen-MT、Qwen-OCR、GUI-Plus：使用 `chat/completions` 接口，`messages` 中 `content` 为数组（支持 `text` + `image_url` 混合）。
  - tongyi-intent-detect-v3：`messages[0]` 必须为 `system` 角色，内容需包含 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.` 指令。
  - Qwen-Deep-Research：**仅支持 DashScope `Generation.call`**，使用 `services/aigc/text-generation/generation` endpoint，且必须分两步调用（反问 → 深入）。
- **流式响应**：Qwen-OCR 和 GUI-Plus 支持 `stream=true`；Qwen-Deep-Research 原生[流式输出](../concepts/streaming-output.md)各阶段（`ResearchPlanning`, `WebResearch`, `answer`），需解析 `phase` 字段；Qwen-MT 和 intent 模型暂不提供原生流式支持。

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research **仅支持华北2（北京）地域**，其他模型虽支持多地域，但 API Key 与 `base_url` 必须匹配（例如北京地域 Key 不可用于新加坡 endpoint）。
- **SDK 限制**：Qwen-Deep-Research **不支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)和 Java SDK**，仅可通过 DashScope Python SDK 调用；GUI-Plus 的 `enable_thinking` 和 `vl_high_resolution_images` 等非标准参数，在 Python SDK 中必须放入 `extra_body`，Node.js/HTTP 中作为顶层参数。
- **输入规范**：Qwen-OCR 和 GUI-Plus 的 `image_url` 支持 HTTP URL 或 Base64 Data URL；本地文件需先上传至可公开访问地址或使用百炼控制台提供的临时上传服务。
- **成本与额度**：tongyi-intent-detect-v3 提供开通后 90 天内 100 万 Token 免费额度，详见其文档；其他模型按实际输入/输出 Token 计费，`usage` 字段在响应中返回（Qwen-Deep-Research 在 `output.usage`，Qwen-OCR/GUI-Plus 在流式末块或非流式响应中）。
- **稳定性建议**：所有模型均**强烈建议迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性不及新域名。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


