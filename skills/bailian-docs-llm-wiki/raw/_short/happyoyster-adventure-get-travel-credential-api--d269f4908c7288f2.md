# HappyOyster-Adventure-获取体验凭证 API参考

三方服务端使用主 API Key 换取短时效、一次性的 ticket，再将其安全下发给客户端。此接口只校验 World 归属、状态与规格，不创建 Travel。

<a id="适用范围"></a>

<a id="ho-adv-gtc-scope-title"></a>

## 适用范围

三方服务端使用主 API Key 换取短时效、一次性的 `ticket`，再将其安全下发给客户端。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **前置条件**：World 必须属于当前主账号和 Adventure 模型，且状态为 `ready`。可通过[查询World构建状态](happyoyster-adventure-query-world-build-status-a-4830e59b84023226.md)接口确认。
    
-   **调用方**：您的**服务端**调用，换得的 `ticket` 应只下发给准备立即进房的客户端。
    

<a id="http调用"></a>

<a id="ho-adv-gtc-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/get-travel-credential`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/get-travel-credential`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/get-travel-credential`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-adv-gtc-req-title"></a><h4>请求参数</h4></td><td rowspan="5"><a id="sec-tabs-2"></a><section><a id="获取体验凭证"></a><section><a id="获取体验凭证-h4"></a><h4>获取体验凭证</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/get-travel-credential' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedWorldId&quot;: &quot;{encryptedWorldId}&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-adv-gtc-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedWorldId</strong> <code>string</code> <strong>（必选）</strong></p><p>当前主账号名下、状态为 <code>ready</code> 的 Adventure World ID。由<a href="happyoyster-adventure-create-world-api-reference-b764ec539142394b.md">创建World</a>接口返回。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-adv-gtc-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="换取成功"></a><section><a id="换取成功-h4"></a><h4>换取成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;ticket&quot;: &quot;tk_a1b2****&quot;,
        &quot;expiresIn&quot;: 1800,
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>ticket</strong> <code>string</code></p><p>前缀为 <code>tk_</code> 的一次性 Travel 凭证。有效期 1800 秒（30 分钟），且只能成功使用一次。</p><p><strong>expiresIn</strong> <code>integer</code></p><p>有效期秒数，固定为 <code>1800</code>，即 30 分钟。</p><p><strong>encryptedWorldId</strong> <code>string</code></p><p>凭证对应的加密 World ID。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-adv-gtc-notes-title"></a>

## 前置状态与调用注意事项

-   World 必须为 `ready`。
-   `ticket` 有效期为 30 分钟且只能成功使用一次；过期或已使用后须重新换取。
-   `ticket` 应只下发给准备立即进房的客户端，不应持久化为长期访问凭证。
-   调用本接口不会创建 Travel；Travel 在[进入房间](happyoyster-adventure-enter-travel-api-reference-3eb107188008bbaf.md)成功时创建。
-   未购买该 World 对应规格时返回 `403007`；容量配置暂不可用时返回 `403008`。

<a id="错误码"></a>

<a id="ho-adv-gtc-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-adv-gtc-next-title"></a>

## 下一步

换取 `ticket` 后：

-   [客户端进入房间](happyoyster-adventure-enter-travel-api-reference-3eb107188008bbaf.md)：客户端使用 `ticket` 创建 Travel 并获取 RTC 配置。
