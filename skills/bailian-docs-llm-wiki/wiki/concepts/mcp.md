# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、可扩展的工具接入协议，用于在大语言模型与外部能力（如地图、搜索、数据库、SaaS 应用等）之间建立安全、声明式的通信通道。它基于开源 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并升级为 Streamable HTTP 协议，支持稳定流式调用与统一工具发现。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用**：在「工具」配置区添加 MCP 服务后，模型根据用户提问语义自动判断是否调用、调用哪个工具及传入哪些参数（例如：“北京明天天气如何？” → 自动触发 `maps_weather` 工具）。最多同时启用 5 个 MCP 服务。
- **工作流应用**：通过拖拽「MCP 节点」手动编排调用逻辑，显式指定工具 ID（如 `websearch_search`）、输入参数（支持引用上游节点输出），适用于确定性、多步骤的工具协同场景。
- **Connector 数据连接平台**：所有 Connector 接入的业务系统（文件、OSS、MySQL、Salesforce、钉钉等）均被封装为 MCP 兼容工具，对外暴露统一 `/mcp` 接口，供智能体或外部客户端按需调用。
- **插件生态集成**：自定义插件发布时，必须先注册为 MCP 服务；官方/三方插件虽可直连，但其底层能力若需跨系统调度（如访问私有数据库），仍需通过 MCP 协议网关完成权限隔离与协议转换。

> ⚠️ 注意：MCP 服务**不支持直接集成到千问 API 原生调用链中**（如 `dashscope.ChatCompletion.create`），仅限智能体和工作流应用内配置使用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `type` | string | 是 | 协议类型，决定通信方式与端点路径 | `"sse"`（对应 `/sse` GET）、`"streamableHttp"`（对应 `/mcp` POST） |
| `url` 或 `command` | string / array | 是 | 远程服务地址 或 本地启动命令（如 npx/uvx） | `"https://your-server/mcp"` 或 `["npx", "-y", "@modelcontextprotocol/server-memory"]` |
| `env` | object | 否 | 环境变量，敏感信息必须使用 `kms://` 前缀加密 | `{"API_KEY": "kms://ak-xxx"}` |
| `deploymentMode` | string | 否 | 部署模式，影响计费与延迟 | `"basic"`（冷启动，按调用时长计费）、`"premium"`（常驻在线，按部署+调用双计费） |

> ✅ 配置校验要点：  
> - `type` 必须与 `url` 路径严格匹配（`"sse"` → `/sse`；`"streamableHttp"` → `/mcp`），否则返回 `11200058`（405）或 `11200059`（404）错误。  
> - 所有环境变量中的密钥必须通过 KMS 加密，明文填写将导致部署失败。

## 面向开发者：快速上手建议

- **优先选用预置服务**：高德地图、WebSearch、Firecrawl 等已开箱即用，开通即用，无需配置密钥（首次默认使用平台级凭证）。
- **自定义服务部署选型**：
  - 简单脚本服务 → 用 `npx/uvx` 部署（要求无本地依赖、提供 `stdio` 入口）；
  - 现有 RESTful API → 用「AI 网关导入」封装为 MCP；
  - 阿里云 OpenAPI → 用「OpenAPI 导入」一键生成工具。
- **调试技巧**：
  - 使用控制台「MCP 服务详情页 > 外部调用」生成 IDE 配置片段；
  - 调用失败时，优先检查 `type`/`url` 匹配性、KMS 加密状态、以及函数计算 FC 的网络出口（无固定 IP，需 VPC 或白名单）；
  - 自定义服务不自动更新，版本变更后务必重新部署。
- **安全红线**：MCP 服务运行于百炼托管环境，**无法访问用户本地资源（如本地文件、数据库）或未授权的公网域名**；涉及敏感操作请严格遵循最小权限原则配置 `env` 和网络策略。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)


