# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能可预期、调用行为可追溯、问题定位可闭环。所有支持能力均以平台当前正式发布的 API 行为与控制台配置为准。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合 TopN 结果，广泛应用于问答系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议注册函数/API，大模型可理解参数结构并自主编排调用；但**不支持透传自定义 HTTP Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称 “Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该描述未明确对应百炼当前公开的 API 分类（如 `/v1/chat/completions` vs `/v1/agents/run`）。实际能力边界请以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的服务支持范围为准，避免将实验性或内部接口误作稳定能力使用。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | boolean | 启用流式响应（SSE 格式） | 否（默认 `false`） |
| `incremental_output` | boolean | 在 `stream=true` 下启用增量式 token 输出（避免重复回传历史内容） | 否（默认 `false`） |
| `md5`（文件上传） | string | 用于校验上传文件完整性，必填于结构化数据导入接口 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- **插件调用**：在应用配置中启用对应插件，自定义插件需按 OpenAPI Schema 格式注册元信息；调用时由大模型自动选择并填充参数，无需客户端显式构造请求体。  
- **RAG 配置**：在知识库设置中指定检索权重、分块策略与重排序规则；测试阶段若结果不准，可通过界面“问题反馈”按钮提交或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式集成**：前端需处理 SSE 响应，解析 `data:` 字段；启用 `incremental_output=True` 后，每个 chunk 仅含本次新增内容，适用于实时 UI 渲染。  
- **文件上传**：PDF 文件后缀必须为小写 `pdf`，否则触发错误码 `140010`；结构化数据（如 Excel）禁止空行，首行为空将被识别为无效文件 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **插件 header 限制**：自定义插件调用时，服务端**仅透传 `Authorization` 头**，其他自定义 header（如 `X-User-ID`、`X-Tenant`）会被丢弃，不可用于身份或上下文透传。  
- **知识库容量上限**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具支持边界**：阿里云售后仅覆盖百炼服务端本身（API 可用性、计费一致性、SDK 调用逻辑），**不支持第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障排查或本地环境（代理/防火墙/内网）问题** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议与合规**：应用上线前须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并签署《阿里云百炼服务协议》等法律文件 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


