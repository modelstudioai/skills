# application [support](support.md)

阿里云百炼平台的 application [support](support.md) 覆盖从模型调用、插件集成、RAG 应用开发到售后响应的全链路支持能力，面向开发者提供可落地的技术保障与问题排查路径。核心支撑包括标准化 API 接口、预置及自定义插件能力、知识检索增强（RAG）工程化实践，以及分层售后服务体系。所有服务均需遵守相关法律协议与平台约束条件。

## 支持的模型/功能

- **插件能力**：官方提供六款开箱即用插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 应用**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分选取 topN 结果进行生成；适用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义函数/插件**：支持通过 OpenAPI 协议注册自定义 API 插件，大模型可理解其参数结构并参与推理调度；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True` 参数。

> **注意**：文档 2 中“Agent 和 Assistant API 的最大区别”描述（“Assistant API 可以提供各种类，方便调优”）表述模糊且未定义“类”的技术含义，缺乏接口契约或 SDK 示例佐证，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 与 SDK 故障诊断支持范围为准，避免依赖该模糊对比。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容，非全量重发） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **插件调用**：预置插件在应用中心直接启用；自定义插件需通过控制台注册 API Schema，并确保符合 OpenAPI 3.0 规范。  
- **RAG 调试**：测试时若出现回复不准确，优先点击模型回复下方的「问题反馈」按钮提交；也可复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入需避免空行（首行为空则整表被判定为空文件）。  
- **合规备案**：接入通义千问模型并上架应用市场/小程序前，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并提交工单申请合作协议。

## 限制和注意事项

- **第三方工具集成**：阿里云仅对百炼服务端状态、API 可用性、SDK 调用示例及计费明细提供支持；**不负责第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障诊断或本地环境（代理/防火墙/VPN）问题排查** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **文件容量与数量**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **协议约束**：所有使用行为须遵守 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)、[体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html) 及 [开源模型协议条款](https://help.aliyun.com/zh/model-studio/open-source-model-terms) [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **渲染与格式**：模型输出中的 `**text**` 为标准 Markdown 加粗语法，需前端自行解析渲染，平台不提供自动 HTML 转义或富文本渲染。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


