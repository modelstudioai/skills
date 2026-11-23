# 文本对话与全模态

阿里云百炼 CLI 文本对话与 Omni 全模态交互的命令速查。

一条命令即可在终端调用阿里云百炼文本对话与全模态交互能力。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl text chat --help`。全部接受文件 URL 的参数也接受本地路径——CLI 会自动上传到临时存储（有效期 48 小时），无需手动托管为 URL。本文命令明细以 bl 2.8.4 为基准核实。

## 命令速查

### bl text chat

发送文本模型请求（OpenAI 兼容，DashScope）。需要 API Key 鉴权。

**语法**

```
bl text chat --message <text> [flags]
```

参数

类型

必填

说明

`--api <chat|responses>`

string

否

调用的 API（默认：chat）

`--model <model>`

string

否

模型 ID（默认：qwen3.8-max）

`--message <text>`

array

否

消息文本（可重复；可使用 role: 前缀指定角色），也可使用 --messages-file

`--messages-file <path>`

string

否

包含 messages 数组的 JSON 文件（使用 - 从 stdin 读取）

`--system <text>`

string

否

系统提示词

`--max-tokens <n>`

number

否

最大生成 Token 数（默认：4096）

`--temperature <n>`

number

否

采样温度 (0.0, 2.0\]

`--top-p <n>`

number

否

核采样阈值

`--enable-search <true|false>`

boolean

否

启用模型内置联网搜索（仅 Chat Completions API；qwen3.8-max 默认开启）

`--stream`

switch

否

流式输出响应 Token（TTY 中默认开启）

`--tool <json-or-path>`

array

否

JSON 格式的工具定义或文件路径（可重复）

`--enable-thinking [true|false]`

boolean

否

设置思考/推理模式；裸 flag 表示 true（模型支持由服务端定义）

`--thinking-budget <n>`

number

否

思考过程最大 Token 数（默认：4096）

`--batch`

switch

否

发送单次同步 Batch Chat 请求（非流式）

`--prime`

switch

否

使用工作空间专属 Endpoint 的 Prime 模式

`--workspace-id <id>`

string

否

默认 Prime Endpoint 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

**示例**：发送文本消息请求模型回复

```
bl text chat --message "通义千问是什么？"
```

**示例**：发送同步 Batch Chat 请求

```
bl text chat --batch --model qwen-plus --message "你好" --timeout 3600
```

-   `--batch` 发送一次同步 Batch Chat 请求，即使在 TTY 中也强制非流式，不能与 `--prime`、`--api responses` 或 `--stream` 同时使用。`--message` 或 `--messages-file` 表示同一请求的对话上下文，不表示文件中的独立请求。
-   Batch Chat 请求总超时默认为 300 秒，`--timeout` 取值需为 60–3600 秒。文件批量推理使用 `batch create/get/download`，创建后返回任务 ID，不等待完成。
-   `--batch` 拒绝显式指定的实时、国际站或 Token Plan Endpoint；显式指定 Batch 或自定义代理地址时保留现有凭证。不发生自动回退或 POST 重放。
-   Prime 模式必须显式指定模型，且当前仅支持 Chat Completions API。
-   Prime Endpoint：已配置的 --base-url、DASHSCOPE\_BASE\_URL 或 Profile base\_url 优先；否则按 --workspace-id、BAILIAN\_WORKSPACE\_ID、配置项 workspace\_id 解析工作空间。
-   `--enable-search` 映射为 Chat Completions 的 `enable_search` 参数，需要模型支持内置联网搜索；白名单模型（qwen3.8-max）默认开启，可传 `--enable-search false` 显式关闭；Responses API 请改用 `--tool '{"type":"web_search"}'`。

### bl omni

支持文本输入与音频输出的多模态对话（Qwen-Omni）。需要 API Key 鉴权。

**语法**

```
bl omni --message <text> [flags]
```

参数

类型

必填

说明

`--message <text>`

array

否

消息文本（可重复；可使用 role: 前缀指定角色）

`--model <model>`

string

否

模型 ID（默认：qwen3.5-omni-plus）

`--system <text>`

string

否

系统提示词

`--image <url>`

array

否

图片 URL 或本地文件（可重复）

`--audio <url>`

array

否

音频 URL 或本地文件（.wav/.mp3/.amr/.aac/.m4a/.ogg/.3gp/.3gpp）

`--video <url>`

array

否

视频文件 URL / 本地路径，或以逗号分隔的帧 URL

`--voice <voice>`

string

否

输出音色 ID（默认：Tina）。使用 --list-voices 查看所有选项

`--list-voices`

switch

否

列出可用的输出音色并退出

`--audio-format <fmt>`

string

否

音频输出格式（默认：wav）

`--audio-out <path>`

string

否

将音频保存到文件（默认：自动生成路径）

`--text-only`

switch

否

仅输出文本，不生成音频

`--max-tokens <n>`

number

否

最大生成 Token 数

`--temperature <n>`

number

否

采样温度 (0.0, 2.0\]

**示例**：预览可用音色列表

```
bl omni --list-voices
```
