# MCP 与工具扩展

MCP 与工具扩展是百炼平台为大模型补齐能力边界的统一机制：通过 MCP（Model Context Protocol）标准协议、插件（Plugin）和 Skill 等形式，让智能体、工作流应用能够调用外部工具、执行代码、处理文件，从而突破大模型在实时信息、精确计算、私有数据访问等方面的原生局限。

## 三类扩展能力对比

百炼提供多种工具扩展形态，适用场景各有侧重：

| 扩展形态 | 本质 | 接入方式 | 典型场景 |
| --- | --- | --- | --- |
| MCP 服务 | 大模型与外部工具间的标准协议通道 | MCP 广场开通/部署后接入智能体或工作流 | 地图、搜索、图表、阿里云 OpenAPI 等第三方工具 |
| 插件（Plugin） | 工具集合，一个插件含多个工具（API） | 组件广场添加到智能体，或经 Assistant API 调用 | 代码解释器、计算器、图片生成、搜索等 |
| Skill | 可扩展能力包，封装端到端任务流程 | 上传 ZIP 技能包添加到智能体 | 文件处理、数据分析（如 xlsx 处理） |

三者可组合使用：新版智能体（Agent 2.0）和 Managed Agents 将知识库、MCP、插件、Skill 统一为工具，由智能体自主规划调用顺序。

## MCP：标准协议接入

MCP 是 Anthropic 提出的开源标准，百炼基于它提供全周期服务，免去为每个外部工具编写专用接口的成本。

### 服务类型

- **官方 MCP 服务**：百炼云端部署，开通即用（如 Amap Maps、Sequential Thinking、QuickChart、联网搜索 WebSearch）。
- **自定义 MCP 服务**：开发者自行部署，三种方式——脚本部署（托管到函数计算 FC，支持 `npx` / `uvx` / `http`）、从 AI 网关导入（RESTful API 升级为 MCP）、从阿里云 OpenAPI 导入（操作 OSS、ECS 等）。

### 使用方式

- **智能体应用**：模型根据对话内容自主判断是否调用，单个智能体最多同时添加 **5 个** MCP 服务，支持多工具组合与动态非固定顺序调用。
- **工作流应用**：每个 MCP 节点只能用一个工具，需手动指定输入参数；通常先用大模型节点把自然语言解析为工具所需参数，再接入 MCP 节点。
- **外部调用**：可集成到 Cherry Studio、Cursor 等第三方客户端，或通过 MCP SDK 编码接入个人项目。

### 关键参数与配置

- **传输协议**：`type` 字段须与端点路径一致，`"sse"` 对应 GET `/sse`，`"streamableHttp"` 对应 POST `/mcp`，不匹配会触发 405/404 错误。百炼已从旧版 SSE 升级为 **Streamable HTTP**，已开通用户需在 MCP 广场执行"取消开通 → 立即开通"完成升级，SDK 使用 `streamablehttp_client`。
- **鉴权**：外部调用使用 `Authorization: Bearer <DASHSCOPE_API_KEY>`，端点如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
- **脚本部署配置示例**：

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

- **敏感信息**：涉及敏感数据的服务在创建时用 KMS 凭据加密管理。
- **部署后修改**：仅支持编辑名称和描述；改部署方式、地域、安装方式或配置须先停止再重新部署。

### MCP 限制

- 不能直连千问 API，必须集成在智能体或工作流中使用。
- 自定义 MCP 托管在 FC，暂不支持访问本地资源；访问远程资源需配置 IP 白名单或打通 VPC。
- 私有 npm 仓库不支持；npx/uvx 部署的服务源版本更新后不会自动更新，需手动重新部署。
- 调用会将返回内容作为上下文传入模型，增加输入 Token 消耗。

## 插件：工具集合

插件是一个工具集合，分官方、三方、自定义三类。官方插件（如 `code_interpreter`、`calculator`、`text_to_image`、`quark_search`、`generate_qrcode`、`github_search`）无需配置输入输出参数即可直接调用。

- **支持模型**：qwen-turbo、qwen-plus、qwen-max、qwen-vl-max、qwen-vl-plus。
- **调用机制**：智能体应用 / Assistant API 由模型判断是否调用；工作流应用中插件作为节点按编排执行。
- **调用配额**：每个智能体应用最多添加 **10 个** 工具；通过 API 调用需正确传递工具 ID（如 `calculator`）。
- **授权**：首次访问需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 子账号需主账号先授予 `ram:CreateServiceLinkedRole` 权限。

## Skill：能力包

Skill 是智能体的可扩展能力包，让智能体在对话中自动识别并处理特定任务（如文件处理、数据分析），无需额外编码。分官方 Skill（自动更新）和自定义 Skill（上传 ZIP）。

- ZIP 包根目录必须含 `SKILL.md`，用 YAML 定义 `name`（唯一，建议小写连字符）和 `description`。
- `description` 质量直接决定智能体调用准确率，建议包含适用输入类型、支持的操作、触发关键词、不适用场景。
- ZIP 包大小不超过 **10 MB**；重新上传同名包生成新版本，已添加的智能体自动使用最新版。

## Managed Agents 中的工具

Managed Agents 智能体托管运行时内置 7 个工具：命令执行 `bash`，文件操作 `read`、`write`、`edit`、`glob`、`grep`、`download_file`，并支持接入 MCP 服务与 Skill。工具在独立云端沙箱执行，事件历史服务端持久化，支持中断与续接，适合多步工具调用、代码执行等长时任务。

## 计费要点

- **云部署 MCP**：限时免部署费；联网搜索免费额度 2000 次，用尽后 29 元/千次，限流 15 QPS。
- **自定义部署 MCP**：基础模式无部署费、按调用时长 0.000156 元/秒计费（有冷启动）；极速模式部署费 0.000036 元/秒 + 调用费 0.000156 元/秒，适合高频在线场景。
- **插件**：多为免费或限时免费（部分需申请开通）。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents](../guides/managed-agents.md)
- [skill](../guides/skill.md)
- [llm application](../guides/llm-application.md)


