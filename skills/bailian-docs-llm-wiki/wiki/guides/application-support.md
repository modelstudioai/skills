# application [support](support.md)

application [support](support.md) 指阿里云百炼平台为开发者在构建、调试和运维 AI 应用（含 Agent、RAG、自定义插件等）过程中提供的技术支撑体系，涵盖功能能力边界、关键配置参数、调用方式规范及服务保障范围。该支持体系以平台原生 API 和控制台能力为基础，同时明确区分阿里云责任边界与用户/第三方责任范围。所有使用均需遵守相关法律协议与合规要求。

## 支持的模型/功能

- **Agent 能力**：官方提供 6 款内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果，广泛应用于问答系统、客户服务、教育训练等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持通过 Assistant API 注册并调用用户自定义函数，大模型可理解参数结构并生成调用逻辑；但**不支持透传除 `Authorization` 外的任意 HTTP Header**，此为硬性限制 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **协议与合规**：所有应用需遵守《阿里云百炼服务协议》《阿里云百炼体验功能特别说明》及开源模型相关条款，上架小程序或应用市场前须完成[应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

> **注意**：文档 2 中“Agent 和 Assistant API 的最大区别”描述（“调整插件模型、基于上下文的理解，用户可以自己去开发”）存在表述模糊，易误解为 Agent 可直接修改底层模型行为；实际二者均为调用百炼托管模型，差异在于编排粒度与 SDK 封装层级——Assistant API 提供更高阶的类封装与 prompt 管理能力，而 Agent 更侧重插件调度与状态管理。建议以控制台实际能力为准。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming.md)，适用于前端实时渲染场景。
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming.md)（即每次返回新 token 而非全量重发），需服务端与 SDK 版本支持。
- 文件上传必填 `MD5`：用于校验文件完整性，上传 PDF 时后缀必须为小写 `pdf`，否则触发错误码 `140010`。
- 知识库文档上限：单业务空间最多 10 万个文档，超限时需提交工单申请扩容。

## 使用方式

- **插件调用**：内置插件在应用配置中启用；自定义插件需通过 Assistant API 注册 schema 并配置 endpoint，模型将依据函数描述自动推理参数。
- **RAG 调试**：若检索结果不准确，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **Markdown 渲染**：模型输出中的 `**text**` 等语法需由前端自行解析渲染，平台不提供服务端富文本转换。
- **备案与合作**：接入通义千问模型的应用上架前，须完成[应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并通过[大模型百炼合作协议备案自助申请助手](https://smartservice.console.aliyun.com/service/self-service-center/search?id=28023&mode=toolPage&trackFrom=topic-llm2&showDrawer=true)提交协议申请。

## 限制和注意事项

- **服务边界**：阿里云百炼售后仅覆盖平台自身服务（API、SDK、控制台、计费系统），**不包含**第三方工具（如 Cursor、Windsurf）、用户本地环境（代理/防火墙/内网）、业务代码实现或跨云厂商集成问题 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **Header 限制**：自定义插件调用时，仅 `Authorization` 头可被透传至目标服务，其他 header（如 `X-User-ID`、`X-Tenant`）将被丢弃，不可绕过。
- **数据导入规则**：结构化数据（如 Excel）导入时，空行将导致后续行被截断；首行为空则整表识别为空文件。
- **法律约束**：所有使用行为须同时遵守[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)，包括但不限于服务协议、体验功能特别说明及开源模型条款。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


