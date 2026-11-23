# ParseX 文档解析

阿里云百炼 CLI 提交 ParseX 文档与音视频解析、字段抽取并查询结果的命令速查。

`bl parsex` 提交文档或音视频解析任务，按 JSON Schema 从文档或已有解析结果中抽取字段，并查询解析与抽取结果。

**说明**ParseX 使用业务空间专属 API 和普通 API Key。通过 `--workspace-id`、`BAILIAN_WORKSPACE_ID` 或配置项 `workspace_id` 指定业务空间。服务可用性取决于业务空间和开通状态。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl parsex parse submit --help`。提交类命令立即返回 `data.biz_id`，不会等待任务完成；使用对应的 `result --follow` 等待结果。本文命令明细以 bl 2.8.0 为基准核实。

在各功能页也可查看对应用法，见 [使用 CLI](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/cli.md)。

## 快速开始

```
bl parsex parse submit --workspace-id <workspace-id> --file-url "https://example.com/document.pdf" --file-name document.pdf --output-file-format markdown --output json
bl parsex parse result --workspace-id <workspace-id> --biz-id <parse-biz-id> --follow --output json
bl parsex extract submit --workspace-id <workspace-id> --parsed-file-biz-id <parse-biz-id> --schema-file schema.json --output json
bl parsex extract result --workspace-id <workspace-id> --biz-id <extract-biz-id> --follow --output json
```

## 文档解析

### bl parsex parse submit

提交 ParseX 文档或媒体解析任务。需要 API Key 鉴权。

**语法**

```
bl parsex parse submit --file-url <url> [--workspace-id <id>] [flags]
```

参数

类型

必填

说明

`--file-url <url>`

string

是

可访问的源文件 URL

`--file-name <name>`

string

否

文件名，与 --file-name-extension 二选一

`--file-name-extension <extension>`

string

否

文件扩展名，例如 pdf

`--config-id <id>`

string

否

已保存的 ParseX 配置 ID

`--processing-file <path>`

string

否

API processing 字段的 JSON 对象文件

`--oss-config-file <path>`

string

否

OSS 凭证 JSON 文件；文件中还需包含 bucket 和 endpoint

`--output-file-format <markdown>`

array

否

结果文件格式（markdown）

`--layout-table-format <markdown|html>`

string

否

Markdown 结果中的表格格式

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--api-key <key>`

string

否

API Key

`--base-url <url>`

string

否

API Base URL

**示例**：提交文档解析

```
bl parsex parse submit --file-url "https://example.com/document.pdf" --file-name document.pdf --workspace-id ws-example
```

**示例**：使用处理配置并指定 Markdown 输出

```
bl parsex parse submit --file-url "https://example.com/document.pdf" --processing-file processing.json --output-file-format markdown --output json
```

**示例**：预览提交参数

```
bl parsex parse submit --file-url "https://example.com/video.mp4" --config-id config-example --dry-run
```

-   输入必须是可访问的 HTTP(S) URL，包括带签名的 OSS URL。本接口不支持上传本地文件。
-   内联的处理配置优先于 `--config-id`。
-   处理配置示例：`{"doc_processing_config":{"page_index":"1-10","layout_position":true}}`。媒体使用 `media_processing_config`，支持说话人分离、摘要和抽帧。
-   dry-run 不发送业务请求，并脱敏 OSS 凭证和 URL 查询参数。

### bl parsex parse result

查询 ParseX 解析状态、结果或结果分片。需要 API Key 鉴权。

**语法**

```
bl parsex parse result --biz-id <id> [--follow] [flags]
```

参数

类型

必填

说明

`--biz-id <id>`

string

是

提交命令返回的 biz\_id

`--follow`

switch

否

轮询直到成功或失败（Ctrl-C 只停止本地轮询）

`--interval <seconds>`

number

否

轮询间隔，1–3600 秒（默认：2；仅 --follow）

`--poll-timeout <seconds>`

number

否

总轮询截止时间，1–86400 秒（默认：600；仅 --follow）

`--step-start <n>`

number

否

版式或媒体分片的起始偏移（服务端默认：0）

`--step-size <n>`

number

否

分片大小（服务端默认：0）

`--oss-config-file <path>`

string

否

OSS 凭证 JSON 文件

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：查询解析结果

```
bl parsex parse result --biz-id biz-example --workspace-id ws-example
```

**示例**：等待解析完成并输出 JSON

```
bl parsex parse result --biz-id biz-example --follow --poll-timeout 600 --output json
```

-   单次查询保留完整 API 响应，任务失败也返回退出码 0。
-   `--follow` 在 stdout 输出一次终态响应，进度写入 stderr；失败退出码 1，超时 5，Ctrl-C 130。
-   使用同一个 `biz_id` 可以恢复查询；本地停止不会取消远端任务。
-   `ResultNotReady` 只在 `--follow` 时继续轮询。
-   `--timeout` 控制单次 HTTP 请求，`--poll-timeout` 控制整个轮询过程。
-   `--follow` 只等待当前分片所在任务完成，不会收集全部分片。需要继续获取版式或媒体分段时，自行递增 `--step-start`。
-   输出文件 URL 可能在全部分片获取完成后才出现。

## 字段抽取

### bl parsex extract submit

提交 ParseX 结构化字段抽取。需要 API Key 鉴权。

**语法**

```
bl parsex extract submit (--file-url <url> | --parsed-file-biz-id <id>) (--schema-file <path> | --processing-file <path> | --config-id <id>) [flags]
```

参数

类型

必填

说明

`--file-url <url>`

string

否

可访问的源文件 URL

`--file-name <name>`

string

否

文件名，与 --file-name-extension 二选一

`--file-name-extension <extension>`

string

否

文件扩展名，例如 pdf

`--config-id <id>`

string

否

已保存的 ParseX 配置 ID

`--processing-file <path>`

string

否

API processing 字段的 JSON 对象文件

`--parsed-file-biz-id <id>`

string

否

复用已完成的解析任务，替代 --file-url

`--schema-file <path>`

string

否

JSON Schema 对象文件，替代 --processing-file

`--user-prompt <text>`

string

否

抽取指令，与 --schema-file 配合使用

`--citation-required <boolean>`

boolean

否

是否返回原文引用（与 --schema-file 配合；服务端默认：true）

`--allow-inference <boolean>`

boolean

否

是否允许推理（与 --schema-file 配合；服务端默认：false）

`--oss-config-file <path>`

string

否

OSS 凭证 JSON 文件；文件中还需包含 bucket 和 endpoint

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：从文档抽取字段

```
bl parsex extract submit --file-url "https://example.com/contract.pdf" --schema-file schema.json --workspace-id ws-example
```

**示例**：复用解析结果并返回引用

```
bl parsex extract submit --parsed-file-biz-id parse-example --schema-file schema.json --citation-required true --allow-inference false
```

**示例**：使用已保存的配置

```
bl parsex extract submit --file-url "https://example.com/contract.pdf" --config-id config-example --output json
```

-   提交后返回 `data.biz_id`，不等待抽取完成。使用 `extract result --follow` 查询。
-   Schema 作为对象发送，不要写成 JSON 字符串。示例：`{"type":"object","properties":{"title":{"type":"string"}}}`。
-   抽取不支持音视频。复用的解析结果仍需在服务端保留期内。
-   与解析命令相同，输入必须是可访问的 HTTP(S) URL，dry-run 不发送业务请求。

### bl parsex extract result

查询 ParseX 抽取状态、字段和引用。需要 API Key 鉴权。

**语法**

```
bl parsex extract result --biz-id <id> [--follow] [flags]
```

参数、轮询行为和退出码与 `bl parsex parse result` 相同（`--step-start` 和 `--step-size` 除外）。

**示例**：查询抽取结果

```
bl parsex extract result --biz-id biz-example --workspace-id ws-example
```

**示例**：等待抽取完成并输出 JSON

```
bl parsex extract result --biz-id biz-example --follow --poll-timeout 600 --output json
```

-   单次查询保留完整 API 响应，任务失败也返回退出码 0。
-   `--follow` 等待终态；失败退出码 1，超时 5，Ctrl-C 130。

## 相关说明

-   使用 `--base-url` 覆盖 Endpoint 源站时，CLI 会丢弃其中的路径。`cn-beijing.pre-maas.aliyuncs.com` 的业务空间主机使用 `pre-parse-x`。
-   服务端保留解析结果的时间有限，需要复用时及时抽取。
