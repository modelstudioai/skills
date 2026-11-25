# HappyOyster-Acting-查询World详情 API参考

查询单个 Acting World 的完整元数据和可回显创建参数。构建进度轮询请使用查询World构建状态接口。

<a id="适用范围"></a>

<a id="ho-act-qwd-scope-title"></a>

## 适用范围

查询单个 Acting World 的完整元数据和可回显创建参数。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **前置条件**：使用[创建World](happyoyster-acting-create-world-api-reference-47f1f4ec26522c7d.md)接口返回的 `encryptedWorldId` 查询。构建进度轮询应使用[查询World构建状态](happyoyster-acting-query-world-build-status-api--5436f98af63bbe85.md)。
    
-   **调用方**：您的服务端调用。
    

<a id="http调用"></a>

<a id="ho-act-qwd-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-act-qwd-req-title"></a><h4>请求参数</h4></td><td rowspan="4"><a id="sec-tabs-2"></a><section><a id="查询world详情"></a><section><a id="查询world详情-h4"></a><h4>查询World详情</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/detail?encryptedWorldId={encryptedWorldId}' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-act-qwd-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>encryptedWorldId</strong> <code>string</code> <strong>（必选）</strong></p><p>当前主账号名下的 Acting 加密 World ID。由<a href="happyoyster-acting-create-world-api-reference-47f1f4ec26522c7d.md">创建World</a>接口返回。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-act-qwd-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;name&quot;: &quot;深夜视频通话&quot;,
        &quot;status&quot;: &quot;ready&quot;,
        &quot;mode&quot;: 3,
        &quot;creationModel&quot;: &quot;simple&quot;,
        &quot;prompt&quot;: &quot;深夜视频通话中，一位安静的女孩微笑着回应镜头&quot;,
        &quot;eventStyle&quot;: &quot;first_frame&quot;,
        &quot;perspective&quot;: null,
        &quot;uploadMode&quot;: &quot;first_frame&quot;,
        &quot;resolution&quot;: &quot;480p&quot;,
        &quot;aspectRatio&quot;: &quot;9:16&quot;,
        &quot;layout&quot;: null,
        &quot;narrative&quot;: null,
        &quot;refWorldId&quot;: null,
        &quot;firstFrameImage&quot;: {
            &quot;url&quot;: &quot;https://cdn.happyoyster.com/frames/portrait-call.jpg&quot;,
            &quot;referenceType&quot;: &quot;default&quot;
        },
        &quot;inputImages&quot;: null,
        &quot;sceneImage&quot;: null,
        &quot;roleImage&quot;: null,
        &quot;scenePrompt&quot;: null,
        &quot;rolePrompt&quot;: null,
        &quot;scriptList&quot;: null,
        &quot;previewUrl&quot;: null,
        &quot;createdAt&quot;: &quot;2026-09-09T08:00:00Z&quot;,
        &quot;updatedAt&quot;: &quot;2026-09-09T08:05:00Z&quot;
    }
}
</code></pre></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedWorldId</strong> <code>string</code></p><p>加密 World ID。</p><p><strong>name</strong> <code>string</code></p><p>World 名称。</p><p><strong>status</strong> <code>string</code></p><p>构建状态：<code>generating</code> / <code>ready</code> / <code>failed</code>。</p><p><strong>mode</strong> <code>integer</code></p><p>Acting 恒为 <code>3</code>。</p><p><strong>creationModel</strong> <code>string</code></p><p>Acting 恒为 <code>simple</code>。</p><p><strong>prompt</strong> <code>string</code></p><p>创建时提交的顶层 Prompt。</p><p><strong>eventStyle</strong> <code>string</code></p><p>兼容返回字段；合规创建省略该字段时，服务端通常按 <code>uploadMode</code> 映射并回显 <code>first_frame</code>。它不是 Acting 的创建参数，客户端不应主动回传。</p><p><strong>perspective</strong> <code>null</code></p><p>Acting 不接受视角创建参数，固定为 <code>null</code>。</p><p><strong>uploadMode</strong> <code>string</code></p><p>固定为 <code>first_frame</code>。</p><p><strong>resolution</strong> <code>string</code></p><p><code>480p</code> / <code>720p</code>；创建时未传则为 <code>480p</code>。</p><p><strong>aspectRatio</strong> <code>string</code></p><p><code>9:16</code> / <code>16:9</code>；创建时未传则为 <code>9:16</code>。</p><p><strong>layout</strong> <code>null</code></p><p>Acting 不接受该创建参数，固定为 <code>null</code>。</p><p><strong>narrative</strong> <code>null</code></p><p>Acting 不接受该创建参数，固定为 <code>null</code>。</p><p><strong>refWorldId</strong> <code>string</code></p><p>衍生创建时使用的 Acting 加密参考 World ID；无则为 <code>null</code>。</p><p><strong>firstFrameImage</strong> <code>object</code></p><p>创建时的必填首帧图；只返回 URL 形式，不回传 base64。含 <code>url</code> 和 <code>referenceType</code>。</p><p><strong>inputImages</strong> <code>null</code></p><p>Acting 当前不使用该字段。</p><p><strong>sceneImage</strong> <code>null</code></p><p>Acting 不使用场景角色图片槽位，固定为 <code>null</code>。</p><p><strong>roleImage</strong> <code>null</code></p><p>Acting 不使用场景角色图片槽位，固定为 <code>null</code>。</p><p><strong>scenePrompt</strong> <code>null</code></p><p>Acting 不使用场景角色文案，固定为 <code>null</code>。</p><p><strong>rolePrompt</strong> <code>null</code></p><p>Acting 不使用场景角色文案，固定为 <code>null</code>。</p><p><strong>scriptList</strong> <code>null</code></p><p>Acting 不支持 ScriptList，固定为 <code>null</code>。</p><p><strong>previewUrl</strong> <code>null</code></p><p>当前固定为 <code>null</code>。</p><p><strong>createdAt</strong> <code>string</code></p><p>创建时间，ISO 8601 格式。</p><p><strong>updatedAt</strong> <code>string</code></p><p>最近更新时间，ISO 8601 格式。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-act-qwd-notes-title"></a>

## 前置状态与调用注意事项

-   本接口可查询 `generating`、`ready` 或 `failed` World；部分构建产物在未就绪时可能为 `null`。
-   详情接口不回显 `async`，因为它是调用行为开关，不是 World 属性。
-   图片只返回 URL 和 `referenceType`，不会回传创建请求中的 base64 内容。
-   `eventStyle` 通常与 `uploadMode` 同值；客户端应以 `uploadMode` 作为 Acting 创建模式的权威字段。
-   播放器可预先读取 `aspectRatio`，但实际进房时仍应以[进入房间](happyoyster-acting-enter-travel-api-reference-56ea4df0a872fdb7.md)响应值设置方向。
-   查询其它模型、其它主账号或已删除的 World 均返回 `403001`，不会泄漏资源是否存在。

<a id="错误码"></a>

<a id="ho-act-qwd-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-act-qwd-next-title"></a>

## 下一步

-   [查询World列表](happyoyster-acting-query-world-list-api-referenc-3550b0de031bc3dc.md)：分页查询所有 Acting World。
-   [删除World](happyoyster-acting-delete-world-api-reference-e7a48c5a6f87668c.md)：删除不再使用的 World。
-   World 为 `ready` 时可[获取体验凭证](happyoyster-acting-get-travel-credential-api-ref-dfc7dc5832959ca8.md)。
