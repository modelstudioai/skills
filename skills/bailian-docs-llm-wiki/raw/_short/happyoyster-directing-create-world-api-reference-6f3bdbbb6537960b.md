# HappyOyster-Directing-创建World API参考

创建一个实时导演 World。支持普通模式（自然语言 Prompt）和剧本模式（结构化 ScriptList），接口立即返回加密 World ID，World 在后台异步构建，客户端轮询构建进度直至完成。

<a id="适用范围"></a>

<a id="ho-dir-cw-scope-title"></a>

## 适用范围

创建一个 Directing World。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md#c38fb45bc6sje)。
-   **调用模式**：推荐使用异步模式。
    
    -   **异步模式**（默认）：`async=true`，接口立即返回 `encryptedWorldId`，需轮询[查询World构建状态](happyoyster-directing-query-world-build-status-a-48bf75e27c43945d.md)获取进度。
    -   **同步模式**：`async=false`，服务端内部轮询（间隔 3s，最长 120s），构建完成后返回；超时则降级为异步，客户端继续轮询。
-   **接口限制**：本接口只能创建 Directing World，无需传 `mode`（服务端按 `2` 写入，传入非 `2` 返回 `400000`）。`creationModel` 支持 `simple`（普通模式，默认）和 `scriptlist`（剧本模式），进房版本固定为 `storyV2`，`aspectRatio` 和 `maxExperienceTimeSec` 固定为 `null`。
    

<a id="http调用"></a>

<a id="ho-dir-cw-http-title"></a>

## HTTP调用

<a id="sec-tabs"></a>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="普通模式-creationmodel-simple"></a>

<a id="ho-dir-cw-simple-title"></a>

### 普通模式（`creationModel=simple`）

<table><tbody><tr><td><a id="ho-dir-cw-simple-req-title"></a><h4>请求参数</h4></td><td rowspan="14"><a id="sec-tabs-2"></a><section><a id="普通模式-纯文本-异步创建"></a><section><a id="普通模式-纯文本-异步创建-h4"></a><h4>普通模式·纯文本（异步创建）</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;async&quot;: true,
    &quot;creationModel&quot;: &quot;simple&quot;,
    &quot;eventStyle&quot;: &quot;normal&quot;,
    &quot;prompt&quot;: &quot;第一视角（POV）互动视频，镜头模拟我的双眼，锁定正对面的白色马尔济斯小狗：白色厨师帽、黑色扣子厨师服。柔和居家厨房背景，光影温暖，小狗眼神始终看向镜头。&quot;,
    &quot;resolution&quot;: &quot;720p&quot;,
    &quot;layout&quot;: &quot;Stable&quot;,
    &quot;narrative&quot;: &quot;Calm&quot;
}'
</code></pre></section><a id="普通模式-文本-参考图-异步创建"></a><section><a id="普通模式-文本-参考图-异步创建-h4"></a><h4>普通模式·文本+参考图（异步创建）</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;async&quot;: true,
    &quot;creationModel&quot;: &quot;simple&quot;,
    &quot;eventStyle&quot;: &quot;normal&quot;,
    &quot;prompt&quot;: &quot;窗边咖啡馆。黑长发年轻女子穿米色高领毛衣侧坐，左手托腮望向布满雨珠的玻璃窗。木桌上有一杯冒热气的深色咖啡。窗外雨夜暖黄街灯，室内一盏吊灯。安静雨夜。&quot;,
    &quot;resolution&quot;: &quot;720p&quot;,
    &quot;inputImages&quot;: [
        {
            &quot;url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9fc7.png&quot;,
            &quot;referenceType&quot;: &quot;default&quot;
        }
    ]
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型，固定为 <code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-dir-cw-simple-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>async</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否异步创建。默认 <code>true</code>：</p><ul><li><code>true</code>：立即返回，World 在后台构建，客户端轮询<a href="happyoyster-directing-query-world-build-status-a-48bf75e27c43945d.md">查询World构建状态</a>。</li><li><code>false</code>：服务端每 3 秒轮询一次，最长等待 120 秒，构建完成后返回；超时仍返回 <code>generating</code>，客户端随后改为自行轮询。</li></ul></td></tr><tr><td><p><strong>creationModel</strong> <code>string</code> <strong>（可选）</strong></p><p>创建子模式，普通模式传 <code>simple</code>（默认）。由您提供自然语言 <code>prompt</code>，服务端生成完整 45 拍剧本、首帧（可自带）和角色参考图。World 创建后，可在 Travel 阶段调用以下控制接口：</p><ul><li><code>instruct</code>：发送文本过程指令</li><li><code>pause</code>：暂停</li><li><code>resume</code>：恢复</li><li><code>rewind</code>：回溯</li><li><code>end</code>：结束</li></ul><p>各接口说明见<a href="#ho-dir-cw-notes-title">补充说明</a>。</p></td></tr><tr><td><p><strong>eventStyle</strong> <code>string</code> <strong>（可选）</strong></p><p>仅 <code>creationModel=simple</code> 生效：选择剧本生成模板。默认 <code>normal</code>。可选值：</p><ul><li><code>normal</code>：常规 / 标准风格（默认）。按用户意图补全 4–5 幕，节奏相对平稳，不强行加入冲突、反转或三幕高潮。</li><li><code>dramatic</code>：戏剧 / 冲突风格。按约 180 秒三幕骨架生成剧本：开场钩子、上升冲突、转折、高潮收束；开放演绎时按类型安排反转（悬疑 / 惊悚 / 逆袭等），节奏更密、戏剧性更强。</li><li><code>regular</code>：旧值，仅为兼容历史入参保留，服务端按 <code>normal</code> 处理；新调用请勿使用。</li></ul></td></tr><tr><td><p><strong>refWorldId</strong> <code>string</code> <strong>（可选）</strong></p><p>基于已有 Directing World 衍生创建。必须是当前主账号名下的 Directing 加密 World ID；其它模型或其它主账号的 World 返回 <code>403001</code>。</p></td></tr><tr><td><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>世界主题描述，支持中英文。非空，最长 2000 字符。</p></td></tr><tr><td><p><strong>resolution</strong> <code>string</code> <strong>（必选）</strong></p><p>视频分辨率。可选值：</p><ul><li><code>480p</code></li><li><code>720p</code></li></ul></td></tr><tr><td><p><strong>layout</strong> <code>string</code> <strong>（可选）</strong></p><p>镜头运动风格（镜头怎么动、切得多猛）。可选值：</p><ul><li><code>Stable</code>：镜头稳、运动少，偏连续长镜头，切镜稀疏</li><li><code>Fast</code>：镜头快、动能强，硬切 / 快速变焦 / 景别跳变更密</li><li><code>Calm</code>：介于两者之间，镜头克制，不急不猛</li></ul></td></tr><tr><td><p><strong>narrative</strong> <code>string</code> <strong>（可选）</strong></p><p>叙事风格（戏密不密、情绪强不强）。可选值：</p><ul><li><code>Calm</code>：事件少，偏氛围、慢推进</li><li><code>Dramatic</code>：事件密，反应 / 反转 / 障碍更明显，张力高</li><li><code>Normal</code>：常规叙事密度，中间档</li><li><code>Steady</code>：节奏匀、不堆高潮，和 <code>Normal</code> 接近</li></ul></td></tr><tr><td><p><strong>firstFrameImage</strong> <code>object</code> <strong>（可选）</strong></p><p>提供后直接复用为 World 首帧，跳过 AI 首帧生成。<code>url</code> 与 <code>base64</code> 二选一且互斥。图片约束如下：</p><ul><li>格式：JPG / JPEG / PNG / WebP</li><li>大小：单张严格小于 6 MB</li><li>宽高比：必须为横屏，宽 / 高为 1.5–2.0（画面比例跟随该图）</li><li>内容安全：未通过内容安全或版权 / IP 校验返回 <code>403004</code> / <code>403005</code></li></ul><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code> <strong>（条件必选）</strong></p><p>首帧图片 URL。约束：</p><ul><li>必须是带 Host 的合法 <code>http</code> / <code>https</code> URL，并可由服务端访问</li><li>真实格式、大小和首帧宽高比在转存后校验</li><li>异步请求可能先返回 <code>generating</code>，随后 World 因图片校验失败进入 <code>failed</code></li></ul><p><strong>base64</strong> <code>string</code> <strong>（条件必选）</strong></p><p>首帧图片 base64。约束：</p><ul><li>推荐使用完整 data URI <code>data:image/&lt;subtype&gt;;base64,&lt;payload&gt;</code></li><li>在创建入口同步校验格式、大小和首帧宽高比</li></ul><p><strong>referenceType</strong> <code>string</code> <strong>（可选）</strong></p><p>参考图类型，默认 <code>default</code>。</p></div></section></td></tr><tr><td><p><strong>inputImages</strong> <code>array</code> <strong>（可选）</strong></p><p>用于剧本生成和角色参考图，最多 6 张，与 <code>firstFrameImage</code> 相互独立。数组每项的 <code>url</code> 与 <code>base64</code> 二选一且互斥。图片约束如下：</p><ul><li>格式：JPG / JPEG / PNG / WebP</li><li>大小：单张严格小于 6 MB</li><li>宽高比：必须为横屏，宽 / 高为 1.5–2.0（画面比例跟随该图）</li><li>内容安全：未通过内容安全或版权 / IP 校验返回 <code>403004</code> / <code>403005</code></li></ul><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code> <strong>（条件必选）</strong></p><p>图片 URL。约束：</p><ul><li>必须是带 Host 的合法 <code>http</code> / <code>https</code> URL，并可由服务端访问</li><li>真实格式、大小和宽高比在转存后校验</li><li>异步请求可能先返回 <code>generating</code>，随后 World 因图片校验失败进入 <code>failed</code></li></ul><p><strong>base64</strong> <code>string</code> <strong>（条件必选）</strong></p><p>图片 base64。约束：</p><ul><li>推荐使用完整 data URI <code>data:image/&lt;subtype&gt;;base64,&lt;payload&gt;</code></li><li>在创建入口同步校验格式、大小和宽高比</li></ul><p><strong>referenceType</strong> <code>string</code> <strong>（可选）</strong></p><p>参考图类型，默认 <code>default</code>。</p></div></section></td></tr></tbody></table>

<a id="剧本模式-creationmodel-scriptlist"></a>

<a id="ho-dir-cw-scriptlist-title"></a>

### 剧本模式（`creationModel=scriptlist`）

<table><tbody><tr><td><a id="ho-dir-cw-scriptlist-req-title"></a><h4>请求参数</h4></td><td rowspan="10"><a id="sec-tabs-3"></a><section><a id="剧本模式-异步创建"></a><section><a id="剧本模式-异步创建-h4"></a><h4>剧本模式（异步创建）</h4><a id="code-block-3"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;async&quot;: true,
    &quot;creationModel&quot;: &quot;scriptlist&quot;,
    &quot;resolution&quot;: &quot;720p&quot;,
    &quot;firstFrameImage&quot;: {
        &quot;url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9fc7.png&quot;,
        &quot;referenceType&quot;: &quot;default&quot;
    },
    &quot;scriptList&quot;: {
        &quot;videoTitle&quot;: &quot;苏念·今晚陪你坐一会儿&quot;,
        &quot;synopsis&quot;: &quot;少女苏念坐在浅色书桌前正对镜头，陪你慢慢聊天、把今天放下。&quot;,
        &quot;subjects&quot;: [
            {
                &quot;label&quot;: &quot;[character_1]&quot;,
                &quot;name&quot;: &quot;苏念&quot;,
                &quot;type&quot;: &quot;character&quot;,
                &quot;gender&quot;: &quot;female&quot;,
                &quot;age&quot;: &quot;少女&quot;,
                &quot;ethnicity&quot;: &quot;东亚&quot;,
                &quot;appearance&quot;: &quot;黑色中长直发偏分，圆润脸型，米白色针织上衣，二次元动漫风，干净线条&quot;,
                &quot;position&quot;: &quot;画面中央，坐在浅色书桌前&quot;,
                &quot;voice&quot;: &quot;温柔少女声，语速偏慢，音量适中&quot;
            }
        ],
        &quot;acts&quot;: [
            {
                &quot;turn&quot;: 1,
                &quot;content&quot;: &quot;[character_1] 坐在浅色书桌前正对镜头，身体微微前倾，眼睛弯起轻声说「来啦，今晚也陪你坐一会儿，慢慢聊」&quot;,
                &quot;cameraType&quot;: &quot;Push-in&quot;,
                &quot;shotSize&quot;: &quot;Medium&quot;,
                &quot;cut&quot;: &quot;long-take&quot;
            },
            {
                &quot;turn&quot;: 2,
                &quot;content&quot;: &quot;[character_1] 双手交叠放在桌上，轻轻点头说「先把今天那些烦心的事，都暂时放到一边吧」&quot;,
                &quot;cameraType&quot;: &quot;Static&quot;,
                &quot;shotSize&quot;: &quot;Medium&quot;,
                &quot;cut&quot;: &quot;long-take&quot;
            },
            {
                &quot;turn&quot;: 3,
                &quot;content&quot;: &quot;[character_1] 微微歪头，表情温和地看着镜头，问「这一天过下来，你还好吗，累不累」&quot;,
                &quot;cameraType&quot;: &quot;Static&quot;,
                &quot;shotSize&quot;: &quot;Medium&quot;,
                &quot;cut&quot;: &quot;long-take&quot;
            }
        ]
    }
}'
</code></pre></section></section></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型，固定为 <code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key 鉴权。仅支持<strong>主 API Key</strong>，以 <code>sk-</code> 开头，如 <code>sk-xxx</code>。通常配置为环境变量 <code>$DASHSCOPE_API_KEY</code>。临时 API Key（<code>st-</code> 开头）调用返回 <code>403003</code>。</p></td></tr><tr><td><a id="ho-dir-cw-scriptlist-req-body-h5"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>async</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否异步创建。默认 <code>true</code>：</p><ul><li><code>true</code>：立即返回，World 在后台构建，客户端轮询<a href="happyoyster-directing-query-world-build-status-a-48bf75e27c43945d.md">查询World构建状态</a>。</li><li><code>false</code>：服务端每 3 秒轮询一次，最长等待 120 秒，构建完成后返回；超时仍返回 <code>generating</code>，客户端随后改为自行轮询。</li></ul></td></tr><tr><td><p><strong>creationModel</strong> <code>string</code> <strong>（可选）</strong></p><p>创建子模式，剧本模式传 <code>scriptlist</code>。结构化剧本由您提供，服务端不再生成剧本，仅做组装并落库。World 创建后，可在 Travel 阶段调用以下控制接口：</p><ul><li><code>update-script</code>：全量替换剧本</li><li><code>pause</code>：暂停</li><li><code>resume</code>：恢复</li><li><code>rewind</code>：回溯</li><li><code>end</code>：结束</li></ul><p>不支持 <code>instruct</code>（发送文本过程指令）。各接口说明见<a href="#ho-dir-cw-notes-title">补充说明</a>。</p><div><div><p><strong>说明</strong></p><code>eventStyle</code> 不参与 scriptlist 创建，请勿传入。</div></div></td></tr><tr><td><p><strong>refWorldId</strong> <code>string</code> <strong>（可选）</strong></p><p>基于已有 Directing World 衍生创建。必须是当前主账号名下的 Directing 加密 World ID；其它模型或其它主账号的 World 返回 <code>403001</code>。</p></td></tr><tr><td><p><strong>resolution</strong> <code>string</code> <strong>（必选）</strong></p><p>视频分辨率。可选值：</p><ul><li><code>480p</code></li><li><code>720p</code></li></ul></td></tr><tr><td><p><strong>firstFrameImage</strong> <code>object</code> <strong>（必选）</strong></p><p>直接复用为 World 首帧的图片引用。<code>url</code> 与 <code>base64</code> 二选一且互斥。图片约束如下：</p><ul><li>格式：JPG / JPEG / PNG / WebP</li><li>大小：单张严格小于 6 MB</li><li>宽高比：必须为横屏，宽 / 高为 1.5–2.0（画面比例跟随该图）</li><li>内容安全：未通过内容安全或版权 / IP 校验返回 <code>403004</code> / <code>403005</code></li></ul><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code> <strong>（条件必选）</strong></p><p>首帧图片 URL。约束：</p><ul><li>必须是带 Host 的合法 <code>http</code> / <code>https</code> URL，并可由服务端访问</li><li>真实格式、大小和首帧宽高比在转存后校验</li><li>异步请求可能先返回 <code>generating</code>，随后 World 因图片校验失败进入 <code>failed</code></li></ul><p><strong>base64</strong> <code>string</code> <strong>（条件必选）</strong></p><p>首帧图片 base64。约束：</p><ul><li>推荐使用完整 data URI <code>data:image/&lt;subtype&gt;;base64,&lt;payload&gt;</code></li><li>在创建入口同步校验格式、大小和首帧宽高比</li></ul><p><strong>referenceType</strong> <code>string</code> <strong>（可选）</strong></p><p>参考图类型，默认 <code>default</code>。</p></div></section></td></tr><tr><td><p><strong>scriptList</strong> <code>object</code> <strong>（必选）</strong></p><p>结构化剧本，必须包含 <code>synopsis</code> 与非空 <code>acts</code>。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>synopsis</strong> <code>string</code> <strong>（必选）</strong></p><p>故事梗概。非空，最长 2000 字。</p><p><strong>videoTitle</strong> <code>string</code> <strong>（可选）</strong></p><p>世界名称。默认 <code>New World</code>，最长 128 字。</p><p><strong>scene</strong> <code>string</code> <strong>（可选）</strong></p><p>场景设定。默认 <code>Static Shot</code>，最长 64 字。</p><p><strong>style</strong> <code>string</code> <strong>（可选）</strong></p><p>视觉风格。默认 <code>Stable</code>，最长 64 字。</p><p><strong>speed</strong> <code>string</code> <strong>（可选）</strong></p><p>叙事节奏。默认 <code>Steady</code>，最长 64 字。</p><p><strong>language</strong> <code>string</code> <strong>（可选）</strong></p><p>剧本语言。默认 <code>en</code>（英文），中文传 <code>zh</code>。最长 64 字。</p><p><strong>setting</strong> <code>string</code> <strong>（可选）</strong></p><p>世界观或背景设定。最长 2000 字。</p><p><strong>soundtrack</strong> <code>string</code> <strong>（可选）</strong></p><p>配乐描述。最长 500 字。</p><p><strong>prologue</strong> <code>string</code> <strong>（可选）</strong></p><p>开场白。最长 1000 字。</p><p><strong>videoTags</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>视频标签。最多 20 个，单个标签最长 32 字。</p><p><strong>subjects</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>预定义主体，最多 6 个。数组每项含以下属性：</p><a id="accordion-subjects-属性"></a><section><p>subjects[] 属性</p><div><p><strong>label</strong> <code>string</code> <strong>（可选）</strong></p><p>在 <code>acts[].content</code> 中引用主体。格式为 <code>[character_x]</code>，默认按数组顺序分配。</p><p><strong>name</strong> <code>string</code> <strong>（可选）</strong></p><p>人类可读名称，不渲染为画面文字。最长 64 字。</p><p><strong>type</strong> <code>string</code> <strong>（可选）</strong></p><p>主体类型，默认 <code>character</code>。决定该主体的形象与其它属性如何填写。可选值：</p><ul><li><code>character</code>：人类角色（默认）。按人填写 <code>gender</code> / <code>position</code> / <code>ethnicity</code> / <code>age</code> / <code>appearance</code>。</li><li><code>animal</code>：真实动物（猫、狗、马等）。用物种代替性别、亚种 / 品种代替族裔。</li><li><code>creature</code>：非人 / 幻想生物（龙、妖怪、外星人等）。同样按非人形象填写。</li><li><code>narrator</code>：旁白 / 画外音。只有声音、不出画面，填写 <code>voice</code>，不产出参考图。</li></ul><p><strong>refImage</strong> <code>object</code> <strong>（可选）</strong></p><p>主体参考图，<code>url</code> 与 <code>base64</code> 二选一且互斥，图片严格小于 6 MB。</p><a id="accordion-refimage-属性"></a><section><p>refImage 属性</p><div><p><strong>url</strong> <code>string</code> <strong>（条件必填）</strong></p><p>主体参考图 URL。</p><p><strong>base64</strong> <code>string</code> <strong>（条件必填）</strong></p><p>主体参考图 base64。</p><p><strong>referenceType</strong> <code>string</code> <strong>（可选）</strong></p><p>参考图类型，默认 <code>default</code>。</p></div></section><p><strong>gender</strong> <code>string</code> <strong>（可选）</strong></p><p>性别描述。最长 64 字。</p><p><strong>position</strong> <code>string</code> <strong>（可选）</strong></p><p>画面位置。最长 64 字。</p><p><strong>ethnicity</strong> <code>string</code> <strong>（可选）</strong></p><p>族裔或人种描述。最长 64 字。</p><p><strong>age</strong> <code>string</code> <strong>（可选）</strong></p><p>年龄描述。最长 64 字。</p><p><strong>appearance</strong> <code>string</code> <strong>（可选）</strong></p><p>外观细节。最长 500 字。</p><p><strong>voice</strong> <code>string</code> <strong>（可选）</strong></p><p>音色、语速和音量描述。最长 200 字。</p></div></section><p><strong>acts</strong> <code>array&lt;object&gt;</code> <strong>（必选）</strong></p><p>逐拍剧本，1–45 条，全部 <code>content</code> 合计不超过 100000 字。数组每项含以下属性：</p><a id="accordion-acts-属性"></a><section><p>acts[] 属性</p><div><p><strong>turn</strong> <code>int</code> <strong>（可选）</strong></p><p>turn 序号。1–45，不可重复，默认按数组顺序从 1 递增。</p><p><strong>content</strong> <code>string</code> <strong>（必选）</strong></p><p>本拍剧本。非空，单拍最长 2000 字，可用 <code>[character_x]</code> 引用主体。</p><p><strong>cameraType</strong> <code>string</code> <strong>（可选）</strong></p><p>镜头类型（镜头怎么拍）。默认 <code>Static</code>。可选值：</p><ul><li><code>Static</code>：机位锁死，不推不摇（默认值）。景别靠 <code>shotSize</code> 控制：远 / 中 / 近</li><li><code>Tracking</code>：跟拍。机位跟着主体走，保持跟拍距离</li><li><code>Pan Left</code>：机位不动，镜头向左横摇</li><li><code>Pan Right</code>：机位不动，镜头向右横摇</li><li><code>Tilt Up</code>：镜头上仰</li><li><code>Tilt Down</code>：镜头下俯</li><li><code>Push-in</code>：光学 / 物理推进，画面逐渐靠近</li><li><code>Pull-out</code>：拉远，画面逐渐变宽</li><li><code>POV Forward</code>：第一人称，镜头即眼睛，向前走</li><li><code>POV Look Down</code>：第一人称低头看</li><li><code>POV Look Up</code>：第一人称抬头看</li><li><code>POV Turn Left</code>：第一人称左转看</li><li><code>POV Turn Right</code>：第一人称右转看</li></ul><p><strong>shotSize</strong> <code>string</code> <strong>（可选）</strong></p><p>景别，默认 <code>Medium</code>。决定这一拍能写多细，换景别应靠切镜，不要在同一拍里既写全身又写指尖。可选值：</p><ul><li><code>Wide</code>：远景 / 全景，含全身与环境关系。适合走位、站位、空间调度，不写微表情、指尖。</li><li><code>Medium</code>：中景（默认），上半身姿态与手势。适合对话、日常动作，不写脚部走位、精细手部操作。</li><li><code>Close-up</code>：特写，一张脸 / 一只手 / 一件道具。适合表情、关键细节，不写全身移动。</li></ul><p>与切镜搭配：要看更细，先 <code>cut-in</code> 到 <code>Close-up</code>，再 <code>cut-out</code> 回宽景；多数拍用 <code>long-take</code> 稳住同一景别，避免景别来回跳。</p><p><strong>cut</strong> <code>string</code> <strong>（可选）</strong></p><p>切镜方式（这一拍怎么切进来）。默认 <code>long-take</code>。可选值：</p><ul><li><code>long-take</code>：不切，上一镜接着拍。默认，也最稳</li><li><code>hard-cut</code>：硬切，瞬间换成另一镜。对话正反打用这个</li><li><code>cut-in</code>：切到更近的景别，例如 <code>Medium</code> → <code>Close-up</code>。看细节、接手部互动用</li><li><code>cut-out</code>：切到更远的景别，例如 <code>Close-up</code> → <code>Medium</code> / <code>Wide</code></li><li><code>cutaway</code>：短暂切到主线之外的细节</li><li><code>cutback</code>：从 <code>cutaway</code> 切回主主体。只能跟在 <code>cutaway</code> 后面</li><li><code>camera movement transition</code>：用快速运镜把两段连起来，不是硬切</li></ul></div></section></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="ho-dir-cw-resp-header-h4"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-4"></a><section><a id="异步创建"></a><section><a id="异步创建-h4"></a><h4>异步创建</h4><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: 0,
    &quot;message&quot;: null,
    &quot;data&quot;: {
        &quot;encryptedWorldId&quot;: &quot;enc_a1b2****&quot;,
        &quot;status&quot;: &quot;generating&quot;,
        &quot;firstFrame&quot;: null
    }
}
</code></pre></section></section></td></tr><tr><td><p><strong>code</strong> <code>integer</code></p><p>返回码。<code>0</code> 表示成功，非 0 为错误码。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>错误信息。成功时为 <code>null</code>。</p></td></tr><tr><td><p><strong>data</strong> <code>object</code></p><p>响应数据。失败时为 <code>null</code>。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>encryptedWorldId</strong> <code>string</code></p><p>加密 World ID，同步 / 异步模式均返回。后续查询构建状态、World 详情和换取体验凭证均使用此值。</p><p><strong>status</strong> <code>string</code></p><p>当前创建状态：</p><ul><li><code>generating</code>：构建中</li><li><code>ready</code>：就绪</li><li><code>failed</code>：构建失败</li></ul><p><strong>firstFrame</strong> <code>string</code></p><p>World 首帧 URL；尚未生成时为 <code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="补充说明"></a>

<a id="ho-dir-cw-notes-title"></a>

## 补充说明

-   **字数计算**：文档中的“最长 N 字”按字符数（Unicode 字符）统计，不区分中英文——中文汉字、英文字母、数字、空格和标点符号均各算 1 个字符。
    
-   **ScriptList 提交要求**：创建 World 时 `acts` 最多 45 条，不要求恰好 45 条；Travel 中调用 [update-script](happyoyster-directing-update-script-api-referenc-559783f11176cb54.md) 时才要求完整提交 45 条。
    
-   **Travel 控制接口**：`creationModel` 中列出的接口名是 World 创建后、在 Travel 阶段可调用的服务端接口，不是本接口的入参枚举值。含义如下：
    
    -   `instruct`：向运行中的 Travel 发送[文本过程指令](happyoyster-directing-instruct-travel-api-refere-2cd5aa6eabceb2c4.md)，仅普通模式。
    -   `pause`：[暂停](happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md) Travel。
    -   `resume`：[恢复](happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md)播放。
    -   `rewind`：[回溯](happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md)到指定时间点，需先暂停。
    -   `end`：[结束](happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md) Travel。
    -   `update-script`：[全量替换剧本](happyoyster-directing-update-script-api-referenc-559783f11176cb54.md)，仅剧本模式。

<a id="错误码"></a>

<a id="ho-dir-cw-errorcode-title"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](../model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

<a id="下一步"></a>

<a id="ho-dir-cw-next-title"></a>

## 下一步

创建成功后可进行以下操作：

-   [查询World构建状态](happyoyster-directing-query-world-build-status-a-48bf75e27c43945d.md)：每 3–5 秒轮询，直到 World 进入 `ready`。
-   World 进入 `ready` 后，调用[获取体验凭证](happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md)换取一次性 `ticket`。
-   [查询World详情](happyoyster-directing-query-world-detail-api-ref-43291135e5d5652f.md)：查询完整创建元数据和 ScriptList。
