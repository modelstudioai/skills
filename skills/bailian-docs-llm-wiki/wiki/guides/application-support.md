# application [support](support.md)

阿里云百炼平台的 application [support](support.md) 覆盖应用开发、部署、调试及运维全生命周期的技术支撑，包括模型调用、插件集成、RAG 知识增强、API 使用规范及售后响应机制。其核心目标是保障开发者高效、合规、稳定地构建基于大模型的应用服务。所有支持行为均以《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》为法律基础，并受平台当前能力边界约束。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。
- **RAG（知识检索增强）**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分选取 topN 结果参与生成；已应用于问答系统、客户服务、教育、内容创作等场景（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。
- **自定义插件**：支持通过符合 OpenAPI 3.0 规范的 HTTP API 接入，模型可理解参数结构并完成[函数调用](../concepts/function-calling.md)；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。

> **注意**：文档2中“Agent和Assistant API的最大区别”条目表述模糊（“调整插件模型、基于上下文的理解，用户可以自己去开发”），未明确技术差异点，且与当前 v2.x SDK 中 Assistant API 实际能力（如内置工具调用、RAG 集成、流式控制）存在偏差，建议以最新 [SDK 文档](https://help.aliyun.com/zh/model-studio/developer-reference/assistant-api) 为准。

## 关键参数

- **[流式输出](../concepts/streaming-output.md)控制**：
  - `stream=True`：启用流式响应（逐 token 返回）；
  - `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增内容，非全量重发）。
- **文件上传校验**：必填 `MD5` 参数用于验证文件完整性；PDF 文件后缀必须为小写 `pdf`，否则触发错误码 `140010`（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。
- **RAG 检索行为**：默认并行检索各知识库，无显式串行顺序控制参数；topN 数量由系统根据置信度动态裁剪，不可手动指定。

## 使用方式

- **问题反馈与排查**：
  - RAG 测试中出现回复不准确时，可通过模型回复下方的「问题反馈」按钮提交，或复制 `RequestId` 提交工单；
  - 连通性问题建议优先使用 `curl` 等标准工具测试服务地址可达性（见 [售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)）。
- **前端渲染适配**：模型输出含 `**xxx**` 等 Markdown 格式标记时，需在客户端自行解析并渲染为加粗等样式。
- **备案与合作**：接入通义千问模型并上架应用市场/小程序前，须完成[应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并提交工单申请合作协议。

## 限制和注意事项

- **第三方工具支持边界**：阿里云百炼仅对自身服务端（API、SDK、控制台、计费系统）提供直接支持；对于 Cursor、Windsurf 等第三方 AI 工具的安装、配置、故障诊断等，仅提供方向性建议，**不承担运维责任**（见 [售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)）。
- **数据容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。
- **结构化数据导入陷阱**：表格中若存在空行（尤其首行为空），将导致后续数据被跳过，仅导入空行前的有效行（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。
- **协议约束**：所有使用行为须遵守《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》《[阿里云百炼体验功能特别说明](../../raw/application-user-guide/application-support/application-related-agreements.md)》及开源模型相关条款（见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)）。

> **注意**：文档2中“自定义插件服务目前暂时不收费”的表述未体现调用计费逻辑——实际按 API 调用量（[Token](../concepts/token.md) 数/请求次数）计费，与是否“自定义”无关；该描述易引发误解，应以控制台计费页及 [价格文档](https://help.aliyun.com/zh/model-studio/pricing) 为准。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


