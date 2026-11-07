# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适模式，所有类型均统一接入百炼推理网关与可观测性体系。核心能力围绕 LLM 编排、工具调用、状态管理及安全隔离展开。

## 支持的模型/功能

- **Managed Agent**：平台托管的声明式 Agent，通过 YAML 配置定义工具链、记忆策略与终止条件，适合标准化客服、FAQ 等场景；不支持自定义 Python 逻辑 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：可视化流程编排 Agent（即 LLM Application），支持节点化连接 LLM、工具、条件分支与变量，可导出为可复用的 Flow 模板 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Sandbox Agent**：基于 Python 的全控制沙箱环境，允许编写任意 `run()` 函数、调用 SDK 工具、管理 session state，并支持异步 I/O 和第三方库（需白名单）[Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- 应用广场提供开箱即用的 Agent 模板，但其底层实现可能混合上述三种模式，具体以模板详情页标注为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model_id` | string | 必填；仅限平台已纳管的模型 ID（如 `qwen-max`），不支持自部署模型直接接入 Agent 运行时 |
| `timeout` | int | 可选；单位秒，默认 30，Sandbox Agent 最高支持 120，超时将强制终止执行 |
| `enable_tracing` | bool | 可选；开启后记录完整 token 流、工具调用链与错误堆栈，用于调试 |

> **注意**：`model_id` 在 Managed Agent 和 Flow Agent 中实际作用于 LLM 节点，而 Sandbox Agent 中需在代码内显式调用 `llm.invoke()` 并传入模型 ID；二者语义不一致，详见 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 与 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 文档差异。

## 使用方式

1. **创建**：在控制台「Agent 开发」页选择类型 → 填写基础信息 → 进入编辑器  
2. **配置/编码**：  
   - Managed Agent：编辑 YAML，参考 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 定义 `tools`、`memory` 等字段  
   - Flow Agent：拖拽节点并配置参数，保存后自动生成可部署 Flow  
   - Sandbox Agent：编写 `run(input: dict) -> dict` 函数，使用 `bailian.tool.*` 调用工具  
3. **调试**：使用「测试面板」输入 JSON 格式 `input`，实时查看输出、日志与 trace  
4. **部署**：发布为 API Endpoint，获取 `POST /v1/agents/{id}/invoke` 调用地址  

## 限制和注意事项

- 所有 Agent 实例共享账户级并发配额，单次请求最大响应体为 2MB；超出将截断并返回 `413 Payload Too Large`  
- Sandbox Agent 禁止执行系统命令（`os.system`、`subprocess`）、文件持久化（`open(..., 'w')`）及网络直连（仅允许通过 `bailian.tool.http` 封装的 HTTP 请求）  
- Flow Agent 的循环节点深度上限为 5 层，避免隐式死循环；Managed Agent 不支持显式循环，需靠工具返回 `continue: true` 触发重试  
- > **注意**：原始文档中 [应用广场](../../raw/application-user-guide/agent-development/application-gallery.md) 提到“支持一键克隆至 Sandbox”，但当前版本该功能已下线，克隆仅生成 Flow Agent 副本，实际行为以控制台操作为准。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


