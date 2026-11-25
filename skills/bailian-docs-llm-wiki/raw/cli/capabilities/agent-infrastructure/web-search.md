# 联网搜索

阿里云百炼 CLI 联网搜索命令速查。

在终端调用阿里云百炼联网搜索能力，实时检索互联网信息。

> **说明**
>
> 联网搜索能力目前仅对中国站（aliyun.com）账号开放。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl search web --help`。本文命令明细以 bl 2.8.4 为基准核实。

<a id="命令速查"></a>

## 命令速查

<a id="bl-search-web"></a>

### bl search web

默认通过支持内置联网搜索的模型检索互联网，也可切换为 DashScope MCP WebSearch 服务。需要 API Key 鉴权。

**语法**

<a id="code-block"></a>

```bash
bl search web --query <text> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--query <text>` | string | 否 | 搜索查询文本 |
| `--count <n>` | number | 否 | 搜索结果数量（默认：10，仅 MCP 模式） |
| `--list-tools` | switch | 否 | 列出可用的 MCP 工具并退出（仅 MCP 模式） |
| `--mode <mcp\|model>` | string | 否 | 搜索模式：model 通过 Chat Completions（enable\_search）由模型联网作答，mcp 调用 WebSearch MCP 服务（默认：model） |
| `--model <model>` | string | 否 | `--mode model` 使用的模型 ID（默认：qwen3.8-max） |

**示例**：搜索阿里云百炼最新功能

<a id="code-block-2"></a>

```bash
bl search web --query "阿里云百炼最新功能"
```

**示例**：使用 MCP 模式获取网页列表

<a id="code-block-3"></a>

```bash
bl search web --mode mcp --query "TypeScript 5.9 新功能" --count 5
```

**示例**：列出 MCP 模式可用的工具

<a id="code-block-4"></a>

```bash
bl search web --list-tools
```

-   默认 `--mode model`：发送单次非流式 Chat Completions 请求（`enable_search: true`），模型回答以单个 `content[].text` 块返回，不返回网页列表。`--mode mcp` 返回 pages 列表。
-   `--count` 和 `--list-tools` 仅支持 MCP 模式。
-   模型按 `--model`、`default_text_model`、`qwen3.8-max` 依次解析。
-   Token Plan 订阅 Key 无法授权 MCP 模式，请使用默认的 model 模式。
