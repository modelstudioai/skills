# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了工具接入的底层差异，使开发者无需为每个第三方服务单独编写适配代码，即可在智能体或工作流中统一调用。该协议基于 Anthropic 提出的开源标准实现，当前百炼平台已全面支持 Streamable HTTP 协议（取代旧版 SSE），并提供云部署、自定义部署及外部集成能力。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用能力依赖于百炼平台内应用所配置的推理模型。目前仅以下两类应用原生支持 MCP：

- **智能体应用**：模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数（如“从杭州萧山国际机场到西湖景区”触发 Amap Maps 的路径规划）；最多可同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式连接输入/输出参数；每个 MCP 节点仅能绑定一个工具 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能**在直接调用千问 API（如 `qwen-max` 的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）时接入；必须通过百炼平台的智能体或工作流应用容器使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

MCP 服务配置涉及两类关键参数：

- **服务级参数**（在 MCP 管理页配置）：
  - `type`：协议类型，必须与接入端点严格匹配——`"sse"` 对应 `/sse` 端点（GET），`"streamableHttp"` 对应 `/mcp` 端点（POST）；配置错误将导致 `11200058` 或 `11200059` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - `command` / `url`：本地部署用 `npx`/`uvx`，远程服务用 `http` + 完整 URL。
  - `env`：敏感环境变量（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密，不可明文填写 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

- **调用级参数**（由模型生成或工作流节点传递）：
  - 工具名（`tool.name`）和输入 Schema（`tool.inputSchema`）需与 MCP 服务实际暴露的接口一致，否则触发 `11200054`（协议解析错误）或 `11200060`（Bad Request）。
  - 外部 SDK 调用时，必须设置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 及正确的 `base_url`（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 使用方式

### 平台内集成
1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）并点击“立即开通”。已开通用户需先“取消开通”再重新开通以升级至 Streamable HTTP 协议 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
2. **配置应用**：
   - *智能体*：创建后在“MCP 服务”模块添加，无需指定工具，模型自动路由。
   - *工作流*：拖入 MCP 节点 → 选择工具 → 在配置中引用上游节点输出（如 `信息提取/result`）作为输入 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
3. **测试验证**：使用典型自然语言指令（如“查询杭州天气”）触发调用，观察日志或输出结果。

### 外部集成
- **第三方 IDE**（Cherry Studio/Cursor）：在 MCP 服务详情页选择对应 IDE，一键配置或手动导入 JSON 配置（含 `DASHSCOPE_API_KEY`）[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **自定义项目**：使用 `mcp` SDK + `openai` SDK，通过 `streamablehttp_client` 连接 MCP Server，将 `list_tools()` 结果转换为 OpenAI `tools` 格式后传入 `chat.completions.create` [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - **不支持访问本地资源**（如本地文件、硬件设备），此类服务须本地部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **部署与维护**：
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - 私有 npm/PyPI 包暂不支持直接部署，需发布至公共仓库或改用 SSE 连接 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **计费与限流**：
  - 云部署服务（如联网搜索）有免费额度（2000 次/月），超量后按 29 元/千次计费；限流 15 QPS，主账号与 RAM 子账号共享 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
  - 自定义服务分“基础模式”（按调用时长计费，0.000156 元/秒）和“极速模式”（另加部署费 0.000036 元/秒），冷启动延迟仅基础模式存在 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试建议**：
  - 遇连接失败（如 `11200044`），优先执行 `curl <MCP_URL>` 测试连通性，并检查下游服务日志。
  - 遇协议错误（如 `11200054`），确认 `type` 与端点路径（`/sse` vs `/mcp`）完全匹配 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


