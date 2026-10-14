# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱环境的全栈开发需求。开发者可根据业务复杂度、可控性要求和运维能力，选择 Managed Agent、Flow Agent 或 Sandbox 三种模式。所有模式均基于百炼统一的运行时与调度框架，确保一致的安全隔离与可观测性。

## 支持的模型/功能

- **Managed Agent**：面向标准任务（如客服问答、知识库检索）的托管式 Agent，内置意图识别、工具调用编排、多轮对话状态管理；无需编写逻辑代码，通过配置即可上线。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图的 LLM 应用构建方式，支持条件分支、循环、自定义函数节点及多模型协同；适用于需灵活控制执行路径的中等复杂度场景。其能力边界与接口规范在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：完全开放的 Python 运行环境，允许加载任意第三方库、调用外部 API、持久化中间状态；适合算法密集型或需深度集成企业内部系统的高级用例。详细约束与初始化机制见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

- `timeout`: 全局执行超时（秒），Flow Agent 和 Sandbox 默认为 120s，Managed Agent 固定为 30s（不可覆盖）；
- `max_steps`: Flow Agent 最大执行步数，默认 50，超过将终止并返回 `TOO_MANY_STEPS` 错误；
- `sandbox_runtime`: Sandbox 环境仅支持 `python3.11`，不支持 `python3.9` 或 `python3.12`（[Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 明确限定）；
- `enable_tracing`: 启用后可获取完整执行链路日志，但会增加约 15% 延迟，生产环境建议按需开启。

## 使用方式

1. 在控制台「应用」→「新建应用」中选择对应类型（Managed / Flow / Sandbox）；
2. Managed Agent 通过表单配置知识库、提示词模板与工具集；  
3. Flow Agent 通过拖拽节点+连线定义执行流，双击节点编辑参数与脚本片段；  
4. Sandbox 需上传 `main.py` 入口文件及 `requirements.txt`，入口函数签名必须为 `def main(inputs: dict) -> dict:`；
5. 所有类型均支持通过 `/v1/agents/{id}/invoke` REST API 调用，请求体结构统一（参考 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)）。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 逻辑或外部 HTTP 调用，若需此类能力，必须切换至 Flow Agent 或 Sandbox；
- Flow Agent 的「自定义函数」节点仅支持同步执行，不支持 `async/await`，且单次调用耗时不得超过 `timeout / 2`；
- > **注意**：原始文档中 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 提到“支持动态加载工具插件”，但该功能已于 v2.3.0 版本下线，当前仅支持控制台预置工具集，实际行为以 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 的最新描述为准；
- Sandbox 每次部署会重建环境，`/tmp` 以外的写入（如 `./cache`）在实例重启后丢失，持久化请使用百炼提供的 `storage` SDK 或外部对象存储；
- 所有 Agent 类型均禁止访问内网地址（如 `10.0.0.0/8`, `192.168.0.0/16`），出向流量仅允许经由百炼代理网关转发。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


