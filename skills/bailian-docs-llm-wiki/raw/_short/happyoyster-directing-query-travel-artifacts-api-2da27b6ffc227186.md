# HappyOyster-Directing-查询Travel产物 API参考

查询已完成 Directing Travel 的录制原片和三个合成变体。原片可用是返回产物响应的前提；对外交付推荐使用 withInstructionAndWatermark。

<a id="适用范围"></a>

<a id="ho-dir-qta-scope-title"></a>

## 适用范围

查询已完成 Directing Travel 的录制原片及三个合成版本。原片可用是返回产物响应的前提；合成版本可以仍在处理中。对外交付推荐使用 `withInstructionAndWatermark`。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **前置条件**：Travel 状态为 `completed`。原片可用是返回产物响应的前提。可通过[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)接口确认。
    
-   **调用方**：您的服务端调用。
    

<a id="http调用"></a>

<a id="ho-dir-qta-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/artifacts`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-dir-qta-req-title"></a><h4>请求参数</h4></td><td rowspan="4"><a id="sec-tabs-2"></a><section><a id="查询travel产物"></a><section><a id="查询travel产物-h4"></a><h4>查询Travel产物</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/artifacts?encryptedTravelId={encryptedTravelId}' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-dir-qta-query-h5"></a><h5>Query 参数</h5></td></tr><tr><td><p><strong>encryptedTravelId</strong> <code>string</code> <strong>（必选）</strong></p><p>状态为 <code>completed</code> 的 Directing 加密 Travel ID。由<a href="happyoyster-directing-enter-travel-api-reference-094ec4d460aff9ef.md">客户端进入房间</a>接口返回。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-qta-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="四路产物全部就绪"></a><section><a id="四路产物全部就绪-h4"></a><h4>四路产物全部就绪</h4><a id="code-block-2"></a><pre class="language-json"><code>{
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
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>encryptedTravelId</strong> <code>string</code></p><p>加密 Travel ID。</p><p><strong>composeStatus</strong> <code>string</code></p><p>三个合成变体的聚合状态：</p><ul><li><code>ready</code>：<code>withWatermark</code>、<code>withInstruction</code>、<code>withInstructionAndWatermark</code> 均为 <code>ready</code></li><li><code>partial</code>：至少一个合成变体为 <code>ready</code>，但尚未全部就绪</li><li><code>processing</code>：三个合成变体均非 <code>ready</code></li></ul><p>只聚合三个合成变体，不包含 <code>original</code>。</p><p><strong>video</strong> <code>object</code></p><p>四类主线视频产物，字段结构固定。每项含 <code>url</code>、<code>status</code>、<code>resolution</code>、<code>durationSec</code>。</p><ul><li><code>original</code>：录制原片，优先选择 720p</li><li><code>withWatermark</code>：仅添加水印的合成版</li><li><code>withInstruction</code>：仅添加用户指令字幕的合成版</li><li><code>withInstructionAndWatermark</code>：用户指令字幕与水印合成版，推荐用于对外交付</li></ul><p><strong>video.*.url</strong> <code>string</code></p><p>视频 URL；<code>status=processing</code> 时为 <code>null</code>。</p><p><strong>video.*.status</strong> <code>string</code></p><p>单项状态：</p><ul><li><code>ready</code>：该视频已就绪，URL 可访问</li><li><code>processing</code>：正在处理；URL 为 <code>null</code></li><li><code>unavailable</code>：合成失败或 URL 暂不可用</li></ul><p><strong>video.*.resolution</strong> <code>string</code></p><p>原片命中 720p 时 <code>video.original.resolution</code> 为 <code>&quot;720p&quot;</code>；其它情况为 <code>null</code>。</p><p><strong>video.*.durationSec</strong> <code>integer</code></p><p>统一解析得到的视频时长秒数；可解析时所有 <code>ready</code> 变体均填写该值，<code>processing</code> / <code>unavailable</code> 或时长暂不可解析时可为 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="前置状态与调用注意事项"></a>

<a id="ho-dir-qta-notes-title"></a>

## 前置状态与调用注意事项

-   需要全部合成版本时，可在 `composeStatus != ready` 时继续轮询。
-   `video.withInstructionAndWatermark` 是推荐的对外交付版本。
-   四个视频变体共用同一时长解析结果，因此同一次响应中已就绪且时长可解析的变体会返回一致的 `durationSec`。
-   不要将 `404000` 一律展示为“尚未完成”：请先通过[查询Travel状态](happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)或[查询Travel列表](happyoyster-directing-query-travel-list-api-refe-d243ea07e641f43d.md)读取 `status` 与 `errorCode`；对 `failed` 的 Travel 展示失败原因。

<a id="ho-dir-qta-404000-h5"></a>

##### 404000 场景

| 场景 | 接口表现 |
| --- | --- |
| Travel 仍在进行中（`init` / `pending` / `running` / `paused`） | 返回业务码 `404000`，`message` = `Video is still being generated, please try again once the process is complete` |
| Travel 处于 `failed` | 返回业务码 `404000`，`message` = `Experience failed and no video was produced (errorCode=<errorCode>): <errorMessage>`；失败是终态，不会再产出视频 |
| Travel 不存在、不归属或不是 Directing | 返回业务码 `404000` |
| 原片 URL 不可用 | 返回业务码 `404000`；原片是整个接口的硬门槛 |
| 原片已就绪、合成仍在处理 | HTTP 200；对应合成条目 `status=processing`、`url=null` |
| 合成失败或 URL 暂不可用 | HTTP 200；对应合成条目 `status=unavailable`、`url=null` |

<a id="错误码"></a>

<a id="ho-dir-qta-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-qta-next-title"></a>

## 下一步

-   [查询Travel列表](happyoyster-directing-query-travel-list-api-refe-d243ea07e641f43d.md)：查看其它历史 Travel。
-   [结束Travel](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)：结束新的 Travel 后再来查询产物。
