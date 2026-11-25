# Tripo-动画重定向

Tripo动画重定向可将预设动画应用到已绑骨的3D模型上，单次最多5个动画。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="适用范围"></a>

<a id="tre013h2scop"></a>

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先通过[Tripo-自动绑骨](../model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)创建任务（`spec`不能为`mixamo`），待任务执行成功后，将其`task_id`传入`original_model_task_id`。

<a id="http调用"></a>

<a id="tre101h2http"></a>

## HTTP调用

API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="tre111h3stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="tre123h4reqp"></a><h4>请求参数</h4><a id="tre142h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="tre154h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。固定值：<code>Tripo/Tripo-AnimationRetarget</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>original_model_task_id</strong> <code>string</code> <strong>（必选）</strong></p><p>前序任务ID。仅支持<a href="../model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md">Tripo-自动绑骨</a>任务，传入该任务创建时返回的<code>task_id</code>，系统会自动使用该任务输出的已绑骨模型。</p><ul><li>前序任务必须已执行成功。</li><li>发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。</li><li>使用<code>mixamo</code>规格（<code>spec</code>）绑骨的模型不能用于动画重定向。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>动画重定向参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>animations</strong> <code>array[string]</code> （条件必填）</p><p>预设动画名称列表，最多5个，<strong>按动画个数计费</strong>。与<code>animation</code>互斥，只能二选一。</p><p>每个元素须为带<code>preset:</code>前缀的预制动画名称（如<code>preset:walk</code>），区分大小写。不在列表中的名称在创建任务时返回400错误，不扣费。</p><p>完整的动画名称请参见<a href="#tre801h2anim">动画名称列表</a>。</p><p><strong>animation</strong> <code>string</code> （条件必填）</p><p>单个预设动画名称，取值要求与<code>animations</code>相同。与<code>animations</code>互斥，只能二选一。此参数为旧版参数，计为1个动画，计费与<code>animations</code>只传1个动画时相同。</p><p><strong>out_format</strong> <code>string</code> （可选）</p><p>输出格式。默认值为<code>glb</code>。可选值：</p><ul><li><code>glb</code>：二进制glTF格式，适用于Web。</li><li><code>fbx</code>：FBX格式，适用于DCC工具和游戏引擎。</li></ul><p><strong>bake_animation</strong> <code>boolean</code> （可选）</p><p>是否烘焙动画。该参数已废弃，传入不会报错，也不会生效或计费，仅为向后兼容保留，无需传入。</p><p><strong>export_with_geometry</strong> <code>boolean</code> （可选）</p><p>导出时是否包含几何体。默认值为<code>true</code>。</p><p><strong>animate_in_place</strong> <code>boolean</code> （可选）</p><p>是否原地播放动画。默认值为<code>false</code>。设为<code>true</code>时，模型在动画中不产生位移。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="单个动画"></a><section><a id="单个动画-h4"></a><h4>单个动画</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-AnimationRetarget&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;
    },
    &quot;parameters&quot;: {
        &quot;animations&quot;: [&quot;preset:walk&quot;],
        &quot;out_format&quot;: &quot;fbx&quot;
    }
}'
</code></pre></section><a id="多个动画"></a><section><a id="多个动画-h4"></a><h4>多个动画</h4><p>通过<code>animations</code>传入多个动画名称，最多5个。</p><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-AnimationRetarget&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;
    },
    &quot;parameters&quot;: {
        &quot;animations&quot;: [&quot;preset:walk&quot;, &quot;preset:run&quot;],
        &quot;out_format&quot;: &quot;glb&quot;
    }
}'
</code></pre></section><a id="非人形骨骼"></a><section><a id="非人形骨骼-h4"></a><h4>非人形骨骼</h4><p>前序自动绑骨任务的<code>rig_type</code>为非人形骨骼（如<code>quadruped</code>）时，动画名称须使用<code>preset:&lt;体型&gt;:&lt;动作&gt;</code>格式，可用名称请参见<a href="#tre803h3nonh">非人形骨骼</a>。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-AnimationRetarget&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;
    },
    &quot;parameters&quot;: {
        &quot;animations&quot;: [&quot;preset:quadruped:walk&quot;]
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tre285h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="tre401h3stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../model-api-reference/more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="tre424h4qr01"></a><h4>请求参数</h4><a id="tre434h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="tre440h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tre448h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含重定向后的3D模型URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong><code>array</code></p><p>重定向结果列表。仅在 task_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>model_url</strong> <code>string</code></p><p>重定向后3D模型的URL。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。仅在任务成功时返回，任务失败时不返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>3d_task_type</strong> <code>string</code></p><p>任务类型。动画重定向固定为<code>animation-retarget</code>。</p><p><strong>credits_consumed</strong> <code>integer</code></p><p>本次任务消耗的积分，按动画数量计费。动画数量为<code>animations</code>中非空元素的个数；使用<code>animation</code>时计为1个动画。</p></div></section></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;36a8ae2d-e929-9315-8394-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;00195645-f254-41bd-8354-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-10-19 12:56:48.349&quot;,
        &quot;scheduled_time&quot;: &quot;2026-10-19 12:56:48.399&quot;,
        &quot;end_time&quot;: &quot;2026-10-19 12:57:04.742&quot;,
        &quot;results&quot;: [
            {
                &quot;model_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/tripo_retarget_xxxx.fbx?auth_key=xxxx&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;3d_task_type&quot;: &quot;animation-retarget&quot;,
        &quot;credits_consumed&quot;: 10
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The parameter is invalid xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="动画名称列表"></a>

<a id="tre801h2anim"></a>

## 动画名称列表

以下为`parameters.animations`和`parameters.animation`参数的可选值。名称须带`preset:`前缀，区分大小写。

<a id="常用动画"></a>

<a id="tre802h3comm"></a>

### 常用动画

-   `preset:idle`：待机
-   `preset:walk`：行走
-   `preset:run`：奔跑
-   `preset:jump`：跳跃
-   `preset:climb`：攀爬
-   `preset:dive`：俯冲
-   `preset:slash`：挥砍
-   `preset:shoot`：射击
-   `preset:hurt`：受击
-   `preset:fall`：跌落
-   `preset:turn`：转身

<a id="非人形骨骼-2"></a>

<a id="tre803h3nonh"></a>

### 非人形骨骼

非人形骨骼仅支持以下名称，写法为`preset:<体型>:<动作>`。

-   四足（`quadruped`）：`preset:quadruped:walk`、`preset:quadruped:catwalk`
-   水生（`aquatic`）：`preset:aquatic:march`
-   蛇形（`serpentine`）：`preset:serpentine:march`
-   六足（`hexapod`）：`preset:hexapod:walk`
-   八足（`octopod`）：`preset:octopod:walk`

<a id="人形骨骼"></a>

<a id="tre804h3biped"></a>

### 人形骨骼

人形骨骼（`biped`）的动作名有两种等价写法：`preset:<动作>`或`preset:biped:<动作>`，例如`preset:walk`与`preset:biped:walk`效果相同。

-   `preset:afraid`、`preset:agree`、`preset:angry_01`、`preset:angry_02`、`preset:angry_03`
-   `preset:basketball_shot`、`preset:blade_wraparound_test`、`preset:bow`、`preset:box_01`、`preset:box_02`、`preset:box_03`
-   `preset:cast_a_spell`、`preset:cheer`、`preset:chop`、`preset:clap`、`preset:climb`、`preset:complain_01`、`preset:complain_02`、`preset:cpr`、`preset:cross_body_crunch`、`preset:crossover_dribble`、`preset:cry`
-   `preset:dance_01`、`preset:dance_02`、`preset:dance_03`、`preset:dance_04`、`preset:dance_05`、`preset:dance_06`、`preset:defeat_02`、`preset:defeat_03`、`preset:depressed`、`preset:dig`、`preset:dive`、`preset:dribble`
-   `preset:fall`、`preset:fire`、`preset:flee_01`、`preset:flee_02`、`preset:flip`、`preset:fold_arms`、`preset:football_catch`、`preset:football_pass`、`preset:football_save`、`preset:freaky`、`preset:frightened`、`preset:front_kick_01`、`preset:front_kick_02`、`preset:frustrated_01`、`preset:frustrated_02`
-   `preset:golf`、`preset:greet_01`、`preset:greet_02`、`preset:greet_03`、`preset:greet_04`
-   `preset:heart_pose`、`preset:hit_to_body_01`、`preset:hit_to_body_02`、`preset:hit_to_head`、`preset:hit_to_side`、`preset:hit_to_stomach`、`preset:hug`、`preset:hurt`
-   `preset:idle`
-   `preset:jump`、`preset:jump_down`、`preset:jump_rope_01`、`preset:jump_rope_02`
-   `preset:laugh_01`、`preset:laugh_02`、`preset:lift_heavy`、`preset:look_around`
-   `preset:make_a_call_01`、`preset:make_a_call_02`
-   `preset:pitch_baseball`、`preset:play_mobile_game`、`preset:play_video_game`、`preset:press-up`
-   `preset:run`、`preset:run_upstairs`
-   `preset:scared_01`、`preset:scared_02`、`preset:scratch`、`preset:shoot`、`preset:shovel`、`preset:sing_01`、`preset:sing_02`、`preset:sing_03`、`preset:sing_04`、`preset:sit`、`preset:slash`、`preset:sob`、`preset:standing_relax`、`preset:surf`、`preset:swagger`、`preset:swim`、`preset:sword_judgment_test`
-   `preset:turn`
-   `preset:victory_celebration`、`preset:volleyball`
-   `preset:wait`、`preset:walk`、`preset:warm_up`、`preset:wave_goodbye_01`、`preset:wave_goodbye_02`

<a id="错误码"></a>

<a id="tre901h2errc"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](../model-api-reference/preparations/error-code.md)进行解决。
