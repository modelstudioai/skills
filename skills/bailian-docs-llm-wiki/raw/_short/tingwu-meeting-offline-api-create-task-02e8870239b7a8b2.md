# CreateTask - 创建离线会议纪要任务

创建离线会议纪要任务的API参考。

<a id="前提条件"></a>

<a id="8a24f2ed09vr0"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

<a id="接入地址"></a>

<a id="52a5ef4ab7tfg"></a>

## 接入地址

<a id="code-block"></a>

```http
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

<a id="请求方式"></a>

<a id="606a6390d6xdn"></a>

## 请求方式

post方法请求

<a id="请求头"></a>

<a id="24323e44bdlg5"></a>

## 请求头

<a id="code-block-2"></a>

```http
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

<a id="创建任务"></a>

<a id="22bffc7225ihe"></a>

## 创建任务

创建离线会议纪要任务。

<a id="请求参数"></a>

<a id="49d9739eabds5"></a>

### 请求参数

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义业务类型，固定为tingwu-meeting</p></td><td><p>tingwu-meeting</p></td></tr><tr><td><p>input</p></td><td><p>object</p></td><td><p>是</p></td><td><p>传入相关业务参数</p></td><td></td></tr><tr><td><p>input.fileUrl</p></td><td><p>string</p></td><td rowspan="3"><p>3选1</p></td><td><p>待分析文件oss URL地址</p></td><td><p>https://<em><strong>.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Expires=</strong></em>&amp;Signature=YOUR_SIGNATURE</p></td></tr><tr><td><p>input.text</p></td><td><p>string</p></td><td><p>待分析文本</p></td><td><p>每行必须按照如下格式：</p><p>${发言人名称}: ${发言人内容}</p><p>示例如下：</p><a id="code-block-3"></a><pre class="language-text"><code>张3: 我想买一个SUV汽车
李4: 想要什么价位的？
</code></pre></td></tr><tr><td><p>input.dataId</p></td><td><p>string</p></td><td><p>关联已经上传并解析完成的任务</p></td><td><p>j0oS1XbbT***</p></td></tr><tr><td><p>input.appId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>应用id</p></td><td><p>tw_YrN4Ss9o5***</p></td></tr><tr><td><p>input.task</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义任务类型，固定为createTask，表示创建任务</p></td><td><p>createTask</p></td></tr><tr><td><p>input.type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>代表创建会议纪要任务的类型，离线会议纪要任务下固定填写offline</p></td><td><p>offline</p></td></tr><tr><td><p>input.phraseId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>热词表id，可在控制台热词库页面中获取</p><p>创建会议时必填，结束会议并生成纪要时非必填</p></td><td><p>z4p5EVXof***</p></td></tr><tr><td><p>parameters</p></td><td><p>object</p></td><td><p>否</p></td><td><p>离线会议纪要的控制参数</p></td><td></td></tr><tr><td><p>parameters.transcription</p></td><td><p>object</p></td><td><p>是</p></td><td><p>转写需要的参数</p></td><td></td></tr><tr><td><p>parameters.transcription.model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>转写模型：</p><ul><li>paraformer-v2（中英文）cn</li><li><code>paraformer-v2（中英日韩粤语）</code>multilingual</li><li><code>paraformer-v2（英）</code>en</li><li><code>paraformer-v2（粤）</code>yue</li><li><code>paraformer-v2（日）</code>ja</li><li><code>paraformer-v2（韩）</code>ko</li><li><code>fun-asr（中英文）</code>fun-asr</li><li><code>教育领域模型（中英）</code>domain-education</li><li><code>汽车领域模型（中英粤</code>domain-automotive</li></ul></td><td><p>cn</p></td></tr><tr><td><p>parameters.transcription.languageHints</p></td><td><p>string[ ]</p></td><td><p>否</p></td><td><p><strong>仅当model传multilingual时</strong>，可选语种，此时传入语种多选框的内容：</p><p>中文（cn）， 英语（en）， 粤语（yue）， 日语（ja）、韩语（ko）、德语（de）、法语（fr）、俄语（ru），</p><p>如：[&quot;cn&quot;, &quot;en&quot;, &quot;yue&quot;, &quot;ko&quot;]=</p></td><td><p>[&quot;cn&quot;]</p></td></tr><tr><td><p>parameters.transcription.diarizationEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启角色分离</p></td><td><p>true</p></td></tr><tr><td><p>parameters.transcription.diarizationSpeakerCount</p></td><td><p>int</p></td><td><p>否</p></td><td><p>开启角色分离时分离人数：0：说话人角色区分结果为不定人数。 2：说话人角色区分结果为2人。</p><p>不传默认0</p></td><td></td></tr><tr><td><p>parameters.transcription.translationEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启翻译</p></td><td><p>true</p></td></tr><tr><td><p>parameters.transcription.translationTargetLang</p></td><td><p>string[ ]</p></td><td><p>否</p></td><td><p>如果开启翻译，需要设置目标翻译语言：</p><p>中文（cn）、 英语（en）、日语（ja）、韩语（ko）、德语（de）、法语（fr）、俄语（ru）</p><p>目前只支持单选，传参类似：[&quot;cn&quot;]，</p><strong>同时注意，该参数需要与model中的参数不同，否则会导致任务创建失败。</strong></td><td><p>[&quot;cn&quot;]</p></td></tr><tr><td><p>parameters.audio</p></td><td><p>object</p></td><td><p>否</p></td><td><p>音频传入相关参数</p></td><td><p>？</p></td></tr><tr><td><p>parameters.audio.audioChannelMode</p></td><td><p>string</p></td><td><p>否</p></td><td><p>paas多音轨设置</p><ul><li>&quot;&quot;：电话录音 或 16K及以上单声道</li><li>mix：16K及以上多声道（车载设备录制）</li><li>不传入：默认音轨 (&quot;&quot;)</li></ul></td><td><p>&quot;&quot;</p></td></tr><tr><td><p>parameters.analysis</p></td><td><p>object</p></td><td><p>是</p></td><td><p>大模型分析参数</p></td><td></td></tr><tr><td><p>parameters.analysis.model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>全局分析模型：</p><ul><li><code>默认项</code> -&gt; default</li><li><code>tingwu-plus</code> -&gt; tingwu-plus</li><li><code>qwen-plus</code> -&gt; qwen-plus</li><li><code>qwq</code> -&gt; qwq</li></ul></td><td><p>default</p></td></tr><tr><td><p>parameters.analysis.keyInformationEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启关键词</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.actionsEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启待办事项</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.fullSummaryEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启全文摘要</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.fullSummaryFormat</p></td><td><p>string</p></td><td><p>否</p></td><td><p>全文摘要格式：</p><ul><li>一段话摘要：default</li><li>markdown摘要：markdown</li></ul></td><td><p>default</p></td></tr><tr><td><p>parameters.analysis.conversationalEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启发言总结</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.questionsAnsweringEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启问答回顾</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.mindMapEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启思维导图</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.mindMapFormat</p></td><td><p>string</p></td><td><p>否</p></td><td><p>思维导图格式：</p><ul><li>带时间戳：timestamp</li><li>不带时间戳：plain</li></ul></td><td><p>timestamp</p></td></tr><tr><td><p>parameters.analysis.pptExtractionEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启ppt抽取</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.autoChaptersEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启章节速览</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.autoChapterGranularity</p></td><td><p>string</p></td><td><p>否</p></td><td><p>章节粒度</p><p>Coarse：粗粒度，每小时音/视频约4个章节</p><p>General：中等粒度，每小时音/视频约6个章节</p><p>Meticulous：细粒度，每小时音/视频约12-15个章节</p></td><td><p>General</p></td></tr><tr><td><p>parameters.analysis.autoChapterTitleLengthLevel</p></td><td><p>string</p></td><td><p>否</p></td><td><p>章节标题长度级别</p><p>Short：6-25字，平均约13字</p><p>Normal：10-28字，平均约16字</p><p>Long：10-30字，平均约20字</p></td><td><p>Short</p></td></tr><tr><td><p>parameters.analysis.textPolishEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启口语书面化</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.customPromptEnabled</p></td><td><p>boolean</p></td><td><p>是</p></td><td><p>是否开启自定义Prompt</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.customPromptModel</p></td><td><p>string</p></td><td><p>否</p></td><td><p>若开启自定义Prompt，选择自定义Prompt模型：</p><ul><li>tingwu-turbo</li><li>tingwu-plus</li><li>qwen-max</li></ul></td><td><p>tingwu-turbo</p></td></tr><tr><td><p>parameters.analysis.customPromptTransType</p></td><td><p>string</p></td><td><p>否</p></td><td><p>在prompt中，{Transcription}占位符会被替换成不同格式的文本，协议如下所示：</p><ul><li><p>default：仅转写文字</p><ul><li>示例：北京天气怎么样？上海天气怎么样？</li></ul></li><li><p>chat：发言人+转写文字</p><ul><li>示例：发言人1:北京天气怎么样？\n发言人2:上海天气怎么样？\n</li></ul></li><li><p>sentence-chat：句子Id+发言人+文字</p><ul><li>示例：【1】发言人1:北京天气怎么样？\n【2】发言人2:上海天气怎么样？\n</li></ul></li></ul></td><td><p>default</p></td></tr><tr><td><p>parameters.analysis.customPromptContent</p></td><td><p>string</p></td><td><p>是</p></td><td><p>用户输入的自定义Prompt，注意：在Prompt需要原文的位置处设置“{Transcription}”占位符，可在实际运行prompts时，将占位符会替换为parameters.analysis.customPromptTransType定义格式的转写文本。</p></td><td><p>请帮我总结一下内容：</p><p>{Transcription}</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="9c516a766ag9w"></a>

### 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| output | object |  |  |
| output.dataId | string | 任务id | lsA\*\*\* |
| usage | object | 用量，返回值为空的Object：{} | {} |
| code | string | 错误码 | InvalidParameter |
| message | string | 错误信息 | Agent Input text format error. |
| request\_id | string | 请求id | f97ee37d-0f9c-9b93-b6bf-bd263a232bf9 |

<a id="请求示例"></a>

<a id="8f1fb0d17czzs"></a>

### 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。获取方式参考：[前提条件](tingwu-meeting-offline-api-create-task-02e8870239b7a8b2.md#8a24f2ed09vr0)。

<a id="code-block-4"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-meeting",
    "input": {
        "task": "createTask",
        "type": "offline",
        "appId": "tw_AxlVSM**",
        "fileUrl": "",
        "phraseId": "z4p5EVXof***"
    },
    "parameters": {
        "transcription": {
            "model": "cn",
            "diarizationEnabled": true,
            "diarizationSpeakerCount": 0,
            "translationEnabled": true,
            "translationTargetLang": [
                "en"
            ]
        },
        "analysis": {
            "model": "default",
            "keyInformationEnabled": true,
            "actionsEnabled": true,
            "fullSummaryEnabled": true,
            "fullSummaryFormat": "markdown",
            "conversationalEnabled": true,
            "questionsAnsweringEnabled": true,
            "mindMapEnabled": true,
            "mindMapFormat": "timestamp",
            "pptExtractionEnabled": true,
            "autoChaptersEnabled": true,
            "autoChapterGranularity": "Coarse",
            "autoChapterTitleLengthLevel": "Short",
            "textPolishEnabled": true,
            "customPromptEnabled": true,
            "customPromptModel": "tingwu-turbo",
            "customPromptTransType": "default",
            "customPromptContent": "{Transcription}推测前面的对话有几个人"
        }
    }
}'
```

<a id="返回示例"></a>

<a id="8c15330051ss9"></a>

### 返回示例

<a id="code-block-5"></a>

```json
{
    "output": {
        "dataId": "z4p***"
    },
    "usage": {},
    "request_id": "1e92069c-e1e6-4a5a-97aa-19c3d880140d"
}
```
