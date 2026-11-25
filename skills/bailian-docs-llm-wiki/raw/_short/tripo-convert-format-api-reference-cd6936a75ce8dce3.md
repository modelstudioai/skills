# Tripo-格式转换

Tripo格式转换可将3D模型转换为GLTF、USDZ、FBX、OBJ、STL、3MF等格式，并支持网格处理、贴图烘焙和导出设置。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="适用范围"></a>

<a id="tcf013h2scop"></a>

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先创建可产出3D模型的任务（如[Tripo-文生/图生3D模型](tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），待任务执行成功后，将其`task_id`传入`original_model_task_id`。

<a id="http调用"></a>

<a id="tcf101h2http"></a>

## HTTP调用

API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="tcf111h3stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="tcf123h4reqp"></a><h4>请求参数</h4><a id="tcf142h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="tcf154h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。固定值：<code>Tripo/Tripo-ConvertFormat</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>original_model_task_id</strong> <code>string</code> <strong>（必选）</strong></p><p>前序任务ID。传入前序任务创建时返回的<code>task_id</code>，系统会自动使用该任务输出的3D模型。</p><p>前序任务可为任意产出3D模型文件（如GLB）的任务，例如<a href="tripo-3d-generation-api-reference-a4c298b3ddebaa99.md">Tripo-文生/图生3D模型</a>。需满足以下条件：</p><ul><li>前序任务必须已执行成功。</li><li>发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。</li><li>使用<code>part_names</code>时，须传入<a href="tripo-segmentation-api-reference-cec9c68cea8a90f7.md">Tripo-网格分割</a>任务的<code>task_id</code>。</li></ul><p>模型限制：</p><ul><li>支持格式：GLB、GLTF、FBX、OBJ、STL。</li><li>文件大小：不超过150MB。</li></ul><p><strong>format</strong> <code>string</code> <strong>（必选）</strong></p><p>目标导出格式。可选值：</p><ul><li><code>GLTF</code>：适用于Web查看器、WebGL引擎（如Three.js、Babylon.js）。</li><li><code>USDZ</code>：适用于Apple AR Quick Look、RealityKit。</li><li><code>FBX</code>：适用于Unreal、Unity及Maya、Blender等DCC工具。</li><li><code>OBJ</code>：传统交换格式，不支持动画。</li><li><code>STL</code>：适用于3D打印，仅包含几何体。</li><li><code>3MF</code>：适用于3D打印。</li></ul><p>兼容写法：<code>format</code>也可传入<code>glb</code>，效果与传入<code>GLTF</code>相同。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>格式转换参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>quad</strong> <code>boolean</code> （可选）</p><p>是否输出四边面网格（而非三角面）。默认值为<code>false</code>。</p><p>开启后，输出格式强制为FBX；未设置<code>face_limit</code>时，默认面数为10,000。</p><p>设置为<code>true</code>时按高级转换计费。</p><p><strong>force_symmetry</strong> <code>boolean</code> （可选）</p><p>是否强制模型对称。默认值为<code>false</code>。仅当<code>quad</code>为<code>true</code>时生效。</p><p><strong>face_limit</strong> <code>integer</code> （可选）</p><p>输出模型的最大面数。建议不低于100。</p><p>默认值为<code>null</code>，即不限制面数，保持原模型面数；开启<code>quad</code>时默认面数为10,000。</p><p>传入非<code>null</code>的值时按高级转换计费。</p><p><strong>flatten_bottom</strong> <code>boolean</code> （可选）</p><p>是否将模型底部压平。默认值为<code>false</code>。设置为<code>true</code>时按高级转换计费。</p><p><strong>flatten_bottom_threshold</strong> <code>number</code> （可选）</p><p>底部压平的深度阈值。默认值为<code>0.01</code>。仅当<code>flatten_bottom</code>为<code>true</code>时生效。取值不为<code>0.01</code>时按高级转换计费。</p><p><strong>texture_size</strong> <code>integer</code> （可选）</p><p>漫反射贴图的尺寸，单位为像素。建议取值512~8192，不要求为2的幂。</p><p>默认值为<code>4096</code>。取值不为<code>4096</code>时按高级转换计费。</p><p><strong>texture_format</strong> <code>string</code> （可选）</p><p>贴图格式。取值不为<code>JPEG</code>时按高级转换计费。可选值：</p><ul><li><code>JPEG</code>：默认值，文件体积最小。</li><li><code>PNG</code>：无损格式，支持透明度。</li><li><code>WEBP</code>：现代Web格式。</li><li><code>BMP</code>、<code>DPX</code>、<code>HDR</code>、<code>OPEN_EXR</code>、<code>TARGA</code>、<code>TIFF</code>：适用于专业用途。</li></ul><p><strong>pivot_to_center_bottom</strong> <code>boolean</code> （可选）</p><p>是否将模型轴心点移至底部中心。默认值为<code>false</code>。设置为<code>true</code>时按高级转换计费。</p><p><strong>scale_factor</strong> <code>number</code> （可选）</p><p>导出模型的缩放系数。取值须大于0。</p><p>默认值为<code>1.0</code>。传入0或负数不会报错，但无法保证转换结果。取值不为<code>1.0</code>时按高级转换计费。</p><p><strong>bake</strong> <code>boolean</code> （可选）</p><p>是否将高级材质烘焙为基础贴图。默认值为<code>true</code>。</p><p><strong>pack_uv</strong> <code>boolean</code> （可选）</p><p>是否将所有UV合并到统一布局。默认值为<code>false</code>。</p><p><strong>with_animation</strong> <code>boolean</code> （可选）</p><p>是否包含骨骼和动画数据。默认值为<code>true</code>。</p><p><strong>animate_in_place</strong> <code>boolean</code> （可选）</p><p>是否导出原地动画（无根骨骼位移）。默认值为<code>false</code>。</p><p><strong>part_names</strong> <code>array[string]</code> （可选）</p><p>要导出的部件名称列表。</p><ul><li>部件名取自前序网格分割任务结果模型（GLB）中的部件节点名，形如<code>tripo_part_0</code>、<code>tripo_part_1</code>；任务结果字段不单独返回部件名，且编号可能不连续，请读取 GLB 的节点名获取。</li><li>仅当前序任务为<a href="tripo-segmentation-api-reference-cec9c68cea8a90f7.md">Tripo-网格分割</a>任务（或<a href="tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md">Tripo-智能分割</a>返回的<code>seg_task_id</code>）时有效。</li><li>不传则处理全部部件。</li><li>传入不存在的名称不报错、照常计费。</li></ul><p><strong>export_vertex_colors</strong> <code>boolean</code> （可选）</p><p>是否导出顶点色。默认值为<code>false</code>。仅对<code>OBJ</code>和<code>GLTF</code>格式生效。</p><p><strong>export_orientation</strong> <code>string</code> （可选）</p><p>导出模型的朝向（前向轴）。可选值：</p><ul><li><code>+x</code>：默认值，X轴正方向朝前。</li><li><code>-x</code>：X轴负方向朝前。</li><li><code>+y</code>：Y轴正方向朝前。</li><li><code>-y</code>：Y轴负方向朝前。</li></ul><p><strong>fbx_preset</strong> <code>string</code> （可选）</p><p>FBX格式的兼容预设。可选值：</p><ul><li><code>blender</code>：默认值，针对Blender导入优化。</li><li><code>3dsmax</code>：针对3ds Max导入优化。</li><li><code>mixamo</code>：兼容Mixamo绑骨。</li><li><code>bake_scale</code>：导出FBX时将缩放变换烘焙进几何体，而不保留在节点transform上。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="基础转换"></a><section><a id="基础转换-h4"></a><h4>基础转换</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-ConvertFormat&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;,
        &quot;format&quot;: &quot;GLTF&quot;
    }
}'
</code></pre></section><a id="高级转换-四边面"></a><section><a id="高级转换-四边面-h4"></a><h4>高级转换（四边面）</h4><p>设置<code>quad</code>、<code>face_limit</code>等参数后按高级转换计费。开启<code>quad</code>后输出格式强制为FBX。</p><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-ConvertFormat&quot;,
    &quot;input&quot;: {
        &quot;original_model_task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;,
        &quot;format&quot;: &quot;FBX&quot;
    },
    &quot;parameters&quot;: {
        &quot;quad&quot;: true,
        &quot;face_limit&quot;: 5000,
        &quot;fbx_preset&quot;: &quot;blender&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tcf285h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="tcf401h3stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：格式转换通常需要10~30秒，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../model-api-reference/more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="tcf424h4qr01"></a><h4>请求参数</h4><a id="tcf434h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="tcf440h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tcf448h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含转换后的3D模型URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong><code>array</code></p><p>转换结果列表。仅在 task_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>model_url</strong> <code>string</code></p><p>转换后3D模型的URL。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。仅在任务成功时返回，任务失败时不返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>3d_task_type</strong> <code>string</code></p><p>任务类型。格式转换固定为<code>convert-3d-format</code>。</p><p><strong>credits_consumed</strong> <code>integer</code></p><p>本次任务消耗的积分，等于<code>convert_level</code>。</p><p><strong>convert_level</strong> <code>integer</code></p><p>格式转换消耗的积分，按转换复杂度（基础转换或高级转换）计算。判定条件见<a href="#tcf801h2bill">计费与参数说明</a>。</p></div></section></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;cc451f5a-fdd7-9d9e-a3a9-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;2ea046a6-d7bd-4c26-af70-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-10-21 12:59:21.869&quot;,
        &quot;scheduled_time&quot;: &quot;2026-10-21 12:59:21.908&quot;,
        &quot;end_time&quot;: &quot;2026-10-21 12:59:30.384&quot;,
        &quot;results&quot;: [
            {
                &quot;model_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/tripo_convert_xxxx.glb?auth_key=xxxx&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;3d_task_type&quot;: &quot;convert-3d-format&quot;,
        &quot;credits_consumed&quot;: 5,
        &quot;convert_level&quot;: 5
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
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

<a id="计费与参数说明"></a>

<a id="tcf801h2bill"></a>

## 计费与参数说明

-   **计费档位**：格式转换分为基础转换和高级转换两档计费，高级转换消耗更多积分。满足以下任一条件即按高级转换计费，均不满足时按基础转换计费。实际消耗的积分见查询结果中的`usage.convert_level`。
    -   `quad`为`true`
    -   `face_limit`为非`null`的值
    -   `flatten_bottom`为`true`
    -   `flatten_bottom_threshold`不为`0.01`
    -   `texture_size`不为`4096`
    -   `texture_format`不为`JPEG`
    -   `pivot_to_center_bottom`为`true`
    -   `scale_factor`不为`1.0`
-   **不支持的参数**：`smart_low_poly`（智能低模）是[Tripo-文生/图生3D模型](tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)接口的参数，格式转换接口不支持。如果请求中带了该参数（例如沿用生成任务的参数），会被忽略，不报错也不计费。
-   **未列出的参数**：除`smart_low_poly`外，传入本文未列出的参数将返回400错误（`InvalidParameter`）。

<a id="错误码"></a>

<a id="tcf901h2errc"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](../model-api-reference/preparations/error-code.md)进行解决。
