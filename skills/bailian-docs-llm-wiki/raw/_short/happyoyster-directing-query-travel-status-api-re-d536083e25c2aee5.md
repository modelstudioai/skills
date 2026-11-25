# HappyOyster-Directing-查询Travel状态 API参考

查询 Directing Travel 生命周期、服务端推流状态、已执行文本指令和章节信息，也可同时上报客户端拉流或播放心跳。

<a id="适用范围"></a>

<a id="ho-dir-qts-scope-title"></a>

## 适用范围

查询 Directing Travel 生命周期、服务端推流状态、已执行文本指令和章节信息，也可同时上报客户端拉流或播放心跳。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：使用[客户端进入房间](happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md)接口返回的 `encryptedTravelId` 查询。
-   **调用方**：您的服务端或客户端均可调用。建议每 2–5 秒轮询。

<a id="http调用"></a>

<a id="ho-dir-qts-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-qts-req-title"></a><h4>请求参数</h4></td><td rowspan="6"><a id="sec-tabs-2"></a><section><a id="查询travel状态"></a><section><a id="查询travel状态-h4"></a><h4>查询Travel状态</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/status?encryptedTravelId={encryptedTravelId}&amp;clientStreamStatus=PLAYING&amp;clientStreamStatusTimeMs=1788940800000' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。</p><ul><li><strong>主 API Key</strong>：以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。</li><li><strong>临时 API Key</strong>：以 <code>st-</code> 开头，如 <code>st-xxx</code>。</li></ul></td></tr><tr><td><a id="ho-dir-qts-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>Directing 加密 Travel ID。由<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">客户端进入房间</a>接口返回。</p></td></tr><tr><td><p><strong>clientStreamStatus</strong> <code>string</code> <strong>（可选）</strong></p><p>客户端 RTC 拉流或播放状态，大小写不敏感。无法识别的值会被忽略。可选值：</p><ul><li><code>DISCONNECTED</code>：未连接或已离开频道</li><li><code>CONNECTING</code>：正在连接 RTC 频道</li><li><code>CONNECTED</code>：已入会，尚未开始播放或首帧未到达</li><li><code>PLAYING</code>：已收到远端流并正在渲染</li><li><code>BUFFERING</code>：缓冲中</li><li><code>PAUSED</code>：客户端暂停播放，不等同于服务端 <code>pause</code></li><li><code>RECONNECTING</code>：重连中</li></ul></td></tr><tr><td><p><strong>clientStreamStatusTimeMs</strong> <code>long</code> <strong>（可选）</strong></p><p>客户端状态变更的毫秒时间戳。与 <code>clientStreamStatus</code> 配套使用。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-qts-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="travel运行中"></a><section><a id="travel运行中-h4"></a><h4>Travel运行中</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;status&quot;: &quot;running&quot;,
        &quot;rtcStatus&quot;: &quot;PUSHING&quot;,
        &quot;updateTime&quot;: &quot;2026-06-04T00:02:00Z&quot;,
        &quot;userInstructions&quot;: [
            {
                &quot;instruction&quot;: &quot;突然出现一只巨大的机器恐龙&quot;,
                &quot;relativeStartTimeMs&quot;: 12000,
                &quot;relativeEndTimeMs&quot;: 16000,
                &quot;startTime&quot;: 12.0,
                &quot;endTime&quot;: 16.0,
                &quot;status&quot;: &quot;executed&quot;
            }
        ],
        &quot;chapters&quot;: [
            {
                &quot;chapterId&quot;: 1,
                &quot;title&quot;: &quot;第一章&quot;,
                &quot;brief&quot;: &quot;侦探进入赛博朋克城市&quot;,
                &quot;actRange&quot;: [0, 10],
                &quot;startTime&quot;: 4,
                &quot;endTime&quot;: 20,
                &quot;chapterImage&quot;: &quot;https://cdn.happyoyster.com/chapters/ch1.jpg&quot;
            }
        ],
        &quot;characterActions&quot;: [],
        &quot;environmentActions&quot;: []
    }
}
</code></pre></section><a id="travel失败"></a><section><a id="travel失败-h4"></a><h4>Travel失败</h4><p><code>errorCode</code> 取值见<a href="../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md#ho-ec-travel-errorcode-title">错误码</a>。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;status&quot;: &quot;failed&quot;,
        &quot;rtcStatus&quot;: null,
        &quot;updateTime&quot;: null,
        &quot;userInstructions&quot;: null,
        &quot;chapters&quot;: null,
        &quot;characterActions&quot;: null,
        &quot;environmentActions&quot;: null,
        &quot;errorCode&quot;: &quot;TRAVEL_SESSION_INIT_FAILED&quot;,
        &quot;errorMessage&quot;: &quot;Failed to allocate inference resources.&quot;
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密 Travel ID。</p><p><strong>status</strong> <code>string</code></p><p>Travel 生命周期状态：</p><ul><li><code>init</code>：正在初始化会话资源</li><li><code>pending</code>：排队或等待服务资源</li><li><code>running</code>：正在运行，可按创建子模式调用支持的控制接口</li><li><code>paused</code>：已完成服务端暂停；可恢复或回溯</li><li><code>failed</code>：Travel 失败；原因见 <code>errorCode</code> / <code>errorMessage</code></li><li><code>completed</code>：Travel 已结束，可查询产物</li></ul><p><strong>rtcStatus</strong> <code>string</code></p><p>服务端 RTC 推流状态；与客户端上报的 <code>clientStreamStatus</code> 不同。</p><p><strong>updateTime</strong> <code>string</code></p><p>最近更新时间，ISO 8601 格式。</p><p><strong>userInstructions</strong> <code>array</code></p><p>文本指令列表；无数据时为 <code>null</code>。每项含 <code>instruction</code>、<code>relativeStartTimeMs</code> / <code>relativeEndTimeMs</code>（相对毫秒）、<code>startTime</code> / <code>endTime</code>（时间轴秒数）、<code>status</code>。</p><p><strong>chapters</strong> <code>array</code></p><p>章节列表；尚未触发章节检测时为 <code>null</code>。每项含 <code>chapterId</code>、<code>title</code>、<code>brief</code>、<code>actRange</code>、<code>startTime</code>、<code>endTime</code>、<code>chapterImage</code>。</p><p><strong>characterActions</strong> <code>array&lt;string&gt; | null</code></p><p>Directing 不支持 SDK 动作控制，固定返回空数组；<code>failed</code> 时为 <code>null</code>。</p><p><strong>environmentActions</strong> <code>array&lt;string&gt; | null</code></p><p>Directing 不支持 SDK 环境动作控制，固定返回空数组；<code>failed</code> 时为 <code>null</code>。</p><p><strong>errorCode</strong> <code>string</code></p><p>仅 <code>status=failed</code> 时返回；结构化失败原因代码，取值见<a href="../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md#ho-ec-travel-errorcode-title">错误码</a>。</p><p><strong>errorMessage</strong> <code>string</code></p><p>与 <code>errorCode</code> 同时返回；英文失败说明。请按 <code>errorCode</code> 分支处理，不要匹配 <code>errorMessage</code> 文案。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-qts-notes-title"></a>

## 前置状态与调用注意事项

-   建议每 2–5 秒轮询。
-   `running` 状态可按 `creationModel` 调用支持的控制接口：普通模式可 `instruct`、`pause`、`resume`、`rewind`、`end`；剧本模式可 `update-script`、`pause`、`resume`、`rewind`、`end`。
-   本接口不返回 `mode`、`aspectRatio`、`playUrl`、`bgmUrl` 或 `sessionId`；播流配置以[进入房间](happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md)响应为准。
-   `clientStreamStatus` 是客户端播放侧心跳，`rtcStatus` 是服务端推流侧状态，两者不可互相替代。
-   `failed` 是终态，不会再产生成片；请按 `errorCode` 展示失败原因，不要展示为“尚未完成”。

<a id="错误码"></a>

<a id="ho-dir-qts-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-qts-next-title"></a>

## 下一步

Travel 为 `running` 或 `paused` 时：

-   普通模式：[发送过程指令](happyoyster-directing-instruct-travel-api-refere-2cd5aa6eabceb2c4.md)。
-   剧本模式：[剧本全量更新](happyoyster-directing-update-script-api-referenc-559783f11176cb54.md)。
-   通用：[暂停](happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md) / [恢复](happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md) / [回溯](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md) / [结束](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)。
