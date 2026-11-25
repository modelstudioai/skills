# 图像生成与编辑

阿里云百炼 CLI 图像生成与编辑的命令速查。

一条命令即可在终端调用阿里云百炼图像生成与编辑能力。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl image generate --help`。全部接受文件 URL 的参数也接受本地路径——CLI 会自动上传到临时存储（有效期 48 小时），无需手动托管为 URL。本文命令明细以 bl 2.8.0 为基准核实。

<a id="命令速查"></a>

## 命令速查

<a id="bl-image-generate"></a>

### bl image generate

生成图片（Qwen-Image / wan2.x）。需要 API Key 鉴权。

**语法**

<a id="code-block"></a>

```bash
bl image generate --prompt <text> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--prompt <text>` | string | 是 | 图片描述 |
| `--model <model>` | string | 否 | 模型 ID（默认：qwen-image-3.0） |
| `--size <W*H>` | string | 否 | 图片尺寸：比例（3:4、16:9、1:1）或像素（2048\*2048） |
| `--n <count>` | number | 否 | 每次请求生成的图片数量（默认：1，最多：6） |
| `--seed <n>` | number | 否 | 用于复现生成结果的随机种子 |
| `--negative-prompt <text>` | string | 否 | 负向提示词，用于排除不需要的内容 |
| `--prompt-extend <bool>` | boolean | 否 | 是否启用提示词扩展（true/false）。不传时：qwen-image 同步调用默认为 true；异步模型不传该参数（使用 API 默认值）。 |
| `--watermark <bool>` | boolean | 否 | 是否启用水印（true/false）。不传时使用 Profile 配置或 CLI 默认值 true。 |
| `--async` | switch | 否 | 直接返回异步任务 ID，不等待任务完成 |
| `--concurrent <n>` | number | 否 | 并行发送 N 个请求（默认：1） |
| `--out-dir <dir>` | string | 否 | 将图片下载到指定目录 |
| `--out-prefix <prefix>` | string | 否 | 文件名前缀（默认：image） |
| `--poll-interval <seconds>` | number | 否 | 等待任务时的轮询间隔（默认：3 秒） |

**示例**：根据描述生成图片

<a id="code-block-2"></a>

```bash
bl image generate --prompt "一只穿着宇航服的猫站在火星上"
```

-   `--model auto`（或在配置中把默认模型设为 `auto`）通过百炼自研 MCP 自动路由 AIGC 模型，只使用 MCP 工具支持的参数。不兼容的参数（如 `--seed`、`--watermark`、`--async`）直接返回用法错误，不会回退到 REST 调用。

<a id="bl-image-edit"></a>

### bl image edit

使用文本指令编辑现有图片（Qwen-Image / Wan 2.7）。需要 API Key 鉴权。

**语法**

<a id="code-block-3"></a>

```bash
bl image edit --image <url> --prompt <text> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--image <url>` | array | 是 | 源图片 URL 或本地文件路径（多图融合时可重复） |
| `--prompt <text>` | string | 是 | 编辑指令文本 |
| `--model <model>` | string | 否 | 模型 ID（默认：qwen-image-3.0） |
| `--size <W*H>` | string | 否 | 输出图片尺寸：比例（3:4、16:9）或像素（2048\*2048） |
| `--n <count>` | number | 否 | 图片数量（默认：1，最多：6） |
| `--seed <n>` | number | 否 | 用于复现结果的随机种子 |
| `--negative-prompt <text>` | string | 否 | 负向提示词，用于排除不需要的内容 |
| `--function <name>` | string | 否 | wanx\*-imageedit 功能（默认：description\_edit）。例如：stylization\_all、description\_edit |
| `--prompt-extend <bool>` | boolean | 否 | 是否启用提示词扩展（true/false）。不传时使用 CLI 默认值 true。 |
| `--watermark <bool>` | boolean | 否 | 是否启用水印（true/false）。不传时使用 Profile 配置或 CLI 默认值 true。 |
| `--out-dir <dir>` | string | 否 | 将图片下载到指定目录 |
| `--out-prefix <prefix>` | string | 否 | 文件名前缀（默认：edited） |
| `--async` | switch | 否 | 直接返回异步任务 ID，不等待任务完成 |
| `--concurrent <n>` | number | 否 | 并行发送 N 个请求（默认：1） |
| `--poll-interval <seconds>` | number | 否 | 等待任务时的轮询间隔（默认：3 秒） |

**示例**：根据指令编辑指定图片

<a id="code-block-4"></a>

```bash
bl image edit --image ./photo.png --prompt "将背景替换为海滩"
```

-   `--model auto` 通过百炼自研 MCP 自动路由 AIGC 模型，只使用 MCP 工具支持的参数。不兼容的参数直接返回用法错误，不会回退到 REST 调用。auto 模式只接受单个 `--image`。
