# application [support](support.md)

阿里云百炼平台的应用支持覆盖模型服务使用、Agent 应用开发、知识库集成及配套运维等核心场景，面向开发者提供标准化的技术支持与问题响应机制。支持范围以阿里云百炼平台自身服务边界为基准，不延伸至第三方工具、用户本地环境或业务代码实现层。具体能力、参数与限制详见以下结构化说明。

## 支持的模型/功能

- **Agent 能力**：官方提供六类内置插件（Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索），部分需申请开通；支持自定义插件接入，但仅限符合协议规范的 API 接口 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索、按得分排序选取 topN 结果，适用于问答系统、客户服务、教育等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)控制**：支持 `stream=True` 启用基础流式响应；如需增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段而非全量重传），需显式设置 `incremental_output=True`。

## 关键参数

- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)，避免重复渲染历史内容。
- `stream=True`：启用基础流式响应（非增量）。
- 上传文件接口必填 `MD5` 参数：用于校验文件完整性，防止传输损坏 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- 自定义插件调用：**仅支持透传 `Authorization` header**，不支持其他自定义 header 字段；若实测未生效，应排查客户端是否正确构造该字段。

> **注意**：文档 2 中“Agent和Assistant API的最大区别”条目表述模糊（“调整插件模型、基于上下文的理解……方便调优”），未明确技术差异点，且与官方 SDK 文档中关于 Assistant API 的标准定义存在不一致。建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中对 API 支持范围的界定为准，即仅保障 API 接口可用性、调用示例与计费核查。

## 使用方式

- **问题反馈**：RAG 测试中模型回复不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单。
- **工单支持**：所有技术问题、故障诊断、配置咨询均通过阿里云工单系统受理；7×24 小时支持渠道包括官网、电话（95187 / 400）、智能在线及标准工单 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **第三方对接建议**：仅提供方向性指导，如确认百炼 API 可达性、提供 curl 测试示例、核查调用明细；不负责第三方工具（如 Cursor、Windsurf 等）的部署、配置或排障。

## 限制和注意事项

- **不支持范围**：
  - 第三方工具（含 AI 编程工具、开源代理框架等）的安装、升级、日常运维；
  - 用户本地环境（内网、代理、VPN、防火墙、OS 兼容性）导致的问题；
  - 业务代码编写、调试与实现；
  - 非阿里云百炼服务相关的账号、财务、合同问题（此类属阿里云通用服务范畴，非百炼专属支持）。
- **责任边界**：阿里云仅对百炼服务端（API、控制台、计量计费、模型推理服务）的稳定性与功能负责；第三方工具的运行维护由用户及对应提供方承担 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **文件上传限制**：PDF 文件后缀必须为小写 `pdf`；单业务空间最多上传 10 万个文档，超限时需提交工单申请扩容。

## 来源文档

- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


