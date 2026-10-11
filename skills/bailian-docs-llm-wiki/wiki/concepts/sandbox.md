# 沙箱执行环境

沙箱执行环境是百炼平台提供的轻量级、按需启停的安全隔离计算单元，基于容器化技术实现资源隔离与系统防护，专为运行用户代码、浏览器脚本、AI Agent 工具调用等不可信或高风险操作而设计。每个沙箱实例独立启动、自动销毁，不共享内存、网络与文件系统，保障平台整体安全与多租户隔离。

## 在百炼平台的不同场景中，这个概念如何使用

沙箱执行环境不是独立模型，而是支撑多种能力的底层运行时基础设施，在以下核心场景中被统一调用：

- **代码解释（Code Interpreter）**：执行 Python 脚本（预装 NumPy/Pandas/Matplotlib 等），用于数据清洗、统计分析与图表生成；禁止外网访问（仅限 `pypi.org` 限速安装）、禁用 `os.system` 等危险调用。
- **浏览器自动化（Browser Use）**：启动无头 Chromium 实例，支持网页导航、表单填写、DOM 查询与截图；默认启用 `--no-sandbox`，但通过 Linux namespace 隔离强化安全。
- **AI Agent 运行时（AIO Sandbox）**：集成代码、浏览器、文件 I/O 和 HTTP 调用能力的多工具协同环境，适用于复杂工作流编排；需显式声明启用的工具（如 `"tools": ["code_interpreter", "browser"]`）。
- **Managed Agents 托管环境**：作为智能体的默认执行载体，承载 `bash`/`read`/`write` 等内置工具及 MCP 插件调用，自动管理会话状态、依赖安装与文件读写。
- **插件（Plug-in）底层支撑**：官方 `code_interpreter` 插件即运行于沙箱环境；所有自定义插件若涉及代码执行或网页抓取，也需绑定沙箱模板以确保安全隔离。

> ✅ 统一入口：无论通过 SDK、REST API 还是低代码界面调用，均使用 `/v1/sandbox/run` 接口，由 `type` 或 `template_id` 参数决定具体运行模式。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 典型值 |
|------|------|------|------|--------|
| `type` | string | 是（简易模式） | 指定预置沙箱类型 | `"code_interpreter"` / `"browser"` / `"aio"` |
| `template_id` | string | 是（高级模式） | 自定义或预置 Docker 模板 ID（优先级高于 `type`） | `"python3.11-cpu"` / `"llm-inference-base"` |
| `timeout` | integer | 否 | 执行超时（秒），范围 1–300 | 默认 `30`（`type` 模式）或 `60`（API 模式） |
| `max_steps` | integer | 否 | AIO 或 Managed Agent 模式下最大推理步数 | 默认 `15`，上限 `50` |
| `files` 或 `file_ids` | array | 否 | Base64 文件列表（SDK）或已上传文件 ID 列表（API） | 支持 `.py`, `.js`, `.csv`, `.pdf` 等 |
| `env` | object | 否 | 环境变量（API 模式），敏感键名（如 `API_KEY`）将被拒绝 | `{"DEBUG": "1", "PYTHONUNBUFFERED": "1"}` |

⚠️ 注意：
- `type` 与 `template_id` 不可同时指定，`template_id` 优先；
- 所有沙箱默认禁用外网访问（`outbound_network: false`），如需公网能力，须在模板中显式启用并经安全审批；
- 输出仅通过 `stdout`/`stderr` 返回 —— 请务必在代码中使用 `print()` 显式输出结果；
- 实例运行结束后自动销毁，磁盘不持久化；如需保存文件，请在代码中将内容打印为 Base64 编码字符串。

## 面向开发者，简洁实用

- ✅ **快速上手**：  
  ```python
  from dashscope import SandboxClient
  client = SandboxClient()
  res = client.run(type="code_interpreter", code="import pandas as pd; print(pd.__version__)")
  print(res.output)  # 输出：2.2.2（示例）
  ```

- ✅ **调试建议**：  
  - 首次失败时，检查 `timeout` 是否过短、`code` 是否语法错误、`files` 是否编码正确；  
  - 浏览器任务失败？确认 URL 可访问、页面加载完成后再操作（推荐加 `time.sleep(1)` 或等待 selector）；  
  - 使用 `env={"DEBUG": "1"}` 可获取更详细的容器启动日志。

- ✅ **性能与成本**：  
  - 免费额度：每月 100 分钟沙箱运行时长；  
  - 计费粒度：按实际执行秒数计费（不足 1 秒按 1 秒计）；  
  - 超时终止不计费，但强制销毁后无法恢复状态。

- ✅ **安全边界牢记**：  
  - ❌ 禁止 fork 子进程、调用 `os.system`、读写 `/proc` 或 `/sys`；  
  - ❌ 禁止挂载宿主机路径、修改内核参数、加载内核模块；  
  - ✅ 允许：pip 安装包（限速）、读写临时目录 `/tmp`、调用预装工具链。  

如需更高资源规格（如 GPU）、自定义镜像或企业级网络策略，请联系技术支持开通配额与审批通道。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)


