# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，涵盖意图理解、深度研究、GUI界面交互和OCR文字识别等场景。这些模型通过统一的 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持精细化参数控制与多模态输入。开发者需根据业务需求选择对应模型，并注意地域、域名与 SDK 兼容性限制。

## 支持的模型/功能

- **意图理解**：`tongyi-intent-detect-v3` 模型支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由与工具编排场景。其能力详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究**：`qwen-deep-research` 模型支持两阶段交互式研究（反问确认 → 深入分析），可自动规划研究路径、执行网络搜索并生成结构化报告，**仅限华北2（北京）地域使用**，且**仅支持 Python DashScope SDK**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI界面交互**：`gui-plus` 系列模型专为桌面自动化设计，支持图像+文本多模态输入，可解析界面截图并生成鼠标/键盘操作指令（如 `computer_use` 工具调用）。
- **OCR文字识别**：`qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等模型支持高精度图像文本提取，兼容多种图像分辨率策略与像素约束配置 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

> **注意**：文档 2 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档 1 和文档 3 均提供了 OpenAI 兼容调用示例。该模型**不兼容 OpenAI 接口**，此为关键限制，非文档疏漏。

## 关键参数

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 模型名称，如 `tongyi-intent-detect-v3`、`qwen-deep-research`、`gui-plus`、`qwen3.5-ocr` | 全部 | 必填 |
| `messages.content`（GUI/OCR） | 支持 `text` + `image_url` 混合数组，`image_url.url` 可为 URL 或 Base64 Data URL | `gui-plus`, `qwen3.5-ocr` 等视觉模型 | `min_pixels`/`max_pixels` 控制图像缩放，单位为像素；不同模型像素/Token 换算关系不同（如 `qwen3.5-ocr`: 32×32 px/Token） |
| `output_format` | 指定研究报告格式：`model_detailed_report`（默认，~6000 Token）或 `model_summary_report`（~1500–2000 Token） | `qwen-deep-research` | 仅 DashScope SDK 支持 |
| `vl_high_resolution_images` | 启用高分辨率图像处理（固定上限 12845056 px），忽略 `max_pixels` | `gui-plus` | 非 OpenAI 标准参数，Python SDK 需置于 `extra_body` 中 |
| `enable_thinking` | 开启混合思考模式（仅 `gui-plus-2026-02-26` 支持），返回 `reasoning_content` 字段 | `gui-plus-2026-02-26` | 非 OpenAI 标准参数，Python SDK 需置于 `extra_body` 中 |
| `temperature` / `top_p` | 控制输出多样性，默认值分别为 `0.01`（GUI-Plus）和 `0.001`（OCR） | GUI-Plus, OCR | 建议二者只设其一；OCR 文档明确建议“设置为默认值即可” |

## 使用方式

1. **域名与认证**：  
   - 所有模型均**推荐迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
   - 必须已[获取并配置 API Key](../preparations/get-api-key.md)，并通过环境变量（`DASHSCOPE_API_KEY`）或 SDK 初始化传入。

2. **SDK 选择**：  
   - `tongyi-intent-detect-v3`、`gui-plus`、`qwen3.5-ocr`：支持 **OpenAI SDK**（需配置 `base_url`）与 **DashScope SDK**。  
   - `qwen-deep-research`：**仅支持 DashScope Python SDK**（`dashscope.Generation.call`），不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK。

3. **典型调用流程**：  
   - **意图识别**：在 `system` message 中声明 `Response in INTENT_MODE.` 并注入工具定义 JSON；或声明意图字典并要求“仅回复标签”。  
   - **深度研究**：分两步调用——第一步传入宽泛主题，解析模型反问内容；第二步将用户澄清回答作为 `assistant` message 加入上下文，再次请求。  
   - **GUI/OCR**：`user` message 的 `content` 字段必须为数组，包含 `{"type": "image_url", "image_url": {"url": "..."} }` 及可选 `{"type": "text", "text": "..."}` 提示词。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`gui-plus` 和 `qwen-vl-ocr` 支持华北2（北京）、新加坡、美国（弗吉尼亚）三地，但各地区 endpoint 不同，需按文档配置 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。  
- **SDK 限制**：`qwen-deep-research` 不支持 OpenAI 兼容接口，dashscope CLI 也不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。  
- **图像参数差异**：`gui-plus` 与 `qwen-vl-ocr` 均支持 `min_pixels`/`max_pixels`，但默认值、取值范围及像素/Token 换算规则不同，不可混用配置。  
- **输出解析**：`tongyi-intent-detect-v3` 返回含 `<tags>`/<tool_call>/`<content>` 的特殊格式，需用正则 + JSON 解析（见文档 1 中 `parse_text` 函数示例）。  
- **免费额度**：`tongyi-intent-detect-v3` 提供 100 万 Token 免费额度（开通后 90 天内），详情参见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


