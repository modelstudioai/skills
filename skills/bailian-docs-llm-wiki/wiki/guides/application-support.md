# application [support](support.md)

application [support](support.md) 是阿里云百炼平台面向开发者提供的应用层能力支撑体系，涵盖插件集成、RAG增强、流式/增量输出、自定义[函数调用](../concepts/function-calling.md)等核心功能，并配套明确的售后支持边界与使用约束。该支持体系以 API 可编程性为基础，强调模型与业务逻辑的协同，同时严格区分平台责任与用户侧运维边界。相关法律协议与合规要求需同步遵循 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通。  
- **RAG（知识检索增强）**：支持多知识库并行检索（按用户配置策略执行），再基于得分选取 topN 结果参与生成；已应用于问答系统、对话系统、客户服务、教育与内容创作等场景。  
- **自定义函数/插件**：支持通过 Assistant API 注册并调用，模型可理解参数结构并返回完整结果；但**仅支持 `Authorization` header 透传，不支持其他自定义 header**（详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。  
- **格式与输出控制**：支持 Markdown 渲染（如 `**text**` → 加粗），需前端自行解析；支持流式（`stream=True`）及增量式[流式输出](../concepts/streaming-output.md)（`incremental_output=True`）。

> **注意**：文档2中第4条称“Assistant API 可提供各种类，方便调优”，但未说明具体类名或 SDK 接口形态；而当前百炼 Python SDK 中实际暴露的是 `AssistantClient` 及 `create_assistant` 等方法，无泛化“类库”概念。该描述易引发歧义，建议以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中代码示例为准，避免依赖模糊术语。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容，非全量重传） |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条） |
| `Authorization` | string | 唯一支持透传的 HTTP header，用于身份鉴权 |

## 使用方式

- **插件调用**：通过 Assistant API 的 `tools` 字段声明插件能力，模型自动规划并调用；自定义插件需符合 OpenAPI 3.0 规范并完成注册。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索权重、topK、重排序策略；测试时若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单。  
- **文件上传**：仅支持小写后缀的 `pdf`/`doc`/`docx`；空行将导致后续结构化数据被截断（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第4条）。  
- **备案与合作**：接入通义千问模型上架应用市场或小程序，须按 [应用合规备案](raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 操作，并通过工单申请合作协议。

## 限制和注意事项

- **服务边界**：阿里云百炼售后仅覆盖平台自身功能（API、控制台、SDK、计费系统等），**不承担第三方工具（如 Cursor、Windsurf、开源代理框架）的安装、配置、故障诊断或优化责任**（详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第4条）。  
- **容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **协议约束**：所有应用必须遵守 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 及 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)，尤其涉及模型输出内容合规性与数据主权。  
- **调试支持**：平台提供标准工单、7×24 智能在线与电话支持（95187），但**不提供业务代码编写指导、定制化集成方案或本地网络环境（如代理、防火墙）问题排查**（见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第4-(2)-(iv)(v) 条）。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


