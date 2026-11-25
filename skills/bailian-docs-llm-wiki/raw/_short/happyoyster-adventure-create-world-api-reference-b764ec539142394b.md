# HappyOyster-Adventure-创建World API参考

创建一个世界探索 World。使用自然语言 Prompt 和必填首帧图创建 World，接口立即返回加密 World ID，World 在后台异步构建，客户端轮询构建进度直至完成。

<a id="适用范围"></a>

<a id="ho-adv-cw-scope-title"></a>

## 适用范围

创建一个 Adventure World。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **调用模式**：推荐使用异步模式。
    
    -   **异步模式**（默认）：`async=true`，接口立即返回 `encryptedWorldId`，需轮询[查询World构建状态](happyoyster-adventure-query-world-build-status-a-4830e59b84023226.md)获取进度。
    -   **同步模式**：`async=false`，服务端内部轮询（间隔 3s，最长 120s），构建完成后返回；超时则降级为异步，客户端继续轮询。
-   **接口限制**：本接口只能创建 Adventure World，无需传 `mode`（服务端按 `1` 写入，传入非 `1` 返回 `400000`）。`creationModel` 恒为 `simple`，`uploadMode` 固定为 `first_frame`，进房版本固定为 `wanderV2`。
    

<a id="http调用"></a>

<a id="ho-adv-cw-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="ho-adv-cw-req-title"></a><h4>请求参数</h4></td><td rowspan="10"><a id="sec-tabs-2"></a><section><a id="首帧图-异步创建"></a><section><a id="首帧图-异步创建-h4"></a><h4>首帧图（异步创建）</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;async&quot;: true,
    &quot;perspective&quot;: &quot;third_person&quot;,
    &quot;prompt&quot;: &quot;第三人称跟拍：一名身穿黑色防寒服、头戴黑色头盔的骑手骑着黑色雪地摩托驶向远方，履带扬起细雪。前方是积雪覆盖的针叶林，更远处是日照岩壁的陡峭雪山与蓝天白云。冬日晴空，雪地高光强烈，开阔冷冽。&quot;,
    &quot;firstFrameImage&quot;: {
        &quot;url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9fc6.png&quot;
    }
}'
</code></pre></section><a id="首帧图base64-异步创建"></a><section><a id="首帧图base64-异步创建-h4"></a><h4>首帧图base64（异步创建）</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;async&quot;: true,
    &quot;perspective&quot;: &quot;third_person&quot;,
    &quot;prompt&quot;: &quot;第三人称跟拍：一名身穿黑色防寒服、头戴黑色头盔的骑手骑着黑色雪地摩托驶向远方，履带扬起细雪。前方是积雪覆盖的针叶林，更远处是日照岩壁的陡峭雪山与蓝天白云。冬日晴空，雪地高光强烈，开阔冷冽。&quot;,
    &quot;firstFrameImage&quot;: {
        &quot;base64&quot;: &quot;data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...&quot;
    }
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-adv-cw-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>async</strong> <code>boolean</code> （可选）</p><p>是否异步创建。默认 <code>true</code>：</p><ul><li><code>true</code>：立即返回，World 在后台构建，客户端轮询<a href="happyoyster-adventure-query-world-build-status-a-4830e59b84023226.md">查询World构建状态</a>。</li><li><code>false</code>：服务端每 3 秒轮询一次，最长等待 120 秒，构建完成后返回；超时仍返回 <code>generating</code>，客户端随后改为自行轮询。</li></ul></td></tr><tr><td><p><strong>perspective</strong> <code>string</code> <strong>（必选）</strong></p><p>视角。可选值：</p><ul><li><code>first_person</code>：第一人称</li><li><code>third_person</code>：第三人称</li></ul><p>缺少该字段返回 <code>400000</code>。</p></td></tr><tr><td><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>世界主题描述，支持中英文。非空，最长 2000 字符。缺失、空白或超限返回 <code>400000</code>。</p></td></tr><tr><td><p><strong>creationModel</strong> <code>string</code> （可选）</p><p>创建子模式。默认 <code>simple</code>，Adventure 仅支持 <code>simple</code>。</p></td></tr><tr><td><p><strong>uploadMode</strong> <code>string</code> （可选）</p><p>图片上传模式。默认 <code>first_frame</code>，Adventure 仅支持 <code>first_frame</code>。</p></td></tr><tr><td><p><strong>refWorldId</strong> <code>string</code> （可选）</p><p>基于已有 Adventure World 衍生创建。必须是当前主账号名下的 Adventure 加密 World ID；其它模型或其它主账号的 World 返回 <code>403001</code>。</p></td></tr><tr><td><p><strong>firstFrameImage</strong> <code>object</code> <strong>（必选）</strong></p><p>直接复用为 World 首帧的图片引用。<code>url</code> 与 <code>base64</code> 二选一且互斥。图片约束如下：</p><ul><li>格式：JPG / JPEG / PNG / WebP</li><li>大小：单张严格小于 6 MB</li><li>宽高比：必须为横屏，宽 / 高为 1.5–2.0（画面比例跟随该图）</li><li>内容安全：未通过内容安全或版权 / IP 校验返回 <code>403004</code> / <code>403005</code></li></ul><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code> （条件必选）</p><p>首帧图片 URL。与 <code>base64</code> 二选一且互斥。约束：</p><ul><li>必须是带 Host 的合法 <code>http</code> / <code>https</code> URL，并可由服务端访问</li><li>真实格式、大小和首帧宽高比在转存后校验</li><li>异步请求可能先返回 <code>generating</code>，随后 World 因图片校验失败进入 <code>failed</code></li></ul><p><strong>base64</strong> <code>string</code> （条件必选）</p><p>首帧图片 base64。与 <code>url</code> 二选一且互斥。约束：</p><ul><li>推荐使用完整 data URI <code>data:image/&lt;subtype&gt;;base64,&lt;payload&gt;</code></li><li>在创建入口同步校验格式、大小和首帧宽高比</li></ul><p><strong>referenceType</strong> <code>string</code> （可选）</p><p>参考图类型。默认 <code>default</code>，当前按 <code>default</code> 使用。</p></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-adv-cw-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="异步创建"></a><section><a id="异步创建-h4"></a><h4>异步创建</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;status&quot;: &quot;generating&quot;,
        &quot;firstFrame&quot;: null
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>encryptedWorldId</strong> <code>string</code></p><p>服务端生成的加密 World ID。同步和异步模式均返回，后续构建状态轮询、详情查询、换取体验凭证均使用此值。</p><p><strong>status</strong> <code>string</code></p><p>当前创建状态：<code>generating</code>（构建中）或 <code>ready</code>（就绪）；同步构建失败时也可能为 <code>failed</code>。</p><p><strong>firstFrame</strong> <code>string</code></p><p>World 首帧 URL；尚未生成时为 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="ho-adv-cw-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-adv-cw-next-title"></a>

## 下一步

创建成功后可进行以下操作：

-   [查询World构建状态](happyoyster-adventure-query-world-build-status-a-4830e59b84023226.md)：每 3–5 秒轮询，直到 World 进入 `ready`。
-   World 进入 `ready` 后，调用[获取体验凭证](happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md)换取一次性 `ticket`。
-   [查询World详情](happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)：查询完整创建元数据。
