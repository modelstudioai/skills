# 数据集管理

阿里云百炼 CLI 数据集上传、校验与管理的命令速查。

在终端管理模型微调所需的数据集：上传、本地校验、查看与删除。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl dataset upload --help`。本文命令明细以 bl 2.2.1 为基准核实。

## 命令速查

### bl dataset upload

将数据集文件（.jsonl 或 .zip）上传到百炼。需要 API Key 鉴权。

**语法**

```
bl dataset upload --file <path> [--purpose <name>] [--schema <chatml|dpo|cpt|tts|image|video>] [--no-validate] [--full-validate]
```

参数

类型

必填

说明

`--file <path>`

string

是

本地数据集文件（.jsonl 或 .zip；SFT/DPO 不超过 200MB，CPT 不超过 300MB，媒体 ZIP 不超过 2GB）

`--purpose <name>`

string

否

数据集用途标签（默认："fine-tune"）

`--schema <s>`

string

否

记录 Schema："chatml"（SFT）、"dpo"（chosen/rejected）、"cpt"（原始文本）、"tts"（音频）、"image"（图片生成）或 "video"（视频生成）。默认逐条自动识别。

`--no-validate`

switch

否

跳过本地 JSONL 预检查（不推荐）

`--full-validate`

switch

否

使用 JSON.parse 检查每一行，而不是抽样检查（速度较慢）

**示例**：上传数据集文件到百炼

```
bl dataset upload --file train.jsonl
```

-   支持 .jsonl（文本）和 .zip（包含 data.jsonl 清单的音频、图片或视频归档）。可识别六种记录 Schema：chatml = {messages:\[...\]}（SFT）；dpo = {messages:\[...\], chosen, rejected}；cpt = {text:"..."}（持续预训练，原始文本）；tts = {wav\_fn:"train/xxx.wav", text:"..."}（音频微调）；image = {img\_path:"..."}（图片生成）；video = {first\_frame\_path:...}（视频生成）。
-   未指定 --schema 时，包含 wav\_fn 的记录按 TTS 验证，包含 img\_path 的按 image 验证，包含 chosen/rejected 的按 DPO 验证，仅含 text（无 messages）的按 CPT 验证，其他记录按 ChatML 验证。
-   上传上限：SFT/DPO 文本 200MB、CPT 300MB、媒体 ZIP 2GB。上传使用 OpenAI 兼容的 /compatible-mode/v1/files Endpoint，以便保留 purpose 标签；DashScope 原生 /api/v1/files 会丢弃该标签。

### bl dataset validate

在本地验证数据集文件（.jsonl 或 .zip），不执行上传。无需鉴权。

**语法**

```
bl dataset validate --file <path> [--full-validate] [--schema <chatml|dpo|cpt|tts|image|video>]
```

参数

类型

必填

说明

`--file <path>`

string

是

本地数据集文件（.jsonl 或 .zip）

`--full-validate`

switch

否

使用 JSON.parse 检查每一行，而不是抽样检查（速度较慢）

`--schema <s>`

string

否

记录 Schema："chatml"（SFT）、"dpo"（chosen/rejected）、"cpt"（原始文本）、"tts"（音频）、"image"（图片生成）或 "video"（视频生成）。默认逐条自动识别。

**示例**：在本地验证数据集文件

```
bl dataset validate --file train.jsonl
```

-   默认扫描：先对每一行进行结构检查，再抽取约 160 行（前 50 行、均匀抽取 100 行、最后 10 行），使用 JSON.parse 按当前 Schema 验证。
-   Schema：chatml = {messages:\[...\]}（SFT）；dpo = {messages:\[...\], chosen, rejected}；cpt = {text:"..."}（持续预训练，原始文本）；tts = {wav\_fn:"train/xxx.wav", text:"..."}（音频微调）；image = {img\_path:"..."}（图片生成）；video = {first\_frame\_path:"...", video\_path:"..."}（视频生成，支持 i2v 首帧或通过 last\_frame\_path 指定 kf2v 首尾帧）。
-   未指定 --schema 时，包含 wav\_fn 的记录按 TTS 验证，包含 img\_path 的按 image 验证，包含 first\_frame\_path/video\_path 的按 video 验证，包含 chosen/rejected 的按 DPO 验证，仅含 text（无 messages）的按 CPT 验证，其他记录按 ChatML 验证。使用 --schema 要求每条记录符合指定结构。
-   ZIP 归档（.zip）除逐条检查记录内容外，还会执行结构验证（存在 data.jsonl、媒体引用可解析）。使用 --full-validate 对每一行执行 JSON.parse。

### bl dataset list

列出已上传的数据集文件。需要 API Key 鉴权。

**语法**

```
bl dataset list [--page <n>] [--page-size <n>] [--purpose <name>]
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

每页结果数（默认：10，最多：100）

`--purpose <name>`

string

否

按用途筛选（例如 "fine-tune"、"evaluation"）。省略时列出全部。

**示例**：列出已上传的数据集文件

```
bl dataset list --purpose fine-tune
```

### bl dataset get

获取单个数据集文件的详情。需要 API Key 鉴权。

**语法**

```
bl dataset get --file-id <id>
```

参数

类型

必填

说明

`--file-id <id>`

string

是

数据集文件 ID

**示例**：获取数据集文件的详情

```
bl dataset get --file-id file-xxx
```

### bl dataset groups

列出 Console 数据集组。需要 Console 鉴权。

**语法**

```
bl dataset groups [--page <n>] [--page-size <n>] [--name <name>]
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

每页条数（默认：10）

`--name <name>`

string

否

按名称筛选（服务端过滤，传入前去除首尾空白）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：列出 Console 数据集组

```
bl dataset groups --page 2 --page-size 20
```

-   仅获取请求的当前页。records 包含数据集组列表，items 为服务端返回的查询总数。每个组的 datasets 仅为单版本预览，不是完整版本列表；使用 `dataset version --dataset-group-id` 获取该组的版本列表。

### bl dataset version

按组列出版本或按 ID 查询单个版本详情。需要 Console 鉴权。

**语法**

```
bl dataset version (--dataset-group-id <id> | --dataset-id <id> [--include-status])
```

参数

类型

必填

说明

`--dataset-group-id <id>`

string

否

按组列出 Console 数据集版本；与 `--dataset-id` 互斥

`--dataset-id <id>`

string

否

Console 数据集版本 ID（非 API 文件 ID）

`--include-status`

switch

否

同时查询导入/发布状态；仅与 `--dataset-id` 一起使用

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：按组列出数据集版本

```
bl dataset version --dataset-group-id example-group-id
```

**示例**：查询单个版本详情及状态

```
bl dataset version --dataset-id example-version-id --include-status --output json
```

-   `--dataset-group-id` 和 `--dataset-id` 必须且只能提供一个。`--include-status` 仅在指定 `--dataset-id` 时有效。
-   先用 `dataset groups` 获取 datasetGroupId，再用 `--dataset-group-id` 列出版本；从返回结果中取 datasetId，通过 `--dataset-id` 查询详情。fileId 属于文件/训练流程，不能替代 Console ID。

### bl dataset delete

通过 ID 删除数据集文件。需要 API Key 鉴权。

**语法**

```
bl dataset delete --file-id <id>
```

参数

类型

必填

说明

`--file-id <id>`

string

是

数据集文件 ID

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除指定的数据集文件，且无法撤销。

**示例**：通过 ID 删除数据集文件

```
bl dataset delete --file-id file-id-xxx
```
