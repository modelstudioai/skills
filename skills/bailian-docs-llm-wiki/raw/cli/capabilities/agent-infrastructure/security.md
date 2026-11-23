# Security

阿里云百炼 CLI 查询安全防护统计、资产分布与风险告警的命令速查。

在终端查询 Agent 安全防护统计、资产分布与风险告警。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl agents security overview --help`。本文命令明细以 bl 2.2.1 为基准核实。

在各功能页也可查看对应用法，见 [Security 使用 CLI](raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 命令速查

### bl agents security overview

查看 Agent 安全防护总览（最近 24 小时）。需要 API Key 鉴权。

**语法**

```
bl agents security overview [flags]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：预览指定工作区的 Agent 安全防护总览

```
bl agents security overview --workspace-id ws-xxx
```

-   鉴权：使用 DashScope API Key（Bearer Token）。
-   `--workspace-id` 可通过 BAILIAN\_WORKSPACE\_ID 环境变量或配置项 workspace\_id 设置。
-   固定统计最近 24 小时；AgentStudio 地域固定为 cn-beijing，不可配置。
-   AgentStudio 域名：默认由 --workspace-id 推导；将 --base-url / DASHSCOPE\_BASE\_URL（或 `auth login --base-url`）指向某个 workspace（例如 https://<workspace-id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio）即可覆盖，此时无需 --workspace-id。

### bl agents security alerts

列出 Agent 安全告警。需要 API Key 鉴权。

**语法**

```
bl agents security alerts [flags]
```

参数

类型

必填

说明

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页结果数（默认：20）

`--risk-level <level>`

string

否

按风险等级筛选：high、medium、low

`--risk-name <text>`

string

否

按风险名称筛选

`--status <status>`

string

否

按处理状态筛选

`--status-list <status>`

array

否

按多个状态筛选（可重复传入）

`--app-name <name>`

string

否

按应用名称筛选

`--asset-type <type>`

string

否

按资产类型筛选：agent、tool、skill、knowledge\_base、memory、channel

`--vendor <vendor>`

string

否

按厂商筛选

`--order-by <field>`

string

否

排序字段（默认：check\_time）

`--order <dir>`

string

否

排序方向：asc、desc（默认：desc）

`--lang <lang>`

string

否

响应语言：zh、en

**示例**：预览指定工作区的 Agent 安全告警列表

```
bl agents security alerts --workspace-id ws-xxx
```

-   鉴权：使用 DashScope API Key（Bearer Token）。
-   `--workspace-id` 可通过 BAILIAN\_WORKSPACE\_ID 环境变量或配置项 workspace\_id 设置。
-   筛选、分页与排序参数走 query string；枚举类 flag 在发起请求前校验。
-   AgentStudio 域名：默认由 --workspace-id 推导；将 --base-url / DASHSCOPE\_BASE\_URL（或 `auth login --base-url`）指向某个 workspace（例如 https://<workspace-id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio）即可覆盖，此时无需 --workspace-id。
