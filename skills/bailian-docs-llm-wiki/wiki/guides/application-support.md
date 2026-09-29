# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能可扩展、调用可追溯、问题可定位、服务可预期。所有支持行为均以阿里云百炼平台自身服务边界为前提，不延伸至第三方工具或用户侧基础设施。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置独立执行），再基于相关性得分聚合选取 topN 结果，适用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段而非全量重发） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议注册函数/API，大模型可理解参数结构并生成调用逻辑；但**仅支持透传 `Authorization` header，不支持其他自定义 header**（如 `X-User-ID` 等）。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类型、抽象接口还是配置模板），该表述缺乏上下文支撑，建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中明确的 API 和 SDK 支持范围为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量输出模式（避免重复返回历史 token） | 否（默认 `False`） |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |
| `Authorization` | string | 自定义插件调用时唯一允许透传的 header 字段 | 是（若需鉴权） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中声明插件能力，或通过 Assistant API 的 `tools` 字段注册函数 schema；模型将自动规划调用时机与参数。  
- **RAG 集成**：在应用配置中绑定知识库，系统自动完成分块、向量化与检索；测试阶段若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行会导致后续数据被截断（第一行为空则视为无效文件） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后支持入口**：7×24 小时支持渠道包括官网在线客服、电话（95187 / 400）、阿里云 APP 及标准工单；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件透传限制**：自定义插件调用时，服务端**仅解析并透传 `Authorization` header**，其余 header（如 `X-Custom-Header`）会被静默丢弃。  
- **知识库容量上限**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具免责**：阿里云不负责 Cursor、Windsurf 等第三方 AI 工具的安装、配置、故障排查或与本地环境（代理/防火墙/VPN）的兼容性问题；仅提供百炼 API 连通性验证与调用示例参考 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须遵守《阿里云百炼服务协议》《体验功能特别说明》及开源模型相关条款，详见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


