# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如 Agent、RAG 应用、插件集成等）过程中提供的技术能力支撑、服务边界说明及使用约束。它涵盖模型/插件调用、流式与增量输出、知识库检索机制、API 参数控制，以及售后支持范围等核心维度。开发者需结合功能文档与协议条款，在平台能力边界内进行集成与问题排查。

## 支持的模型/功能

- **Agent 能力**：支持通过插件扩展智能体行为，官方提供六款内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后取 topN 结果融合生成；适用于问答系统、客服、教育、内容创作等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持开发者注册 HTTP API 插件，模型可理解其参数定义并自主调用；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义该 API 的当前形态、接口规范或是否仍为独立 SDK；而平台当前主推的是 `assistant` 类型应用与 `messages` 接口。该描述可能已过时，建议以 [API 文档中心](https://help.aliyun.com/zh/model-studio/developer-reference) 最新 `v1/assistants` 和 `v1/messages` 接口为准。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)（逐 token 返回）。
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（每次返回新增内容，非全量重发），适用于前端实时渲染场景。
- 文件上传必填 `MD5`：用于校验文件完整性，PDF 文件后缀必须为小写 `pdf`，否则触发错误码 `140010`。
- 知识库检索无显式参数控制并行/串行，实际为**并行检索 + 得分聚合**，由平台自动调度。

## 使用方式

- 插件调用：在创建 Assistant 或配置 Function Calling 时声明插件 schema，模型将基于自然语言指令自动选择并填充参数。
- RAG 应用调试：若检索结果不准确，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- 增量渲染：模型输出含 `**text**` 等 Markdown 格式时，需前端自行解析渲染，平台不提供富文本转换服务。
- 备案与合作：接入通义千问模型上架应用市场或小程序，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)并提交工单申请合作协议。

## 限制和注意事项

- **第三方工具支持边界明确**：阿里云百炼售后仅覆盖自身服务端（API 可用性、SDK 调用、计费明细、控制台问题）；对 Cursor、Windsurf 等第三方 AI 工具的安装、配置、本地环境（代理/防火墙/VPN）、业务代码实现等问题**不提供支持**，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **数据规模限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。
- **结构化数据导入容错弱**：表格中存在空行会导致后续数据被跳过（尤其首行为空时视为无效文件）。
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》，开源模型还需遵循对应 [开源模型协议条款](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


