# HappyOyster-Acting-查询Travel产物 API参考

查询已完成 Acting Travel 的录制原片和三个合成变体。对外交付推荐使用 withInstructionAndWatermark。

<a id="适用范围"></a>

<a id="ho-act-qta-scope-title"></a>

## 适用范围

查询已完成 Acting Travel 的录制原片和三个合成变体。`withInstruction` 是用户过程指令的叠加版本；对外交付推荐使用 `withInstructionAndWatermark`。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **前置条件**：Travel 状态为 `completed`。原片 URL 可用是返回产物响应的前提。可通过[查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)接口确认。
    
-   **调用方**：您的服务端调用。
    

<a id="http调用"></a>

<a id="ho-act-qta-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-act-qta-req-title"></a><h4>请求参数</h4></td><td rowspan="4"><a id="sec-tabs-2"></a><section><a id="查询travel产物"></a><section><a id="查询travel产物-h4"></a><h4>查询Travel产物</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/artifacts?encryptedTravelId={encryptedTravelId}' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-act-qta-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>状态为 <code>completed</code> 的 Acting 加密 Travel ID。由<a href="happyoyster-acting-enter-travel-api-reference-56ea4df0a872fdb7.md">客户端进入房间</a>接口返回。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-act-qta-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="四路产物全部就绪"></a><section><a id="四路产物全部就绪-h4"></a><h4>四路产物全部就绪</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;composeStatus&quot;: &quot;ready&quot;,
        &quot;video&quot;: {
            &quot;original&quot;: {
                &quot;url&quot;: &quot;https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_raw.mp4?v=2&quot;,
                &quot;status&quot;: &quot;ready&quot;,
                &quot;resolution&quot;: &quot;720p&quot;,
                &quot;durationSec&quot;: 180
            },
            &quot;withWatermark&quot;: {
                &quot;url&quot;: &quot;https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_wm.mp4?v=2&quot;,
                &quot;status&quot;: &quot;ready&quot;,
                &quot;resolution&quot;: null,
                &quot;durationSec&quot;: 180
            },
            &quot;withInstruction&quot;: {
                &quot;url&quot;: &quot;https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_overlay.mp4?v=2&quot;,
                &quot;status&quot;: &quot;ready&quot;,
                &quot;resolution&quot;: null,
                &quot;durationSec&quot;: 180
            },
            &quot;withInstructionAndWatermark&quot;: {
                &quot;url&quot;: &quot;https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_all.mp4?v=2&quot;,
                &quot;status&quot;: &quot;ready&quot;,
                &quot;resolution&quot;: null,
                &quot;durationSec&quot;: 180
            }
        }
    }
}
</code></pre></section><a id="合成仍在处理"></a><section><a id="合成仍在处理-h4"></a><h4>合成仍在处理</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedTravelId&quot;: &quot;trvl_a1b2****&quot;,
        &quot;composeStatus&quot;: &quot;processing&quot;,
        &quot;video&quot;: {
            &quot;original&quot;: {
                &quot;url&quot;: &quot;https://cdn.happyoyster.com/exports/trvl_a1b2c3d4e5f6_raw.mp4?v=2&quot;,
                &quot;status&quot;: &quot;ready&quot;,
                &quot;resolution&quot;: &quot;720p&quot;,
                &quot;durationSec&quot;: 180
            },
            &quot;withWatermark&quot;: {
                &quot;url&quot;: null,
                &quot;status&quot;: &quot;processing&quot;,
                &quot;resolution&quot;: null,
                &quot;durationSec&quot;: null
            },
            &quot;withInstruction&quot;: {
                &quot;url&quot;: null,
                &quot;status&quot;: &quot;processing&quot;,
                &quot;resolution&quot;: null,
                &quot;durationSec&quot;: null
            },
            &quot;withInstructionAndWatermark&quot;: {
                &quot;url&quot;: null,
                &quot;status&quot;: &quot;processing&quot;,
                &quot;resolution&quot;: null,
                &quot;durationSec&quot;: null
            }
        }
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密 Travel ID。</p><p><strong>composeStatus</strong> <code>string</code></p><p>三个合成变体的聚合状态：</p><ul><li><code>ready</code>：<code>withWatermark</code>、<code>withInstruction</code>、<code>withInstructionAndWatermark</code> 均为 <code>ready</code></li><li><code>partial</code>：至少一个合成变体为 <code>ready</code>，但未全部就绪</li><li><code>processing</code>：三个合成变体均不是 <code>ready</code></li></ul><p>只聚合三个合成变体，不包含 <code>original</code>。</p><p><strong>video</strong> <code>object</code></p><p>主线视频的四种固定变体。每项含 <code>url</code>、<code>status</code>、<code>resolution</code>、<code>durationSec</code>。</p><ul><li><code>original</code>：录制原片，优先返回可用的 720p 表示</li><li><code>withWatermark</code>：仅水印合成版</li><li><code>withInstruction</code>：用户过程指令叠加的合成版</li><li><code>withInstructionAndWatermark</code>：用户过程指令叠加 + 水印合成版，推荐用于对外交付</li></ul><p><strong>video.*.url</strong> <code>string</code></p><p>下载 URL；<code>processing</code> 或 <code>unavailable</code> 时为 <code>null</code>。</p><p><strong>video.*.status</strong> <code>string</code></p><p>单项状态：</p><ul><li><code>ready</code>：已就绪，<code>url</code> 可访问</li><li><code>processing</code>：仍在合成，<code>url=null</code></li><li><code>unavailable</code>：合成失败或 URL 暂不可用，<code>url=null</code></li></ul><p><strong>video.*.resolution</strong> <code>string</code></p><p><code>original</code> 命中 720p 时为 <code>&quot;720p&quot;</code>；其它情况可能为 <code>null</code>。</p><p><strong>video.*.durationSec</strong> <code>integer</code></p><p>统一解析得到的视频时长秒数；可解析时所有 <code>ready</code> 变体均填写该值，<code>processing</code> / <code>unavailable</code> 或时长暂不可解析时可为 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-act-qta-notes-title"></a>

## 前置状态与调用注意事项

-   客户端可在 `composeStatus != ready` 时按受控间隔轮询。
-   `video.withInstruction` 是过程指令叠加版，不是无指令原片。
-   对外交付推荐读取 `video.withInstructionAndWatermark`；如业务只需要原片，可继续读取 `video.original.url`。
-   四个视频变体共用同一时长解析结果，因此同一次响应中已就绪且时长可解析的变体会返回一致的 `durationSec`。
-   使用 `TRAVEL_NO_STREAM_AUTO_END` 结束的 Travel 为 `failed`，不会生成可查询产物。
-   收到 `404000` 时不要一律展示为“尚未完成”：请先通过[查询Travel状态](happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)或[查询Travel列表](happyoyster-acting-query-travel-list-api-referen-643c3b55678ff459.md)读取 `status` 与 `errorCode`，`failed` 的 Travel 应展示失败原因。

<a id="ho-act-qta-404000-h5"></a>

##### 404000 场景

| 场景 | 接口行为 |
| --- | --- |
| Travel 仍在进行中（`init` / `pending` / `running` / `paused`） | 返回业务码 `404000`，`message` 为 `Video is still being generated, please try again once the process is complete` |
| Travel 已 `failed` | 返回业务码 `404000`，`message` 为 `Experience failed and no video was produced (errorCode=<errorCode>): <errorMessage>`；失败为终态，不会再有成片 |
| Travel 不存在、不归属或不是 Acting | 返回业务码 `404000` |
| 原片 URL 不可用 | 返回业务码 `404000`；原片是整个接口的硬门槛 |
| 原片已就绪、合成仍在处理 | HTTP 200；对应合成项 `status=processing`、`url=null` |
| 合成失败或 URL 暂不可用 | HTTP 200；对应合成项 `status=unavailable`、`url=null` |

<a id="错误码"></a>

<a id="ho-act-qta-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-act-qta-next-title"></a>

## 下一步

-   [查询Travel列表](happyoyster-acting-query-travel-list-api-referen-643c3b55678ff459.md)：查看其它历史 Travel。
-   [结束Travel](happyoyster-acting-end-travel-api-reference-07665d664cc3dbc3.md)：结束新的 Travel 后再来查询产物。
