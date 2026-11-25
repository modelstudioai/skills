# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全链路开发。开发者可根据业务复杂度、可控性要求和运维能力选择 Managed Agent、Flow Agent 或 Sandbox 模式。所有模式均基于统一的运行时框架，但模型调用、状态管理与扩展机制存在差异。

## 支持的模型/功能

- **Managed Agent**：封装了意图识别、[工具调用](../concepts/tool-calling.md)、多轮记忆等能力，开箱即用，适用于标准客服、知识问答等场景；底层默认使用 Qwen-Max 或 Qwen-Plus（可配置），详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：基于可视化流程图构建 LLM 应用，支持条件分支、并行调用、自定义函数节点；其能力边界由所选模型决定，当前仅支持 `qwen-turbo` 及以上模型的流式响应能力，参考 [Flow Agent 文档](../../raw/llm-application.md)。  
- **Sandbox**：提供 Python 运行环境，允许用户编写任意逻辑（含异步 I/O、第三方库导入），但需自行实现工具注册、上下文维护与错误降级；该模式下模型调用必须通过 `dashscope.Generation.call()` 显式发起，具体约束见 [Sandbox](../../raw/agent-development/sandbox.md)。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 指定主推理模型 ID，如 `qwen-max`；Sandbox 中若未显式调用则无效 | `qwen-plus` |
| `enable_memory` | bool | 是否启用内置对话历史管理（仅 Managed/Flow Agent 生效） | `true` |
| `max_iterations` | int | [工具调用](../concepts/tool-calling.md)最大循环次数（防死循环） | `5` |
| `timeout` | int | 单次执行超时（秒），Sandbox 中作用于整个 `run()` 函数 | `30` |

> **注意**：`enable_memory` 在 Flow Agent 中实际受流程图中 Memory 节点配置控制，与该参数无直接关联；以 [Flow Agent 文档](../../raw/llm-application.md) 中的节点配置为准。

## 使用方式

1. **Managed Agent**：在控制台「Agent 开发」页创建，填写 [prompt](prompt.md)、配置工具集后一键部署，无需编码；  
2. **Flow Agent**：通过画布拖拽组件构建流程，导出为 YAML 或直接发布为 API；  
3. **Sandbox**：上传 `main.py` 入口文件及 `requirements.txt`，实现 `def run(inputs: dict) -> dict:` 接口；所有依赖须在 `requirements.txt` 中声明，否则运行时报错。

## 限制和注意事项

- Sandbox 模式不支持持久化存储、系统级进程或 `subprocess` 创建子 shell，且无法访问 `/tmp` 以外的文件路径；  
- 所有 Agent 类型均禁止调用外部服务（如 HTTP 请求）**除非**已通过平台「网络代理」白名单审核；未审核调用将被拦截并返回 `403`；  
- Managed Agent 的[工具调用](../concepts/tool-calling.md)结果最大返回长度为 8192 字符，超出部分将被截断——此限制未在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中明确说明，但实测生效；  
- Flow Agent 的 `max_iterations` 参数对条件分支内的循环无效，仅约束顶层工具调用链深度。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


