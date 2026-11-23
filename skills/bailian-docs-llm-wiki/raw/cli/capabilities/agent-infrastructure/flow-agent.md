# Flow Agent

阿里云百炼 CLI 管理智能体应用与工作流的命令速查。

在终端管理阿里云百炼上的智能体应用与工作流：创建、查询、更新、发布、删除、复制，以及管理工作流画布。

**说明**应用管理相关能力目前仅对中国站（aliyun.com）账号开放。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl flow-agent create --help`。本文命令明细以 bl 2.10.0 为基准核实。

在各功能页也可查看对应用法，见[调用智能体应用](raw/_short/call-single-agent-application-7bb88312c0915edf.md)。

## 命令速查

### bl flow-agent call

调用百炼应用（智能体或工作流）。需要 API Key 鉴权。

**语法**

```
bl flow-agent call --app-id <id> --prompt <text> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--prompt <text>`

string

是

输入提示词文本

`--image <url>`

array

否

传给应用的图片 URL（可重复）

`--file-id <id>`

array

否

已上传的文件 ID（可重复）

`--session-id <id>`

string

否

多轮对话的 Session ID

`--stream`

switch

否

流式输出响应（TTY 中默认开启）

`--pipeline-ids <ids>`

string

否

知识库 Pipeline ID（以逗号分隔）

`--memory-id <id>`

string

否

长期记忆使用的 Memory ID

`--biz-params <json>`

string

否

业务参数 JSON（工作流变量）

`--has-thoughts`

switch

否

显示智能体思考过程

**示例**：调用指定应用并输入提示词

```
bl flow-agent call --app-id abc123 --prompt "你好"
```

### bl flow-agent list

列出百炼应用。需要 Console 鉴权。

**语法**

```
bl flow-agent list [flags]
```

参数

类型

必填

说明

`--name <name>`

string

否

按应用名称筛选（关键词搜索）

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页结果数（默认：30）

`--type <agent|workflow>`

string

否

应用类型：agent（默认）、workflow

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：按名称筛选并列出应用

```
bl flow-agent list --name 客户服务
```

**示例**：列出工作流

```
bl flow-agent list --type workflow
```

### bl flow-agent get

获取百炼应用详情（智能体或工作流）。需要 Console 鉴权。

**语法**

```
bl flow-agent get --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--type <agent|workflow>`

string

否

应用类型：agent（默认）、workflow

`--scope <draft|publish>`

string

否

数据范围：draft（默认）、publish

`--agent-version <n>`

number

否

智能体版本号（仅智能体；默认隐含已发布范围）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：获取应用详情

```
bl flow-agent get --app-id abc123
```

### bl flow-agent create

创建百炼应用（智能体或工作流）。需要 Console 鉴权。

**语法**

```
bl flow-agent create --name <name> [flags]
```

参数

类型

必填

说明

`--name <name>`

string

是

应用名称

`--type <agent|workflow>`

string

否

应用类型：agent（默认）、workflow

`--description <text>`

string

否

应用描述

`--icon <key>`

string

否

应用图标键

`--model <model>`

string

否

智能体模型 ID（默认自动选择；仅智能体）

`--config-json <json>`

string

否

配置 JSON 字符串（与 `--config-file` 互斥）

`--config-file <path>`

string

否

配置 JSON 文件路径（与 `--config-json` 互斥）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：创建智能体应用

```
bl flow-agent create --name "客服助手" --model qwen3-max --description "售后机器人"
```

**示例**：创建工作流应用

```
bl flow-agent create --name "订单流程" --type workflow
```

-   智能体创建使用 app-control 2.0 API，默认配置为 model=auto、dialog\_round=3。`--config-json` / `--config-file` 浅合并到默认配置之上；`--model` 覆盖 config.model。
-   工作流创建时生成空白草稿画布；使用 `flow-agent workflow save` 编辑，使用 `flow-agent workflow publish` 发布。

### bl flow-agent update

更新百炼应用（智能体配置或工作流元数据）。需要 Console 鉴权。

**语法**

```
bl flow-agent update --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--type <agent|workflow>`

string

否

应用类型：agent（默认）、workflow

`--name <name>`

string

否

新应用名称

`--description <text>`

string

否

新应用描述

`--icon <key>`

string

否

新应用图标键

`--model <model>`

string

否

智能体模型 ID（仅智能体；设置 config.model）

`--instructions <text>`

string

否

智能体指令（仅智能体；设置 config.instruction）

`--config-json <json>`

string

否

配置 JSON 字符串（与 `--config-file` 互斥）

`--config-file <path>`

string

否

配置 JSON 文件路径（与 `--config-json` 互斥）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：更新智能体模型和指令

```
bl flow-agent update --app-id abc123 --model qwen3-max --instructions "你是一个有帮助的助手"
```

-   先读取当前草稿，再按顺序合并：当前配置 → `--config-json` / `--config-file`（浅合并）→ `--model` / `--instructions`。仅发送变更字段。即使 `--dry-run` 也需要控制台令牌（只读规划）。
-   智能体更新使用 app-control 2.0。工作流更新仅修改元数据（名称/描述/图标）；编辑画布请使用 `flow-agent workflow save`。

### bl flow-agent publish

发布百炼智能体应用。需要 Console 鉴权。

**语法**

```
bl flow-agent publish --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--description <text>`

string

否

版本描述

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：发布智能体应用

```
bl flow-agent publish --app-id abc123 --description "Release v2"
```

-   通过 app-control 2.0 发布当前智能体草稿。发布工作流请使用 `flow-agent workflow publish`。

### bl flow-agent delete

删除百炼应用（智能体或工作流）。需要 Console 鉴权。

**语法**

```
bl flow-agent delete --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--yes`

switch

否

确认执行此高风险操作

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**警告**该操作会永久删除应用及其配置，且无法撤销。执行前请通过 `flow-agent list` 或 `flow-agent get` 确认应用 ID。

**示例**：删除应用

```
bl flow-agent delete --app-id abc123 --yes
```

### bl flow-agent copy

复制百炼应用（智能体或工作流）。需要 Console 鉴权。

**语法**

```
bl flow-agent copy --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：复制应用

```
bl flow-agent copy --app-id abc123
```

### bl flow-agent versions

列出百炼应用的已发布版本。需要 Console 鉴权。

**语法**

```
bl flow-agent versions --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--type <agent|workflow>`

string

否

应用类型：agent（默认）、workflow

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：列出应用的已发布版本

```
bl flow-agent versions --app-id abc123
```

## 工作流画布管理

### bl flow-agent workflow get

获取工作流画布（草稿或已发布版本）。需要 Console 鉴权。

**语法**

```
bl flow-agent workflow get --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--flow-version <version>`

string

否

要读取的已发布版本（默认：当前草稿）

`--scope <draft|publish>`

string

否

数据范围：draft（默认）、publish

`--output-file <path>`

string

否

将画布配置 JSON 写入此文件（覆盖）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：获取当前草稿画布

```
bl flow-agent workflow get --app-id abc123
```

**示例**：导出画布到文件

```
bl flow-agent workflow get --app-id abc123 --output-file ./canvas.json
```

-   未指定 `--flow-version` 时读取当前草稿画布（config + version）。指定 `--flow-version` 时读取已发布版本（scope 默认为 publish）。画布配置为 JSON 字符串；`--output-file` 写入解析并格式化后的内容。

### bl flow-agent workflow save

保存工作流画布（替换当前草稿）。需要 Console 鉴权。

**语法**

```
bl flow-agent workflow save --app-id <id> (--config-json <json> | --config-file <path>) [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--config-json <json>`

string

否

配置 JSON 字符串（与 `--config-file` 互斥）

`--config-file <path>`

string

否

配置 JSON 文件路径（与 `--config-json` 互斥）

`--flow-version <version>`

string

否

期望的当前版本号，用于乐观锁（默认：从服务端读取）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：从文件保存工作流画布

```
bl flow-agent workflow save --app-id abc123 --config-file ./canvas.json
```

-   画布配置为整幅替换草稿。建议先用 `flow-agent workflow get --output-file` 导出，编辑后再保存。未指定 `--flow-version` 时从服务端读取当前版本（需要控制台令牌，`--dry-run` 同样需要）。

### bl flow-agent workflow publish

发布工作流（发布当前草稿画布）。需要 Console 鉴权。

**语法**

```
bl flow-agent workflow publish --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--description <text>`

string

否

版本描述

`--trigger-list <json>`

string

否

触发器列表 JSON 数组（默认：从当前草稿读取）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：发布工作流

```
bl flow-agent workflow publish --app-id abc123 --description "Release v2"
```

-   读取当前草稿画布和版本号后发布。触发器取自草稿（applicationConfigDTO.triggerList，回退到 Start 节点），除非指定 `--trigger-list`；'none' 类型的触发器会被丢弃。即使 `--dry-run` 也需要控制台令牌（只读规划）。

### bl flow-agent workflow export

将工作流导出为 DSL Schema（下载链接）。需要 Console 鉴权。

**语法**

```
bl flow-agent workflow export --app-id <id> [flags]
```

参数

类型

必填

说明

`--app-id <id>`

string

是

应用 ID

`--flow-version <version>`

string

否

要导出的已发布版本（默认：当前草稿）

`--output-file <path>`

string

否

将 DSL 下载到此文件，而不是打印 URL

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：导出工作流 DSL

```
bl flow-agent workflow export --app-id abc123 --output-file ./flow.dsl
```

## 已废弃命令

**警告**以下命令已废弃，将在未来版本移除。请改用对应的 `bl flow-agent` 命令。

已废弃命令

替代命令

`bl app call`

`bl flow-agent call`

`bl app list`

`bl flow-agent list`
