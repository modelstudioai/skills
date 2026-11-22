# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适模式，所有类型均统一接入百炼推理网关与可观测性体系。核心能力围绕 LLM 编排、工具调用、状态管理及安全隔离展开。

## 支持的模型/功能

- **Managed Agent**：平台托管的声明式 Agent，通过 YAML 配置定义工具链、记忆策略与终止条件，适合标准化客服、FAQ 等场景；不支持自定义 Python 逻辑 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：可视化流程编排 Agent（即 LLM Application），支持节点化连接 LLM、工具、条件分支与变量，可导出为可复用的 Flow JSON 模板 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Sandbox Agent**：基于容器的代码沙箱 Agent，允许上传完整 Python 项目（含 `requirements.txt` 和 `app.py` 入口），完全掌控执行逻辑与依赖，适用于需调用私有 SDK 或复杂状态机的场景 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- 应用广场提供预置 Agent 模板，可一键部署或作为开发起点。

## 关键参数

- `model_id`：必须指定，仅支持百炼已纳管的模型 ID（如 `qwen-max`, `qwen-plus`），不支持外部模型直连。  
- `enable_cot`：启用思维链输出（默认 `false`），仅对支持 `reasoning` 能力的模型生效。  
- `max_iterations`：最大工具调用轮次（Flow/Managed Agent 有效），范围 1–50，默认 15；Sandbox Agent 由用户代码控制迭代逻辑。  
- `timeout_ms`：端到端请求超时，最小 5000 ms，最大 300000 ms（5 分钟）。

## 使用方式

1. 创建 Agent 实例时，在控制台选择类型（Managed / Flow / Sandbox）；  
2. 按向导填写配置：Managed Agent 上传 YAML，Flow Agent 拖拽编排并保存，Sandbox Agent 上传 ZIP 包；  
3. 调用时通过 `/v1/agents/{agent_id}/chat` 接口发送 `messages` 数组，格式与标准 Chat API 一致；  
4. Sandbox Agent 的 `app.py` 必须实现 `run(messages: List[Dict], **kwargs) -> Dict` 接口，返回含 `content` 和可选 `tool_calls` 的响应。

## 限制和注意事项

- Managed Agent 和 Flow Agent 不支持动态加载外部模块或访问网络（除已授权工具外）；Sandbox Agent 的网络访问需在创建时显式开启 `allow_internet: true`，且受 VPC 安全组约束。  
- 所有 Agent 类型的输入 `messages` 总长度（字符数）上限为 100,000；单次响应 `content` 长度上限为 32,768 字符。  
- > **注意**：原始文档中提到的 [应用广场](raw/application-user-guide/agent-development/application-gallery.md) 当前仅支持 Flow Agent 模板导入，而旧版文档曾暗示 Managed Agent 模板亦可发布——该描述已过时，实际不支持。  
- Sandbox Agent 的构建过程会缓存依赖层，但每次上传新 ZIP 将触发完整重建，建议固定 `requirements.txt` 版本号以提升冷启性能。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


