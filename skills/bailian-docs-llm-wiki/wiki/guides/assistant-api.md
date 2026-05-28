# assistant api

Assistant API 提供了一套标准化的服务端接口，用于快速构建具备多轮对话、上下文管理与工具调用能力的大模型应用。该接口通过封装模型推理流程与状态机逻辑，有效降低了复杂 AI Agent 的集成门槛。详细接口规范与交互说明可参考 [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md)。

## 支持的模型/功能
- **模型支持**：兼容千问系列核心模型，标识符包括 `qwen-turbo`、`qwen-plus`、`qwen-max`。
- **内置工具生态**：原生集成多款官方工具及扩展调用方式，无需额外配置外部服务。
  | 工具名称 | 标识符 | 适用场景 |
  |---|---|---|
  | 代码解释器 | `code_interpreter` | Python 执行、数学计算、数据分析 |
  | 夸克搜索 | `quark_search` | 实时网络信息检索 |
  | 文生图 | `text_to_image` | 文本转图像生成 |
  | 计算器 | `calculator` | 高精度数值运算 |
  | 生成二维码 | `generate_qrcode` | 文本转二维码 |
  | GitHub搜索 | `github_search` | 开源项目信息检索 |
  | [[function-calling|函数调用]] | `function` | 本地环境自定义逻辑执行 |
  | 知识检索增强 | `rag` | 外部知识库匹配与引用 |
  | 自定义插件 | `${plugin_id}` | 对接内部业务接口 |
- **核心能力**：自动维护 [[上下文管理]] 历史，支持 [[流式输出]]，并提供标准化编排模板以实现 [[多智能体]] 协同。完整能力矩阵详见 [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md)。

## 关键参数
API 交互依赖以下四个核心对象参数，需按生命周期顺序实例化：
- **Assistant**：定义模型基座（`model`）、系统指令（`instructions`）及启用的工具列表（`tools`）。
- **Thread**：会话级容器（`thread_id`），用于持久化存储多轮交互记录，解除开发者手动拼接 `history` 的负担。
- **Message**：内容载体，需指定 `role`（`user` / `assistant` / `system`）与 `content`。支持附加文件元数据。
- **Run**：推理与执行控制器。关键状态包括 `in_progress`、`requires_action`（待提交工具输出）、`completed` / `failed`。支持配置 `stream: true` 开启实时事件推送。

## 使用方式
标准调用链路遵循 `创建会话 -> 注入上下文 -> 触发执行 -> 处理回调` 模式：
1. 调用 `Assistants.create` 初始化配置。
2. 调用 `Threads.create` 获取独立 `thread_id`。
3. 调用 `Messages.create` 追加用户输入。
4. 调用 `Runs.create` 启动推理流。若返回 `thread.run.requires_action`，需解析 `tool_calls` 参数，在本地执行对应逻辑后，调用 `Runs.submit_tool_outputs` 将结果回传，直至 `run` 状态终结。
完整状态流转示例、事件枚举处理及工具回调代码可在 [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md) 中获取。

## 限制和注意事项
> **注意**：该 API 目前处于**下线中**阶段，官方已停止新增功能迭代。建议新项目全面迁移至 [[responses-api]]，新接口提供更完整的上下文生命周期管理及更丰富的原生工具支持。
- **体系隔离**：[[智能体应用]] 与 Assistant API 创建的实例在底层完全独立。控制台配置的应用仅能通过应用调用 API 访问，不可混用本接口管理。
- **快照版本兼容限制**：使用 `qwen-plus-1220`、`qwen-max-1220` 等带日期的快照版本时，系统仅支持 `function` 与 `rag` 工具。如需调用 `code_interpreter` 或搜索类工具，请使用无后缀的最新版本标识符。
- **容错建议**：自定义插件与外部搜索工具的执行成功率受网络及目标服务稳定性影响。建议在 `submit_tool_outputs` 环节增加重试机制与异常拦截，避免 `run` 状态因单次调用失败而永久阻塞。

## 来源文档

- [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md)

