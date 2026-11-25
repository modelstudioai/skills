# HappyOyster-Directing-结束Travel API参考

结束 Directing Travel。正常结束时状态变为 completed 并进入产物处理；无推流超时结束时变为 failed，且不生成回放产物。

<a id="适用范围"></a>

<a id="ho-dir-en-scope-title"></a>

## 适用范围

结束 Directing Travel。正常结束时状态变为 `completed` 并进入产物处理；无推流超时结束时变为 `failed`，且不生成回放产物。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 必须尚未进入终态，并处于服务端可结束的状态。可通过[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

<a id="http调用"></a>

<a id="ho-dir-en-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-en-req-title"></a><h4>请求参数</h4></td><td rowspan="7"><a id="sec-tabs-2"></a><section><a id="正常结束"></a><section><a id="正常结束-h4"></a><h4>正常结束</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedTravelId&quot;: &quot;{encryptedTravelId}&quot;,
    &quot;userAgent&quot;: &quot;your-client/1.2.0&quot;
}'
</code></pre></section><a id="无推流超时结束"></a><section><a id="无推流超时结束-h4"></a><h4>无推流超时结束</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;encryptedTravelId&quot;: &quot;{encryptedTravelId}&quot;,
    &quot;failCode&quot;: &quot;TRAVEL_NO_STREAM_AUTO_END&quot;,
    &quot;userAgent&quot;: &quot;your-client/1.2.0&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-dir-en-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>要结束的 Directing 加密 Travel ID。由<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">客户端进入房间</a>接口返回。</p></td></tr><tr><td><p><strong>failCode</strong> <code>string</code> <strong>（可选）</strong></p><p>失败结束原因。省略时按正常结束处理。当前仅支持：</p><ul><li><code>TRAVEL_NO_STREAM_AUTO_END</code>：用于<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">进入房间</a>后超过 <code>noStreamAutoEndTimeoutSec</code> 仍未收到推流的场景，该结束方式不生成回放产物</li></ul><p>传入未支持的值返回 <code>400000</code>。</p></td></tr><tr><td><p><strong>userAgent</strong> <code>string</code> <strong>（可选）</strong></p><p>SDK 或客户端版本标识。非空字符串，优先于 HTTP <code>User-Agent</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-en-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="正常结束-2"></a><section><a id="正常结束-2-h4"></a><h4>正常结束</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;status&quot;: &quot;completed&quot;,
        &quot;endedAt&quot;: &quot;2026-06-04T00:03:00Z&quot;,
        &quot;durationSec&quot;: 180
    }
}
</code></pre></section><a id="无推流超时结束-2"></a><section><a id="无推流超时结束-2-h4"></a><h4>无推流超时结束</h4><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;status&quot;: &quot;failed&quot;,
        &quot;errorCode&quot;: &quot;TRAVEL_NO_STREAM_AUTO_END&quot;,
        &quot;errorMessage&quot;: &quot;Something went wrong.&quot;,
        &quot;endedAt&quot;: &quot;2026-06-04T00:03:00Z&quot;,
        &quot;durationSec&quot;: null
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>已结束的加密 Travel ID。</p><p><strong>status</strong> <code>string</code></p><p>结束状态：<code>completed</code>（正常结束）/ <code>failed</code>（带受支持 <code>failCode</code> 时的失败结束）。</p><p><strong>errorCode</strong> <code>string</code></p><p>失败原因代码；正常结束时为 <code>null</code>。</p><p><strong>errorMessage</strong> <code>string</code></p><p>失败说明；正常结束时为 <code>null</code>。</p><p><strong>endedAt</strong> <code>string</code></p><p>结束时间，ISO 8601 格式。</p><p><strong>durationSec</strong> <code>integer</code></p><p>有效视频时长秒数；无推流失败结束或时长尚不可解析时为 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-en-notes-title"></a>

## 前置状态与调用注意事项

-   客户端应在进房后轮询[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)。如果在 `noStreamAutoEndTimeoutSec` 内 `rtcStatus` 未进入推流态，使用 `TRAVEL_NO_STREAM_AUTO_END` 结束。
-   传入 `TRAVEL_NO_STREAM_AUTO_END` 后 Travel 为 `failed`，不能查询到回放产物。
-   正常结束后，`durationSec` 优先使用最终视频文件时长；最终视频尚不可用时，使用当前最新可用生成结果的 `durationMs`。两者均不可用时为 `null`。
-   正常结束进入 `completed` 后，产物合成仍可能进行中；按[查询Travel产物](happyoyster-directing-query-travel-artifacts-api-2da27b6ffc227186.md)的返回状态决定是否继续轮询。

<a id="错误码"></a>

<a id="ho-dir-en-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-en-next-title"></a>

## 下一步

Travel 进入 `completed` 后：

-   [查询Travel产物](happyoyster-directing-query-travel-artifacts-api-2da27b6ffc227186.md)：轮询获取录制原片和合成变体。
-   [查询Travel列表](happyoyster-directing-query-travel-list-api-refe-d243ea07e641f43d.md)：查看历史 Travel。
