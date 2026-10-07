# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能可验证、行为可预期、问题可追溯。所有支持能力均以百炼服务端 API 和控制台能力为边界，不延伸至用户侧代码或第三方工具的深度运维。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成，适用于问答、客服、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可启用增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范注册的[函数调用](../concepts/function-calling.md)，大模型可理解参数结构并生成符合协议的调用请求；但**仅支持透传 `Authorization` header，不支持其他自定义 header**（如 `X-User-ID` 等），该限制已在实际调用中验证 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类型、配置类或抽象接口类）；当前 SDK 文档与控制台无对应“类”级配置入口，建议以实际 API 参数和 SDK 方法为准，避免依赖该模糊表述。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量 token 输出（避免重复回传历史内容） | 否（默认 `False`） |
| `md5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |
| `authorization` | string | 自定义插件调用时唯一允许透传的 header 字段 | 是（若需鉴权） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用插件，或通过 Assistant API 的 `tools` 字段声明函数 schema；模型将自动选择并填充参数生成 `tool_calls`。  
- **RAG 应用调试**：在测试窗中复现问题后，点击回复下方「问题反馈」按钮提交类型与描述；**务必复制 RequestId**，以便工单精准定位日志 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；上传前需计算文件 MD5 并作为 `md5` 参数传入。  
- **售后支持入口**：7×24 小时可通过官网、电话（95187）、阿里云 APP 提交标准工单；深度支持（如定制集成方案）需联系商务经理订购增值服务 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件 header 限制**：自定义插件调用时，服务端**仅解析并透传 `Authorization` header**，其余 header（如 `X-Custom-Header`）会被静默丢弃，不可用于业务上下文传递。  
- **文件与数据限制**：单业务空间最多上传 10 万个文档；结构化数据导入时，**空行将导致后续所有行被跳过**（包括首行为空时整表识别为空）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具责任边界**：阿里云仅对百炼服务端（API 可用性、计费记录、SDK 示例）提供支持；第三方工具（如 Cursor、Windsurf）的部署、配置、故障排查不在售后范围内，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需额外遵循对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


