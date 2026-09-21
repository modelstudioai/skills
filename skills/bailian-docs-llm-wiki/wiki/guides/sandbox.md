# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络隔离，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，通过模版统一配置运行时环境，再基于模版快速启动多个实例。

## 支持的模型/功能

Sandbox 不直接提供语言模型，而是作为**运行时环境**支撑智能体调用各类能力。根据基础镜像不同，支持以下三类功能组合：

- **代码解释器镜像（`code-interpreter-v1`）**：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行与结构化结果生成。推荐用于[使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)场景。
- **浏览器镜像（`browser`）**：预装 Chromium 的浏览器环境，通过 CDP（Chrome DevTools Protocol）暴露 `wss://<host>/ws/automation` 端点，支持 Puppeteer、Playwright 或 BrowserUse 接入，适用于网页自动化、截图、巡检等任务。详见[使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型镜像（`all-in-one`）**：同时集成浏览器（3000 端口）与 Code Interpreter（5000 端口），支持在单个沙箱中完成“访问网页 → 下载/截图 → 本地清洗 → 导出报告”的端到端流水线。适用于复杂多阶段任务，参考[使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：所有镜像均不支持用户自定义安装系统级依赖（如 `apt-get install`），长期依赖应固化至模版；`all-in-one` 镜像中的 Code Interpreter 服务端口为 5000，但 SDK 调用 `run_code` 时无需显式指定端口，由 SDK 自动路由。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建后获得，必填 | 来自[模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必须匹配工作区地域与 ID，见[实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `Authorization` header | 实际鉴权凭证，值为 `Bearer <阿里云百炼 API Key>` | 真实业务鉴权字段，`sk-...` 格式，从控制台 [API-KEY](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 |
| `api_key` | E2B SDK 必填占位参数，仅用于满足 SDK 格式校验 | 必须以 `e2b_` 开头且后缀为十六进制字符（如 `e2b_${ALIYUN_UID}`），**百炼侧不使用该字段鉴权** |
| `timeoutMs` | 实例创建超时（毫秒），建议设为 `300_000`（5 分钟）以上，尤其对 `browser`/`all-in-one` 镜像 | 浏览器冷启动耗时较长，见[使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) |

## 使用方式

### 1. 控制台快速入门  
完成服务授权 → 创建模版（选择镜像、资源配置、生命周期）→ 获取 API Key → 使用 SDK 调用。全程约 5 分钟，详见[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)。

### 2. SDK 调用（推荐）  
安装固定版本 SDK（**必须**）：
```bash
pip install "e2b==2.31.0"  # Python
# 或
npm install e2b@2.31.0      # Node.js
```
> **注意**：文档 3、5、6、8 均明确指出，更高版本 SDK 创建实例时返回 HTTP 405 错误；此为当前生产环境强约束，非临时兼容问题。

示例（Python）：
```python
from e2b import Sandbox

sbx = Sandbox.create(
    api_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
    api_key=f"e2b_{ALIYUN_UID}",
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
    template="your-template-code",
)

# 执行命令
result = sbx.commands.run("python --version")

# 写入/读取文件
sbx.files.write("/tmp/input.csv", "a,b\n1,2")
content = sbx.files.read("/tmp/input.csv")

# （仅 code-interpreter/all-in-one）运行代码
execution = sbx.run_code("print(1+1)")

sbx.kill()  # 显式释放资源
```

### 3. REST API（高级场景）  
兼容 E2B 协议的管控面 API，用于模版管理、批量实例操作等。SDK 未覆盖的能力（如创建/删除模版）需直接调用，详见[Sandbox API](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- **生命周期限制**：实例最大存活时间为 7 天（从首次创建或恢复起计），空闲超时最长也为 7 天，二者二选一配置于模版中。超时后自动释放，**不支持续期**。
- **资源规格**：仅提供两种预设配置：`1 Core｜2 GB`（推荐）与 `4 Core｜8 GB`，不支持自定义 CPU/内存配比。
- **网络与安全**：
  - 沙箱公网 URL（如 `wss://<host>/ws/automation`）等同于访问凭证，**未启用应用层鉴权时，持有者可完全控制沙箱内浏览器（含 Cookie、登录态）**。严禁公开分享、写入日志或前端代码（见[使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 和 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) 警告）。
  - 网络策略仅支持白/黑名单规则，不支持细粒度防火墙策略或自定义 DNS。
- **文件系统**：所有写入 `/home/user/workspace/` 或 `/tmp/` 的文件在实例释放后永久删除；暂停（`pause()`）可保留文件系统与内存状态，但暂停期间不计费。
- **版本锁定**：E2B SDK 必须严格使用 `2.31.0`（Python/Node.js），`e2b-code-interpreter` 对应 `2.8.1`（Python）或 `2.6.1`（Node.js）。此限制源于服务端协议兼容性，非客户端可绕过。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)


