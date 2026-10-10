# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，通过模版统一配置运行时环境，再基于模版快速启动多个隔离实例。

## 支持的模型/功能

Sandbox 不直接运行大语言模型，而是作为**运行时环境**支撑智能体执行多类任务，其能力由基础镜像决定：

- **代码解释器镜像（`code-interpreter-v1`）**：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行与结构化结果生成。推荐用于[使用 Code Interpreter Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)场景。
- **浏览器镜像（`browser`）**：预装 Chromium 的浏览器服务（端口 3000），支持 CDP 连接 Puppeteer/Playwright/BrowserUse，适用于网页自动化、截图、巡检与轻量 E2E 测试。
- **全能型镜像（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口），支持在同一实例中完成“访问网页 → 下载/截图 → 数据清洗 → 报告导出”的连续任务，详见[使用 AIO Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档 9 明确列出三种基础镜像名称为 `code-interpreter-v1`、`browser`、`all-in-one`；而文档 1 和文档 3 的表格中仅写为“代码解释器”“浏览器”“全能型”，属描述性简称。实际 API/SDK 中必须使用带版本号的完整镜像标识（如 `code-interpreter-v1`），否则创建失败。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建模版后生成，必填。见[模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)。 | 必须与控制台中创建的模版完全一致，大小写敏感 |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | workspace_id 需从控制台获取，地域固定为 `cn-beijing` |
| `Authorization` | 真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>` | **唯一有效鉴权方式**，见[实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `api_key` | E2B SDK 必填字段，仅用于满足 SDK 格式校验（需以 `e2b_` 开头且后缀为十六进制字符） | 推荐填 `e2b_${ALIYUN_UID}`，百炼侧**完全忽略该值**，不参与业务鉴权 |
| `timeoutMs` | 实例创建超时（单位毫秒），浏览器类任务建议 ≥300000（5 分钟） | 创建 AIO 或 Browser Sandbox 时需显著提高，避免因 browser 冷启动超时失败 |

## 使用方式

1. **前置准备**：完成[服务授权](raw/application-user-guide/sandbox/sandbox-quick-start.md)，开通 Sandbox 权限并创建模版；
2. **安装 SDK**：固定版本，`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）。更高版本创建实例时返回 HTTP 405 错误；
3. **创建实例**：
   ```python
   from e2b import Sandbox
   sbx = Sandbox.create(
       api_url="https://xxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
       api_key=f"e2b_{ALIYUN_UID}",
       headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
       template="your-template-code"
   )
   ```
4. **数据面操作**：
   - 执行命令：`sbx.commands.run("ls -l")`
   - 读写文件：`sbx.files.write("/path", content)` / `sbx.files.read("/path")`
   - 运行代码（需 `e2b-code-interpreter`）：`sbx.run_code("print(1+1)")`
   - 浏览器操作：通过 `sbx.getHost(3000)` 获取 host，构造 `wss://<host>/ws/automation` 连接 CDP；
5. **生命周期管理**：`sbx.pause()`（暂停）、`Sandbox.connect(sandbox_id=...)`（恢复）、`sbx.kill()`（释放）。

## 限制和注意事项

- **SDK 版本强约束**：所有文档（文档 4、5、6、7）均明确要求 `e2b==2.31.0`（Python）或 `e2b@2.31.0`（Node.js），更高版本创建实例时返回 405。`e2b-code-interpreter` 对应版本为 `2.8.1`（文档 5）或 `2.6.1`（文档 7），不可混用；
- **公网 URL 即凭证**：沙箱暴露的 `wss://<host>/ws/automation` 或 noVNC 地址（`https://<host>/static/vnc.html?path=/ws/livestream`）等同于控制权，**严禁公开分享、记录日志或嵌入前端代码**；
- **计费粒度**：按秒计费，包含「会话运行费」（按资源配置档位）与「数据保留费」（暂停/Snapshot 占用空间 × 时长），详情见[计费说明](raw/application-user-guide/sandbox/sandbox-billing.md)；
- **路径与协议细节**：noVNC 的 `path` 参数**必须以 `/` 开头**（如 `/ws/livestream`），相对路径会被错误解析；根路径 `/vnc.html` 返回 404；
- **鉴权唯一性**：`Authorization: Bearer <百炼 API Key>` 是唯一生效的鉴权方式，`api_key` 字段纯属 SDK 兼容占位，百炼服务端不校验其内容。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [计费说明](../../raw/application-user-guide/sandbox/sandbox-billing.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


