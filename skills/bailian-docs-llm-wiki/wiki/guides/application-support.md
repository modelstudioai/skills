# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境需求设计，强调可配置性、可观测性和边界清晰的服务范围。所有功能均需结合具体 API 版本与控制台配置生效，部分能力需申请开通。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需[申请通过后方可使用](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按用户配置的排序策略（如得分）选取 topN 结果，适用于问答系统、客户服务、教育培训等场景（详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第5条）。  
- **自定义插件**：支持通过协议注册外部 API，大模型可理解其参数结构并生成调用请求；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。  
- **[流式输出](../concepts/streaming-output.md)**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复返回历史内容。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `stream` | bool | 启用流式响应（逐 token 返回） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第8条 |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增 token） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第8条 |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条（数据管理章节） |

> **注意**：文档中未明确 `incremental_output` 与 `stream=True` 的依赖关系。实际调用时需同时设置 `stream=True` 才能启用 `incremental_output`，否则参数无效——该行为与 OpenAI 兼容 API 设计惯例一致，但[常见问题](../../raw/application-user-guide/application-support/application-faq.md)未作说明，建议以 SDK 示例为准。

## 使用方式

- **插件调用**：在应用配置中启用对应插件，自定义插件需按 OpenAPI Schema 格式声明函数签名，由模型自动解析参数并构造请求。  
- **RAG 配置**：在知识库设置中指定检索权重、分块策略与重排模型，检索过程为并行执行（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第9条）。  
- **错误反馈**：RAG 输出不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单。  
- **合规备案**：若应用需上架至应用市场或小程序平台，须按 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 流程完成备案，并单独申请合作协议。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第1、4条）。  
- **知识库容量**：单业务空间上限为 10 万个文档，超限时需提交工单申请扩容。  
- **第三方工具支持边界**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障排查或业务代码实现（详见 [售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第4条）。  
- **协议约束**：服务使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需符合对应 [开源模型协议条款](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


