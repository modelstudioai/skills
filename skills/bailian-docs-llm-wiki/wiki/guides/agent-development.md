# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱环境的全栈开发需求。开发者可根据业务复杂度、可控性要求和运维能力，选择 Managed Agent、Flow Agent 或 Sandbox 模式。所有模式均基于统一的运行时框架，但抽象层级与扩展能力差异显著。

## 支持的模型/功能

- **Managed Agent**：面向标准任务（如客服问答、知识检索）的托管式 Agent，内置意图识别、工具调用编排与结果后处理，无需编写逻辑代码。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图的 LLM 应用构建方式，支持条件分支、循环、多模型串联及自定义函数节点，适合中等复杂度业务逻辑。其能力边界与配置项在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：完全开放的 Python 运行环境，允许加载任意第三方库、调用外部 API、持久化状态，并直接控制 LLM 调用链路。该模式的资源限制与安全策略见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

- `timeout`: 全局执行超时（秒），Flow Agent 和 Sandbox 默认 120s，Managed Agent 固定为 30s（不可覆盖）；
- `max_steps`: Sandbox 模式下最大推理步数，默认 50，超过将强制终止；
- `enable_tracing`: 是否启用全链路追踪（仅 Flow Agent 和 Sandbox 支持，Managed Agent 不支持）；
- `tools`: 工具列表仅对 Managed Agent 和 Flow Agent 有效；Sandbox 需自行实现工具注册逻辑。

## 使用方式

1. 在控制台创建应用 → 选择「Agent」类型 → 指定模式（Managed / Flow / Sandbox）；
2. Managed Agent：上传知识库 + 配置提示词模板 + 绑定工具（可选）；
3. Flow Agent：拖拽节点构建流程图，双击节点配置模型、提示词、工具或函数；
4. Sandbox：上传 `main.py` 入口文件及依赖 `requirements.txt`，通过 `@app.agent` 装饰器声明入口函数；
5. 所有模式均通过 `/v1/agents/{id}/invoke` 接口调用，请求体结构一致（详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)）。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 逻辑或异步 I/O，若需此类能力，必须切换至 Flow Agent 或 Sandbox；
- Flow Agent 的循环节点最多嵌套 3 层，且每次循环内 `max_steps` 累计计算；
- > **注意**：原始文档中 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 提到“支持动态工具加载”，但该功能已于 v2.3 版本下线，实际仅支持静态绑定工具列表，最新行为以 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 为准；
- Sandbox 模式禁止访问内网地址（如 `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`）及本地文件系统（`/tmp` 除外），违反将触发沙箱隔离；
- 所有模式均不支持 WebSocket 长连接，流式响应仅通过 SSE（Server-Sent Events）实现。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


