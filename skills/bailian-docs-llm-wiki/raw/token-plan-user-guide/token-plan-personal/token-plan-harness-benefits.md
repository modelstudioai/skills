# Harness 权益

Token Plan 个人版 Standard 与 Pro 套餐附赠 Harness 权益，覆盖 AgentStudio 工具的每月免费额度与后付费折扣，使用百炼 API Key 调用，不占用套餐 Credits。

<a id="权益概览"></a>

<a id="tphb-h-overview"></a>

## 权益概览

Standard 与 Pro 套餐在模型 Credits 之外，额外附赠 Harness 权益：

-   **每月免费额度**：覆盖联网搜索、图像生成、语音合成等 AgentStudio 工具，额度按月发放。
-   **后付费 88 折**：免费额度用尽后，超出部分按原目录价 88 折继续计费。
-   **不占用 Credits**：Harness 权益消耗独立计量，不从套餐 Credits 或用量包抵扣。

Lite 与 Essential 套餐不包含 Harness 权益；团队版不支持 Harness 权益。

<a id="工具与每月免费额度"></a>

<a id="tphb-h-tools"></a>

## 工具与每月免费额度

下表为 Standard 与 Pro 套餐各工具的每月免费额度，未列免费额度的工具仅享 88 折后付费。

<table><thead><tr><th><p><strong>分类</strong></p></th><th><p><strong>工具</strong></p></th><th><p><strong>Standard 每月额度</strong></p></th><th><p><strong>Pro 每月额度</strong></p></th></tr></thead><tbody><tr><td rowspan="8"><p>自研工具</p></td><td><p>联网搜索增强版</p></td><td><p>100 次</p></td><td><p>500 次</p></td></tr><tr><td><p>垂类搜索</p></td><td><p>100 次</p></td><td><p>500 次</p></td></tr><tr><td><p>网页解析</p></td><td><p>1,000 次</p></td><td><p>5,000 次</p></td></tr><tr><td><p>图像生成</p></td><td><p>20 张</p></td><td><p>50 张</p></td></tr><tr><td><p>语音合成</p></td><td><p>1 万字符</p></td><td><p>1 万字符</p></td></tr><tr><td><p>语音识别</p></td><td><p>5 小时</p></td><td><p>5 小时</p></td></tr><tr><td><p>视频生成</p></td><td><p>—</p></td><td><p>—</p></td></tr><tr><td><p>代码解释器</p></td><td><p>100 次</p></td><td><p>500 次</p></td></tr><tr><td><p>百炼知识库</p></td><td><p>知识库 RAG</p></td><td><p>—</p></td><td><p>—</p></td></tr><tr><td><p>百炼记忆库</p></td><td><p>记忆库 Memory</p></td><td><p>—</p></td><td><p>—</p></td></tr><tr><td><p>百炼全托管智能体</p></td><td><p>托管智能体 Managed Agent</p></td><td><p>—</p></td><td><p>—</p></td></tr><tr><td><p>百炼沙箱</p></td><td><p>云沙箱 Sandbox</p></td><td><p>—</p></td><td><p>—</p></td></tr></tbody></table>

“—”表示该工具无每月免费额度，仍享 88 折后付费。额度数值与折扣以[控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)订阅页展示为准。

<a id="计费与抵扣"></a>

<a id="tphb-h-billing"></a>

## 计费与抵扣

-   Harness 权益消耗独立计量，不从套餐 Credits 或用量包抵扣。
-   免费额度优先抵扣；用尽后超出部分按原目录价 88 折后付费。
-   Harness 权益与模型 Credits 抵扣相互独立，两者不混算。
-   **API Key 说明**：Harness 权益工具通过百炼 API Key（格式为 sk-xxx）调用 MCP 服务，消耗计入 Harness 权益额度与折扣；与 Token Plan 专属 API Key（格式为 sk-sp-xxx，用于模型调用、按 Credits 抵扣）不同，两者不可混用。

> **重要**
>
> 查看各工具的折后单价与折扣明细，在控制台 Harness 权益页签点击对应工具的“查看明细”。

<a id="额度升配"></a>

<a id="tphb-h-upgrade"></a>

### 额度升配

套餐升级后（如从 Standard 升到 Pro），Harness 权益的剩余额度按以下公式计算：

<a id="code-block"></a>

```text
剩余权益额度 =（原档位总次数 − 已用次数）+（新档位总次数 − 原档位总次数）× 剩余天数 ÷ 30
```

-   原档位总次数 − 已用次数：原档位剩余次数，直接继承。 -（新档位总次数 − 原档位总次数）× 剩余天数 ÷ 30：新档位比原档位多的额度，按剩余天数折算补偿。

向上取整，具体以控制台升级页展示为准。

例如：Standard 每月 100 次、已用 20 次，Pro 每月 500 次，剩余 10 天，则剩余 = (100−20) + (500−100)×10÷30 ≈ 214 次。

<a id="接入-harness-工具"></a>

<a id="tpha-h-access"></a>

## 接入 Harness 工具

Standard 与 Pro 套餐附赠的 Harness 权益提供联网搜索、图像生成、语音合成、知识库等 AgentStudio 工具。各工具支持 MCP、CLI、API、SDK 等接入方式，具体以控制台 Harness 权益页签标注为准。

接入流程：

1.  在百炼控制台**我的订阅**页面切换到**Harness 权益**页签，查看可用工具。
2.  在工具卡片点击**说明文档**或**AI Native 接入**查看该工具的具体接入方法。
3.  点击**前往控制台**获取对应服务的接入凭证。

<a id="示例-接入联网搜索增强版"></a>

<a id="tpha-h-example"></a>

### 示例：接入联网搜索增强版

以联网搜索增强版为例，展示 Harness 权益工具的接入流程。联网搜索增强版是 Standard 与 Pro 套餐附赠的 Harness 权益工具，订阅即享每月免费额度与 88 折后付费，无需单独开通，不占用 Credits。额度与折扣见上文。

<a id="前提条件"></a>

<a id="6571295485s9e"></a>

#### 前提条件

1.  已订阅 Token Plan 个人版 Standard 或 Pro 套餐。
2.  已在 AI 编程工具（如 Claude Code、Qwen Code）中完成接入配置且能正常对话，详见[接入客户端/开发工具](../use-chat-client-or-development-tool.md)。
3.  已获取[百炼 API Key](../../model-api-reference/preparations/get-api-key.md)（格式为 sk-xxx），用于调用 MCP 服务，与 Token Plan 专属 API Key（格式为 sk-sp-xxx）不同。

<a id="ai-native-接入"></a>

<a id="tpha-h-ainative"></a>

#### AI Native 接入

联网搜索增强版的完整配置指令如下，复制发给本地 Agent（支持 Qoder、QwenWork、Claude Code、Codex）：

<a id="code-block-2"></a>

```text
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

> **说明**
>
> 使用 AI Native 接入，资源将创建在默认业务空间下。

<a id="手动接入"></a>

<a id="tpha-h-mcpconfig"></a>

#### 手动接入

直接将 MCP 配置写入本地 Agent 的全局配置。各工具的 MCP 地址在控制台**我的订阅 > Harness 权益**页签的工具卡片获取，API Key 用前提条件中的百炼 API Key（sk-xxx）。

以联网搜索增强版为例，URL 为 `https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp`，请求头 `Authorization: Bearer YOUR_API_KEY`，类型 HTTP Streamable。以下以几个工具为例：

<a id="sec-tabs"></a>

<a id="opencode"></a>

<a id="opencode-h4"></a>

#### OpenCode

<a id="code-block-3"></a>

```bash
opencode mcp add EnhancedSearch --url https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp --header "Authorization=Bearer YOUR_API_KEY"
```

进入 OpenCode 后执行 `/mcps` 确认 EnhancedSearch 状态为 connected。

<a id="codex"></a>

<a id="codex-h4"></a>

#### Codex

<a id="code-block-4"></a>

```bash
codex mcp add EnhancedSearch --url https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp
```

Codex 不支持命令行设鉴权头，需在 `~/.codex/config.toml` 的 `[mcp_servers.EnhancedSearch]` 下添加：

<a id="code-block-5"></a>

```toml
[mcp_servers.EnhancedSearch]
url = "https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp"
bearer_token_env_var = "DASHSCOPE_API_KEY"
```

设置环境变量：

<a id="sec-tabs-2"></a>

<a id="macos-linux"></a>

<a id="macos-linux-h4"></a>

#### macOS / Linux

<a id="code-block-6"></a>

```bash
export DASHSCOPE_API_KEY=YOUR_API_KEY
```

<a id="windows-powershell"></a>

<a id="windows-powershell-h4"></a>

#### Windows PowerShell

<a id="code-block-7"></a>

```powershell
$env:DASHSCOPE_API_KEY="YOUR_API_KEY"
```

引用变量时使用 `$env:DASHSCOPE_API_KEY`。

<a id="windows-cmd"></a>

<a id="windows-cmd-h4"></a>

#### Windows CMD

<a id="code-block-8"></a>

```batch
set DASHSCOPE_API_KEY=YOUR_API_KEY
```

<a id="claude-code"></a>

<a id="claude-code-h4"></a>

#### Claude Code

<a id="code-block-9"></a>

```bash
claude mcp add EnhancedSearch https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"
```

进入 Claude Code 后执行 `/mcp` 确认 EnhancedSearch 状态为 connected。

<a id="qwen-code"></a>

<a id="qwen-code-h4"></a>

#### Qwen Code

在 `~/.qwen/settings.json` 的 `mcpServers` 中添加：

<a id="code-block-10"></a>

```json
"EnhancedSearch": {
  "httpUrl": "https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" }
}
```

其他 Harness 权益工具的 MCP 地址同样在控制台**我的订阅 > Harness 权益**页签的工具卡片获取，配置方式相同。

<a id="注意事项"></a>

<a id="tphb-h-notes"></a>

## 注意事项

-   **权益归属**：Harness 权益为 Standard 与 Pro 套餐附赠，随订阅周期发放；续费、升配后的权益发放规则以控制台展示为准。
-   **额度刷新**：每月免费额度按订阅周期发放，未用完的额度不结转，具体刷新规则以控制台为准。
-   **退订**：个人版不支持自助退订；Harness 权益随订阅失效而终止。
-   **地域**：Token Plan 个人版目前仅支持华北2（北京）地域。

<a id="常见问题"></a>

<a id="tphb-h-faq"></a>

## 常见问题

<a id="accordion-harness-权益的抵扣顺序是什么"></a>

Harness 权益的抵扣顺序是什么？

<a id="tphb-h-faq-order"></a>

先抵扣对应服务本身的免费额度（如各产品自带的试用/新用户额度），再抵扣 Token Plan 附赠的权益额度；权益额度用尽后，超出部分按对应服务的折扣价继续按量计费。

<a id="accordion-harness-调用使用哪个-api-key"></a>

Harness 调用使用哪个 API Key？

<a id="tphb-h-faq-apikey"></a>

Harness 服务（联网搜索、图像生成、代码解释器、RAG、Memory、Managed Agent、Sandbox 等）使用百炼 API Key（以 `sk-` 开头）和百炼标准 Base URL 接入。系统自动识别账号下的 Token Plan 订阅并应用附赠权益，无需切换到 Token Plan 专属凭证。Token Plan 专属 API Key（以 `sk-sp-` 开头）仅用于模型调用抵扣 Credits，不用于 Harness 服务。

<a id="accordion-harness-调用会消耗套餐-credits-吗"></a>

Harness 调用会消耗套餐 Credits 吗？

<a id="tphb-h-faq-credits"></a>

不会。Harness 权益独立核算，调用只扣自身权益次数/额度，超出部分按折扣价走按量账单，不占用套餐 Credits，也不占用用量包。

<a id="accordion-在哪查看-harness-权益的剩余额度"></a>

在哪查看 Harness 权益的剩余额度？

<a id="tphb-h-faq-view"></a>

在百炼控制台**我的订阅**页面切换到**Harness 权益**页签，查看各工具的免费额度发放状态、剩余次数与到期时间。

<a id="accordion-加量包能否抵扣-harness-服务的费用"></a>

加量包能否抵扣 Harness 服务的费用？

<a id="tphb-h-faq-bundle"></a>

不能。用量包仅用于补充 Token Plan 套餐的模型 Credits 额度，Harness 权益独立核算，超出权益部分按对应服务的折扣价走按量账单，不占用用量包。
