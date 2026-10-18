# 函数调用

函数调用（Function Calling）是百炼平台中让大模型主动识别用户意图、生成结构化工具请求，并交由执行环境安全调用外部能力的核心机制。它不是简单的代码执行，而是模型推理层与业务逻辑层之间的标准化契约——模型输出 JSON Schema 格式的调用指令，平台负责参数校验、沙箱执行、结果注入与错误处理。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼三大 Agent 范式中承担不同角色，但均遵循统一语义协议（基于 OpenAPI 3.0 描述）：

- **Managed Agent**：通过 `Skill` 资源注册函数，模型在多步推理中自动触发调用；平台自动管理凭证注入（Vault）、超时控制（≤30 秒）和重试（默认 2 次，不可配置）。适用于 WebSearch、CodeInterpreter 等预置能力及企业自定义业务接口。
- **Flow Agent**：以「函数调用节点」形式嵌入可视化流程图，支持显式配置 `retry_times`、`timeout_ms` 和失败分支跳转；函数输入可来自上游节点输出或上下文变量（如 `{{memory.last_query}}`），适合需要人工干预决策路径的中等复杂度任务。
- **Sandbox**：不提供自动函数调用能力，但开发者可在 `main.py` 中直接调用已预装库（如 `requests`）或动态安装的第三方包；此时“函数调用”退化为普通 Python 函数调用，需自行处理参数构造、异常捕获与结果格式化（必须返回 JSON-serializable 对象），且受沙箱安全策略严格限制（禁止外网访问、系统命令等）。

> ⚠️ 注意：所有场景下，函数定义必须符合 OpenAPI 3.0 规范（含 `name`、`description`、`parameters`），否则注册失败；模型仅能调用已在当前 Agent 实例中显式声明并启用的函数。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 |
|------|----------|------|------|
| `name` | 全部 | string | 函数唯一标识符，必须与 OpenAPI `operationId` 一致；模型输出中 `name` 字段必须精确匹配，区分大小写。 |
| `parameters` | 全部 | object | JSON Schema 定义的参数结构，**必须指定 `type: "object"` 且包含 `properties`**；模型将据此生成结构化参数，平台执行前校验必填字段与类型。 |
| `retry_times` | Flow Agent | integer | 函数节点级重试次数（0–5），默认 `0`（不重试）；Managed Agent 中不可配置。 |
| `timeout_ms` | Flow Agent / Managed Agent Skill | integer | 单次函数执行最大毫秒数；Flow Agent 节点默认 `10000`，Managed Agent Skill 硬上限 `30000`。 |
| `enable_memory`（间接影响） | Managed / Flow | boolean | 若启用，函数调用结果可自动写入 Memory Store（需配置 `memory_store_type`），供后续对话引用；Sandbox 需手动实现。 |

> ✅ 最佳实践：在 `parameters` 中为每个字段添加 `description`，显著提升模型参数填充准确率；避免嵌套过深（建议 ≤3 层）或使用 `anyOf`/`oneOf` 等复杂联合类型。

## 面向开发者，简洁实用

- **调试技巧**：开启 `stream=false` 同步调用，查看模型原始 `tool_calls` 输出（含 `name` 和 `arguments` 字符串），快速定位参数生成问题；Flow Agent 可在控制台流程图中点击节点查看实时日志。
- **错误处理**：函数执行失败时，Managed/Flow Agent 默认将错误信息（如 `HTTP 404` 或 `JSON decode error`）作为字符串注入上下文，模型可能重试或转向其他工具；建议在函数逻辑中主动抛出带业务语义的异常（如 `"库存不足"`），而非裸露技术错误。
- **性能提示**：单次请求中函数调用总耗时计入 Agent 全局 `timeout_seconds`（Managed）或 `timeout_ms`（Flow），避免链式调用导致超时；高频低延迟函数（如查缓存）建议合并为单次调用。
- **安全边界**：函数代码运行在隔离沙箱，无法访问宿主文件系统、环境变量或未声明的网络地址；如需访问内网服务，请通过百炼 Connector 注册后调用，而非在函数内直连。

## 关联主题页

- [agent development](../guides/agent-development.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)


