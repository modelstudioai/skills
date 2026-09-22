# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、OCR、深度研究和GUI自动化等方向。这些模型在通用大模型基础上进行了领域精调与能力增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，适用于高精度、低延迟、强结构化输出的生产级任务。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 适用场景 | 文档引用 |
|----------|------|-----------|------------|-----------|
| `farui-plus` | 法律大模型 | 法律问答、案情推理、文书生成、合同审查、RAG检索增强 | 法律咨询、司法辅助、合规审查 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策（INTENT_MODE）、多标签分类 | 智能客服路由、Agent 工具选择、语音助手语义解析 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 机器翻译模型 | 多语言互译、术语干预、翻译记忆（TM）、领域提示（IT/金融/医疗等） | 技术文档本地化、合同双语生成、跨语言内容分发 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | OCR 模型 | 图像文本提取、结构化信息抽取（如车票/发票/合同）、多分辨率自适应处理 | 票据识别、表单录入、文档数字化、视觉内容分析 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 + 网络搜索 + 报告生成）、引用溯源、多轮规划 | 行业竞品分析、政策影响评估、学术文献综述、市场调研 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `gui-plus-*` | GUI 自动化模型 | 屏幕理解、UI 元素定位、鼠标键盘操作指令生成、混合思考模式（可选） | 桌面应用自动化测试、RPA 流程编排、无障碍交互辅助 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 模型**仅支持华北2（北京）地域**，且**不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，必须使用 Python DashScope SDK 调用 —— 此限制在 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中明确说明，与其他模型的多语言 SDK 支持存在显著差异。

## 关键参数

所有模型均支持以下通用参数（部分为非 OpenAI 标准参数，需按 SDK 要求放入 `extra_body` 或顶层）：

| 参数名 | 类型 | 默认值 | 说明 | 注意事项 |
|--------|------|--------|------|-----------|
| `temperature` | `float` | `0.01` | 控制输出随机性；值越高越多样，建议与 `top_p` 二选一 | 所有模型一致，[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 和 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 均采用此默认值 |
| `top_p` | `float` | `0.001`（intent-detect）、`0.01`（gui-plus）、`0.001`（farui） | 核采样阈值；值越高越多样 | 各模型默认值不统一，开发时需显式检查文档 |
| `max_tokens` | `integer` | 按模型而异（如 `farui-plus`: 2k, `qwen3.5-ocr`: 32768） | 限制输出长度；超长将被截断 | `qwen-vl-ocr` 系列默认为 4096，如需提升至 8192 需联系商务申请 —— 见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `stream` | `boolean` | `false` | 是否启用流式响应 | `farui-plus`、`qwen-deep-research`、`qwen3.5-ocr` 等均支持，但 `qwen-deep-research` 的流式响应结构含 `phase` 字段（如 `"ResearchPlanning"`），需特殊解析 |
| `vl_high_resolution_images` | `boolean` | `false` | （仅 `gui-plus-*`）启用高分辨率图像处理（固定上限 12845056 像素） | 非 OpenAI 标准参数，Python SDK 中须置于 `extra_body` |
| `translation_options` | `object` | — | （仅 `qwen-mt-plus`）控制源/目标语言、术语表、翻译记忆、领域提示 | 必须通过 `extra_body` 传入 OpenAI SDK，见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |

## 使用方式

### 1. 基础调用流程
- ✅ **前置准备**：获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`），安装对应 SDK（[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；
- ✅ **域名迁移**：强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 —— 此要求在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 和 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中多次强调；
- ✅ **模型选择**：根据场景严格选用对应模型 ID（如法律场景用 `farui-plus`，勿误用 `qwen-mt-plus`）。

### 2. 多模态输入（图像类模型）
- `qwen3.5-ocr` 和 `gui-plus-*` 支持 `image_url` 类型消息，需在 `content` 数组中组合 `{"type": "image_url", "image_url": {"url": "..."}, "min_pixels": ..., "max_pixels": ...}` 与文本 Prompt；
- `min_pixels` / `max_pixels` 的默认值与取值范围因模型版本而异（如 `qwen3.5-ocr` 每 [Token](../concepts/token.md) 对应 `32×32` 像素，`qwen-vl-ocr` 旧版为 `28×28`），务必查阅对应文档。

### 3. 特殊交互模式
- **意图识别**：需在 `system` message 中声明 `Response in INTENT_MODE.` 并注入工具定义或意图字典；
- **深度研究**：必须执行两阶段调用：第一阶段获取模型反问（`stream=True`），第二阶段将反问+用户回答作为上下文再次调用；
- **GUI 自动化**：需在 `system` message 中提供完整工具签名（`<tools>` XML），响应格式强制为 `Action` + `<tool_call>...<tool_call>` JSON 块。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；
- **SDK 限制**：`qwen-deep-research` 仅支持 Python DashScope SDK，Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)均不可用；
- **流式响应解析**：`qwen-deep-research` 的流式响应含 `phase` 字段（如 `"WebResearch"`、`"answer"`），需按阶段解析 `extra.deep_research` 结构；`farui-plus` 流式响应则为标准 `Generation` 对象数组；
- **成本与限流**：各模型输入/输出 [Token](../concepts/token.md) 成本不同（如 `farui-plus` 输入 20元/百万 [Token](../concepts/token.md)），且受全局限流策略约束 —— 详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **图像分辨率适配**：`qwen3.5-ocr` 与 `gui-plus-*` 的 `min_pixels`/`max_pixels` 计算逻辑依赖像素/Token 比例，错误设置会导致图像缩放异常或请求拒绝；
- **安全实践**：API Key 务必配置于环境变量，禁止硬编码；生产环境应使用最小权限 API Key，并启用 IP 白名单。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


