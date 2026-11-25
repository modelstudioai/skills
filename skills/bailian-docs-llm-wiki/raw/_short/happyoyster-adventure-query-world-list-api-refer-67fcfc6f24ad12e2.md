# HappyOyster-Adventure-查询World列表 API参考

分页查询当前主账号名下的 Adventure World。接口自动按模型隔离，不会返回 Directing 或 Acting World。

<a id="适用范围"></a>

<a id="ho-adv-qwl-scope-title"></a>

## 适用范围

分页查询当前主账号名下的 Adventure World。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **调用方**：您的服务端调用。
    

<a id="http调用"></a>

<a id="ho-adv-qwl-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-adv-qwl-req-title"></a><h4>请求参数</h4></td><td rowspan="7"><a id="sec-tabs-2"></a><section><a id="查询world列表"></a><section><a id="查询world列表-h4"></a><h4>查询World列表</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds?page=1&amp;pageSize=20&amp;status=ready' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-adv-qwl-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>page</strong> <code>integer</code> <strong>（可选）</strong></p><p>页码，默认 <code>1</code>。<code>page &lt;= 0</code> 时按 <code>1</code> 处理。</p></td></tr><tr><td><p><strong>pageSize</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页条数，默认 <code>20</code>。<code>pageSize &lt;= 0</code> 时按 <code>20</code>，大于 <code>100</code> 时按 <code>100</code> 处理。</p></td></tr><tr><td><p><strong>status</strong> <code>string</code> <strong>（可选）</strong></p><p>按构建状态筛选。未知值不筛选。可选值：</p><ul><li><code>generating</code>：构建中</li><li><code>ready</code>：就绪</li><li><code>failed</code>：构建失败</li></ul></td></tr><tr><td><p><strong>mode</strong> <code>integer</code> <strong>（可选）</strong></p><p>无需传入。列表已按 Adventure 模型过滤，<code>items[].mode</code> 恒为 <code>1</code>。若仍传入且非 <code>1</code> 返回 <code>400000</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-adv-qwl-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="查询成功"></a><section><a id="查询成功-h4"></a><h4>查询成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;items&quot;: [
            {
                &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
                &quot;name&quot;: &quot;赛博朋克侦探世界&quot;,
                &quot;status&quot;: &quot;ready&quot;,
                &quot;mode&quot;: 1,
                &quot;previewUrl&quot;: null,
                &quot;createdAt&quot;: &quot;2026-06-03T10:00:00Z&quot;,
                &quot;perspective&quot;: &quot;first_person&quot;,
                &quot;creationModel&quot;: &quot;simple&quot;,
                &quot;uploadMode&quot;: &quot;first_frame&quot;
            }
        ],
        &quot;pagination&quot;: {
            &quot;page&quot;: 1,
            &quot;pageSize&quot;: 20,
            &quot;total&quot;: 1,
            &quot;hasMore&quot;: false
        }
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>items</strong> <code>array</code></p><p>当前页 World 列表；无结果时为空数组。每项含 <code>encryptedWorldId</code>、<code>name</code>、<code>status</code>（<code>generating</code> / <code>ready</code> / <code>failed</code>）、<code>mode</code>（恒为 <code>1</code>）、<code>previewUrl</code>（通常为 <code>null</code>）、<code>createdAt</code>、<code>perspective</code>（<code>first_person</code> / <code>third_person</code>）、<code>creationModel</code>（恒为 <code>simple</code>）、<code>uploadMode</code>（固定为 <code>first_frame</code>）。</p><p><strong>pagination</strong> <code>object</code></p><p>分页信息。含 <code>page</code>、<code>pageSize</code>、<code>total</code>、<code>hasMore</code>（<code>page × pageSize &lt; total</code> 时为 <code>true</code>）。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-adv-qwl-notes-title"></a>

## 前置状态与调用注意事项

-   列表项是轻量快照，不返回图片、Prompt、`refWorldId` 或其它完整创建参数；需要完整配置时调用[查询World详情](happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)。
-   未知 `status` 不会报错，而是按不筛选状态处理。
-   翻页时应使用响应中的 `pagination.pageSize` 和 `hasMore`，不要假设请求值一定原样采用。
-   空结果不是错误，返回 `items=[]` 和对应分页信息。

<a id="错误码"></a>

<a id="ho-adv-qwl-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-adv-qwl-next-title"></a>

## 下一步

-   [查询World详情](happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)：查看单个 World 完整元数据。
-   [删除World](happyoyster-adventure-delete-world-api-reference-55040f62da8f233e.md)：删除不再使用的 World。
