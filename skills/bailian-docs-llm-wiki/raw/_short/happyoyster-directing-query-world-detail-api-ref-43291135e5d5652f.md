# HappyOyster-Directing-查询World详情 API参考

查询单个 Directing World 的当前状态、创建参数和可返回的 ScriptList 信息。构建进度轮询请使用查询World构建状态接口。

<a id="适用范围"></a>

<a id="ho-dir-qwd-scope-title"></a>

## 适用范围

查询单个 Directing World 的当前状态、创建参数和可返回的 ScriptList 信息。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **前置条件**：使用[创建World](happyoyster-directing-create-world-api-reference-6f3bdbbb6537960b.md)接口返回的 `encryptedWorldId` 查询。构建进度轮询应使用[查询World构建状态](happyoyster-directing-query-world-build-status-a-48bf75e27c43945d.md)。
    
-   **调用方**：您的服务端调用。
    

<a id="http调用"></a>

<a id="ho-dir-qwd-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-qwd-req-title"></a><h4>请求参数</h4></td><td rowspan="4"><a id="sec-tabs-2"></a><section><a id="查询world详情"></a><section><a id="查询world详情-h4"></a><h4>查询World详情</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/detail?encryptedWorldId={encryptedWorldId}' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-dir-qwd-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>encryptedWorldId</strong> <code>string</code> <strong>（必选）</strong></p><p>当前主账号名下的 Directing 加密 World ID。由<a href="happyoyster-directing-create-world-api-reference-6f3bdbbb6537960b.md">创建World</a>接口返回。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-qwd-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="查询成功-剧本模式"></a><section><a id="查询成功-剧本模式-h4"></a><h4>查询成功（剧本模式）</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;name&quot;: &quot;午夜访客&quot;,
        &quot;status&quot;: &quot;ready&quot;,
        &quot;mode&quot;: 2,
        &quot;creationModel&quot;: &quot;scriptlist&quot;,
        &quot;prompt&quot;: null,
        &quot;eventStyle&quot;: &quot;normal&quot;,
        &quot;perspective&quot;: null,
        &quot;uploadMode&quot;: null,
        &quot;resolution&quot;: &quot;720p&quot;,
        &quot;layout&quot;: null,
        &quot;narrative&quot;: null,
        &quot;refWorldId&quot;: null,
        &quot;firstFrameImage&quot;: {
            &quot;url&quot;: &quot;https://cdn.happyoyster.com/frames/room.png&quot;,
            &quot;referenceType&quot;: &quot;default&quot;
        },
        &quot;inputImages&quot;: null,
        &quot;scriptList&quot;: {
            &quot;synopsis&quot;: &quot;深夜，苏黎被敲门声惊醒。&quot;,
            &quot;videoTitle&quot;: &quot;午夜访客&quot;,
            &quot;subjects&quot;: [
                {
                    &quot;label&quot;: &quot;[character_1]&quot;,
                    &quot;name&quot;: &quot;苏黎&quot;,
                    &quot;type&quot;: &quot;character&quot;,
                    &quot;refImage&quot;: {
                        &quot;url&quot;: &quot;https://cdn.happyoyster.com/subjects/suli.png&quot;,
                        &quot;referenceType&quot;: &quot;default&quot;
                    }
                }
            ],
            &quot;acts&quot;: [
                {
                    &quot;turn&quot;: 1,
                    &quot;content&quot;: &quot;雨水拍打窗户，[character_1] 从睡梦中惊醒。&quot;,
                    &quot;cameraType&quot;: &quot;Static&quot;,
                    &quot;shotSize&quot;: &quot;Wide&quot;,
                    &quot;cut&quot;: &quot;long-take&quot;
                },
                {
                    &quot;turn&quot;: 2,
                    &quot;content&quot;: &quot;[character_1] 走向房门，门外再次响起敲门声。&quot;,
                    &quot;cameraType&quot;: &quot;Push-in&quot;,
                    &quot;shotSize&quot;: &quot;Close-up&quot;,
                    &quot;cut&quot;: &quot;long-take&quot;
                }
            ]
        },
        &quot;previewUrl&quot;: null,
        &quot;aspectRatio&quot;: null,
        &quot;createdAt&quot;: &quot;2026-06-03T10:00:00Z&quot;,
        &quot;updatedAt&quot;: &quot;2026-06-03T10:05:00Z&quot;
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedWorldId</strong> <code>string</code></p><p>加密 World ID。</p><p><strong>name</strong> <code>string</code></p><p>World 名称。</p><p><strong>status</strong> <code>string</code></p><p>构建状态：<code>generating</code> / <code>ready</code> / <code>failed</code>。</p><p><strong>mode</strong> <code>integer</code></p><p>Directing 恒为 <code>2</code>。</p><p><strong>creationModel</strong> <code>string</code></p><p><code>simple</code> / <code>scriptlist</code>；决定 Travel 可调用的控制接口。</p><p><strong>prompt</strong> <code>string</code></p><p><code>simple</code> 模式创建时的 Prompt；<code>scriptlist</code> 固定为 <code>null</code>。</p><p><strong>eventStyle</strong> <code>string</code></p><p>创建时的事件风格：<code>normal</code> / <code>dramatic</code> / <code>regular</code>。</p><p><strong>perspective</strong> <code>null</code></p><p>Directing 模型通常为 <code>null</code>。</p><p><strong>uploadMode</strong> <code>null</code></p><p>Directing World 通常为 <code>null</code>。</p><p><strong>resolution</strong> <code>string</code></p><p><code>480p</code> / <code>720p</code>。</p><p><strong>layout</strong> <code>string</code></p><p><code>simple</code> 模式的镜头运动风格；未传或 <code>scriptlist</code> 时通常为 <code>null</code>。</p><p><strong>narrative</strong> <code>string</code></p><p><code>simple</code> 模式的叙事风格；未传或 <code>scriptlist</code> 时通常为 <code>null</code>。</p><p><strong>refWorldId</strong> <code>string</code></p><p>衍生创建时使用的加密参考 World ID。</p><p><strong>firstFrameImage</strong> <code>object</code></p><p>创建时的首帧图；响应不返回 base64。</p><p><strong>inputImages</strong> <code>array</code></p><p><code>simple</code> 模式创建时持久化的参考图；<code>scriptlist</code> 不接受该字段，通常为 <code>null</code>。</p><p><strong>scriptList</strong> <code>object</code></p><p>仅 <code>scriptlist</code> World 有值；结构化剧本反解失败时为 <code>null</code>。含 <code>synopsis</code>、<code>videoTitle</code>、<code>scene</code>、<code>style</code>、<code>speed</code>、<code>language</code>、<code>setting</code>、<code>soundtrack</code>、<code>prologue</code>、<code>videoTags</code>、<code>subjects</code>（含 <code>label</code>/<code>name</code>/<code>type</code>/<code>refImage</code> 等）、<code>acts</code>（按已存内容完整返回，含 <code>turn</code>/<code>content</code>/<code>cameraType</code>/<code>shotSize</code>/<code>cut</code>）。</p><p><strong>previewUrl</strong> <code>null</code></p><p>当前固定为 <code>null</code>。</p><p><strong>aspectRatio</strong> <code>null</code></p><p>Directing 模型固定为 <code>null</code>。</p><p><strong>createdAt</strong> <code>string</code></p><p>创建时间，ISO 8601 格式。</p><p><strong>updatedAt</strong> <code>string</code></p><p>最近更新时间，ISO 8601 格式。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-qwd-notes-title"></a>

## 前置状态与调用注意事项

-   本接口可查询 `generating`、`ready` 或 `failed` World。
-   不回显创建请求中的 `async`。
-   图片字段只返回 URL 和 `referenceType`，不会回传 base64。`simple` 模式的 `inputImages` 会作为参考图持久化并可在详情中返回；`scriptlist` 不接受该字段。
-   `scriptList` 正常反解时返回已保存的完整结构，`acts` 按已存内容完整返回；反解失败时返回 `scriptList=null`，不会用空 `acts` 表示反解失败。
-   查询其它模型、其它主账号或已删除的 World 均返回 `403001`，不会泄漏资源是否存在。

<a id="错误码"></a>

<a id="ho-dir-qwd-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-qwd-next-title"></a>

## 下一步

-   [查询World列表](happyoyster-directing-query-world-list-api-refer-77a7187e20e73d36.md)：分页查询所有 Directing World。
-   [删除World](happyoyster-directing-delete-world-api-reference-3e47ecd2da7486dd.md)：删除不再使用的 World。
-   World 为 `ready` 时可[获取体验凭证](happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md)。
