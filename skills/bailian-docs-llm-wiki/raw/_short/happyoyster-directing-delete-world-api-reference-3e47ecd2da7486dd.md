# HappyOyster-Directing-删除World API参考

删除当前主账号名下的 Directing World。同账号下 World 已不存在时幂等返回 deleted=false。

<a id="适用范围"></a>

<a id="ho-dir-dw-scope-title"></a>

## 适用范围

删除当前主账号名下的 Directing World。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **前置条件**：使用[创建World](happyoyster-directing-create-world-api-reference-6f3bdbbb6537960b.md)接口返回的 `encryptedWorldId` 删除。
    
-   **调用方**：您的服务端调用。本接口不接受请求体字段 `userAgent`。
    

<a id="http调用"></a>

<a id="ho-dir-dw-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/delete`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/delete`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-dw-req-title"></a><h4>请求参数</h4></td><td rowspan="5"><a id="sec-tabs-2"></a><section><a id="删除world"></a><section><a id="删除world-h4"></a><h4>删除World</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/delete' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedWorldId&quot;: &quot;{encryptedWorldId}&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-dir-dw-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedWorldId</strong> <code>string</code> <strong>（必选）</strong></p><p>要删除的 Directing 加密 World ID。由<a href="happyoyster-directing-create-world-api-reference-6f3bdbbb6537960b.md">创建World</a>接口返回。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-dw-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="删除成功"></a><section><a id="删除成功-h4"></a><h4>删除成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;deleted&quot;: true
    }
}
</code></pre></section><a id="world-已不存在"></a><section><a id="world-已不存在-h4"></a><h4>World 已不存在</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;deleted&quot;: false
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedWorldId</strong> <code>string</code></p><p>请求中的加密 World ID。</p><p><strong>deleted</strong> <code>boolean</code></p><p><code>true</code> 表示已删除；<code>false</code> 表示本次未删除到 World。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-dw-notes-title"></a>

## 前置状态与调用注意事项

-   同账号下 World 已不存在时返回 `code=0` 且 `deleted=false`，不返回 `403001`。
-   ID 可解析但跨账号、workspace 不匹配或资源不是 Directing World 时，返回 `403001`。
-   删除后继续查询该 World 时，按不存在或已删除资源处理。

<a id="错误码"></a>

<a id="ho-dir-dw-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-dw-next-title"></a>

## 下一步

-   [查询World列表](happyoyster-directing-query-world-list-api-refer-77a7187e20e73d36.md)：查看剩余 Directing World。
-   [创建World](happyoyster-directing-create-world-api-reference-6f3bdbbb6537960b.md)：创建新的 Directing World。
