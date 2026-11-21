# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全链路能力。开发者可根据业务复杂度、可控性需求和运维成本，在 Managed Agent、Flow Agent 和 Sandbox 三种模式中选择合适路径。所有模式均基于百炼统一的模型服务与运行时基础设施。

## 支持的模型/功能

- **Managed Agent**：面向标准任务（如客服问答、知识库检索）的托管式 Agent，内置意图识别、多跳检索、结果格式化等能力，无需编写逻辑代码；模型层默认使用 Qwen-Max 或 Qwen-Plus，支持在 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档中查看可选模型列表及切换方式。  
- **Flow Agent**：基于可视化流程图的 LLM 应用编排，支持条件分支、循环、工具调用（如数据库查询、API 调用）、状态管理；其底层执行引擎兼容 Qwen 系列全部大模型，具体能力边界详见 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md)。  
- **Sandbox**：提供 Python 运行环境与 SDK（`bailian-sdk`），允许完全自定义 Agent 行为（如自研记忆模块、异步工具调度）；需自行处理模型调用、流式响应、错误重试等细节，参考 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 获取环境约束与 API 规范。

## 关键参数

- `model_id`：必需，指定基础大模型（如 `qwen-max`, `qwen-plus`），不同 Agent 类型对 model_id 的校验严格度不同（Managed Agent 仅允许白名单模型）。  
- `timeout`：默认 30s，Flow Agent 和 Sandbox 可设为 60–180s，Managed Agent 固定为 30s 且不可覆盖。  
- `enable_stream`：仅 Flow Agent 和 Sandbox 支持 `true`；Managed Agent 不支持[流式输出](../concepts/streaming-output.md)，该参数会被忽略。  
- `tools`：仅 Flow Agent 和 Sandbox 支持显式声明工具列表；Managed Agent 的工具集由场景模板预置，不可动态增删。

## 使用方式

1. 在控制台「Agent 开发」页选择创建类型（Managed / Flow / Sandbox）；  
2. 配置基础参数（名称、描述、模型、超时等），按向导完成初始化；  
3. Managed Agent 直接部署上线；Flow Agent 需绘制节点并连接边；Sandbox 需上传 `main.py` 入口文件；  
4. 所有类型均支持通过 `/v1/agents/{agent_id}/chat` 接口调用，请求体结构统一（见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)）；调试阶段推荐使用控制台内置 Chat UI 实时验证。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 逻辑或外部依赖，若需扩展行为，必须迁移到 Flow Agent 或 Sandbox；  
- Flow Agent 的单次流程最大节点数为 50，嵌套深度 ≤ 5，超出将触发编译失败；  
- Sandbox 每次部署的代码包体积上限为 50MB（含依赖），且禁止执行系统命令（`os.system`, `subprocess` 等）；  
> **注意**：原始文档中 [应用广场](../../raw/application-user-guide/agent-development/application-gallery.md) 提到“可一键克隆广场 Agent 并修改为 Sandbox”，但当前平台实际仅支持克隆为 Flow Agent，Sandbox 克隆功能尚未上线（截至 v2.3.1），请勿依赖该描述。  
- 所有 Agent 类型均不支持跨 workspace 调用；若需复用，须导出配置后在目标 workspace 重新导入。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


