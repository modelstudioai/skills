# getting started [overview](overview.md)

ParseX 是面向开发者和 Agent 应用的文档智能处理平台，提供文档解析（Parse）与信息抽取（Extract）两类核心能力，支持将非结构化文档、图片、音视频等输入转换为可编程访问的内容或结构化字段。开发者可通过 API 或控制台快速集成，适用于合同核验、报告分析、手册问答等典型场景。建议从明确任务目标出发，优先在控制台验证效果，再固化配置用于生产调用。

## 支持的模型/功能

- **Parse（文档解析）**：支持 PDF、Word、Excel、PPT、图像（含扫描件）、音频、视频等格式，输出正文文本、结构化表格、图像描述、音视频时间戳片段等内容。适用于需理解上下文、构建检索库或进行语义分析的场景。  
- **Extract（信息抽取）**：基于预定义字段 Schema（如 `contract_amount: number`, `effective_date: date`），从图文材料中提取结构化结果，并附带原文位置锚点。适用于字段明确、规则驱动的业务核验类任务。  
- 两种能力可组合使用：例如先用 Parse 获取高质量解析结果，再作为 Extract 的输入源以提升准确率。详见 [产品概览](../../raw/application-user-guide/getting-started-overview.md) 中的“标准工作流”说明。

## 关键参数

- **`task_type`**：必填，取值为 `"parse"` 或 `"extract"`，决定底层处理链路。  
- **`file_url` / `file_bytes`**：输入源，支持公网可访问 URL 或 base64 编码二进制数据；视频/音频需确保时长 ≤ 30 分钟（超限将截断）。  
- **`config_id`**（仅 Extract）：指向已保存的字段 Schema 配置；首次调试建议省略该参数，直接传入 `schema` 字段定义。  
- **`options`**（可选）：控制解析粒度（如 `table_mode: "markdown"`）、OCR 强度（`ocr_engine: "advanced"`）等，具体选项见 [Parse 文档解析](../../raw/application-user-guide/getting-started-overview/overview.md) 和 [Extract 信息提取](../../raw/application-user-guide/getting-started-overview/extract-overview.md)。

## 使用方式

1. **控制台验证**：登录百炼控制台 → 进入 ParseX 模块 → 选择 Parse 或 Extract 标签页 → 上传样本文件并配置参数 → 查看结构化输出与原文对齐效果。  
2. **API 集成**：调用 `/v1/parse` 或 `/v1/extract` 接口，按文档要求组织 JSON 请求体；推荐使用 SDK（Python/Java）自动处理鉴权与重试。  
3. **配置复用**：在控制台保存验证通过的 Extract Schema 或 Parse 处理策略为命名配置，后续 API 调用中通过 `config_id` 引用，避免重复传参。此机制已在 [产品概览](../../raw/application-user-guide/getting-started-overview.md) 的“标准工作流”中明确说明。

## 限制和注意事项

- 单次请求最大文件体积为 100 MB；PDF 页面数上限为 500 页（超出部分将被静默跳过）。  
- Extract 的字段 Schema 中，`type` 仅支持 `string`、`number`、`date`、`boolean` 及其数组形式；不支持嵌套对象定义。  
- > **注意**：原始文档中提及“视频/音频支持时长 ≤ 30 分钟”，但最新 API 文档（`raw/api-reference/v1/extract.md`）已更新为 60 分钟。请以实际接口返回的 `400` 错误提示及 `X-RateLimit-Remaining` 响应头为准，旧版控制台界面尚未同步该变更。  
- 解析结果中的表格可能因原始排版复杂而出现合并单元格识别偏差，建议在控制台开启 `table_debug: true` 选项查看中间结构。  
- 所有调用均受项目级 QPS 与日配额限制，详情请查阅配额管理页面；超出后返回 `429 Too Many Requests`。

## 来源文档

- [产品概览](../../raw/application-user-guide/getting-started-overview.md)


