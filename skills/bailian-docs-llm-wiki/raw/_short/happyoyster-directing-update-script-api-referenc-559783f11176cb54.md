# HappyOyster-Directing-剧本全量更新 API参考

在剧本模式 Travel 中提交完整的 45 个 turn，全量替换当前 Travel 的 acts。仅 creationModel=scriptlist 支持。

<a id="适用范围"></a>

<a id="ho-dir-us-scope-title"></a>

## 适用范围

在剧本模式（`creationModel=scriptlist`）Travel 中提交完整的 45 个 turn，全量替换当前 Travel 的 `acts`。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 的 `creationModel` 必须为 `scriptlist`，状态需为 `running` 或 `pending`。可通过[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

<a id="http调用"></a>

<a id="ho-dir-us-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/update-script`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/update-script`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-us-req-title"></a><h4>请求参数</h4></td><td rowspan="8"><a id="sec-tabs-2"></a><section><a id="剧本全量更新"></a><section><a id="剧本全量更新-h4"></a><h4>剧本全量更新</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/update-script' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedTravelId&quot;: &quot;{encryptedTravelId}&quot;,
    &quot;scriptList&quot;: {
        &quot;acts&quot;: [
            {
                &quot;turn&quot;: 1,
                &quot;content&quot;: &quot;[character_1] wakes up and looks toward the door.&quot;,
                &quot;cameraType&quot;: &quot;Static&quot;,
                &quot;shotSize&quot;: &quot;Medium&quot;,
                &quot;cut&quot;: &quot;long-take&quot;
            },
            {
                &quot;turn&quot;: 2,
                &quot;content&quot;: &quot;[character_1] walks slowly across the dark room.&quot;,
                &quot;cameraType&quot;: &quot;Tracking&quot;,
                &quot;shotSize&quot;: &quot;Wide&quot;,
                &quot;cut&quot;: &quot;hard-cut&quot;
            }
        ]
    },
    &quot;userAgent&quot;: &quot;your-client/1.2.0&quot;
}'
</code></pre></section></section><blockquote><p>示例中仅展示第 1、2 个 act 用于说明结构，<strong>不可直接提交</strong>。实际请求必须包含 turn 1–45 共 45 条，连续且不重复。</p></blockquote></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-dir-us-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>要更新的 Directing 加密 Travel ID，<code>creationModel</code> 必须为 <code>scriptlist</code>。由<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">客户端进入房间</a>接口返回。</p></td></tr><tr><td><p><strong>scriptList</strong> <code>object</code> <strong>（必选）</strong></p><p>全量剧本容器。仅 <code>acts</code> 生效；即使包含 <code>subjects</code>、<code>synopsis</code>、<code>scene</code>、<code>style</code>、<code>speed</code>、<code>language</code>、<code>setting</code>、<code>soundtrack</code>、<code>prologue</code> 或 <code>videoTags</code>，这些字段也会被忽略，平台继续使用创建 World 时已保存的值。</p><p><strong>scriptList.acts</strong> <code>array</code> <strong>（必选）</strong></p><p>完整 act 列表。约束：</p><ul><li>必须恰好 45 条</li><li><code>turn</code> 必须覆盖 1–45，连续且不可重复</li><li><code>content</code> 非空，单拍最长 2000 字；全部 <code>content</code> 合计最长 100000 字</li><li><code>cameraType</code>（可选，默认 <code>Static</code>）、<code>shotSize</code>（可选 <code>Wide</code> / <code>Medium</code> / <code>Close-up</code>，默认 <code>Medium</code>）、<code>cut</code>（可选，默认 <code>long-take</code>）</li></ul><p>本接口是全量替换，不支持只提交发生变化的 turn。</p></td></tr><tr><td><p><strong>userAgent</strong> <code>string</code> <strong>（可选）</strong></p><p>SDK 或客户端版本标识。非空字符串，优先于 HTTP <code>User-Agent</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-us-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="更新已接受"></a><section><a id="更新已接受-h4"></a><h4>更新已接受</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;accepted&quot;: true,
        &quot;turnCount&quot;: 45
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密的 Travel ID。</p><p><strong>accepted</strong> <code>boolean</code></p><p>是否已接受完整剧本并进入处理流程。</p><p><strong>turnCount</strong> <code>integer</code></p><p>本次全量更新的 turn 数，固定为 <code>45</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-us-notes-title"></a>

## 前置状态与调用注意事项

-   仅 `creationModel=scriptlist` 支持本接口；普通模式 Travel 误调用返回 `409000`。
-   Travel 状态必须为 `running` 或 `pending`。
-   `acts` 必须恰好 45 条；turn 必须为 1–45，连续且不可重复，否则返回 `400000`。
-   剧本内容未通过内容安全策略时返回 `403004`；触发版权或 IP 合规拒绝时返回 `403005`。

<a id="错误码"></a>

<a id="ho-dir-us-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-us-next-title"></a>

## 下一步

更新后：

-   [查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)：查看章节信息。
-   [暂停Travel](happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md) / [回溯Travel](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md)。
-   [结束Travel](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)：结束会话并处理产物。
