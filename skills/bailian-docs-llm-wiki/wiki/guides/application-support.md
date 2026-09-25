# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境，强调可配置性、可观测性和边界清晰性。开发者需明确平台能力边界与第三方依赖责任划分，以保障集成稳定性。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合选取 topN 结果，广泛应用于问答系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复渲染历史内容。  
- **自定义插件**：支持通过标准协议注册函数/API，大模型可理解参数结构并调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类型、抽象接口或配置模板），且其他文档未佐证该表述；建议以实际 SDK 文档和 OpenAPI 规范为准，避免依赖模糊术语。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅当 `stream=True` 时生效） | 否（默认 `False`） |
| `MD5` | string | 文件上传时用于校验完整性的哈希值，必填于结构化数据导入接口 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- **插件调用**：通过 Assistant API 或 Agent 框架注册插件描述（OpenAPI Schema 格式），由大模型自主决策调用时机与参数填充；自定义插件需确保 endpoint 可被百炼服务端直连（不支持内网穿透或私有代理）。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索权重、分块策略与重排序规则；测试时若结果不准，应优先检查知识库切片质量与 query embedding 匹配度，而非直接提交工单。  
- **流式响应解析**：前端需按 SSE 协议解析 `data:` 字段，并对 `\*\*text\*\*` 等 Markdown 片段做安全渲染（参见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 7 条）。  
- **错误排查**：遇到 `140010` 错误（文件格式不支持）时，确认 PDF 后缀为小写 `pdf`；空行导致结构化数据截断问题，需预处理清洗 Excel/CSV 源文件。

## 限制和注意事项

- **插件 Header 限制**：仅支持 `Authorization` 请求头透传，其他自定义 Header（如 `X-User-ID`、`X-Tenant`）将被丢弃，不可用于身份上下文传递。  
- **知识库容量上限**：单业务空间最多上传 10 万个文档；超限时须通过阿里云工单申请扩容，无自助扩容入口。  
- **售后支持边界**：  
  - ✅ 覆盖：API 故障诊断、SDK 使用问题、控制台操作咨询、计费明细核查；  
  - ❌ 不覆盖：第三方工具（如 Cursor、Windsurf）部署与调试、用户本地网络/防火墙/代理问题、业务逻辑代码编写、非百炼侧服务（如 GitHub API 限流）的协同排障 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》及《阿里云百炼体验功能特别说明》，开源模型调用还需符合对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


