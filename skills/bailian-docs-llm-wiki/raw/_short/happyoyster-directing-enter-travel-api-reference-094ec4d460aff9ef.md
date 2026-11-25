# HappyOyster-Directing-客户端进入房间 API参考

客户端使用 ticket 创建实际 Travel，并获取 RTC 入会配置和 Directing 能力版本。creationModel 决定 Travel 可调用的控制接口。

<a id="适用范围"></a>

<a id="ho-dir-et-scope-title"></a>

## 适用范围

客户端使用 `ticket` 创建实际 Travel，并获取 RTC 入会配置。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，使用 `ticket` 完成进房校验。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：`ticket` 由[获取体验凭证](happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md)接口换取，未过期且未使用，对应 World 状态为 `ready`。
-   **调用方**：您的客户端调用。

<a id="http调用"></a>

<a id="ho-dir-et-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-et-req-title"></a><h4>请求参数</h4></td><td rowspan="5"><a id="sec-tabs-2"></a><section><a id="客户端进入房间"></a><section><a id="客户端进入房间-h4"></a><h4>客户端进入房间</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/enter-travel' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;ticket&quot;: &quot;{ticket}&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-dir-et-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>ticket</strong> <code>string</code> <strong>（必选）</strong></p><p>未过期且未使用的一次性凭证。由<a href="happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md">获取体验凭证</a>接口换取。同一 <code>ticket</code> 再次使用返回 <code>401011</code>。</p><div><div><p><strong>说明</strong>Directing 进房不消费</p><code>maxExperienceTimeSec</code>，请勿传入。该字段仅 Adventure 生效；若仍传入非法档位，会在模型分流前返回 <code>400000</code>。成功响应仍为 <code>null</code>。</div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-et-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;mode&quot;: 2,
        &quot;creationModel&quot;: &quot;simple&quot;,
        &quot;playUrl&quot;: null,
        &quot;firstFrame&quot;: &quot;https://cdn.happyoyster.com/frames/world_xyz789.jpg&quot;,
        &quot;rtcConfig&quot;: {
            &quot;channelId&quot;: &quot;stream_abc123&quot;,
            &quot;appId&quot;: &quot;18bca2e3218c46aebf8ff3a32fb12311&quot;,
            &quot;token&quot;: &quot;007eJxTYOh...&quot;,
            &quot;userId&quot;: &quot;user_1&quot;
        },
        &quot;version&quot;: &quot;storyV2&quot;,
        &quot;aspectRatio&quot;: null,
        &quot;noStreamAutoEndTimeoutSec&quot;: 30,
        &quot;maxExperienceTimeSec&quot;: null
    }
}
</code></pre></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>新创建的加密 Travel ID。后续<a href="happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md">查询Travel状态</a>、回溯、暂停、恢复、结束、产物查询均使用此值。</p><p><strong>encryptedWorldId</strong> <code>string</code></p><p>当前 Travel 对应的加密 World ID。</p><p><strong>mode</strong> <code>integer</code></p><p>Directing 恒为 <code>2</code>。</p><p><strong>creationModel</strong> <code>string</code></p><p><code>simple</code> 或 <code>scriptlist</code>；决定 Travel 可调用的控制接口：</p><ul><li><code>simple</code>：<code>instruct</code>、<code>pause</code>、<code>resume</code>、<code>rewind</code>、<code>end</code></li><li><code>scriptlist</code>：<code>update-script</code>、<code>pause</code>、<code>resume</code>、<code>rewind</code>、<code>end</code>（不支持 <code>instruct</code>）</li></ul><p><strong>playUrl</strong> <code>null</code></p><p>暂不可用，固定为 <code>null</code>。</p><p><strong>firstFrame</strong> <code>string</code></p><p>World 首帧 URL。</p><p><strong>rtcConfig</strong> <code>object</code></p><p>RTC 入会配置；没有可用推流频道时为 <code>null</code>，客户端不能据此开始播放。</p><ul><li><code>channelId</code>：RTC 频道 ID</li><li><code>appId</code>：平台分配的 RTC 应用 ID</li><li><code>token</code>：RTC 入会 Token</li><li><code>userId</code>：RTC 入会用户 ID，固定为 <code>user_1</code></li></ul><p><strong>version</strong> <code>string</code></p><p>Directing 进房版本，固定为 <code>storyV2</code>。</p><p><strong>aspectRatio</strong> <code>null</code></p><p>Directing 模型固定为 <code>null</code>。</p><p><strong>noStreamAutoEndTimeoutSec</strong> <code>integer</code></p><p>无推流自动结束超时秒数，默认 30，以实际响应为准。进房后若在此时间内 <code>rtcStatus</code> 未进入推流态，应调用<a href="happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md">结束Travel</a>并传入 <code>failCode=TRAVEL_NO_STREAM_AUTO_END</code>。</p><p><strong>maxExperienceTimeSec</strong> <code>null</code></p><p>Directing 模型固定为 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-et-notes-title"></a>

## 前置状态与调用注意事项

-   `ticket` 对应的 World 必须为 `ready`，且 ticket 未过期、未使用。
-   不要传 `maxExperienceTimeSec`。Directing 不按该字段限制体验时长。
-   调用成功即创建 Travel；同一 `ticket` 再次使用返回 `401011`。
-   `creationModel=scriptlist` 时不要调用 `instruct`，应使用[剧本全量更新](happyoyster-directing-update-script-api-referenc-559783f11176cb54.md)。
-   `rtcConfig=null` 表示当前没有可用推流频道，客户端不能据此开始播放。

<a id="错误码"></a>

<a id="ho-dir-et-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-et-next-title"></a>

## 下一步

进房成功后：

-   [查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)：每 2–5 秒轮询，按 `creationModel` 调用可用的控制接口。
-   普通模式：[发送过程指令](happyoyster-directing-instruct-travel-api-refere-2cd5aa6eabceb2c4.md)。
-   剧本模式：[剧本全量更新](happyoyster-directing-update-script-api-referenc-559783f11176cb54.md)。
-   通用：[暂停](happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md) / [恢复](happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md) / [回溯](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md) / [结束](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)。
