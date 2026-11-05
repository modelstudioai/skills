# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全链路能力。开发者可根据业务复杂度、可控性要求和运维成本选择合适模式。所有 Agent 均基于百炼统一推理底座运行，并与平台鉴权、监控、日志体系深度集成。

## 支持的模型/功能

- **Managed Agent**：平台托管的轻量级 Agent，适用于标准对话、知识问答等场景，无需编写代码，通过可视化配置即可发布；其能力依赖于底层 LLM 模型（如 Qwen-Max、Qwen-Plus）及向量库插件。详情见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于节点化工作流的可编程 Agent，支持条件分支、工具调用、多步记忆管理；本质是 LLM Application 的子集，与 [LLM 应用开发指南](../../raw/application-user-guide/llm-application.md) 中描述的流程引擎完全一致。
- **Sandbox Agent**：完全开放的 Python 沙箱环境，允许自定义模型调用、外部 API 集成、状态管理逻辑；需注意资源隔离与超时约束，具体限制参见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model` | string | 指定基础大模型 ID（如 `qwen-max`），仅 Managed/Flow Agent 支持显式设置；Sandbox 中由用户代码控制 | `qwen-plus` |
| `timeout` | int | 整个 Agent 执行最大耗时（秒），Sandbox 场景下不可超过 120s | 60 |
| `enable_tracing` | bool | 是否启用全链路追踪（含 LLM 调用、工具执行、缓存命中等） | `false` |

> **注意**：`model` 参数在 Flow Agent 中实际作用于每个 LLM 节点，而非全局生效；该行为与 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中“统一模型配置”的表述存在不一致，应以 [LLM 应用开发指南](../../raw/application-user-guide/llm-application.md) 的节点级配置为准。

## 使用方式

1. **创建 Agent**：在控制台「应用开发」→「Agent」中选择类型（Managed / Flow / Sandbox）；
2. **配置核心逻辑**：
   - Managed：填写提示词、绑定知识库、设置响应格式；
   - Flow：拖拽节点构建流程图，配置 LLM 节点模型与系统提示；
   - Sandbox：上传 `main.py` 入口文件，遵循 `def run(input: dict) -> dict` 签名；
3. **调试与部署**：使用内置 Playground 测试输入输出，通过「发布」生成 API Endpoint；发布后可通过 HTTP POST 调用，请求体为 JSON 格式 `{"input": {...}}`。完整接口规范见 [应用广场](../../raw/application-user-guide/agent-development/application-gallery.md) 中的调用示例部分。

## 限制和注意事项

- Sandbox Agent 不支持持久化写入本地磁盘、fork 子进程或加载动态链接库（`.so`/`.dll`）；
- 所有 Agent 的输入 `input` 字段最大长度为 1MB，超出将被截断并记录警告；
- Managed Agent 不支持自定义工具函数，如需扩展能力，必须切换至 Flow 或 Sandbox 模式；
- 同一账号下 Sandbox Agent 实例并发数上限为 5，如需提升请联系技术支持。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


