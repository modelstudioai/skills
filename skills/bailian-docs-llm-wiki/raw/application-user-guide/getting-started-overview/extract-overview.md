# 字段抽取概览

使用 ParseX Extract 从图文文档中抽取符合字段结构的业务数据，并复用已有解析结果。

字段抽取面向合同、票据、报告、表格等图文资料，按照你定义的字段结构抽取业务数据。它不仅返回可供业务系统使用的数据，还提供逐字段状态，帮助你识别缺失、推断和冲突项。

## Extract适合解决什么问题

-   从合同中提取合同编号、签约方、金额和日期。
-   从票据或表格中提取抬头、明细项与汇总字段。
-   将报告中的关键指标转换为固定的 JSON 结构。
-   为审核、归档或业务自动化生成带字段状态的结构化结果。

例如，报告分析 Agent 需要“报告期间、营业收入、预算承诺占用率”。你定义这几个字段后，ParseX 按相同结构整理结果，Agent 再使用这些数据完成报告分析。

## 开始使用

-   [在控制台中使用](raw/application-user-guide/getting-started-overview/extract-overview/playground-extract.md)：上传样例、编辑字段、运行抽取并检查结果。
-   [配置字段抽取](raw/application-user-guide/getting-started-overview/extract-overview/extract-configuration.md)：了解 Schema 以及抽取配置。
-   [获取抽取结果](raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)：获取并查看字段抽取的结果。
