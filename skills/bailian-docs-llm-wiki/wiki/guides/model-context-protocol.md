# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务**不直接绑定特定大模型**，而是通过百炼平台的智能体（Agent）和工作流（Workflow）应用间接调用。当前支持以下两类集成场景：

- **平台内集成**：在智能体或工作流应用中配置 MCP 服务后，由通义千问系列模型（如 `qwen-max`、`qwen-plus`）根据提示词自动触发调用。智能体最多可同时启用 5 个 MCP 服务；工作流中每个 MCP 节点仅能绑定一个具体工具（如 `maps_weather`），需手动指定输入参数并传递输出。
- **平台外集成**：支持通过外部调用方式接入第三方应用（如 Cherry Studio、Cursor）或自有项目，依赖 MCP SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。详细方法见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 5 明确指出“MCP 服务能否在调用千问 API 时接入？不可以”，即 MCP **不能**直接用于裸调用 `dashscope` 或 `qwen` API 接口，必须依托百炼平台的智能体/工作流容器运行。

## 关键参数

MCP 服务配置涉及两类关键参数：

- **服务级参数**（部署时设定）：
  - `type`：协议类型，必须与端点路径严格匹配——`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp`（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 错误码 11200058/11200059）；
  - `command` / `args`：用于脚本部署（如 `npx` 或 `uvx`），需确保命令可执行且环境变量（如 `AMAP_MAPS_API_KEY`）已正确注入；
  - `url`：远程服务地址，必须可公网访问且 TLS 证书有效（否则触发 `MCP_SSL_ERROR`）。

- **调用级参数**（运行时传递）：
  - 工具名（`tool.name`）和输入 Schema（`tool.inputSchema`）由 MCP 服务自身定义，智能体/工作流通过 `list_tools()` 获取；
  - 外部调用时需提供 `DASHSCOPE_API_KEY` 及 `Authorization` 请求头；
  - 敏感参数（如 API Key）必须通过 KMS 凭据加密，不可明文配置。

## 使用方式

### 1. 开通服务
- **官方服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击目标服务（如 Amap Maps）→ “立即开通”。试用版无需填写 API Key；商业化定制需配置个人 Key 并加密。
- **自定义服务**：支持三种方式：
  - *脚本部署*：适用于开源或自研 MCP Server（Node.js/Python），通过函数计算 FC 托管（见 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)）；
  - *AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *OpenAPI 导入*：将阿里云产品（OSS/ECS）操作发布为 MCP 工具。

### 2. 集成到应用
- **智能体**：创建后在「MCP 服务」模块添加，系统自动识别工具能力，对话中由模型自主决策调用时机。
- **工作流**：拖入 MCP 节点 → 选择具体工具 → 通过上游大模型节点解析自然语言为结构化参数（如城市名）→ 引用输出至下游节点。
- **外部调用**：使用 MCP SDK（如 `streamablehttp_client`）连接 `https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp`，或一键配置至 Cherry Studio/Cursor（见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

## 限制和注意事项

- **网络与权限限制**：
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）；
  - 不支持访问用户本地资源（如本地文件、硬件设备）；
  - 私有 npm/PyPI 仓库暂不支持直接部署，需发布至公共仓库或改用 SSE 连接。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**（非旧版 SSE），已开通用户需取消再重新开通以完成升级（见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）；
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，必须手动重新部署。

- **计费与限流**：
  - 云部署服务：Amap Maps 限时免费；联网搜索服务免费额度 2000 次/月，超量后 29 元/千次；
  - 自定义服务：基础模式按调用时长计费（0.000156 元/秒），极速模式另收部署费（0.000036 元/秒）；
  - 全局限流：15 QPS，主账号与 RAM 子账号共享。

- **调试建议**：
  - 遇到连接失败（如 `MCP_CONNECTION_REFUSED`），优先执行 `curl <服务地址>` 测试连通性；
  - 工作流中 MCP 调用失败，检查上游大模型节点的 System Prompt 是否清晰描述了工具输入/输出格式；
  - 模型未触发 MCP 调用，需优化提示词明确指令（如“调用 Amap Maps MCP 服务规划路线”）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


