# 工具

查询和调用 MCP 工具，按需求推荐工具。

工具接口用于查询 MCP 服务提供的工具、调用指定工具，以及根据自然语言需求推荐工具。

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| [查询工具列表](overview/list-64eddd50625ee03f.md) | GET `/{mcpCode}/tools` | 查询 MCP 提供的工具 |
| [调用工具](overview/call.md) | POST `/{mcpCode}/tools/call` | 调用指定工具 |
| [推荐工具](overview/recommend.md) | GET `/tools/recommend` | 按自然语言需求推荐工具 |
