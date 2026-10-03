# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了工具接入的底层差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式调用能力。MCP 基于开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

- **适用场景**：MCP 服务仅可在百炼平台的 **智能体应用** 和 **工作流应用** 中配置使用，**不支持直接集成到千问 API 调用链中**（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第3条）。  
- **官方服务**：已预置并托管多种开箱即用的 MCP 服务，包括 `Amap Maps`（地理信息）、`WebSearch`（联网搜索）、`Firecrawl`（网页爬取）、`Sequential Thinking`（逻辑推理）和 `QuickChart`（图表生成）等。其中 Amap Maps 限时免费，WebSearch 提供 2000 次/月免费额度。  
- **自定义服务**：支持三类部署方式：  
  - **脚本部署**（npx/uvx）：适用于已发布至 npm 或 PyPI 的开源或自研 MCP 服务（如 `@modelcontextprotocol/server-memory`）；  
  - **AI 网关导入**：将现有 RESTful API 封装为 MCP 服务；  
  - **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）的 OpenAPI 快速发布为 MCP 工具。  
  > **注意**：并非所有开源 MCP 服务都兼容 npx/uvx 部署方式；若缺少 `stdio` 入口或依赖本地资源（如文件系统、硬件），则无法云端部署（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第9条）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `type` | 连接协议类型，必须与服务端端点严格匹配 | `"stdio"`（本地进程）、`"sse/streamableHttp"`（远程 HTTP） |
| `command` / `url` | 启动命令或服务地址 | `"npx"` + `["-y", "@modelcontextprotocol/server-memory"]` 或 `"https://your-mcp-server/sse"` |
| `env` | 环境变量（敏感信息需通过 KMS 凭据加密） | `{"AMAP_MAPS_API_KEY": "kms://xxx"}` |
| `deploymentMode` | 部署模式（影响计费与延迟） | `"basic"`（按调用时长计费，有冷启动）、`"premium"`（按部署+调用双计费，常驻在线） |

> **注意**：`type` 与 URL 路径必须一致——`"sse"` 对应 `/sse` 端点（GET），`"streamableHttp"` 对应 `/mcp` 端点（POST）。配置错误将导致 `11200058`（HTTP 405）或 `11200059`（HTTP 404）错误（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)错误码表）。

## 使用方式

1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)，选择服务并点击“立即开通”。首次开通无需配置密钥；如需定制（如使用个人高德 Key），需通过 KMS 加密后填入。  
2. **配置到应用**：  
   - **智能体**：在应用编辑页 → “工具” → “添加 MCP 服务”，最多可同时启用 5 个；模型根据提示词自动决定是否及如何调用（见[文档 5](raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。  
   - **工作流**：拖入“MCP 节点”，手动指定具体工具（如 `maps_weather`）及输入参数（支持引用上游节点输出）。  
3. **外部调用**：  
   - **第三方 IDE**（Cherry Studio/Cursor）：在 MCP 服务详情页 → “外部调用” → 选择平台 → 点击“一键配置”，自动注入 `DASHSCOPE_API_KEY`；  
   - **自定义项目**：使用 `mcp` SDK（如 `streamablehttp_client`）连接 `https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`，配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)完成工具发现与调用（见[文档 3](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)代码示例）。

## 限制和注意事项

- **网络与权限**：  
  - 自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第6条）；  
  - **不支持访问用户本地资源**（如本地文件、数据库），此类服务须本地部署（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第5、9条）。  
- **版本与维护**：  
  - 通过 npx/uvx 部署的服务**不会自动更新**，版本变更后需手动重新部署（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第10条）；  
  - 阿里云百炼仅提供服务接入渠道，**不保证第三方 MCP 服务的长期可用性**（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第1条）。  
- **调试与排障**：  
  - 部署失败时，优先检查：① 本地能否正常运行该 MCP 服务；② 函数计算 FC 权限与余额；③ 配置中 `type`/`url` 是否匹配（见[文档 4](raw/application-user-guide/model-context-protocol/mcp-faq.md)第2条）；  
  - 外部调用失败常见原因包括 API Key 无效、额度耗尽、协议升级未同步（旧版 SSE 已停用，必须使用 Streamable HTTP），详见[文档 3](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)常见问题。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)


