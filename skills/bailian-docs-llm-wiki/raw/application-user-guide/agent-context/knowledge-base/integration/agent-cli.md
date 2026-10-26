# 快速配置到 Agent

面向 AI agent。读完本文即可自主完成 Knowledge Studio Skill 的安装、凭证配置与可用性验证，装完重启即可在对话中检索与问答知识库。

## 前置要求

以下三项全部就绪后，Skill 才能真正调通：

1.  **Node.js ≥18** —— [下载安装](https://nodejs.org/)
2.  **已开通阿里云百炼知识库服务** —— 访问[知识库页面](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，点击 **立即开通**，等待 1–2 分钟生效。未开通时调用会返回 `403 Forbidden`
3.  **DashScope API Key** —— 在 [API Key 页](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，格式 `sk-xxx`。注意：`sk-sp-xxx` 是 Coding Plan Key，**不支持**知识库服务

## 安装 Skill

在终端执行（按你的 Agent 替换 `--agent` 值）：

```
npx skills add aliyun/alibabacloud-aiops-skills \
  --skill alibabacloud-bailian-rag-knowledgebase \
  --agent claude-code \
  -y --full-depth
```

支持的 Agent：

Agent

\--agent 值

Claude Code

`claude-code`

Qoder

`qoder`

Qwen Code

`qwen-code`

Cursor

`cursor`

Codex

`codex`

Gemini CLI

`gemini-cli`

GitHub Copilot

`github-copilot`

OpenClaw

`openclaw`

安装范围：默认当前项目；加 `-g` 全局安装（所有项目可用）。

## 配置 API Key（关键）

Skill 的检索脚本通过 `Authorization: Bearer` 调 DashScope API，必须取得 API Key。脚本按以下优先级自动获取：

1.  阿里云 CLI 配置 `~/.aliyun/config.json` 当前 profile 的 `dashscope.api_key`
2.  环境变量 `DASHSCOPE_API_KEY`
3.  阿里云 CLI 可用时自动创建

**方式 A：环境变量（最简单）**

由用户在自己的 shell 配置文件（`~/.zshrc` / `~/.bashrc`）中添加，或当前会话临时设置：

```
export DASHSCOPE_API_KEY=sk-xxxxxxxx
```

**方式 B：阿里云 CLI 自动创建（无需手动管理 Key）**

适合不想手动处理 Key 的场景。装好后 Skill 首次调用时自动创建并写入配置：

```
# 1. 安装阿里云 CLI（macOS 示例）
brew install aliyun-cli
# 2. 安装 ModelStudio 插件
aliyun plugin install --names aliyun-cli-modelstudio --enable-pre
# 3. 配置凭证（AK/SK 或 RAM 角色）
aliyun configure
```

RAM 用户需具备 `AliyunBailianFullAccess` 系统策略，或自定义策略包含 `modelstudio:ListWorkspaces`、`modelstudio:CreateApiKey`、`modelstudio:DeleteApiKey`。

**警告**API Key 属于敏感凭证。Agent 不应明文输出、硬编码或写入脚本。配置由用户在 shell 或阿里云 CLI 完成，Agent 只需确认凭证就绪。Skill 脚本会自动读取，无需 Agent 经手 Key 值。

## 验证安装

```
# 确认 Skill 已安装
npx skills ls          # 当前项目
npx skills ls -g       # 全局
```

或检查文件是否存在：`.<agent>/skills/alibabacloud-bailian-rag-knowledgebase/SKILL.md`（如 `.claude/skills/...`）。

## 重启 Agent 客户端

**重要**Skill 装好后必须重启 Agent 客户端才会加载。Agent 无法自行重启，请提示用户手动重启 Claude Code / Cursor / Qoder 等。

## 装好后怎么用

重启后在对话中直接用自然语言提问，Agent 会自动调用 Skill：

-   「列出我账号下的知识库」
-   「检索『产品文档』知识库，问：支持哪些认证方式？」

Skill 会先列出知识库（返回 `id` 与 `name`），再按问题检索相关切片并组织答案，末尾标注来源（库名；文档名；章节名）。

## 排错

现象

原因

处理

`401 InvalidApiKey`

API Key 未配或无效

检查 `DASHSCOPE_API_KEY` 或 `~/.aliyun/config.json` 中的 `dashscope.api_key`

`403 Forbidden` / `Service not activated`

未开通知识库服务

控制台[知识库页面](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)点 **立即开通**

Agent 识别不到 Skill

未重启 / 目录不对 / SKILL.md 缺失

重启客户端，检查 `.<agent>/skills/alibabacloud-bailian-rag-knowledgebase/SKILL.md`

`npx skills add` 报错

Node 版本低 / 网络

确认 Node ≥18，重试

## 更多信息

-   控制台 [**服务渠道**](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面提供交互式安装命令
-   [阿里云 Skills 使用文档](https://help.aliyun.com/zh/skillsportal/quickly-use-alibaba-cloud-skills)
