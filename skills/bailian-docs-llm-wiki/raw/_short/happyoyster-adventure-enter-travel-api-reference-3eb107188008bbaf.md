# HappyOyster-Adventure-客户端进入房间 API参考

客户端使用 ticket 创建实际 Travel，并获取 RTC 入会配置和 Adventure 能力版本。maxExperienceTimeSec 仅在 Adventure 模型中生效。

<a id="适用范围"></a>

<a id="ho-adv-et-scope-title"></a>

## 适用范围

客户端使用 `ticket` 创建实际 Travel，并获取 RTC 入会配置。`maxExperienceTimeSec` 仅在 Adventure 模型中生效。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，使用 `ticket` 完成进房校验。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：`ticket` 由[获取体验凭证](happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md)接口换取，未过期且未使用，对应 World 状态为 `ready`。
-   **调用方**：您的客户端调用。

<a id="http调用"></a>

<a id="ho-adv-et-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-adv-et-req-title"></a><h4>请求参数</h4></td><td rowspan="6"><a id="sec-tabs-2"></a><section><a id="客户端进入房间"></a><section><a id="客户端进入房间-h4"></a><h4>客户端进入房间</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;ticket&quot;: &quot;{ticket}&quot;,
    &quot;maxExperienceTimeSec&quot;: 90
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-adv-et-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>ticket</strong> <code>string</code> <strong>（必选）</strong></p><p>未过期且未使用的一次性凭证。由<a href="happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md">获取体验凭证</a>接口换取。同一 <code>ticket</code> 再次使用返回 <code>401011</code>。</p></td></tr><tr><td><p><strong>maxExperienceTimeSec</strong> <code>integer</code> <strong>（可选）</strong></p><p>最大体验时长，单位秒，必须是 JSON 整数。默认 <code>60</code>。可选值：</p><ul><li><code>60</code></li><li><code>90</code></li><li><code>120</code></li></ul><p>不接受字符串或其它数值（如 <code>&quot;60&quot;</code> 不是合法值）；非法档位返回 <code>400000</code>。服务端在达到该时长后自动结束 Travel。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-adv-et-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="进房成功"></a><section><a id="进房成功-h4"></a><h4>进房成功</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;mode&quot;: 1,
        &quot;creationModel&quot;: &quot;simple&quot;,
        &quot;playUrl&quot;: null,
        &quot;firstFrame&quot;: &quot;https://cdn.happyoyster.com/frames/world_xyz789.jpg&quot;,
        &quot;rtcConfig&quot;: {
            &quot;channelId&quot;: &quot;stream_abc123&quot;,
            &quot;appId&quot;: &quot;18bca2e3218c46aebf8ff3a32fb12311&quot;,
            &quot;token&quot;: &quot;007eJxTYOh...&quot;,
            &quot;userId&quot;: &quot;user_1&quot;
        },
        &quot;version&quot;: &quot;wanderV2&quot;,
        &quot;aspectRatio&quot;: null,
        &quot;noStreamAutoEndTimeoutSec&quot;: 30,
        &quot;maxExperienceTimeSec&quot;: 90
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>新创建的加密 Travel ID。后续<a href="happyoyster-adventure-query-travel-status-api-re-c8c769da81dc5895.md">查询Travel状态</a>、结束、产物查询均使用此值。</p><p><strong>encryptedWorldId</strong> <code>string</code></p><p>当前 Travel 对应的加密 World ID。</p><p><strong>mode</strong> <code>integer</code></p><p>Adventure 恒为 <code>1</code>。</p><p><strong>creationModel</strong> <code>string</code></p><p>Adventure 恒为 <code>simple</code>。</p><p><strong>playUrl</strong> <code>null</code></p><p>暂不可用，固定为 <code>null</code>。</p><p><strong>firstFrame</strong> <code>string</code></p><p>World 首帧 URL。</p><p><strong>rtcConfig</strong> <code>object</code></p><p>RTC 入会配置；没有可用推流频道时为 <code>null</code>，客户端不能据此开始播放。</p><ul><li><code>channelId</code>：RTC 频道 ID</li><li><code>appId</code>：平台分配的 RTC 应用 ID</li><li><code>token</code>：RTC 入会 Token</li><li><code>userId</code>：RTC 入会用户 ID，固定为 <code>user_1</code></li></ul><p><strong>version</strong> <code>string</code></p><p>Adventure 进房版本，固定为 <code>wanderV2</code>。须按此版本通过 SDK <code>sendCommand</code> 发送控制数据。</p><p><strong>aspectRatio</strong> <code>null</code></p><p>Adventure 固定为 <code>null</code>；播放器画幅不从本字段读取，跟随首帧图比例。</p><p><strong>noStreamAutoEndTimeoutSec</strong> <code>integer</code></p><p>无推流自动结束超时秒数，默认 30，以实际响应为准。进房后若在此时间内 <code>rtcStatus</code> 未进入推流态，应调用<a href="happyoyster-adventure-end-travel-api-reference-f46d5ab187c27653.md">结束Travel</a>并传入 <code>failCode=TRAVEL_NO_STREAM_AUTO_END</code>。</p><p><strong>maxExperienceTimeSec</strong> <code>integer</code></p><p>服务端实际采用的体验时长，只会是 <code>60</code> / <code>90</code> / <code>120</code>。达到该时长后服务端自动结束 Travel。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-adv-et-notes-title"></a>

## 前置状态与调用注意事项

-   `ticket` 对应的 World 必须为 `ready`，且 ticket 未过期、未使用。
-   调用成功即创建 Travel；同一 `ticket` 再次使用返回 `401011`。
-   `version` 必须按 `wanderV2` 处理，不能按其它模型的交互协议发送控制数据。
-   服务端在达到 `maxExperienceTimeSec` 后结束体验，客户端应处理随后到达的终态。
-   Adventure 的方向、视角和动作控制不是服务端 HTTP Open API，客户端必须使用对应平台 SDK 的 `sendCommand`，由 SDK 经 RTC DataChannel 发送。
-   `rtcConfig=null` 表示当前没有可用推流频道，客户端不能据此开始播放。

<a id="错误码"></a>

<a id="ho-adv-et-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-adv-et-next-title"></a>

## 下一步

进房成功后：

-   [查询Travel状态](happyoyster-adventure-query-travel-status-api-re-c8c769da81dc5895.md)：每 2–5 秒轮询，读取可用动作池。
-   Travel 为 `running` 后，客户端通过 SDK `sendCommand` 发送方向、视角和动作控制。
-   [结束Travel](happyoyster-adventure-end-travel-api-reference-f46d5ab187c27653.md)：结束会话并处理产物。
