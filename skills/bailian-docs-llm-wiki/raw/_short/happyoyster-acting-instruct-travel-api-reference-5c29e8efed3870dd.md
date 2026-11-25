# HappyOyster-Acting-发送文本过程指令 API参考

向 Acting Travel 发送一条文本指令，驱动后续角色表演和画面生成。Travel 为 running 或 paused 时可调用。

<a id="适用范围"></a>

<a id="ho-act-in-scope-title"></a>

## 适用范围

向 Acting Travel 发送一条文本指令，驱动后续角色表演和画面生成。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 状态需为 `running` 或 `paused`。可通过[查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

<a id="http调用"></a>

<a id="ho-act-in-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/instruct`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/instruct`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-act-in-req-title"></a><h4>请求参数</h4></td><td rowspan="8"><a id="sec-tabs-2"></a><section><a id="发送文本过程指令"></a><section><a id="发送文本过程指令-h4"></a><h4>发送文本过程指令</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/instruct' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedTravelId&quot;: &quot;{encryptedTravelId}&quot;,
    &quot;content&quot;: &quot;微笑着问候，并询问我今天过得怎么样&quot;,
    &quot;clientRequestId&quot;: &quot;instruction_greeting_001&quot;,
    &quot;userAgent&quot;: &quot;HappyOyster-Web/1.2.0&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-act-in-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>要控制的 Acting 加密 Travel ID。由<a href="happyoyster-acting-enter-travel-api-reference-56ea4df0a872fdb7.md">客户端进入房间</a>接口返回。</p></td></tr><tr><td><p><strong>content</strong> <code>string</code> <strong>（必选）</strong></p><p>文本过程指令。非空，最长 2000 字符；缺失、为空或超限返回 <code>400000</code>。</p></td></tr><tr><td><p><strong>clientRequestId</strong> <code>string</code> <strong>（可选）</strong></p><p>指令重试的计费幂等键。同一条逻辑指令重试时复用同值，避免重复计费。推荐格式 <code>[A-Za-z0-9_-]{1,32}</code>。</p><ul><li>缺省或格式不符合建议时不会返回参数错误：服务端会回退使用网关 <code>request_id</code>，仍不可用时使用随机计费幂等键</li><li>该字段只用于计费去重，不保证指令处理本身只执行一次</li></ul></td></tr><tr><td><p><strong>userAgent</strong> <code>string</code> <strong>（可选）</strong></p><p>SDK 或客户端版本标识。非空字符串，优先于 HTTP <code>User-Agent</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-act-in-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="指令已接受"></a><section><a id="指令已接受-h4"></a><h4>指令已接受</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;content&quot;: &quot;微笑着问候，并询问我今天过得怎么样&quot;,
        &quot;accepted&quot;: true
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密的 Travel ID。</p><p><strong>content</strong> <code>string</code></p><p>已接受的指令文本。</p><p><strong>accepted</strong> <code>boolean</code></p><p>是否已接受指令并进入处理流程。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-act-in-notes-title"></a>

## 前置状态与调用注意事项

-   Travel 状态必须为 `running` 或 `paused`。
-   `content` 必填、不可为空或只有空白字符，最长 2000 字符。
-   在 `paused` 状态发送指令只会接受指令，**不会自动恢复** Travel；需要继续运行时，客户端必须另行调用[恢复Travel](happyoyster-acting-resume-travel-api-reference-e2cfa0a73db72db0.md)。
-   同一条逻辑指令重试时应复用 `clientRequestId`，以避免重复计费。
-   已结束或失败的 Travel 不可写。
-   指令未通过内容安全策略时返回 `403004`。
-   Acting 的 `creationModel` 恒为 `simple`，不需要判断 ScriptList 子模式。

<a id="错误码"></a>

<a id="ho-act-in-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-act-in-next-title"></a>

## 下一步

发送指令后：

-   [查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)：查看指令执行状态和章节信息。
-   [暂停Travel](happyoyster-acting-pause-travel-api-reference-65ff563386f561f7.md) / [恢复Travel](happyoyster-acting-resume-travel-api-reference-e2cfa0a73db72db0.md)：控制运行节奏。
-   [结束Travel](happyoyster-acting-end-travel-api-reference-07665d664cc3dbc3.md)：结束会话并处理产物。
