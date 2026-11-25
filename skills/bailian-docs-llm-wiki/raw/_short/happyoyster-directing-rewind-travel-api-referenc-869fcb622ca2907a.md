# HappyOyster-Directing-回溯Travel API参考

将 Travel 回溯到指定视频时间点，并从实际落点恢复运行。Travel 必须先进入 paused 状态。

<a id="适用范围"></a>

<a id="ho-dir-rw-scope-title"></a>

## 适用范围

将 Travel 回溯到指定视频时间点，并从实际落点恢复运行。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 必须先进入 `paused` 状态，不能在 `running` 时直接回溯。可通过[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

<a id="http调用"></a>

<a id="ho-dir-rw-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/rewind`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/rewind`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-rw-req-title"></a><h4>请求参数</h4></td><td rowspan="6"><a id="sec-tabs-2"></a><section><a id="回溯travel"></a><section><a id="回溯travel-h4"></a><h4>回溯Travel</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/rewind' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedTravelId&quot;: &quot;{encryptedTravelId}&quot;,
    &quot;rewindToSec&quot;: 84.0,
    &quot;userAgent&quot;: &quot;your-client/1.2.0&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-dir-rw-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>要回溯的 Directing 加密 Travel ID。由<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">客户端进入房间</a>接口返回。</p></td></tr><tr><td><p><strong>rewindToSec</strong> <code>number</code> <strong>（必选）</strong></p><p>目标视频时间，单位秒。大于或等于 <code>0</code>，建议为 4 的倍数（如 4、8、12）。服务端按 <code>Math.round(rewindToSec / 4) × 4</code> 四舍五入到最近的 4 秒边界。实际落点以响应中的 <code>resumedAtSec</code> / <code>actualRewindToSec</code> 为准。</p><p><strong>userAgent</strong> <code>string</code> <strong>（可选）</strong></p><p>SDK 或客户端版本标识。非空字符串，优先于 HTTP <code>User-Agent</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-rw-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="回溯成功"></a><section><a id="回溯成功-h4"></a><h4>回溯成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;status&quot;: &quot;running&quot;,
        &quot;resumedAtSec&quot;: 84.0,
        &quot;actualRewindToSec&quot;: 84.0
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密的 Travel ID。</p><p><strong>status</strong> <code>string</code></p><p>回溯完成后的状态，返回 <code>running</code>。</p><p><strong>resumedAtSec</strong> <code>number</code></p><p>实际恢复播放的秒数，可能与请求值略有偏差。</p><p><strong>actualRewindToSec</strong> <code>number</code></p><p>实际回溯落点，与 <code>resumedAtSec</code> 相同。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-rw-notes-title"></a>

## 前置状态与调用注意事项

-   Travel 必须先进入 `paused`；不能在 `running` 时直接回溯。
-   [暂停Travel](happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md)存在约 3 秒的异步确认屏障。收到 pause 响应后，仍应轮询[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)，确认对外状态已经是 `paused` 再调用本接口。
-   剧本按 4 秒 Block 组织，`rewindToSec` 建议使用 4、8、12 等 4 的倍数（如 `6 → 8`）。
-   实际落点以 `resumedAtSec` / `actualRewindToSec` 为准。

<a id="错误码"></a>

<a id="ho-dir-rw-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-rw-next-title"></a>

## 下一步

回溯后 Travel 回到 `running`：

-   [查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)：确认运行状态。
-   普通模式：[发送过程指令](happyoyster-directing-instruct-travel-api-refere-2cd5aa6eabceb2c4.md)。
-   [暂停Travel](happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md)：再次暂停以进行下一次回溯。
-   [结束Travel](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)：结束会话并处理产物。
