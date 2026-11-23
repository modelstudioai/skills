# RAG

阿里云百炼 CLI 管理知识库、文档、分片与检索/问答服务的命令速查。

在终端调用阿里云百炼知识库全部能力：检索/问答服务调用、知识库生命周期管理、文档与分片管理、分类与数据合集管理。

**说明**知识库相关能力目前仅对中国站（aliyun.com）账号开放。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl knowledge search --help`。删除类高危操作未显式追加 `--yes` 时会阻断执行（退出码 7）；如需预览，改用 `--dry-run`。除下文注明的 2.5.0 迁移变更外，本文命令明细以 bl 2.8.0 为基准核实。

在各功能页也可查看对应用法，见 [RAG 知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。

## 检索与问答

`search` / `chat` 通过 `--agent-id` 调用已发布的检索/问答服务，具体检索策略（多路召回、排序、重排序等）由服务端配置决定。

### bl knowledge search

搜索百炼知识库（RAG 语义检索）。需要 API Key 鉴权。

**语法**

```
bl knowledge search --agent-id <id> (--query <text> | --image <url>) [flags]
```

参数

类型

必填

说明

`--query <text>`

string

否

搜索查询文本，与 --image 至少提供一个

`--agent-id <id>`

string

是

检索服务 ID（可在控制台知识库检索页面查看）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--agent-version <version>`

string

否

要调用的服务版本：beta（用于调试的草稿）或已发布版本号；默认使用最新发布版本

`--image <url>`

array

否

多模态检索使用的图片 URL（可重复），支持纯图片检索

`--kb-search-configs-file <path>`

string

否

包含知识库 ID 和在线 search\_filters 的 JSON 数组文件

**示例**：搜索百炼知识库中的 RAG 语义信息

```
bl knowledge search --query "什么是 RAG？" --agent-id aid-xxx --workspace-id ws-xxx
```

-   检索范围与策略（多索引权重、路由、重排序等）由 agent\_id 服务配置决定。agent\_id 必填，query 和 image 至少提供一个。
-   在线检索过滤配置通过 `--kb-search-configs-file` 传入，文件中按知识库指定 `search_filters`。
-   鉴权：使用 DashScope API Key（Bearer Token）。可在控制台 API Key 页面获取。
-   `--workspace-id` 可通过 BAILIAN\_WORKSPACE\_ID 环境变量或 `kscli config set workspace_id <id>` 设置。
-   `--agent-version beta` 会调用尚未部署的草稿配置，便于发布前调试。
-   JSON 输出保留接口返回的 `request_id`、`data.total`、`data.cost_time` 和 `data.nodes`；每个节点包含 `score`、`text` 和 `metadata`（标题、文档 ID、链接、页码、媒体地址等）。
-   文本模式按节点输出得分、文本和媒体摘要。

### bl knowledge chat

与百炼知识库对话（支持流式输出的 RAG 问答）。需要 API Key 鉴权。

**语法**

```
bl knowledge chat --message <text> --agent-id <id> [flags]
```

参数

类型

必填

说明

`--message <text>`

array

否

消息文本（可重复）。支持使用 role:content 前缀指定角色（例如 user:hello），默认为 user。遵循 OpenAI 消息格式

`--agent-id <id>`

string

是

问答服务 ID（可在控制台知识库问答页面查看）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--agent-version <version>`

string

否

要调用的服务版本：beta（用于调试的草稿）或已发布版本号；默认使用最新发布版本

`--image <url>`

array

否

图片 URL（可重复）。将作为多模态内容附加到最后一条用户消息

`--messages-file <path>`

string

否

完整的 messages JSON 数组，包含工具历史（与 --message、--image 互斥）

`--enable-cache-control <true|false>`

boolean

否

显式控制上下文缓存

`--request-id <id>`

string

否

业务请求 ID

`--session-file-id <fileId>`

array

否

会话文件 ID（可重复，最多 10 个；需要服务端开启文件预处理）

**示例**：与百炼知识库进行 RAG 问答对话

```
bl knowledge chat --message "什么是 RAG？" --agent-id aid-xxx --workspace-id ws-xxx
```

-   响应以 SSE 流事件返回。事件生命周期：tool\_calling → tool\_return → plan\_start → planning → plan\_end → generation\_start → generating → generation\_end。tool\_calling → tool\_return 可能循环多次。
-   鉴权：使用 DashScope API Key（Bearer Token）。可在控制台 API Key 页面获取。
-   `--workspace-id` 可通过 BAILIAN\_WORKSPACE\_ID 环境变量或 `kscli config set workspace_id <id>` 设置。
-   多轮对话：使用 --message "user:..." 和 --message "assistant:..." 传入对话历史。
-   `--agent-version beta` 会调用尚未部署的草稿配置，便于发布前调试。
-   结构化输出把最终答案与阶段、工具、来源和用量分开保存。quiet 模式只隐藏进度和过程提示，保留最终答案及完整结果、警告和错误。
-   JSON 输出从 `answer` 读取最终答案，从 `phases`、`tools`、`docs`、`usage`、`events` 读取过程信息。原先依赖 quiet 模式提取答案的脚本，改为读取 JSON 字段。

### retrieve 迁移说明

阿里云百炼 CLI 2.5.0 已移除 `bl knowledge retrieve` 和 `kscli retrieve`。请改用 `bl knowledge search`；使用独立 Knowledge Studio CLI 时，改用 `kscli search`。

迁移时，使用绑定目标知识库的检索服务 ID 作为 `--agent-id`，不能直接填入原 `--index-id` 的值。召回、排序和重排序等策略由检索服务配置，旧检索参数不能直接照搬。调用语法与示例见上文 `bl knowledge search`，服务的创建、配置和发布见下文“检索/问答服务管理”。

## 知识库管理

### bl knowledge init

初始化知识库并验证样例检索。需要 API Key 鉴权。

**语法**

```
bl knowledge init [--name <name>] [--state-file <path>] [flags]
```

参数

类型

必填

说明

`--name <name>`

string

否

知识库名称（1–20 个字符，默认：cli-demo）

`--state-file <path>`

string

否

恢复检查点（默认：`~/.bailian/knowledge/init/<key>.json`，按 Workspace 和名称区分）

`--poll-interval <seconds>`

number

否

轮询间隔（默认：5 秒）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认创建知识库并开始计费

**示例**：预览初始化计划

```
bl knowledge init --dry-run
```

**示例**：确认后执行初始化

```
bl knowledge init --yes
```

**警告**知识库创建后即按运行时长计费，即使没有检索也会计费。标准版一次性 720 小时额度仅限新账号，由多个知识库共享，开通后 30 天内有效；模型调用另行计费。未追加 `--yes` 时会阻断执行（退出码 7）。确认操作范围后才可追加 `--yes` 执行。关闭 CLI 不会停止计费；剩余额度尚未核实，需要按返回的清理动作删除不再使用的知识库。

-   依次完成样例上传、建库、检索服务创建和首次检索验证，支持恢复和资源复用。
-   使用检索服务的 beta 草稿，不发布服务，也不创建问答服务。
-   dry-run 需要凭证并读取已有资源，但不修改资源或检查点。保留状态文件用于恢复。
-   计费规则见[知识库计费](raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。

### bl knowledge create

创建知识库并导入数据中心文件或类目。需要 API Key 鉴权。

**语法**

```
bl knowledge create --name <text> --description <text> (--doc-id <id> | --category-id <id>) [flags]
```

参数

类型

必填

说明

`--name <text>`

string

是

知识库名称（1–20 个字符，在 Workspace 中唯一）

`--description <text>`

string

是

知识库装了什么内容、给谁用，用于在 Workspace 列表中区分同类知识库（1–500 个字符）

`--doc-id <id>`

array

否

要导入的数据中心文件 ID（可重复）；不能与 --category-id 同时使用

`--category-id <id>`

array

否

导入该类目下的所有文件（可重复）；不能与 --doc-id 同时使用

`--embedding-model <name>`

string

否

Embedding 模型名称（文档知识库默认：text-embedding-v4；多媒体/视觉场景：qwen3-vl-embedding）

`--knowledge-type <document|multimedia>`

string

否

知识库类型：document 或 multimedia

`--knowledge-scene <scene>`

string

否

知识库场景，需与 --knowledge-type 一起使用

`--multimodal-embedding-model <name>`

string

否

多模态 Embedding 模型，multimedia/视觉场景下是 --embedding-model 的别名

`--chunk-size <n>`

number

否

Chunk 字符数（默认：600，建议：300–800）

`--wait`

switch

否

轮询初始导入任务直到进入终态

`--poll-interval <seconds>`

number

否

等待时的轮询间隔（默认：5）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：创建知识库并导入数据中心文件

```
bl knowledge create --name demo --description '产品文档' --doc-id file-xxx --workspace-id ws-xxx
```

-   结构和存储类型为 unstructured、BUILT\_IN。多媒体知识库使用 basic\_multimedia\_qa、qwen3-vl-embedding 和 qwen3-vl-rerank，重排序方式类似。显式指定的模型由服务端校验。
-   知识库创建后即按运行时长计费，即使没有检索也会计费。标准版一次性 720 小时额度仅限新账号，由多个知识库共享，开通后 30 天内有效；模型调用另行计费。计费规则见[知识库计费](raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
-   返回知识库 ID（pipelineId）和初始导入任务 ID（ingestionId）。
-   使用导入任务状态命令（或 --wait）跟踪初始导入。

### bl knowledge list

列出 Workspace 中的知识库。需要 API Key 鉴权。

**语法**

```
bl knowledge list [flags]
```

参数

类型

必填

说明

`--name <text>`

string

否

按知识库名称筛选（模糊匹配，1–20 个字符）

`--page-number <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每次请求的分页大小

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：列出 Workspace 中的知识库

```
bl knowledge list --workspace-id ws-xxx
```

-   鉴权：使用 DashScope API Key（Bearer Token）。
-   `--workspace-id` 可通过 BAILIAN\_WORKSPACE\_ID 环境变量或配置项 workspace\_id 设置。
-   在知识库/文档管理命令中，将返回的 ID 作为 --index-id 使用。

### bl knowledge info

查看知识库配置详情。需要 API Key 鉴权。

**语法**

```
bl knowledge info --index-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：查看知识库配置详情

```
bl knowledge info --index-id idx-xxx --workspace-id ws-xxx
```

-   索引设置不可修改；如需更改，必须重新创建知识库。

### bl knowledge update

更新知识库名称、描述或 Rerank 阈值。需要 API Key 鉴权。

**语法**

```
bl knowledge update --index-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--name <text>`

string

否

新的知识库名称（1–20 个字符）

`--description <text>`

string

否

新的知识库描述

`--rerank-min-score <score>`

number

否

Rerank 最低分数阈值，范围 0–1（低于阈值的 Chunk 会被过滤）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：确认执行更新知识库信息

```
bl knowledge update --index-id idx-xxx --description '产品文档 v2' --workspace-id ws-xxx
```

-   索引设置（Embedding 模型、Chunk 大小等）不可修改——如需更改，请重新创建知识库。

### bl knowledge delete

删除知识库及其所有文档和 Chunk。需要 API Key 鉴权。

**语法**

```
bl knowledge delete --index-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除知识库及其全部文档和 Chunk，但不会删除数据中心文件。

**示例**：确认执行删除知识库及其内容

```
bl knowledge delete --index-id idx-xxx --workspace-id ws-xxx
```

-   该操作不可撤销——知识库及所有已索引内容将被永久删除。
-   数据中心中的文件不受影响；仅删除知识库索引。

### bl knowledge stats

查看知识库存储和 QPS 监控数据。需要 API Key 鉴权。

**语法**

```
bl knowledge stats --index-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--start <time>`

string

否

范围开始时间：Unix 秒或 ISO 日期，必须是过去时间（默认：24 小时前）

`--end <time>`

string

否

范围结束时间：Unix 秒或 ISO 日期，必须是过去时间（默认：当前时间）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：查看知识库存储和 QPS 监控数据

```
bl knowledge stats --index-id idx-xxx --workspace-id ws-xxx
```

-   省略 --start/--end 时，默认查询最近 24 小时。
-   时间戳会按服务端要求归一化为 Epoch 秒。
-   监控 API 只返回历史数据，因此未来的 --start 会被拒绝，未来的 --end 会被截断为当前时间。

## 文档与文件管理

数据中心文件（file）是原始素材，导入知识库后成为文档（doc）；两者删除操作互相独立。

### bl knowledge doc upload

上传本地文件或目录到数据中心，并可选择导入知识库。需要 API Key 鉴权。

**语法**

```
bl knowledge doc upload --file <path> [flags]
```

参数

类型

必填

说明

`--file <path>`

array

是

本地文件或目录路径（可重复）。目录会递归扫描，不支持的格式将被跳过

`--index-id <id>`

string

否

文件注册后导入该知识库（所有文件共用一个任务）

`--category-id <id>`

string

否

目标数据中心类目；默认为 Workspace 的默认类目

`--tag <text>`

array

否

文件标签（可重复），应用于每个上传文件

`--category-type <UNSTRUCTURED|SESSION_FILE>`

string

否

文件类目类型；SESSION\_FILE 用于临时会话附件

`--parser <name>`

string

否

文件解析器，例如 AUTO\_SELECT 或 DOCMIND\_LLM\_VERSION\_MEDIA

`--parser-config-file <path>`

string

否

包含解析器配置的 JSON 对象文件

`--wait`

switch

否

轮询导入任务直到进入终态（需要 --index-id）

`--poll-interval <seconds>`

number

否

等待时的轮询间隔（默认：5）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：上传本地文件或目录到数据中心

```
bl knowledge doc upload --file ./a.md --workspace-id ws-xxx
```

-   处理流程：申请上传凭证 → 流式 PUT 到 OSS → 注册文件 →（传入 --index-id 时）创建导入任务。
-   音视频文件单个最大 2 GiB。传入 --index-id 时，每次调用最多处理 50 个本地媒体文件，不自动拆分。
-   未传入 --category-id 时，会自动解析 Workspace 的默认类目。
-   目录会递归扫描；node\_modules、.git 等目录会被自动跳过。
-   多个文件会依次处理；失败时，错误提示会列出已经注册成功的文件 ID。

### bl knowledge doc import

把数据中心已有文件导入指定知识库。需要 API Key 鉴权。

**语法**

```
bl knowledge doc import --index-id <id> (--doc-id <fileId> ... | --category-id <id> ...) [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

已有知识库 ID

`--doc-id <fileId>`

array

否

数据中心文件 ID（可重复）；不能与 --category-id 同时使用

`--category-id <id>`

array

否

数据中心类目 ID（可重复）；不能与 --doc-id 同时使用

`--chunk-mode <h1|h2|h3|h4|h5|length|page|regex>`

string

否

文档切片模式（不用于视频时间切片）

`--chunk-size <characters>`

number

否

文档切片大小，1–6000 个字符

`--overlap-size <characters>`

number

否

文档重叠大小，0–1024 个字符

`--separator <regex>`

string

否

regex 切片模式使用的分隔符

`--enable-headers <true|false>`

boolean

否

是否启用文档标题提取

`--wait`

switch

否

等待导入任务结束

`--poll-interval <seconds>`

number

否

轮询间隔（默认：5 秒）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：导入数据中心文件并等待完成

```
bl knowledge doc import --index-id idx-xxx --doc-id file-xxx --wait
```

**示例**：预览按类目导入

```
bl knowledge doc import --index-id idx-xxx --category-id category-xxx --dry-run
```

-   复用文件 ID，不会重新上传。
-   导入可能触发解析和索引。

### bl knowledge doc sync

把本地文档目录同步到知识库。需要 API Key 鉴权。

**语法**

```
bl knowledge doc sync --dir <path> --index-id <id> [flags]
```

参数

类型

必填

说明

`--dir <path>`

string

是

本地文档目录

`--index-id <id>`

string

是

目标知识库 ID

`--category-id <id>`

string

否

数据中心类目 ID（首次运行默认使用 Workspace 默认类目）

`--delete`

switch

否

删除本地已不存在的托管索引文档

`--sync-id <uuid>`

string

否

同步集 UUID

`--state-file <path>`

string

否

检查点路径（默认：`<dir>/.bailian/sync/<key>.json`，按知识库 ID 区分）

`--poll-interval <seconds>`

number

否

轮询间隔（默认：5 秒）

`--yes`

switch

否

确认执行此高风险操作

**示例**：预览同步计划

```
bl knowledge doc sync --dir ./docs --index-id idx-example --dry-run
```

**示例**：执行同步

```
bl knowledge doc sync --dir ./docs --index-id idx-example --yes
```

**示例**：预览删除本地已不存在的文档

```
bl knowledge doc sync --dir ./docs --index-id idx-example --delete --dry-run
```

**警告**同步可能替换或删除知识库中的托管索引文档。执行前先预览受影响的路径。替换和删除需要确认，未追加 `--yes` 时会阻断执行（退出码 7）。

-   源文件保留在本地。
-   保留状态文件，并确保同一个同步集同时只有一个写入方，包括跨 CI 机器执行时。
-   导入可能产生模型调用费用。删除文档不会停止知识库的运行时长计费。

### bl knowledge doc import-oss

从已授权的 OSS Bucket 批量导入文件到数据中心。需要 API Key 鉴权。

**语法**

```
bl knowledge doc import-oss --bucket <name> --region <id> --oss-key <key> [flags]
```

参数

类型

必填

说明

`--bucket <name>`

string

是

已授权的 OSS Bucket 名称

`--region <id>`

string

是

OSS Region ID（例如 cn-beijing）

`--oss-key <key>`

array

是

要导入的 OSS Object Key（可重复，每次调用 1–10 个）

`--category-id <id>`

string

否

目标数据中心类目（默认：默认类目）

`--tag <text>`

array

否

应用于每个导入文件的标签（可重复，最多 10 个）

`--overwrite`

switch

否

覆盖此前从相同 OSS Key 导入的文件

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：从 OSS 批量导入文件到数据中心

```
bl knowledge doc import-oss --bucket my-bucket --region cn-beijing --oss-key docs/a.pdf --workspace-id ws-xxx
```

-   必须预先将 Bucket 授权给平台服务角色；服务端权限错误将原样透传，并提示在 RAM 控制台检查 AliyunServiceRoleForBailian。
-   文件名取自 OSS Key 的 basename。
-   \--overwrite 会替换此前导入的文件并生成新的 fileId（旧 fileId 将失效）——已通过真实环境验证。

### bl knowledge doc list

列出知识库文档及其解析/索引状态。需要 API Key 鉴权。

**语法**

```
bl knowledge doc list --index-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--page-number <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每次请求的分页大小

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：列出知识库文档及其解析状态

```
bl knowledge doc list --index-id idx-xxx --workspace-id ws-xxx
```

-   文本模式会突出显示状态为 FAILED 的文档——请使用导入任务状态命令检查失败详情。
-   分页大小默认为 10（服务端默认值），最大为 100。

### bl knowledge doc status

检查知识库导入任务状态。需要 API Key 鉴权。

**语法**

```
bl knowledge doc status --index-id <id> --job-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--job-id <id>`

string

是

导入任务 ID（导入命令返回的 ingestionId）

`--page-number <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每次请求的分页大小

`--wait`

switch

否

轮询直到任务进入终态

`--poll-interval <seconds>`

number

否

等待时的轮询间隔（默认：5）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：检查知识库导入任务状态

```
bl knowledge doc status --index-id idx-xxx --job-id job-xxx --workspace-id ws-xxx
```

-   \--index-id 和 --job-id 均为必填（只传其中一个会返回 SystemError）。
-   如果出现 SystemError，任务可能不存在——请检查文档列表输出中的 ingestion ID。
-   任务整体状态为 PENDING / RUNNING / COMPLETED；单个文档失败（例如 PARSE\_FAILED）时会以非零状态退出，并原样透传错误信息。

### bl knowledge doc tag

批量更新数据中心文件标签。需要 API Key 鉴权。

**语法**

```
bl knowledge doc tag --doc-id <id> --tag <text> [flags]
```

参数

类型

必填

说明

`--doc-id <id>`

array

是

要添加标签的数据中心文件 ID（可重复，每次调用 1–20 个）

`--tag <text>`

array

是

应用于每个 --doc-id 的标签（可重复，每个最多 32 个字符）

`--mode <mode>`

string

否

更新模式：append（默认）或 overwrite

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：批量更新数据中心文件标签

```
bl knowledge doc tag --doc-id file-xxx --tag project-a --tag draft --workspace-id ws-xxx
```

-   同一组标签会应用于每个 --doc-id；若需应用不同标签组，请多次运行该命令。
-   服务端限制：每个文件最多 100 个标签，标签总长度最多 700 个字符，单个标签最多 32 个字符。

### bl knowledge doc delete

从知识库中删除文档及其 Chunk。需要 API Key 鉴权。

**语法**

```
bl knowledge doc delete --index-id <id> --doc-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--doc-id <id>`

array

是

要删除的文档 ID（可重复）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除所选文档及其全部 Chunk，且无法撤销。

**示例**：预览删除知识库文档及其 Chunk

```
bl knowledge doc delete --index-id idx-xxx --doc-id file-xxx --workspace-id ws-xxx --dry-run
```

-   仅从知识库索引中移除文档；源文件仍保留在数据中心。
-   请使用 `knowledge doc list --quiet` 返回的 doc\_id，而不是 `knowledge doc upload` 返回的 fileId。通过 `knowledge create --doc-id` 创建的文档，其 doc\_id 等于 fileId；通过 `knowledge doc upload --index-id` 导入的文档，其 doc\_id 可能带有 Workspace 后缀。
-   删除结果最多可能需要约 30 秒才会生效——文档可能会短暂地继续出现在列表中。
-   输出会列出实际删除的 ID。

### bl knowledge file get

查看数据中心文件详情（大小、MD5、标签、时间戳）。需要 API Key 鉴权。

**语法**

```
bl knowledge file get --file-id <id> [flags]
```

参数

类型

必填

说明

`--file-id <id>`

string

是

数据中心文件 ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：查看数据中心文件详情

```
bl knowledge file get --file-id file-xxx --workspace-id ws-xxx
```

### bl knowledge file list

列出数据中心类目中的文件。需要 API Key 鉴权。

**语法**

```
bl knowledge file list --category-id <id> [flags]
```

参数

类型

必填

说明

`--category-id <id>`

string

是

要列出文件的类目（通过类目列表命令查找 ID）；精确匹配

`--name <text>`

string

否

按不含扩展名的文件名精确筛选（a.md 应传入 a）

`--file-id <id>`

array

否

按文件 ID 精确筛选（可重复）

`--next-token <token>`

string

否

下一页游标（来自上一次输出）

`--max-result <n>`

number

否

每页条目数

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：列出数据中心类目中的文件

```
bl knowledge file list --category-id cate-xxx --workspace-id ws-xxx
```

-   必须提供真实的类目 ID——此处不会解析 default 值。请通过类目列表命令查找 ID。
-   \--name 精确匹配不含扩展名的文件名（a.md 应传入 a）；部分关键字不会返回结果。
-   分页使用游标：复用输出中的 next token 继续查询。

### bl knowledge file delete

从数据中心永久删除文件。需要 API Key 鉴权。

**语法**

```
bl knowledge file delete --file-id <id> [flags]
```

参数

类型

必填

说明

`--file-id <id>`

string

是

要删除的数据中心文件 ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除数据中心文件；引用该文件的知识库文档索引可能失效。

**示例**：从数据中心永久删除文件

```
bl knowledge file delete --file-id file-xxx --workspace-id ws-xxx
```

-   该操作不可撤销。如果知识库引用了此文件，其相关文档索引将失效。
-   如果只需从单个知识库中移除文档，请改用文档删除命令。

## 分片管理

### bl knowledge chunk add

直接向知识库添加 Chunk。需要 API Key 鉴权。多媒体知识库不支持添加 Chunk。

**语法**

```
bl knowledge chunk add --index-id <id> (--content <text> | --field <k=v>) [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--doc-id <id>`

string

否

来自文档列表命令的所属文档 ID；实际使用时所有知识库类型都需要提供

`--content <text>`

string

否

Chunk 正文，最多 6000 个字符（文档型）；与 --content-file 二选一

`--content-file <path>`

string

否

从 UTF-8 纯文本文件（.md/.txt 等）读取 Chunk 正文

`--title <text>`

string

否

Chunk 标题，最多 50 个字符（文档型）

`--image-url <url>`

array

否

Chunk 图片 URL（可重复，最多 10 个；文档型）

`--field <key=value>`

array

否

表格/图片知识库的自定义字段（可重复），键为 Excel 列标题；不能与 content/title/image 相关选项同时使用

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：直接向知识库添加 Chunk

```
bl knowledge chunk add --index-id idx-xxx --content "Chunk 文本" --title 简介 --workspace-id ws-xxx
```

-   支持文档、表格和图片知识库；不支持音视频知识库。
-   实际使用时，所有知识库类型都需要 --doc-id。请使用文档列表命令返回的文档级 ID；Chunk 列表每行返回的 doc\_id 不被接受。
-   图片型文档不支持文本 Chunk；请改为操作文本型文档（docx/pdf/txt）。
-   该 API 具有幂等性，但限流为每秒 10 次调用——批处理脚本需要控制速率。
-   响应不包含 Chunk ID；添加后请列出 Chunk 以查找新条目。
-   表格/图片知识库请使用 --field，并以 Excel 列标题作为键；值将按字符串原样传递。

### bl knowledge chunk list

列出知识库中的 Chunk 及其内容和状态。需要 API Key 鉴权。

**语法**

```
bl knowledge chunk list --index-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--doc-id <id>`

string

否

仅显示属于该文档的 Chunk

`--page-number <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每次请求的分页大小

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：列出知识库中的 Chunk 及其内容和状态

```
bl knowledge chunk list --index-id idx-xxx --workspace-id ws-xxx
```

-   在 Chunk 更新/删除命令中，使用 metadata.\_id 作为 Chunk ID，使用 metadata.doc\_id 作为文档 ID。
-   分页大小默认为 20（服务端默认值），最大为 100。

### bl knowledge chunk update

更新 Chunk 内容或切换其检索可见性。需要 API Key 鉴权。

**语法**

```
bl knowledge chunk update --index-id <id> --chunk-id <id> --doc-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--chunk-id <id>`

string

是

Chunk ID（来自 Chunk 列表输出的 metadata.\_id）

`--doc-id <id>`

string

是

Chunk 所属文档 ID（来自 Chunk 列表输出的 metadata.doc\_id）

`--content <text>`

string

否

新的 Chunk 内容，10–6000 个字符；与 --content-file 二选一

`--content-file <path>`

string

否

从 UTF-8 纯文本文件（.md/.txt 等）读取新内容

`--title <text>`

string

否

Chunk 标题，0–50 个字符（空字符串表示清除；省略则保持不变）

`--exclude`

switch

否

在检索中排除该 Chunk

`--include`

switch

否

在检索中包含该 Chunk（默认）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：更新 Chunk 内容或切换其检索可见性

```
bl knowledge chunk update --index-id idx-xxx --chunk-id chunk-xxx --doc-id file-xxx --content "修正后的文本"
```

-   内容必须为 10–6000 个字符，且不能超过知识库的最大 Chunk 大小。
-   \--content-file 需要 UTF-8 纯文本文件；此处不会解析 .docx/.pdf 等文档格式。
-   仅切换 --exclude/--include 而不提供新内容时，会自动重新提交现有内容。

### bl knowledge chunk delete

从知识库中删除 Chunk（不可撤销）。需要 API Key 鉴权。

**语法**

```
bl knowledge chunk delete --index-id <id> --chunk-id <id> [flags]
```

参数

类型

必填

说明

`--index-id <id>`

string

是

知识库 ID

`--chunk-id <id>`

array

是

要删除的 Chunk ID（可重复；每 10 个自动分批发送）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除所选 Chunk，且无法撤销。

**示例**：从知识库中删除 Chunk

```
bl knowledge chunk delete --index-id idx-xxx --chunk-id chunk-a --chunk-id chunk-b --workspace-id ws-xxx
```

-   每次调用最多接受 10 个 Chunk ID；更多 ID 会自动分批处理。
-   批量删除失败时，会分别报告已完成批次、结果未确认批次和未执行部分。

## 分类与数据合集

分类（category）用于按业务域组织数据中心文件；数据合集（collection）是文件的存储位置，默认使用平台托管存储，也可绑定自定义 OSS Bucket。

### bl knowledge category add

创建数据中心类目。需要 API Key 鉴权。

**语法**

```
bl knowledge category add --name <text> [flags]
```

参数

类型

必填

说明

`--name <text>`

string

是

类目名称（1–20 个字符）

`--parent-id <id>`

string

否

创建为该类目的子类目

`--collection-id <id>`

string

否

在该数据集合下创建（默认为平台数据集合）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：创建数据中心类目

```
bl knowledge category add --name product-docs --workspace-id ws-xxx
```

-   使用类目按业务领域组织数据中心文件。

### bl knowledge category list

列出数据中心类目。需要 API Key 鉴权。

**语法**

```
bl knowledge category list [flags]
```

参数

类型

必填

说明

`--collection-id <id>`

string

否

按数据集合 ID 精确筛选

`--parent-id <id>`

string

否

列出该父类目下的子类目

`--name <text>`

string

否

按类目名称筛选（精确匹配，与知识库列表不同）

`--next-token <token>`

string

否

下一页游标（来自上一次输出）

`--max-result <n>`

number

否

每页条目数（默认：20）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：列出数据中心类目

```
bl knowledge category list --workspace-id ws-xxx
```

-   未指定类目时，文件会进入标记为 \[default\] 的类目。
-   分页使用游标：复用输出中的 next token 继续查询。

### bl knowledge category delete

删除数据中心类目。需要 API Key 鉴权。

**语法**

```
bl knowledge category delete --category-id <id> [flags]
```

参数

类型

必填

说明

`--category-id <id>`

string

是

要删除的类目 ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会删除所选数据中心类目，且无法撤销。

**示例**：删除指定工作区的数据中心类目

```
bl knowledge category delete --category-id cate-xxx --workspace-id ws-xxx
```

-   包含文件或子类目时的处理行为由服务端定义——服务端返回的错误将原样透传。

### bl knowledge collection create

创建 FILE 数据集合。需要 API Key 鉴权。

**语法**

```
bl knowledge collection create --name <text> --description <text> [flags]
```

参数

类型

必填

说明

`--name <text>`

string

是

数据集合名称

`--description <text>`

string

是

数据集合装了什么内容、给谁用，用于在列表中区分同类集合

`--store-type <type>`

string

否

存储类型：platform（托管）或 custom（自有 OSS Bucket）

`--oss-region <id>`

string

否

OSS Region ID（使用 --store-type custom 时必填）

`--oss-bucket <name>`

string

否

OSS Bucket 名称（使用 --store-type custom 时必填）

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：创建名为 my-collection 的数据集合

```
bl knowledge collection create --name my-collection --description '团队文档' --workspace-id ws-xxx
```

-   存储类型默认为 platform（托管存储）；custom 使用已授权的自有 OSS Bucket。
-   自定义 Bucket 必须带有 bailian-connector-access=ReadAndWrite 标签（百炼基于标签的访问控制）；缺少该标签时，服务端会以容易误解的 'setBucketCORS failed' 错误拒绝创建。
-   目前没有删除数据集合的 API——请谨慎创建。

### bl knowledge collection get

查看数据集合详情。需要 API Key 鉴权。

**语法**

```
bl knowledge collection get (--collection-id <id> | --name <text>) [flags]
```

参数

类型

必填

说明

`--collection-id <id>`

string

否

数据集合 ID；与 --name 二选一

`--name <text>`

string

否

数据集合名称；与 --collection-id 二选一

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：查看指定数据集合的详情

```
bl knowledge collection get --collection-id conn-xxx --workspace-id ws-xxx
```

## 检索/问答服务管理

服务（agent）是 `search` / `chat` 的调用入口：先创建服务并绑定知识库，调试通过后发布为正式版本。

### bl knowledge service create

创建检索/问答服务（初始状态：draft，版本：beta）。需要 API Key 鉴权。

**语法**

```
bl knowledge service create --name <text> --scene <chat|search> [flags]
```

参数

类型

必填

说明

`--name <text>`

string

是

服务名称（最多 200 个字符，在 Workspace 的同一场景中唯一）

`--scene <scene>`

string

是

服务场景：chat（问答）或 search（检索）

`--description <text>`

string

否

这个服务能回答什么、给谁用 —— 建议填写：agent 靠它判断该调用哪个服务（最多 1000 个字符）

`--index-id <id>`

string

否

绑定该知识库；其他设置使用服务端默认值

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：创建名为 my-qa 的问答服务

```
bl knowledge service create --name my-qa --scene chat --description '回答产品常见问题' --workspace-id ws-xxx
```

-   未显式提供配置时，服务端会应用默认 Agent 设置。
-   部署前，可在 search/chat 命令中使用 --agent-version beta 测试草稿（beta）版本。
-   需要 Workspace 中的知识库创建权限。

### bl knowledge service list

列出 Workspace 中的检索/问答服务（Agent）。需要 API Key 鉴权。

**语法**

```
bl knowledge service list --scene <chat|search> [flags]
```

参数

类型

必填

说明

`--scene <scene>`

string

是

服务场景：chat（问答）或 search（检索）

`--status <status>`

string

否

按状态筛选：draft、deployed（包含 edited）或 deleted

`--name <text>`

string

否

按服务名称模糊筛选

`--agent-id <id>`

string

否

按 Agent ID 精确筛选

`--index-id <id>`

string

否

按关联的知识库（Pipeline）ID 精确筛选

`--page-number <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每次请求的分页大小

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：列出工作区中 chat 场景的服务

```
bl knowledge service list --scene chat --workspace-id ws-xxx
```

-   必须指定场景（chat 或 search）——要查看两类服务，请分别运行一次。
-   将返回的 agent\_id 用于 search/chat 命令或服务管理命令。

### bl knowledge service get

查看服务（Agent）详情及各版本配置。需要 API Key 鉴权。

**语法**

```
bl knowledge service get --agent-id <id> [flags]
```

参数

类型

必填

说明

`--agent-id <id>`

string

是

服务（Agent）ID

`--agent-version <version>`

string

否

要查看的指定版本（beta 或已发布版本号）；省略则返回全部版本

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：查看指定服务的详情及版本配置

```
bl knowledge service get --agent-id aid-xxx --workspace-id ws-xxx
```

-   未传入 --agent-version 时，会返回所有版本（beta 草稿和已发布版本号）。
-   版本值将原样传递；有效版本集合由服务端状态决定。

### bl knowledge service update

更新服务名称、描述或草稿配置。需要 API Key 鉴权。

**语法**

```
bl knowledge service update --agent-id <id> [flags]
```

参数

类型

必填

说明

`--agent-id <id>`

string

是

服务（Agent）ID

`--name <text>`

string

否

新服务名称（最多 200 个字符）

`--description <text>`

string

否

新服务描述（最多 1000 个字符）

`--agent-version <version>`

string

否

目标版本（默认：beta 草稿）。已发布版本只接受 --version-desc

`--version-desc <text>`

string

否

版本描述

`--policy <policy>`

string

否

Agent 策略：turbo（快速）或 agentic（多轮）

`--model <name>`

string

否

生成模型代码（必须在平台白名单中）

`--temperature <n>`

number

否

采样温度，范围 0–2

`--max-llm-calls <n>`

number

否

每次请求最大 LLM 调用次数，范围 1–30

`--enable-session-file <bool>`

string

否

启用会话文件：true 或 false

`--enable-refusal <bool>`

string

否

启用拒答：true 或 false

`--enable-anti-leak <bool>`

string

否

启用防提示词泄露：true 或 false

`--enable-rich-text <bool>`

string

否

启用富文本输出：true 或 false

`--enable-citation <bool>`

string

否

启用引用：true 或 false

`--config-file <path>`

string

否

替换整个 agent\_config 的 JSON 文件（用于 kb\_search\_configs 等嵌套设置）；不能与标量配置选项同时使用

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：更新指定服务的温度参数

```
bl knowledge service update --agent-id aid-xxx --temperature 0.7 --workspace-id ws-xxx
```

-   配置修改只应用于 beta 草稿；已发布版本只接受 --version-desc。
-   要修改已发布版本的配置，请先更新 beta 草稿（不传 --agent-version，或传 --agent-version beta），然后运行 service deploy 发布新版本。
-   标量配置选项会合并到当前草稿配置（读取-合并-写入）；--config-file 会替换整个配置，且不能与标量配置选项同时使用。
-   更新草稿后，先在 search/chat 命令中使用 --agent-version beta 验证，再部署。
-   需要 Workspace 中的知识库修改权限。

### bl knowledge service deploy

将服务的 beta 草稿发布为新版本。需要 API Key 鉴权。

**语法**

```
bl knowledge service deploy --agent-id <id> [flags]
```

参数

类型

必填

说明

`--agent-id <id>`

string

是

服务（Agent）ID

`--version-desc <text>`

string

否

新发布版本的描述

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会将当前草稿发布为新版本，并改变线上调用方使用的服务行为。

**示例**：将服务草稿发布为新版本

```
bl knowledge service deploy --agent-id aid-xxx --workspace-id ws-xxx
```

-   版本号会自动递增；状态将变为 deployed。
-   发布会影响线上调用方——确认提示用于避免误操作。
-   需要 Workspace 中的知识库修改权限。

### bl knowledge service copy

将服务复制为新草稿（名称会添加 copy\_ 前缀）。需要 API Key 鉴权。

**语法**

```
bl knowledge service copy --agent-id <id> [flags]
```

参数

类型

必填

说明

`--agent-id <id>`

string

是

要复制的源服务（Agent）ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：复制指定服务为新草稿

```
bl knowledge service copy --agent-id aid-xxx --workspace-id ws-xxx
```

-   副本初始为 beta 草稿；请使用 --agent-version beta 测试，然后部署发布。
-   需要 Workspace 中的知识库创建权限。

### bl knowledge service delete

删除检索/问答服务（软删除，幂等）。需要 API Key 鉴权。

**语法**

```
bl knowledge service delete --agent-id <id> [flags]
```

参数

类型

必填

说明

`--agent-id <id>`

string

是

服务（Agent）ID

`--workspace-id <id>`

string

否

API Endpoint URL 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会删除服务，使其 Agent ID 无法再用于搜索和对话调用，且无法撤销。

**示例**：删除指定的检索/问答服务

```
bl knowledge service delete --agent-id aid-xxx --workspace-id ws-xxx
```

-   删除无法撤销；该 agent\_id 将不能再用于 search 和 chat 调用。
-   该操作具有幂等性——重复删除已删除的服务不会失败。
-   需要 Workspace 中的知识库删除权限。
