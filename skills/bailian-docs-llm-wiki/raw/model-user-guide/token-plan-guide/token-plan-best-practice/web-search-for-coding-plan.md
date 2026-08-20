# 联网搜索

在 Token Plan 支持的编程工具中添加联网搜索工具，使模型能够检索实时信息。

## 适用范围

本文适用于需要通过 MCP 扩展联网搜索能力的工具，如 Qwen Code、Claude Code 等。部分工具（如 Cursor）已内置联网搜索功能，无需额外添加联网搜索服务。

## 前提条件

1.  已订阅 [Token Plan](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription)，详情请参见[快速开始](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。
2.  已在 Token Plan 支持的工具（如 Claude Code、Qwen Code）中完成接入配置，且能正常对话，详情请参见[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool)。
3.  已获取[百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)。此处的 API Key 为百炼通用 API Key（格式为 sk-xxx），用于调用 MCP 服务，与 Token Plan 专属 API Key（格式为 sk-sp-xxx）不同。

## 开通或升级联网搜索 MCP

联网搜索 MCP 已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。请根据您的情况选择对应的操作步骤：

#### 首次开通（新用户）

1.  进入百炼的[MCP广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)，找到**联网搜索** MCP 服务。
    
2.  单击**立即开通确认开通**。
    
    -   联网搜索 MCP 全部用户前 2000 次调用免费，免费额度用尽后按 29 元/千次计费。如果使用第三方 MCP 服务，该 MCP 服务可能收费，以 MCP 服务的介绍信息为准。
    -   部分MCP服务支持**个人FC资源部署**，按实际调用时长和次数计费，适用于需要专属资源、指定资源地域等场景。
3.  开通成功后，可以获取以下配置信息：
    
    1.  **Streamable HTTP Endpoint**：MCP 服务的连接地址。联网搜索 MCP 的连接地址为`https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
    2.  **API Key**：即百炼 API Key，是 MCP 服务的鉴权密钥。

#### 升级协议（已开通用户）

1.  进入百炼的[MCP广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)，找到**联网搜索** MCP 服务。
    
2.  单击右侧**取消开通**，再单击**立即开通确认开通**。
    
    -   联网搜索 MCP 全部用户前 2000 次调用免费，免费额度用尽后按 29 元/千次计费。如果使用第三方 MCP 服务，该 MCP 服务可能收费，以 MCP 服务的介绍信息为准。
    -   部分MCP服务支持**个人FC资源部署**，按实际调用时长和次数计费，适用于需要专属资源、指定资源地域等场景。
3.  重新开通成功后，即完成协议升级，可以获取以下配置信息：
    
    1.  **Streamable HTTP Endpoint**：MCP 服务的连接地址。联网搜索 MCP 的连接地址为`https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
    2.  **API Key**：即百炼 API Key，是 MCP 服务的鉴权密钥。

## 接入工具

将 MCP 服务添加到 AI 编程工具中。

#### OpenClaw

1.  在终端执行如下命令安装 MCPorter。

```
npm install -g mcporter
```

2.  在终端执行如下命令，启用 MCPorter。

```
openclaw config set skills.entries.mcporter.enabled true
```

3.  在`~/.openclaw /workspace`目录下，执行如下命令。执行命令前，将命令中的 YOUR\_API\_KEY 替换为[开通或升级联网搜索 MCP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan#da7cd47fa8pcd)时获取的阿里云百炼 API Key。

```
mcporter config add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp --transport http --header "Authorization=Bearer YOUR_API_KEY" --scope home
```

4.  在`~/.openclaw /workspace`目录下，执行如下命令确认MCP已安装。

```
mcporter list
```
```
mcporter 0.7.3 — Listing 1 server(s) (per-server timeout: 30s)
- websearch (1 tool, 2.4s)
[ok] Listed 1 server (1 healthy).
```

5.  在终端执行如下命令使配置生效。

```
openclaw gateway restart
```

6.  发送提问`用 mcporter 搜索阿里云的新闻`即可看到搜索结果。
    
    系统返回包含 4 条阿里云相关新闻的卡片，每条新闻显示标题、来源及发布时间，底部提示是否需要抓取某篇新闻的详细内容。
    

#### OpenCode

1.  在 OpenCode 配置文件`~/.config/opencode/opencode.json`中写入 MCP 配置信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。

```
{
  "mcp": {
    "WebSearch": {
      "type": "remote",
      "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

若`opencode.json`中已有其他配置（如 provider），将 mcp 字段合并到现有配置中即可。配置完成后，保存文件。 2. 在终端中执行以下命令进入 OpenCode。

```
opencode
```

3.  在对话框执行`/mcps`确认`websearch`状态是否为 Enabled。确认后按 Esc 退出。
    
4.  发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

```
已为您搜索到最新的阿里云相关新闻：
主要新闻摘要
1. 阿里云2026年战略目标
阿里云目标在2026年拿下中国AI云市场增量的80%，重点发力MaaS（模型即服务）和GPU算力服务。
目前阿里云上调用大模型API的客户中，有七成同时使用其GPU算力服务。
2. 阿里云服务器2026年优惠活动
- 最便宜服务器：38元/年（2核2G、200M峰值带宽）
- 99元/年 ECS服务器（新老用户同享，续费同价）
- 199元/年企业专享服务器（2核4G、5M带宽）
3. AI自动化工具生态
阿里云推出OpenClaw（原Clawdbot）AI
自动化代理工具部署方案，支持一键部署到轻量应用服务器，可与阿里云百炼大模型无缝联动。
4. 企业智能客服
瓴羊Quick Service智能客服平台基于通义千问大模型，提供大模型驱动的语义理解、多轮对话、
知识库智能生成等功能。
```

#### Claude Code

1.  添加联网搜索MCP服务。
    
    1.  将以下命令复制到终端。

```
claude mcp add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"
```

2.  将命令中的 YOUR\_API\_KEY 替换为[开通或升级联网搜索 MCP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan#da7cd47fa8pcd)时获取的阿里云百炼 API Key。
    
3.  在终端执行更新后的命令。
    
    **说明**终端返回`Added HTTP MCP server WebSearch with URL: ... to local config`并不代表 MCP 添加成功，其连接状态需通过以下步骤确认。
    
4.  在终端执行以下命令进入 Claude Code。
    

```
claude
```

3.  在对话框执行`/mcp`命令，确认`websearch`的状态为 connected。首次添加可能需要等待状态从 connecting 变成 connected。
    
    若连接状态显示 failed，请选中该 MCP 并选择 Reconnect 重连。若重试 1-2 次仍失败，请核实配置。
    

```
/mcp
WebSearch MCP Server
Status: [ok] connected
Auth: [ok] authenticated
URL: https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp
xxx
Capabilities: tools
Tools: 1 tools
  1. View tools
  2. Re-authenticate
  3. Clear authentication
> 4. Reconnect
  5. Disable
```

4.  按 Esc 退出 MCP 列表后，发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

```
> 用websearch MCP搜索阿里云的新闻
* websearch – bailian_web_search (MCP)(query: "阿里云 新闻", count: 10)
  └ {
      "status": 0,
      "pages": [
    … +51 lines (ctrl+o to expand)
    ]
  }
* 搜索结果已返回，以下是阿里云的最新新闻摘要：
  阿里云近期新闻
  1. 编程模型订阅服务推出（2026 年 2 月 25 日）
  阿里云百炼推出 Coding Plan 编程模型订阅服务，包含四款开源模型 API：
  - Qwen3.5、GLM-5、MiniMax M2.5、Kimi K2.5
  - 用户可在 Qwen Code、Claude Code、Cline 等 AI 工具上无缝切换使用
  - 降低开发者模型选型与接入成本
  2. 千问 3.5 新模型开源（2026 年 2 月 25 日）
  阿里发布三款中型千问 3.5 新模型：
  - Qwen3.5-35B-A3B、Qwen3.5-122B-A10B、Qwen3.5-27B
  - 基于 Qwen3.5-35B-A3B 的托管模型 Qwen3.5-Flash 已上线阿里云百炼
  - 每百万 Token 输入低至 0.2 元
  3. 市场表现亮眼
  - 千问（Qwen）大模型调用量占比跃升至 32.1%，排名中国企业级大模型第一
  - 2026 财年第二季度收入 398.24 亿元，同比增长 34%
  - AI 相关产品收入连续第九个季度实现三位数增长
```

#### Qwen Code

1.  添加联网搜索 MCP。
    
    1.  将以下命令复制到终端。

```
qwen mcp add WebSearch \
  -t http \
  "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

2.  将命令中的 YOUR\_API\_KEY 替换为[开通或升级联网搜索 MCP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan#da7cd47fa8pcd)时获取的阿里云百炼 API Key。
    
3.  在终端执行更新后的命令。
    
    **说明**终端返回`MCP server "WebSearch" added to user settings. (http)`并不代表 MCP 添加成功，其连接状态需通过以下步骤确认。
    
4.  在终端执行以下命令进入 Qwen Code。
    

```
qwen
```

3.  在`Qwen Code`对话框执行`/mcp`命令以确认 MCP 连接状态。

```
> /mcp
Configured MCP servers:
* WebSearch – Ready (1 tool)
  Tools:
  – mcp__WebSearch__bailian_web_search
[tip] Tips:
  – Use /mcp desc to show server and tool descriptions
  – Use /mcp schema to show tool parameter schemas
  – Use /mcp nodesc to hide descriptions
  – Use /mcp auth <server-name> to authenticate with OAuth-enabled servers
  – Press Ctrl+T to toggle tool descriptions on/off
```

4.  发送提问`用 websearch MCP 搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及`websearch MCP`。
    

```
* 搜索结果已返回，我需要整理并总结其中与阿里云相关的主要新闻信息，以清晰的方式呈现给用户。
* 已为您搜索到阿里云相关新闻，以下是主要内容：
  阿里云最新动态
  1. 阿里云千问大模型表现亮眼
   - 2025 年下半年，阿里云千问（Qwen）在中国企业级大模型市场占比跃升至32.1%，几乎翻倍（上半年为
     17.7%），位居第一
   - 字节豆包占比 21.3% 排名第二，DeepSeek 占比 18.4% 排名第三
  2. AI 战略投入
   - 阿里豪掷3800 亿元押注 AI 基础设施
   - 2026 年，阿里云将 AI 相关收入目标增速上调至200%
   - 2026 年 2 月推出30 亿元"春节请客计划"，联合淘宝、飞猪、盒马等以免单形式发放福利
  3. Coding Plan 服务更新
   - 阿里云 Coding Plan 订阅服务新增支持 Qwen 3.5-Plus、GLM-4.7、Kimi-K2.5 等编程模型
   - 新用户首月首购享两折优惠
  4. 技术进展
   - 除夕夜开源的千问 Qwen3.5-Plus 采用混合注意力机制和稀疏 MoE 架构
   - 总参数 3970 亿，激活 170 亿，推理速度达主流模型的 2 倍
  需要我为您搜索更具体的阿里云新闻主题吗？
> 输入您的消息或 @ 文件路径
按 ? 查看快捷键                                              1.8% context used
```

#### Cline

1.  点击MCP Servers，进入Configure页面，点击Configure MCP Servers。
    
2.  在配置文件`cline_mcp_settings.json`中写入 MCP 配置信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。配置完成后，保存文件。
    

```
{
  "mcpServers": {
    "websearch": {
      "type": "http",
      "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      },
      "disabled": false
    }
  }
}
```

3.  配置完成后，在Configure页面下可以查看MCP的相关信息。
    
4.  新开对话，发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

#### Kilo CLI

1.  在配置文件`~/.config/kilo/opencode.json`中写入 MCP 配置信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。配置完成后，保存文件。

```
{
  "mcp": {
    "websearch": {
      "type": "remote",
      "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

若`opencode.json`中已有其他配置（如 provider），将 mcp 字段合并到现有配置中即可。配置完成后，保存文件。 2. 在终端中执行以下命令查看 MCP 状态。Connected 即表示连接成功。

```
kilocode mcp list
```
```
MCP Servers
│
* [ok] websearch connected
│     https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp
│
└ 1 server(s)
```

3.  在终端中执行以下命令进入 Kilo CLI。

```
kilo
```

4.  发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

```
以下是阿里云的最新新闻要点：
阿里云千问大模型市场份额跃升第一
- 市场份额翻倍：根据沙利文2026年2月报告，阿里云千问（Qwen）占比跃升至*32.1%*，相较2025年上半年的17.7%几乎翻倍，超越字节豆包（21.3%）和DeepSeek(18.4%)，成为企业级大模型市场第一
- 日均调用量激增：2025年下半年中国企业级大模型日均调用量达37.0万亿tokens，较上半年增长263%
AI基础设施投资战略
- 3800亿元投资：阿里宣布豪掷3800亿元押注AI基础设施
- 收入目标：2026年将AI相关收入目标增速上调至200%
- 市场目标：阿里云目标拿下中国AI云市场增量的80%
千问模型技术进展
- 开源Qwen3.5-Plus：除夕夜开源，采用混合注意力机制和稀疏MoE架构
- 高效能设计：总参数3970亿，仅激活170亿，推理速度达到主流模型的2倍
- 春节免单计划：千问启动30亿元"春节请客计划"，联合淘宝、飞猪、盒马等生态业务发放福利
其他动态
- Coding Plan上新：支持千问3.5、GLM-4.7、Kimi-K2.5等编程模型，新用户首月两折优惠
- 云服务器优惠：轻量应用服务器38元/年起，200M带宽不限流量
Code · kimi-k2.5 · 49.8s
```

#### Kilo Code IDE 插件

1.  打开Kilo Code IDE插件配置联网搜索 MCP 信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。配置完成后，保存文件。
    
    依次单击左上角齿轮图标，在侧边栏选择 **Agent Behaviour**，单击 **MCP Servers** 页签，然后单击底部 **Edit Global MCP** 按钮，打开 `mcp_settings.json` 配置文件，将以下 JSON 内容粘贴并保存。
    

```
{
  "mcpServers": {
    "websearch": {
      "type": "streamable-http",
      "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

当联网搜索的MCP状态显示为绿色时，表示添加成功。 2. 返回对话界面，发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。

> 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。

## 常见问题

### 无法连接联网搜索 MCP 服务怎么办？

常见原因及排查方式：

1.  **未开通或者未升级联网搜索 MCP 服务**：请确认已在百炼 MCP 广场开通或升级联网搜索 MCP 服务，详情请参见[开通或升级联网搜索 MCP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan#da7cd47fa8pcd)。
    
2.  **Streamable HTTP Endpoint 地址错误**：
    
    -   请检查 URL 是否拼写正确，完整 URL 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
    -   如果使用的 URL 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse`，说明开通的是旧版 SSE 协议，请将协议[升级至Streamable HTTP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan#da7cd47fa8pcd)。
3.  **API Key 错误**：请确认使用了有效的百炼通用 API Key（格式为 sk-xxx，非 Token Plan 专属 API Key），并已在命令中正确替换 YOUR\_API\_KEY。
    
4.  **免费额度用尽**：联网搜索 MCP 全部用户前 2000 次调用免费，免费额度用尽后按 29 元/千次计费，请确认账户余额充足。
    
5.  **网络不通**：确认当前网络可以访问。
    

### 对话中模型没有调用联网搜索怎么办？

1.  请确保联网搜索 MCP 服务连接成功并可用。
2.  在对话中明确提及工具名称，例如：`用 websearch MCP 搜索阿里云的新闻`。
