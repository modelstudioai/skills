# Qwen 基础大模型与 Qwen 机器翻译模型对比

## 背景与目的  
Qwen 系列模型在百炼平台上提供两类核心能力：通用大语言模型（LLM）和专用机器翻译模型（MT）。尽管二者同源（均基于 Qwen 底座优化），但在设计目标、输入输出范式、能力边界及工程集成方式上存在本质差异。本文旨在为开发者提供清晰、可落地的技术选型参考，帮助其根据实际业务场景（如是否需要多轮对话、是否强依赖格式保真、是否处理非文本模态等）快速判断应选用 `qwen-*`（如 `qwen-max`）还是 `qwen-mt-*`（如 `qwen-mt-uni`）系列模型，避免因接口误用导致功能缺失、计费异常或体验降级。

---

## 关键维度对比

| 维度 | Qwen 基础大模型（`qwen-max` / `qwen-plus` / `qwen-turbo`） | Qwen 机器翻译模型（`qwen-mt` / `qwen-mt-image` / `qwen-mt-uni`） |
|------|-----------------------------------------------------------|----------------------------------------------------------------|
| **核心定位** | 通用文本生成与推理引擎，支持问答、摘要、代码、创作、工具调用等泛化任务 | 专用跨语言转换引擎，聚焦语义对齐、格式保真与多模态内容理解（OCR/ASR） |
| **输入格式** | 标准 `messages` 数组（含 `role` + `content`），支持多轮对话上下文；`content` 可为纯文本或结构化 JSON（如工具调用参数） | 按模型类型区分：<br>• `qwen-mt`：`{"text": "..."}`<br>• `qwen-mt-image`：`{"image_url": "...", "text": "..."}` 或 base64 图片<br>• `qwen-mt-uni`：支持 `text`/`image`/`document`/`audio` 四类 `input_type`，需显式声明 |
| **输出格式** | 原生生成文本（`choices[0].message.content`），流式响应支持 `data: {...}`（OpenAI）或 JSON 数组（DashScope）；工具调用返回结构化 `tool_use` 对象 | 结构化 JSON 响应，含 `translated_text`、`source_language`、`target_language` 等字段；`qwen-mt-image` 和 `qwen-mt-uni` 额外返回坐标信息、排版标记、原文段落映射等；**不支持流式响应** |
| **支持模型** | `qwen-max`（高精度）、`qwen-plus`（均衡）、`qwen-turbo`（低延迟） | `qwen-mt`（纯文本）、`qwen-mt-image`（图像OCR+翻译）、`qwen-mt-uni`（全模态：文本/图/文档/音频） |
| **API 端点（典型）** | • OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`<br>• DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | • `qwen-mt`：`https://dashscope.aliyuncs.com/api/v1/services/aigc/multilingual-translation/text`<br>• `qwen-mt-image`：`https://dashscope.aliyuncs.com/api/v1/services/aigc/multilingual-translation/image`<br>• `qwen-mt-uni`：`https://dashscope.aliyuncs.com/api/v1/services/aigc/multilingual-translation/uni` |
| **关键参数差异** | • 通用参数：`temperature`, `top_p`, `max_output_tokens`（DashScope）/`max_tokens`（OpenAI）<br>• 工具调用：`tools`, `tool_choice`（仅 Anthropic/DashScope 接口支持） | • 必填参数：`source_language`, `target_language`<br>• 模型专属参数：`preserve_format`（仅 image/uni）、`input_type`（仅 uni）、`response_format`（`json`/`text`）<br>• **无 `temperature`/`top_p` 等采样控制参数**（翻译结果确定性优先） |
| **计费方式** | 按 **输入 token + 输出 token** 总和计费（统一计入 `text-generation` 计量单元）；不同模型单价不同（`qwen-max` > `qwen-plus` > `qwen-turbo`） | 按 **请求次数 + 输入内容复杂度** 计费：<br>• `qwen-mt`：按字符数阶梯计费（≤8192 字符/次）<br>• `qwen-mt-image`：按图片分辨率与 OCR 文本量综合计费<br>• `qwen-mt-uni`：按输入类型加权计费（文档/音频 > 图片 > 文本）；**不按 token 计费** |
| **典型场景** | • 多轮客服对话<br>• 技术文档摘要与改写<br>• 代码生成与解释<br>• 结合搜索/数据库的智能助手<br>• 需要逻辑推理或创造性输出的任务 | • 网站/APP 多语言实时翻译<br>• 扫描件/PDF 合同双语对照生成<br>• 教育课件图文混排翻译（保留表格、公式位置）<br>• 视频字幕自动翻译（音频→文本→翻译）<br>• 出海电商商品页批量本地化 |

---

## 适用场景建议

### ✅ 选择 Qwen 基础大模型，当您的需求满足以下任一条件：
- 需要**多轮上下文感知**（如用户连续追问、历史记忆）；
- 任务本质是**生成、推理或决策**（如“总结会议纪要”“将需求转为 SQL”“分析错误日志原因”）；
- 需要**调用外部工具**（如查天气、搜知识库、执行计算）；
- 输入为**非结构化自然语言指令**，且输出需具备创造性或多样性（如文案润色、故事续写）；
- 已有 OpenAI 兼容 SDK，希望最小改造接入通用 LLM 能力。

### ✅ 选择 Qwen 机器翻译模型，当您的需求满足以下任一条件：
- 核心目标是**高保真、低延迟的语言转换**，且对术语一致性、格式还原（如 PDF 表格、图片文字位置）有硬性要求；
- 输入源为**非纯文本**（扫描图片、PDF 合同、培训视频音频）；
- 需要**开箱即用的多语言支持**（100+ 语言对），无需自行构建 prompt 或微调；
- 对输出**确定性要求极高**（禁止“同义替换”“风格改写”，必须严格忠实原文）；
- 业务已明确划分为“翻译管道”（如 CMS 内容出海），需独立计量、监控与 SLA 保障。

> ⚠️ **特别注意**：  
> - 不要用 `qwen-*` 模型做专业文档翻译——缺乏格式保真能力，易破坏表格结构、丢失脚注编号；  
> - 不要用 `qwen-mt-*` 模型做问答或摘要——无对话状态管理、不支持 `system` 角色指令、无法执行推理；  
> - 若需“翻译 + 解释”，应采用**组合调用**：先用 `qwen-mt` 获取精准译文，再将译文送入 `qwen-*` 进行二次处理。

---

## 开发者技术选型参考

| 选型问题 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **我的应用是双语客服机器人，需理解用户方言并生成本地化回复** | `qwen-plus`（DashScope 接口） + 自建翻译后处理模块 | 基础模型支持方言理解与多轮对话；翻译需结合业务术语表定制，通用 MT 模型难以覆盖垂直领域表达 |
| **我要把 500 页英文技术手册 PDF 翻译成中文，并保持目录层级与图表编号** | `qwen-mt-uni`（`input_type: document`） | 唯一支持 PDF 结构解析与排版重建的模型；`qwen-*` 无法识别 PDF 逻辑结构，`qwen-mt` 仅支持纯文本 |
| **我需要将手机拍摄的菜单照片实时翻译为英文，且标注每道菜在图中的位置** | `qwen-mt-image` | 原生支持 OCR 坐标输出与图文对齐；`qwen-*` 无法直接处理图像输入，需额外集成视觉模型 |
| **我正在迁移 OpenAI 应用，希望快速替换为国产模型，且已有大量 `messages` 格式 prompt** | `qwen-turbo`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） | 接口完全兼容，仅需修改 `model` 参数；`qwen-mt-*` 的输入结构完全不同，需重写请求逻辑 |
| **我要为跨境电商平台实现商品标题自动翻译，要求 99% 以上术语准确率（如“USB-C”不译为“通用串行总线-C”）** | `qwen-mt` + 自定义术语词典（通过百炼平台术语管理功能注入） | `qwen-mt` 提供术语强制保留机制；`qwen-*` 的自由生成特性会导致术语被意译或省略 |

> 💡 **最佳实践提示**：  
> - 在百炼控制台启用 **「模型能力沙箱」**，对同一份测试数据并行调用两类模型，直观对比输出质量与延迟；  
> - 使用 `qwen-mt-uni` 处理混合输入时，务必在请求中显式指定 `input_type`，否则默认按 `text` 解析，导致图片/音频上传失败；  
> - 调用 `qwen-*` 进行翻译任务时，若需稳定结果，请固定 `temperature=0` 并关闭 `top_p`，但效果仍显著弱于专用 MT 模型。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


