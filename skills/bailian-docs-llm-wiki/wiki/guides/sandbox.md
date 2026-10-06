# sandbox

sandbox 是百炼平台提供的安全隔离执行环境，用于运行用户提交的代码、浏览器自动化脚本或 AI Agent 指令。它通过容器化沙箱机制保障系统安全与资源隔离，支持按需启动、自动销毁，并与百炼应用工作流深度集成。开发者可通过 SDK、API 或低代码模版快速接入。

## 支持的模型/功能

sandbox 当前支持三类执行模式：
- **Code Interpreter Sandbox**：执行 Python 代码（含 NumPy、Pandas、Matplotlib 等预装库），适用于数据处理与可视化任务；
- **Browser Use Sandbox**：基于 Chromium 的无头浏览器环境，支持网页抓取、表单交互与截图；
- **AIO Sandbox**：面向 AI Agent 的增强型沙箱，集成工具调用、多步任务编排与状态持久化能力（详见 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)）。

> **注意**：[使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md) 中列出的 `pyspark` 库在 v2.12+ 版本中已被移除，实际可用库请以 `sandbox-sdk list-languages --runtime python311` 输出为准。

## 关键参数

创建 sandbox 实例时需指定以下核心参数：
- `runtime`: 必填，取值为 `code_interpreter` / `browser_use` / `aio`；
- `timeout`: 执行超时时间（秒），默认 300，最大 1800；
- `max_memory_mb`: 内存上限（MB），默认 2048，最高 8192；
- `template_id`: 可选，引用预置模版 ID（参见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)）。

## 使用方式

推荐通过 `qwen-sandbox-sdk`（v0.8.0+）初始化并调用：
```python
from qwen_sandbox import SandboxClient
client = SandboxClient(api_key="sk-xxx")
result = client.run(
    runtime="code_interpreter",
    code="import pandas as pd; pd.__version__"
)
```
也可直接调用 REST API（`POST /v1/sandboxes/run`），请求体结构与 SDK 参数一致。完整示例见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- 单次执行输出日志上限 10 MB，超出部分将被截断；
- Browser Use Sandbox 不支持 WebSocket 长连接及 WebRTC；
- 所有 sandbox 实例在执行完成后自动销毁，**不保留文件系统状态**（AIO Sandbox 的显式 `save_state` 除外）；
- 免费试用额度仅限 `code_interpreter` 运行时，`browser_use` 和 `aio` 需开通付费配额（详见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）。

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


