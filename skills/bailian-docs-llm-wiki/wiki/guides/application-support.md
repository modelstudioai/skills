# application [support](support.md)

`application support` 指百炼平台为开发者构建和运行 AI 应用（如 Agent、RAG 增强应用、插件集成应用等）所提供的核心能力支持体系，涵盖模型调用、功能扩展、参数控制、[流式输出](../concepts/streaming-output.md)、知识库检索及售后响应机制。该支持面向生产级集成场景，强调可配置性、可观测性和边界清晰的服务范围。

## 支持的模型/功能

- **Agent 能力**：支持基于大模型的智能体编排，内置六款官方插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分插件需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索（按用户配置执行），再基于相关性得分聚合排序选取 topN 结果，适用于问答系统、客户服务、教育等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持通过符合协议的 API 插件接入，大模型可理解其参数结构并完成调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”指代 SDK 接口类型、抽象封装层级或配置维度；当前最新 SDK 文档（v3.0+）中已统一使用 `Assistant` 作为核心客户端类名，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 所述 API 和 SDK 行为为准，避免依赖模糊术语。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)，适用于前端实时渲染。
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token 而非全量重发），需服务端模型与 SDK 版本协同支持。
- `MD5`（上传文件接口）：用于校验文件完整性，必填。
- `RequestId`：所有 API 调用返回的唯一请求标识，是定位 RAG 检索不准、模型回复异常等问题的关键线索，应记录并用于工单反馈。

## 使用方式

- **插件调用**：通过 `tools` 字段声明插件列表，由模型自主决策是否调用及传参；自定义插件需遵循 OpenAI-style function calling 协议。
- **RAG 应用测试**：在控制台测试窗中提交问题后，若结果不准确，可点击回复下方「问题反馈」按钮提交，或复制 `RequestId` 提交工单。
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行会导致结构化数据截断（如首行为空则识别为空文件）。
- **备案与协议**：上架应用/小程序前，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)并申请通义千问合作协议；相关法律条款详见 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 限制和注意事项

- **插件权限**：部分插件需单独申请开通，未获批前调用将失败。
- **Header 限制**：自定义插件调用时，仅 `Authorization` 可透传，其他 header（如 `X-User-ID`、`X-Tenant`）会被丢弃。
- **知识库容量**：单业务空间上限为 10 万个文档；超限时需提交工单申请扩容。
- **第三方工具支持边界**：阿里云售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障排查；仅提供阿里云百炼侧接口可用性、调用示例、计费核查及基础连通性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **责任划分**：阿里云仅保障百炼服务端（API、控制台、计量计费）的稳定性与正确性；用户本地环境（代理、防火墙、内网策略）、业务代码逻辑、第三方服务异常等不在标准支持范围内。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


