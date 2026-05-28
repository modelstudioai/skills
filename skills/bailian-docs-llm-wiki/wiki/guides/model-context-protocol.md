# model context protocol

模型上下文协议（Model Context Protocol, MCP）是 Anthropic 提出的开源标准，旨在为大模型与外部工具/数据源之间建立标准化的信息交互通道。通过该协议，开发者无需为各类第三方接口编写重复的适配代码，即可在百炼平台快速集成地理信息、联网搜索、云资源管理等扩展能力，显著降低[[智能体应用]]与[[工作流应用]]的开发门槛。

## 支持的模型/功能
- **协议标准**：底层基于 JSON-RPC 通信。百炼平台已全面升级支持 `streamableHttp` 传输协议，兼顾旧版 `sse` 的兼容性。
- **服务分类**：
  - **官方托管服务**：预置 Amap Maps（地理路径）、QuickChart（数据可视化）、联网搜索等，开通即用。敏感参数自动通过 KMS 加密。
  - **自定义服务**：支持通过脚本托管 Node.js/Python 代码包、[[AI网关]] 转发现有 RESTful API，或快速接入阿里云 OpenAPI 生态。
- **核心能力**：动态工具路由、多步参数解析、结构化数据获取、云端异步任务执行。
更多场景示例与协议架构说明，详见[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 关键参数
- **计费模式（自定义脚本部署）**：
  - **基础模式**：免部署费，无调用不产生费用。实际调用按运行时长计费（`0.000156 元/秒`），存在容器冷启动延迟，适合低频场景。
  - **极速模式**：收取基础部署时长费（`0.000036 元/秒`）+ 调用费，服务常驻内存，消除冷启动耗时，适合高频/低延迟业务。
- **外部调用端点**：标准格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/<service-name>/mcp`，HTTP Header 必须携带 `Authorization: Bearer <DASHSCOPE_API_KEY>`。
- **配置结构（JSON）**：
  ```json
  {
    "mcpServers": {
      "service_alias": {
        "type": "stdio", // 本地托管使用 stdio；远程使用 sse 或 streamableHttp
        "command": "npx", // Node.js 服务
        "args": ["-y", "@scope/package_name"],
        "env": {"API_KEY": "value"},
        "url": "https://remote-server/sse" // 仅 type 为 sse/streamableHttp 生效
      }
    }
  }
  ```
详细部署参数与[[函数计算]]托管逻辑，参考[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 使用方式
- **平台内集成**：
  - **[[智能体应用]]**：最多可挂载 5 个 MCP 服务。大模型基于对话上下文自动触发工具调用。建议在 System Prompt 中明确工具名称、触发场景与边界，避免误调用。
  - **[[工作流应用]]**：采用单节点绑定单工具模式。需手动串联参数流转：通常使用大模型节点前置提取自然语言参数，映射至 MCP 节点输入，再将 `result` 输出至后续处理节点。
- **外部/第三方集成**：
  - **IDE 一键配置**：在控制台 MCP 广场生成配置 JSON，直接导入 Cherry Studio 或 Cursor 客户端，自动注入 API Key 与服务地址。
  - **SDK 开发**：通过 `qwen-agent` 等框架声明 `tools` 字段，将 MCP 服务作为 function calling 资源注入，实现完全定制化的业务逻辑编排。完整 Python 示例见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项
- **网络与环境边界**：自定义服务托管于云端无状态环境，**无固定公网出口 IP**。访问云数据库等远程资源必须配置白名单或 VPC 内网互通。**不支持直接访问本地文件系统、数据库或硬件**，强依赖本地上下文的工具需本地化部署。
- **依赖与版本管理**：暂不支持拉取私有 npm/PyPI 仓库，需发布至公共源或改用远程 SSE/HTTP 接入。第三方包版本更新后**不会自动同步**，需在控制台手动停止并重新部署。
- **模型与调用限制**：MCP **不可直接通过 [[千问API]] 调用**，必须依托百炼智能体或工作流应用编排。调用过程会将获取的外部数据拼接入上下文，导致 Input Token 增加，并可能因信息丰富度提升间接推高 Output Token。
- **协议升级操作**：已开通的旧版 SSE 服务需先执行“取消开通”，再重新“立即开通”，方可切换至新版 `streamableHttp` 端点。
- **私有性与安全**：自定义服务仅限主账号及授权 RAM 子账号访问。若模型未触发 MCP，请检查 Prompt 是否缺乏明确工具指令，或尝试升级至 qwen-max/qwen3 等强推理模型。

> **注意**：官方文档中关于自定义服务“基础模式”的计费术语存在表述差异（部分页面标注为“按次计费”），实际底层结算逻辑均为**按调用运行时长（0.000156 元/秒）累计**，具体扣费请以控制台实时账单为准。
> **注意**：百炼 MCP 传输协议已全面迁移至 `streamableHttp`，旧版 SSE 接入点已进入弃用过渡期。生产环境请务必使用新版端点地址，避免因连接被拒导致 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED` 或 `MCP_CONNECTION_REFUSED` 异常。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)

