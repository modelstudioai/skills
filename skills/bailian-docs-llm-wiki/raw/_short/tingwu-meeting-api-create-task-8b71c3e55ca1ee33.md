# CreateTask - 创建实时会议纪要任务

创建实时会议纪要任务。

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

<a id="整体调用流程"></a>

<a id="c9ece8a318kdl"></a>

## 整体调用流程

请参考[实时会议](tingwu-meeting-api-usage-bfedb8b7aed31f51.md)。

<a id="接入地址"></a>

<a id="e8ae9f13941un"></a>

## 接入地址

<a id="code-block"></a>

```http
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

<a id="请求方式"></a>

<a id="58355fb966c2u"></a>

## 请求方式

POST方法

<a id="请求头"></a>

<a id="24323e44bdlg5"></a>

## 请求头

<a id="code-block-2"></a>

```http
Authorization: Bearer sk-xxxxxxxxxxxxxx
Content-Type: application/json
```

> **说明**
>
> Authorization需替换为实际的API Key

<a id="请求参数"></a>

<a id="34b842a7838b1"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义业务类型，固定为<code>tingwu-meeting</code></p></td><td><p>tingwu-meeting</p></td></tr><tr><td><p>input</p></td><td><p>object</p></td><td><p>是</p></td><td><p>传入相关业务参数</p></td><td></td></tr><tr><td><p>input.type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示创建任务类型，创建实时会议任务固定为realtime</p></td><td><p>realtime</p></td></tr><tr><td><p>input.appId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>应用id，可在控制台的应用配置页面获取</p></td><td></td></tr><tr><td><p>input.task</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义任务类型，固定为<code>createTask</code>，表示创建任务</p></td><td><p>createTask</p></td></tr><tr><td><p>input.format</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示会议音频的编码格式，目前支持格式：pcm、opus、aac、speex、mp3</p><p>创建会议时必填，结束会议并生成纪要时非必填</p></td><td><p>pcm</p></td></tr><tr><td><p>input.sampleRate</p></td><td><p>int</p></td><td><p>是</p></td><td><p>表示会议音频的采样率，目前支持8000、16000</p><p>创建会议时必填，结束会议并生成纪要时非必填</p></td><td><p>16000</p></td></tr><tr><td><p>input.phraseId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>热词表id，可在控制台热词库页面中获取</p><p>创建会议时必填，结束会议并生成纪要时非必填</p></td><td></td></tr><tr><td><p>input.dataId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>创建会议时获取的dataId</p><p>结束会议并生成纪要时必填，创建会议时非必填</p></td><td></td></tr><tr><td><p>parameters</p></td><td><p>object</p></td><td><p>否</p></td><td><p>实时会议纪要生成控制参数，若传入空对象则复用已发布上线的配置项</p></td><td></td></tr><tr><td><p>parameters.transcription</p></td><td><p>object</p></td><td><p>否</p></td><td><p>转写相关控制参数</p></td><td></td></tr><tr><td><p>parameters.transcription.model</p></td><td><p>string</p></td><td><p>否</p></td><td><p>转写模型，可选值：</p><ul><li><p>cn（支持中文、英文）</p></li><li><p>multilingual（支持中、英、日、韩、粤语）</p></li><li><p>en（英文模型）</p></li><li><p>yue（粤语模型）</p></li><li><p>ja（日语模型）</p></li><li><p>ko（韩语模型）</p></li><li><p>domain-education（教育领域模型，支持中英文）</p></li><li><p>domain-automotive（汽车领域模型，支持中、英、粤语）</p></li></ul></td><td><p>multilingual</p></td></tr><tr><td><p>parameters.transcription.languageHints</p></td><td><p>array</p></td><td><p>否</p></td><td><p>当且仅当<code>parameters.transcription.model</code>配置为<code>multilingual</code>生效，表示音频中可能存在的语种，未配置的语种将不会出现在识别结果中</p></td><td><p>[&quot;cn&quot;, &quot;en&quot;]</p></td></tr><tr><td><p>parameters.transcription.diarizationEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>表示是否开启发言人分离</p></td><td><p>true</p></td></tr><tr><td><p>parameters.transcription.diarizationSpeakerCount</p></td><td><p>int</p></td><td><p>否</p></td><td><p>表示发言人分离的目标个数，可选值：</p><ul><li><p>0：代表不确定发言人个数</p></li><li><p>2：代表只区分2个发言人</p></li></ul><p>默认值为0</p></td><td><p>0</p></td></tr><tr><td><p>parameters.transcription.translationEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否开启翻译</p></td><td><p>true</p></td></tr><tr><td><p>parameters.transcription.translationTargetLang</p></td><td><p>array</p></td><td><p>否</p></td><td><p>如果开启翻译，需要设置目标翻译语言，目前支持的目标语种有：</p><ul><li><p>cn：中文</p></li><li><p>en（英文）</p></li><li><p>ja（日语）</p></li><li><p>ko（韩语）</p></li><li><p>de（德语）</p></li><li><p>fr（法语）</p></li><li><p>ru（俄语）</p></li></ul><p>目前仅支持单选</p></td><td><p>[&quot;en&quot;]</p></td></tr><tr><td><p>parameters.audio</p></td><td><p>object</p></td><td><p>否</p></td><td><p>音频相关参数</p></td><td></td></tr><tr><td><p>parameters.audio.audioChannelMode</p></td><td><p>string</p></td><td><p>否</p></td><td><p>多音轨配置项，可选值：</p><ul><li><p>mix（多音轨时混合音轨后进行发言人分离）</p></li><li><p>空字符串</p></li></ul><p>若传空字符串不传该参数，则会根据音频采样率进行不同操作：</p><ul><li><p>16K音频：仅对首通道进行识别</p></li><li><p>8K音频：将1通道识别为发言人1，将2通道识别为发言人2</p></li></ul></td><td><p>mix</p></td></tr><tr><td><p>parameters.analysis</p></td><td><p>object</p></td><td><p>否</p></td><td><p>大模型分析参数</p></td><td></td></tr><tr><td><p>parameters.analysis.model</p></td><td><p>string</p></td><td><p>否</p></td><td><p>全局分析模型，可选值：</p><ul><li><p>default（默认分析模型）</p></li><li><p>tingwu-plus</p></li><li><p>qwen-plus</p></li><li><p>qwq</p></li></ul></td><td><p>tingwu-plus</p></td></tr><tr><td><p>parameters.analysis.keyInformationEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取关键词</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.actionsEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取待办</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.fullSummaryEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取全文摘要</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.fullSummaryFormat</p></td><td><p>string</p></td><td><p>否</p></td><td><p>提取全文摘要的形式，可选值：</p><ul><li><p>default（一段话形式的全文摘要）</p></li><li><p>markdown（Markdown格式的全文摘要）</p></li></ul><p>仅当<code>parameters.analysis.fullSummaryEnabled</code>为true时生效</p></td><td><p>default</p></td></tr><tr><td><p>parameters.analysis.conversationalEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取发言人总结</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.questionsAnsweringEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取问答回顾（或要点回顾）</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.mindMapEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取思维导图</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.mindMapFormat</p></td><td><p>string</p></td><td><p>否</p></td><td><p>提取的思维导图格式，可选值：</p><ul><li><p>timestamp（在思维导图中携带时间戳）</p></li><li><p>plain（不在思维导图中携带时间戳）</p></li></ul><p>仅当<code>parameters.analysis.mindMapEnabled</code>为true时生效</p></td><td><p>timestamp</p></td></tr><tr><td><p>parameters.analysis.pptExtractionEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否提取视频中PPT及PPT摘要</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.autoChaptersEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否开启章节速览</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.autoChapterGranularity</p></td><td><p>string</p></td><td><p>否</p></td><td><p>章节速览提取粒度，可选值：</p><ul><li><p>Coarse：粗粒度，每小时音/视频约4个章节</p></li><li><p>General：中等粒度，每小时音/视频约6个章节</p></li><li><p>Meticulous：细粒度，每小时音/视频约12-15个章节</p></li></ul><p>仅当<code>parameters.analysis.autoChaptersEnabled</code>为true时生效</p></td><td><p>Coarse</p></td></tr><tr><td><p>parameters.analysis.autoChapterTitleLengthLevel</p></td><td><p>string</p></td><td><p>否</p></td><td><p>章节标题长度级别，可选值：</p><ul><li><p>Short：6-25字，平均约13字</p></li><li><p>Normal：10-28字，平均约16字</p></li><li><p>Long：10-30字，平均约20字</p></li></ul><p>仅当<code>parameters.analysis.autoChaptersEnabled</code>为true时生效</p></td><td><p>Normal</p></td></tr><tr><td><p>parameters.analysis.textPolishEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否将口语书面化</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.customPromptEnabled</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否开启自定义Prompt</p></td><td><p>true</p></td></tr><tr><td><p>parameters.analysis.customPromptModel</p></td><td><p>string</p></td><td><p>否</p></td><td><p>自定义Prompt的分析模型，可选值：</p><ul><li><p>tingwu-turbo</p></li><li><p>tingwu-plus</p></li><li><p>qwen-max</p></li></ul><p>仅当<code>parameters.analysis.customPromptEnabled</code>为true时生效</p></td><td><p>tingwu-plus</p></td></tr><tr><td><p>parameters.analysis.customPromptTransType</p></td><td><p>string</p></td><td><p>否</p></td><td><p>控制在Prompt中，<code>{Transcription}</code>占位符会如何被替换成文本，协议如下所示：</p><ul><li><p>default：仅转写结果</p><ul><li><p>示例：北京天气怎么样？上海天气怎么样？</p></li></ul></li><li><p>chat：发言人+转写结果</p><ul><li><p>示例：发言人1:北京天气怎么样？\n发言人2:上海天气怎么样？\n</p></li></ul></li><li><p>sentence-chat：句子Id+发言人+结果</p><ul><li><p>示例：【1】发言人1:北京天气怎么样？\n【2】发言人2:上海天气怎么样？\n</p></li></ul></li></ul><p>仅当<code>parameters.analysis.customPromptEnabled</code>为true时生效</p></td><td><p>chat</p></td></tr><tr><td><p>parameters.analysis.customPromptContent</p></td><td><p>string</p></td><td><p>否</p></td><td><p>自定义Prompt</p><p>仅当<code>parameters.analysis.customPromptEnabled</code>为true时生效</p><p>注意您必须在此项中加入<code>{Transcription}</code>占位符，听悟会自动将转写结果补充到占位符所在的位置。</p><p>若未设置<code>{Transcription}</code>占位符，自定义Prompt功能将无法生效</p></td><td><p>请帮我提取原文中每个发言人Id对应的角色，可能存在的角色有销售人员和试驾客户。原文结果如下：{Transcription}</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="e75d785e9ftr3"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>object</p></td><td></td><td></td></tr><tr><td><p>output.dataId</p></td><td><p>string</p></td><td><p>任务id</p></td><td></td></tr><tr><td><p>output.status</p></td><td><p>int</p></td><td><ul><li><p>0：已完成</p></li><li><p>1：生成纪要中</p></li><li><p>2：失败</p></li><li><p>3：转写中</p></li></ul></td><td><p>3</p></td></tr><tr><td><p>usage</p></td><td><p>object</p></td><td><p>用量，目前为空object</p></td><td><p>{}</p></td></tr><tr><td><p>code</p></td><td><p>string</p></td><td><p>错误码</p></td><td><p>InvalidParameter</p></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td><p>Agent Input text format error.</p></td></tr><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求id</p></td><td><p>f97ee37d-0f9c-9b93-b6bf-bd263a232bf9</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="b38dac29897ll"></a>

## 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

<a id="创建实时会议"></a>

<a id="3578983862v9j"></a>

### 创建实时会议

<a id="code-block-3"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-******e181c' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-meeting",
    "input": {
        "task": "createTask",
        "appId": "tw_***",
        "type": "realtime",
        "format": "pcm",
        "sampleRate": 16000,
        "phraseId": "DEA******Isv"
    },
    "parameters": {
        "transcription": {
          "model": "multilingual",
          "languageHints": ["cn", "en"],
          "diarizationEnabled": true,
          "diarizationSpeakerCount": 0,
          "translationEnabled": true,
          "translationTargetLang": ["ja"]
        },
        "audio": {
          "audioChannelMode": ""
        },
        "analysis": {
          "model": "default",
          "keyInformationEnabled": true,
          "actionsEnabled": false,
          "fullSummaryEnabled": true,
          "fullSummaryFormat": "default",
          "conversationalEnabled": false,
          "questionsAnsweringEnabled": false,
          "mindMapEnabled": true,
          "mindMapFormat": "plain",
          "pptExtractionEnabled": false,
          "autoChaptersEnabled": true,
          "autoChapterGranularity": "Coarse",
          "autoChapterTitleLengthLevel": "Short",
          "textPolishEnabled": false,
          "customPromptEnabled": true,
          "customPromptModel": "tingwu-turbo",
          "customPromptTransType": "chat",
          "customPromptContent": "请帮我提取原文中每个发言人Id对应的角色，可能存在的角色有销售人员和试驾客户。原文结果如下：{Transcription}"
       }
    }
}'
```

<a id="结束实时会议并创建会议纪要"></a>

<a id="98141fc268sw7"></a>

### 结束实时会议并创建会议纪要

<a id="code-block-4"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-******e181c' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-meeting",
    "input": {
        "task": "createTask",
        "appId": "tw_***",
        "type": "realtime",
        "dataId": "BEc******syu"
    }
}'
```
