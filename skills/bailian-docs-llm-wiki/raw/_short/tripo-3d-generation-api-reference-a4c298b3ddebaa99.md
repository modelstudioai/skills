# Tripo-文生/图生3D模型

Tripo 3D模型生成支持文生3D模型、单图生3D模型和多图生3D模型。

**相关文档**：[使用指南](../model-user-guide/model-experience/image-and-video-generation/3d-model/tripo-3d-generation-guide.md)

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="前提条件"></a>

<a id="tp013a0h2scop"></a>

## 前提条件

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="tp101a0h2http"></a>

## HTTP调用

由于3D模型生成任务耗时较长，API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="tp111a0h3stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="tp123a0h4reqp"></a><h4>请求参数</h4><a id="tp142a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="tp154a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值：</p><ul><li><code>Tripo/Tripo-H3.1</code>：高精度3D模型生成，输出产物最高200万面。对应 Tripo 官方 API 版本 <code>v3.1-20260211</code>。</li><li><code>Tripo/Tripo-P1.0</code>：专业3D模型生成，输出产物最高2万面，速度更快。对应 Tripo 官方 API 版本 <code>P1-20260311</code>。</li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入信息。<code>prompt</code>、<code>image</code>、<code>images</code> 三者互斥，仅能选择其中一种输入方式。同时传入多个将会报错。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （条件必填）</p><p>文本提示词，用于描述期望生成的3D模型。<strong>仅在文生3D模型时必填。</strong></p><p>支持多语言（中文、英文等），每个字符（含中文汉字、英文字母等）均计为1个字符，最大长度1024个字符。</p><p>示例值：一只可爱的猫。</p><p><strong>image</strong> <code>string</code> （条件必填）</p><p>单张图像的URL。<strong>仅在单图生3D模型时必填。</strong></p><p>图像限制：</p><ul><li>格式：JPEG、PNG。</li><li>分辨率：宽和高的范围为[20, 6000]像素，建议边长大于256像素。</li><li>文件大小：不超过20MB。</li></ul><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<code>https://xxx/xxx.jpg</code>。</li></ul><p><strong>images</strong> <code>array[object]</code> （条件必填）</p><p>多张图像的对象列表。<strong>仅在多图生3D模型时必填。</strong></p><p>数组长度固定为4，对应图片顺序为<strong>前、左、后、右</strong>。</p><ul><li>某个视角不需要图片时传入空对象<code>{}</code>；前视角（第1个元素）必须传入图片，有效图片数量为2~4张。</li><li>每张图像的限制与<code>image</code>参数相同，分辨率和宽高比不要求一致。</li><li>建议所有图像为同一物体在一致光照下的不同视角，多视角输入可提高几何精度和贴图覆盖度。</li></ul><p>每个图像对象包含以下字段：</p><ul><li><code>type</code>：图像格式，可选值为<code>jpeg</code>或<code>png</code>。</li><li><code>file_token</code>：图像的公网URL。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>3D模型生成参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>texture_quality</strong> <code>string</code> （可选）</p><p>贴图质量。贴图是覆盖在3D模型表面的纹理图像，决定了模型的外观细节和视觉效果。</p><p>可选值：</p><ul><li><code>standard</code>：默认值，标清贴图，兼顾质量与速度。</li><li><code>detailed</code>：高清贴图，保真度更高，生成速度较慢。</li><li><code>extreme</code>：8K贴图，保真度最高。</li></ul><p><strong>geometry_quality</strong> <code>string</code> （可选）</p><p>支持模型：<code>Tripo/Tripo-H3.1</code>。<code>Tripo/Tripo-P1.0</code>传入此参数会被忽略，不会报错。</p><p>几何精度。可选值：</p><ul><li><code>standard</code>：默认值，标准版，兼顾质量与速度。生成的3D模型最高150万面。</li><li><code>ultra</code>：超清版，几何细节更精细。生成的3D模型最高200万面。等同于 Tripo 官方 API 的<code>detailed</code>。</li></ul><p><strong>pbr</strong> <code>boolean</code> （可选）</p><p>是否生成PBR材质模型。PBR材质包含基础色（base_color）、金属度（metallic）、粗糙度（roughness）和法线（normal）贴图。默认值为<code>true</code>。</p><p>当<code>pbr</code>设为<code>true</code>时，会强制启用贴图（即<code>texture</code>也会被设为<code>true</code>），返回结果中包含<code>pbr_model_url</code>。</p><p><strong>texture</strong> <code>boolean</code> （可选）</p><p>是否生成贴图。默认值为<code>true</code>。</p><p>如需生成无贴图模型，需同时设置<code>texture</code>和<code>pbr</code>为<code>false</code>，返回结果中包含<code>base_model_url</code>。</p><p><strong>quad</strong> <code>boolean</code> （可选）</p><p>支持模型：<code>Tripo/Tripo-H3.1</code>。<code>Tripo/Tripo-P1.0</code>传入此参数会被忽略，不会报错。</p><p>是否输出四边面网格（而非三角面）。默认值为<code>false</code>。</p><p>开启后，输出格式强制为FBX；未设置<code>face_limit</code>时，默认面数为10,000。</p><p><strong>smart_low_poly</strong> <code>boolean</code> （可选）</p><p>支持模型：<code>Tripo/Tripo-H3.1</code>。<code>Tripo/Tripo-P1.0</code>传入此参数会被忽略，不会报错。</p><p>是否生成智能低模，即具有手工建模风格、拓扑干净的低面数模型。默认值为<code>false</code>。适合结构简单的输入，复杂模型可能偶尔生成失败。</p><p>开启后，<code>face_limit</code>的取值范围为：三角面500~20,000，四边面500~10,000。与<code>generate_parts</code>同时开启时，<code>generate_parts</code>不生效。</p><p><strong>generate_parts</strong> <code>boolean</code> （可选）</p><p>支持模型：<code>Tripo/Tripo-H3.1</code>。<code>Tripo/Tripo-P1.0</code>传入此参数会被忽略，不会报错。</p><p>是否生成可编辑的分割部件。默认值为<code>false</code>。</p><p>开启后，与以下参数不兼容：</p><ul><li><code>texture</code>、<code>pbr</code>：不传时二者默认按<code>false</code>处理。设置<code>texture</code>或<code>pbr</code>为<code>true</code>，或传入<code>texture_quality</code>时，返回400错误。</li><li><code>quad</code>：设置为<code>true</code>时会被忽略，返回的部件为三角面网格。</li><li><code>smart_low_poly</code>：同时开启时，<code>smart_low_poly</code>优先，不会生成部件。</li></ul><p>如需生成部件，<code>texture</code>和<code>pbr</code>可不传或设置为<code>false</code>，且不要传入<code>texture_quality</code>、<code>quad</code>和<code>smart_low_poly</code>。</p><p><strong>compress</strong> <code>string</code> （可选）</p><p>支持模型：<code>Tripo/Tripo-H3.1</code>。</p><p>压缩模式。不传则不压缩。可选值：</p><ul><li><code>geometry</code>：使用 meshopt 压缩几何数据，减小文件体积。</li></ul><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用于描述不希望在3D模型中出现的内容。最大长度255个字符。</p><p><strong>face_limit</strong> <code>integer</code> （可选）</p><p>生成的3D模型面数上限。不传时由模型自适应决定。取值范围：</p><ul><li><code>Tripo/Tripo-H3.1</code>：三角面不超过1,500,000（<code>geometry_quality</code>为<code>ultra</code>时不超过2,000,000）；四边面（<code>quad</code>为<code>true</code>）不超过150,000。未开启<code>smart_low_poly</code>时建议不低于500，需要更低面数时请开启<code>smart_low_poly</code>或使用<a href="tripo-retopology-api-reference-41eecbead5b85b83.md">Tripo-重拓扑</a>。开启<code>smart_low_poly</code>时的取值范围见该参数说明。</li><li><code>Tripo/Tripo-P1.0</code>：50~20,000，超出范围返回400错误。</li></ul><p>建议值：游戏资产50,000~100,000，Web和移动端10,000~50,000。</p><p><strong>model_seed</strong> <code>integer</code> （可选）</p><p>几何体生成的随机种子。取值范围：-2147483648~2147483647。</p><p>使用相同种子和相同输入将生成相同的3D网格。不设置时每次使用随机种子。</p><p><strong>image_seed</strong> <code>integer</code> （可选）</p><p>图像生成环节的随机种子。取值范围：-2147483648~2147483647。</p><p>主要用于文生3D模型时根据提示词生成参考图。单图、多图生3D模型仅在开启<code>enable_image_autofix</code>，或<code>texture_quality</code>为<code>detailed</code>、<code>extreme</code>时生效，一般无需设置。</p><p><strong>texture_seed</strong> <code>integer</code> （可选）</p><p>贴图生成的随机种子。取值范围：-2147483648~2147483647。</p><p>使用相同种子将生成相同的贴图。不设置时每次使用随机种子。如需获取几何体相同、贴图不同的模型，请保持<code>model_seed</code>不变并更改<code>texture_seed</code>。</p><p><strong>texture_alignment</strong> <code>string</code> （可选）</p><p>贴图对齐方式。可选值：</p><ul><li><code>original_image</code>：默认值，优先匹配输入图像的颜色。</li><li><code>geometry</code>：优先匹配生成的几何体。</li></ul><p><strong>orientation</strong> <code>string</code> （可选）</p><p>模型朝向。仅当<code>texture</code>为<code>true</code>时生效。可选值：</p><ul><li><code>default</code>：默认值，自动朝向。</li><li><code>align_image</code>：将模型对齐至输入图像的视角。</li></ul><p><strong>export_orientation</strong> <code>string</code> （可选）</p><p>导出模型的朝向（前向轴）。可选值：</p><ul><li><code>+x</code>：默认值，X轴正方向朝前。</li><li><code>-x</code>：X轴负方向朝前。</li><li><code>+y</code>：Y轴正方向朝前。</li><li><code>-y</code>：Y轴负方向朝前。</li></ul><div><div><p><strong>说明</strong></p><ul><li>此参数仅作用于本次生成。如需将模型用于后续的贴图、绑定、重定向、格式转换等后处理任务，不建议设置此参数。</li><li>设置此参数后再进行后处理，可能因模型方向错误影响最终效果，但任务状态仍为<code>SUCCEEDED</code>，不会报错。</li><li>如计划对模型做后处理，建议不设置此参数，在最后一步通过格式转换调整朝向。</li></ul></div></div><p><strong>auto_size</strong> <code>boolean</code> （可选）</p><p>是否自动将模型缩放至真实世界尺寸。默认值为<code>false</code>。开启后模型尺寸以米为单位，适用于AR/VR或游戏引擎场景。</p><p><strong>export_uv</strong> <code>boolean</code> （可选）</p><p>是否在生成过程中进行UV展开。默认值为<code>true</code>。设为<code>false</code>可加快生成速度并减小文件体积，UV展开将在贴图阶段处理。</p><p><strong>enable_image_autofix</strong> <code>boolean</code> （可选）</p><p>是否自动修复输入图像。默认值为<code>false</code>。仅在单图生3D模型（传入<code>image</code>）时生效。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="文生3d模型-有贴图"></a><section><a id="文生3d模型-有贴图-h4"></a><h4>文生3D模型（有贴图）</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-P1.0&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只可爱的猫&quot;
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;standard&quot;
    }
}'
</code></pre></section><a id="单图生3d模型-有贴图"></a><section><a id="单图生3d模型-有贴图-h4"></a><h4>单图生3D模型（有贴图）</h4><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-P1.0&quot;,
    &quot;input&quot;: {
        &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/cfbxhg/tripo-single.jpg&quot;
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;standard&quot;
    }
}'
</code></pre></section><a id="单图生3d模型-h3-1超清"></a><section><a id="单图生3d模型-h3-1超清-h4"></a><h4>单图生3D模型（H3.1超清）</h4><p>仅<code>Tripo/Tripo-H3.1</code>支持<code>geometry_quality</code>和<code>quad</code>参数。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-H3.1&quot;,
    &quot;input&quot;: {
        &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/cfbxhg/tripo-single.jpg&quot;
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;detailed&quot;,
        &quot;geometry_quality&quot;: &quot;ultra&quot;,
        &quot;quad&quot;: true
    }
}'
</code></pre></section><a id="多图生3d模型-有贴图"></a><section><a id="多图生3d模型-有贴图-h4"></a><h4>多图生3D模型（有贴图）</h4><a id="code-block-4"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-P1.0&quot;,
    &quot;input&quot;: {
        &quot;images&quot;: [
            { &quot;type&quot;: &quot;png&quot;, &quot;file_token&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png&quot; },
            { &quot;type&quot;: &quot;png&quot;, &quot;file_token&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/slgluy/tripo-images-2.png&quot; },
            { &quot;type&quot;: &quot;png&quot;, &quot;file_token&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/zjqhyn/tripo-images-3.png&quot; },
            { &quot;type&quot;: &quot;png&quot;, &quot;file_token&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mqfzww/tripo-images-4.png&quot; }
        ]
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;standard&quot;
    }
}'
</code></pre></section><a id="多图生3d模型-传入2张图"></a><section><a id="多图生3d模型-传入2张图-h4"></a><h4>多图生3D模型（传入2张图）</h4><p>图片顺序为前、左、后、右，不需要的视角传入空对象<code>{}</code>即可。</p><a id="code-block-5"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-P1.0&quot;,
    &quot;input&quot;: {
        &quot;images&quot;: [
            { &quot;type&quot;: &quot;png&quot;, &quot;file_token&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png&quot; },
            {},
            { &quot;type&quot;: &quot;png&quot;, &quot;file_token&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/zjqhyn/tripo-images-3.png&quot; },
            {}
        ]
    },
    &quot;parameters&quot;: {
        &quot;texture_quality&quot;: &quot;standard&quot;
    }
}'
</code></pre></section><a id="无贴图生成"></a><section><a id="无贴图生成-h4"></a><h4>无贴图生成</h4><p>需同时将<code>texture</code>和<code>pbr</code>设为<code>false</code>。</p><a id="code-block-6"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;Tripo/Tripo-P1.0&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只可爱的猫&quot;
    },
    &quot;parameters&quot;: {
        &quot;texture&quot;: false,
        &quot;pbr&quot;: false
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tp285a0h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-7"></a><pre class="language-json"><code>{
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

<a id="tp401a0h3stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：3D模型生成通常需要30~120秒，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../model-api-reference/more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="tp424a0h4qr01"></a><h4>请求参数</h4><a id="tp434a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="tp440a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-9"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="tp448a0h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的3D模型URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong><code>array</code></p><p>生成结果列表。仅在 task_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>model_url</strong> <code>string</code></p><p>3D模型的URL。生成任务均返回。</p><p><strong>pbr_model_url</strong> <code>string</code></p><p>PBR材质模型的URL。未开启<code>quad</code>时为GLB格式，开启<code>quad</code>时为FBX格式。当<code>pbr</code>为<code>true</code>（默认）且未开启<code>generate_parts</code>时返回。<code>texture</code>为<code>true</code>、<code>pbr</code>为<code>false</code>时不返回，带贴图的模型通过<code>model_url</code>获取。</p><p><strong>base_model_url</strong> <code>string</code></p><p>无贴图基础模型的URL。未开启<code>quad</code>时为GLB格式，开启<code>quad</code>时为FBX格式。当请求参数中<code>texture</code>和<code>pbr</code>均为<code>false</code>时返回。</p><p><strong>rendered_image_url</strong> <code>string</code></p><p>3D模型预览渲染图的URL（1张）。</p><p><strong>generated_image_url</strong> <code>string</code></p><p>文生3D模型时，根据提示词生成的中间图像的URL。</p></div></section><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。仅在任务成功时返回，任务失败时不返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>3d_task_type</strong> <code>string</code></p><p>3D模型生成任务类型。枚举值：</p><ul><li><code>text-to-3d</code>：文生3D模型。</li><li><code>image-to-3d</code>：单图生3D模型。</li><li><code>multi-image-to-3d</code>：多图生3D模型。</li></ul><p><strong>credits_consumed</strong> <code>integer</code></p><p>本次任务消耗的积分。计算公式：</p><p><code>credits_consumed</code> = 基础项积分 + <code>texture_quality</code> + <code>geometry_quality</code> + <code>quad</code> + <code>smart_low_poly</code> + <code>generate_parts</code></p><ul><li>基础项积分由模型和任务类型决定，不单独返回。各计费项的积分请参见<a href="../model-user-guide/test-1/model-pricing.md#trp002a0h2001">模型调用价格</a>。</li><li>公式中的计费参数为<code>usage</code>中返回的积分增量，积分增量为0的计费参数不返回，按0计算。</li></ul><p><strong>texture_quality</strong> <code>integer</code></p><p>生成贴图增加的积分，按贴图质量计算。生成贴图但未传<code>texture_quality</code>时（包括不传任何贴图参数），按<code>standard</code>计费。生成无贴图模型（<code>texture</code>和<code>pbr</code>均为<code>false</code>）时不返回。</p><p><strong>geometry_quality</strong> <code>integer</code></p><p>使用高精度几何增加的积分。仅<code>Tripo/Tripo-H3.1</code>且<code>geometry_quality</code>为<code>ultra</code>时返回。</p><p><strong>quad</strong> <code>integer</code></p><p>输出四边面网格增加的积分。仅<code>Tripo/Tripo-H3.1</code>开启<code>quad</code>时返回。</p><p><strong>smart_low_poly</strong> <code>integer</code></p><p>生成智能低模增加的积分。仅<code>Tripo/Tripo-H3.1</code>开启<code>smart_low_poly</code>时返回。</p><p><strong>generate_parts</strong> <code>integer</code></p><p>按部件生成增加的积分。仅<code>Tripo/Tripo-H3.1</code>开启<code>generate_parts</code>且生效时返回。</p></div></section></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;5fc8c4c2-f8b1-9ea2-bdda-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;ca51d54a-ffba-4ecc-8e42-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-10-16 16:39:53.349&quot;,
        &quot;scheduled_time&quot;: &quot;2026-10-16 16:39:53.388&quot;,
        &quot;end_time&quot;: &quot;2026-10-16 16:41:36.379&quot;,
        &quot;results&quot;: [
            {
                &quot;rendered_image_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/legacy_mesh.webp?auth_key=xxxx&quot;,
                &quot;model_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/tripo_base_model_xxxx.glb?auth_key=xxxx&quot;,
                &quot;generated_image_url&quot;: &quot;https://openapi.cdn.tripo3d.com/xxxx/text2image_xxxx.jpeg?auth_key=xxxx&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;3d_task_type&quot;: &quot;text-to-3d&quot;,
        &quot;credits_consumed&quot;: 40,
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

<a id="0d0a562d05nkh"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](../model-api-reference/preparations/error-code.md)进行解决。
