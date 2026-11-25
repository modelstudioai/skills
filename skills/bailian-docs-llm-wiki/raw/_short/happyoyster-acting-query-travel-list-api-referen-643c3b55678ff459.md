# HappyOyster-Acting-查询Travel列表 API参考

分页查询当前主账号名下的 Acting Travel，可按状态或关联 World 筛选。

<a id="适用范围"></a>

<a id="ho-act-qtl-scope-title"></a>

## 适用范围

分页查询当前主账号名下的 Acting Travel，可按状态或关联 World 筛选。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **调用方**：您的服务端调用。
    

<a id="http调用"></a>

<a id="ho-act-qtl-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-act-qtl-req-title"></a><h4>请求参数</h4></td><td rowspan="7"><a id="sec-tabs-2"></a><section><a id="查询travel列表"></a><section><a id="查询travel列表-h4"></a><h4>查询Travel列表</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels?page=1&amp;pageSize=20&amp;status=completed&amp;encryptedWorldId={encryptedWorldId}' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-act-qtl-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>page</strong> <code>integer</code> <strong>（可选）</strong></p><p>页码，默认 <code>1</code>。<code>page &lt;= 0</code> 时按 <code>1</code> 处理。</p></td></tr><tr><td><p><strong>pageSize</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页条数，默认 <code>20</code>。<code>pageSize &lt;= 0</code> 时按 <code>20</code>，大于 <code>100</code> 时按 <code>100</code> 处理。</p></td></tr><tr><td><p><strong>status</strong> <code>string</code> <strong>（可选）</strong></p><p>按 Travel 状态筛选。未知值不筛选。可选值：</p><ul><li><code>init</code>：正在初始化会话资源</li><li><code>pending</code>：排队或等待服务资源</li><li><code>running</code>：正在运行</li><li><code>failed</code>：Travel 失败；原因见 <code>errorCode</code> / <code>errorMessage</code></li><li><code>completed</code>：Travel 已结束，可查询产物</li></ul></td></tr><tr><td><p><strong>encryptedWorldId</strong> <code>string</code> <strong>（可选）</strong></p><p>当前主账号名下的 Acting World ID。传入时仅返回该 World 的 Travel。本接口不支持 <code>mode</code> Query 参数，模型专属入口会自动限定为 Acting。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-act-qtl-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="查询成功"></a><section><a id="查询成功-h4"></a><h4>查询成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;items&quot;: [
            {
                &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
                &quot;status&quot;: &quot;completed&quot;,
                &quot;mode&quot;: 3,
                &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
                &quot;durationSec&quot;: 180,
                &quot;createdAt&quot;: &quot;2026-09-09T08:10:00Z&quot;,
                &quot;endedAt&quot;: &quot;2026-09-09T08:13:00Z&quot;
            },
            {
                &quot;encryptedTravelId&quot;: &quot;trvl_g7h8****&quot;,
                &quot;status&quot;: &quot;running&quot;,
                &quot;mode&quot;: 3,
                &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
                &quot;durationSec&quot;: null,
                &quot;createdAt&quot;: &quot;2026-09-09T09:10:00Z&quot;,
                &quot;endedAt&quot;: null
            },
            {
                &quot;encryptedTravelId&quot;: &quot;trvl_m3n4****&quot;,
                &quot;status&quot;: &quot;failed&quot;,
                &quot;mode&quot;: 3,
                &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
                &quot;durationSec&quot;: null,
                &quot;createdAt&quot;: &quot;2026-09-09T10:10:00Z&quot;,
                &quot;endedAt&quot;: &quot;2026-09-09T10:10:05Z&quot;,
                &quot;errorCode&quot;: &quot;TRAVEL_SESSION_INIT_FAILED&quot;,
                &quot;errorMessage&quot;: &quot;Failed to allocate inference resources.&quot;
            }
        ],
        &quot;pagination&quot;: {
            &quot;page&quot;: 1,
            &quot;pageSize&quot;: 20,
            &quot;total&quot;: 3,
            &quot;hasMore&quot;: false
        }
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>items</strong> <code>array</code></p><p>当前页 Travel 列表；无结果时为空数组。每项含 <code>encryptedTravelId</code>、<code>status</code>、<code>mode</code>（恒为 <code>3</code>）、<code>encryptedWorldId</code>、<code>durationSec</code>（进行中、失败或时长尚不可用时为 <code>null</code>）、<code>createdAt</code>、<code>endedAt</code>（进行中时为 <code>null</code>）；<code>status=failed</code> 的条目额外携带 <code>errorCode</code>（结构化失败原因，取值见<a href="happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md">查询Travel状态</a>）和 <code>errorMessage</code>（英文说明），其它状态没有这两个键。</p><p><strong>pagination</strong> <code>object</code></p><p>分页信息。含 <code>page</code>、<code>pageSize</code>、<code>total</code>、<code>hasMore</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-act-qtl-notes-title"></a>

## 前置状态与调用注意事项

-   接口自动只返回 Acting Travel，`items[].mode` 恒为 `3`。
-   使用 `encryptedWorldId` 筛选时，该 World 必须属于当前主账号和 Acting 模型；其它模型的 World 返回 `403001`。
-   进行中 Travel 的 `durationSec` 和 `endedAt` 通常为 `null`。
-   `failed` 条目额外携带 `errorCode` / `errorMessage`，其它状态的条目没有这两个键；历史列表展示失败原因时以 `errorCode` 为准。
-   未知 `status` 不会报错，而是按不筛选状态处理；查询单个 Travel 的实时 `paused` 状态应使用[查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)。
-   空结果不是错误，返回 `items=[]` 和对应分页信息。

<a id="错误码"></a>

<a id="ho-act-qtl-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-act-qtl-next-title"></a>

## 下一步

-   [查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)：查询单个 Travel 的实时状态。
-   [查询Travel产物](happyoyster-acting-query-travel-artifacts-api-re-af546d869e863975.md)：查询已完成 Travel 的视频产物。
