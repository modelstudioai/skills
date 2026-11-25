# 千问-图像生成与编辑 API参考

千问-图像生成与编辑模型同时支持文生图（T2I）和图生图/图像编辑（I2I），可根据文本提示词直接生成图像，也可基于参考图结合编辑指令进行精确编辑。支持通过OpenAI 兼容或DashScope协议调用。

<a id="模型概览"></a>

<a id="6740266-model-title"></a>

## 模型概览

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型简介</strong></p></th><th><p><strong>输出图像规格</strong></p></th></tr></thead><tbody><tr><td><p>qwen-image-3.0-pro</p></td><td><p>千问图像生成与编辑3.0 Pro系列，同时支持文生图（T2I）和图生图/图像编辑（I2I）。</p></td><td rowspan="4"><p>图像分辨率：</p><ul><li><p><strong>文生图（T2I）</strong>：总像素需在512*512至2048*2048之间。</p></li><li><p><strong>图生图（I2I）</strong>：总像素需在512*512至2048*2048之间。</p></li><li><p><strong>默认</strong>：不指定<code>size</code>时，模型根据提示词自动推荐分辨率。</p></li></ul><p>图像格式：png</p></td></tr><tr><td><p>qwen-image-3.0</p></td><td><p>千问图像生成与编辑3.0标准模型，同时支持文生图（T2I）和图生图/图像编辑（I2I），兼顾质量与速度。</p></td></tr><tr><td><p>qwen-image-2.1-pro</p></td><td><p>千问图像生成与编辑2.1 Pro模型，图生图/图像编辑（I2I）支持传入最多10张参考图，且能够根据提示词描述自动决定输出普通图像还是带有透明通道的图像。</p></td></tr><tr><td><p>qwen-image-2.1-turbo</p></td><td><p>千问图像生成与编辑2.1 Turbo模型，是目前Qwen-Image系列中综合表现与性价比最优的模型，图生图/图像编辑（I2I）支持传入最多10张参考图，且能够根据提示词描述自动决定输出普通图像还是带有透明通道的图像。</p></td></tr></tbody></table>

<a id="适用范围"></a>

<a id="hh01scope-title"></a>

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](../../../model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：获取该地域的[API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。

> **说明**
>
> 本文的示例代码适用于**华北2（北京）地域**。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="接入方式"></a>

<a id="6740266-access-title"></a>

## 接入方式

千问-图像生成与编辑提供三种接入方式，模型能力一致，请根据业务情况选择：

| 接入方式 | 适用场景 |
| --- | --- |
| [OpenAI 兼容](qwen-image-generation-and-editing-api-reference.md#6740266-openai-title) | 已基于 OpenAI Images 协议或 OpenAI SDK 开发的应用，只需切换`base_url`和`model`即可接入。仅支持同步调用，图像输入支持公网 URL 和 Base64。 |
| [DashScope同步调用](qwen-image-generation-and-editing-api-reference.md#6740266-sync-title) | 推荐方式，功能最完整，支持公网 URL 和 Base64 两种图像输入。 |
| [DashScope异步调用](qwen-image-generation-and-editing-api-reference.md#6740266-async-title) | 批量生成或不希望长时间占用连接的场景。提交任务后通过`task_id`轮询结果。 |

<a id="openai-兼容"></a>

<a id="6740266-openai-title"></a>

## OpenAI 兼容

如果您的应用已基于 OpenAI Images 协议或 OpenAI SDK 开发，可通过 OpenAI 兼容模式调用千问-图像生成与编辑，无需改造请求结构。文生图（T2I）与图生图/图像编辑（I2I）共用同一个接口：**不传**`image`**为文生图，传**`image`**为图生图**。

> **说明**
>
> OpenAI 兼容模式为**同步、非流式**接口，图生图通过`/images/generations`接口的扩展字段`image`实现，**不使用**OpenAI 官方`/images/edits`的 multipart 文件上传形式。以下能力暂不支持：异步调用、流式输出、partial image、`/images/edits`、multipart 与 mask。如需异步调用，请使用[DashScope异步调用](qwen-image-generation-and-editing-api-reference.md#6740266-async-title)。

<a id="url"></a>

<a id="6740266-openai-url-title"></a>

### URL

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

HTTP请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/images/generations`

SDK调用配置的base\_url：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

HTTP请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/images/generations`

SDK调用配置的base\_url：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

HTTP请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/images/generations`

SDK调用配置的base\_url：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

HTTP请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/images/generations`

SDK调用配置的base\_url：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

HTTP请求地址：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1/images/generations`

SDK调用配置的base\_url：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="6740266-openai-req-params-title"></a><h3>请求参数</h3><a id="6740266-openai-headers-h4"></a><h4>请求头（Headers）</h4><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="6740266-openai-body-h4"></a><h4>请求体（Request Body）</h4><p>与DashScope协议不同，OpenAI 兼容模式的所有参数<strong>平铺在请求体顶层</strong>，没有<code>input</code>和<code>parameters</code>嵌套结构。</p><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，可选值为<code>qwen-image-3.0-pro</code>、<code>qwen-image-3.0</code>、<code>qwen-image-2.1-pro</code>和<code>qwen-image-2.1-turbo</code>。</p><p><strong>response_format</strong> <code>string</code> （可选）</p><p>输出图像的返回格式。默认值为 <code>url</code>，可选值：</p><ul><li><code>url</code>：通过 <code>data[].url</code> 返回图像临时签名 URL。</li><li><code>b64_json</code>：通过 <code>data[].b64_json</code> 返回图像的 Base64 编码数据，不返回图像临时签名 URL。</li></ul><p><code>b64_json</code> 仅支持 <code>qwen-image-3.0</code> 和 <code>qwen-image-3.0-pro</code> 的同步调用。</p><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>正向提示词，用于描述您期望生成或编辑的图像内容、风格和构图。支持中英文，推荐不超过4500Token。不能为空字符串。</p><p><strong>image</strong> <code>string</code><strong> 或 </strong><code>array</code> （可选）</p><p>输入图像的 URL 或 Base64 编码数据。不传此参数为文生图（T2I）；传入此参数为图生图（I2I），qwen-image-2.1系列支持传入1-10张图像，qwen-image-3.0系列支持传入1-3张图像。单张图像可直接传字符串，多张图像传字符串数组，按数组顺序定义图像顺序。</p><p><strong>注意</strong>：不能传入<code>null</code>或空数组，否则将返回400错误。</p><strong>图像要求：</strong><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP和GIF。</li><li>图像分辨率：宽和高须在1至8000像素之间，超过将返回400错误；建议在384至2048像素之间以获得最佳效果。</li><li>图像宽高比：长边与短边之比不超过10:1。</li><li>图像大小：不超过10MB。</li></ul><strong>支持的输入格式</strong><ol><li>公网URL：支持 HTTP 和 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</li><li>Base64 编码：格式为<code>data:{MIME_type};base64,{base64_data}</code>。</li></ol><p><strong>n</strong> <code>integer</code> （可选）</p><p>输出图像的数量，支持输出1-6张图片，默认值为1。必须传入整数，传入字符串形式（如<code>&quot;1&quot;</code>）将返回400错误。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>设置输出图像的分辨率，格式为<code>宽x高</code>，例如<code>&quot;1024x1024&quot;</code>，也可传入<code>auto</code>。未指定时由模型根据提示词自动推荐分辨率。</p><div><div><p><strong>警告</strong>OpenAI 协议使用<strong>字母</strong><code>x</code><strong>作为分隔符</strong>（<code>1024x1024</code>），与DashScope协议的星号<code>*</code>（<code>1024*1024</code>）不同，从DashScope迁移时请注意修改。</p></div></div><ul><li><strong>文生图（T2I）</strong>：像素面积范围512x512至2048x2048，宽高比限制1:8至8:1。</li><li><strong>图生图（I2I）</strong>：像素面积范围512x512至2048x2048，宽高比限制1:8至8:1。</li></ul><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。仅 qwen-image-3.0 系列支持此参数。</p><p><strong>seed</strong> <code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>，未传入时，服务会随机选择种子。固定种子可使生成结果相对稳定。</p><p><strong>prompt_extend</strong> <code>boolean</code> （可选）</p><p>是否开启提示词智能改写，默认值为 <code>true</code>（建议开启）。开启后，模型会按照<code>prompt_extend_mode</code>指定的方式优化正向提示词，对描述较简单的提示词效果提升明显。</p><p><strong>prompt_extend_mode</strong> <code>string</code> （可选）</p><p>提示词改写方式，默认值为<code>direct</code>。可选值：</p><ul><li><code>direct</code>：直接提示词增强（DPE），适用于大多数场景。T2I和I2I均支持。</li><li><code>agent</code>：智能体提示词增强（APE），提供更精细的改写效果。仅支持文生图（T2I），图生图（I2I）场景传入<code>agent</code>将返回400错误。</li></ul><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>是否开启思考模式，默认值为<code>true</code>。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。仅在 prompt_extend=true 时生效，适用于 Direct T2I、Direct I2I 和 Agent T2I，I2I Agent 暂不支持。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印，默认值为 <code>false</code>。</p><div><div><p><strong>说明</strong><code>image</code>、<code>negative_prompt</code>、<code>seed</code>、<code>prompt_extend</code>、<code>prompt_extend_mode</code>、<code>enable_thinking</code>、<code>watermark</code>为阿里云百炼扩展字段，不属于 OpenAI 官方参数。直接发送HTTP请求时放在请求体顶层即可；使用 OpenAI SDK 时需通过<code>extra_body</code>传入。</p></div></div></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-文生图-tab"></a>文生图<div><a id="code-code-group-文生图"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/images/generations' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-image-3.0-pro&quot;,
    &quot;prompt&quot;: &quot;画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。&quot;,
    &quot;size&quot;: &quot;1024x1024&quot;,
    &quot;n&quot;: 1,
    &quot;prompt_extend&quot;: true
}'
</code></pre></div><a id="fig-code-group-图生图-tab"></a>图生图<div><a id="code-code-group-图生图"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/images/generations' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-image-3.0-pro&quot;,
    &quot;prompt&quot;: &quot;帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物脱下原本的米色针织上衣，换上一套彰显高雅气质的都市职场穿搭，身穿一件质感垂顺的香槟色真丝衬衫，外搭一件剪裁利落的深灰色休闲西装外套，下身搭配同色系的高腰阔腿裤，整体造型既干练又富有女人味。场景设定在一家装修现代简约的高端咖啡店内，背景是通透的落地玻璃窗，窗外隐约可见繁华的城市街景，室内摆放着深色实木长桌和舒适的皮质座椅，桌面上放置着一台打开的银色笔记本电脑、一份文件和一杯热气腾腾的美式咖啡。人物呈现出慵懒而放松的办公姿态，身体微微后仰倚靠在椅背上，一只手臂自然搭在扶手上，另一只手轻轻握着咖啡杯置于桌边，头部微侧，眼神清澈从容且带有一丝慵懒地直视镜头，嘴角挂着一抹优雅自信的微笑。人物化着精致得体的正式场合妆容，底妆清透干净，眉眼线条清晰利落，唇部涂抹着显气色的豆沙色口红，展现出成熟知性的魅力。光线采用午后柔和的自然光，从侧面透过落地窗洒入，在人物的面部轮廓和衣物褶皱上留下细腻的光影过渡，背景呈现自然的景深虚化效果，色彩以大地色、灰色和暖白色为主调，营造出宁静、高级且充满故事感的都市办公氛围，构图采用经典的竖幅七分身人像视角，人物位于画面视觉中心略偏右，比例协调，画质清晰细腻。&quot;,
    &quot;image&quot;: &quot;https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png&quot;,
    &quot;size&quot;: &quot;1024x1024&quot;,
    &quot;n&quot;: 1,
    &quot;prompt_extend&quot;: true
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="6740266-openai-resp-title"></a><h3>响应参数</h3><p><strong>created</strong> <code>integer</code></p><p>响应创建时间的 Unix 时间戳（秒）。</p><p><strong>data</strong> <code>array</code></p><p>生成结果列表。传入<code>n</code>大于1时，数组内包含多个元素。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code></p><p><code>response_format=url</code>: 生成图像的 URL，格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p><p><strong>b64_json</strong> <code>string</code></p><p>图像的 Base64 编码数据。仅在 <code>response_format=b64_json</code> 时返回，不包含 <code>data:image/...;base64,</code> 前缀，可直接进行 Base64 解码。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>本次调用的资源使用情况，仅调用成功时返回。此处为<strong>图片输入/输出计量信息，不是 Token 用量</strong>。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><a id="sec-tabs-2"></a><section><a id="qwen-image-3-0-系列"></a><section><a id="qwen-image-3-0-系列-h4"></a><h4>qwen-image-3.0 系列</h4><p><strong>output_width</strong> <code>integer</code></p><p>最终输出图片的宽度（像素）。</p><p><strong>output_height</strong> <code>integer</code></p><p>最终输出图片的高度（像素）。</p><p><strong>input_image_count</strong> <code>integer</code></p><p>用户请求中输入图片的数量。文生图（T2I）时为0，图生图（I2I）按实际输入图片数返回。</p><p><strong>input_image_type</strong> <code>string</code></p><p>输入图片计量档位。按输出分辨率像素面积判断：面积≤2,250,000为<code>qima_input_1k</code>，面积&gt;2,250,000为<code>qima_input_2k</code>。</p><p><strong>output_image_count</strong> <code>integer</code></p><p>实际返回的输出图片数量。</p><p><strong>output_image_type</strong> <code>string</code></p><p>输出图片计量档位。按输出分辨率像素面积判断：面积≤2,250,000为<code>qima_output_1k</code>，面积&gt;2,250,000为<code>qima_output_2k</code>。</p></section><a id="qwen-image-2-1系列"></a><section><a id="qwen-image-2-1系列-h4"></a><h4>qwen-image-2.1系列</h4><p><strong>image_count</strong> <code>integer</code></p><p>模型生成图像的数量。</p><p><strong>width</strong> <code>integer</code></p><p>模型生成图像的宽度（像素）。</p><p><strong>height</strong> <code>integer</code></p><p>模型生成图像的高度（像素）。</p></section></section></div></section><p><strong>error</strong> <code>object</code></p><p>错误信息，仅调用失败时返回。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>message</strong> <code>string</code></p><p>请求失败的详细信息。</p><p><strong>type</strong> <code>string</code></p><p>错误类型，如<code>invalid_request_error</code>。</p><p><strong>param</strong> <code>string</code></p><p>出错的参数名，无法定位到具体参数时为<code>null</code>。</p><p><strong>code</strong> <code>string</code></p><p>请求失败的错误码。详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><div><div><p><strong>说明</strong>与DashScope协议不同，OpenAI 兼容模式<strong>不在响应体中返回</strong><code>request_id</code>，请求唯一标识通过HTTP响应头<code>x-request-id</code>返回。使用 OpenAI Python SDK 时，成功响应可读取<code>response._request_id</code>，失败时可从<code>APIStatusError.request_id</code>读取。反馈问题时请提供该标识。</p></div></div></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>图像URL仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-qwen-image-3-0-系列-tab"></a>qwen-image-3.0 系列<div><a id="code-code-group-2-qwen-image-3-0-系列"></a><pre class="language-json"><code>{
    &quot;created&quot;: 1788339600,
    &quot;data&quot;: [
        {
            &quot;url&quot;: &quot;https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx&quot;
        }
    ],
    &quot;usage&quot;: {
        &quot;output_height&quot;: 1024,
        &quot;output_width&quot;: 1024,
        &quot;input_image_count&quot;: 0,
        &quot;input_image_type&quot;: &quot;qima_input_1k&quot;,
        &quot;output_image_count&quot;: 1,
        &quot;output_image_type&quot;: &quot;qima_output_1k&quot;
    }
}
</code></pre></div><a id="fig-code-group-2-qwen-image-2-1系列-tab"></a>qwen-image-2.1系列<div><a id="code-code-group-2-qwen-image-2-1系列"></a><pre class="language-json"><code>{
    &quot;created&quot;: 1788339600,
    &quot;data&quot;: [
        {
            &quot;url&quot;: &quot;https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx&quot;
        }
    ],
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1,
        &quot;width&quot;: 1024,
        &quot;height&quot;: 1024
    }
}
</code></pre></div></div></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回<code>error</code>对象，可以通过<code>code</code>和<code>message</code>字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;error&quot;: {
        &quot;message&quot;: &quot;Field 'prompt' is required&quot;,
        &quot;type&quot;: &quot;invalid_request_error&quot;,
        &quot;param&quot;: null,
        &quot;code&quot;: &quot;InvalidParameter&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="sdk调用"></a>

<a id="6740266-openai-sdk-title"></a>

### SDK调用

请先安装或升级 OpenAI Python SDK：

<a id="code-block-2"></a>

```bash
pip install -U openai
```

> **重要**
>
> 图像生成耗时较长，请显式设置足够大的客户端超时时间。多图输出（较大的`n`）或并发场景建议从600秒起配置，避免客户端提前断开。

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-文生图-tab"></a>

文生图

<a id="code-code-group-3-文生图"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    timeout=600.0,
)

response = client.images.generate(
    model="qwen-image-3.0-pro",
    prompt="画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。",
    size="1024x1024",
    n=1,
    # 以上均为OpenAI官方参数。image、prompt_extend等扩展字段需通过extra_body传入，参见图生图示例
)

for item in response.data:
    print(item.url)
print(f"request_id: {response._request_id}")
```

<a id="fig-code-group-3-图生图-tab"></a>

图生图

<a id="code-code-group-3-图生图"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    timeout=600.0,
)

response = client.images.generate(
    model="qwen-image-3.0-pro",
    prompt="帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物换上一套彰显高雅气质的都市职场穿搭，场景设定在一家装修现代简约的高端咖啡店内。",
    size="1024x1024",
    n=1,
    extra_body={
        # 单张图像也可直接传字符串；也支持Base64：data:{MIME_type};base64,{base64_data}
        "image": [
            "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png"
        ],
        "prompt_extend": True,
    },
)

for item in response.data:
    print(item.url)
print(f"request_id: {response._request_id}")
```

<a id="fig-code-group-3-读取request-id-tab"></a>

读取request\_id

<a id="code-code-group-3-读取request-id"></a>

```python
import os
from openai import OpenAI, APIStatusError

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    timeout=600.0,
)

try:
    response = client.images.generate(
        model="qwen-image-3.0-pro",
        prompt="画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。",
    )
    print(response.data[0].url)
except APIStatusError as exc:
    print(f"status_code: {exc.status_code}")
    print(f"request_id: {exc.request_id}")
    print(exc)
```

<a id="dashscope同步调用-推荐"></a>

<a id="6740266-sync-title"></a>

## DashScope同步调用（推荐）

<a id="http调用"></a>

<a id="6740266-http-title"></a>

### HTTP调用

<a id="sec-tabs-4"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<a id="日本-东京-2"></a>

<a id="日本-东京-2-h4"></a>

#### 日本（东京）

`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="6740266-req-params-h4"></a><h4>请求参数</h4><a id="6740266-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="6740266-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，可选值为<code>qwen-image-3.0-pro</code>、<code>qwen-image-3.0</code>、<code>qwen-image-2.1-pro</code>和<code>qwen-image-2.1-turbo</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。<strong>当前仅支持单轮对话</strong>，因此数组内<strong>有且只有一个对象</strong>，该对象包含<code>role</code>和<code>content</code>两个属性。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息发送者角色，必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组，根据使用场景有不同的组合方式：</p><ul><li><strong>文生图（T2I）</strong>：仅包含一个<code>{&quot;text&quot;: &quot;...&quot;}</code>对象。</li><li><strong>图生图（I2I）</strong>：qwen-image-2.1系列包含1-10个<code>{&quot;image&quot;: &quot;...&quot;}</code>对象，qwen-image-3.0系列包含1-3个，以及1个<code>{&quot;text&quot;: &quot;...&quot;}</code>对象。</li></ul><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code> （可选）</p><p>输入图像的 URL 或 Base64 编码数据。I2I场景下，qwen-image-2.1系列支持传入1-10张图像，qwen-image-3.0系列支持传入1-3张图像。多图输入时，按照数组顺序定义图像顺序。</p><strong>图像要求：</strong><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP和GIF。</li><li>图像分辨率：宽和高须在1至8000像素之间，超过将返回400错误；建议在384至2048像素之间以获得最佳效果。</li><li>图像宽高比：长边与短边之比不超过10:1。</li><li>图像大小：不超过10MB。</li></ul><strong>支持的输入格式</strong><ol><li>公网URL：支持 HTTP 和 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</li><li>Base64 编码：格式为<code>data:{MIME_type};base64,{base64_data}</code>。</li></ol><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词，用于描述您期望生成或编辑的图像内容、风格和构图。支持中英文，推荐不超过4500Token。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>控制图像生成的附加参数。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>response_format</strong> <code>string</code> （可选）</p><p>输出图像的返回格式。默认值为 <code>url</code>，可选值：</p><ul><li><code>url</code>：通过 <code>output.choices[].message.content[].image</code> 返回图像临时签名 URL。</li><li><code>b64_json</code>：通过 <code>output.choices[].message.content[].image</code> 返回图像的 Data URL，包含 MIME 类型和 Base64 编码数据，不返回图像临时签名 URL。</li></ul><p><code>b64_json</code> 仅支持 <code>qwen-image-3.0</code> 和 <code>qwen-image-3.0-pro</code> 的同步调用。异步调用设置 <code>parameters.response_format=&quot;b64_json&quot;</code> 时，任务失败，错误码为 <code>InvalidParameter</code>。</p><p><strong>prompt_extend</strong> <code>boolean</code> （可选）</p><p>是否开启提示词智能改写，默认值为 <code>true</code>（建议开启）。开启后，模型会按照<code>prompt_extend_mode</code>指定的方式优化正向提示词，对描述较简单的提示词效果提升明显。</p><p><strong>prompt_extend_mode</strong> <code>string</code> （可选）</p><p>提示词改写方式，默认值为<code>direct</code>。可选值：</p><ul><li><code>direct</code>：直接提示词增强（DPE），适用于大多数场景。T2I和I2I均支持。</li><li><code>agent</code>：智能体提示词增强（APE），提供更精细的改写效果。仅支持文生图（T2I），图生图（I2I）场景传入<code>agent</code>将返回400错误。</li></ul><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>是否开启思考模式，默认值为<code>true</code>。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。仅在 prompt_extend=true 时生效，适用于 Direct T2I、Direct I2I 和 Agent T2I，I2I Agent 暂不支持。</p><p><strong>n</strong> <code>integer</code> （可选）</p><p>输出图像的数量，支持输出1-6张图片，默认值为1。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>设置输出图像的分辨率，格式为<code>宽*高</code>，例如<code>&quot;1024*1024&quot;</code>。未指定时由模型根据提示词自动推荐分辨率。</p><ul><li><strong>文生图（T2I）</strong>：像素面积范围512*512至2048*2048，宽高比限制1:8至8:1。</li><li><strong>图生图（I2I）</strong>：像素面积范围512*512至2048*2048，宽高比限制1:8至8:1。</li></ul><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。仅 qwen-image-3.0 系列支持此参数。</p><p><strong>seed</strong> <code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>，未传入时，服务会随机选择种子。固定种子可使生成结果相对稳定。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印，默认值为 <code>false</code>。</p></div></section></td><td><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-文生图-tab"></a>文生图<div><a id="code-code-group-4-文生图"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-image-3.0-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-4-图生图-tab"></a>图生图<div><a id="code-code-group-4-图生图"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-image-3.0-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;image&quot;: &quot;https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png&quot;
                    },
                    {
                        &quot;text&quot;: &quot;帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物脱下原本的米色针织上衣，换上一套彰显高雅气质的都市职场穿搭，身穿一件质感垂顺的香槟色真丝衬衫，外搭一件剪裁利落的深灰色休闲西装外套，下身搭配同色系的高腰阔腿裤，整体造型既干练又富有女人味。场景设定在一家装修现代简约的高端咖啡店内，背景是通透的落地玻璃窗，窗外隐约可见繁华的城市街景，室内摆放着深色实木长桌和舒适的皮质座椅，桌面上放置着一台打开的银色笔记本电脑、一份文件和一杯热气腾腾的美式咖啡。人物呈现出慵懒而放松的办公姿态，身体微微后仰倚靠在椅背上，一只手臂自然搭在扶手上，另一只手轻轻握着咖啡杯置于桌边，头部微侧，眼神清澈从容且带有一丝慵懒地直视镜头，嘴角挂着一抹优雅自信的微笑。人物化着精致得体的正式场合妆容，底妆清透干净，眉眼线条清晰利落，唇部涂抹着显气色的豆沙色口红，展现出成熟知性的魅力。光线采用午后柔和的自然光，从侧面透过落地窗洒入，在人物的面部轮廓和衣物褶皱上留下细腻的光影过渡，背景呈现自然的景深虚化效果，色彩以大地色、灰色和暖白色为主调，营造出宁静、高级且充满故事感的都市办公氛围，构图采用经典的竖幅七分身人像视角，人物位于画面视觉中心略偏右，比例协调，画质清晰细腻。&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="6740266-resp-h4"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>包含模型生成结果。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>rewrite_status</strong> <code>string</code></p><p>提示词改写状态，具体取值由请求是否开启改写以及改写执行结果决定。</p><p><strong>choices</strong> <code>array</code></p><p>结果选项列表。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><p>消息内容，包含生成的图像信息。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code></p><p><code>response_format=url</code>: 生成图像的 URL，格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p><p><code>response_format=b64_json</code>：返回图像的 Data URL，格式为 <code>data:{MIME_type};base64,{base64_data}</code>，例如 <code>data:image/png;base64,...</code>。MIME 类型取决于实际图像格式。解码时，提取第一个逗号后的 Base64 编码数据。</p></div></section></div></section></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>本次调用的资源使用情况，仅调用成功时返回。此处为<strong>图片输入/输出计量信息，不是 Token 用量</strong>。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><a id="sec-tabs-5"></a><section><a id="qwen-image-3-0-系列-2"></a><section><a id="qwen-image-3-0-系列-2-h4"></a><h4>qwen-image-3.0 系列</h4><p><strong>output_width</strong> <code>integer</code></p><p>最终输出图片的宽度（像素）。</p><p><strong>output_height</strong> <code>integer</code></p><p>最终输出图片的高度（像素）。</p><p><strong>input_image_count</strong> <code>integer</code></p><p>用户请求中输入图片的数量。文生图（T2I）时为0，图生图（I2I）按实际输入图片数返回。</p><p><strong>input_image_type</strong> <code>string</code></p><p>输入图片计量档位。按输出分辨率像素面积判断：面积≤2,250,000为<code>qima_input_1k</code>，面积&gt;2,250,000为<code>qima_input_2k</code>。</p><p><strong>output_image_count</strong> <code>integer</code></p><p>实际返回的输出图片数量。</p><p><strong>output_image_type</strong> <code>string</code></p><p>输出图片计量档位。按输出分辨率像素面积判断：面积≤2,250,000为<code>qima_output_1k</code>，面积&gt;2,250,000为<code>qima_output_2k</code>。</p></section><a id="qwen-image-2-1系列-2"></a><section><a id="qwen-image-2-1系列-2-h4"></a><h4>qwen-image-2.1系列</h4><p><strong>image_count</strong> <code>integer</code></p><p>模型生成图像的数量。</p><p><strong>width</strong> <code>integer</code></p><p>模型生成图像的宽度（像素）。</p><p><strong>height</strong> <code>integer</code></p><p>模型生成图像的高度（像素）。</p></section></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功-2"></a><section><a id="任务执行成功-2-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-qwen-image-3-0-系列-tab"></a>qwen-image-3.0 系列<div><a id="code-code-group-5-qwen-image-3-0-系列"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx&quot;
                        }
                    ],
                    &quot;role&quot;: &quot;assistant&quot;
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;output_height&quot;: 1024,
        &quot;output_width&quot;: 1024,
        &quot;input_image_count&quot;: 0,
        &quot;input_image_type&quot;: &quot;qima_input_1k&quot;,
        &quot;output_image_count&quot;: 1,
        &quot;output_image_type&quot;: &quot;qima_output_1k&quot;
    },
    &quot;request_id&quot;: &quot;571ae02f-5c9d-436c-83c2-f221e6df0xxx&quot;
}
</code></pre></div><a id="fig-code-group-5-qwen-image-2-1系列-tab"></a>qwen-image-2.1系列<div><a id="code-code-group-5-qwen-image-2-1系列"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx&quot;
                        }
                    ],
                    &quot;role&quot;: &quot;assistant&quot;
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1,
        &quot;width&quot;: 1024,
        &quot;height&quot;: 1024
    },
    &quot;request_id&quot;: &quot;571ae02f-5c9d-436c-83c2-f221e6df0xxx&quot;
}
</code></pre></div></div></section><a id="任务执行异常-2"></a><section><a id="任务执行异常-2-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;31f808fd-8eef-9004-xxxxx&quot;,
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;Invalid API-key provided.&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="sdk调用-2"></a>

<a id="6740266-sdk-title"></a>

### SDK调用

以下以图生图/图像编辑（I2I）为示例，展示Python和Java SDK的调用方式。

<a id="fig-code-group-6"></a>

<a id="fig-code-group-6-python-tab"></a>

Python

<a id="code-code-group-6-python"></a>

```python
import os
import base64
import mimetypes
import dashscope
from dashscope import MultiModalConversation

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Unsupported or unrecognized image format")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# [方法一] 使用公网图像URL
image_url = "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png"

# [方法二] 使用Base64编码图像
# image_url = encode_file("./your_image.png")

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-image-3.0-pro",
    messages=[{
        "role": "user",
        "content": [
            {"image": image_url},
            {"text": "帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物换上一套彰显高雅气质的都市职场穿搭，场景设定在一家装修现代简约的高端咖啡店内。"}
        ]
    }],
    prompt_extend=True
)

print(response)
if response.status_code == 200:
    url = response.output.choices[0].message.content[0]["image"]
    print(f"Generated image URL: {url}")
else:
    print(f"Error: {response.code} - {response.message}")
```

<a id="fig-code-group-6-java-tab"></a>

Java

<a id="code-code-group-6-java"></a>

```java
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.utils.Constants;

public class ImageEditExample {
    public static void main(String[] args) {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";

        // [方法一] 使用公网图像URL
        String imageUrl = "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png";

        // [方法二] 使用Base64编码图像
        // String imageUrl = encodeFile("/path/to/your/image.png");

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
            .role(Role.USER.getValue())
            .content(Arrays.asList(
                Collections.singletonMap("image", imageUrl),
                Collections.singletonMap("text", "帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物换上一套彰显高雅气质的都市职场穿搭，场景设定在一家装修现代简约的高端咖啡店内。")
            ))
            .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen-image-3.0-pro")
            .messages(Arrays.asList(userMessage))
            .parameter("prompt_extend", true)
            .build();
        try {
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("File does not exist: " + filePath);
        }
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("Cannot detect file type: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("Unsupported or unrecognized image format");
        }
        byte[] fileBytes = null;
        try {
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("Cannot read file content: " + filePath);
        }
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }
}
```

<a id="dashscope异步调用"></a>

<a id="6740266-async-title"></a>

## DashScope异步调用

千问-图像生成与编辑模型除了支持上文的同步调用外，还支持异步调用。异步接口与同步接口共用相同的请求参数结构，仅需在请求头中增加`X-DashScope-Async: enable`，服务受理后返回任务ID（`task_id`），再通过任务ID轮询查询接口获取最终结果。

> **重要**
>
> 异步接口的请求地址与同步接口不同，请使用本节给出的Endpoint，不要沿用同步接口地址。

<a id="http调用-2"></a>

<a id="6740266-async-http-title"></a>

### HTTP调用

调用流程分为两步：

1.  **创建任务获取任务ID**：发送一个请求创建任务，该请求会返回**任务ID（task\_id）**。
2.  **根据任务ID查询结果**：使用task\_id轮询任务状态，直到任务完成并获得图像URL。

<a id="步骤1-创建任务获取任务id"></a>

<a id="6740266-async-step1-title"></a>

#### 步骤1：创建任务获取任务ID

<a id="sec-tabs-7"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<a id="美国-弗吉尼亚-3"></a>

<a id="美国-弗吉尼亚-3-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<a id="德国-法兰克福-3"></a>

<a id="德国-法兰克福-3-h4"></a>

#### 德国（法兰克福）

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<a id="日本-东京-3"></a>

<a id="日本-东京-3-h4"></a>

#### 日本（东京）

`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<a id="中国香港-2"></a>

<a id="中国香港-2-h4"></a>

#### 中国香港

`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<table><tbody><tr><td><a id="6740266-async-req-params-h5"></a><h5>请求参数</h5><a id="6740266-async-headers-h6"></a><h6>请求头（Headers）</h6><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。<strong>必须设置为</strong><code>enable</code>。本节的Endpoint仅受理异步请求，不支持同步调用。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="6740266-async-body-h6"></a><h6>请求体（Request Body）</h6><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，可选值为<code>qwen-image-3.0-pro</code>、<code>qwen-image-3.0</code>、<code>qwen-image-2.1-pro</code>和<code>qwen-image-2.1-turbo</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。<strong>当前仅支持单轮对话</strong>，因此数组内<strong>有且只有一个对象</strong>，该对象包含<code>role</code>和<code>content</code>两个属性。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息发送者角色，必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组，根据使用场景有不同的组合方式：</p><ul><li><strong>文生图（T2I）</strong>：仅包含一个<code>{&quot;text&quot;: &quot;...&quot;}</code>对象。</li><li><strong>图生图（I2I）</strong>：qwen-image-2.1系列包含1-10个<code>{&quot;image&quot;: &quot;...&quot;}</code>对象，qwen-image-3.0系列包含1-3个，以及1个<code>{&quot;text&quot;: &quot;...&quot;}</code>对象。</li></ul><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code> （可选）</p><p>输入图像的 URL 或 Base64 编码数据。I2I场景下，qwen-image-2.1系列支持传入1-10张图像，qwen-image-3.0系列支持传入1-3张图像。多图输入时，按照数组顺序定义图像顺序。</p><strong>图像要求：</strong><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP和GIF。</li><li>图像分辨率：宽和高须在1至8000像素之间，超过将返回400错误；建议在384至2048像素之间以获得最佳效果。</li><li>图像宽高比：长边与短边之比不超过10:1。</li><li>图像大小：不超过10MB。</li></ul><strong>支持的输入格式</strong><ol><li>公网URL：支持 HTTP 和 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</li><li>Base64 编码：格式为<code>data:{MIME_type};base64,{base64_data}</code>。</li></ol><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词，用于描述您期望生成或编辑的图像内容、风格和构图。支持中英文，推荐不超过4500Token。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>控制图像生成的附加参数。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>prompt_extend</strong> <code>boolean</code> （可选）</p><p>是否开启提示词智能改写，默认值为 <code>true</code>（建议开启）。开启后，模型会按照<code>prompt_extend_mode</code>指定的方式优化正向提示词，对描述较简单的提示词效果提升明显。</p><p><strong>prompt_extend_mode</strong> <code>string</code> （可选）</p><p>提示词改写方式，默认值为<code>direct</code>。可选值：</p><ul><li><code>direct</code>：直接提示词增强（DPE），适用于大多数场景。T2I和I2I均支持。</li><li><code>agent</code>：智能体提示词增强（APE），提供更精细的改写效果。仅支持文生图（T2I），图生图（I2I）场景传入<code>agent</code>将返回400错误。</li></ul><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>是否开启思考模式，默认值为<code>true</code>。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。仅在 prompt_extend=true 时生效，适用于 Direct T2I、Direct I2I 和 Agent T2I，I2I Agent 暂不支持。</p><p><strong>n</strong> <code>integer</code> （可选）</p><p>输出图像的数量，支持输出1-6张图片，默认值为1。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>设置输出图像的分辨率，格式为<code>宽*高</code>，例如<code>&quot;1024*1024&quot;</code>。未指定时由模型根据提示词自动推荐分辨率。</p><ul><li><strong>文生图（T2I）</strong>：像素面积范围512*512至2048*2048，宽高比限制1:8至8:1。</li><li><strong>图生图（I2I）</strong>：像素面积范围512*512至2048*2048，宽高比限制1:8至8:1。</li></ul><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。仅 qwen-image-3.0 系列支持此参数。</p><p><strong>seed</strong> <code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>，未传入时，服务会随机选择种子。固定种子可使生成结果相对稳定。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印，默认值为 <code>false</code>。</p></div></section></td><td><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-文生图-tab"></a>文生图<div><a id="code-code-group-7-文生图"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'X-DashScope-Async: enable' \
--data '{
    &quot;model&quot;: &quot;qwen-image-3.0-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-7-图生图-tab"></a>图生图<div><a id="code-code-group-7-图生图"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'X-DashScope-Async: enable' \
--data '{
    &quot;model&quot;: &quot;qwen-image-3.0-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;image&quot;: &quot;https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png&quot;
                    },
                    {
                        &quot;text&quot;: &quot;帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物脱下原本的米色针织上衣，换上一套彰显高雅气质的都市职场穿搭，身穿一件质感垂顺的香槟色真丝衬衫，外搭一件剪裁利落的深灰色休闲西装外套，下身搭配同色系的高腰阔腿裤，整体造型既干练又富有女人味。场景设定在一家装修现代简约的高端咖啡店内，背景是通透的落地玻璃窗，窗外隐约可见繁华的城市街景，室内摆放着深色实木长桌和舒适的皮质座椅，桌面上放置着一台打开的银色笔记本电脑、一份文件和一杯热气腾腾的美式咖啡。人物呈现出慵懒而放松的办公姿态，身体微微后仰倚靠在椅背上，一只手臂自然搭在扶手上，另一只手轻轻握着咖啡杯置于桌边，头部微侧，眼神清澈从容且带有一丝慵懒地直视镜头，嘴角挂着一抹优雅自信的微笑。人物化着精致得体的正式场合妆容，底妆清透干净，眉眼线条清晰利落，唇部涂抹着显气色的豆沙色口红，展现出成熟知性的魅力。光线采用午后柔和的自然光，从侧面透过落地窗洒入，在人物的面部轮廓和衣物褶皱上留下细腻的光影过渡，背景呈现自然的景深虚化效果，色彩以大地色、灰色和暖白色为主调，营造出宁静、高级且充满故事感的都市办公氛围，构图采用经典的竖幅七分身人像视角，人物位于画面视觉中心略偏右，比例协调，画质清晰细腻。&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="6740266-async-resp1-h5"></a><h5>响应参数</h5><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-8"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="6740266-async-step2-title"></a>

#### 步骤2：根据任务ID查询结果

<a id="sec-tabs-9"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="美国-弗吉尼亚-4"></a>

<a id="美国-弗吉尼亚-4-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="德国-法兰克福-4"></a>

<a id="德国-法兰克福-4-h4"></a>

#### 德国（法兰克福）

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="日本-东京-4"></a>

<a id="日本-东京-4-h4"></a>

#### 日本（东京）

`GET https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="中国香港-3"></a>

<a id="中国香港-3-h4"></a>

#### 中国香港

`GET https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/tasks/{task_id}`

必须使用提交任务时的地域、业务空间和API Key查询任务，不可跨地域或跨业务空间查询。

<table><tbody><tr><td><a id="6740266-async-step2-req-h5"></a><h5>请求参数</h5><a id="6740266-async-step2-headers-h6"></a><h6>请求头（Headers）</h6><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="6740266-async-step2-path-h6"></a><h6>URL路径参数（Path parameters）</h6><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-10"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="6740266-async-resp2-h5"></a><h5>响应参数</h5><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>rewrite_status</strong> <code>string</code></p><p>提示词改写状态，具体取值由请求是否开启改写以及改写执行结果决定。</p><p><strong>choices</strong> <code>array</code></p><p>结果选项列表。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><p>消息内容，包含生成的图像信息。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>本次调用的资源使用情况，仅调用成功时返回。此处为<strong>图片输入/输出计量信息，不是 Token 用量</strong>。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><a id="sec-tabs-11"></a><section><a id="qwen-image-3-0-系列-3"></a><section><a id="qwen-image-3-0-系列-3-h4"></a><h4>qwen-image-3.0 系列</h4><p><strong>output_width</strong> <code>integer</code></p><p>最终输出图片的宽度（像素）。</p><p><strong>output_height</strong> <code>integer</code></p><p>最终输出图片的高度（像素）。</p><p><strong>input_image_count</strong> <code>integer</code></p><p>用户请求中输入图片的数量。文生图（T2I）时为0，图生图（I2I）按实际输入图片数返回。</p><p><strong>input_image_type</strong> <code>string</code></p><p>输入图片计量档位。按输出分辨率像素面积判断：面积≤2,250,000为<code>qima_input_1k</code>，面积&gt;2,250,000为<code>qima_input_2k</code>。</p><p><strong>output_image_count</strong> <code>integer</code></p><p>实际返回的输出图片数量。</p><p><strong>output_image_type</strong> <code>string</code></p><p>输出图片计量档位。按输出分辨率像素面积判断：面积≤2,250,000为<code>qima_output_1k</code>，面积&gt;2,250,000为<code>qima_output_2k</code>。</p></section><a id="qwen-image-2-1系列-3"></a><section><a id="qwen-image-2-1系列-3-h4"></a><h4>qwen-image-2.1系列</h4><p><strong>image_count</strong> <code>integer</code></p><p>模型生成图像的数量。</p><p><strong>width</strong> <code>integer</code></p><p>模型生成图像的宽度（像素）。</p><p><strong>height</strong> <code>integer</code></p><p>模型生成图像的高度（像素）。</p></section></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-12"></a><section><a id="任务执行成功-3"></a><section><a id="任务执行成功-3-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-qwen-image-3-0-系列-tab"></a>qwen-image-3.0 系列<div><a id="code-code-group-8-qwen-image-3-0-系列"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;17d7d840-82b9-485b-a954-724d06bc88d2&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-08-07 15:50:14.837&quot;,
        &quot;scheduled_time&quot;: &quot;2026-08-07 15:50:14.884&quot;,
        &quot;end_time&quot;: &quot;2026-08-07 15:50:33.607&quot;,
        &quot;rewrite_status&quot;: &quot;not_use&quot;,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;output_height&quot;: 1024,
        &quot;output_width&quot;: 1024,
        &quot;input_image_count&quot;: 0,
        &quot;input_image_type&quot;: &quot;qima_input_1k&quot;,
        &quot;output_image_count&quot;: 1,
        &quot;output_image_type&quot;: &quot;qima_output_1k&quot;
    },
    &quot;request_id&quot;: &quot;2bd94002-5624-9129-916b-fbdde107b4ba&quot;
}
</code></pre></div><a id="fig-code-group-8-qwen-image-2-1系列-tab"></a>qwen-image-2.1系列<div><a id="code-code-group-8-qwen-image-2-1系列"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;17d7d840-82b9-485b-a954-724d06bc88d2&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-08-07 15:50:14.837&quot;,
        &quot;scheduled_time&quot;: &quot;2026-08-07 15:50:14.884&quot;,
        &quot;end_time&quot;: &quot;2026-08-07 15:50:33.607&quot;,
        &quot;rewrite_status&quot;: &quot;not_use&quot;,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1,
        &quot;width&quot;: 1024,
        &quot;height&quot;: 1024
    },
    &quot;request_id&quot;: &quot;2bd94002-5624-9129-916b-fbdde107b4ba&quot;
}
</code></pre></div></div></section><a id="任务执行异常-3"></a><section><a id="任务执行异常-3-h4"></a><h4>任务执行异常</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;17d7d840-82b9-485b-a954-724d06bc88d2&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InternalError&quot;,
        &quot;message&quot;: &quot;An internal error has occurred.&quot;
    },
    &quot;request_id&quot;: &quot;31f808fd-8eef-9004-xxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
