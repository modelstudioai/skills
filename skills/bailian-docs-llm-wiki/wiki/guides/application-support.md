# application [support](support.md)

百炼平台的应用支持体系面向开发者提供从功能能力、参数配置到售后保障的全链路支撑。核心涵盖插件与RAG等增强能力的使用规范、关键API参数说明、流式/增量输出等工程实践方式，以及明确的服务边界与限制条件。所有能力均需在百炼服务协议与合规框架下使用。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果，广泛应用于问答系统、客户服务、教育及内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议接入，大模型可理解参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
> **注意**：文档1中“Agent和Assistant API的最大区别”描述模糊且未定义术语（如“调整插件模型”“提供各种类”），缺乏技术细节，建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中明确的API与SDK支持范围为准，避免依赖该条表述进行架构设计。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming.md)（逐token返回）。  
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming.md)（仅返回本次新增内容，非全量重发）。  
- 文件上传接口必填 `MD5` 参数：用于校验文件完整性，防止传输损坏。  
- 知识库检索配置中 `topN`、权重策略等参数影响RAG结果排序与召回质量。

## 使用方式

- 插件调用：通过 Assistant API 或 Agent 框架声明工具集，由大模型自主规划调用路径；自定义插件需符合 OpenAPI 3.0 协议规范。  
- RAG 应用调试：若回复不准确，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 前端渲染：模型输出含 `**text**` 等 Markdown 语法时，需自行解析并渲染为对应样式（如加粗），百炼不提供自动HTML转换。  
- 备案与合作：上架应用市场或小程序前，须完成[应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并提交工单申请通义千问合作协议。

## 限制和注意事项

- **文件限制**：上传仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；单业务空间上限 10 万文档，超限需提交工单申请扩容。  
- **结构化数据导入**：表格中存在空行将导致后续数据被截断（空行后全部丢弃），首行为空则判定为空文件。  
- **第三方集成边界**：阿里云百炼仅保障自身服务端可用性、API 接口行为与计费准确性；对第三方工具（如 Cursor、Windsurf 等）的部署、配置、故障排查不提供支持 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)及[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html) [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
> **注意**：文档2中引用的《阿里云百炼体验功能特别说明》协议链接域名（`alicdn.com`）与阿里云主站（`aliyun.com`）不一致，且协议编号年份为“2026”，明显为占位或过期版本，实际使用请以控制台或官网最新公布的协议文本为准。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


