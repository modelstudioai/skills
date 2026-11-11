# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，包括意图理解、深度研究、OCR识别与GUI自动化等。这些模型在各自领域具备更强的专业能力与更优的性能表现，开发者可根据业务场景按需选用。所有模型均支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，但部分模型存在地域、SDK 或协议限制。

## 支持的模型/功能

当前 `more models` 类别下主要包含以下四类专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级用户意图识别与工具调用决策，适用于对话系统中的路由与[函数调用](../concepts/function-calling.md)前置判断。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，支持两阶段交互式研究（反问确认 + 深度分析），可自动规划研究路径、执行网络搜索并生成结构化报告，**仅限华北2（北京）地域使用**，且**仅支持 DashScope Python SDK**，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR识别模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr` 等系列，专为图像文本提取与结构化信息抽取设计，支持多分辨率图像输入与自定义 Prompt 提取字段。
- **GUI自动化模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），面向桌面界面操作任务，支持结合截图与工具调用完成鼠标键盘控制、应用启动、窗口交互等，需配合 `computer_use` 工具函数使用。

> **注意**：文档 4 中 `vl_high_resolution_images` 参数说明存在矛盾——其描述称该参数“默认值为 `false`”，但后续示例代码中却显式传入 `{"vl_high_resolution_images": True}` 且未标注此为非常规配置；同时文档未明确 `gui-plus` 是否支持除华北2外的其他地域。建议以控制台实际可用模型列表及最新 SDK 文档为准。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus` | 图像预处理像素阈值，影响 OCR/GUI 识别精度与延迟。不同模型单位换算规则不同（如 `qwen3.5-ocr` 为 `32×32`/token）[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) | `qwen3.5-ocr`: 3072 / 8388608；`gui-plus`: 3136 / 1003520（`vl_high_resolution_images=false`时） |
| `output_format` | `qwen-deep-research` | 控制研究报告输出粒度：`model_detailed_report`（约6000 Token）或 `model_summary_report`（约1500–2000 Token） | `model_detailed_report` |
| `enable_thinking` | `gui-plus-2026-02-26` | 是否启用混合思考模式，开启后返回 `reasoning_content` 字段 | `false` |
| `stream` + `stream_options.include_usage` | 所有支持流式的模型 | 流式响应中是否在末尾数据块返回 token 消耗统计 | `false` |

## 使用方式

### 基础前提
- 已在百炼控制台创建业务空间并获取对应 `WorkspaceId`；
- 已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 根据模型要求安装对应 SDK（如 `qwen-deep-research` 仅支持 DashScope Python SDK）。

### 推荐调用域名
为获得最佳性能与稳定性，**强烈建议迁移至业务空间专属域名**：
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`

> **注意**：文档 1 与文档 3 均强调专属域名迁移建议，但文档 2 仅提及华北2地域支持，未说明其是否也应使用专属域名。实践中，`qwen-deep-research` 同样需使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`（见文档 2 的 Python 示例），因此所有模型均应统一采用专属域名。

### 典型调用模式
- **意图识别**：需严格设置 System Message，含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯标签分类）；
- **深度研究**：必须分两步调用——先发起研究请求获取澄清问题，再将问题+用户回答作为上下文二次调用；
- **OCR/GUI**：`messages.content` 必须为数组，支持 `text` 与 `image_url` 混合输入；图像 URL 需可公开访问或使用 Base64 Data URL。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen3.5-ocr` 和 `gui-plus` 在华北2、新加坡、美国（弗吉尼亚）均可用。
- **协议与 SDK 限制**：
  - `qwen-deep-research` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，仅 DashScope Python SDK 可用；
  - `dashscope CLI` 当前不支持 `understanding` 子命令，意图识别需用 Python SDK [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
  - `gui-plus` 的 `enable_thinking` 和 `vl_high_resolution_images` 为非 OpenAI 标准参数，Python SDK 中需置于 `extra_body` 对象内传递。
- **图像处理限制**：`qwen-vl-ocr` 系列模型对 `max_tokens` 有硬性上限（如 `qwen-vl-ocr` 默认 4096），若需提升至 4097–8192，须联系商务经理申请。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 Token 免费额度，详见其计费说明。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


