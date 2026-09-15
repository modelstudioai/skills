# CreateTask - 创建实时会议纪要任务

创建实时会议纪要任务。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

## 整体调用流程

请参考[实时会议](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-meeting/tingwu-meeting-api/tingwu-meeting-api-usage.md)。

## 接入地址

```
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## 请求方式

POST方法

## 请求头

```
Authorization: Bearer sk-xxxxxxxxxxxxxx
Content-Type: application/json
```

**说明**Authorization需替换为实际的API Key

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

model

string

是

定义业务类型，固定为`tingwu-meeting`

tingwu-meeting

input

object

是

传入相关业务参数

input.type

string

是

表示创建任务类型，创建实时会议任务固定为realtime

realtime

input.appId

string

是

应用id，可在控制台的应用配置页面获取

input.task

string

是

定义任务类型，固定为`createTask`，表示创建任务

createTask

input.format

string

是

表示会议音频的编码格式，目前支持格式：pcm、opus、aac、speex、mp3

创建会议时必填，结束会议并生成纪要时非必填

pcm

input.sampleRate

int

是

表示会议音频的采样率，目前支持8000、16000

创建会议时必填，结束会议并生成纪要时非必填

16000

input.phraseId

string

否

热词表id，可在控制台热词库页面中获取

创建会议时必填，结束会议并生成纪要时非必填

input.dataId

string

是

创建会议时获取的dataId

结束会议并生成纪要时必填，创建会议时非必填

parameters

object

否

实时会议纪要生成控制参数，若传入空对象则复用已发布上线的配置项

parameters.transcription

object

否

转写相关控制参数

parameters.transcription.model

string

否

转写模型，可选值：

-   cn（支持中文、英文）
    
-   multilingual（支持中、英、日、韩、粤语）
    
-   en（英文模型）
    
-   yue（粤语模型）
    
-   ja（日语模型）
    
-   ko（韩语模型）
    
-   domain-education（教育领域模型，支持中英文）
    
-   domain-automotive（汽车领域模型，支持中、英、粤语）
    

multilingual

parameters.transcription.languageHints

array

否

当且仅当`parameters.transcription.model`配置为`multilingual`生效，表示音频中可能存在的语种，未配置的语种将不会出现在识别结果中

\["cn", "en"\]

parameters.transcription.diarizationEnabled

bool

否

表示是否开启发言人分离

true

parameters.transcription.diarizationSpeakerCount

int

否

表示发言人分离的目标个数，可选值：

-   0：代表不确定发言人个数
    
-   2：代表只区分2个发言人
    

默认值为0

0

parameters.transcription.translationEnabled

bool

否

是否开启翻译

true

parameters.transcription.translationTargetLang

array

否

如果开启翻译，需要设置目标翻译语言，目前支持的目标语种有：

-   cn：中文
    
-   en（英文）
    
-   ja（日语）
    
-   ko（韩语）
    
-   de（德语）
    
-   fr（法语）
    
-   ru（俄语）
    

目前仅支持单选

\["en"\]

parameters.audio

object

否

音频相关参数

parameters.audio.audioChannelMode

string

否

多音轨配置项，可选值：

-   mix（多音轨时混合音轨后进行发言人分离）
    
-   空字符串
    

若传空字符串不传该参数，则会根据音频采样率进行不同操作：

-   16K音频：仅对首通道进行识别
    
-   8K音频：将1通道识别为发言人1，将2通道识别为发言人2
    

mix

parameters.analysis

object

否

大模型分析参数

parameters.analysis.model

string

否

全局分析模型，可选值：

-   default（默认分析模型）
    
-   tingwu-plus
    
-   qwen-plus
    
-   qwq
    

tingwu-plus

parameters.analysis.keyInformationEnabled

bool

否

是否提取关键词

true

parameters.analysis.actionsEnabled

bool

否

是否提取待办

true

parameters.analysis.fullSummaryEnabled

bool

否

是否提取全文摘要

true

parameters.analysis.fullSummaryFormat

string

否

提取全文摘要的形式，可选值：

-   default（一段话形式的全文摘要）
    
-   markdown（Markdown格式的全文摘要）
    

仅当`parameters.analysis.fullSummaryEnabled`为true时生效

default

parameters.analysis.conversationalEnabled

bool

否

是否提取发言人总结

true

parameters.analysis.questionsAnsweringEnabled

bool

否

是否提取问答回顾（或要点回顾）

true

parameters.analysis.mindMapEnabled

bool

否

是否提取思维导图

true

parameters.analysis.mindMapFormat

string

否

提取的思维导图格式，可选值：

-   timestamp（在思维导图中携带时间戳）
    
-   plain（不在思维导图中携带时间戳）
    

仅当`parameters.analysis.mindMapEnabled`为true时生效

timestamp

parameters.analysis.pptExtractionEnabled

bool

否

是否提取视频中PPT及PPT摘要

true

parameters.analysis.autoChaptersEnabled

bool

否

是否开启章节速览

true

parameters.analysis.autoChapterGranularity

string

否

章节速览提取粒度，可选值：

-   Coarse：粗粒度，每小时音/视频约4个章节
    
-   General：中等粒度，每小时音/视频约6个章节
    
-   Meticulous：细粒度，每小时音/视频约12-15个章节
    

仅当`parameters.analysis.autoChaptersEnabled`为true时生效

Coarse

parameters.analysis.autoChapterTitleLengthLevel

string

否

章节标题长度级别，可选值：

-   Short：6-25字，平均约13字
    
-   Normal：10-28字，平均约16字
    
-   Long：10-30字，平均约20字
    

仅当`parameters.analysis.autoChaptersEnabled`为true时生效

Normal

parameters.analysis.textPolishEnabled

bool

否

是否将口语书面化

true

parameters.analysis.customPromptEnabled

bool

否

是否开启自定义Prompt

true

parameters.analysis.customPromptModel

string

否

自定义Prompt的分析模型，可选值：

-   tingwu-turbo
    
-   tingwu-plus
    
-   qwen-max
    

仅当`parameters.analysis.customPromptEnabled`为true时生效

tingwu-plus

parameters.analysis.customPromptTransType

string

否

控制在Prompt中，`{Transcription}`占位符会如何被替换成文本，协议如下所示：

-   default：仅转写结果
    
    -   示例：北京天气怎么样？上海天气怎么样？
        
-   chat：发言人+转写结果
    
    -   示例：发言人1:北京天气怎么样？\\n发言人2:上海天气怎么样？\\n
        
-   sentence-chat：句子Id+发言人+结果
    
    -   示例：【1】发言人1:北京天气怎么样？\\n【2】发言人2:上海天气怎么样？\\n
        

仅当`parameters.analysis.customPromptEnabled`为true时生效

chat

parameters.analysis.customPromptContent

string

否

自定义Prompt

仅当`parameters.analysis.customPromptEnabled`为true时生效

注意您必须在此项中加入`{Transcription}`占位符，听悟会自动将转写结果补充到占位符所在的位置。

若未设置`{Transcription}`占位符，自定义Prompt功能将无法生效

请帮我提取原文中每个发言人Id对应的角色，可能存在的角色有销售人员和试驾客户。原文结果如下：{Transcription}

## 返回参数

**名称**

**类型**

**描述**

**示例值**

output

object

output.dataId

string

任务id

output.status

int

-   0：已完成
    
-   1：生成纪要中
    
-   2：失败
    
-   3：转写中
    

3

usage

object

用量，目前为空object

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

## 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

### 创建实时会议

```
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

### 结束实时会议并创建会议纪要

```
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
