# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、可扩展的工具集成协议，用于在大语言模型与外部能力（如地图、搜索、计算、记忆服务等）之间建立安全、声明式的通信通道。它基于开源 MCP 标准（[modelcontextprotocol.io](https://modelcontextprotocol.io/)）实现，并已升级为 **Streamable HTTP 协议**，支持稳定流式交互与生产级集成。

## 在百炼平台的不同场景中如何使用

MCP 不是独立 API，而是深度嵌入百炼应用架构的协议层，仅在以下两类托管式应用中生效：

- **智能体应用（Agent App）**：  
  模型根据对话上下文自动识别调用时机、选择工具并填充参数（如“查上海明天天气” → 自动调用 `weather` MCP 工具）。最多可同时配置 5 个 MCP 服务，由模型自主编排调用顺序与组合逻辑。

- **工作流应用（Workflow App）**：  
  开发者需显式添加 **MCP 节点**，手动指定工具 ID（如 `amap_maps`）、输入参数来源（通常来自前置大模型节点的结构化输出），并定义输出字段如何传递至后续节点（如将经纬度传给图表生成节点）。适用于确定性流程与多系统协同场景。

> ⚠️ 重要限制：MCP **不可直接接入千问 API 原始调用链路**（如 `/v1/chat/completions`）。若需工具调用能力，必须构建智能体或工作流应用，而非调用基础模型接口。

## 关键参数和配置

MCP 的部署与调用依赖以下核心配置项，均在百炼控制台「MCP 服务管理」或应用编排界面中设置：

| 类别 | 参数 | 说明 | 开发提示 |
|------|------|------|----------|
| **服务元信息** | `name`, `description` | 仅用于控制台识别，不影响运行时行为 | 建议用简明英文命名（如 `memory`），便于调试日志定位 |
| **部署方式** | `install_mode`（`npx` / `uvx` / `http`） | 指定服务启动方式：`npx`（Node.js）、`uvx`（Python）、`http`（远程 Streamable HTTP 端点） | 优先选 `http` 模式以规避冷启动；自研服务必须实现 `/tools` 和 `/call` 接口 |
| **运行模式** | `deployment_mode`（`basic` / `ultra`） | `basic`：按次计费，有冷启动延迟；`ultra`：常驻内存，按部署时长+调用次数双计费 | 高频调用场景务必选 `ultra`，避免响应抖动 |
| **连接配置** | `mcpServers`（JSON 对象） | 定义服务映射关系，格式：`{ "tool_id": { "command": "...", "args": [...], "env": { "API_KEY": "kms://..." } } }` | `tool_id` 必须与工具实际注册名一致（如 `maps_weather`），且全小写、无空格 |
| **安全凭证** | KMS 加密变量（如 `AMAP_MAPS_API_KEY`） | 所有敏感凭据必须通过 KMS 密钥加密后填入 `env` 字段 | 明文填写将导致部署失败；KMS 密钥需授予百炼服务角色权限 |

## 面向开发者的实用建议

- ✅ **快速上手**：直接从 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通官方服务（如 Amap Maps、Memory），无需配置即可在智能体中调用。  
- ✅ **自定义服务**：推荐使用 **AI 网关导入** 方式，将现有 RESTful API 封装为 MCP 工具（自动处理鉴权、参数映射、错误重试）；比 `npx`/`uvx` 更易维护。  
- ✅ **调试技巧**：在工作流中启用「节点日志」，查看 MCP 调用的完整请求/响应体（含 `tool_id`、`input`、`output`）；智能体调试可开启 `debug: true` 获取工具决策链路。  
- ❌ **避坑提醒**：  
  - 不要尝试在 Assistant API 或 DashScope SDK 中直接传入 MCP 配置——它不被识别；  
  - MCP 服务无法访问用户本地文件或设备，需本地部署的工具请改用客户端 SDK 直连；  
  - 升级 Streamable HTTP 后，旧版 SSE 配置（`type: "sse"`）将失效，需重新开通服务。  

MCP 的本质是「让模型像调用函数一样调用世界」。专注定义 *要什么*（工具语义），而非 *怎么连*（网络细节）——这是百炼平台对 AI 应用工程化的关键抽象。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)
- [managed agents api](../api/managed-agents-api.md)


