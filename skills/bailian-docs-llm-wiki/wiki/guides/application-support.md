# application [support](support.md)

阿里云百炼平台的应用支持体系面向开发者提供覆盖模型调用、插件集成、RAG 应用开发及售后响应的全链路支撑。核心聚焦于服务可用性保障、API/SDK 问题诊断、控制台使用指导及合规协议遵循，不覆盖第三方工具运维或用户侧环境问题。所有支持边界与责任划分以官方文档为准。

## 支持的模型/功能

- **插件能力**：当前官方提供六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过 Assistant API 或 Agent 框架接入，模型可理解插件参数并按协议调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后取 topN；适用于问答、客服、教育等场景，但检索结果准确性依赖数据质量与 [prompt](prompt.md) 设计 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True` 参数。

> **注意**：文档 3 中“Agent 和 Assistant API 的最大区别”描述模糊（“调整插件模型、基于上下文的理解……方便调优”），未明确技术差异；实际应以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的服务边界为准——即两类 API 均属百炼平台原生能力，其使用咨询、故障诊断均在基础售后范围内，不因类型不同而改变支持等级。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容，非全量重发） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **技术支持渠道**：7×24 小时电话（95187 / 400）、智能在线、标准工单；覆盖模型功能咨询、API/SDK 故障诊断、控制台问题、账号与计费咨询 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **问题提报**：RAG 测试中模型回复不准确时，可点击反馈按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方对接建议**：仅提供方向性支持，如确认百炼 API 可用性、提供官方 SDK 示例、协助核查调用明细；**不负责第三方工具（如 Cursor、Windsurf）的安装、配置或故障排查** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **第三方工具免责**：阿里云不承担任何外部工具（含 AI 编程工具、开源代理框架等）的运行维护责任；其安装、升级、兼容性及本地环境（代理/防火墙/VPN/OS）问题不在支持范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **文件上传限制**：PDF 文件后缀必须为小写 `pdf`；单业务空间最多上传 10 万个文档，超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **协议约束**：使用前须遵守《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》《[阿里云百炼体验功能特别说明](../../raw/application-user-guide/application-support/application-related-agreements.md)》及开源模型相关条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **备案要求**：若产品接入通义千问并上架应用市场/小程序，须完成 [应用合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 并申请合作协议。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)


