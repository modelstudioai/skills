# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理等核心功能，以及配套的售后响应机制与服务边界说明。支持方式包括文档指引、控制台操作、API 参数配置及工单系统。所有能力均需遵循[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)约束。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请开通 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略打分后取 topN 结果融合生成；适用于问答、对话、摘要、客服等场景 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **结构化数据导入**：支持 Excel/CSV 等表格数据解析，但空行会导致后续数据被截断（首行为空则视为无效文件） [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持 `stream=True` 启用基础流式响应；如需增量式（即每次仅返回新 token，非全量重传），须显式设置 `incremental_output=True`。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回），默认 `False` |
| `incremental_output` | bool | 启用增量式流式输出（仅返回新增内容），需与 `stream=True` 同时使用 |
| `MD5` | string | 文件上传必填，用于校验文件完整性 [原文标题](../../raw/application-user-guide/application-support/application-faq.md) |
| `authorization` | string | 自定义插件调用时唯一支持透传的 Header 字段；其他自定义 Header（如 `X-User-ID`）将被忽略 [原文标题](../../raw/application-user-guide/application-support/application-faq.md) |

> **注意**：文档 1 中第 10 条明确“不支持自定义 header，仅支持 authorization”，但未说明是否支持 `Content-Type` 或 `Accept` 等标准 Header。实践中建议仅依赖 `authorization` 传递认证信息，业务上下文应通过请求体或 query 参数传递。

## 使用方式

- **插件调用**：通过 Assistant API 或 Agent 框架注册插件 schema，模型自动理解参数并调度执行；自定义插件需符合 OpenAPI 3.0 协议规范 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 调试**：测试中若结果不准确，可点击回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：PDF 文件后缀必须为小写 `pdf`，否则触发错误码 `140010`；单业务空间上限 10 万文档，超限时需提交工单申请扩容。  
- **合规备案**：上架应用市场或小程序前，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并单独申请通义千问合作协议。

## 限制和注意事项

- **插件透传限制**：仅 `Authorization` Header 可透传至自定义插件服务端，其余 Header 均被剥离。  
- **第三方工具支持边界**：阿里云百炼售后**不提供**第三方工具（如 Cursor、Windsurf、开源代理框架）的安装、配置、调试或故障诊断服务；仅提供阿里云侧接口可用性、调用示例、计费核查等方向性建议 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **数据容量硬限**：单业务空间最多容纳 10 万个文档；结构化数据导入时，空行将导致后续行被跳过，需预处理清洗。  
- **服务协议约束**：所有使用行为须遵守[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)及[体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)，开源模型使用还需符合对应[开源模型协议条款](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


