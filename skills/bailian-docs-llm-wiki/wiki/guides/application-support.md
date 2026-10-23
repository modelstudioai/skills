# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖模型调用、插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)等核心功能的使用指导与问题响应机制。支持范围明确区分平台原生能力（如 API 接口、控制台、SDK）与外部依赖（如第三方工具、用户本地环境），并提供基础工单、7×24 咨询及付费增值服务。具体细节请以最新版文档为准。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略打分后取 topN 结果；适用于问答系统、客服对话、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持 `stream=True`（全量流式）与 `incremental_output=True`（增量式流式），用于优化前端渲染体验。  
- **自定义插件**：支持通过标准协议注册函数或 API，大模型可理解参数结构并调用；但**不支持透传自定义 Header，仅允许 `Authorization` 字段** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的语义（如 SDK 类、抽象接口类或模型类型），且与当前百炼 SDK 实际设计（基于 `Client` 和 `ChatCompletion` 等统一接口）存在表述偏差，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中对 API 和 SDK 的支持描述为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回）；默认 `False` |
| `incremental_output` | bool | 启用增量式流式（仅返回新增内容，非全量重传）；需配合 `stream=True` 使用 |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- **问题反馈**：RAG 测试中若出现回复不准确，可通过模型回复下方的「问题反馈」按钮提交，或复制 `RequestId` 提交阿里云工单。  
- **服务接入支持**：  
  - 基础支持：7×24 电话（95187）、智能在线、标准工单，覆盖 API 调用、SDK 故障、控制台操作等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；  
  - 方向性建议：针对第三方工具接入百炼 API，可协助确认服务端可用性、提供 curl 示例、核查调用明细，但**不负责第三方工具本身的安装、配置或故障排查** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **合规与备案**：应用上架前需完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并申请通义千问合作协议。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被跳过 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限 10 万个文档；超限时需提交工单申请扩容。  
- **Header 限制**：自定义插件调用时，仅 `Authorization` 头可透传，其他 header（如 `X-User-ID`）会被丢弃。  
- **责任边界**：阿里云百炼仅保障自身服务端（API、计费、控制台）的稳定性与可用性；用户侧网络、代理、防火墙、第三方工具、业务代码等问题不在基础支持范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


