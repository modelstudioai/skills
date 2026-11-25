# HappyOyster-Acting-客户端进入房间 API参考

客户端使用 ticket 创建实际 Travel，并获取 RTC 入会配置、Acting 能力版本和播放器画幅。调用成功即创建 Travel。

<a id="适用范围"></a>

<a id="ho-act-et-scope-title"></a>

## 适用范围

客户端使用 `ticket` 创建实际 Travel，并获取 RTC 入会配置、Acting 能力版本和播放器画幅。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，使用 `ticket` 完成进房校验。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：`ticket` 由[获取体验凭证](happyoyster-acting-get-travel-credential-api-ref-dfc7dc5832959ca8.md)接口换取，未过期且未使用，对应 World 状态为 `ready`。
-   **调用方**：您的客户端调用。

<a id="http调用"></a>

<a id="ho-act-et-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-act-et-req-title"></a><h4>请求参数</h4></td><td rowspan="6"><a id="sec-tabs-2"></a><section><a id="客户端进入房间"></a><section><a id="客户端进入房间-h4"></a><h4>客户端进入房间</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/enter-travel' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;ticket&quot;: &quot;{ticket}&quot;
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-act-et-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>ticket</strong> <code>string</code> <strong>（必选）</strong></p><p>未过期且未使用的一次性凭证。由<a href="happyoyster-acting-get-travel-credential-api-ref-dfc7dc5832959ca8.md">获取体验凭证</a>接口换取。同一 <code>ticket</code> 再次使用返回 <code>401011</code>。</p></td></tr></tbody></table>

> **说明**
>
> Acting 进房不消费 `maxExperienceTimeSec`，请勿传入。若仍传入非法档位，会在模型分流前返回 `400000`。

<table><tbody><tr><td><a id="ho-act-et-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="进房成功"></a><section><a id="进房成功-h4"></a><h4>进房成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;mode&quot;: 3,
        &quot;creationModel&quot;: &quot;simple&quot;,
        &quot;playUrl&quot;: null,
        &quot;firstFrame&quot;: &quot;https://cdn.happyoyster.com/frames/acting_world_xyz789.jpg&quot;,
        &quot;rtcConfig&quot;: {
            &quot;channelId&quot;: &quot;stream_abc123&quot;,
            &quot;appId&quot;: &quot;18bca2e3218c46aebf8ff3a32fb12311&quot;,
            &quot;token&quot;: &quot;007eJxTYOh...&quot;,
            &quot;userId&quot;: &quot;user_1&quot;
        },
        &quot;version&quot;: &quot;actingV2&quot;,
        &quot;aspectRatio&quot;: &quot;9:16&quot;,
        &quot;noStreamAutoEndTimeoutSec&quot;: 30,
        &quot;maxExperienceTimeSec&quot;: null
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>新创建的加密 Travel ID。后续<a href="happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md">查询Travel状态</a>、暂停、恢复、结束、产物查询均使用此值。</p><p><strong>encryptedWorldId</strong> <code>string</code></p><p>当前 Travel 对应的加密 World ID。</p><p><strong>mode</strong> <code>integer</code></p><p>Acting 恒为 <code>3</code>。</p><p><strong>creationModel</strong> <code>string</code></p><p>Acting 恒为 <code>simple</code>。</p><p><strong>playUrl</strong> <code>null</code></p><p>暂不可用，固定为 <code>null</code>。</p><p><strong>firstFrame</strong> <code>string</code></p><p>World 首帧 URL。</p><p><strong>rtcConfig</strong> <code>object</code></p><p>RTC 入会配置；没有可用推流频道时为 <code>null</code>，客户端不能据此开始播放。</p><ul><li><code>channelId</code>：RTC 频道 ID</li><li><code>appId</code>：平台分配的 RTC 应用 ID</li><li><code>token</code>：RTC 入会 Token</li><li><code>userId</code>：RTC 入会用户 ID，固定为 <code>user_1</code></li></ul><p><strong>version</strong> <code>string</code></p><p>Acting 进房版本，固定为 <code>actingV2</code>。须按此版本调用控制接口。</p><p><strong>aspectRatio</strong> <code>string</code></p><p>画幅。客户端须在拉流前据此设置播放器方向：</p><ul><li><code>9:16</code>（竖屏）</li><li><code>16:9</code>（横屏）</li></ul><p><strong>noStreamAutoEndTimeoutSec</strong> <code>integer</code></p><p>无推流自动结束超时秒数，默认 30，以实际响应为准。进房后若在此时间内 <code>rtcStatus</code> 未进入推流态，应调用<a href="happyoyster-acting-end-travel-api-reference-07665d664cc3dbc3.md">结束Travel</a>并传入 <code>failCode=TRAVEL_NO_STREAM_AUTO_END</code>。</p><p><strong>maxExperienceTimeSec</strong> <code>null</code></p><p>Acting 不使用最大体验时长，固定返回 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-act-et-notes-title"></a>

## 前置状态与调用注意事项

-   `ticket` 对应的 World 必须为 `ready`，且 ticket 未过期、未使用。
-   调用成功即创建 Travel；同一 `ticket` 再次使用返回 `401011`。
-   Acting 功能或规格未开通时返回 `403007`，且不会创建 Travel。
-   `version` 必须按 `actingV2` 处理；不要按其它能力版本调用控制接口。
-   客户端应在建立拉流或渲染容器前读取 `aspectRatio`：`9:16` 使用竖屏容器，`16:9` 使用横屏容器。
-   不要传 `maxExperienceTimeSec`。Acting 不按该字段自动结束，客户端不能据此做倒计时。
-   `rtcConfig=null` 表示当前没有可用推流频道，客户端不能据此开始播放。

<a id="错误码"></a>

<a id="ho-act-et-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-act-et-next-title"></a>

## 下一步

进房成功后：

-   [查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)：每 2–5 秒轮询，Travel 为 `running` 或 `paused` 时可发送指令。
-   [发送文本过程指令](happyoyster-acting-instruct-travel-api-reference-5c29e8efed3870dd.md)：驱动后续角色表演。
-   [暂停Travel](happyoyster-acting-pause-travel-api-reference-65ff563386f561f7.md) / [恢复Travel](happyoyster-acting-resume-travel-api-reference-e2cfa0a73db72db0.md)：按需控制运行节奏。
-   [结束Travel](happyoyster-acting-end-travel-api-reference-07665d664cc3dbc3.md)：结束时进入 `completed`，开始处理产物。
