# MCP & Skill

阿里云百炼 CLI 编排 MCP 服务与管理技能注册表的命令速查。

在终端编排 MCP 服务与管理技能注册表：列出已激活的 MCP 服务、查看与调用工具、把 MCP 服务注册进 Agent 原生配置，以及安装、更新与移除技能。

**说明**MCP 相关能力目前仅对中国站（aliyun.com）账号开放。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl mcp call --help`。本文命令明细以 bl 2.5.1 为基准核实。

## MCP 编排

在各功能页也可查看对应用法，见 [MCP 服务](raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。

### bl mcp list

列出百炼账号下已激活的 MCP 服务器。

**语法**

```
bl mcp list [flags]
```

参数

类型

必填

说明

`--name <text>`

string

否

按服务器名称筛选（子字符串匹配）

`--type <type>`

string

否

服务器类型：OFFICIAL | PRIVATE（默认：OFFICIAL）

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页结果数（默认：30）

**示例**：按名称筛选并列出已激活的 MCP 服务器

```
bl mcp list --name finance
```

### bl mcp tools

列出 MCP 服务器提供的工具（tools/list）。需要 API Key 鉴权。

**语法**

```
bl mcp tools --server <code> [--url <url>]
```

参数

类型

必填

说明

`--server <code>`

string

是

来自 `mcp list` 的 Server Code（例如 market-cmapi00073529）

`--url <url>`

string

否

覆盖 MCP Endpoint URL（非百炼）。先尝试 Streamable HTTP，再在同一 URL 上回退到传统 SSE。

**示例**：列出指定 MCP 服务器提供的工具

```
bl mcp tools --server market-cmapi00073529
```

### bl mcp call

调用 MCP 服务器上的工具（tools/call）。需要 API Key 鉴权。

**语法**

```
bl mcp call --target <server.tool> [--arg k=v ...] [--json '{...}'] [--url <url>]
```

参数

类型

必填

说明

`--target <server.tool>`

string

是

由点号连接的 Server Code 和工具名称，例如 market-cmapi00073529.SmartStockSelection

`--arg <kv>`

array

否

工具参数（可重复）。值会优先按 JSON 解析，否则作为字符串。

`--json <obj>`

string

否

完整的 JSON 参数对象；与 --arg 合并（--arg 优先）。

`--query <text>`

string

否

\--arg query=<text> 的快捷方式（与许多 DashScope MCP 工具一致）。

`--url <url>`

string

否

覆盖 MCP Endpoint URL（非百炼）。先尝试 Streamable HTTP，再在同一 URL 上回退到传统 SSE。

**示例**：调用指定 MCP 服务器上的工具并执行查询

```
bl mcp call --target market-cmapi00073529.SmartStockSelection --query "筛选 ROE 大于 15% 的消费股"
```

## Agent 原生注册

### bl mcp connect

将百炼 MCP 服务注册到 Agent 的原生配置中。需要 API Key 鉴权。

**语法**

```
bl mcp connect --server <code> --transport <streamable-http|sse> --agent <agent|all>
```

参数

类型

必填

说明

`--server <code>`

string

是

百炼 MCP Server Code，例如 TextGenerateImage

`--transport <transport>`

string

是

服务端提供的 MCP 传输协议：streamable-http 或 sse

`--agent <agent>`

string

是

目标 Agent：codex、claude-code、cursor、qoder、qoderwork、qwenwork、qwen-code、gemini、opencode、openclaw、deepseek-harness、zcode、workbuddy、pi，或 all

**示例**：将 MCP 服务注册到指定 Agent 的原生配置中

```
bl mcp connect --server TextGenerateImage --transport streamable-http --agent cursor
```

-   本期固定注册中国站官方 MCP 地址；模型 API 的 --base-url 不会改变 MCP 地址。
-   解析出的 API Key 会写入所选 Agent 的本地私有配置；CLI 不会覆盖非其管理的同名条目。
-   qoder、qoderwork、qwenwork 是彼此独立的产品。qwenwork 是千问办公（QwenWork）；qoderwork 是 Qoder Work。
-   workbuddy 覆盖 CodeBuddy / WorkBuddy。deepseek-harness 是 DeepSeek Harness，仅支持 streamable-http。

### bl mcp disconnect

移除此前由 bailian-cli 管理且未被修改的 MCP 注册。无需鉴权。

**语法**

```
bl mcp disconnect --server <code> --agent <agent|all>
```

参数

类型

必填

说明

`--server <code>`

string

是

connect 时使用的百炼 MCP Server Code

`--agent <agent>`

string

是

目标 Agent：codex、claude-code、cursor、qoder、qoderwork、qwenwork、qwen-code、gemini、opencode、openclaw、deepseek-harness、zcode、workbuddy、pi，或 all

**示例**：移除指定 Agent 上注册的 MCP 服务

```
bl mcp disconnect --server TextGenerateImage --agent cursor
```

-   如果注册项在 connect 后被修改，CLI 会保留该配置并报告冲突。

## 技能管理

在各功能页也可查看对应用法，见 [Skill](raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

### bl skill init

安装全部 bailian-\* Skill（用于新环境的一次性初始化）。无需鉴权。

**语法**

```
bl skill init
```

该命令仅支持全局参数。

-   获取 Registry 索引并安装名称以 `bailian-` 开头的所有 Skill。
-   等价于：`bl skill add --all`（筛选为 `bailian-*` Skill）。

### bl skill add

将百炼 Skill Registry 中的 Skill 安装到本地 Agent。无需鉴权。

**语法**

```
bl skill add --all | --name <name,...>
```

参数

类型

必填

说明

`--all`

switch

否

安装 Registry 中的全部 Skill

`--name <name,...>`

string

否

要安装的 Skill 名称，以逗号分隔

**示例**：安装 Skill Registry 中的全部技能到本地

```
bl skill add --all
```

### bl skill list

列出 Registry Skill，并与本地安装结果比较。无需鉴权。

**语法**

```
bl skill list
```

该命令仅支持全局参数。

**示例**：输出 JSON 格式的技能列表信息

```
bl skill list --output json
```

-   STATUS：installed | outdated | not-installed | missing（Lock 中存在但目录已删除）| untracked（目录存在但未被管理）

### bl skill update

将已安装的 Skill 更新到 Registry 最新版本。无需鉴权。

**语法**

```
bl skill update [--all] [--name <name,...>]
```

参数

类型

必填

说明

`--all`

switch

否

更新全部已安装 Skill（未指定 --all 或 --name 时的默认行为）

`--name <name,...>`

string

否

要更新的 Skill 名称，以逗号分隔（必须已安装）

**示例**：更新全部已安装的技能至最新版本

```
bl skill update --all
```

### bl skill remove

移除本地已安装的 Skill（不修改 Registry）。无需鉴权。

**语法**

```
bl skill remove --name <all|name,...>
```

参数

类型

必填

说明

`--name <all|name,...>`

string

是

要移除的 Skill：all 或以逗号分隔的 Skill 名称

**示例**：移除本地指定名称的技能

```
bl skill remove --name spark-video
```
