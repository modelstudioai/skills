# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能正确性、服务稳定性与调试可追溯性。所有支持行为均以阿里云百炼服务协议及当前生效的官方文档为准。

## 支持的模型/功能

- **插件能力**：平台官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。其中部分插件需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合选取 topN 结果；广泛应用于问答系统、对话系统、客户服务等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 描述接入，大模型可理解参数结构并自主调用；但**不支持透传自定义 HTTP Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复渲染历史内容。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式（每次仅返回新增 token） | 否（需 `stream=True` 时生效） |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

> **注意**：文档 1 中第 8 条明确 `incremental_output=True` 为独立参数，但实际 SDK 实现中该参数常作为 `stream` 的子选项（如 `stream_options={"include_usage": false, "incremental": true}`）。请以最新版 [aliyun-openapi-python-sdk](https://pypi.org/project/aliyun-openapi-python-sdk/) 文档为准，避免直接硬编码布尔值。

## 使用方式

- **插件调用**：在 Assistant API 或 Agent 配置中声明插件 schema，由大模型自动选择并填充参数；自定义插件需确保 endpoint 可被百炼服务端直连（不支持内网/代理穿透）。  
- **RAG 测试优化**：若检索结果不准确，可通过控制台问题反馈按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行会导致结构化数据截断（首行为空则识别为空文件）。  
- **售后支持入口**：7×24 小时可通过官网、电话（95187）、阿里云 APP 或[标准工单系统](https://smartservice.console.aliyun.com/service/create-ticket)提交；深度定制需求（如业务代码指导）需联系商务经理评估 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何请求头透传；插件调用失败时不会自动重试，需应用层捕获异常并处理。  
- **数据规模**：单业务空间最多上传 10 万个文档；超限时须提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方集成边界**：阿里云仅对百炼服务端状态、API 可达性、SDK 调用示例及计费明细提供支持；第三方工具（如 Cursor、Windsurf）的安装、配置、本地环境（代理/防火墙/VPN）问题不在保障范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


