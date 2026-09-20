# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个沙箱实例基于模版启动，拥有独立计算资源、文件系统与网络隔离。开发者可通过控制台快速配置，或使用 E2B SDK 以标准方式接入和管理。

## 支持的模型/功能

Sandbox 不运行大语言模型本身，而是提供三种预置基础镜像（即运行时环境），供智能体调用执行任务：

- `code-interpreter-v1`：轻量级代码解释器，支持 Python / Node.js，适用于数据分析、脚本执行等场景（见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)）；
- `browser`：基于 Chromium 的浏览器环境，支持 UI 自动化、网页截图、表单交互等（见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)）；
- `all-in-one`：全能型镜像，集成代码解释器、浏览器及常用工具链，适用于需多能力协同的任务（见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）。

> **注意**：所有镜像均不支持用户自定义安装系统级依赖（如 `apt install`），仅允许在运行时通过 `pip install` 或 `npm install` 安装 Python/Node.js 包（该限制未在原始文档中明确说明，但由实际运行机制决定，属隐含约束）。

## 关键参数

| 参数 | 说明 | 来源与要求 |
|------|------|------------|
| `template` | 模版唯一标识符（`templateCode`），创建模版后生成，必填 | 控制台创建后记录；详见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `api_url` | 接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必须与当前工作区匹配，`workspace_id` 可从控制台 URL 或工作区设置获取 |
| `Authorization` | 真实鉴权凭证，`Bearer <阿里云百炼 API Key>` | 用于百炼服务端鉴权；`api_key` 字段仅满足 E2B SDK 格式要求，**不参与业务鉴权**（见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)） |
| `api_key` | E2B SDK 必填字段，格式需为 `e2b_` + 十六进制字符串（如 `e2b_${ALIYUN_UID}`） | `ALIYUN_UID` 为纯数字，天然合规；SDK 侧校验，百炼服务端忽略该值 |
| 生命周期参数 | `idle_timeout_seconds`（空闲超时）或 `max_duration_seconds`（最大存活时间），二选一，上限均为 604800 秒（7 天） | 在模版高级配置中设定；实例暂停后状态保留，但空闲超时触发的是休眠而非释放（见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)） |

## 使用方式

1. **前置准备**：开通百炼服务并确保账号具备 Sandbox 操作权限（见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）；
2. **授权与模版创建**：首次使用需完成 SLR 授权（角色名 `AliyunServiceRoleForSFMSandbox`），随后在控制台创建模版并记录 `templateCode`；
3. **SDK 集成**：
   - 安装推荐版本：`pip install "e2b==2.31.0"`，如需 `run_code` 则额外安装 `e2b-code-interpreter==2.8.1`；
   - 调用 `Sandbox.create()` 创建实例，传入 `api_url`、`headers={"Authorization": "Bearer <sk-...>"}`、`template` 和占位 `api_key`；
   - 实例创建后，可直接调用 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()` 等方法；
4. **生命周期管理**：使用 `sbx.pause()` 暂停、`Sandbox.connect()` 恢复、`sbx.kill()` 释放实例（见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)）。

## 限制和注意事项

- **资源规格固定**：仅支持两种配置：1 Core / 2 GB（推荐）或 4 Core / 8 GB，不支持自定义 CPU 内存配比；
- **文件挂载限制**：高级配置中“文件挂载”最多支持 5 个初始文件，且仅在实例首次启动时生效，运行中无法动态挂载；
- **网络策略粒度**：白/黑名单仅支持域名或 IP 段（CIDR），不支持端口级控制；
- **实例状态持久性**：暂停实例保留内存与文件系统状态，但若因底层资源调度被强制回收（非用户主动 `kill`），状态可能丢失 —— 此行为未在任一文档中说明，属平台隐含风险；
- **API 兼容性边界**：E2B SDK 的 `Sandbox.get_info()` 等方法可用，但模版管理（如创建/更新模版）无对应 SDK 封装，必须调用 raw HTTP 接口（见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 中说明）。

## 来源文档

- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)


