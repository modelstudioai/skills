# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运维 AI 应用过程中提供的技术能力支撑与服务保障，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming.md)控制、API 调用规范及售后响应机制等核心环节。其目标是确保应用功能可扩展、调用可调试、问题可追溯、服务可保障。所有能力均需结合具体模型与配置生效，部分高级功能需申请开通或依赖付费服务。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需[申请通过后方可使用](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置执行），再基于相关性得分选取 topN 结果；广泛应用于问答系统、对话系统、客户服务等场景，详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中第5条。  
- **流式与增量输出**：支持 `stream=True` 启用流式响应；若需逐 token 增量返回（而非全量重发），必须额外设置 `incremental_output=True`（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第8条）。  
- **自定义插件**：支持通过协议注册函数/API，大模型可理解参数结构并调用；但**仅支持透传 `Authorization` header**，其他自定义 header 将被忽略（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。

> **注意**：文档1中第4条称“Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类、抽象接口类或模型类型），且该表述与其他文档无交叉印证，建议以实际 SDK 文档和 OpenAPI 规范为准，避免依赖此模糊描述。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `stream` | bool | 否 | 设为 `True` 启用[流式输出](../concepts/streaming.md)（默认 `False`） |
| `incremental_output` | bool | 否 | 仅当 `stream=True` 时有效；设为 `True` 表示增量式[流式输出](../concepts/streaming.md)（即每次返回新 token，不重复历史内容） |
| `MD5` | string | 是（文件上传） | 用于校验上传文件完整性，见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第3条 |

## 使用方式

- 插件调用：通过 `tools` 字段声明插件列表，由模型自主决定是否调用及传参；自定义插件需符合 OpenAPI Schema v3 协议。  
- RAG 配置：在应用编辑页绑定知识库，设置检索权重、topK、分块策略等；检索为并行执行，非串行（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第9条）。  
- 错误排查：  
  - 文件上传失败（如错误码 `140010`）：确认 PDF 后缀为小写 `pdf`；  
  - RAG 回复不准：点击回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单；  
  - 自定义插件 header 未生效：确认仅使用 `Authorization`，其余 header 不被透传。  
- 售后接入：7×24 小时支持通过官网、电话（95187）、阿里云 APP 及标准工单获取；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题等，详见 [售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件限制**：自定义插件当前免费，但 [prompt](prompt.md) 优化、应用调用测试等环节将产生计费（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第2条）；不支持除 `Authorization` 外的任何自定义请求头。  
- **数据管理限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容；结构化数据导入时，空行将导致后续行被截断（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第2、4条）。  
- **第三方集成边界**：阿里云仅保障百炼服务端可用性与 API 正确性；对第三方工具（如 Cursor、Windsurf 等）的安装、配置、本地环境（代理/防火墙/VPN）、业务代码实现等问题**不提供支持**，详见 [售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第4条。  
- **协议约束**：使用前须遵守《阿里云百炼服务协议》及《体验功能特别说明》，相关条款详见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


