# 服务渠道

了解 REST API、Agent Skill 与 CLI 三种接入方式，以及 Skill 的产品规划状态。

## 接入方式对比

渠道

类型

适用场景

说明

**REST API**

REST

自有后端服务

DashScope HTTP 接口

**CLI**

命令行

本地调试 / 脚本

`bailian-cli`，用 `bl parsex` 提交和查询任务

**Agent Skill**

技能包

Qoder / Claude Code / Codex

以技能包形式接入，AI 编码工具自动加载

## REST API

所有文档解析与信息抽取能力通过 DashScope API 提供，服务地址为：

```
https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x
```

鉴权方式使用百炼的 API-KEY：

```
Authorization: Bearer <DASHSCOPE_API_KEY>
```

API Key 在[**控制台 API Key 页**](raw/model-api-reference/preparations/get-api-key.md)创建，系统根据 API Key 自动路由到对应业务空间

接口

方法

业务路径

用途

解析任务提交

`POST`

`/api/v2/apps/parse-x/parse/submit`

提交 Parse 任务

解析任务查询

`POST`

`/api/v2/apps/parse-x/parse/result`

查询 Parse 状态、结果或分片

抽取任务提交

`POST`

`/api/v2/apps/parse-x/extract/submit`

提交 Extract 任务

抽取任务查询

`POST`

`/api/v2/apps/parse-x/extract/result`

查询 Extract 状态与结果

完整接口列表见 [**API 参考**](raw/application-api-reference/api-overview.md)。

## CLI

阿里云百炼 CLI 把 ParseX 的解析与字段抽取封装为命令。安装与鉴权见[安装与鉴权](https://help.aliyun.com/zh/model-studio/cli/installation)，操作步骤和示例见[使用 CLI](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/cli.md)。

```
bl parsex parse submit --workspace-id <workspace-id> --file-url "https://example.com/document.pdf" --output-file-format markdown --output json
bl parsex parse result --workspace-id <workspace-id> --biz-id <parse-biz-id> --follow --output json
```

完整参数见 [ParseX 命令参考](https://help.aliyun.com/zh/model-studio/cli/parsex)。

## **Agent Skill**

> 在终端中执行命令安装，请确保已安装 [Node.js](https://nodejs.org/) (≥18) 和 [skills](https://www.npmjs.com/package/skills/v/1.5.12) (≥1.5.12)

支持Agent：qoder、qwen-code、claude-code、openclaw、codex、cursor、gemini-cli、github-copilot

项目安装：

```
npx skills add "https://agenthub.aliyun-inc.com/api/skill-sources/alibabacloud-parse-x" --yes
```

全局安装：

```
npx skills add "https://agenthub.aliyun-inc.com/api/skill-sources/alibabacloud-parse-x" --yes -g
```
