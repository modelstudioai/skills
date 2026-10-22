# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发需求。开发者可根据任务复杂度、可控性要求和运维能力选择合适的 Agent 类型。所有 Agent 均基于平台统一的执行引擎与可观测性基础设施。

## 支持的模型/功能

- **Managed Agent**：面向业务逻辑封装的托管式 Agent，内置工具调用、记忆管理与多轮对话状态追踪，适合快速交付标准化服务。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图（LLM Application）构建的声明式 Agent，支持条件分支、并行调用、自定义函数节点，适用于规则明确、可建模的决策链路。其能力边界与配置项在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有完整说明。
- **Sandbox**：提供 Python 运行时沙箱，允许编写任意逻辑（含第三方库导入、HTTP 调用、本地计算），适用于需要强控制力或私有协议集成的场景。详细约束与 API 规范见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

- `timeout_ms`：全局执行超时，默认 30000（30 秒），Sandbox 可设为最高 60000；Flow Agent 不支持超过 45000。
- `max_steps`：仅 Flow Agent 和 Managed Agent 支持，限制 LLM 决策步数，默认 15，最大 50。
- `enable_memory`：布尔值，控制是否启用会话级[长期记忆](../concepts/long-term-memory.md)（仅 Managed Agent 默认开启）。
- `sandbox_runtime`：Sandbox 专用，指定 Python 版本（`python3.9` 或 `python3.11`），必须显式声明。

## 使用方式

1. 在控制台「Agent 开发」页新建项目，选择类型（Managed / Flow / Sandbox）；
2. 根据向导填写基础配置（名称、描述、入口函数等）；
3. 编辑核心逻辑：
   - Managed：配置工具集、设定意图识别规则；
   - Flow：拖拽节点、连接边、绑定 LLM 节点与函数节点；
   - Sandbox：编写 `main(input: dict) -> dict` 函数，确保返回 JSON 序列化对象；
4. 保存后点击「调试」，使用模拟请求验证行为。

## 限制和注意事项

- Sandbox 不支持持久化存储、系统级调用（如 `os.system`）、子进程创建及 `threading` 模块；内存上限 2GB，CPU 时间配额 30 秒（硬限）。
- Flow Agent 的 `max_steps` 实际生效需配合 LLM 节点的 `stop` 参数设置，否则可能因模型未按预期输出终止符而跳过步数检查。
- > **注意**：原始文档中 [Managed Agent](raw/application-user-guide/agent-development/managed-agents.md) 提到“支持异步工具回调”，但当前平台版本（v2.8.3+）尚未实现该能力，该描述已过时，请以控制台实际可用配置为准。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


