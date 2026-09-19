# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具调用协议，用于在大模型与外部能力（如地图、搜索、数据库、SaaS 应用等）之间建立安全、统一、可发现的信息通道。它将异构工具抽象为声明式接口，使大模型能在运行时基于自然语言上下文自主规划、选择并调用合适工具，无需开发者手动编写适配胶水代码。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）**：MCP 是智能体“自主决策”的核心支撑。开通 MCP 服务后，在智能体配置中一键勾选（最多 5 个），模型即可根据用户提问自动判断是否调用、调用哪个工具及传入参数（例如：“查上海明天的天气” → 自动调用 `maps_weather` 工具）。所有官方与自定义 MCP 服务在 Agent 2.0 中被统一建模为“工具”，与知识库、函数计算等能力同级调度。

- **工作流（Workflow）**：MCP 以显式节点形式集成。拖入「MCP 节点」→ 选择已开通的服务及具体工具（如 `websearch`）→ 手动配置输入参数（支持引用上游节点输出，如从意图识别节点提取的关键词）→ 将输出结果传递至下游节点。适用于流程确定、需精确控制调用时机与参数的业务场景。

- **Connector（数据连接平台）**：作为 MCP 的规模化落地载体，Connector 将文件、OSS、MySQL、钉钉、语雀等数十类数据源自动封装为标准化 MCP 工具，并通过**单个聚合 MCP 地址**（`https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`）统一暴露。开发者只需配置一次客户端，即可发现并调用全部已连接 App 的能力，实现“一处接入、全域可用”。

- **高代码应用与第三方集成**：通过百炼提供的 MCP SDK（如 `mcp.client.streamable_http`）或标准 HTTP 客户端，可直接对接百炼托管的 MCP endpoint。支持在自有 Python 服务、Cherry Studio、Cursor 等环境中调用，适用于需要深度定制或跨平台复用的工程场景。

> ⚠️ 注意：MCP 不是模型本身，也不替代 RAG 或插件。它是**工具调用层的通信规范**——RAG 提供静态知识，MCP 提供动态能力；插件是历史能力封装方式，MCP 是其演进和统一标准（自定义插件需发布为 MCP 服务后方可被智能体 2.0 调用）。

## 关键参数和配置

MCP 服务的配置围绕**通信方式**与**部署属性**展开，开发者需重点关注以下参数：

| 参数 | 必填 | 说明 | 常见值 | 注意事项 |
|------|------|------|--------|----------|
| `type` | ✅ | 通信协议类型 | `"sse"`、`"streamableHttp"`、`"stdio"` | 必须与服务端点严格匹配：<br>• `type: "sse"` → 对应 `/sse`（GET）<br>• `type: "streamableHttp"` → 对应 `/mcp`（POST）<br>错配将返回错误码 `11200058` 或 `11200059` |
| `url`（HTTP 类型） / `command`（本地类型） | ✅ | 服务地址或启动命令 | `"https://your-server/mcp"` / `"npx mcp-server"` | `url` 需含完整路径（如 `/mcp`），不可省略 |
| `env` | ❌（但强推荐） | 环境变量（用于密钥、配置） | `{"AMAP_MAPS_API_KEY": "xxx"}` | 敏感凭证**必须通过 KMS 加密注入**，禁止明文写入配置 |
| `deploymentMode` | ❌（默认 `basic`） | 部署模式 | `"basic"`（按次计费）、`"ultra"`（极速响应） | `ultra` 模式适用于低延迟关键链路 |
| `region` | ✅（自定义服务） | 部署地域 | `"cn-beijing"` | 必须与业务空间所在地域一致 |

此外，外部客户端调用 MCP 时，需提供两个全局必需参数：
- `DASHSCOPE_API_KEY`：用于鉴权，需在百炼控制台 API Key 页面创建；
- `workspaceId`：业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于路由请求。

## 面向开发者，简洁实用

- ✅ **快速上手**：优先使用官方 MCP 服务（如 Amap Maps、WebSearch），开通即用，无需部署。访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 一键开通。
- ✅ **安全第一**：所有敏感凭证（API Key、OAuth [Token](token.md)、邮箱授权码）必须通过 KMS 加密或环境变量注入，**严禁硬编码或提交至 Git**。
- ✅ **调试技巧**：在智能体测试页开启「工具调用详情」开关，可查看模型生成的工具调用请求/响应原始 JSON，快速定位参数缺失或格式错误。
- ✅ **协议升级**：旧版 SSE 协议已全面升级为 Streamable HTTP（推荐），新服务请默认选用 `type: "streamableHttp"` + `/mcp` 端点。
- ✅ **统一入口**：无论使用 Connector、官方服务还是自定义服务，最终都通过同一个 MCP 协议交互——掌握一种客户端配置，即可接入全部能力。

> 💡 提示：MCP 的本质是“让大模型像人一样调用工具”。你只需定义好工具能做什么（描述）、需要什么（参数）、返回什么（输出结构），剩下的规划、调用、容错，交给百炼智能体自动完成。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)


