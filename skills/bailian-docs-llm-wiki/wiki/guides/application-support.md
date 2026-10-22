# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理等核心功能。其支持范围明确区分平台原生能力（如官方插件调用、API 参数配置）与第三方依赖边界（如外部工具部署、本地环境问题），开发者需重点关注服务协议约束与实际能力边界。相关细节详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)、[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 和 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 支持的模型/功能

- **官方插件**：当前提供六款内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；部分需申请开通。
- **RAG 检索增强**：支持多知识库并行检索，按配置策略（如相似度得分）选取 topN 结果后融合生成；适用于问答系统、客服对话、教育内容生成等场景。
- **结构化数据导入**：支持 Excel/CSV 等表格格式，但存在空行即截断的解析策略（首行为空则视为无效文件）。
- **[流式输出](../concepts/streaming-output.md)控制**：支持 `stream=True` 全量[流式输出](../concepts/streaming-output.md)；如需增量式（即仅返回本次新增 token），须显式设置 `incremental_output=True`。

> **注意**：文档 1 中第 4 条称 “Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该描述未定义“插件模型”具体指代（是自定义 LLM 还是函数工具？），且与当前百炼控制台中统一通过 `tools` 字段注册函数插件的实践不符；建议以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中第 3 条关于函数参数透传的说明为准，即插件本质为符合 OpenAI-style function calling 协议的 HTTP 函数。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用流式响应（SSE），默认 `False`；设为 `True` 后响应体为 `text/event-stream`。 |
| `incremental_output` | bool | 仅在 `stream=True` 时生效；若为 `True`，每次 event 返回增量 token；若为 `False`，每次返回从开头累计的全量文本。 |
| `MD5`（上传接口） | string | 文件完整性校验字段，必填；用于服务端比对上传文件哈希值，防止传输损坏。 |
| `authorization`（插件调用） | header | 唯一支持透传的 HTTP Header；自定义 Header（如 `X-Api-Key`）将被丢弃，见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 第 10 条。 |

## 使用方式

- **插件调用**：通过 `tools` 字段声明函数 schema，模型自动选择并填充参数；服务端仅透传 `Authorization` header，其余 header 不生效。
- **RAG 测试优化**：若检索结果不准确，可通过回复下方「问题反馈」按钮提交，或复制 `RequestId` 提交工单；不建议依赖前端渲染逻辑修正语义偏差。
- **文件上传**：PDF 文件后缀必须为小写 `pdf`，否则报错 `140010`；单业务空间上限 10 万文档，超限时需提交工单申请扩容。
- **流式消费**：客户端需按 SSE 协议解析 `data:` 字段；启用 `incremental_output=True` 后，前端应累积拼接各 chunk 而非覆盖渲染。

## 限制和注意事项

- **插件能力限制**：自定义插件本身不收费，但通过智能体 API 进行 prompt 调优、应用调用测试等操作将产生计费。
- **第三方工具支持边界**：阿里云仅保障百炼服务端可用性、API 接口规范及计费一致性；对于 Cursor/Windsurf 等第三方工具的安装、配置、本地代理/防火墙导致的连通性问题，或用户业务代码逻辑错误，不在售后支持范围内（详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第 4 条）。
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型调用还需符合对应 [开源模型协议条款](../../raw/application-user-guide/application-support/application-related-agreements.md)。
- **安全与备案**：若应用需上架至应用市场或小程序平台，必须完成 [应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并单独申请通义千问合作协议。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


