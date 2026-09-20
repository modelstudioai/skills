# 接入 Harness 工具

接入 Token Plan 个人版 Harness 权益提供的 AgentStudio 工具，并示例联网搜索 MCP 的接入流程。

## Harness 权益工具接入

Standard 与 Pro 套餐附赠的 Harness 权益提供联网搜索、图像生成、语音合成、知识库等 AgentStudio 工具。各工具支持 MCP、CLI、API、SDK 等接入方式，具体以控制台 Harness 权益页签标注为准。

接入流程：

1.  在百炼控制台**我的订阅**页面切换到**Harness 权益**页签，查看可用工具。
2.  在工具卡片点击**说明文档**或**AI Native 接入**查看该工具的具体接入方法。
3.  点击**前往控制台**获取对应服务的接入凭证。

Harness 权益的额度与折扣说明详见 [Harness 权益](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-benefits.md)。

## 示例：接入联网搜索增强版

以联网搜索增强版为例，展示 Harness 权益工具的接入流程。联网搜索增强版是 Standard 与 Pro 套餐附赠的 Harness 权益工具，订阅即享每月免费额度与 88 折后付费，无需单独开通，不占用 Credits。额度与折扣详见 [Harness 权益](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-benefits.md)。

### 前提条件

1.  已订阅 Token Plan 个人版 Standard 或 Pro 套餐。
2.  已在 AI 编程工具（如 Claude Code、Qwen Code）中完成接入配置且能正常对话，详见[接入客户端/开发工具](raw/model-user-guide/use-chat-client-or-development-tool.md)。
3.  已获取[百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)（格式为 sk-xxx），用于调用 MCP 服务，与 Token Plan 专属 API Key（格式为 sk-sp-xxx）不同。

### AI Native 接入

联网搜索增强版的完整配置指令如下，复制发给本地 Agent（支持 Qoder、QwenWork、Claude Code、Codex）：

```
## Harness 服务本地配置指南

请按照以下步骤配置 Harness 服务给本地 Agent 使用。

### 前置依赖安装与检查
1. 检查是否安装百炼 CLI，如没有安装请参照如下文档进行安装：https://bailian.aliyun.com/cli/install.md
2. 使用百炼 CLI 完成登录：bl auth login --console
3. 执行如下命令：bl config show，拿到 config_file 文件路径，并读取文件内部 api_key。

### 需要配置的服务 — 自研工具
将以下 MCP 服务器配置写入本地全局配置（请识别准确目录），直接通过 MCP 协议调用，不经 bailian-cli 中转。所有服务的公共信息：
- 类型：HTTP Streamable
- 请求头：Authorization: Bearer ${DASHSCOPE_API_KEY}

需要配置的服务清单：

| 服务名 | URL |
|---|---|
| 联网搜索增强版 | https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp |
```

其他工具请在控制台[**我的订阅**](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)页面切换到**Harness 权益**页签，点击**一键接入**选择工具并复制配置指令。

**说明**使用 AI Native 接入，资源将创建在默认业务空间下。

### 手动接入

直接将 MCP 配置写入本地 Agent 的全局配置。各工具的 MCP 地址在控制台**我的订阅 > Harness 权益**页签的工具卡片获取，API Key 用前提条件中的百炼 API Key（sk-xxx）。

以联网搜索增强版为例，URL 为 `https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp`，请求头 `Authorization: Bearer YOUR_API_KEY`，类型 HTTP Streamable。以下以几个工具为例：

#### OpenCode

```
opencode mcp add EnhancedSearch --url https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp --header "Authorization=Bearer YOUR_API_KEY"
```

进入 OpenCode 后执行 `/mcps` 确认 EnhancedSearch 状态为 connected。

#### Codex

```
codex mcp add EnhancedSearch --url https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp
```

Codex 不支持命令行设鉴权头，需在 `~/.codex/config.toml` 的 `[mcp_servers.EnhancedSearch]` 下添加：

```
[mcp_servers.EnhancedSearch]
url = "https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp"
bearer_token_env_var = "DASHSCOPE_API_KEY"
```

设置环境变量：`export DASHSCOPE_API_KEY=YOUR_API_KEY`

#### Claude Code

```
claude mcp add EnhancedSearch https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"
```

进入 Claude Code 后执行 `/mcp` 确认 EnhancedSearch 状态为 connected。

#### Qwen Code

在 `~/.qwen/settings.json` 的 `mcpServers` 中添加：

```
"EnhancedSearch": {
  "httpUrl": "https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" }
}
```

其他 Harness 权益工具的 MCP 地址同样在控制台**我的订阅 > Harness 权益**页签的工具卡片获取，配置方式相同。
