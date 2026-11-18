# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适模式，所有类型均统一接入百炼推理网关与可观测性体系。核心能力围绕 LLM 编排、工具调用、状态管理与调试诊断展开。

## 支持的模型与功能

- **Managed Agent**：平台托管的声明式 Agent，通过 YAML 配置定义工具链、记忆策略与终止条件，适合标准化任务（如客服问答、数据查询）；底层默认使用 Qwen-Max 或 Qwen-Plus，支持按需切换 [原文标题](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：可视化流程编排 Agent，支持节点拖拽、条件分支、循环与自定义 Python 脚本节点；完整兼容百炼内置工具（如 WebSearch、数据库连接器）及用户上传的 API 工具 [原文标题](../../raw/application-user-guide/agent-development.md)。
- **Sandbox Agent**：完全开放的 Python 沙箱环境，允许 `pip install` 第三方包、读写临时文件、调用 `requests` 等标准库，适用于需要复杂逻辑或私有协议集成的场景 [原文标题](../../raw/application-user-guide/agent-development.md)。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 仅 Flow/Managed Agent 可设；取值如 `"qwen-max"`、`"qwen-plus"`；Sandbox 中需在代码内显式初始化 `DashScopeClient` |
| `max_iterations` | integer | 默认 10，控制 Agent 最大推理步数（含工具调用），超限将强制终止 |
| `enable_memory` | boolean | 默认 `true`，启用会话级上下文缓存；Managed Agent 中可通过 `memory_strategy: "summary"` 压缩历史 |

> **注意**：`max_iterations` 在 Sandbox Agent 中**不生效**，需在用户代码中自行实现迭代控制逻辑，否则可能无限循环——该行为与 [原文标题](../../raw/application-user-guide/agent-development.md) 中“统一迭代限制”的描述存在矛盾，以实际运行时为准。

## 使用方式

1. **创建入口**：在控制台「应用开发」→「新建应用」→ 选择 Agent 类型（Managed / Flow / Sandbox）  
2. **配置与调试**：  
   - Managed：编辑 YAML，点击「实时预览」触发[流式输出](../concepts/streaming-output.md)与工具调用日志  
   - Flow：拖入节点后双击配置参数，在「调试面板」中上传测试输入 JSON  
   - Sandbox：编写 `main.py` 入口函数（必须含 `def main(input: dict) -> dict:` 签名），支持断点调试（需开启 `debug_mode: true`）  
3. **部署**：通过「发布」生成 API Endpoint，支持 REST 调用或嵌入 SDK（`from baiLian import AgentClient`）

## 限制和注意事项

- Sandbox 的 CPU 内存上限为 2GB，单次执行超时 60 秒；禁止访问 `/etc/`、`/proc/` 等系统路径及发起外网 DNS 查询（白名单域名除外）  
- 所有 Agent 类型均**不支持**跨会话共享内存（即不同 `session_id` 间无状态关联），需自行通过外部存储（如 Redis）实现持久化  
- Managed Agent 的 YAML 中若引用未发布的工具，保存时会报错，但错误提示未明确指向具体行号——该问题已在 [原文标题](../../raw/application-user-guide/agent-development.md) 的「常见问题」章节提及，建议结合控制台红字提示定位

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


