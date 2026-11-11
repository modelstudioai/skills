# application [support](support.md)

阿里云百炼平台的应用支持体系面向开发者提供覆盖模型调用、插件集成、RAG应用构建及日常运维的全链路技术保障。支持范围以平台自身服务边界为基准，聚焦 API/SDK 使用、控制台操作、计费核查与基础连通性诊断；第三方工具、本地环境及业务代码等非平台侧问题属于方向性建议范畴。所有支持均以《[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)》为根本依据。

## 支持的模型与功能

- **官方插件能力**：当前开放六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；部分需申请开通。
- **自定义插件**：支持通过符合 OpenAPI 规范的 HTTP 接口注册，模型可理解参数结构并完成调用；但**不支持透传除 `Authorization` 外的任意自定义 Header**（详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第10条）。
- **RAG 应用**：支持多知识库并行检索 + 得分排序（topN），适用于问答、客服、教育等场景；检索结果准确性优化可通过工单提交 `RequestId` 反馈。
- **[流式输出](../concepts/streaming-output.md)控制**：支持增量式流式响应，需同时设置 `stream=True` 与 `incremental_output=True`（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第8条）。

> **注意**：文档3中第4条称“Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该描述未在其他文档中得到技术实现层面印证，且与文档1明确限定的“支持范围不包括用户业务代码编写”存在潜在冲突。实际开发中，插件逻辑须由用户自主实现并托管，百炼仅提供调用协议与路由能力。

## 关键参数

| 参数 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（避免重复返回历史内容） | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `MD5`（文件上传） | string | 用于校验文件完整性，必填 | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |
| `Authorization` | string | 唯一支持透传至自定义插件的 Header 字段 | [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **技术支持渠道**：7×24 小时电话（95187 / 400）、智能在线、标准工单；优先推荐通过控制台提交工单并附带 `RequestId`（如 RAG 调试问题）。
- **调试建议**：
  - 连通性验证：使用 `curl` 测试百炼服务地址可达性；
  - 接口测试：参考官方 SDK 示例与 API 文档；
  - 计费核查：通过控制台查看调用明细与账单记录。
- **合规与备案**：接入通义千问模型上架应用市场或小程序，须按 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 指南操作，并通过工单申请合作协议。

## 限制和注意事项

- **不支持范围**（严格遵循 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)）：
  - 第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级及故障排查；
  - 用户本地环境（代理、VPN、防火墙、操作系统兼容性）导致的问题；
  - 业务代码编写、调试与实现；
  - 开源模型协议条款解释（参见 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)）；
  - 第三方工具内部统计（如 Token 数、费用预估）与阿里云实际计费数据的差异归因。
- **责任边界**：阿里云仅对百炼服务端（API 接口、计量计费系统、控制台功能）负责；第三方工具运行维护由用户及对应提供方承担。
- **法律依据**：所有服务受《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》约束，体验功能另需遵守《阿里云百炼体验功能特别说明》。

## 来源文档

- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)


