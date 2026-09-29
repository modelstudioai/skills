# sandbox

sandbox 是百炼平台提供的安全隔离执行环境，用于运行用户提交的代码、浏览器自动化脚本或 AI Agent 指令。它通过容器化沙箱机制保障系统安全与资源隔离，支持按需启动、自动销毁，并与百炼应用工作流深度集成。开发者可通过 SDK 或 API 控制沙箱生命周期，适用于代码解释、网页抓取、多步工具调用等场景。

## 支持的模型/功能

sandbox 本身不直接对应“模型”，而是作为**执行载体**支持多种能力模块：
- **Code Interpreter Sandbox**：执行 Python 代码（含 NumPy、Pandas、Matplotlib 等预装库），适用于数据处理与可视化 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)  
- **Browser Use Sandbox**：启动无头 Chromium 实例，支持 Puppeteer/Playwright 风格 API 进行网页交互与截图 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)  
- **AIO Sandbox**（Agent-in-One）：集成 LLM 调用、工具选择、代码执行与浏览器操作的端到端 Agent 运行时，适用于复杂任务编排 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)  

> **注意**：`AIO Sandbox` 在 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 中被描述为“实验性功能”，但 [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md) 显示其已于 v2.3.0 版本转为正式支持，文档状态不一致，请以 changelog 为准。

## 关键参数

创建 sandbox 实例时需指定以下核心参数（均通过 `create_sandbox()` SDK 方法或 `/v1/sandboxes` API 传入）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 取值：`code_interpreter` / `browser_use` / `aio` |
| `timeout` | integer | 否 | 执行超时（秒），默认 60，最大 300 |
| `max_memory_mb` | integer | 否 | 内存上限，默认 1024，范围 512–4096 |
| `keep_alive` | boolean | 否 | 是否保持实例存活（仅限调试），默认 `false`；设为 `true` 时需手动调用 `destroy` |

## 使用方式

1. **初始化 SDK**（Python）：
   ```python
   from baiLian import SandboxClient
   client = SandboxClient(api_key="YOUR_API_KEY")
   ```

2. **创建并运行实例**：
   ```python
   # 示例：执行一段 Python 代码
   sandbox = client.create_sandbox(type="code_interpreter")
   result = sandbox.run("import pandas as pd; pd.DataFrame({'x': [1,2]}).to_json()")
   print(result.output)  # 输出 JSON 字符串
   ```

3. **Browser Use 与 AIO 需额外传入上下文配置**，详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- 单次 sandbox 实例最长存活时间为 30 分钟（即使 `keep_alive=True`），超时后自动销毁；
- `code_interpreter` 禁止访问外网（除白名单 CDN 如 `pypi.org`、`cdn.jsdelivr.net` 外），禁止 fork 子进程或加载 `.so` 文件；
- `browser_use` 默认启用严格 CSP 与网络拦截，如需访问特定域名，须在创建时通过 `allowed_origins` 参数显式声明；
- 所有 sandbox 输出日志默认保留 7 天，原始文件（如生成的 PNG、CSV）需在实例销毁前主动下载，否则不可恢复；
- 沙箱内无法访问宿主机文件系统或其它 sandbox 实例，跨实例数据传递必须通过 API 显式传输。

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


