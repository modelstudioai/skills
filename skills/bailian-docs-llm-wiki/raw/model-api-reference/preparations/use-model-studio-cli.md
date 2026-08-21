# 使用百炼 CLI

阿里云百炼 CLI 是阿里云百炼平台专为 AI Agent 打造的命令行工具。只需一行安装指令并完成认证，即可将百炼平台的 AI 能力集成至各类 AI 工具中。

## 安装与配置

**阿里云百炼CLI 安装说明**

\# 阿里云百炼CLI 安装说明（供 AI Agent 阅读）

本文档面向 \*\*AI Agent\*\*：按下列步骤为用户安装并校验 \*\*阿里云百炼CLI\*\*（npm 包名 \`bailian-cli\`，命令 \`bl\` / \`bailian\`）。用户通常通过 \*\*npm 全局安装\*\* 使用，\*\*无需\*\*访问本仓库源码。不要臆造版本号或路径；以用户环境为准。

\## 1. 安装前检查

\*\*原则\*\*：先执行检查；若 \*\*Node / 包管理器 / 网络\*\* 任一不满足下文要求，Agent 应 \*\*在本机终端内主动完成安装或配置\*\*（例如升级 Node、切换镜像、配置 \`npm\` 代理等），再继续 \`bailian-cli\` 安装。仅在无权限或环境无法自动化时，再向用户说明原因并请其配合。

1\. \*\*Node.js\*\*

\- 要求 \*\*≥ 22.12.0\*\*，执行 \`node -v\` 确认。

\- 未安装或版本不足：由 Agent 自行安装或升级 Node。

2\. \*\*npm\*\*（\*\*唯一\*\*允许的包管理器）

\- 执行 \`npm -v\` 确认可用。

\- 未安装或不可用：由 Agent \*\*安装或修复 npm\*\*（不要改用 pnpm/yarn 装 \`bailian-cli\`），再执行 \`npm install -g bailian-cli\`。

\- 即使本机已安装 \`pnpm\`、\`yarn\` 等，\*\*也仅用于其它项目\*\*；装 \`bailian-cli\` 时仍必须用 \`npm\`。

3\. \*\*网络\*\*

\- 需能访问 npm registry（默认 \*\*registry.npmjs.org\*\*）。

\- 不可达：由 Agent 自行配置镜像或代理后重试。

\---

\## 2. 安装 CLI 与 Skills

\*\*仅允许以下命令\*\*（不要用 \`pnpm add -g\`、\`yarn global add\` 等）。按顺序执行，上一步通过后再进行下一步。

\*\*2.1 安装 CLI\*\*

\`\`\`bash

npm install -g bailian-cli

\`\`\`

安装成功后，应能在 PATH 中找到：

\- \`bl\`（短别名）

\- \`bailian\`（全名）

\*\*校验\*\*（Agent 应执行并检查退出码与输出）：

\`\`\`bash

bl --version

which bl # Windows 可用 where bl

\`\`\`

若 \`command not found\`：检查全局 bin 是否在 PATH（\`npm config get prefix\`，其下 \`bin\` 目录应加入 PATH）。

\*\*2.2 安装 Skills\*\*

CLI 校验通过后，在本机终端执行：

\`\`\`bash

npx skills add modelstudioai/cli --all -g

\`\`\`

安装成功后，用中文简要说明已安装的 skills 及用户可做什么。

\---

\## 3. 鉴权（安装后必做才能调 API）

\### 推荐：浏览器登录（控制台会话）

适用于本机交互式安装，无需用户手动复制 API Key：

1\. 执行 \`bl auth status --output json\`，判断是否已配置。

2\. 若未配置，在\*\*用户本机终端\*\*执行 \`bl auth login --console\`；命令会拉起浏览器完成阿里云控制台登录授权。

3\. 登录成功后执行 \`bl auth status --output json\` 确认；汇报时只使用 masked 字段，\*\*禁止\*\*回显完整凭据。

\> 此方式同时打通 \`app list\`、\`usage free\` 等控制台能力，并自动配置 API Key 调用所需的鉴权信息。

\### 备选：由 Agent 引导用户输入 API Key 后登录

适用于无法拉起浏览器的对话式安装（远程 SSH、CI 调试、纯终端环境等）：

\- 获取入口：\[百炼控制台 API Key\](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key)

1\. 执行 \`bl auth status --output json\`，判断是否已配置。

2\. 若未配置或后续 API 校验失败，\*\*请用户粘贴 API Key\*\*（可说明从上述控制台复制；勿要求用户发到公开渠道）。

3\. 用户提供了 Key 之后，在\*\*用户本机终端\*\*执行（Agent 用终端工具跑，勿把 Key 写进回复正文）：\`bl auth login --api-key <用户提供的\_Key>\`

4\. 登录成功后执行 \`bl auth status --output json\` 确认；汇报时只使用 masked 字段，\*\*禁止\*\*回显完整 Key。

\### 其他方式

\- \*\*环境变量\*\*（不落盘到配置文件）：在 shell 中配置 API Key 环境变量；变量名见 \`bl auth status --help\`，勿在对话中向用户解释底层命名。

\- \*\*写入配置文件\*\*（持久化，与 \`auth login\` 落盘相同）：\`bl config set --key api\_key --value <key>\`（\`--key api-key\` 亦可）。\*\*不会\*\*像 \`bl auth login --api-key\` 那样先校验 Key 是否可用；Agent 引导安装时仍\*\*优先\*\*用 \`auth login\`。

\- \*\*命令行临时传入\*\*：需要 API Key 的 \`bl\` 子命令可在\*\*当次\*\*执行附加全局 \`--api-key <key>\`，仅本次生效、不落盘（例：\`bl text chat --api-key sk-xxx --message "你好"\`）。与上文持久化方式不是同一用途。

\### Agent 安全约束

\- \*\*禁止\*\*把真实 API Key 写入仓库、日志、Skill、聊天记录的可公开部分。

\- CI / 非交互环境：使用 \`bl ... --non-interactive\`；通过密钥管理或环境变量注入，勿在脚本中硬编码 Key。

\---

\## 4. 最小功能验证

在鉴权配置完成后执行：

\`\`\`bash

bl auth status --output json

bl text chat --message "ping" --non-interactive --output json

\`\`\`

若失败：根据 stderr / JSON 中的 \`hint\` 或 \`message\` 排查（网络、Key 无效、region 等）。全局 region：\`--region cn|us|intl\`，默认 \`cn\`。

\---

\## 5. 常见问题（Agent 排障清单）

| 现象 | 可能原因 | 建议动作 |

| ----------------------- | -------------------- | --------------------------------------------------------------- |

| \`bl: command not found\` | 全局 bin 不在 PATH | 检查 \`npm prefix -g\` 与 PATH |

| 安装报错 engines | Node 版本过低 | 升级到 ≥ 22.12 |

| 401 / 鉴权失败 | 未 login 或 Key 无效 | 引导用户更新 Key 并 \`bl auth login --api-key\` |

| 企业网络无法访问 npm | 代理 / 镜像 | 配置 registry 或代理后再装 |

| 本机只有 pnpm、没有 npm | Agent 误用 pnpm 安装 | 先装/修好 \*\*npm\*\*，再用 \`npm install -g bailian-cli\`；勿用 pnpm |

### 安装

**说明**

前置要求：Node.js **≥ 22.12.0**。百炼 CLI 仅支持通过 npm 安装。

**方式一：在 AI Agent 中安装（推荐）**

在 AI Agent 中告诉 Agent：

```
请阅读 https://bailian.aliyun.com/cli/install.md 并按照说明为我安装阿里云百炼 CLI
```

**方式二：手动安装**

```
# 第 1 步：安装 CLI
npm install -g bailian-cli

# 第 2 步：安装 Skills（将百炼能力描述文件注册到各 Agent 的 Skills 目录）
npx skills add modelstudioai/cli --all -g

# 第 3 步：验证安装
bl --version
```

### 认证与配置

使用百炼 CLI 前，您需要完成身份认证。支持以下认证方式：

**认证方式**

**命令**

**适用场景**

控制台登录（推荐）

`bl auth login --console`

模型调用 + 应用管理（拉起浏览器完成 OAuth 登录）

API Key

`bl auth login --api-key sk-xxx`（[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key)）

模型调用（文本、图像、视频、语音等）

Token Plan API Key

`bl auth login --config token-plan --api-key sk-sp-xxx`（[获取 Token Plan API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key)）

Token Plan 个人版订阅用户的模型调用。使用 `bl config use --name token-plan` 切换为默认配置，或在命令中加 `--config token-plan` 单次指定

环境变量

配置 API Key 环境变量

CI/CD、无界面环境

配置文件

`bl config set --key api_key --value sk-xxx`

持久化（不校验 Key 有效性）

临时传入

`bl text chat --api-key sk-xxx --message "你好"`

单次调用，不落盘

> 控制台登录和 API Key 可同时配置，互不覆盖。

**说明**

如果您通过控制台登录后，执行 `bl text chat` 等模型调用命令时仍提示"缺少 API Key"，请先运行 `bl update` 升级到最新版本。若升级后问题仍然存在，请单独配置 API Key：`bl auth login --api-key <your-key>`。

认证完成后，您可以通过 `bl config` 设置模型、输出目录等参数：

```
# 查看当前配置
bl config show

# 设置默认文本模型
bl config set --key default-text-model --value qwen3.7-max

# 设置输出目录
bl config set --key output_dir --value ~/bailian-output
```

**常用全局参数**

**参数**

**说明**

`--api-key <key>`

指定 API Key（仅本次生效）

`--region <cn|us|intl>`

切换地域（默认 cn）

`--base-url <url>`

自定义 API 端点

`--output <text|json>`

输出格式

`--timeout <seconds>`

请求超时时间

`--quiet`

静默模式，减少输出

`--verbose`

打印 HTTP 请求/响应详情

`--no-color`

禁用 ANSI 颜色

`--dry-run`

预览请求，不实际执行

`--non-interactive`

非交互模式，适用于 Agent 和 CI/CD

`--concurrent <n>`

并发请求数（默认 1）

百炼 CLI 兼容 Claude Code、Cursor、Codex、Qwen Code 等主流 AI 工具和框架。完整兼容列表和集成方式，请参见[百炼 CLI GitHub 仓库](https://github.com/modelstudioai/cli)。

## 场景实战

### 电商套图生成

告诉 Agent：

```
帮我生成一套亚马逊电商主图，6 张图，产品是纯黑色夏日男装 T 恤
```

Agent 会组合多个命令完成任务：

1.  生成 6 张产品主图：
    
    ```
    bl image generate --prompt "纯黑色夏日男装T恤，白色背景，亚马逊电商主图风格" --n 6 --out-dir ./ecommerce/
    ```
    
2.  如需调整某张图：
    
    ```
    bl image edit --image ./ecommerce/image_01.png --prompt "添加模特穿着效果"
    ```
    
3.  如需生成产品展示视频：
    
    ```
    bl video generate --image ./ecommerce/image_01.png --prompt "T恤360度旋转展示" --download tshirt-demo.mp4
    ```
    

### 新闻播客生成

告诉 Agent：

```
搜索今天关于 AI 的新闻，写一段相声，然后生成男女音色区分的音频播客
```

Agent 会依次执行：

1.  联网搜索获取新闻素材：
    
    ```
    bl search web --query "今天AI新闻"
    ```
    
2.  用大模型撰写相声稿本：
    
    ```
    bl text chat --message "根据以下新闻素材，写一段相声..."
    ```
    
3.  分角色生成音频：
    
    ```
    bl speech synthesize --text "甲：您听说了吗..." --voice Ethan --out host_male.mp3
     bl speech synthesize --text "乙：怎么了？..." --voice Cherry --out host_female.mp3
    ```
    
4.  用 ffmpeg 合并音频片段为完整播客。
    

### 故事书生成

告诉 Agent：

```
帮我生成一部小红帽的故事书，真人写实版本，保持人物连续一致性，需要有 20 页，尺寸是 16:9 的，变成 PDF 给我
```

Agent 会自动完成：为每页生成故事文字 → 根据文字生成风格一致的配图 → 排版并输出 PDF。

## 命令参考

### 文本对话

**bl text chat**

发送文本对话请求，兼容 OpenAI 接口格式。

```
bl text chat --message <text> [flags]
```

**参数**

**说明**

**默认值**

`--model <model>`

模型 ID

qwen3.7-max

`--message <text>`

消息内容（可重复，前缀 `role:` 设置角色）

—

`--messages-file <path>`

从 JSON 文件读取消息（`-` 表示标准输入）

—

`--system <text>`

系统提示词

—

`--max-tokens <n>`

最大生成 token 数

4096

`--temperature <n>`

采样温度 (0.0, 2.0\]

—

`--top-p <n>`

核采样阈值

—

`--stream`

流式输出（TTY 下默认开启）

—

`--tool <json-or-path>`

工具定义，JSON 或文件路径（可重复）

—

`--enable-thinking`

开启思考模式（适用于 qwen3/qwq 模型）

—

`--thinking-budget <n>`

思考模式最大 token 数

4096

### 全模态理解

**bl omni**

全模态对话，支持图片、音频、视频输入，文本和语音输出。

```
bl omni --message <text> [flags]
```

**参数**

**说明**

**默认值**

`--message <text>`

消息内容（可重复）

—

`--model <model>`

模型 ID

qwen3.5-omni-plus

`--system <text>`

系统提示词

—

`--image <url>`

图片 URL 或本地文件（可重复）

—

`--audio <url>`

音频 URL 或本地文件（可重复）

—

`--video <url>`

视频 URL 或本地文件

—

`--voice <voice>`

输出音色（可选：Chelsie、Cherry、Ethan、Serena、Tina）

Cherry

`--audio-format <fmt>`

音频输出格式

wav

`--audio-out <path>`

保存音频到文件

自动生成

`--text-only`

仅输出文本，不生成音频

—

`--max-tokens <n>`

最大生成 token 数

—

`--temperature <n>`

采样温度 (0.0, 2.0\]

—

### 图像生成与编辑

**bl image generate**

文字生成图像。

```
bl image generate --prompt <text> [flags]
```

**参数**

**说明**

**默认值**

`--prompt <text>`

图像描述

—

`--model <model>`

模型 ID

qwen-image-2.0

`--size <W*H>`

图像尺寸，支持比例（3:4, 16:9）或像素（2048\*2048）

—

`--n <count>`

每次生成图片数量（最多 6）

1

`--seed <n>`

随机种子，用于复现结果

—

`--negative-prompt <text>`

反向提示词，排除不需要的内容

—

`--prompt-extend <bool>`

是否启用提示词扩展

true（同步模式）

`--watermark <bool>`

是否添加水印

true

`--no-wait`

异步模式，立即返回任务 ID

—

`--out-dir <dir>`

图片保存目录

—

`--out-prefix <prefix>`

文件名前缀

image

`--poll-interval <seconds>`

轮询间隔

3

**bl image edit**

编辑已有图像，支持多图合成。

```
bl image edit --image <url> --prompt <text> [flags]
```

**参数**

**说明**

**默认值**

`--image <url>`

源图片 URL 或本地文件（可重复，用于多图合成）

—

`--prompt <text>`

编辑指令

—

`--model <model>`

模型 ID

qwen-image-2.0

`--size <W*H>`

输出尺寸

—

`--n <count>`

生成数量（最多 6）

1

`--seed <n>`

随机种子

—

`--negative-prompt <text>`

反向提示词

—

`--prompt-extend <bool>`

是否启用提示词扩展

true

`--watermark <bool>`

是否添加水印

true

`--out-dir <dir>`

保存目录

—

`--out-prefix <prefix>`

文件名前缀

edited

### 视频生成与编辑

**bl video generate**

文字或图片生成视频。

```
bl video generate --prompt <text> [--image <url>] [flags]
```

**参数**

**说明**

**默认值**

`--prompt <text>`

视频描述

—

`--model <model>`

模型 ID

happyhorse-1.1-t2v（有 --image 时为 i2v）

`--image <url>`

输入图片，启用图生视频模式

—

`--negative-prompt <text>`

反向提示词

—

`--resolution <res>`

分辨率（如 1280\*720）

—

`--ratio <ratio>`

宽高比（如 16:9, 1:1）

—

`--duration <seconds>`

视频时长（秒）

5

`--prompt-extend <bool>`

是否启用提示词扩展

—

`--watermark <bool>`

是否添加水印

true

`--seed <n>`

随机种子

—

`--download <path>`

完成后保存到文件

—

`--async`

立即返回任务 ID（异步模式，适用于 Agent/CI）

—

`--poll-interval <seconds>`

轮询间隔

5

**bl video edit**

编辑视频，支持风格转换、对象替换等。

```
bl video edit --video <url> --prompt <text> [flags]
```

**参数**

**说明**

**默认值**

`--video <url>`

输入视频 URL 或本地文件（2-10 秒）

—

`--prompt <text>`

编辑指令

—

`--model <model>`

模型 ID

happyhorse-1.0-video-edit

`--ref-image <url>`

参考图片（最多 4 张，逗号分隔）

—

`--negative-prompt <text>`

反向提示词

—

`--resolution <res>`

分辨率：720P 或 1080P

1080P

`--ratio <ratio>`

宽高比（16:9, 9:16, 1:1, 4:3, 3:4）

—

`--duration <seconds>`

输出时长（2-10 秒）

—

`--audio-setting <mode>`

音频处理：auto 或 origin（保留原声）

auto

`--prompt-extend <bool>`

是否启用提示词扩展

—

`--watermark <bool>`

是否添加水印

true

`--seed <n>`

随机种子

—

`--download <path>`

保存到文件

—

`--no-wait`

立即返回任务 ID

—

`--poll-interval <seconds>`

轮询间隔

15

**bl video ref**

多图参考生成视频，支持多主体、多镜头、配音。

```
bl video ref --prompt <text> --image <url>... [flags]
```

**参数**

**说明**

**默认值**

`--prompt <text>`

视频描述，使用标记引用素材（图1、视频1 等）

—

`--model <model>`

模型 ID

happyhorse-1.1-r2v

`--image <url>`

参考图片（可重复，用于多主体）

—

`--ref-video <url>`

参考视频（可重复）

—

`--image-voice <url>`

图片对应的配音（按位置配对）

—

`--video-voice <url>`

视频对应的配音（按位置配对）

—

`--resolution <res>`

分辨率：720P 或 1080P

720P

`--ratio <ratio>`

宽高比（16:9, 9:16, 1:1）

—

`--duration <seconds>`

视频时长（2-10 秒）

5

`--prompt-extend <bool>`

是否启用提示词扩展

—

`--watermark <bool>`

是否添加水印

true

`--seed <n>`

随机种子

—

`--download <path>`

保存到文件

—

`--no-wait`

立即返回任务 ID

—

`--poll-interval <seconds>`

轮询间隔

15

**bl video task get**

查询异步视频任务的状态。

```
bl video task get --task-id <id>
```

**参数**

**说明**

`--task-id <id>`

异步任务 ID

**bl video download**

按任务 ID 下载已完成的视频。

```
bl video download --task-id <id> --out <path>
```

**参数**

**说明**

`--task-id <id>`

任务 ID

`--out <path>`

输出文件路径

### 视觉理解

**bl vision describe**

使用视觉模型描述图片或视频内容。

```
bl vision describe --image <path-or-url> [flags]
```

**参数**

**说明**

**默认值**

`--image <path-or-url>`

图片路径或 URL

—

`--video <url>`

视频文件路径或 URL

—

`--prompt <text>`

关于内容的问题

自动检测

`--model <model>`

视觉模型

qwen3-vl-plus

### 语音合成与识别

**bl speech synthesize**

文字转语音（TTS）。

```
bl speech synthesize --text <text> [flags]
```

**参数**

**说明**

**默认值**

`--text <text>`

要合成的文本

—

`--text-file <path>`

从文件读取文本

—

`--model <model>`

模型 ID

cosyvoice-v3-flash

`--voice <voice>`

音色 ID（用 --list-voices 查看）

—

`--list-voices`

列出可用音色

—

`--format <format>`

音频格式：mp3、pcm、wav、opus

mp3

`--sample-rate <rate>`

采样率（Hz）

—

`--volume <volume>`

音量（0-100）

50

`--rate <rate>`

语速（0.5-2.0）

1.0

`--pitch <pitch>`

音调（0.5-2.0）

1.0

`--seed <seed>`

随机种子（0-65535）

—

`--language <lang>`

语言提示（zh、en、ja、ko 等）

—

`--instruction <text>`

自然语言风格指令（如"请用温柔的语调"）

—

`--enable-ssml`

启用 SSML 标记解析

—

`--out <path>`

保存音频到文件

自动生成

`--stream`

流式输出原始 PCM 音频

—

**bl speech recognize**

语音转文字（ASR）。

```
bl speech recognize --url <audio-url> [flags]
```

**参数**

**说明**

**默认值**

`--url <url>`

音频文件 URL 或本地路径（可重复，最多 100 个）

—

`--model <model>`

模型 ID

fun-asr

`--language <lang>`

语言提示（zh、en、ja 等）

—

`--diarization`

启用说话人分离

—

`--speaker-count <n>`

预期说话人数（需配合 --diarization）

—

`--vocabulary-id <id>`

热词表 ID，提高识别准确率

—

`--channel-id <n>`

音频通道 ID

0

`--out <path>`

保存完整识别结果到 JSON 文件

—

`--no-wait`

立即返回任务 ID

—

`--poll-interval <seconds>`

轮询间隔

2

### 联网搜索

**bl search web**

联网搜索。

```
bl search web --query <text> [flags]
```

**参数**

**说明**

**默认值**

`--query <text>`

搜索关键词

—

`--count <n>`

搜索结果数量

10

`--list-tools`

列出可用的 MCP 搜索工具

—

### 应用与数据

**bl app call**

调用百炼应用（智能体或工作流）。

```
bl app call --app-id <id> --prompt <text> [flags]
```

**参数**

**说明**

**默认值**

`--app-id <id>`

应用 ID（必填）

—

`--prompt <text>`

输入提示

—

`--image <url>`

图片 URL（可重复）

—

`--file-id <id>`

预上传的文件 ID（可重复）

—

`--session-id <id>`

会话 ID，用于多轮对话

—

`--stream`

流式输出（TTY 下默认开启）

—

`--pipeline-ids <ids>`

知识库 Pipeline ID（逗号分隔）

—

`--memory-id <id>`

记忆 ID，启用长期记忆

—

`--biz-params <json>`

业务参数 JSON（工作流变量）

—

`--has-thoughts`

显示 Agent 思考过程

—

**bl app list**

列出百炼应用。

```
bl app list [flags]
```

**参数**

**说明**

**默认值**

`--name <name>`

按名称搜索

—

`--page <n>`

页码

1

`--page-size <n>`

每页数量

30

`--region <region>`

API 地域

cn-beijing

**bl memory add**

添加记忆。

```
bl memory add --user-id <id> [flags]
```

**参数**

**说明**

`--user-id <id>`

用户 ID（必填）

`--messages <json>`

消息 JSON 数组

`--content <text>`

自定义记忆内容

`--profile-schema <id>`

用户画像 Schema ID

`--memory-library-id <id>`

记忆库 ID（隔离记忆空间）

**bl memory search**

搜索记忆。

```
bl memory search --user-id <id> [flags]
```

**参数**

**说明**

**默认值**

`--user-id <id>`

用户 ID（必填）

—

`--query <text>`

搜索关键词

—

`--messages <json>`

消息 JSON 数组，用于上下文搜索

—

`--top-k <n>`

返回结果数量

10

`--memory-library-id <id>`

记忆库 ID

—

**bl memory list**

列出记忆。

```
bl memory list --user-id <id> [flags]
```

**参数**

**说明**

**默认值**

`--user-id <id>`

用户 ID（必填）

—

`--page-size <n>`

每页数量

10

`--page <n>`

页码

1

`--memory-library-id <id>`

记忆库 ID

—

**bl knowledge retrieve**

从百炼知识库检索（需要 AccessKey 认证）。

```
bl knowledge retrieve --index-id <id> --query <text> [flags]
```

**参数**

**说明**

**默认值**

`--index-id <id>`

知识库索引 ID（必填）

—

`--query <text>`

搜索关键词（必填）

—

`--workspace-id <id>`

百炼工作空间 ID

—

`--top-k <n>`

返回结果数量

10

`--rerank`

启用重排序

—

`--rerank-top-n <n>`

重排序后保留数量

—

`--access-key-id <key>`

阿里云 AccessKey ID

—

`--access-key-secret <key>`

阿里云 AccessKey Secret

—

### 开发辅助

**bl file upload**

上传本地文件到 DashScope 临时存储（48 小时有效）。

```
bl file upload --file <path> --model <model>
```

**参数**

**说明**

`--file <path>`

本地文件路径

`--model <model>`

目标模型名称（文件绑定到此模型）

**bl usage free**

查询模型免费额度。

```
bl usage free --model <model> [flags]
```

**参数**

**说明**

**默认值**

`--model <model>`

模型名称

—

`--region <region>`

API 地域

cn-beijing

**bl mcp list**

列出已激活的 MCP 服务。

```
bl mcp list [flags]
```

**参数**

**说明**

**默认值**

`--name <text>`

按名称过滤

—

`--type <type>`

服务类型：OFFICIAL 或 PRIVATE

OFFICIAL

`--page <n>`

页码

1

`--page-size <n>`

每页数量

30

`--region <region>`

API 地域

cn-beijing

**bl pipeline run**

运行流水线工作流。

```
bl pipeline run <file> [flags]
```

**参数**

**说明**

**默认值**

`--input <json>`

运行时输入（JSON）

—

`--input-file <path>`

从文件读取输入

—

`--concurrency <n>`

最大并行步骤数

1

`--events <format>`

事件输出格式：jsonl

—

`--timeout <seconds>`

步骤超时时间

—

**bl advisor recommend**

根据需求推荐最佳模型。

```
bl advisor recommend <prompt> [flags]
```

**参数**

**说明**

`--message <text>`

描述您的需求

`--dry-run`

仅显示意图分析和候选列表，不进行排序

## 常见问题

**Q：安装失败怎么办？**

确认 Node.js 版本 ≥ 22.12.0 且使用 npm 安装（不支持 pnpm/yarn）：

```
node --version
npm install -g bailian-cli
npx skills add modelstudioai/cli --all -g
```

**Q：提示认证失败？**

检查 API Key 是否正确配置：

```
bl auth status
```

如需重新配置：

```
bl auth logout
bl auth login --api-key sk-xxx
# 或拉起浏览器登录
bl auth login --console
```

**Q：本地文件可以直接用吗？**

可以。直接把文件路径传给 Agent 即可，CLI 会自动上传到临时存储（48 小时有效）：

```
帮我把 ./photo.png 改成水彩风格
帮我识别 ./meeting.wav 这段录音
描述一下 ./demo.mp4 这个视频的内容
```

**Q：如何查看命令的完整参数？**

告诉 Agent “看一下 bl image generate 有哪些参数”，或直接运行：

```
bl <命令> --help
```
