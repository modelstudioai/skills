# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象是「模版（Template）」与「实例（Sandbox）」：模版定义运行时配置（镜像、资源、网络等），实例是基于模版启动的隔离运行单元 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 不直接提供大语言模型，而是通过三种预置基础镜像支持不同能力组合：

- **代码解释器（`code-interpreter-v1`）**：轻量 Python/Node.js 运行环境，适用于数据分析、脚本执行与结构化结果生成。推荐用于智能问答、运营分析等场景 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器（`browser`）**：基于 Chromium 的浏览器执行环境，暴露 CDP 端点（`wss://<host>/ws/automation`），支持 Puppeteer、Playwright 或 BrowserUse 接入，适用于网页自动化、截图、巡检与轻量 E2E 测试 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口）的复合镜像，支持“访问网页 → 下载产物 → 本地清洗 → 导出报告”连续任务，适用于网页采集后分析、内容生产 Agent 等场景 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档 6 和文档 7 均强调“沙箱公网 URL 应视为访问凭证”，但文档 6 的警告语句出现在正文首段，而文档 7 的相同警告位于次级标题下；二者内容一致，无实质矛盾，以首次出现位置为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `Authorization` | 鉴权头，值为 `Bearer <阿里云百炼 API Key>`，**真实生效的鉴权方式** | [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `api_key` | E2B SDK 必填字段，仅用于满足格式校验（需为 `e2b_` + 十六进制字符），推荐填 `e2b_${ALIYUN_UID}`；**百炼侧不使用该字段鉴权** | [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `template` | 控制台创建模版后生成的 `templateCode`，用于指定运行环境 | [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `timeoutMs` | 实例创建超时（如 `900_000` ms），尤其 AIO 场景需预留浏览器冷启动+页面加载+代码执行时间 | [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) |

## 使用方式

1. **前置准备**：完成服务授权（创建 SLR 角色 `AliyunServiceRoleForSFMSandbox`），并获取阿里云百炼 API Key（`sk-...`）[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）、高级配置（网络白名单、环境变量、生命周期），获取 `templateCode`。
3. **调用 SDK**：
   - 安装固定版本 SDK：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；更高版本创建实例时返回 405 错误 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。
   - 创建实例：传入 `api_url`、`api_key`（占位）、`headers={"Authorization": "Bearer <API Key>"}` 和 `template`。
   - 执行操作：调用 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()`（需 `e2b-code-interpreter`）或连接 CDP（`sandbox.getHost(3000)`）。
   - 生命周期管理：`sbx.pause()` 暂停、`Sandbox.connect()` 恢复、`sbx.kill()` 释放。

## 限制和注意事项

- **SDK 版本强约束**：所有文档（2、3、5、6、7）均明确要求 `e2b==2.31.0`（Python）或 `e2b@2.31.0`（Node.js），更高版本创建实例时返回 HTTP 405 错误，此为硬性兼容限制。
- **实例生命周期**：空闲超时与最大存活时间二选一，**最长不超过 7 天**；暂停状态保留内存与文件系统，但不计费 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。
- **安全边界**：
  - 公网 URL（如 `wss://<host>/ws/automation`）等同于控制凭证，禁止公开分享、写入日志或前端代码 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
  - 登录态、Cookie、业务 [Token](../concepts/token.md) 等敏感信息必须运行时注入，**严禁固化到模版镜像中**。
- **资源与输入限制**：生产建议限制单次任务的文件大小、下载类型、命令超时及最大步数（如 BrowserUse 的 `max_steps`），避免资源耗尽或无限循环 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


