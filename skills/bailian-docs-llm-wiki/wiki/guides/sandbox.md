# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心能力通过模版（Template）定义，实例（Sandbox）基于模版启动并继承全部运行时配置 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 本身不提供大模型推理能力，而是作为**运行时环境**，支撑三类典型 AI Agent 场景：

- **代码解释器（Code Interpreter）**：基于 `code-interpreter-v1` 镜像，支持 Python/Node.js 脚本执行、数据分析与结构化结果生成，适用于智能问答、报表生成等场景 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器操作（Browser Use）**：基于 `browser` 镜像，暴露 CDP 端点（`wss://<host>/ws/automation`），支持 Puppeteer/Playwright/BrowserUse 连接，完成网页访问、交互、截图与动态内容采集 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型（AIO）**：基于 `all-in-one` 镜像，同时集成浏览器服务（3000 端口）与 Code Interpreter 服务（5000 端口），支持“网页采集 → 下载 → 数据清洗 → 报告导出”端到端流水线 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档 1 和文档 8 中列出的镜像名称存在不一致——文档 1 称“代码解释器”“浏览器”“全能型”，而文档 8 明确给出实际镜像 code 为 `code-interpreter-v1`、`browser`、`all-in-one`。开发中必须使用后者作为 `template` 参数值，前者仅为控制台显示别名。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` | 模版唯一标识符（`templateCode`），创建模版后获得 | 必填；取值必须为控制台创建模版时生成的实际 code，如 `browser-abc123` |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必填；需替换 `{workspace_id}` 为实际工作区 ID |
| `Authorization` | 鉴权头，`Bearer <阿里云百炼 API Key>` | **真实鉴权凭据**；必须使用百炼控制台生成的 `sk-...` 类型 API Key |
| `api_key` | E2B SDK 必填字段，仅用于满足 SDK 格式校验 | 值需满足 `e2b_` + 十六进制字符（如 `e2b_123456789`），推荐用 `e2b_${ALIYUN_UID}`；**百炼侧不使用该值鉴权** [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `timeoutMs` | 实例创建超时（单位 ms），建议设为 `300000`（5 分钟）以上 | 浏览器/AIO 沙箱冷启动耗时较长，过短易导致 `create()` 失败 |

## 使用方式

1. **准备模版**：在控制台 [Sandbox > 我的模版](https://bailian.console.aliyun.com/cn-beijing/sandbox/my-template) 创建模版，选择镜像、资源配置（1C2G 或 4C8G）、可选挂载文件/环境变量/网络策略，并设置生命周期（空闲超时或最大存活时间，最长 7 天）[模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)。
2. **安装 SDK**：固定版本，避免 405 错误：
   ```bash
   pip install "e2b==2.31.0" "e2b-code-interpreter==2.8.1"  # Python
   npm install e2b@2.31.0 @e2b/code-interpreter@2.6.1        # Node.js
   ```
3. **创建并使用实例**：
   - 调用 `Sandbox.create()` 启动实例，获取 `sandbox_id`；
   - 通过 `sbx.commands.run()` 执行命令、`sbx.files.write()` 写入数据、`sbx.run_code()` 运行代码（需 `e2b-code-interpreter`）；
   - 浏览器/AIO 沙箱需调用 `sbx.getHost(3000)` 获取公网 host，再构造 CDP URL（`wss://<host>/ws/automation`）连接 Puppeteer/Playwright；
   - 任务结束调用 `sbx.kill()` 释放资源。

## 限制和注意事项

- **SDK 版本强约束**：所有文档（3、4、5、6、8）均明确指出，`e2b>=2.32.0` 及更高版本创建实例时返回 HTTP 405 错误，必须锁定 `e2b==2.31.0` 及配套子包版本。
- **URL 安全风险**：沙箱公网 host（如 `xxx.cn-beijing.maas.aliyuncs.com`）即为浏览器控制凭证，未启用应用层鉴权时，持有者可完全接管浏览器会话（含 Cookie、登录态）。**严禁公开分享、写入日志或前端代码** [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **资源与生命周期**：单实例最大资源配置为 4 Core｜8 GB；实例最长存活时间为 7 天（由模版生命周期配置决定）；暂停实例保留内存与文件系统状态，但不计费。
- **文件与网络**：文件挂载上限为 5 个；网络白/黑名单需在模版中预设；下载文件、截图等产物需主动写入沙箱文件系统（如 `/tmp/`），再通过 `sbx.files.read()` 下载回本地。
- **调试支持**：所有镜像内置 noVNC，可通过 `https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true` 实时观察浏览器或终端操作（注意 `path` 必须以 `/` 开头）。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)


