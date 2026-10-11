# sandbox

sandbox 是百炼平台提供的安全隔离执行环境，用于运行用户提交的代码、浏览器自动化脚本或 AI Agent 指令。它通过容器化沙箱机制保障资源隔离与系统安全，支持按需启动、自动销毁，并与百炼模型调用链深度集成。开发者可通过 SDK、API 或低代码界面接入，适用于代码解释、网页交互、多步骤任务编排等场景。

## 支持的模型/功能

sandbox 本身不是模型，而是执行环境，但可与以下能力协同使用：
- **Code Interpreter Sandbox**：执行 Python 代码（含 NumPy、Pandas、Matplotlib 等预装库），适用于数据处理与可视化 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)；
- **Browser Use Sandbox**：启动无头 Chromium 实例，支持网页导航、表单填写、截图等操作 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)；
- **AIO Sandbox**：集成多工具链（含代码、浏览器、文件 I/O、HTTP 调用）的高级 Agent 运行时，适用于复杂工作流 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：`AIO Sandbox` 在 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 中被描述为“默认启用全部工具”，但 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) 明确要求显式声明 `tools: ["code_interpreter", "browser"]`，实际行为以后者为准。

## 关键参数

调用 sandbox 实例时需指定以下核心参数（以 REST API 和 SDK 为例）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 取值为 `"code_interpreter"`、`"browser"` 或 `"aio"` |
| `timeout` | integer | 否 | 执行超时（秒），默认 30，最大 300 |
| `max_steps` | integer | 否 | AIO 模式下最大推理步数，默认 15，上限 50 |
| `files` | array | 否 | Base64 编码的文件列表（仅 Code Interpreter / AIO 支持） |

完整参数定义见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 使用方式

1. **SDK 调用（推荐）**：安装 `dashscope` >= 1.20.0，使用 `SandboxClient` 初始化并调用 `run()` 方法；  
2. **REST API**：向 `POST /v1/sandbox/run` 提交 JSON payload，需携带 `Authorization: Bearer <api_key>`；  
3. **低代码界面**：在「应用构建」→「模版管理」中选择预置 sandbox 模板，配置输入变量后发布 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)。

所有方式均返回 `instance_id`，可用于轮询状态或获取执行结果。

## 限制和注意事项

- 单次 sandbox 实例最长运行 300 秒，超时强制终止且不计费；
- Code Interpreter 禁止访问外网（除 `pypi.org` 限速安装外）、禁止 fork 子进程、禁用 `os.system` 等高危系统调用；
- Browser Use Sandbox 默认启用 `--no-sandbox` 标志（因容器环境限制），但已通过 namespace 隔离加固，详情参见 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)；
- 免费额度每月 100 分钟 sandbox 运行时长，超出后按实际秒级计费，计费规则详见 [计费说明](../../raw/application-user-guide/sandbox/sandbox-billing.md)。

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


