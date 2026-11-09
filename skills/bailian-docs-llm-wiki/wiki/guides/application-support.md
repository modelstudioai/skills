# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理，以及售后响应机制等核心环节。该支持体系面向生产环境需求设计，强调可配置性、可观测性和问题闭环能力。开发者需结合具体场景合理选用功能，并注意协议约束与服务边界。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合选取 topN 结果，广泛应用于问答系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **结构化数据导入**：支持 Excel/CSV 等格式结构化数据批量导入，但存在空行截断逻辑（首行为空则视为无效文件）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 描述让大模型理解参数并调用，但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称 “Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但未明确说明 Assistant API 是否原生支持插件调用；而当前平台实际以 Agent 模式统一承载插件编排与执行。建议以控制台插件配置页及 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中插件启用流程为准，Assistant API 主要用于轻量对话封装。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)（逐 token 返回）。  
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（仅返回本次新增内容，非全量重发）。  
- 文件上传必填 `MD5`：用于校验文件完整性，上传 PDF 时后缀必须为小写 `pdf`。  
- RAG 检索结果数：由知识库配置中的 `top_k` 控制，服务端默认并行检索后合并排序。

## 使用方式

- **插件调用**：在应用编辑页启用对应插件，配置参数 schema（JSON Schema 格式），无需修改前端渲染逻辑；自定义插件需确保 endpoint 可被百炼服务端直连且响应符合 OpenAPI 规范。  
- **RAG 调试**：测试中若结果不准，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后支持接入**：7×24 小时可通过官网、电话（95187）、阿里云 APP 或标准工单获取基础服务；深度支持（如定制集成方案）需联系商务经理订购增值服务 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **合规备案**：上架应用市场或小程序前，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并申请通义千问合作协议。

## 限制和注意事项

- **文件限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **插件 Header 限制**：自定义插件调用时，仅 `Authorization` 头可透传，其他 header（如 `X-User-ID`）将被丢弃。  
- **第三方工具责任边界**：阿里云不负责 Cursor、Windsurf 等第三方工具的安装、配置、故障排查或本地网络（代理/防火墙/VPN）问题 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须审阅《阿里云百炼服务协议》《体验功能特别说明》及开源模型条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **计费提示**：自定义插件本身免费，但涉及 prompt 优化、应用调用及测试窗测试等操作将产生费用 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


