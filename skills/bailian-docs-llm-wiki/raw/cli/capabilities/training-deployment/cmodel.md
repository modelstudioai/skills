# 模型导入

阿里云百炼 CLI 从 OSS 导入自定义模型、跟踪导入任务并管理导入模型的命令速查。

`bl cmodel` 从 OSS 导入自定义模型，查询可导入的基础模型，跟踪导入任务，并查询或删除已导入模型。

**说明**模型导入 API 目前仅在北京地域开放。导入命令固定调用北京地域的公共 DashScope Endpoint，不使用 Profile 的 Base URL；业务空间 API Key 仍可用于鉴权。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl cmodel import --help`。删除已导入模型是高危操作，未追加 `--yes` 时会阻断执行（退出码 7）。本文命令明细以 bl 2.8.0 为基准核实。

## 快速开始

```
bl cmodel base-models
bl cmodel import --base-model qwen3-32b --weight-type lora --bucket my-model-bucket --object-key models/qwen3-32b-lora/
bl cmodel watch --job-id <job-id> --follow
bl cmodel list
```

## 导入模型

### bl cmodel base-models

列出可导入为自定义模型的基础模型。需要控制台登录。

**语法**

```
bl cmodel base-models
```

该命令仅支持全局参数和控制台参数。

**示例**：列出北京地域可导入的基础模型

```
bl cmodel base-models --console-region cn-beijing
```

-   列表由控制台 API 动态返回，可能随版本变化。
-   导入目前仅在北京地域开放。

### bl cmodel import

从 OSS 导入自定义模型，创建导入任务。需要 API Key 鉴权。

**语法**

```
bl cmodel import --base-model <model> --weight-type <lora|full> --bucket <bucket> --object-key <dir/> [--display-name <name>]
```

参数

类型

必填

说明

`--base-model <model>`

string

是

调优使用的基础模型 ID，例如 qwen3-32b

`--weight-type <lora|full>`

string

是

调优权重类型：lora 或 full

`--bucket <bucket>`

string

是

存放模型文件的 OSS Bucket

`--object-key <dir/>`

string

是

模型文件所在的 OSS 目录前缀，必须以 / 结尾且不能是 Bucket 根目录

`--display-name <name>`

string

否

显示名称，最长 50 个字符

**示例**：导入 LoRA 模型

```
bl cmodel import --base-model qwen3-32b --weight-type lora --bucket my-model-bucket --object-key models/qwen3-32b-lora/
```

**示例**：指定显示名称

```
bl cmodel import --base-model qwen3-32b --weight-type lora --bucket my-model-bucket --object-key models/qwen3-32b-lora/ --display-name my-lora
```

-   提交后使用 `cmodel watch --job-id` 跟踪任务，使用 `cmodel get` 或 `cmodel list` 查看详情。
-   Bucket 需要带有 `bailian-datahub-access=read` 标签，不能使用归档、冷归档、深度冷归档存储或 SSE-KMS。目录中需要包含平台要求的模型文件，例如 `adapter_model.safetensors`、`adapter_config.json`、`config.json`。
-   当前产品版本支持导入 LoRA 模型，提交 `full` 可能被服务端拒绝。API 契约保留 `lora` 和 `full` 两个值，CLI 不会隐藏 `full`。
-   有可用的控制台会话时，提交前会用控制台支持的基础模型列表校验：把模型 ID 归一为目录中的 `model` 值，并按模型的 `supportTrainTypes` 校验权重类型（lora 需要 efficient\_sft，full 需要 sft）。不支持的组合直接返回用法错误。控制台会话缺失或过期时跳过校验并给出警告，以导入 API 的最终结果为准。

### bl cmodel get

查看自定义模型导入任务详情。需要 API Key 鉴权。

**语法**

```
bl cmodel get --job-id <id>
```

参数

类型

必填

说明

`--job-id <id>`

string

是

`cmodel import` 返回的导入任务 ID

**示例**：查看导入任务详情

```
bl cmodel get --job-id 937b-xxxx --output json
```

-   失败任务会保留服务端返回的 `error_code`，CLI 不做翻译。

### bl cmodel list

分页列出已导入的自定义模型。需要 API Key 鉴权。

**语法**

```
bl cmodel list [--page <n>] [--page-size <n>] [--status <status>] [--model-name <name>]
```

参数

类型

必填

说明

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页条数（默认：10，最大 100）

`--status <PENDING|RUNNING|SUCCESSED|FAILED>`

string

否

按状态筛选（服务端筛选）

`--model-name <name>`

string

否

按服务端生成的模型标识精确匹配（服务端筛选）

**示例**：查看运行中的导入任务

```
bl cmodel list --status RUNNING
```

-   `--status` 和 `--model-name` 在全部结果上做服务端筛选，不是当前页的本地筛选。
-   失败条目包含服务端返回的 `error_code`。

### bl cmodel watch

查询导入任务状态。默认只查询一次，传入 `--follow` 后轮询到终态。需要 API Key 鉴权。

**语法**

```
bl cmodel watch --job-id <id> [--follow] [--interval <sec>] [--poll-timeout <sec>]
```

参数

类型

必填

说明

`--job-id <id>`

string

是

`cmodel import` 返回的导入任务 ID

`--follow`

switch

否

阻塞轮询直到终态。不传时只查询一次并立即返回

`--interval <sec>`

number

否

使用 --follow 时的轮询间隔（默认：10，最小 1）；不传 --follow 时忽略

`--poll-timeout <sec>`

number

否

使用 --follow 时的总轮询时间（默认：不限）；不传 --follow 时忽略

**示例**：查询一次状态

```
bl cmodel watch --job-id 937b-xxxx
```

**示例**：轮询到任务结束

```
bl cmodel watch --job-id 937b-xxxx --follow --interval 5 --poll-timeout 3600
```

-   终态为 `SUCCESSED` 和 `FAILED`。未知的服务端状态原样展示，并按非终态处理。
-   终态为 `FAILED` 时返回非零退出码，保留服务端 `error_code`。`SUCCESSED` 和仍在运行的状态返回 0。
-   使用 `--follow` 超过 `--poll-timeout` 时返回超时错误。

### bl cmodel delete

删除自定义模型及其百炼侧导入记录。需要 API Key 鉴权。

**语法**

```
bl cmodel delete --job-id <id> [--yes]
```

参数

类型

必填

说明

`--job-id <id>`

string

是

`cmodel import` 返回的导入任务 ID

`--yes`

switch

否

确认高危操作

**示例**：删除已导入模型

```
bl cmodel delete --job-id 937b-xxxx
```

**警告**删除会永久移除百炼侧导入记录和已导入的模型副本，无法恢复。OSS 源文件不会被修改。只有 `SUCCESSED` 或 `FAILED` 的任务可以删除；删除 `RUNNING` 任务会被服务端拒绝（OperationDenied）。

-   预览删除操作时使用 `--dry-run`。
-   确认操作范围后，才可追加 `--yes` 执行。
