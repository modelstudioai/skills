# HappyOyster-Adventure-查询World构建状态 API参考

查询 Adventure World 的构建进度。接口返回加密 World ID、构建状态和首帧 URL，客户端轮询直至 World 进入 ready。

<a id="适用范围"></a>

<a id="ho-adv-qwb-scope-title"></a>

## 适用范围

查询 Adventure World 的构建进度。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：使用[创建World](happyoyster-adventure-create-world-api-reference-b764ec539142394b.md)接口返回的 `encryptedWorldId` 查询。可从 `generating` 状态开始查询。
-   **调用方**：您的服务端或客户端均可调用。

<a id="http调用"></a>

<a id="ho-adv-qwb-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-adv-qwb-req-title"></a><h4>请求参数</h4></td><td rowspan="4"><a id="sec-tabs-2"></a><section><a id="查询world构建状态"></a><section><a id="查询world构建状态-h4"></a><h4>查询World构建状态</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status?encryptedWorldId={encryptedWorldId}' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-adv-qwb-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>encryptedWorldId</strong> <code>string</code> <strong>（必选）</strong></p><p><a href="happyoyster-adventure-create-world-api-reference-b764ec539142394b.md">创建World</a>接口返回的加密 World ID，由服务端加密生成，无需自行解密。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-adv-qwb-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="构建中"></a><section><a id="构建中-h4"></a><h4>构建中</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;status&quot;: &quot;generating&quot;,
        &quot;firstFrame&quot;: null
    }
}
</code></pre></section><a id="构建完成"></a><section><a id="构建完成-h4"></a><h4>构建完成</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;status&quot;: &quot;ready&quot;,
        &quot;firstFrame&quot;: &quot;https://cdn.happyoyster.com/frames/world_xyz789.jpg&quot;,
        &quot;name&quot;: &quot;赛博朋克侦探世界&quot;,
        &quot;mode&quot;: 1
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedWorldId</strong> <code>string</code></p><p>加密 World ID。</p><p><strong>status</strong> <code>string</code></p><p>构建状态：</p><ul><li><code>generating</code>：构建中</li><li><code>ready</code>：就绪，可换取体验凭证并进房</li><li><code>failed</code>：构建失败</li></ul><p><strong>firstFrame</strong> <code>string</code></p><p>World 首帧 URL；尚未生成或构建失败时为 <code>null</code>。</p><p><strong>name</strong> <code>string</code></p><p>World 名称。仅 <code>status=ready</code> 时返回。</p><p><strong>mode</strong> <code>integer</code></p><p>Adventure 恒为 <code>1</code>。仅 <code>status=ready</code> 时返回。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-adv-qwb-notes-title"></a>

## 前置状态与调用注意事项

-   建议每 3–5 秒轮询，直到 `status` 为 `ready` 或 `failed`。
-   只有 `ready` 的 World 才能[换取体验凭证](happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md)并[进入房间](happyoyster-adventure-enter-travel-api-reference-3eb107188008bbaf.md)。
-   URL 图片在异步转存后校验失败时，World 可能从 `generating` 进入 `failed`。
-   本接口不返回 `aspectRatio`；需要 `perspective`、`uploadMode` 等创建元数据时，请调用[查询World详情](happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)。

<a id="错误码"></a>

<a id="ho-adv-qwb-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-adv-qwb-next-title"></a>

## 下一步

World 进入 `ready` 后：

-   [获取体验凭证](happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md)：换取一次性 `ticket`。
-   [查询World详情](happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)：查询完整创建元数据。
