# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖模型调用、插件集成、RAG 检索、[流式输出](../concepts/streaming-output.md)等核心功能的使用指导与问题响应机制。支持范围包括 API 行为规范、参数配置说明、常见错误排查路径，以及明确的服务边界（如不覆盖第三方工具运维）。所有支持均以平台当前稳定版功能为准，具体以控制台实际能力及 [原文标题](../../raw/application-user-guide/application-support/application-faq.md) 中的技术描述为准。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通。自定义插件支持通过协议声明函数签名，由大模型解析参数并调用 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）聚合 topN 结果后生成回复；已应用于问答系统、客户服务、教育等场景 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复返回历史 token。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回），默认 `False` |
| `incremental_output` | bool | 启用增量式流式（仅返回新增 token），需与 `stream=True` 共同使用 |
| `authorization` | string | 唯一支持透传的 HTTP Header 字段；**不支持其他自定义 header** [原文标题](../../raw/application-user-guide/application-support/application-faq.md) |
| `MD5` | string | 文件上传必填，用于校验文件完整性 |

> **注意**：文档 1 中第 10 条明确“不支持自定义 header，仅支持 authorization”，但未说明是否支持 `x-api-key` 等阿里云通用鉴权头。实践中应以控制台 API 文档或 SDK 实现为准，该限制优先级高于通用云服务惯例。

## 使用方式

- **问题反馈**：RAG 应用测试中若出现回复不准确，可通过模型回复下方的「问题反馈」按钮提交，或复制 `RequestId` 提交工单 [原文标题](../../raw/application-user-guide/application-support/application-faq.md)。
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时需确保无空行，否则后续行将被跳过。
- **售后接入**：7×24 小时支持渠道包括官网智能在线、电话（95187 / 400）、标准工单；基础服务覆盖 API 故障诊断、SDK 使用、控制台操作及计费咨询 [原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件调用限制**：自定义插件不支持透传除 `Authorization` 外的任何 HTTP Header；插件调用产生的 prompt 优化、API 调用及测试窗测试行为将计费。
- **服务边界明确**：阿里云百炼**不提供**以下支持：
  - 第三方工具（如 Cursor、Windsurf）的安装、配置、升级或故障排查；
  - 用户本地环境（代理、防火墙、内网策略）导致的连通性问题；
  - 业务代码编写、调试或定制化集成方案（需联系商务经理订购增值服务）[原文标题](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **法律协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需遵循对应 [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


