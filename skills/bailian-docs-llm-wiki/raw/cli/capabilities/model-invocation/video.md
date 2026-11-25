# 视频生成与编辑

阿里云百炼 CLI 视频生成、参考生视频与视频编辑的命令速查。

一条命令即可在终端调用阿里云百炼视频生成与编辑能力。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl video generate --help`。全部接受文件 URL 的参数也接受本地路径——CLI 会自动上传到临时存储（有效期 48 小时），无需手动托管为 URL。本文命令明细以 bl 2.8.0 为基准核实。

<a id="命令速查"></a>

## 命令速查

<a id="bl-video-generate"></a>

### bl video generate

根据文本或图片生成视频（wan3.0-video / wan2.6-t2v / happyhorse-1.1-i2v）。需要 API Key 鉴权。

**语法**

<a id="code-block"></a>

```bash
bl video generate --prompt <text> [--image <url>] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型 ID（默认：wan3.0-video） |
| `--prompt <text>` | string | 是 | 视频描述 |
| `--image <url>` | string | 否 | 图生视频使用的输入图片 URL |
| `--last-frame <url>` | string | 否 | 尾帧图片 URL（与 --image 配合，启用 kf2v 首尾帧模式） |
| `--negative-prompt <text>` | string | 否 | 负向提示词，用于排除不需要的内容 |
| `--resolution <res>` | string | 否 | 分辨率：720P 或 1080P（默认：1080P） |
| `--ratio <ratio>` | string | 否 | 宽高比（例如 16:9、9:16、1:1） |
| `--duration <seconds>` | number | 否 | 视频时长，单位为秒（默认：5） |
| `--prompt-extend <bool>` | boolean | 否 | 是否启用提示词扩展（true/false）。不传时省略该参数（使用 DashScope 默认值）。 |
| `--watermark <bool>` | boolean | 否 | 是否启用水印（true/false）。不传时使用 Profile 配置或 CLI 默认值 true。 |
| `--seed <n>` | number | 否 | 用于复现生成结果的随机种子 |
| `--download <path>` | string | 否 | 完成后将视频保存到文件 |
| `--file <url-or-path>` | string | 否 | 参考文件 URL 或本地路径，用于文件生视频（仅 wan3.0-video；与 --image/--last-frame 互斥） |
| `--prime` | switch | 否 | 使用工作空间专属 Endpoint 的 Prime 模式 |
| `--workspace-id <id>` | string | 否 | 默认 Prime Endpoint 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID） |
| `--async` | switch | 否 | 直接返回异步任务 ID，不等待任务完成 |
| `--concurrent <n>` | number | 否 | 并行发送 N 个请求（默认：1） |
| `--poll-interval <seconds>` | number | 否 | 等待任务时的轮询间隔（默认：5 秒） |

**示例**：根据文本描述生成视频

<a id="code-block-2"></a>

```bash
bl video generate --prompt "一个人正在读书，固定镜头"
```

-   `--model auto`（或在配置中把默认模型设为 `auto`）通过百炼自研 MCP 自动路由 AIGC 模型，只使用 MCP 工具支持的参数。不兼容的参数（如 `--seed`、`--watermark`、`--prime`、`--async`）直接返回用法错误，不会回退到 REST 调用。
    
-   Prime 模式必须显式指定模型。
    
-   Prime Endpoint：已配置的 --base-url、DASHSCOPE\_BASE\_URL 或 Profile base\_url 优先；否则按 --workspace-id、BAILIAN\_WORKSPACE\_ID、配置项 workspace\_id 解析工作空间。
    

<a id="bl-video-ref"></a>

### bl video ref

参考生视频（wan3.0-video / happyhorse-1.1-r2v / wan2.6-r2v）：支持多主体、多镜头和语音。需要 API Key 鉴权。

**语法**

<a id="code-block-3"></a>

```bash
bl video ref --prompt <text> --image <url>... [--ref-video <url>...] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型 ID（默认：wan3.0-video） |
| `--prompt <text>` | string | 是 | 包含引用标记的视频描述（image1、video1 等） |
| `--image <url>` | array | 否 | 参考图片 URL 或本地文件（多个主体时可重复） |
| `--ref-video <url>` | array | 否 | 参考视频 URL 或本地文件（可重复） |
| `--image-voice <url>` | array | 否 | 对应图片的语音 URL（按位置配对）。在 wan3.0-video 上作为 reference\_audio 条目发送（prompt 中用“音频1”“音频2”引用） |
| `--video-voice <url>` | array | 否 | 对应参考视频的语音 URL（按位置配对）。在 wan3.0-video 上作为 reference\_audio 条目发送（prompt 中用“音频1”“音频2”引用） |
| `--resolution <res>` | string | 否 | 分辨率：720P 或 1080P（默认：1080P） |
| `--ratio <ratio>` | string | 否 | 宽高比（16:9、9:16、1:1） |
| `--duration <seconds>` | number | 否 | 视频时长，单位为秒（默认：5） |
| `--prompt-extend <bool>` | boolean | 否 | 是否启用提示词扩展（true/false）。不传时省略该参数（使用 DashScope 默认值）。 |
| `--watermark <bool>` | boolean | 否 | 是否启用水印（true/false）。不传时使用 Profile 配置或 CLI 默认值 true。 |
| `--seed <n>` | number | 否 | 用于复现生成结果的随机种子 |
| `--download <path>` | string | 否 | 完成后将视频保存到文件 |
| `--async` | switch | 否 | 直接返回异步任务 ID，不等待任务完成 |
| `--concurrent <n>` | number | 否 | 并行发送 N 个请求（默认：1） |
| `--poll-interval <seconds>` | number | 否 | 等待任务时的轮询间隔（默认：15 秒） |

**示例**：参考图片生成多主体视频

<a id="code-block-4"></a>

```bash
bl video ref --prompt "图片 1 中的人物在草地上奔跑" --image person.jpg
```

<a id="bl-video-edit"></a>

### bl video edit

使用 happyhorse-1.0-video-edit 编辑视频（风格转换、对象替换等）。需要 API Key 鉴权。

**语法**

<a id="code-block-5"></a>

```bash
bl video edit --video <url> --prompt <text> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型 ID（默认：happyhorse-1.0-video-edit） |
| `--video <url>` | string | 是 | 输入视频 URL 或本地文件（mp4/mov，2–10 秒） |
| `--prompt <text>` | string | 否 | 编辑指令（例如“将场景转换为黏土动画风格”） |
| `--ref-image <url>` | string | 否 | 参考图片 URL（最多 4 个，以逗号分隔） |
| `--negative-prompt <text>` | string | 否 | 负向提示词，用于排除不需要的内容 |
| `--resolution <res>` | string | 否 | 分辨率：720P 或 1080P（默认：1080P） |
| `--ratio <ratio>` | string | 否 | 宽高比（16:9、9:16、1:1、4:3、3:4） |
| `--duration <seconds>` | number | 否 | 输出视频时长，单位为秒（2–10） |
| `--audio-setting <mode>` | string | 否 | 音频：auto（默认）或 origin（保留原音频） |
| `--prompt-extend <bool>` | boolean | 否 | 是否启用提示词扩展（true/false）。不传时省略该参数（使用 DashScope 默认值）。 |
| `--watermark <bool>` | boolean | 否 | 是否启用水印（true/false）。不传时使用 Profile 配置或 CLI 默认值 true。 |
| `--seed <n>` | number | 否 | 用于复现生成结果的随机种子 |
| `--download <path>` | string | 否 | 完成后将视频保存到文件 |
| `--async` | switch | 否 | 直接返回异步任务 ID，不等待任务完成 |
| `--concurrent <n>` | number | 否 | 并行发送 N 个请求（默认：1） |
| `--poll-interval <seconds>` | number | 否 | 等待任务时的轮询间隔（默认：15 秒） |

**示例**：将视频转换为黏土动画风格

<a id="code-block-6"></a>

```bash
bl video edit --video https://example.com/input.mp4 --prompt "将整个场景转换为黏土动画风格"
```

<a id="bl-video-download"></a>

### bl video download

通过任务 ID 下载已完成的视频。需要 API Key 鉴权。

**语法**

<a id="code-block-7"></a>

```bash
bl video download --task-id <id> --out <path>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--task-id <id>` | string | 是 | 要下载的任务 ID |
| `--out <path>` | string | 是 | 输出文件路径 |

**示例**：通过任务 ID 下载已生成视频

<a id="code-block-8"></a>

```bash
bl video download --task-id 3b256896-xxxx --out video.mp4
```

<a id="bl-video-task-get"></a>

### bl video task get

查询异步任务状态。需要 API Key 鉴权。

**语法**

<a id="code-block-9"></a>

```bash
bl video task get --task-id <id>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--task-id <id>` | string | 是 | 异步任务 ID |

**示例**：查询异步任务状态

<a id="code-block-10"></a>

```bash
bl video task get --task-id 3b256896-3e70-xxxx-xxxx-xxxxxxxxxxxx
```
