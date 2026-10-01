# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化工具接入机制，用于在大语言模型与外部系统（如地图、数据库、SaaS 应用、爬虫服务等）之间建立安全、可扩展、协议一致的信息通道。它基于开源 MCP 标准实现，屏蔽底层通信细节，使模型能以统一语义理解并调用各类工具，无需为每个服务重复开发适配逻辑。

## 在百炼平台的不同场景中如何使用

MCP 不是独立运行的服务，而是深度嵌入百炼应用架构的**协议层能力**，其使用严格绑定于以下两类运行环境：

- **智能体（Agent 2.0）应用**：  
  最常用场景。在智能体配置中，可一次性添加最多 5 个 MCP 服务（如高德天气、Firecrawl 爬虫、QuickChart 图表生成）。模型根据用户输入自动判断是否需要调用、调用哪个工具，并动态构造参数。整个“规划-执行-反思”链路全程可追溯，开发者无需编写调度逻辑。

- **工作流（Workflow）应用**：  
  以节点形式显式编排。每个 MCP 节点**仅绑定一个工具**（如 `maps_weather`），需手动配置输入参数来源（例如从上游大模型节点提取的城市名）和输出结果的后续处理方式。适用于流程确定、需强控执行顺序的业务场景（如“查天气→生成报告→发送钉钉”）。

> ⚠️ 注意：MCP **不支持**在直接调用千问 API（如 `qwen-max` 的 [OpenAI 兼容接口](openai-compatibility.md)）时使用；也不支持在插件（Plugin）体系中混用。它专属于百炼托管的 Agent/Workflow 运行时环境。

此外，MCP 也是百炼 **Connector（连接器）** 的底层协议：所有文件、OSS、数据库、钉钉、Salesforce 等连接器，均被封装为符合 MCP 规范的工具，由智能体或工作流统一发现与调用。

## 关键参数和配置

MCP 服务的注册与调用依赖以下核心参数，均在控制台「MCP 服务管理」或部署脚本中配置：

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `type` | 协议类型，决定通信方式与端点路径 | `"streamableHttp"` | 必须与服务实际暴露路径匹配：`"sse"` → `/sse`；`"streamableHttp"` → `/mcp` |
| `url` | MCP Server 地址 | `"https://my-server.example.com/mcp"` | 需确保函数计算（FC）实例可访问；若访问云数据库等资源，需配置 VPC 或 IP 白名单 |
| `env` | 环境变量，用于注入敏感凭证 | `{"AMAP_MAPS_API_KEY": "kms://xxx"}` | **必须使用 KMS 加密 URI**，禁止明文填写密钥 |
| `command` / `args` | 启动命令（用于自定义部署） | `"npx", ["-y", "@modelcontextprotocol/server-memory"]` | 版本变更后需手动重新部署，不自动更新 |
| `服务名称` / `描述` | 控制台标识字段 | `"杭州天气查询"` / `"调用高德API获取实时天气"` | 描述直接影响模型工具选择准确率，需清晰说明用途与输入约束 |

> ✅ 提示：所有 MCP 服务均通过 `workspaceId`（如 `llm-xxxxxxxxxxxx`）隔离数据范围，确保多租户安全。

## 面向开发者：简洁实用指南

- **快速起步**：优先选用平台托管的 [官方 MCP 服务](https://help.aliyun.com/zh/bailian/user-guide/official-and-third-party-mcp)（如 Amap Maps、Firecrawl），1 分钟内完成添加，无需部署。
- **自定义集成**：使用 `npx` 或 `uvx` 启动标准 MCP Server（如 `@modelcontextprotocol/server-http`），按文档配置 `env` 和 `url`，再在百炼控制台注册即可。
- **调试技巧**：  
  - 用 `curl -X POST ${MCP_URL}/tools` 测试服务连通性；  
  - 查看函数计算（FC）日志定位 `404`（路径错误）或 `Connection refused`（网络不通）；  
  - 在智能体调试面板中观察 `tool_calls` 字段，确认模型是否正确识别并构造了调用请求。
- **性能注意**：MCP 返回结果将作为上下文输入模型，显著增加输入 Token。建议对返回内容做精简（如只取关键字段），避免长文本拖慢响应。
- **安全红线**：严禁在 `env` 中明文写密钥；严禁在代码/配置中硬编码 `DASHSCOPE_API_KEY`；所有凭证必须通过 KMS 或环境变量注入。

MCP 是百炼实现“模型即调度中心”的关键协议——它让大模型真正成为业务系统的智能中枢，而非孤立的文本生成器。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


