# Tripo-自动绑骨

Tripo自动绑骨可自动为3D模型添加骨骼绑定，支持多种骨骼类型。建议先进行可绑骨检查，验证模型兼容性。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="适用范围"></a>

<a id="tar013h2scop"></a>

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](../../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先创建可产出3D模型的任务（如[Tripo-文生/图生3D模型](../../../../_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），待任务执行成功后，将其`task_id`传入`original_model_task_id`；也可不创建前序任务，通过`model_url`直接传入模型文件的公网URL。建议先通过[Tripo-可绑骨检查](tripo-rig-check-api-reference.md)确认模型可绑骨并获取骨骼类型。

<a id="http调用"></a>

<a id="tar101h2http"></a>

## HTTP调用

API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="tar111h3stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="tar123h4reqp"></a><h4>请求参数</h4><a id="tar142h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="tar154h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。固定值：<code>Tripo/Tripo-AutoRig</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>original_model_task_id</strong> <code>string</code> （条件必填）</p><p>前序任务ID。传入前序任务创建时返回的<code>task_id</code>，系统会自动使用该任务输出的3D模型。与<code>model_url</code>二选一。</p><p>前序任务可为任意产出3D模型文件（如GLB）的任务，例如<a href="../../../../_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md">Tripo-文生/图生3D模型</a>。需满足以下条件：</p><ul><li>前序任务必须已执行成功。</li><li>发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。</li></ul><p><strong>model_url</strong> <code>string</code> （条件必填）</p><p>模型文件的公网URL。与<code>original_model_task_id</code>二选一。</p><p>模型限制：</p><ul><li>支持格式：GLB、FBX、OBJ、STL。</li><li>文件大小：不超过150MB。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>绑骨参数。传入未列出的字段将返回400错误。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>out_format</strong> <code>string</code> （可选）</p><p>输出格式。默认值为<code>glb</code>。可选值：</p><ul><li><code>glb</code>：二进制glTF格式，适用于Web。</li><li><code>fbx</code>：FBX格式，适用于DCC工具和游戏引擎。</li></ul><p>传入其他值返回400错误。</p><p><strong>spec</strong> <code>string</code> （可选）</p><p>绑骨规范，即骨骼的命名规范。仅在<code>rig_type</code>为<code>biped</code>时生效。默认值为<code>tripo</code>。可选值：</p><ul><li><code>tripo</code>：Tripo原生骨骼命名。</li><li><code>mixamo</code>：兼容Mixamo的骨骼命名。使用此规范绑骨的模型不能用于<a href="../../../../_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md">Tripo-动画重定向</a>。</li></ul><p><strong>rig_type</strong> <code>string</code> （可选）</p><p>骨骼类型。默认值为<code>biped</code>。建议先调用<a href="tripo-rig-check-api-reference.md">Tripo-可绑骨检查</a>，使用其返回的<code>rig_type</code>。可选值：</p><ul><li><code>biped</code>：双足人形。</li><li><code>quadruped</code>：四足动物。</li><li><code>hexapod</code>：六足生物。</li><li><code>octopod</code>：八足生物。</li><li><code>avian</code>：鸟类或有翼生物。</li><li><code>serpentine</code>：蛇形生物。</li><li><code>aquatic</code>：鱼类或水生生物。</li></ul><p><strong>model_version</strong> <code>string</code> （可选）</p><p>绑骨算法版本。默认值为<code>v1.0-20240301</code>。可选值：</p><ul><li><code>v1.0-20240301</code>：仅适用于（且推荐用于）双足人形绑骨，支持90多种预设动画。</li><li><code>v2.5-20260210</code>：适用于非人形的动物绑骨，包括四足、六足、八足、蛇形、水生和鸟类。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="传入前序任务id"></a><section><a id="传入前序任务id-h4"></a><h4>传入前序任务ID</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-AutoRig&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;
    },
    &quot;parameters&quot;: {
        &quot;rig_type&quot;: &quot;biped&quot;
    }
}'
</code></pre></section><a id="传入模型url"></a><section><a id="传入模型url-h4"></a><h4>传入模型URL</h4><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-AutoRig&quot;,
    &quot;input&quot;: {
        &quot;model_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb&quot;
    },
    &quot;parameters&quot;: {
        &quot;out_format&quot;: &quot;fbx&quot;,
        &quot;rig_type&quot;: &quot;quadruped&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tar285h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="tar401h3stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：自动绑骨可能需要数分钟，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="tar424h4qr01"></a><h4>请求参数</h4><a id="tar434h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="tar440h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tar448h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含绑骨后的3D模型URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong><code>array</code></p><p>绑骨结果列表。仅在 task_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>rendered_image_url</strong> <code>string</code></p><p>3D模型预览渲染图的URL。</p><p><strong>model_url</strong> <code>string</code></p><p>绑骨后3D模型的URL。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。仅在任务成功时返回，任务失败时不返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>3d_task_type</strong> <code>string</code></p><p>任务类型。自动绑骨固定为<code>auto-rig</code>。</p><p><strong>credits_consumed</strong> <code>integer</code></p><p>本次任务消耗的积分。自动绑骨按次计费，无额外计费参数。</p></div></section></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;6b8db7b5-c8bb-95ec-86fc-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;0a0d7d32-3e9c-4888-8057-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-10-19 12:22:09.204&quot;,
        &quot;scheduled_time&quot;: &quot;2026-10-19 12:22:09.255&quot;,
        &quot;end_time&quot;: &quot;2026-10-19 12:23:46.598&quot;,
        &quot;results&quot;: [
            {
                &quot;rendered_image_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/legacy_mesh.webp?auth_key=xxxx&quot;,
                &quot;model_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/tripo_rigging_xxxx.glb?auth_key=xxxx&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;3d_task_type&quot;: &quot;auto-rig&quot;,
        &quot;credits_consumed&quot;: 25
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The parameter is invalid xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="tar901h2errc"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](../../../preparations/error-code.md)进行解决。
