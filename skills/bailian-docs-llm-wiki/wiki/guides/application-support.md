# application support

阿里云百炼平台的 application support 覆盖应用构建、部署、调试及运维全生命周期的技术支撑能力，包括插件集成、RAG 知识增强、流式/增量输出等核心功能支持，以及配套的售后响应机制与服务边界说明。开发者可基于官方 API、SDK 和控制台快速集成智能体能力，同时需关注协议约束与平台限制。所有服务均以阿里云百炼平台自身能力为边界，第三方工具或用户侧环境问题不在标准支持范围内。

## 支持的模型/功能

- **插件能力**：当前官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索（按配置策略执行），再基于相关性得分聚合 topN 结果，广泛应用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重传） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过 OpenAPI 协议注册函数，模型可理解参数结构并调用；但**仅支持 `Authorization` header 透传，不支持其他自定义 header**（如 `X-Api-Key` 等）> **注意**：该限制与部分第三方工具文档暗示的“通用 header 透传”存在冲突，以本条为准 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE） | 否，默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式 token 输出（避免重复回传历史内容） | 否，默认 `False` |
| `md5` | string | 文件上传接口必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

> **注意**：`incremental_output=True` 仅在 `stream=True` 时生效；若单独设置 `incremental_output=True` 而未开启 `stream`，行为未定义，建议始终成对使用。

## 使用方式

- **插件调用**：通过 Assistant API 或 Agent SDK 注册函数描述（function calling schema），模型将自动解析参数并生成符合协议的调用请求。  
- **RAG 应用测试**：在控制台测试窗中验证检索效果；若结果不准确，可通过回复下方「问题反馈」按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；上传前需计算文件 MD5 并作为请求参数传入；空行会导致结构化数据截断（如首行为空则识别为空文件） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **合规备案**：接入通义千问模型并上架应用市场/小程序时，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并提交工单申请合作协议 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **服务边界**：标准售后服务覆盖模型服务、API/SDK、控制台、账号及计费问题；**不包含**第三方工具（如 Cursor、Windsurf 等）的安装配置、业务代码编写、本地网络/代理/防火墙问题排查，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **文件容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **协议约束**：使用前须阅读并接受《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》及开源模型相关条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **Markdown 渲染**：模型输出中的 `**text**` 等 Markdown 语法需由前端自行解析渲染，平台不提供富文本转换能力 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


