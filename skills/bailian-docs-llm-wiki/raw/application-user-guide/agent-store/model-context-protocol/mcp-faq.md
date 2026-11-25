# MCP 常见问题

可查阅有关 MCP 协议和 MCP 服务的常见问题。

<a id="mcp-协议"></a>

<a id="48bed193c0q65"></a>

## MCP 协议

1.  **MCP 协议是如何实现的？**
    
    MCP 是 Anthropic 提出的开源标准协议。详细实现请参考 [MCP 官网](https://modelcontextprotocol.io/)。
    

<a id="云部署-mcp-服务"></a>

<a id="421126d61coh7"></a>

## 云部署 MCP 服务

1.  **Firecrawl/EverArt MCP Server 报错：请求用量受限/余额不足？**
    
    请填入服务商 API-Key，并确保其免费额度或账户余额充足。
    
2.  **为什么我的 Notion/Github MCP Server 运行出错，提示没有足够的权限？**
    
    请为 API-Key 授予足够的权限。具体操作请参考对应 MCP 服务的文档。
    

<a id="自定义-mcp-服务"></a>

<a id="12beda7007ibq"></a>

## 自定义 MCP 服务

1.  **所有 MCP 服务都可以正常部署使用吗？**
    
    不保证。MCP 服务商可能修改或关闭服务，阿里云百炼仅提供获取渠道，不保证其一直可用。
    
2.  **自定义 MCP 服务部署失败了，应该怎么排查？**
    
    请确认：
    
    1.  MCP 服务本地可正常运行。
    2.  MCP 服务可云端托管（无需浏览器/本地应用通信）。
    3.  部署时安装方式及配置代码正确。
    4.  已开通函数计算 FC 及相关权限，主账号未欠费。
3.  **我能否部署自己开发的 MCP 服务？**
    
    -   **Node.js：** 软件包发布到公共 npm 仓库，通过 npx <package-name> 部署。
    -   **Python：** 软件包发布到 PyPI 仓库，通过 uvx <package-name> 部署。
    -   **已部署在远程服务器：** 通过 SSE 连接。
    
    详见[自定义MCP服务](custom-mcp.md)。
    
4.  **阿里云百炼 MCP 服务能在其他 MCP 客户端 （Cline、Cherry Studio）中使用吗？**
    
    支持。可以在 MCP 服务详情页的**安装**区域复制 MCP 服务地址，在支持 Streamable HTTP 或 SSE 的客户端中手动添加，并配置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 请求头。控制台支持快捷安装到 Qoder、Codex、Claude Code 和 Cursor。详见[外部调用](mcp-external-calls.md)。
    
5.  **阿里云百炼 MCP 服务能访问本地数据库吗？**
    
    暂不支持。目前不能访问用户本地资源。
    
6.  **为什么我的 MCP 服务无法访问远程资源（例如云数据库）？**
    
    因为 MCP 服务托管在[函数计算 FC](https://www.aliyun.com/product/fc)，无固定出口公网 IP。请为远程资源（如云数据库）配置[函数计算 FC 的 IP 白名单或进行 VPC 网络打通](https://help.aliyun.com/zh/functioncompute/how-to-configure-an-ip-address-whitelist-when-i-access-a-database)。
    
7.  **我的 MCP Server 保存在私有 npm 仓库中，可以部署到阿里云百炼吗？**
    
    暂不支持。请发布到公共 npm 仓库，或改用 SSE 连接方式。
    
8.  **我自己编写的 MCP Server，部署后会被别人使用吗？**
    
    不会。仅限阿里云主账号及授权 RAM 用户访问。
    
9.  **为什么有些本地端 MCP Server无法在阿里云百炼上自定义部署？**
    
    因为它们需要访问本地资源（如文件、硬件），云端环境无法访问。建议此类服务在本地部署。
    
10.  **我的 MCP Server 版本更新了，部署在阿里云百炼的自定义 MCP 服务也会更新吗？**
     
     不会。通过 npx/uvx 部署的服务，版本更新后需手动重新部署。
     

<a id="自定义-mcp-服务错误码及排查方案"></a>

<a id="a3f7c91b2dek8"></a>

## 自定义 MCP 服务错误码及排查方案

<table><thead><tr><th><p><strong>错误码</strong></p></th><th><p><strong>问题及可能原因</strong></p></th><th><p><strong>排查方案</strong></p></th></tr></thead><tbody><tr><td><p>11200044 - MCP_CONNECTION_REFUSED<br></p></td><td><p>客户端无法与目标服务建立连接，连接被拒绝。可能原因：</p><ul><li><p>服务未启动。</p></li><li><p>端口未开放或防火墙拦截。</p></li><li><p>网络不可达或地址配置错误。</p></li></ul></td><td><ul><li><p>执行 <code>curl &lt;服务地址&gt;</code> 测试连通性。</p></li><li><p>查看下游服务日志，确认 MCP 服务是否已经启动。</p></li><li><p>检查下游服务的网关或防火墙配置，是否有 IP 白名单等连接拒绝配置。</p></li></ul></td></tr><tr><td><p>11200045 - MCP_CONNECTION_TIMEOUT</p></td><td><p>连接建立超时。可能原因：</p><ul><li><p>网络延迟或丢包。</p></li><li><p>服务端负载较高、响应慢。</p></li><li><p>路由或网络不稳定。</p></li><li><p>经代理访问时链路较长。</p></li></ul></td><td><p>建议先重试 2~3 次：</p><ul><li><p>如果偶尔可以正常访问，则是网络问题。</p></li><li><p>如果持续出现问题，需要检查下游服务链路上的网关或防火墙配置，是否有 IP 白名单配置。</p></li></ul></td></tr><tr><td><p>11200046 - MCP_REQUEST_TIMEOUT</p></td><td><p>连接已建立，但等待响应超时。可能原因：</p><ul><li><p>服务端处理耗时较长或资源不足。</p></li><li><p>网络带宽或延迟导致响应慢。</p></li></ul></td><td><p>建议先重试 2~3 次。若仍失败：</p><ul><li><p>拆分业务，减少单次请求耗时。或对业务进行异步化。</p></li><li><p>npx/uvx 部署：在<a href="https://fcnext.console.aliyun.com/cn-hangzhou/functions">函数计算 FC 控制台</a>开启日志服务查看错误详情，可切换为极速模式减少冷启动耗时。</p></li></ul></td></tr><tr><td><p>11200047 - MCP_NETWORK_ERROR</p></td><td><p>网络可达性、域名解析或连接中断相关的异常。</p><p>可能原因：</p><ul><li><p>域名无法解析或解析异常。</p></li><li><p>连接在中途被对端或中间设备关闭。</p></li><li><p>目标主机不可达或路由异常。</p></li></ul></td><td><p>建议先重试 2~3 次。若仍失败：</p><ul><li><p>执行 <code>nslookup</code> 确认域名解析正常，异常时更换 DNS 后重试。</p></li><li><p>检查配置中的 <code>url</code> 字段，执行 <code>curl &lt;url&gt;</code> 测试服务是否响应。</p></li></ul></td></tr><tr><td><p>11200048 - MCP_SSL_ERROR</p></td><td><p>TLS/SSL 握手或证书校验失败。可能原因：</p><ul><li><p>服务端证书过期、域名与证书不匹配或证书链不完整。</p></li><li><p>本机不信任服务端证书（如自签名证书）。</p></li><li><p>TLS 版本或加密套件不兼容。</p></li><li><p>代理或网关改写了证书。</p></li></ul></td><td><ul><li><p>在浏览器中打开服务地址，查看证书是否过期或域名不匹配。</p></li><li><p>使用自签名证书时，按要求完成信任配置。</p></li><li><p>关闭代理直连测试，排查证书是否被代理改写。</p></li></ul></td></tr><tr><td><p>11200049 - MCP_SERVER_HTTP_UNAUTHORIZED</p></td><td><p>HTTP 401，请求未携带有效认证或认证已失效。可能原因：</p><ul><li><p>未提供或未正确传递鉴权信息（如 Token、API Key）。</p></li><li><p>Token 已过期、被撤销或格式错误。</p></li><li><p>服务端要求特定请求头或 Cookie 未满足。</p></li></ul></td><td><ul><li><p>查看下游 MCP 服务文档，了解鉴权方式。</p></li><li><p>在 MCP 服务中正确添加鉴权信息，例如Headers中的Authorization信息。</p></li><li><p>使用curl工具测试直连下游服务，确保配置是正确的。</p></li></ul></td></tr><tr><td><p>11200050 - MCP_SERVER_HTTP_FORBIDDEN</p></td><td><p>HTTP 403，已认证但无权限访问。可能原因：</p><ul><li><p>当前账号或角色不具备该 MCP 或实例的访问权限。</p></li><li><p>存在 IP 或来源限制。</p></li></ul></td><td><ul><li><p>查看下游MCP服务文档，了解鉴权方式。</p></li><li><p>使用curl工具测试直连下游服务，确保配置是正确的。</p></li></ul></td></tr><tr><td><p>11200051 - MCP_HTTP_RATE_LIMIT</p></td><td><p>HTTP 429，请求频率超过限流阈值。可能原因：</p><ul><li><p>短时间内请求次数过多。</p></li><li><p>当前账号或实例的配额已用尽。</p></li></ul></td><td><ul><li><p>降低调用频率；若响应中带有 Retry-After，按建议间隔重试。</p></li><li><p>若业务需要更高配额，可联系 MCP 服务提供方申请。</p></li></ul></td></tr><tr><td><p>11200052 - MCP_HTTP_CLIENT_ERROR</p></td><td><p>HTTP 4xx 且非 400/401/403/404/405/429 的其它客户端错误。可能原因：</p><ul><li><p>请求方法、URL、请求头或请求体不符合服务端要求。</p></li><li><p>请求体过大或 URL 过长。</p></li><li><p>请求在服务端等待超时（如 408）。</p></li></ul></td><td><ul><li><p>查看响应体中的具体状态码和错误信息，查阅下游MCP服务文档尝试解决。</p></li><li><p>使用 <code>curl</code>工具进行测试， 查看完整请求和响应以及下游MCP服务日志。</p></li></ul></td></tr><tr><td><p>11200053 - MCP_HTTP_SERVER_ERROR</p></td><td><p>HTTP 5xx，服务端或网关内部错误。可能原因：</p><ul><li><p>MCP 服务或网关异常、过载或维护中。</p></li><li><p>依赖的下游服务不可用。</p></li></ul></td><td><p>建议先重试 2~3 次。若仍失败：</p><ul><li><p>查看响应错误详情以及下游MCP服务的日志。。</p></li><li><p>npx/uvx 部署：在<a href="https://fcnext.console.aliyun.com/cn-hangzhou/functions">函数计算 FC 控制台</a>查看运行日志（需先开启日志服务）。</p></li><li><p>使用 <code>curl</code>工具进行测试， 查看完整请求和响应以及下游MCP服务日志。</p></li></ul></td></tr><tr><td><p>11200054 - MCP_PROTOCOL_ERROR</p></td><td><p>响应无法按 MCP 协议正确解析。可能原因：</p><ul><li><p>服务端返回标准 JSON-RPC 错误（如解析错误、无效请求、方法不存在、参数无效、内部错误）。</p></li><li><p>协议或版本不兼容。</p></li></ul></td><td><ul><li><p>根据 JSON-RPC error code 修正请求格式、方法名或参数。</p></li><li><p>确认配置中 <code>type</code> 与端点路径一致：<code>&quot;sse&quot;</code> 对应 <code>/sse</code>，<code>&quot;streamableHttp&quot;</code> 对应 <code>/mcp</code>。</p></li></ul></td></tr><tr><td><p>11200055 - MCP_SESSION_NOT_FOUND</p></td><td><p>会话不存在或已过期。可能原因：</p><ul><li><p>服务端重启或会话过期后客户端仍使用旧会话。</p></li><li><p>会话 ID 传递错误或丢失。</p></li><li><p>服务端路由策略导致请求没有命中同一实例。</p></li></ul></td><td><ul><li><p>优化下游MCP服务，遵守标准的MCP协议行为。</p></li><li><p>检查日志，MCP下游服务可能出现异常重启，导致会话丢失。</p></li></ul></td></tr><tr><td><p>11200056 - MCP_UNKNOWN_ERROR</p></td><td><p>无法归入上述分类的异常，返回信息中携带原始错误内容。可能原因：</p><ul><li><p>运行环境或依赖产生的未分类异常。</p></li></ul></td><td><ul><li><p>根据返回的原始错误信息与上下文排查。</p></li><li><p>npx/uvx 部署：在<a href="https://fcnext.console.aliyun.com/cn-hangzhou/functions">函数计算 FC 控制台</a>开启日志服务查看运行日志。</p></li></ul></td></tr><tr><td><p>11200057 - MCP_INIT_TIMEOUT</p></td><td><p>初始化阶段未收到服务端就绪信号。可能原因：</p><ul><li><p>服务端未及时推送初始化数据。</p></li><li><p>网络延迟或丢包。</p></li><li><p>中间代理或网关对长连接支持异常。</p></li></ul></td><td><p>建议先重试 2~3 次。若仍失败：</p><ul><li><p>前往<a href="https://bailian.console.aliyun.com/?tab=app#/mcp-manage">MCP 管理</a>核对接入地址和传输方式（<code>sse</code> 或 <code>streamableHttp</code>）。</p></li><li><p>执行 <code>curl &lt;接入地址&gt;</code> 测试连通性。</p></li><li><p>反向代理需启用长连接并设置足够超时时间。</p></li><li><p>npx/uvx 部署：在<a href="https://fcnext.console.aliyun.com/cn-hangzhou/functions">函数计算 FC 控制台</a>查看启动日志，基础模式有冷启动延迟，可切换为极速模式。</p></li></ul></td></tr><tr><td><p>11200058 - MCP_SERVER_HTTP_METHOD_NOT_ALLOWED</p></td><td><p>HTTP 405，端点不接受所使用的 HTTP 方法。可能原因：</p><ul><li><p>使用的传输方式与接入路径不匹配（如 SSE 与 Message 端点混用）。</p></li><li><p>对同一 URL 使用了服务端不支持的方法（如误用 GET/POST）。</p></li></ul></td><td><ul><li><p>确认配置中 <code>type</code> 与端点路径匹配：<code>&quot;sse&quot;</code> 对应 GET <code>/sse</code>，<code>&quot;streamableHttp&quot;</code> 对应 POST <code>/mcp</code>。配置错误时在<a href="https://bailian.console.aliyun.com/?tab=app#/mcp-manage">MCP 管理</a>中修改后重新部署。</p></li><li><p>建议使用标准的 MCP SDK 实现下游MCP服务。</p></li></ul></td></tr><tr><td><p>11200059 - MCP_SERVER_HTTP_NOT_FOUND</p></td><td><p>HTTP 404，请求路径不存在。可能原因：</p><ul><li><p>接入 URL 路径配置错误（如缺少路径前缀）。</p></li><li><p>服务端路由或网关未将该路径转发到 MCP 服务。</p></li><li><p>实例已下线或未正确部署。</p></li></ul></td><td><ul><li><p>确认配置中 <code>type</code> 与端点路径匹配：<code>&quot;sse&quot;</code> 对应 GET <code>/sse</code>，<code>&quot;streamableHttp&quot;</code> 对应 POST <code>/mcp</code>。配置错误时在<a href="https://bailian.console.aliyun.com/?tab=app#/mcp-manage">MCP 管理</a>中修改后重新部署。</p></li><li><p>前往<a href="https://bailian.console.aliyun.com/?tab=app#/mcp-manage">MCP 管理</a>确认服务状态，未部署时重新部署。</p></li><li><p>使用 <code>curl</code>工具测试连通性。</p></li></ul></td></tr><tr><td><p>11200060 - MCP_SERVER_HTTP_BAD_REQUEST</p></td><td><p>HTTP 400，请求格式或参数不合法。可能原因：</p><ul><li><p>请求体不是合法 JSON 或不符合 MCP/JSON-RPC 格式。</p></li><li><p>必填参数缺失或类型错误。</p></li><li><p>请求头或查询参数未通过服务端校验。</p></li></ul></td><td><ul><li><p>检查相关字段的类型和必填项是否与服务端要求是否一致。</p></li><li><p>使用 <code>curl</code>工具测试连通性。</p></li></ul></td></tr></tbody></table>

<a id="接入智能体-工作流应用"></a>

<a id="33a5325b37lgn"></a>

## 接入智能体/工作流应用

1.  **为什么智能体应用无法调用 MCP 服务，或报参数错误？**
    
    智能体根据提示词（Prompt）决定调用和参数。请尝试：
    
    1.  优化提示词，明确意图。
    2.  若无效，更换更强的推理模型（如千问 3 系列）。
2.  **调用 MCP 会导致模型输入或输出 Token 增加吗？**
    
    会，调用 MCP 可能导致模型输入和输出 Token 增加。
    
    1.  输入 Token 增加：从 MCP 服务获取的内容会作为上下文传递给模型，直接增加来输入 Token 数量。
    2.  输出 Token 增加：虽然调用 MCP 本身不直接产生输出 Token，但由于模型获得了更丰富的上下文信息，可能生成更详细、更完整的响应，从而间接增加输出 Token 数量。
3.  **MCP 服务能否在调用千问 API 时接入？**
    
    不可以。阿里云百炼 MCP 服务需集成在**智能体**或**工作流**应用中使用，不能直接在调用千问 API 时接入。
