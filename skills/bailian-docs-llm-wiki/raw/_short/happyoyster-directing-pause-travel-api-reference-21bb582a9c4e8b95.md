# HappyOyster-Directing-暂停Travel API参考

请求暂停正在运行的 Directing Travel。暂停完成后可调用恢复或回溯。

<a id="适用范围"></a>

<a id="ho-dir-pa-scope-title"></a>

## 适用范围

请求暂停正在运行的 Directing Travel。暂停完成后可调用[恢复](happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md)或[回溯](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md)。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 状态需为 `running`。可通过[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

<a id="http调用"></a>

<a id="ho-dir-pa-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/pause`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/pause`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-pa-req-title"></a><h4>请求参数</h4></td><td rowspan="6"><a id="sec-tabs-2"></a><section><a id="暂停travel"></a><section><a id="暂停travel-h4"></a><h4>暂停Travel</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/pause' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedTravelId&quot;: &quot;{encryptedTravelId}&quot;,
    &quot;userAgent&quot;: &quot;your-client/1.2.0&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-dir-pa-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>要暂停的 Directing 加密 Travel ID。由<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">客户端进入房间</a>接口返回。</p></td></tr><tr><td><p><strong>userAgent</strong> <code>string</code> <strong>（可选）</strong></p><p>SDK 或客户端版本标识。非空字符串，优先于 HTTP <code>User-Agent</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-pa-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="暂停成功"></a><section><a id="暂停成功-h4"></a><h4>暂停成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;status&quot;: &quot;paused&quot;
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密的 Travel ID。</p><p><strong>status</strong> <code>string</code></p><p>暂停目标状态，返回 <code>paused</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-pa-notes-title"></a>

## 前置状态与调用注意事项

-   Travel 当前状态必须为 `running`。
-   进房响应中的 `version` 必须为 `storyV2`；本模型进房固定返回该值。
-   pause 的服务端状态确认是异步过程。需要紧接着调用[回溯](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md)或[恢复](happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md)时，应轮询[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)直到状态为 `paused`。

<a id="错误码"></a>

<a id="ho-dir-pa-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-pa-next-title"></a>

## 下一步

暂停后可进行以下操作：

-   [恢复Travel](happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md)：恢复已暂停的 Travel 继续运行。
-   [回溯Travel](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md)：回到指定视频时间点。
-   [结束Travel](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)：直接结束 Travel。
