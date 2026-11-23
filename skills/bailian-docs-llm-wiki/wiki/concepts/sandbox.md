# 沙箱环境

沙箱环境是百炼平台提供的**隔离、可控、按需启停的 Python 运行时实例**，专为安全执行用户代码（如工具调用、网页自动化、文件解析、自定义逻辑）而设计。它通过容器化技术实现网络、文件系统与进程空间的强隔离，确保代码运行不干扰平台主服务，也不泄露敏感上下文。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发模式选择**：作为三种 Agent 范式之一（与 Managed Agent、Flow Agent 并列），Sandbox 模式允许开发者完全自主实现 `Agent.run()` 接口，适用于需要深度控制执行流程、集成外部 SDK、处理二进制数据或实现复杂状态机的高自由度场景。
- **工具调用载体**：在 Managed 或 Flow Agent 中，当需执行 Python 代码（`sandbox://python`）或浏览器操作（`sandbox://browser`）时，系统自动调度一个沙箱实例完成任务，调用完成后默认释放（可配置持久化快照）。
- **安全执行边界**：所有沙箱内禁止执行系统命令（如 `os.system`, `subprocess.Popen`）、写入本地磁盘、监听端口、访问内网地址或加载未签名第三方包；违反即触发强制终止，保障平台整体安全性。
- **CLI 与 API 统一接入**：可通过 `bl agent sandbox exec` 命令快速启动临时沙箱调试代码，也可通过 Sandbox API（`/sandboxes` 等路径）进行全生命周期管理，实现 CI/CD 集成或批量作业编排。
- **计费独立单元**：沙箱按实例运行时长（小时）和存储快照（GiB·小时）单独计费，与其他组件（模型、知识库、记忆库）额度不互通，便于成本精细化管控。

## 关键参数和配置

| 参数 | 类型 | 说明 | 取值范围/示例 |
|------|------|------|----------------|
| `templateID` | string | 必填。已构建就绪（`buildStatus=ready`）的沙箱模版 ID | `tmpl-abc123xyz` |
| `timeout` | integer | 实例最大存活时间（秒） | `300`–`604800`（5 分钟–7 天） |
| `allow_internet_access` | boolean | 是否允许公网出向访问 | `true` / `false`（默认 `false`） |
| `lifecycle.on_timeout` | string | 超时后行为 | `"pause"`（暂停）、`"destroy"`（销毁，默认） |
| `auto_resume` | boolean | 暂停后首次连接是否自动恢复运行 | `true` / `false`（默认 `false`） |
| `cpuCount` / `memoryMB` | integer | 模版资源配置，必须成对指定且匹配平台规格 | `2`/`4096`、`4`/`8192` 等预设组合 |
| `mntConfig.originFileId` | string | 挂载文件 ID，仅支持 `source=sandbox_template` 且 `status=available` 的文件 | `file-sandbox-789` |
| `networkConfig.allowOut` | array[string] | 允许访问的域名白名单（仅限 `allow_internet_access=true` 时生效） | `["api.example.com", "cdn.jsdelivr.net"]` |
| `networkConfig.denyOut` | array[string] | 禁止访问的 IPv4/IPv6/CIDR（**不支持域名**） | `["192.168.0.0/16", "2001:db8::/32"]` |

> ⚠️ 注意：文件上传需先调用 `/files` 接口并轮询至 `status=available`；单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 等类型明确不支持。

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台创建 Sandbox Agent → 上传 `agent.py`（含 `class MyAgent(Agent)` 和 `run()` 方法）→ 调试 → 发布。
- ✅ **API 直连**：用 `bailian-sdk` 或直接调用 Sandbox API，推荐使用 `/v3/templates` 创建模版、`/sandboxes` 启动实例。
- ✅ **调试技巧**：通过 `POST /sandboxes/{id}/connect` 获取 `domain` 和 token，用 WebSocket 连接实时执行命令或上传文件。
- ✅ **成本优化**：非必要禁用公网访问；及时 `DELETE` 无用实例；避免长期保留快照（¥0.003/个/小时）；暂停后勿遗忘 `resume` 或 `destroy`。
- ❌ **禁止行为**：不要尝试绕过限制（如 `os.popen("curl ...")`），会立即终止；不要在沙箱内持久化业务数据——应通过 API 回传至外部服务。

沙箱不是通用服务器，而是**受控的、一次性的、面向任务的执行单元**。善用它，即可在安全前提下释放最大开发灵活性。

## 关联主题页

- [sandbox api](../api/sandbox-api.md)
- [agent billing](../guides/agent-billing.md)
- [agent development](../guides/agent-development.md)
- [capabilities](../guides/capabilities.md)
- [get started with agents](../guides/get-started-with-agents.md)


