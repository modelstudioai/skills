# SubmitVideoAnalysisTask

阿里云百炼轻应用-提交视频理解离线异步任务。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

<a id="异步任务说明"></a>

### 异步任务说明

区别于在线同步接口，提交异步任务后实时返回，无需等待执行结束。任务由后台异步调度（排队、并行），结果可通过"获取异步任务状态和结果"接口查询。

<a id="接口调用说明"></a>

### 接口调用说明

-   支持绝大部分开发语言 SDK 方式接入
-   可在 OpenAPI 门户 直接调试和使用
-   也可前往 [轻应用-影视传媒视频理解控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)，切换到"API"页签查看调用 Demo

<a id="并发说明"></a>

### 并发说明

| 项目 | 说明 |
| --- | --- |
| 默认并发 | 2 并发（异步任务运行并发，非接口调用并发） |
| 可调上限 | 通过 `UpdateVideoAnalysisConfig` 配置接口可调整至 30 |
| 更高并发 | 业务量大可联系客服或运营申请更多并发 |
| 排队机制 | 并发数 = 后台同时运行的任务数，超过并发数的任务自动后台排队 |

<a id="角色识别说明"></a>

### 角色识别说明

-   通过 API 接口实现"识别视频中的人物身份"
-   **默认可识别**：16 个人物，每个角色 1 张图片
-   **放宽限制**：如需进一步放宽，请加入钉钉群 `116015001424` 联系产研
-   **超时风险**：一个视频理解任务中做太多次人物角色匹配，存在超时风险

<a id="调度轮询最佳实践"></a>

### 调度轮询最佳实践

因接口调用并发有限制，建议如下：

-   **扩并发**：扩的是异步处理任务的并发，非提交任务接口的并发
-   **提交任务**：理论串行即可。任务多时可适当 2~3 个并发提交
-   **结果轮询**：任务按提交顺序调度，只需周期轮询最早未完成的 top n（n == 异步任务并发数）即可。更多任务状态只会是排队中，轮询意义不大

<a id="agent-集成"></a>

### Agent 集成

Agent 可通过 Skill 直接使用视频理解能力：

-   **Skill 名称**：`alibabacloud-bailian-videoanalysis`
-   **Skill 地址**：[https://skills.aliyun.com/skills/alibabacloud-bailian-videoanalysis](https://skills.aliyun.com/skills/alibabacloud-bailian-videoanalysis)

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| quanmiaolightapp:SubmitVideoAnalysisTask | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/quanmiao/lightapp/videoAnalysis/submitVideoAnalysisTask HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 阿里云百炼业务空间唯一标识：[获取 workspaceId](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) | llm-xxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>videoUrl</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频 url</p></div></td><td><p><a href="http://xxxx.mp4">http://xxxx.mp4</a></p></td></tr><tr><td>videoModelId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频 vl 任务模型唯一标识，支持的模型：</p><ul><li><p>quanmiao-vl-turbo</p></li><li><p>quanmiao-vl-plus</p></li><li><p>quanmiao-vl-max-thinking</p></li><li><p>quanmiao-vl-max</p></li><li><p>Qwen-VL-Post</p></li></ul></div></td><td><p>quanmiao-vl-turbo</p></td></tr><tr><td>videoModelCustomPromptTemplate</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频 vl 任务 prompt 模版：必须包含{videoAsrText}变量，{videoAsrText}是视频的 ASR 文本信息，默认取页面看到的默认值。</p></div></td><td><p># 角色 你是一名视频分析师，擅长对各种视频片段进行理解。 # 任务描述 给你一个视频片段的多张关键帧图片，请你完成以下任务。 - 输出每张图片的画面信息，包括人物、物体、动作、文字、字幕、镜头语言等。 - 把每张图片的信息串联起来，生成视频的详细概述，还原该片段的剧情。 # 限制 - 分析范围严格限定于提供的视频子片段，不涉及视频之外的任何推测或背景信息。 - 总结时需严格依据视频内容，不可添加个人臆测或创意性内容。 - 保持对所有视频元素（尤其是文字和字幕）的高保真还原，避免信息遗漏或误解。 # 输入数据 ## 视频片段ASR信息 （如果输入为空则忽略ASR信息） {videoAsrText} # 输出格式 直接按照任务目标里即可,先输出每张图片的描述，再串联起来输出整个视频片段的剧情。</p></td></tr><tr><td>modelId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频总结（文本加工）依赖的大模型唯一标识，</p><p><strong>如果文本加工阶段想跑多任务</strong>，可以走 textProcessTasks 字段，如果传入了 textProcessTasks，则当前字段和当前字段对应的 prompt 模版 id，prompt 模版将不再生效。</p><ul><li><p>quanmiao-llm-max</p></li><li><p>quanmiao-llm-max-thinking</p></li><li><p>quanmiao-llm-plus</p></li><li><p>quanmiao-llm-turbo</p></li></ul></div></td><td><p>quanmiao-llm-max</p></td></tr><tr><td>modelCustomPromptTemplateId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频总结依赖的大模型 prompt 模版唯一标识：</p><ul><li><p>PlotDetail：剧情详解（默认）；</p></li><li><p>Summary：内容概述；</p></li><li><p>ExtractVideoTag：提取标签；</p></li><li><p>ExplosivePointAnalysis：爆点分析；</p></li><li><p>MultiTask：多类任务；</p></li></ul><p>如果 modelCustomPromptTemplate 未传，则会取模版唯一标识对应的默认 prompt，modelCustomPromptTemplate 优先级高于 modelCustomPromptTemplateId。</p></div></td><td><p>PlotDetail</p></td></tr><tr><td>modelCustomPromptTemplate</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频总结依赖的大模型 prompt 模版：必须同时包含{videoAsrText} 和 {videoAnalysisText}变量，{videoAsrText}是视频的 ASR 文本信息，{videoAnalysisText}是视频的各个子镜头的 VL 视觉信息（视觉语言分析结果）。</p></div></td><td><p># 角色 你是一个专业的视频标注专员，擅长结合视频镜头信息来分析处理各种视频任务。 # 任务目标 请你结合输入数据串联、还原出整个视频的详细剧情。 # 限制 1.如出现语法上错误，或逻辑不通，请直接修改 2.在视频分镜中，如果包含台词，可能会出现说话者与其所说内容不匹配的情况。因此，必须根据剧情的进展，准确判断每段台词的真实说话者 3.如果视频分镜中无台词，请根据视频音频文字为其匹配台词 4.修改后的故事请适当保留视频分镜中对人物、场景的描写 5.帮忙润色一下故事，使其更具逻辑性 6.结合视频分镜中的人物外观特点，如果有外观相近的人物是同一个角色。因此，需要将不同分镜中的人物角色统一。 # 输入数据 ## 资料一：视频分镜信息（视频各镜头的视觉描述信息） {videoAnalysisText} ## 资料二：视频ASR转录信息（未标注出说话者，可能有错误和遗漏，如果没有输入ASR，则忽略此信息） {videoAsrText} # 输出格式 直接输出视频剧情，不要输出其他信息。</p></td></tr><tr><td>generateOptions</td><td><p>array</p></td><td><p>否</p></td><td><div><p>视频理解生成任务选项。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频理解生成任务选项：包含的任务，会自动前置执行。</p><ul><li><p>videoAnalysis：视频语言分析（VL）：如果仅传次值，则运行到视频语言分析后就结束了，不再跑后面的文本加工等子任务；</p></li><li><p><strong>videoGenerate：文本加工-视频总结（默认）</strong>，包含 videoAnalysis；</p></li><li><p>videoTitleGenerate：视频标题生成，包含 videoAnalysis、videoGenerate；</p></li><li><p>videoMindMappingGenerate：视频思维导图生成，包含 videoAnalysis、videoGenerate；videoRoleRecognition：角色自动识别。</p></li></ul></div></td><td><p>videoGenerate</p></td></tr><tr><td>videoExtraInfo</td><td><p>string</p></td><td><p>否</p></td><td><div><p>和视频相关的补充文字资料：您可以自定义扩展文本素材，应用到生成中，需要手动调整 prompt 模版，增加{videoExtraInfo}变量，传入的内容可以是视频摘要、视频简介或视频 ASR 转录信息。</p></div></td><td><p>视频描述了：xx</p></td></tr><tr><td>snapshotInterval</td><td><p>number</p></td><td><p>否</p></td><td><div><p>抽帧间隔：X 秒一帧，取值范围[1, 10]，间隔越大模型能提取到的信息越少，耗时越长，成本越高，默认已是最佳实践，一般无需修改，如果要修改，请根据视频时长来定，建议[1~3]。 建议使用：当前字段优先级高于 frameSampleMethod.interval，一般场景可以使用 frameSampleMethod 字段自定义（userdefined）模式下的 interval，区别在于 frameSampleMethod 自定义模式 interval 取值需要在指定的视频时长对应抽帧间隔范围内。</p></div></td><td><p>2</p></td></tr><tr><td>splitInterval</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>视频分镜最小间隔：单位秒，取值范围[1, 150]，默认根据视频长度取推荐值</p></div></td><td><p>10</p></td></tr><tr><td>language</td><td><p>string</p></td><td><p>否</p></td><td><div><p>语言，可传参数</p><ul><li><p>chinese：中文（默认）</p></li><li><p>french：法语</p></li><li><p>english：英语</p></li><li><p>japanese：日语</p></li><li><p>chineseEnglishFreely：中英文自由说</p></li><li><p>arabic：阿拉伯语</p></li><li><p>korean：韩语</p></li><li><p>malay：马来语</p></li><li><p>thai：泰语</p></li><li><p>portuguese：葡萄牙语</p></li><li><p>spanish：西班牙语</p></li><li><p>indonesian：印尼语</p></li><li><p>vietnamese：越南语</p></li></ul></div></td><td><p>chinese</p></td></tr><tr><td>frameSampleMethod</td><td><p>object</p></td><td><p>否</p></td><td><div><p>抽帧方式</p></div></td><td><p>english</p></td></tr><tr><td>methodName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>抽帧类型，可传参数包括</p><ul><li><p>fast：快速/更低成本</p></li><li><p>standard：标准（默认）</p></li><li><p>userdefined：自定义</p></li></ul></div></td><td><p>standard</p></td></tr><tr><td>interval</td><td><p>number</p></td><td><p>否</p></td><td><div><p>抽帧间隔：单位秒，仅在 userdefined 模式下有效</p></div></td><td><p>2</p></td></tr><tr><td>pixel</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>抽帧像素：每一帧最大边像素，仅在 userdefined 模式下有效，取值范围是 300 到 768</p></div></td><td><p>768</p></td></tr><tr><td>videoRoles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>识别视频中的人物身份列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>识别视频中的人物身份</p></div></td><td></td></tr><tr><td>roleName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>人物名称</p></div></td><td><p>张三</p></td></tr><tr><td>roleInfo</td><td><p>string</p></td><td><p>否</p></td><td><div><p>人物信息描述</p></div></td><td><p>张三是一个男生</p></td></tr><tr><td>urls</td><td><p>array</p></td><td><p>否</p></td><td><div><p>人物头像地址</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>人物头像地址</p></div></td><td><p>http://xxx</p></td></tr><tr><td>isAutoRecognition</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>自动识别是否使用的是自动识别单独的视频地址（是：则人脸图片无法使用时间与视频帧用时间对应，因为可能是不同的视频）</p></div></td><td><p>false</p></td></tr><tr><td>timeIntervals</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>角色出场时间段列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>startTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>开始时间</p></div></td><td><p>0</p></td></tr><tr><td>endTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>结束时间</p></div></td><td><p>345546789</p></td></tr><tr><td>textProcessTasks</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>视频总结(文本加工)任务列表:最多支持 3 个</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>视频总结(文本加工)任务</p></div></td><td></td></tr><tr><td>modelId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频总结依赖的大模型唯一标识，支持的模型</p><ul><li><p>qwen-max-latest</p></li><li><p>qwen-max</p></li><li><p>qwen-plus-latest</p></li><li><p>qwen-plus</p></li><li><p>qwen2.5-7b-instruct-1m</p></li></ul></div></td><td><p>qwen-max-latest</p></td></tr><tr><td>modelCustomPromptTemplate</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频总结依赖的大模型 prompt 模版：必须同时包含{videoAsrText} 和 {videoAnalysisText}变量，{videoAsrText}是视频的 ASR 文本信息，{videoAnalysisText}是视频的各个子镜头的 VL 视觉信息（视觉语言分析结果）。</p></div></td><td><p>xx</p></td></tr><tr><td>modelCustomPromptTemplateId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频总结依赖的大模型 prompt 模版唯一标识：</p><ul><li><p>PlotDetail：剧情详解（默认）；</p></li><li><p>Summary：内容概述；</p></li><li><p>ExtractVideoTag：提取标签；</p></li><li><p>ExplosivePointAnalysis：爆点分析；</p></li><li><p>MultiTask：多类任务；</p></li></ul><p>如果 modelCustomPromptTemplate 未传，则会取模版唯一标识对应的默认 prompt，modelCustomPromptTemplate 优先级高于 modelCustomPromptTemplateId。</p></div></td><td><p>PlotDetail</p></td></tr><tr><td>faceIdentitySimilarityMinScore</td><td><p>number</p></td><td><p>否</p></td><td><div><p>人物识别相似度阈值：0~1</p></div></td><td><p>0.7</p></td></tr><tr><td>videoShotFaceIdentityCount</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>人物匹配时，单镜头(分镜)，参与匹配的抽帧（图片）数量：[1~5]</p></div></td><td><p>2</p></td></tr><tr><td>deduplicationId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>排重字段：可以根据业务需要和业务场景定义自己的业务唯一标识，当前字段重复的数据，系统会保证至少 72h 内不允许重复提交</p></div></td><td><p>1</p></td></tr><tr><td>excludeGenerateOptions</td><td><p>array</p></td><td><p>否</p></td><td><div><p>排除的生成步骤：</p><ul><li><p>videoCaption：视频语音识别</p></li></ul></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>排除的生成步骤：</p><ul><li><p>videoCaption：视频语音识别</p></li></ul></div></td><td><p>[\&quot;videoCaption\&quot;]</p></td></tr><tr><td>videoCaptionInfo</td><td><p>object</p></td><td><p>否</p></td><td><div><p>字幕（asr）信息</p></div></td><td></td></tr><tr><td>videoCaptions</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>字幕（ASR）内容，和 videoCaptionsFIleUrl 二选一</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>字幕（asr）内容</p></div></td><td></td></tr><tr><td>startTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>当前句子开始时间：毫秒</p></div></td><td><p>1000</p></td></tr><tr><td>endTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>当前句子结束时间：毫秒</p></div></td><td><p>10000</p></td></tr><tr><td>text</td><td><p>string</p></td><td><p>否</p></td><td><div><p>内容</p></div></td><td><p>你好</p></td></tr><tr><td>speaker</td><td><p>string</p></td><td><p>否</p></td><td><div><p>角色</p></div></td><td><p>张三</p></td></tr><tr><td>videoCaptionFileUrl</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频字幕（ASR）文件</p></div></td><td><p>oss:// | http://</p></td></tr><tr><td>autoRoleRecognitionVideoUrl</td><td><p>string</p></td><td><p>否</p></td><td><div><p>自动识别功能单独的视频地址 Url</p></div></td><td><p>http://</p></td></tr><tr><td>splitType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>分镜类型：minDuration(限制分镜最小时长), fixDuration(按照固定时长分镜)，默认采用 minDuration 模式</p></div></td><td><p>fixDuration</p></td></tr><tr><td>addDocumentParam</td><td><p>object</p></td><td><p>否</p></td><td><div><p>指定数据集后：视频理解结果作为 meta 信息和视频一起上传到妙搜</p></div></td><td></td></tr><tr><td>datasetId</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>数据集 id：如果期望上传到妙搜，这个字段必选</p></div></td><td><p>3031</p></td></tr><tr><td>datasetName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据集名称</p></div></td><td><p>xxx</p></td></tr><tr><td>document</td><td><p>object</p></td><td><p>否</p></td><td><div><p>上传妙搜相关参数：不录入会自动生成</p></div></td><td></td></tr><tr><td>title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>视频名称</p></div></td><td><p>xx</p></td></tr><tr><td>docId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档业务唯一标识：同数据集会排重</p></div></td><td><p>xxx</p></td></tr><tr><td>categoryUuid</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>tags</td><td><p>array</p></td><td><p>否</p></td><td><div><p>标签</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签</p></div></td><td><p>xx</p></td></tr><tr><td>extend1</td><td><p>string</p></td><td><p>否</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>extend2</td><td><p>string</p></td><td><p>否</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>extend3</td><td><p>string</p></td><td><p>否</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>metadata</td><td><p>object</p></td><td><p>否</p></td><td><div><p>元数据</p></div></td><td></td></tr><tr><td>keyValues</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>keyValue 结构的元数据</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>keyValue 结构的元数据</p></div></td><td></td></tr><tr><td>key</td><td><p>string</p></td><td><p>否</p></td><td><div><p>字段名称</p></div></td><td><p>summary</p></td></tr><tr><td>value</td><td><p>string</p></td><td><p>否</p></td><td><div><p>字段值</p></div></td><td><p>xxx</p></td></tr><tr><td>videoUrls</td><td><p>array</p></td><td><p>否</p></td><td><div><p>多视频 url</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>多视频 url：会合并成一个视频处理，适合短视频场景</p></div></td><td><p>xxx</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| requestId | string | 请求唯一标识 | 085BE2D2-BB7E-59A6-B688-F2CB32124E7F |
| success | boolean | 是否成功：true 成功，false 失败 | True |
| code | string | 状态码 | xx |
| message | string | 错误说明 | success |
| httpStatusCode | integer | http 状态码 | 200 |
| data | object | 结果 |  |
| taskId | string | 任务唯一标识 | 3feb69ed02d9b1a17d0f1a942675d300 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "requestId": "085BE2D2-BB7E-59A6-B688-F2CB32124E7F",
  "success": true,
  "code": "xx",
  "message": "success",
  "httpStatusCode": 200,
  "data": {
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action , Please check the assignment of the workspaceId. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/SubmitVideoAnalysisTask#workbench-doc-change-demo)。
