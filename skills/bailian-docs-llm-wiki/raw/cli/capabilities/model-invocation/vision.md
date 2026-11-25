# 视觉理解

阿里云百炼 CLI 视觉理解能力——图像、文档、长视频解析与多语言 OCR 的命令速查。

一条命令即可在终端调用阿里云百炼视觉理解能力，解析图像、文档与长视频内容。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl vision describe --help`。所有接受文件 URL 的参数也接受本地路径——CLI 会自动上传到临时存储（有效期 48 小时），无需手动托管为 URL。本文命令明细以 bl 2.2.1 为基准核实。

<a id="命令速查"></a>

## 命令速查

<a id="bl-vision-describe"></a>

### bl vision describe

使用 Qwen-VL 描述图片或视频。需要 API Key 鉴权。

**语法**

<a id="code-block"></a>

```bash
bl vision describe --image <path-or-url> [--video <url>] [--prompt <text>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--image <path-or-url>` | string | 否 | 本地图片路径或 URL |
| `--video <url>` | array | 否 | 视频文件 URL 或本地路径（mp4/mov/avi/mkv/webm） |
| `--prompt <text>` | string | 否 | 针对内容的问题（默认：自动识别） |
| `--model <model>` | string | 否 | 视觉模型（默认：qwen3-vl-plus） |

**示例**：描述指定图片或视频内容

<a id="code-block-2"></a>

```bash
bl vision describe --image photo.jpg
```
