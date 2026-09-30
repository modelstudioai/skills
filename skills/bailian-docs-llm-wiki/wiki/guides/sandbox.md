# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络隔离，支持按需创建、暂停、恢复与释放。其核心能力通过模版（Template）统一配置，再由实例（Sandbox）按需承载具体任务。

## 支持的模型/功能

Sandbox 本身不提供大模型推理能力，而是作为**运行时环境**支撑智能体调用多种能力组件。根据基础镜像类型，支持以下功能组合：

- **代码解释器镜像（`code-interpreter-v1`）**：轻量 Python / Node.js 执行环境，适用于数据分析、脚本运行与文件处理。支持 `run_code`（需 `e2b-code-interpreter` SDK）及通用命令执行（`sbx.commands.run`）。详见 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器镜像（`browser`）**：预装 Chromium 的无头浏览器环境，3000 端口暴露 CDP 接口（`wss://<host>/ws/automation`），支持 Puppeteer、Playwright 或 BrowserUse 连接，用于网页自动化、截图、表单填写等。详见 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型镜像（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口）的复合环境，支持“网页采集 → 文件下载 → 本地分析 → 结果导出”端到端流水线。详见 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档中多次强调 `e2b==2.31.0` 和 `e2b-code-interpreter==2.8.1`（或 `@e2b/code-interpreter==2.6.1`）为当前稳定版本；更高版本 SDK 创建实例时返回 `405` 错误，该限制在 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 和 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 中均被明确指出，属已知兼容性约束，非文档矛盾。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建后生成，必填。决定镜像类型、资源配置与生命周期策略。 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。 | 见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `headers.Authorization` | 真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>`（`sk-...`）。**此为唯一生效的认证方式**。 | 见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 和 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `api_key` | E2B SDK 必填字段，仅用于满足格式校验（需以 `e2b_` 开头且后缀为十六进制字符），**百炼侧完全忽略该值**。推荐填 `e2b_${ALIYUN_UID}`。 | 见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `timeoutMs` | 实例创建/连接超时（毫秒），浏览器冷启动或长脚本需设为 `300000`–`900000`。 | 见 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 和 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) |

## 使用方式

1. **前置准备**：开通百炼服务并完成 [服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取阿里云 UID 与 API Key（`sk-...`）。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G），配置高级选项（如网络白名单、生命周期）。记录生成的 `templateCode`。
3. **初始化 SDK**：
   ```bash
   pip install "e2b==2.31.0"  # 必须指定版本
   pip install "e2b-code-interpreter==2.8.1"  # 如需 run_code
   ```
4. **创建并使用实例**：
   - 创建：`Sandbox.create(template="xxx", api_url="...", headers={"Authorization": "Bearer sk-..."})`
   - 执行：`sbx.commands.run("ls")`、`sbx.files.write(...)`、`sbx.run_code("...")`
   - 浏览器连接：`sbx.getHost(3000)` 获取 host，拼接 `wss://<host>/ws/automation`
   - 生命周期：`sbx.pause()` / `Sandbox.connect(...)` / `sbx.kill()`

## 限制和注意事项

- **实例生命周期**：空闲超时与最大存活时间二选一，**最长不超过 7 天**（见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 和 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）。
- **安全风险**：沙箱公网 URL（如 `wss://.../ws/automation`）等同于访问凭证，未加应用层鉴权时，持有者可完全控制浏览器会话（含 Cookie、登录态）。**严禁公开分享、写入日志或前端代码**（该警告在 [Browser Use](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 和 [AIO](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) 文档中重复强调）。
- **资源与文件**：输入文件需通过 `sbx.files.write()` 上传，单次任务建议限制大小与类型；产物文件（截图、CSV、JSON）应写入 `/tmp` 或自定义任务目录，再由业务侧主动读取。
- **调试支持**：所有镜像内置 noVNC，可通过 `https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true` 实时观察浏览器或终端（注意 `path` 必须以 `/` 开头）。
- **依赖固化**：生产环境应将常用库（如 `pandas`、`playwright-core`）固化至模版，而非每次运行时 `pip install`，以提升稳定性与启动速度。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)


