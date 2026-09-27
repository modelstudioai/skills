# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络隔离，支持按需创建、暂停、恢复与释放。其核心设计目标是保障多租户任务间的数据隔离与运行时安全，适用于数据分析、网页自动化、多工具协同等典型 Agent 场景 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 本身不提供大语言模型，而是作为**运行时环境**支撑各类 Agent 能力，通过三种预置基础镜像实现不同功能组合：

- **代码解释器（`code-interpreter-v1`）**：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行与结构化结果生成。推荐用于智能问答、运营分析等场景 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器（`browser`）**：基于 Chromium 的浏览器执行环境，暴露 CDP 接口（`wss://<host>/ws/automation`），支持 Puppeteer、Playwright 或 BrowserUse 连接，适用于网页采集、UI 测试与截图归档 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口）的复合环境，支持“访问网页 → 下载/截图 → 本地清洗 → 导出报告”端到端流水线 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档中多次强调 `e2b-code-interpreter` SDK 在 Node.js 侧需固定版本（如 `@e2b/code-interpreter@2.6.1`），而 Python 侧示例使用 `e2b-code-interpreter==2.8.1`。但文档 5 和文档 7 均明确指出：**更高版本的 `e2b` SDK（Python 与 Node.js）创建实例时返回 HTTP 405 错误**。因此必须统一锁定 `e2b==2.31.0`，否则无法完成实例创建。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` | 模版唯一标识符（`templateCode`），控制台创建模版后生成，必填 | 来自 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)；模版定义镜像、资源、网络策略等全部运行时配置 |
| `api_url` | 阿里云百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必须与工作区地域匹配；详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `Authorization` | 真实鉴权头，值为 `Bearer <阿里云百炼 API Key>`（`sk-...`） | **唯一生效的鉴权方式**；`api_key` 参数仅用于满足 E2B SDK 格式要求（见下条） |
| `api_key` | E2B SDK 必填字段，格式需为 `e2b_` + 十六进制字符串（如 `e2b_${ALIYUN_UID}`） | 阿里云 UID 为纯数字，天然满足校验；**百炼侧完全忽略该值，不用于业务鉴权** [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `timeoutMs` | 实例创建或命令执行超时（毫秒）。浏览器类任务建议 ≥600000（10 分钟） | AIO/Browser 场景需显著延长，因含浏览器冷启动、页面加载与脚本执行三阶段耗时 |

## 使用方式

1. **前置准备**：在百炼控制台完成[服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取具备 Sandbox 权限的账号及 API Key（`sk-...`）。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）、高级配置（如网络白名单、生命周期），生成 `templateCode`。
3. **初始化 SDK**：
   ```bash
   pip install "e2b==2.31.0" "e2b-code-interpreter==2.8.1"  # Python
   npm install e2b@2.31.0 @e2b/code-interpreter@2.6.1      # Node.js
   ```
4. **创建并使用实例**：
   - 代码类任务：调用 `sbx.commands.run()` 或 `sbx.run_code()`；
   - 浏览器类任务：先调用 `sbx.getHost(3000)` 获取 host，再通过 `wss://<host>/ws/automation` 连接 CDP；
   - AIO 类任务：组合上述两种模式，共享同一 `sandbox_id` 文件系统；
   - 所有任务结束必须调用 `sbx.kill()` 释放资源。

## 限制和注意事项

- **生命周期限制**：实例最大存活时间与空闲超时二选一，**最长不超过 7 天**；超时后自动释放，数据不可恢复 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。
- **URL 安全警告**：沙箱公网 URL（如 `https://xxx.cn-beijing.maas.aliyuncs.com`）等同于访问凭证，**未启用应用层鉴权时，持有者可完全控制浏览器会话（含 Cookie 与登录态）**。严禁公开分享、写入日志或前端代码 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **文件与资源限制**：上传文件数 ≤5 个（模版挂载）；单次命令/代码执行建议设置 `timeoutMs`（默认 30s 易中断）；生产环境需对输入文件大小、类型、输出路径做校验，避免磁盘耗尽或路径遍历 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **noVNC 调试路径**：需使用完整路径 `https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true`，`path` 参数**不可省略且必须以 `/` 开头**；相对路径或 `/vnc.html` 均导致连接失败 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)


