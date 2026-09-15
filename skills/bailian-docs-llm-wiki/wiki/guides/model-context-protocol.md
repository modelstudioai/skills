# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地理服务、网页爬取、天气查询等）之间建立安全、可扩展的信息通道。它屏蔽了工具接入的底层复杂性，使开发者无需为每个第三方服务单独开发适配层，即可在智能体或工作流中声明式调用多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用能力需通过百炼平台的**智能体应用**和**工作流应用**触发。当前支持以下两类使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数。支持同时配置最多 5 个 MCP 服务（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。典型用例包括路径规划（Amap Maps）、逻辑推理（Sequential Thinking）、多工具协同（如天气+图表生成）。
- **工作流应用**：需显式添加 MCP 节点并手动指定所用工具（如 `maps_weather`），输入参数须由前置节点（如大模型节点）结构化提取，输出参数需传递至后续节点处理（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**。文档 5 明确指出：“MCP 服务能否在调用千问 API 时接入？不可以。阿里云百炼 MCP 服务需集成在**智能体**或**工作流**应用中使用，不能直接在调用千问 API 时接入。” 因此，若需 MCP 能力，必须构建百炼应用而非调用 `/v1/chat/completions` 接口。

## 关键参数

MCP 服务配置与调用涉及以下核心参数，按部署方式分类：

| 参数类别 | 配置项 | 说明 | 示例值 |
|----------|--------|------|--------|
| **通用元信息** | 服务名称、描述 | 仅用于控制台识别，不影响模型调用逻辑 | `"长期记忆"`、`"该服务使大模型能够记录个性化信息..."` |
| **部署方式** | 安装方式 | 决定如何启动服务：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE/Streamable HTTP） | `"npx"` |
| | 部署模式 | `基础模式`（按调用时长计费，有冷启动延迟）或 `极速模式`（按部署+调用双计费，常驻内存） | `"基础模式：按次计费"` |
| **连接配置** | `mcpServers` 配置块 | JSON 格式，定义服务类型、命令、参数及环境变量（见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)） | `{ "memory": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"] } }` |
| **安全凭证** | KMS 凭据 | 敏感字段（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 加密管理，不可明文填写 | — |

## 使用方式

### 1. 接入官方 MCP 服务  
前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ 点击“立即开通”→ 在智能体/工作流中添加即可使用。试用版无需提供 API Key；商业化定制需配置 KMS 加密的凭据。

### 2. 部署自定义 MCP 服务  
支持三种方式（见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)）：  
- **脚本部署**：适用于开源或自研 MCP 服务（如 `@modelcontextprotocol/server-memory`），通过函数计算托管；  
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；  
- **OpenAPI 导入**：将阿里云产品（OSS/ECS）操作发布为 MCP 工具。  

> **注意**：所有自定义服务部署前，必须确认其兼容 `stdio` 或 `streamableHttp` 协议。文档 3 强调：“并非所有 MCP 服务都支持 npx/uvx/http 方式部署……建议参考 [MCP 官方文档](https://modelcontextprotocol.io/quickstart/server) 进行本地部署。”

### 3. 外部调用集成  
支持两种路径：  
- **第三方应用一键配置**：如 Cherry Studio、Cursor，通过百炼控制台“一键配置”自动注入服务地址与认证；  
- **SDK 编码集成**：使用 `mcp` SDK + OpenAI 兼容客户端（如示例中调用 WebSearch 服务），详见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：  
  - MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通（见文档 5）；  
  - **不支持访问用户本地资源**（如本地文件、硬件设备），此类服务需本地部署（文档 5 第9条）；  
  - 私有 npm/PyPI 仓库暂不支持直接部署（文档 5 第7条）。

- **协议与兼容性**：  
  - 百炼已全面升级至 **Streamable HTTP 协议**（替代旧版 SSE），已开通用户需取消再重新开通以完成升级（见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）；  
  - 配置中 `type` 字段必须与端点路径严格匹配：`"sse"` → `/sse`，`"streamableHttp"` → `/mcp`，否则报错 `11200058`（HTTP 405）。

- **计费与限流**：  
  - 官方服务（如联网搜索）有免费额度（2000 次/月），超量后按 29 元/千次计费；  
  - 自定义服务按调用时长（0.000156 元/秒）或部署时长（0.000036 元/秒）计费；  
  - 云部署服务限流为 **15 QPS**，主账号与 RAM 子账号共享（见文档 1）。

- **调试与错误排查**：  
  - 常见错误码（如 `11200044` 连接拒绝、`11200054` 协议解析失败）需结合 `curl` 测试、FC 日志及下游服务文档定位（见文档 5 错误码表）；  
  - 模型无法调用 MCP 时，优先检查提示词是否明确工具名称与能力（文档 4 最后一条常见问题）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


