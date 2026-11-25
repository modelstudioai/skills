# 工具调用

工具调用（Tool Calling）是百炼平台中大模型主动识别用户意图、自主决策并执行外部能力的关键机制。它使 LLM 能够突破自身知识边界与计算局限，安全、可控地调用预注册的函数、API 或插件，完成实时信息检索、代码执行、图像生成、系统集成等任务。

## 在百炼平台的不同场景中，这个概念如何使用

工具调用在百炼平台并非单一接口能力，而是贯穿多种应用形态的统一执行范式，具体体现为以下三类典型场景：

- **托管智能体（Managed Agents）**：Agent 运行时，模型基于 `tools` 列表中的 Skill 定义（含名称、描述、参数 Schema），自主判断是否需要调用及调用哪个工具；调用结果自动注入后续推理上下文。开发者通过 `POST /v1/agents/{agent_id}/sessions` 的 `tools` 参数显式控制本次会话可用的工具子集。

- **流程化智能体（Flow Agent）**：工具以「HTTP 工具节点」形式被显式编排在流程图中，由开发者定义触发条件、输入映射与错误处理分支。此时调用非模型自主决策，而是流程逻辑驱动，适用于强确定性、需人工审核或需多工具协同的业务链路。

- **低代码应用（LLM Application）**：在新版智能体应用（Agent 2.0）中，工具调用默认启用（`enable_auto_tool_call: true`），插件作为“工具”被绑定至应用，模型根据用户输入和工具描述动态选择；而在工作流类应用中，工具节点（如 `quark_search`、`code_interpreter`）作为标准节点拖入画布，输入/输出严格遵循 `input_schema`/`output_schema` 校验。

> ✅ 共同前提：所有工具调用均依赖模型具备 tool-calling 原生能力。当前**仅 `qwen-plus` 和 `qwen-max` 明确支持且经文档交叉验证**；`qwen-turbo` 仅在 Managed Agents API 中提及支持，但未在插件文档中确认兼容性；其他模型（如 `qwen2.5-*`）暂不支持。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必需 |
|------|------|------|------|----------|
| `tools` | 请求体（Managed Agents / Assistant API） | array | 工具定义列表，每个元素含 `function.name`、`description`、`parameters`（JSON Schema 格式） | 否（未传则使用 Agent 默认技能集） |
| `tool_choice` | 请求体（部分 API） | string / object | 控制调用策略：`"auto"`（默认）、`"none"`（禁用）、或 `{ "type": "function", "function": { "name": "xxx" } }`（强制指定） | 否 |
| `tool_id` | 插件市场 / 自定义插件配置 | string | 工具全局唯一标识，用于控制台绑定或 API 显式引用 | 是（绑定/调用时必需） |
| `biz_params` / `user_defined_params` | 请求体（SDK/API） | object | 业务侧透传参数，绕过模型识别，直接注入工具请求体（常用于鉴权 token、租户 ID 等） | 否（按需） |
| `input_schema` / `output_schema` | Flow / LLM Application 配置 | object | 定义工具节点的输入约束与输出结构，用于运行时校验与类型转换 | 是（流程/应用发布时必需） |

> ⚠️ 注意：  
> - `code_interpreter` 等沙箱类工具**不支持网络访问与文件上传**，依赖库版本固定；  
> - 自定义插件的 `Object` 类型参数**子属性不可为空**，工具名长度 ≤ 20 字符；  
> - 所有 HTTP 工具节点目标域名**必须提前在控制台白名单备案**，且仅支持 HTTPS。

## 面向开发者，简洁实用

- **快速启用**：在控制台创建智能体时，直接从插件市场添加 `calculator`、`quark_search` 等官方工具；或在 Flow 编辑器中拖入「HTTP 工具」节点并填写 API 地址。
- **API 调用示例（Managed Agents）**：
  ```json
  POST /v1/agents/agt_abc123/sessions
  {
    "input": { "text": "计算 (123 + 456) * 789 的结果" },
    "tools": [
      {
        "function": {
          "name": "calculator",
          "description": "执行数学表达式计算",
          "parameters": {
            "type": "object",
            "properties": { "expression": { "type": "string" } },
            "required": ["expression"]
          }
        }
      }
    ]
  }
  ```
- **调试建议**：开启 `stream: true` 查看模型思考过程（含 `tool_calls` 事件）；对失败调用，检查 `X-RateLimit-Remaining` 头与错误码（如 `TOOL_EXECUTION_FAILED`、`INVALID_TOOL_INPUT`）。
- **安全第一**：敏感工具（如数据库操作）务必配置 Vault 凭证注入，避免硬编码密钥；RAM 子账号需主账号授予 `AliyunServiceRoleForSFMAccessCloudAPI` 角色权限方可使用插件市场。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [plug in](../guides/plug-in.md)
- [agent context](../guides/agent-context.md)
- [llm application](../guides/llm-application.md)


