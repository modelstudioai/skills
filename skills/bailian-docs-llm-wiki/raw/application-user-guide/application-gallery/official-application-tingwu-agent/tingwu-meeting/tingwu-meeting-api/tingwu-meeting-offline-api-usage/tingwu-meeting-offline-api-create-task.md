# CreateTask - 创建离线会议纪要任务

创建离线会议纪要任务的API参考。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

## 接入地址

```
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## 请求方式

post方法请求

## 请求头

```
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

## 创建任务

创建离线会议纪要任务。

### 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

model

string

是

定义业务类型，固定为tingwu-meeting

tingwu-meeting

input

object

是

传入相关业务参数

input.fileUrl

string

3选1

待分析文件oss URL地址

https://_**.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR\_ACCESS\_KEY\_ID&Expires=**_&Signature=YOUR\_SIGNATURE

input.text

string

待分析文本

每行必须按照如下格式：

${发言人名称}: ${发言人内容}

示例如下：

```
张3: 我想买一个SUV汽车
李4: 想要什么价位的？
```

input.dataId

string

关联已经上传并解析完成的任务

j0oS1XbbT\*\*\*

input.appId

string

是

应用id

tw\_YrN4Ss9o5\*\*\*

input.task

string

是

定义任务类型，固定为createTask，表示创建任务

createTask

input.type

string

是

代表创建会议纪要任务的类型，离线会议纪要任务下固定填写offline

offline

input.phraseId

string

是

热词表id，可在控制台热词库页面中获取

创建会议时必填，结束会议并生成纪要时非必填

z4p5EVXof\*\*\*

parameters

object

否

离线会议纪要的控制参数

parameters.transcription

object

是

转写需要的参数

parameters.transcription.model

string

是

转写模型：

-   paraformer-v2（中英文）cn
-   `paraformer-v2（中英日韩粤语）`multilingual
-   `paraformer-v2（英）`en
-   `paraformer-v2（粤）`yue
-   `paraformer-v2（日）`ja
-   `paraformer-v2（韩）`ko
-   `fun-asr（中英文）`fun-asr
-   `教育领域模型（中英）`domain-education
-   `汽车领域模型（中英粤`domain-automotive

cn

parameters.transcription.languageHints

string\[ \]

否

**仅当model传multilingual时**，可选语种，此时传入语种多选框的内容：

中文（cn）， 英语（en）， 粤语（yue）， 日语（ja）、韩语（ko）、德语（de）、法语（fr）、俄语（ru），

如：\["cn", "en", "yue", "ko"\]=

\["cn"\]

parameters.transcription.diarizationEnabled

boolean

是

是否开启角色分离

true

parameters.transcription.diarizationSpeakerCount

int

否

开启角色分离时分离人数：0：说话人角色区分结果为不定人数。 2：说话人角色区分结果为2人。

不传默认0

parameters.transcription.translationEnabled

boolean

是

是否开启翻译

true

parameters.transcription.translationTargetLang

string\[ \]

否

如果开启翻译，需要设置目标翻译语言：

中文（cn）、 英语（en）、日语（ja）、韩语（ko）、德语（de）、法语（fr）、俄语（ru）

目前只支持单选，传参类似：\["cn"\]，

**同时注意，该参数需要与model中的参数不同，否则会导致任务创建失败。**

\["cn"\]

parameters.audio

object

否

音频传入相关参数

？

parameters.audio.audioChannelMode

string

否

paas多音轨设置

-   ""：电话录音 或 16K及以上单声道
-   mix：16K及以上多声道（车载设备录制）
-   不传入：默认音轨 ("")

""

parameters.analysis

object

是

大模型分析参数

parameters.analysis.model

string

是

全局分析模型：

-   `默认项` -> default
-   `tingwu-plus` -> tingwu-plus
-   `qwen-plus` -> qwen-plus
-   `qwq` -> qwq

default

parameters.analysis.keyInformationEnabled

boolean

是

是否开启关键词

true

parameters.analysis.actionsEnabled

boolean

是

是否开启待办事项

true

parameters.analysis.fullSummaryEnabled

boolean

是

是否开启全文摘要

true

parameters.analysis.fullSummaryFormat

string

否

全文摘要格式：

-   一段话摘要：default
-   markdown摘要：markdown

default

parameters.analysis.conversationalEnabled

boolean

是

是否开启发言总结

true

parameters.analysis.questionsAnsweringEnabled

boolean

是

是否开启问答回顾

true

parameters.analysis.mindMapEnabled

boolean

是

是否开启思维导图

true

parameters.analysis.mindMapFormat

string

否

思维导图格式：

-   带时间戳：timestamp
-   不带时间戳：plain

timestamp

parameters.analysis.pptExtractionEnabled

boolean

是

是否开启ppt抽取

true

parameters.analysis.autoChaptersEnabled

boolean

是

是否开启章节速览

true

parameters.analysis.autoChapterGranularity

string

否

章节粒度

Coarse：粗粒度，每小时音/视频约4个章节

General：中等粒度，每小时音/视频约6个章节

Meticulous：细粒度，每小时音/视频约12-15个章节

General

parameters.analysis.autoChapterTitleLengthLevel

string

否

章节标题长度级别

Short：6-25字，平均约13字

Normal：10-28字，平均约16字

Long：10-30字，平均约20字

Short

parameters.analysis.textPolishEnabled

boolean

是

是否开启口语书面化

true

parameters.analysis.customPromptEnabled

boolean

是

是否开启自定义Prompt

true

parameters.analysis.customPromptModel

string

否

若开启自定义Prompt，选择自定义Prompt模型：

-   tingwu-turbo
-   tingwu-plus
-   qwen-max

tingwu-turbo

parameters.analysis.customPromptTransType

string

否

在prompt中，{Transcription}占位符会被替换成不同格式的文本，协议如下所示：

-   default：仅转写文字
    
    -   示例：北京天气怎么样？上海天气怎么样？
-   chat：发言人+转写文字
    
    -   示例：发言人1:北京天气怎么样？\\n发言人2:上海天气怎么样？\\n
-   sentence-chat：句子Id+发言人+文字
    
    -   示例：【1】发言人1:北京天气怎么样？\\n【2】发言人2:上海天气怎么样？\\n

default

parameters.analysis.customPromptContent

string

是

用户输入的自定义Prompt，注意：在Prompt需要原文的位置处设置“{Transcription}”占位符，可在实际运行prompts时，将占位符会替换为parameters.analysis.customPromptTransType定义格式的转写文本。

请帮我总结一下内容：

{Transcription}

### 返回参数

**名称**

**类型**

**描述**

**示例值**

output

object

output.dataId

string

任务id

lsA\*\*\*

usage

object

用量，返回值为空的Object：{}

{}

code

string

错误码

InvalidParameter

message

string

错误信息

Agent Input text format error.

request\_id

string

请求id

f97ee37d-0f9c-9b93-b6bf-bd263a232bf9

### 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。获取方式参考：[前提条件](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-create-task#8a24f2ed09vr0)。

```
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

### 返回示例

```
{
    "output": {
        "dataId": "z4p***"
    },
    "usage": {},
    "request_id": "1e92069c-e1e6-4a5a-97aa-19c3d880140d"
}
```
