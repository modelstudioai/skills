# 批量推理

阿里云百炼 CLI 创建、跟踪和下载异步批量推理任务的命令速查。

`bl batch` 把 CSV 转换为 Batch JSONL，创建 Chat 或 Embedding 异步批量任务，跟踪进度，取消任务，并下载结果与错误文件。异步文件批量任务与同步单请求 `bl text chat --batch` 分开使用。

> **说明**
>
> `batch convert` 在本地转换，无需鉴权。创建、查询、取消和下载任务需要模型 API Key。Batch 的可用范围和限额取决于模型与服务。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl batch create --help`。本文命令明细以 bl 2.8.0 为基准核实。

<a id="快速开始"></a>

## 快速开始

<a id="code-block"></a>

```bash
bl batch convert --file input.csv --model qwen-plus --output-file input.jsonl
bl batch create --file input.jsonl
bl batch get --batch-id <batch-id> --follow
bl batch download --batch-id <batch-id> --csv
```

<a id="任务管理"></a>

## 任务管理

<a id="bl-batch-convert"></a>

### bl batch convert

在本地把 UTF-8 CSV 转换为 Batch JSONL。无需鉴权。

**语法**

<a id="code-block-2"></a>

```bash
bl batch convert --file <csv> --model <model> --output-file <jsonl> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--file <csv>` | string | 是 | 带表头的 UTF-8 CSV 文件 |
| `--output-file <jsonl>` | string | 是 | 本地 JSONL 输出路径 |
| `--model <model>` | string | 是 | 为每条记录指定的模型 |
| `--id-column <name>` | string | 否 | ID 列名（默认：custom\_id） |
| `--input-column <name>` | string | 否 | 输入列名（默认：content） |
| `--system <text>` | string | 否 | 共用的系统提示词（仅 Chat） |
| `--body-file <json>` | string | 否 | 共用的请求体参数，不包含 model、messages 或 input |
| `--endpoint </v1/chat/completions\|/v1/embeddings\|/v1/chat/ds-test>` | string | 否 | Batch Endpoint，可从本地 JSONL 推断 |
| `--force` | switch | 否 | 覆盖已存在的输出文件（按文件原子替换） |

**示例**：把 CSV 转换为 Chat JSONL

<a id="code-block-3"></a>

```bash
bl batch convert --file input.csv --model qwen-plus --output-file input.jsonl
```

**示例**：把 CSV 转换为 Embedding JSONL

<a id="code-block-4"></a>

```bash
bl batch convert --file input.csv --model text-embedding-v4 --endpoint /v1/embeddings --output-file vectors.jsonl
```

-   仅支持文本与 Embedding 的字段映射。多模态或多轮输入请直接编写 JSONL。
-   ID 始终按字符串处理。用电子表格软件导入 CSV 时，把 ID 列设为文本，避免丢失前导零。
-   dry-run 不调用业务 API，也不写入业务文件。

<a id="bl-batch-create"></a>

### bl batch create

上传或引用输入文件，创建异步 Batch 任务。需要 API Key 鉴权。

**语法**

<a id="code-block-5"></a>

```bash
bl batch create (--file <jsonl> | --input-file-id <source> --endpoint <path>) [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--file <jsonl>` | string | 否 | 本地 Batch JSONL，与 --input-file-id 互斥 |
| `--input-file-id <source>` | string | 否 | 文件 ID、OSS HTTPS URL 或 oss:region:bucket/path |
| `--completion-window <24h\|7d>` | string | 否 | 完成窗口，24–336 小时（默认：24h） |
| `--name <text>` | string | 否 | 任务名称，最长 100 个字符 |
| `--description <text>` | string | 否 | 任务描述，最长 200 个字符 |
| `--callback-url <url>` | string | 否 | 完成回调，目前仅北京地域有说明 |
| `--metadata <KEY=VALUE>` | array | 否 | 自定义任务元数据（可重复） |
| `--endpoint </v1/chat/completions\|/v1/embeddings\|/v1/chat/ds-test>` | string | 否 | Batch Endpoint，可从本地 JSONL 推断 |

**示例**：预览创建任务

<a id="code-block-6"></a>

```bash
bl batch create --file input.jsonl --name eval-1 --dry-run
```

**示例**：引用文件 ID 创建任务

<a id="code-block-7"></a>

```bash
bl batch create --input-file-id file-batch-xxx --endpoint /v1/chat/completions
```

**示例**：引用 OSS 路径并设置 7 天完成窗口

<a id="code-block-8"></a>

```bash
bl batch create --input-file-id oss:cn-beijing:my-bucket/input.jsonl --endpoint /v1/chat/completions --completion-window 7d
```

Chat JSONL 示例：

<a id="code-block-9"></a>

```json
{"custom_id":"req-001","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-plus","messages":[{"role":"user","content":"Introduce yourself"}]}}
```

Embedding JSONL 示例：

<a id="code-block-10"></a>

```json
{"custom_id":"req-001","method":"POST","url":"/v1/embeddings","body":{"model":"text-embedding-v4","input":"Introduce yourself","encoding_format":"float"}}
```

-   本地输入上限：50,000 条请求、500 MiB、单行 6 MiB。单行超过 1 MiB 时给出警告。
-   `batch-test-model` 限制为 100 条请求、1 MiB。
-   远程引用需要授权且 URL 在有效期内，CLI 不会下载文件做校验。
-   创建成功后返回任务 ID，不等待任务完成。失败时不会自动重放 POST，也不会清理已上传文件。

<a id="bl-batch-get"></a>

### bl batch get

查询 Batch 任务详情，可跟踪进度。需要 API Key 鉴权。

**语法**

<a id="code-block-11"></a>

```bash
bl batch get --batch-id <id> [--follow] [--interval <seconds>] [--poll-timeout <seconds>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--batch-id <id>` | string | 是 | Batch 任务 ID |
| `--follow` | switch | 否 | 轮询直到终态（Ctrl-C 只停止本地轮询） |
| `--interval <seconds>` | number | 否 | 查询间隔，最小 60 秒（默认：65 秒；仅 --follow） |
| `--poll-timeout <seconds>` | number | 否 | 总轮询时间预算（默认：不限；仅 --follow） |

**示例**：跟踪任务直到结束

<a id="code-block-12"></a>

```bash
bl batch get --batch-id batch_xxx --follow
```

-   单次查询成功后退出码为 0，与任务状态无关。
-   `--follow` 的退出码：completed 为 0（可能包含失败行），failed、expired 或 cancelled 为 1，客户端超时为 5，Ctrl-C 为 130。
-   `finalizing` 和 `cancelling` 都不是终态。
-   进度写入 stderr，最终结果写入 stdout。
-   只有传输错误、超时或 HTTP 429/5xx 会重试，最多 3 次。
-   服务端保留结果的时间有限，任务完成后尽快下载。

<a id="bl-batch-list"></a>

### bl batch list

分页列出 Batch 任务。需要 API Key 鉴权。

**语法**

<a id="code-block-13"></a>

```bash
bl batch list [filters] [--after <id>] [--limit <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--limit <n>` | number | 否 | 每页条数：1–100（默认：20） |
| `--after <id>` | string | 否 | 上一页返回的 last\_id |
| `--name <text>` | string | 否 | 按任务名称筛选 |
| `--input-file-id <id>` | array | 否 | 按输入文件筛选（可重复，最多 20 个） |
| `--status <status>` | array | 否 | 按任务状态筛选（可重复）：validating、in\_progress、finalizing、completed、failed、expired、cancelling、cancelled |
| `--created-after <yyyyMMddHHmmss>` | string | 否 | 创建时间晚于此 API 时间戳 |
| `--created-before <yyyyMMddHHmmss>` | string | 否 | 创建时间早于此 API 时间戳 |

**示例**：查看已完成和失败的任务

<a id="code-block-14"></a>

```bash
bl batch list --status completed --status failed --limit 20
```

-   返回 `data`、`last_id` 和 `has_more`。下一页把 `last_id` 传给 `--after`。
-   API 时间戳不做时区转换。

<a id="bl-batch-cancel"></a>

### bl batch cancel

请求取消 Batch 任务。需要 API Key 鉴权。

**语法**

<a id="code-block-15"></a>

```bash
bl batch cancel --batch-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--batch-id <id>` | string | 是 | Batch 任务 ID |

**示例**：请求取消任务

<a id="code-block-16"></a>

```bash
bl batch cancel --batch-id batch_xxx
```

-   取消请求被接受后可能返回 `cancelling`，不代表已经取消。用 `batch get --follow` 确认。
-   已执行的请求仍会计费，文件不会删除。

<a id="bl-batch-download"></a>

### bl batch download

下载原始结果或错误文件，可选导出 CSV。需要 API Key 鉴权。

**语法**

<a id="code-block-17"></a>

```bash
bl batch download --batch-id <id> [--out-dir <path>] [--csv] [--force]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--batch-id <id>` | string | 是 | Batch 任务 ID |
| `--out-dir <path>` | string | 否 | 输出目录（默认：`./batch-results/<batch-id>/`） |
| `--csv` | switch | 否 | 同时生成 result.csv（有损展示投影） |
| `--force` | switch | 否 | 覆盖已存在的输出文件（按文件原子替换） |

**示例**：下载结果并导出 CSV

<a id="code-block-18"></a>

```bash
bl batch download --batch-id batch_xxx --out-dir ./out --csv
```

-   JSONL 是保真结果。CSV 只读取 `choices[0].message.content`、Embedding 数据、`response.request_id`、`status_code`、用量及 `error.code`、`error.message`。
-   CSV 不包含工具调用和额外候选结果，并把类似公式的文本按文本处理。导入 ID 时选择文本类型以保留前导零。
-   不保证保持原始输入顺序。
-   按文件原子发布，不按目录原子发布。CSV 生成失败时保留已下载的 JSONL；用 `--force` 重跑恢复。

<a id="相关命令"></a>

## 相关命令

同步单请求使用 `bl text chat --batch`，不创建异步任务。见[文本对话与全模态](text-chat.md)。
