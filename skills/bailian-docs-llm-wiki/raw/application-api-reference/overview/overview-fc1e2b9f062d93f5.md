# 生命周期

开通、关闭、停用和启用 MCP 服务。

生命周期接口用于开通和关闭官方 MCP，以及停用和启用自定义 MCP。

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| [开通 MCP](overview/activate.md) | POST `/{mcpCode}/activate` | 开通官方 MCP |
| [关闭官方 MCP](overview/deactivate.md) | POST `/{mcpCode}/deactivate` | 关闭官方 MCP |
| [停用自定义 MCP](overview/disable.md) | POST `/{mcpCode}/disable` | 停用自定义 MCP |
| [启用自定义 MCP](overview/enable.md) | POST `/{mcpCode}/enable` | 启用自定义 MCP |
