# Tripo-贴图

Tripo贴图可为已有3D模型生成贴图，支持PBR材质和最高8K贴图质量。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="适用范围"></a>

<a id="ttx013h2scop"></a>

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先创建可产出3D模型的任务（如[Tripo-文生/图生3D模型](tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），待任务执行成功后，将其`task_id`传入`original_model_task_id`；也可不创建前序任务，通过`model_url`直接传入模型文件的公网URL。

<a id="http调用"></a>

<a id="ttx101h2http"></a>

## HTTP调用

API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="ttx111h3stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="ttx123h4reqp"></a><h4>请求参数</h4><a id="ttx142h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="ttx154h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。固定值：<code>Tripo/Tripo-Texture</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>original_model_task_id</strong> <code>string</code> （条件必填）</p><p>前序任务ID。传入前序任务创建时返回的<code>task_id</code>，系统会自动使用该任务输出的3D模型。与<code>model_url</code>二选一。</p><p>前序任务可为任意产出3D模型文件（如GLB）的任务，例如<a href="tripo-3d-generation-api-reference-a4c298b3ddebaa99.md">Tripo-文生/图生3D模型</a>。需满足以下条件：</p><ul><li>前序任务必须已执行成功。</li><li>发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。</li><li>前序任务不是Tripo-文生/图生3D模型任务时，须同时传入<code>texture_prompt</code>。</li><li>使用<code>part_names</code>时，须传入<a href="tripo-segmentation-api-reference-cec9c68cea8a90f7.md">Tripo-网格分割</a>任务的<code>task_id</code>。</li></ul><p><strong>model_url</strong> <code>string</code> （条件必填）</p><p>可公开访问的3D模型文件URL。与<code>original_model_task_id</code>二选一。</p><p>模型限制：</p><ul><li>支持格式：GLB、GLTF、FBX、OBJ、STL。</li><li>文件大小：不超过150MB。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>贴图参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>texture_quality</strong> <code>string</code> （可选）</p><p>贴图质量。可选值：</p><ul><li><code>standard</code>：默认值，标清贴图，兼顾质量与速度。</li><li><code>detailed</code>：高清贴图，保真度更高，生成速度较慢。</li><li><code>extreme</code>：8K贴图，保真度最高，相比<code>detailed</code>消耗更多积分。</li></ul><p><strong>model_version</strong> <code>string</code> （可选）</p><p>贴图模型版本。请根据源3D模型的生成版本选择。可选值：</p><ul><li><code>v3.0-20250812</code>：默认值。推荐用于<code>v3.0-20250812</code>或<code>v3.1-20260211</code>版本生成的模型。</li><li><code>v2.5-20250123</code>：推荐用于<code>v2.5-20250123</code>版本生成的模型。</li></ul><p><strong>pbr</strong> <code>boolean</code> （可选）</p><p>是否生成PBR材质。默认值为<code>true</code>。</p><p><strong>texture_prompt</strong> <code>object</code> （可选）</p><p>贴图引导输入，用于通过文本或参考图指导贴图生成。待贴图模型由Tripo生成时可不传，但前序任务不是Tripo-文生/图生3D模型任务（如网格分割任务）时必须传入，否则任务失败。<code>text</code>、<code>image</code>、<code>images</code>三者互斥，只能选择其一；<code>style_image</code>仅可与<code>text</code>搭配使用。</p><ul><li><p><code>text</code>：描述期望贴图风格的文本提示词。示例：</p><a id="code-block"></a><pre class="language-json"><code>{&quot;text&quot;: &quot;磨损的皮革带划痕&quot;}
</code></pre></li><li><p><code>style_image</code>：风格参考图的公网URL，仅可与<code>text</code>搭配使用，建议分辨率不低于256×256像素。示例：</p><a id="code-block-2"></a><pre class="language-json"><code>{&quot;text&quot;: &quot;赛博朋克风格&quot;, &quot;style_image&quot;: &quot;https://.../xx.png&quot;}
</code></pre></li><li><p><code>image</code>：单张参考图的公网URL。</p></li><li><p><code>images</code>：多视角参考图，须传入正面视角，且至少提供2个视角。支持以下两种写法：</p><ul><li><p>key-value写法（推荐）：传入一个对象，以视角名称为键、图片的公网URL为值。视角名称可选<code>front</code>（正面）、<code>left</code>（左侧）、<code>back</code>（背面）、<code>right</code>（右侧），没有的视角直接省略。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;images&quot;: {
        &quot;front&quot;: &quot;https://.../front.png&quot;,
        &quot;left&quot;: &quot;https://.../left.png&quot;
    }
}
</code></pre></li><li><p>数组写法：传入长度为4的数组，按正面、左侧、背面、右侧的顺序依次填入图片的公网URL，缺失的视角传<code>null</code>或<code>&quot;&quot;</code>占位。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;images&quot;: [
        &quot;https://.../front.png&quot;,
        &quot;https://.../left.png&quot;,
        null,
        null
    ]
}
</code></pre></li></ul></li></ul><p>参考图（<code>style_image</code>、<code>image</code>、<code>images</code>）须为公网URL，单张图片不超过20MB，建议使用JPG、PNG或WebP格式。</p><div><div><p><strong>说明</strong>若通过<code>original_model_task_id</code>发起贴图任务，建议在本次请求中重新传入参考图。</p></div></div><p><strong>texture_alignment</strong> <code>string</code> （可选）</p><p>贴图对齐优先级。可选值：</p><ul><li><code>original_image</code>：默认值，优先匹配输入图像的颜色。</li><li><code>geometry</code>：优先匹配几何体。</li></ul><p><strong>texture_seed</strong> <code>integer</code> （可选）</p><p>贴图生成的随机种子。取值范围：-2147483648~2147483647。</p><p>使用相同种子将生成相同的贴图。不设置时每次使用随机种子。</p><p><strong>bake</strong> <code>boolean</code> （可选）</p><p>是否将高级材质效果烘焙到基础贴图中，以提高兼容性。默认值为<code>true</code>。</p><p><strong>part_names</strong> <code>array[string]</code> （可选）</p><p>需要贴图的部件名称列表。</p><ul><li>部件名取自前序网格分割任务结果模型（GLB）中的部件节点名，形如<code>tripo_part_0</code>、<code>tripo_part_1</code>；任务结果字段不单独返回部件名，且编号可能不连续，请读取 GLB 的节点名获取。</li><li>仅当前序任务为<a href="tripo-segmentation-api-reference-cec9c68cea8a90f7.md">Tripo-网格分割</a>任务（或<a href="tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md">Tripo-智能分割</a>返回的<code>seg_task_id</code>）时有效。</li><li>不传则处理全部部件。</li><li>传入不存在的名称不报错、照常计费。</li></ul><p><strong>compress</strong> <code>string</code> （可选）</p><p>压缩模式。不传则不压缩。可选值：</p><ul><li><code>geometry</code>：使用 meshopt 压缩几何数据，减小文件体积。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="模型url-文本引导"></a><section><a id="模型url-文本引导-h4"></a><h4>模型URL + 文本引导</h4><a id="code-block-5"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-Texture&quot;,
    &quot;input&quot;: {
        &quot;model_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb&quot;
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;standard&quot;,
        &quot;texture_prompt&quot;: {
            &quot;text&quot;: &quot;橘白相间的短毛猫&quot;
        }
    }
}'
</code></pre></section><a id="任务id-参考图引导"></a><section><a id="任务id-参考图引导-h4"></a><h4>任务ID + 参考图引导</h4><a id="code-block-6"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-Texture&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;57f62a73-a9f0-4846-9627-xxxxxx&quot;
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;detailed&quot;,
        &quot;pbr&quot;: false,
        &quot;bake&quot;: true,
        &quot;texture_alignment&quot;: &quot;geometry&quot;,
        &quot;texture_prompt&quot;: {
            &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png&quot;
        }
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="ttx285h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="ttx401h3stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../model-api-reference/more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="ttx424h4qr01"></a><h4>请求参数</h4><a id="ttx434h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="ttx440h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-9"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="ttx448h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含贴图后的3D模型URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong><code>array</code></p><p>贴图结果列表。仅在 task_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>model_url</strong> <code>string</code></p><p>贴图后3D模型的URL。</p><p><strong>pbr_model_url</strong> <code>string</code></p><p>PBR材质模型的URL。按需返回。</p><p><strong>rendered_image_url</strong> <code>string</code></p><p>3D模型预览渲染图的URL。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。仅在任务成功时返回，任务失败时不返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>3d_task_type</strong> <code>string</code></p><p>任务类型。贴图固定为<code>texture</code>。</p><p><strong>credits_consumed</strong> <code>integer</code></p><p>本次任务消耗的积分，等于<code>texture_quality</code>。</p><p><strong>texture_quality</strong> <code>integer</code></p><p>生成贴图消耗的积分，按贴图质量计算。</p></div></section></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;26070204-a08e-998e-9366-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;0cc7f681-4547-4183-af5e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-10-19 09:20:29.666&quot;,
        &quot;scheduled_time&quot;: &quot;2026-10-19 09:20:29.731&quot;,
        &quot;end_time&quot;: &quot;2026-10-19 09:21:36.232&quot;,
        &quot;results&quot;: [
            {
                &quot;rendered_image_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/legacy_mesh.webp?auth_key=xxxx&quot;,
                &quot;model_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/tripo_texture_xxxx.glb?auth_key=xxxx&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;3d_task_type&quot;: &quot;texture&quot;,
        &quot;credits_consumed&quot;: 10,
        &quot;texture_quality&quot;: 10
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The parameter is invalid xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="ttx901h2errc"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](../model-api-reference/preparations/error-code.md)进行解决。
