# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）旨在搭建大模型和外部工具之间的信息传递通道。通过 MCP 协议，开发者不用为每个外部工具编写复杂的接口，阿里云百炼应用也能够接入海量第三方工具。

<a id="one-key-service"></a>

<a id="h-onekey-service"></a>

## One Key Service

阿里云百炼 MCP 广场提供 **One Key Service** 体验——只需一个阿里云百炼 API Key，即可调用广场内的 One Key MCP 服务。

-   **无需二次开通**：One Key MCP 服务无需单独开通或订阅，首次调用自动生效。
-   **统一鉴权**：使用阿里云百炼 API Key（`DASHSCOPE_API_KEY`）即可访问全部 One Key MCP 服务，无需为每个服务单独获取密钥。
-   **按量后付费**：按实际调用量计费，无需预付费或购买资源包。部分服务提供免费额度，首次调用时自动激活，用完后转为按量计费。

<a id="如何使用-mcp"></a>

<a id="2abb6d3a8ct0d"></a>

## 如何使用 MCP

阿里云百炼支持以下两种 MCP 服务，可以接入阿里云百炼智能体、工作流等应用，也可以通过 Endpoint 远程调用：

-   **广场 MCP**：MCP 广场上架的服务，对全部账号可见，分为 One Key MCP（无需开通，API Key 直接调用）和需手动开通的 MCP。详见[官方 MCP 服务](official-and-third-party-mcp.md)。
-   **自定义 MCP**：支持部署自有 MCP 服务或从开源社区接入，仅当前账号可见。详见[自定义 MCP 服务](custom-mcp.md)。

也可在终端用阿里云百炼 CLI 直接编排 MCP：列出已激活服务、查看工具、直接调用任意工具。详见[使用 CLI](../../../cli/capabilities/agent-infrastructure/mcp-skill.md)。

<a id="计费说明"></a>

<a id="fb482455a3u8c"></a>

## 计费说明

<a id="广场-mcp"></a>

<a id="2fa9fb647clfl"></a>

### 广场 MCP

广场 MCP 服务（含 One Key MCP）的计费模式因服务而异，具体服务的收费标准请在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)对应服务卡片中查看。其中部分服务由第三方供应商通过云市场提供，计量数据由服务商推送给云市场。

<a id="联网搜索-mcp-服务"></a>

<a id="95cd768ceeskn"></a>

#### 联网搜索 MCP 服务

-   **接入方式**：在[联网搜索 MCP 服务](https://bailian.console.aliyun.com/cn-beijing/store/mcp/detail/WebSearch)详情页的**安装**区域，复制安装命令或 MCP 服务地址。该服务已加入 One Key Service，无需手动开通。
-   **调用费用**：免费额度 2000 次，额度用尽后按 29 元/千次计费。
-   **限流说明**：限流为 15 QPS，阿里云主账号与其 RAM 子账号共享限流限制。

<a id="自定义部署-mcp-服务"></a>

<a id="9fe08242b2eib"></a>

### 自定义部署 MCP 服务

根据服务的响应速度，阿里云百炼提供以下两种计费模式：

-   **基础模式**：
    -   **部署费用**：无。
    -   **调用费率**：0.000156 元/秒，无调用时不计费，有调用时按时长计费。
    -   **适用场景**：偶尔调用，对启动速度要求不高（首次调用会有一定启动延迟）。
-   **极速模式**：
    -   **部署费率**：0.000036 元/秒，无调用时按部署时长计费。
    -   **调用费率**：0.000156 元/秒，有调用时另按调用时长计费。
    -   **适用场景**：需要长时间保持在线，且调用较频繁的场景，可减少频繁启动服务带来的延迟。
