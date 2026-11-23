# 语音合成与识别

阿里云百炼 CLI 语音合成（TTS）、语音识别（ASR）与热词词汇表管理的命令速查。

一条命令即可在终端调用阿里云百炼语音合成与识别能力，并管理热词词汇表提升识别准确率。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl speech synthesize --help`。全部接受文件 URL 的参数也接受本地路径——CLI 会自动上传到临时存储（有效期 48 小时），无需手动托管为 URL。本文命令明细以 bl 2.8.0 为基准核实。

## 语音合成

### bl speech synthesize

将文本合成为语音。需要 API Key 鉴权。

**语法**

```
bl speech synthesize --text <text> [flags]
```

参数

类型

必填

说明

`--text <text>`

string

否

要合成为语音的文本（也可使用 --text-file）

`--text-file <path>`

string

否

从文件读取文本，而非使用 --text

`--model <model>`

string

否

模型 ID（默认：Profile 配置的 TTS 模型，否则为 cosyvoice-v3-flash）。系统音色因模型而异

`--voice <voice>`

string

否

音色 ID。使用 --list-voices 查看所选模型的内置音色（如 qwen-audio-3.0-tts-plus/flash、cosyvoice-v3-flash）；使用 v3.5-flash 时需提供复刻/设计音色 ID

`--list-voices`

switch

否

列出所选模型的内置系统音色并退出（输出中会显示控制台链接）

`--format <format>`

string

否

音频格式：mp3、pcm、wav、opus（默认：mp3；流式模式默认：pcm）

`--sample-rate <rate>`

string

否

音频采样率，单位为 Hz（例如 24000）

`--volume <volume>`

string

否

音量 0–100（默认：50）

`--rate <rate>`

string

否

语速 0.5–2.0（默认：1.0）

`--pitch <pitch>`

string

否

音高倍数 0.5–2.0（默认：1.0）

`--seed <seed>`

string

否

用于复现合成结果的随机种子 0–65535

`--language <lang>`

string

否

语言提示（例如 zh、en、ja、ko、fr、de）

`--instruction <text>`

string

否

用于控制语音风格的自然语言指令（例如“使用温柔的语气”）

`--enable-ssml`

switch

否

解析输入文本中的 SSML 标记

`--out <path>`

string

否

将音频保存到文件（默认：在临时目录中自动生成路径）

`--stream`

switch

否

将原始 PCM 音频流式输出到 stdout（可通过管道传给播放器）

`--concurrent <n>`

number

否

并行发送 N 个请求（默认：1）

**示例**：预览可用音色列表

```
bl speech synthesize --list-voices --model qwen-audio-3.0-tts-plus
```

-   `--model auto` 通过百炼自研 MCP 自动路由 AIGC 模型，只使用 MCP 工具支持的参数（文本和音色）。不兼容的参数（如 `--format`、`--sample-rate`、`--stream`）直接返回用法错误，不会回退到 REST 调用。
-   流式输出指定 JSON 格式时，需要通过 `--out` 指定保存文件，避免音频数据与 JSON 结果混在同一输出流。

## 语音识别

### bl speech recognize

识别音频文件中的语音（FunAudio-ASR / Qwen-ASR Flash）。需要 API Key 鉴权。

**语法**

```
bl speech recognize --url <audio-url> [flags]
```

参数

类型

必填

说明

`--url <url>`

array

是

音频文件 URL 或本地文件路径（可重复，最多 100 个）

`--model <model>`

string

否

模型 ID（默认：Profile 配置的 ASR 模型，否则为 fun-asr）。异步：fun-asr / _\-filetrans / paraformer-_；同步：qwen3-asr-flash\* / fun-asr-flash\* / qwen-audio-\*-asr-flash

`--language <lang>`

string

否

语言提示（例如 zh、en、ja）。传统异步/input-audio：language\_hints；qwen3-filetrans：language；qwen3 同步：asr\_options.language

`--diarization`

switch

否

启用自动说话人分离

`--speaker-count <n>`

number

否

预期的说话人数量（需启用 --diarization）

`--vocabulary-id <id>`

string

否

预编译热词列表 ID（可用 `speech vocabulary create` 创建）。其 target\_model 必须与 --model 完全一致，否则静默失效且无报错。支持模型比 --vocabulary 更广，含 Fun-ASR 与 Paraformer 系列

`--vocabulary <json>`

string

否

即时热词，JSON 对象“热词→权重”，例如 '{"奋斗者":4}'。权重 1-5（推荐 4，过高会拖累其他词），50 表示超级热词。无需预先创建热词表。仅 Qwen-Audio-3.0-ASR-Flash 系列模型生效

`--context <text>`

string

否

上下文增强词表，提升专有名词准确率；须包含待识别的原词本身（只写主题描述效果有限），最长 400 字符。仅 Qwen-Audio-3.0-ASR-Flash 系列与 Fun-ASR-Flash 模型生效

`--channel-id <n>`

number

否

音频声道 ID（默认：0）

`--out <path>`

string

否

将完整转写结果保存到 JSON 文件

`--async`

switch

否

直接返回异步任务 ID，不等待任务完成

`--poll-interval <seconds>`

number

否

轮询间隔，单位为秒（默认：2）

**示例**：识别指定音频文件中的语音

```
bl speech recognize --url https://example.com/audio.mp3
```

-   `--model auto` 通过百炼自研 MCP 自动路由 AIGC 模型，只使用 MCP 工具支持的参数，并简化文本输出。不兼容的参数直接返回用法错误，不会回退到 REST 调用。音频仅支持公网 http(s) URL；本地文件需改用 `--model <id>` 指定具体模型。
-   JSON 输出保留完整响应和转写结果。没有转写结果时仍返回任务信息。

## 热词词汇表管理

管理可复用的预构建热词词汇表，提升 ASR 对专有名词的识别准确率。

### bl speech vocabulary create

创建用于语音识别的预编译热词表。需要 API Key 鉴权。

**语法**

```
bl speech vocabulary create --model <model> --prefix <prefix> (--words <json> | --words-file <path>) [flags]
```

参数

类型

必填

说明

`--model <model>`

string

是

该热词表服务的 ASR 模型（必填）。必须与后续 `speech recognize` 的 --model 完全一致，否则热词表静默失效

`--prefix <prefix>`

string

是

热词表自定义前缀（必填）。仅允许数字和小写字母，最长 10 个字符

`--words <json>`

string

否

热词，JSON 对象“热词→权重”，例如 '{"奋斗者":4}'；需要逐条指定语言时可传 API 的条目数组。权重 1-5（推荐 4）；当热词表的 target\_model 为 Qwen-Audio-3.0-ASR-Flash 系列时还可使用 50（超级热词）。也可使用 --words-file

`--words-file <path>`

string

否

包含热词的 JSON 文件（使用 - 从 stdin 读取）

`--lang <code>`

string

否

对象形态时应用到所有热词的语言代码（选填；数组形态忽略）。Paraformer 支持 zh/en/ja/yue/ko/de/fr/ru；Fun-ASR 支持 zh/en/ja

**示例**：创建指定前缀的热词表

```
bl speech vocabulary create --model fun-asr --prefix demo --words '{"奋斗者":4,"鲸落":4}'
```

-   \--model 必须与后续 `speech recognize --vocabulary-id` 使用的 --model 完全一致；不一致时热词表会静默失效且无报错。

### bl speech vocabulary list

列出预编译热词表。需要 API Key 鉴权。

**语法**

```
bl speech vocabulary list [--prefix <prefix>] [--page <n>] [--page-size <n>]
```

参数

类型

必填

说明

`--prefix <prefix>`

string

否

按热词表前缀过滤

`--page <n>`

number

否

页码，从 1 开始（默认：1）。映射为 API 的 page\_index（从 0 开始）：page - 1

`--page-size <n>`

number

否

每页结果数（默认：10）

**示例**：列出指定前缀的热词表

```
bl speech vocabulary list --prefix demo
```

-   list 响应不含 target\_model；要对齐模型请使用 `speech vocabulary get`。
-   status 为 UNDEPLOYED 的热词表会被 ASR 静默忽略。

### bl speech vocabulary get

查看预编译热词表详情。需要 API Key 鉴权。

**语法**

```
bl speech vocabulary get --id <id>
```

参数

类型

必填

说明

`--id <id>`

string

是

热词表 ID

**示例**：查看指定热词表的详情

```
bl speech vocabulary get --id vocab-demo-xxx
```

-   调用 `speech recognize --vocabulary-id` 前请用本命令确认 target\_model；模型不一致会导致静默失效。

### bl speech vocabulary update

完全替换预编译热词表的内容。需要 API Key 鉴权。

**语法**

```
bl speech vocabulary update --id <id> (--words <json> | --words-file <path>) [flags]
```

参数

类型

必填

说明

`--id <id>`

string

是

热词表 ID

`--words <json>`

string

否

热词，JSON 对象“热词→权重”，例如 '{"奋斗者":4}'；需要逐条指定语言时可传 API 的条目数组。权重 1-5（推荐 4）；当热词表的 target\_model 为 Qwen-Audio-3.0-ASR-Flash 系列时还可使用 50（超级热词）。也可使用 --words-file

`--words-file <path>`

string

否

包含热词的 JSON 文件（使用 - 从 stdin 读取）

`--lang <code>`

string

否

对象形态时应用到所有热词的语言代码（选填；数组形态忽略）。Paraformer 支持 zh/en/ja/yue/ko/de/fr/ru；Fun-ASR 支持 zh/en/ja

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会完全替换热词表中的全部词条。未列出的词将被丢弃，且无法撤销。

**示例**：预览更新热词表内容

```
bl speech vocabulary update --id vocab-demo-xxx --words '{"奋斗者":4}' --dry-run
```

-   update 是完全替换，不是增量追加。建议先用 --dry-run 预览将要写入的完整词表。

### bl speech vocabulary delete

删除预编译热词表。需要 API Key 鉴权。

**语法**

```
bl speech vocabulary delete --id <id>
```

参数

类型

必填

说明

`--id <id>`

string

是

热词表 ID

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除指定的热词表，且无法撤销。

**示例**：预览删除热词表

```
bl speech vocabulary delete --id vocab-demo-xxx --dry-run
```
