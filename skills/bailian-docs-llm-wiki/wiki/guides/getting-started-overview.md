# getting started [overview](overview.md)

ParseX 是面向开发者和 Agent 应用的文档智能平台，提供文档解析（Parse）与信息抽取（Extract）两类核心能力，将非结构化文档、图片、音视频等材料转化为可编程处理的内容或结构化字段。开发者可根据任务目标选择合适的能力路径，并通过配置复用降低集成成本。本文档为快速上手的概览指引，覆盖能力边界、关键参数、调用方式及常见约束。

## 支持的模型/功能

- **Parse 文档解析**：支持 PDF、Word、Excel、PPT、图片（含扫描件）、音频、视频等格式；输出包括正文文本、语义分段、表格结构、图像描述、音视频时间戳对齐内容等。适用于需理解上下文、构建检索库或生成摘要的场景。  
- **Extract 信息抽取**：基于用户定义的字段 Schema（如 `contract_amount: number`, `sign_date: date`），从图文材料中提取结构化结果，并附带原文定位（page、bbox、text snippet）。字段定义支持正则、语义匹配、多模态联合判断等多种策略。  
- 两种能力可组合使用：例如先用 Parse 获取高质量图文解析结果，再作为 Extract 的输入源，提升抽取准确率与稳定性。详见 [产品概览](../../raw/application-user-guide/getting-started-overview.md) 中的“标准工作流”部分。

## 关键参数

- `task_type`：必填，取值为 `"parse"` 或 `"extract"`，决定底层执行路径。  
- `file_url` 或 `file_bytes`：原始文件输入方式，推荐使用预签名 URL（`file_url`）以避免请求体过大；音视频需确保可公开访问且支持流式读取。  
- `config_id`（仅 Extract）：指向已保存的字段配置 ID；首次调试建议使用 `config_definition` 直接内联定义字段 Schema，避免配置未同步导致结果偏差。  
- `parse_options`（仅 Parse）：可选控制解析粒度，如 `enable_ocr: true`（默认启用）、`enable_table_recognition: true`、`max_pages: 50` 等。完整参数见 [Parse 文档解析](../../raw/application-user-guide/getting-started-overview/overview.md)。  
- > **注意**：`max_pages` 在 `parse_options` 中单位为页，但在某些旧版 SDK 示例中被误标为“字符数”，请以 [Parse 文档解析](../../raw/application-user-guide/getting-started-overview/overview.md) 定义为准。

## 使用方式

1. **控制台验证优先**：在百炼控制台「ParseX」模块上传样本文件，选择 Parse 或 Extract 模式，实时查看结构化输出与可视化溯源（如表格还原、字段高亮）。这是调试字段定义与解析效果的最高效方式。  
2. **API 集成**：调用 `/v1/parse` 或 `/v1/extract` 接口，按需传入参数。推荐使用官方 SDK（Python/Java/Go），自动处理鉴权、重试与 multipart 上传。  
3. **配置复用**：控制台中保存的配置可通过 `config_id` 复用；生产环境应避免硬编码 `config_definition`，防止字段变更时服务不可控。配置管理逻辑详见 [Extract 信息提取](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

## 限制和注意事项

- 单文件大小上限：Parse 为 200 MB，Extract 为 50 MB（因依赖解析前置结果，实际建议 ≤20 MB 以保障响应延迟 <15s）。  
- 音视频时长限制：单文件 ≤ 2 小时；超长视频建议按场景切分后并行处理。  
- 字段抽取可靠性依赖输入质量：扫描件 OCR 错误率 >15% 时，Extract 准确率显著下降；建议 Parse 阶段开启 `enable_ocr_correction: true`（需对应模型版本支持）。  
- > **注意**：文档中“面向 Agent 的典型场景”表格所列“应用如何继续使用”属于参考性业务逻辑，不构成 ParseX 的功能承诺；具体下游处理（如规则核验、历史比对）需由开发者自行实现，详见 [产品概览](../../raw/application-user-guide/getting-started-overview.md)。

## 来源文档

- [产品概览](../../raw/application-user-guide/getting-started-overview.md)


