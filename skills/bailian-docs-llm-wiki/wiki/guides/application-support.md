# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖[插件](../concepts/plugin.md)集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能可验证、行为可预期、问题可追溯。所有支持能力均以平台当前正式发布版本为准，历史文档中未同步更新的描述需以控制台实际配置项和 API 文档为准。

## 支持的模型/功能

- **[插件](../concepts/plugin.md)能力**：官方提供六类内置[插件](../concepts/plugin.md)：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按用户配置的排序策略（如语义相似度）选取 topN 结果后融合生成；适用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范注册的 HTTP API 插件，模型可解析其参数定义并自主调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中“Agent 和 Assistant API 的最大区别”条目表述模糊且缺乏技术细节（如未说明协议差异、调用方式或生命周期管理），与当前控制台中统一的 `Assistant API v2` 接口设计不符，该条目已过时，应以 [API 文档中心](https://help.aliyun.com/zh/model-studio/developer-reference/assistant-api-overview) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `stream` | boolean | 否 | 设为 `true` 启用流式响应（SSE）。默认 `false`。 |
| `incremental_output` | boolean | 否 | 仅当 `stream=true` 时有效；设为 `true` 表示增量输出（每 chunk 仅含新增内容）。默认 `false`（全量重传）。 |
| `retrieval_config` | object | 否 | RAG 检索配置，含 `top_k`、`score_threshold` 等字段，控制知识库召回行为。 |
| `plugins` | array | 否 | 指定启用的插件 ID 列表，如 `["python_interpreter", "qwen_search"]`。 |

## 使用方式

- **调试与反馈**：RAG 应用测试中若出现回复不准确，应点击模型回复下方的「问题反馈」按钮提交类型，并**复制 RequestId** 一并提交阿里云工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：PDF 文件后缀必须为小写 `pdf`；结构化数据导入时需确保无空行（首行为空将被识别为无效文件）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后接入**：7×24 小时支持渠道包括官网智能在线、电话（95187）、阿里云 APP 及标准工单；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题及计费咨询 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **第三方集成**：阿里云仅对百炼服务端状态、API 可达性、官方 SDK 示例及调用明细提供支持；**不负责第三方工具（如 Cursor、Windsurf）的部署、配置或故障排查** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件调用限制**：自定义插件仅支持 `Authorization` Header 透传，其他 Header（如 `X-Custom-Id`）将被丢弃。  
- **知识库容量**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **MD5 校验**：上传接口必填 `MD5` 参数，用于校验文件完整性，不可省略或伪造。  
- **责任边界**：阿里云不对外部第三方工具的陈述、行为或故障承担责任；所有非百炼服务端直接引发的问题（如本地代理、防火墙、操作系统兼容性、业务代码逻辑错误），均不在基础售后范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须审阅《阿里云百炼服务协议》及《体验功能特别说明》，相关条款具有法律效力 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


