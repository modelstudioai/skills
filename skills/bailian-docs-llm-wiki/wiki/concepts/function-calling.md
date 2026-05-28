# 函数调用

函数调用（Function Calling）是大语言模型将自然语言意图转化为结构化外部工具请求的机制。模型根据上下文与系统指令自主调度已注册的插件、API 或协议服务，执行外部逻辑后回传结果，从而突破纯文本生成边界并实现复杂业务闭环。

## 在百炼平台不同场景中的使用
百炼平台提供多种架构范式支持函数调用，开发者可根据业务确定性需求选择适配路径：
- **[[智能体应用]]**：采用提示词驱动与模型自主规划架构（ReAct）。开发者挂载工具后，模型基于对话上下文动态触发调用、解析参数并串联多步执行。支持配置 `ReAct 最大轮次`（1-50）控制单次会话的调用上限。
- **[[工作流应用]]**：采用可视化节点确定性编排。函数调用被固化为独立插件或代码节点，参数流转需手动通过变量映射串联，不依赖模型自主决策，适用于高稳定性要求的固定业务链。
- **API 直调与 Assistant 架构**：通过请求体 `tools` 字段声明可用函数。模型推理遇外部任务时，返回 `requires_action` 状态及结构化 `tool_calls` 指令。开发者需在本地环境执行逻辑，并调用 `Runs.submit_tool_outputs` 回传结果以驱动状态机流转。
- **[[模型上下文协议]] (MCP)**：基于 JSON-RPC 标准化协议接入外部服务。在智能体中作为函数调用资源池由模型动态调度；在工作流中采用“单节点绑定单工具”模式。支持 `streamableHttp` 传输与云端异步任务执行。

## 关键参数与配置
| 参数/配置项 | 说明与应用场景 |
|---|---|
| `tools` / 工具声明 | 定义可用函数集合。需提供唯一标识符、功能描述及 JSON Schema 参数定义，直接决定模型路由准确率。 |
| `tool_calls` / `requires_action` | 模型返回的调用指令结构。包含目标工具 ID 及从上下文中提取的入参值。在 Assistant API 中表现为 `Run` 对象的阻塞状态。 |
| `submit_tool_outputs` | 用于回传工具执行结果的核心接口。结果将自动拼接至上下文，触发模型二次推理并生成最终答复。 |
| `biz_params` (业务透传) | 应用调用 API 中的动态参数注入字段。通过 `user_defined_params` 结构可将运行时变量精准路由至指定自定义插件。 |
| **入参映射策略** | 支持“大模型识别”（自动从对话提取）或“业务透传”（SDK/HTTP 显式传入）。出参结构需严格遵循 JSON 规范，子属性严禁为空。 |
| **执行超时限制** | 自定义插件与工具执行默认存在 **5 秒超时**。高频或耗时场景建议改用 [[高代码应用]] 实现异步队列，或启用 MCP 极速模式消除冷启动。 |

## 开发注意事项
- **网络与安全边界**：官方 `code_interpreter` 隔离运行且无外网权限；MCP 自定义服务部署于无状态云端，**无固定公网 IP**，访问云资源需配置白名单或 VPC 互通。搜索类工具仅返回标题与摘要，不直接抓取网页详情。
- **状态机与容错设计**：函数调用链路依赖严格的状态流转。外部服务网络波动易导致 `Run` 永久阻塞，建议在 `submit_tool_outputs` 环节增加指数退避重试与异常拦截。
- **触发策略调优**：若模型未触发预期调用，优先检查工具描述（Description）是否清晰、System Prompt 是否划定调用边界，或尝试升级至 `qwen-max` 等强推理模型。
- **架构演进提示**：旧版 `[[assistant api]]` 已处于**下线中**阶段。新建项目推荐迁移至 `[[responses-api]]` 或平台原生应用架构，以获得更完整的上下文生命周期管理与更低的集成维护成本。

## 相关主题
- [[智能体应用]]
- [[工作流应用]]
- [[模型上下文协议]]
- [[插件]]
- [[responses-api]]
- [[assistant api]]

## 关联主题页

- [[assistant-api|assistant api]] — `../guides/assistant-api.md`
- [[plug-in|plug in]] — `../guides/plug-in.md`
- [[model-context-protocol|model context protocol]] — `../guides/model-context-protocol.md`
- [[llm-application|llm application]] — `../guides/llm-application.md`
- [[bailian-application-calling|bailian [[application-call|application call]]ing]] — `../guides/bailian-application-calling.md`
- [[assistantapi|assistantapi]] — `../api/[[assistantapi|assistantapi]].md`

