# Qwen 基础大模型与 Qwen 机器翻译模型对比

本文旨在帮助开发者清晰区分百炼平台上两类核心能力：**通用基础大模型（Qwen 系列）** 与 **垂直领域专用模型（Qwen-MT 系列）**。随着多语言、多模态内容处理需求激增，准确理解二者在定位、能力边界、接口设计及成本结构上的差异，对构建高性能、高性价比的 AI 应用至关重要。本对比基于当前（2024 年底）百炼平台正式发布的 API 规范与模型能力说明，聚焦技术选型关键维度，不涉及内部训练细节或未公开实验性功能。

## 关键维度对比

| 维度 | Qwen 基础大模型（如 `qwen3.8-max`, `qwen-flash`, `qwen3-vl-plus` 等） | Qwen 机器翻译模型（`qwen-mt`, `qwen-mt-image`, `qwen-mt-uni`） |
|------|--------------------------------------------------------------------|-------------------------------------------------------------|
| **核心定位** | 通用人工智能底座：支持开放式文本生成、推理、代码、多模态理解、工具调用等泛化任务 | 垂直领域专用模型：聚焦高保真、强结构化、跨模态的翻译任务，强调语义一致性、格式保留与领域适配 |
| **输入格式** | 灵活多样：<br>• Chat API：标准 `messages` 数组（含 `system`/`user`/`assistant`/`tool` 角色）<br>• Responses API：支持纯字符串 `input` 或结构化 `EasyInputMessage`<br>• DashScope 原生：`text-generation`（纯文本）或 `multimodal-generation`（图像/视频 URL/Base64） | 严格按模态定义：<br>• `qwen-mt`：`{"text": "..."}`<br>• `qwen-mt-image`：`{"image": "https://..."}` 或 Base64<br>• `qwen-mt-uni`：`{"file": "base64_or_url", "file_type": "pdf/docx/png/wav"}`<br>**不接受 `messages` 数组或 `system` 消息** |
| **输出格式** | 非结构化为主，可配置流式（`stream: true`）；Responses API 支持 `ResponseOutputMessage` 结构；Anthropic API 支持 JSON Schema 强约束输出 | 固定结构化输出：<br>• `text`（默认）：纯翻译结果字符串<br>• `json`：含 `source_text`, `translated_text`, `confidence`, `bounding_boxes`（图像/文档）等字段<br>• `pdf`：重排版后带原文位置映射的 PDF 文件（仅 `qwen-mt-image`/`qwen-mt-uni`）<br>**不支持流式响应（`stream` 参数被忽略）** |
| **支持模型** | 覆盖广泛：<br>• 文本：`qwen3.8-max`, `qwen3.7-plus`, `qwen-flash`<br>• 多模态：`qwen3.8-omni-flash`, `qwen3-vl-plus`, `Qwen2.5-VL`<br>• 代码/数学/音频：`qwen3-coder-flash`, `qwen-math`, `qwen-audio`<br>• 第三方：`deepseek-v4.1-flash-1017`, `glm-5.3`, `kimi-k3` | 专用模型族：<br>• `qwen-mt`（纯文本）<br>• `qwen-mt-image`（图像 OCR+翻译）<br>• `qwen-mt-uni`（全模态统一翻译）<br>**不支持通用 Qwen 模型或第三方模型** |
| **API 端点** | 多协议并行：<br>• OpenAI 兼容 Chat：`/compatible-mode/v1/chat/completions`<br>• OpenAI 兼容 Responses：`/compatible-mode/v1/responses`<br>• DashScope 原生：`/api/v1/services/aigc/text-generation/generation` 或 `/multimodal-generation/generation`<br>• Anthropic 兼容：`/apps/anthropic/v1/messages` | 统一服务端点：<br>• OpenAI 兼容模式：`/api/v1/services/aigc/multimodal-translation`<br>• DashScope 原生模式：`/api/v1/services/aigc/multimodal-translation/generation`（需显式指定 `service: "multimodal-translation"`）<br>**无 Anthropic 兼容路径** |
| **计费方式** | 按 **输入 + 输出 tokens 总数** 计费（不同模型 token 定价不同）；视频/图像按 `total_pixels` 折算为 token 当量；工具调用（如 `web_search`）单独计费 | 按 **实际处理单元** 计费：<br>• 文本：按输入 tokens 计费<br>• 图像：按分辨率当量（`width × height`）计费<br>• PDF/DOCX：按页数计费<br>• 音频：按时长（秒）计费<br>**术语表（`glossary`）不额外计费** |
| **典型场景** | • 多轮智能对话助手<br>• 自动生成报告/邮件/文案<br>• 代码解释与生成<br>• 网页内容摘要与联网搜索<br>• 视频理解与关键帧分析<br>• 数学证明与逻辑推理 | • 跨语言文档本地化（法律合同、产品手册）<br>• 手机截图/扫描件实时翻译（保留表格/公式布局）<br>• PPT/Word/PDF 一键双语对照生成<br>• 教育场景：教材图片中公式+文字同步翻译<br>• 出海电商：商品图+描述批量多语种生成 |

## 各方案适用场景建议

- **选择 Qwen 基础大模型，当您需要：**  
  ✅ 构建具备自主思考、工具调用、多轮记忆的通用 AI 助手；  
  ✅ 对非结构化输入（如自由提问、长篇文档、复杂指令）进行开放式生成；  
  ✅ 利用 `system` 消息定制角色、设定规则或注入知识；  
  ✅ 要求低延迟流式响应（如聊天界面逐字输出）；  
  ❌ 不推荐用于对翻译质量、术语一致性、格式保真度有严苛要求的生产级本地化任务——其翻译能力属“副产物”，缺乏领域微调与结构化输出保障。

- **选择 Qwen 机器翻译模型，当您需要：**  
  ✅ 生产环境交付专业级翻译结果（尤其法律、医疗、技术文档）；  
  ✅ 处理含复杂排版的图像/PDF/幻灯片，并严格保留原文位置与样式；  
  ✅ 统一接入文本、图像、音频、文档多种源格式，使用同一套 API 流程；  
  ✅ 通过 `glossary` 参数强制术语统一（如品牌名、产品型号）；  
  ✅ 获取带置信度、坐标、段落对齐信息的结构化翻译元数据；  
  ❌ 不推荐用于需要上下文持续推理、多步任务规划或生成非翻译类内容（如写诗、编故事）的场景。

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **是否需多轮对话状态管理？** | Qwen 基础模型（Responses API） | 使用 `previous_response_id` 实现无状态服务端会话缓存；Qwen-MT 无此能力，每次请求均为独立翻译任务。 |
| **是否需自定义系统指令（`system` prompt）？** | Qwen 基础模型 | `system` 是 Chat/Responses/Anthropic 接口的核心参数；Qwen-MT **完全忽略 `system` 字段**，所有控制必须通过 `parameters`（如 `source_language`, `preserve_layout`）显式声明。 |
| **是否需处理图像/PDF/音频并保持原始布局？** | Qwen-MT-Uni 或 Qwen-MT-Image | 基础 Qwen 多模态模型（如 `qwen3-vl-plus`）可“理解”图像，但无法输出重排版 PDF 或带坐标的 JSON；Qwen-MT 系列专为此优化。 |
| **是否需术语强管控与领域适配？** | Qwen-MT 系列 | `glossary` 参数为 Qwen-MT 独有，且在 `qwen-mt-uni` v2.3+ 中已实测生效；基础模型仅能通过 prompt 提示，效果不可控。 |
| **是否需最低延迟流式响应？** | Qwen 基础模型（Chat API） | Qwen-MT **明确不支持流式**，必须等待完整结果返回；若 UI 依赖渐进式渲染，应避免选用。 |
| **是否需调用外部工具（如搜索、计算器）？** | Qwen 基础模型（Responses / Anthropic API） | Qwen-MT 为纯翻译服务，无工具调用能力；若需“先搜索再翻译”，须由上层应用组合调用。 |
| **是否需兼容 Anthropic 协议（如 `thinking` 块、JSON Schema 输出）？** | Qwen 基础模型（Anthropic 兼容 Messages API） | Qwen-MT 仅支持 OpenAI 兼容与 DashScope 原生协议，无 Anthropic 路径。 |

> **重要提醒**：  
> - **不要混用模型与接口**：向 `/chat/completions` 端点传 `qwen-mt` 模型名将返回错误；向 `/multimodal-translation` 端点传 `qwen3.8-max` 将被拒绝。  
> - **认证与域名一致**：两者均使用百炼 Workspace 专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）及相同 API Key 认证方式。  
> - **调试建议**：首次集成 Qwen-MT 时，务必使用 `format: "json"` 查看结构化输出字段；集成基础模型时，优先测试 Responses API 的 `previous_response_id` 多轮能力。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


