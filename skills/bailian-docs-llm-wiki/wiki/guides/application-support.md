# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 知识增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境需求设计，强调可配置性、可观测性和问题闭环能力。开发者需结合自身业务场景，在平台能力边界内进行合理集成。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识检索增强（RAG）**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成；已应用于问答系统、客户服务、教育训练等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新增 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 协议注册的函数插件，模型可理解参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称 “Agent 和 Assistant API 的最大区别是调整插件模型、基于上下文的理解，用户可以自己去开发”，该描述模糊且未定义“调整插件模型”的具体含义；而当前百炼控制台与 SDK 文档中无对应功能入口或参数说明。建议以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中明确列出的插件调用方式为准，避免依赖此条表述。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否，默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式 token 输出（避免重复回传历史内容） | 否，默认 `False` |
| `md5` | string | 文件上传时必填，用于校验文件完整性 | 是（见数据管理章节） |
| `Authorization` | string | 自定义插件调用时唯一支持透传的 Header 字段 | 是（若需鉴权） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用对应插件，或通过 Assistant API 的 `tools` 字段声明函数 schema；模型将自动规划调用时机与参数。  
- **RAG 集成**：在应用配置中绑定知识库，设置检索粒度（chunk size）、重排序策略及召回数量；测试时可通过问题反馈按钮提交 `RequestId` 进行精准问题定位 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；上传接口必须携带 `MD5` 校验值，否则返回错误码 `140010` [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后支持接入**：7×24 小时可通过官网、电话（95187）、阿里云 APP 或标准工单提交问题；基础服务覆盖 API 故障诊断、SDK 使用、控制台操作及计费核查 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何 Header 透传；插件调用失败时，模型可能返回空结果或 fallback 响应，需在客户端做容错处理。  
- **文件与数据限制**：单业务空间最多上传 10 万个文档；结构化数据导入时，**空行将导致后续所有行被跳过**（包括首行为空行时整表识别为空）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具免责**：阿里云仅对百炼服务端（API、计费、控制台）提供直接支持；对接 Cursor、Windsurf 等第三方工具时，安装、配置、本地网络/代理/防火墙问题、业务代码逻辑等均不在服务范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型调用还需符合对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


