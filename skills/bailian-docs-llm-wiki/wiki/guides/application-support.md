# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境设计，强调可配置性、可观测性和边界清晰的服务范围。所有功能均需结合具体 API 版本与控制台配置生效，建议以最新版 SDK 和控制台为准。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合 TopN 结果，广泛应用于问答系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重发）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议注册函数/API，大模型可理解参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”描述模糊且未定义术语（如“调整插件模型”“提供各种类”），缺乏可验证的技术接口对比，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 支持范围为准，避免依赖该条表述进行架构决策。

## 关键参数

| 参数名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否，默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量输出模式（仅返回新增 tokens） | 否，默认 `False` |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

## 使用方式

- **插件调用**：在应用配置中启用对应插件，自定义插件需按 OpenAPI Schema 注册；调用时由模型自动选择并填充参数，无需显式触发。  
- **RAG 配置**：在知识库设置中指定检索权重、分块策略与重排序规则；测试阶段若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式集成**：前端需解析 SSE 响应，并对含 `**text**` 的 Markdown 片段做渲染处理（如加粗）；后端应确保 HTTP 连接保持活跃，避免超时中断 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后支持入口**：7×24 小时支持通过官网、电话（95187）、阿里云 APP 或标准工单获取；涉及第三方工具（如 Cursor、Windsurf）的问题，仅提供方向性建议，不承担部署与调试责任 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限 10 万文档；超限时需提交工单申请扩容。  
- **Header 限制**：自定义插件调用时，仅 `Authorization` 头可透传至目标服务，其他 header（如 `X-User-ID`、`X-Tenant`）会被丢弃。  
- **第三方集成边界**：阿里云不支持对非百炼平台组件（如开源代理框架、AI 编程工具）的安装、配置、故障诊断或业务代码编写指导；所有本地网络环境（代理/防火墙/VPN）问题需用户自行排查 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须审阅 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) 及 [阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)，后者适用于免费试用功能。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


