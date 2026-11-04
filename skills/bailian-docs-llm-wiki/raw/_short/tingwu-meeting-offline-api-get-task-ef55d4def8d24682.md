# GetTask - 获取离线会议纪要任务结果

获取离线会议纪要任务结果的API参考。

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

`tingwu-meeting`

input

object

是

传入相关业务参数

input.task

string

是

定义任务类型，固定为`getTask`，表示获取任务结果

getTask

input.dataId

string

是

需要查询的离线会议纪要任务id

wkb\*\*\*

## 返回参数

**名称**

**类型**

**描述**

**示例值/解析协议**

code

string

错误码

message

string

错误信息

request\_id

string

请求id

f97ee37d-0f9c-9b93-b6bf-bd263a232bf9

usage

object

用量，目前无值

{}

output

object

业务返回体

output.status

int

任务状态：

-   0：成功
    
-   1：进行中
    
-   2：失败
    

0

output.errorCode

string

任务成功提交，但是执行失败（`status`为2时）的错误码

TSC.FileError

output.errorMessage

string

任务成功提交，但是任务执行失败（`status`为2时）的错误信息

File cannot be read.

output.playbackUrl

string

回听音频url，有效期是24h

ossUrl对应的文件内容解析协议参见：

-   [output.transcriptionPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#842aa17ccdv95)
    
-   [output.translationsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#87d3ea1c81d4p)
    
-   [output.autoChaptersPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#0d8cca338fay8)
    
-   [output.summarizationPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#085d4a95d3ffb)
    
-   [output.meetingAssistancePath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#2ef20891aftjk)
    
-   [output.pptExtractionPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#dbbb3c7eb6sz8)
    
-   [output.textPolishPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#bfde32a6a5n6k)
    
-   [output.customPromptPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#041ed2bfbd5z4)
    

注意，当且仅当url中字符串为null时，代表子任务失败，否则认为子任务成功

output.transcriptionPath

string

转写结果对象的ossUrl

output.translationsPath

string

翻译的ossUrl

output.autoChaptersPath

string

章节速览的ossUrl

output.summarizationPath

string

全文摘要、发言总结、问答回顾、思维导图的ossUrl

output.meetingAssistancePath

string

待办事项、关键词的ossUrl

output.pptExtractionPath

string

PPT抽取及摘要的ossUrl

output.textPolishPath

string

口语书面化的ossUrl

output.customPromptPath

string

自定义Prompt的ossUrl

#### output.transcriptionPath的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

audioInfo

object

音频信息对象。

audioInfo.Size

long

音频大小，单位：字节。

3335756

audioInfo.Duration

long

音频时长，单位：毫秒。（实时语音转写时，该字段不表示实际音频时长）

104006

audioInfo.SampleRate

int

音频采样率。

16000

audioInfo.Language

string

音频语种。

cn

audioSegments

array<array<int>>

有效音频片断范围。

audioSegments\[i\]\[0\]

int

有效音频片段的开始时间，单位为毫秒。

1690

audioSegments\[i\]\[1\]

int

有效音频片段的结束时间，单位为毫秒。

10704

paragraphs

array

段落列表

paragraphs\[0\].paragraphId

String

段落ID

16987422100275\*\*\*\*\*

paragraphs\[0\].speakerId

String

说话者ID

1

paragraphs\[0\].words

array

字词列表

paragraphs\[0\].words\[0\].id

int

字词编号

10

paragraphs\[0\].words\[0\].sentenceId

int

句子ID

1

paragraphs\[0\].words\[0\].start

int

开始时间（毫秒）

4970

paragraphs\[0\].words\[0\].end

int

结束时间（毫秒）

5560

paragraphs\[0\].words\[0\].text

String

字词文本

您好，

示例json如下：

```
{
  "audioInfo": {
    "duration": 300000,
    "language": "cn",
    "sampleRate": 16000,
    "size": 9605546
  },
  "audioSegments": [
    [
      2960,
      6908
    ],
    [
      7310,
      12879
    ]
  ],
  "paragraphs": [
    {
      "paragraphId": "1758265418316500000",
      "speakerId": "1",
      "words": [
        {
          "end": 3895,
          "id": 10,
          "sentenceId": 1,
          "start": 2960,
          "text": "这会儿"
        },
        {
          "end": 4030,
          "id": 20,
          "sentenceId": 1,
          "start": 3895,
          "text": "我"
        }
      ]
    }
  ]
}
```

#### output.translationsPath的解析协议

最外层是一个Object，具体字段如下：

**参数名**

**类型**

**说明**

paragraphs

list\[\]

翻译结果以段落形式组织的集合，和语音识别结果报文对应。

paragraphs.paragraphId

string

段落分段id标识，和语音识别结果中的ParagraphId对应。

paragraphs.sentences

list\[\]

翻译文本集合。

paragraphs.sentences\[i\].sentenceId

long

句子id。

paragraphs.sentences\[i\].start

long

该段相对于音频起始时间的开始时间，相对时间戳，单位毫秒。

paragraphs.sentences\[i\].end

long

该段相对于音频起始时间的结束时间，相对时间戳，单位毫秒。

paragraphs.sentences\[i\].text

string

翻译文本，和语音识别结果报文对应。

示例json如下：

```
{
  "paragraphs": [
    {
      "paragraphId": "1758274598863500000",
      "sentences": [
        {
          "end": 6908,
          "sentenceId": 1,
          "start": 2960,
          "text": "At the moment, I will systematically tell you some things before we leave. "
        },
        {
          "end": 12879,
          "sentenceId": 2,
          "start": 7310,
          "text": "First of all, our car is equipped with this kind of remote control key, which can be directly controlled in APP. "
        },
        {
          "end": 14576,
          "sentenceId": 3,
          "start": 13850,
          "text": "This has two advantages. "
        },
        {
          "end": 22510,
          "sentenceId": 4,
          "start": 14580,
          "text": "First, if you are out of town and your car is now, for example, on the side of the road, you want to park your car in your garage, but you are not there, what should you do at this time? "
        },
        {
          "end": 36466,
          "sentenceId": 5,
          "start": 22820,
          "text": "Sharing one is to use this APP to share a key and remote key with your friend or driver. Let him tilt in the car prohibited by this APP. Just park the car and let him sleep again. It is to give him a temporary key. This is the first advantage. "
        },
        {
          "end": 45255,
          "sentenceId": 6,
          "start": 36740,
          "text": "The second advantage is that you can see the car locks and windows. If you are not sure whether the car doors are closed or not, you can watch and use them at home. "
        },
        {
          "end": 48408,
          "sentenceId": 7,
          "start": 47210,
          "text": "No, as long as there's a match for Wang. "
        }
      ]
    }
  ]
}
```

#### output.autoChaptersPath的解析协议

最外层是一个array，具体字段如下：

**参数名**

**类型**

**说明**

\[i\].id

int

该章节序号。

\[i\].start

long

该章节相对于音频起始时间的开始时间，相对时间戳，单位毫秒。

\[i\].end

long

该章节相对于音频起始时间的结束时间，相对时间戳，单位毫秒。

\[i\].headline

string

该章节的一句话标题。

\[i\].summary

string

章节总结。

示例json如下：

```
[
    {
        "end": 245450,
        "headline": "智能汽车远程操控与泊车功能",
        "id": 1,
        "start": 2960,
        "summary": "介绍了智能汽车的远程操控功能，包括通过APP分享临时钥匙、远程控制车锁车窗、启动车辆等，以及自动泊车和进出车位的辅助功能。同时，提及了车内语音控制系统，支持前后排乘客无需唤醒即可操作。"
    },
    {
        "end": 299930,
        "headline": "城市NGP与驾驶辅助功能解析",
        "id": 2,
        "start": 248440,
        "summary": "讨论了城市NGP的使用条件，指出在部分路段开通时可尝试使用，未开通则仅提供ACC等基础辅助功能。强调在光线不佳条件下手动驾驶的危险性，以及NGP系统在有无特定路段支持时的行为差异。"
    }
]
```

#### output.summarizationPath的解析协议

最外层是一个Object，具体字段如下：

**参数名**

**类型**

**说明**

paragraphSummary

string

全文摘要结果，以`@#`符号分割为两部分：

-   `@#`前：开头通过简短的文字，总结全文内容；
    
-   `@#`后：用markdown格式的无序列表呈现内容要点
    

conversationalSummary

list\[\]

发言总结摘要结果列表。

conversationalSummary\[i\].speakerId

string

发言人id。

conversationalSummary\[i\].speakerName

string

发言人名字。

conversationalSummary\[i\].summary

string

该发言人对应的总结。

questionsAnsweringSummary

list\[\]

问答回顾摘要结果列表。

questionsAnsweringSummary\[i\].question

string

问题

questionsAnsweringSummary\[i\].sentenceIdsOfQuestion

list\[\]

提炼出该问题对应的原语音转写的SentenceId列表。

questionsAnsweringSummary\[i\].answer

string

问题对应的答案。

questionsAnsweringSummary\[i\].sentenceIdsOfAnswer

list\[\]

总结出该答案对应的原语音转写的SentenceId列表。

mindMapSummary

list\[\]

思维导图结果列表。

mindMapSummary\[i\].title

string

思维导图单个节点的文本内容。

mindMapSummary\[i\].beginTime

int

思维导图单个节点相较于开始时的时间戳，单位ms，仅存在叶子节点中。

mindMapSummary\[i\].topic

list\[\]

思维导图单个节点的子节点列表

示例json如下：

```
{
  "conversationalSummary": [
    {
      "speakerId": "2",
      "speakerName": "发言人2",
      "summary": "讨论了车辆自动驾驶与手动控制的转换"
    },
    {
      "speakerId": "1",
      "speakerName": "发言人1",
      "summary": "详细介绍了车辆出发前的准备事项"
    }
  ],
  "mindMapSummary": [
    {
      "title": "出发前车辆功能介绍",
      "topic": [
        {
          "title": "遥控钥匙与APP操控",
          "topic": [
            {
              "beginTime": 14580,
              "title": "远程操控车辆，如分享临时钥匙给朋友或代驾停入车库",
              "topic": []
            },
            {
              "beginTime": 36740,
              "title": "检查车门锁闭状态，确保安全",
              "topic": []
            }
          ]
        },
        {
          "title": "远程启动与鸣笛定位",
          "topic": [
            {
              "beginTime": 54080,
              "title": "地下车库找车时，通过鸣笛定位车辆位置",
              "topic": []
            }
          ]
        }
      ]
    }
  ],
  "paragraphSummary": "本记录讲述了智能汽车远程控制与自动化驾驶功能的详细介绍与演示，包括远程钥匙、进出车位、语音操控等，以及城市NGP驾驶辅助系统的工作原理。@#\n\n- **远程控制功能介绍[2]**\n  1. **远程钥匙分享[4]**\n  2. **车门与车窗状态确认[6]**",
  "questionsAnsweringSummary": [
    {
      "answer": "这个系统有两个好处。首先，在外地时，如果想让朋友或代驾将车停进车库，可以分享APP中的远程钥匙，让他们通过APP操作停车。其次，车主可以在家里通过APP查看并控制车锁、车窗是否关闭，甚至实现远程启动和鸣笛等功能。",
      "question": "这个远程钥匙系统有哪些好处呢？",
      "sentenceIdsOfAnswer": [
        1,
        2,
        3,
        4,
        5,
        6,
        7
      ],
      "sentenceIdsOfQuestion": [
        1,
        2,
        3,
        4,
        5,
        6,
        7
      ]
    }
  ]
}
```

#### output.meetingAssistancePath的解析协议

最外层是一个Object，具体字段如下：

**参数名**

**类型**

**说明**

keywords

list\[\]

关键词提取结果。

actions

list\[\]

待办内容、待办摘要的集合。

actions\[i\].id

long

待办序号。

actions\[i\].sentenceId

long

该关键句在原ASR转写中对应的句子Id。

actions\[i\].start

long

相对于音频起始时间的开始时间，相对时间戳，单位毫秒。

actions\[i\].end

long

相对于音频起始时间的结束时间，相对时间戳，单位毫秒。

actions\[i\].text

string

待办内容。

classifications

object

场景识别分类，目前只有3种场景分类。

classifications.interview

float

面试场景置信度得分。

classifications.lecture

float

演讲场景置信度得分。

classifications.meeting

float

会议场景置信度得分。

示例json如下：

```
{
  "actions": [
    {
      "end": 0,
      "id": 1,
      "sentenceId": 5,
      "start": 0,
      "text": "反馈快递部门关于快递包装损坏的情况，并要求重新包装或赔偿。"
    }
  ],
  "classifications": {
    "interview": 0.0,
    "lecture": 0.22630735,
    "meeting": 0.2158773
  },
  "keywords": [
    "快递",
    "包装损坏"
  ]
}
```

#### output.pptExtractionPath的解析协议

最外层是一个Object，具体字段如下：

**参数名**

**类型**

**说明**

availableForSummary

boolean

标识是否存在PPT总结文本。为false表示没有PPT总结结果，为true表示至少有一条。

keyFrameList

list\[\]

PPT结果list，含PPT图片和总结文本。

keyFrameList\[i\].id

long

序号。

keyFrameList\[i\].start

long

相对于音频起始时间的开始时间，相对时间戳，单位毫秒。

keyFrameList\[i\].end

long

相对于音频起始时间的结束时间，相对时间戳，单位毫秒。

keyFrameList\[i\].fileUrl

string

生成的PPT图片结果，HTTP下载链接。

keyFrameList\[i\].summary

string

对应的PPT总结。

示例json如下：

```
{
    "availableForSummary": true,
    "keyFrameList": [
        {
            "end": 17470,
            "fileUrl": "https://prod-tingwu-paas-common-beijing.oss-cn-beijing.aliyuncs.com/***",
            "id": 1,
            "start": 30
        }
    ]
}
```

#### output.textPolishPath的解析协议

最外层是一个array，具体字段如下：

**JSON字段**

**类型**

**说明**

\[i\].formalParagraphText

string

口语书面化的文本结果。

\[i\].sentenceIds

list

口语书面化改写内容对应的SentenceId列表。

\[i\].paragraphId

string

文本结果的段落id，和语音转写结果中的段落id对应。

\[i\].start

long

文本结果在原音频中的开始时间，相对时间戳，单位为毫秒。

\[i\].end

long

文本结果在原音频中的结束时间，相对时间戳，单位为毫秒。

示例json如下：

```
[
    {
        "end": 32392,
        "formalParagraphText": "大家好，我是通义听悟的产品经理李喆。今天，我将为大家带来通义听悟公共云API的介绍。首先，让我们来了解一下听悟整体情况。听悟是一个专注于音视频内容的工作学习助手，它能够精准分析、提取并总结音视频内容，帮助企业客户迅速抓住关键信息，提高内容利用效率。内置的大型模型支持摘要、质检、翻译等多种功能，同时兼具语音识别和视觉理解能力。",
        "paragraphId": "1758527947000500001",
        "sentenceIds": [
            1,
            2,
            3,
            4,
            5
        ],
        "start": 30
    }
]
```

#### output.customPromptPath的解析协议

最外层是一个array，具体字段如下：

JSON字段

类型

说明

\[i\].name

string

任务相应的dataId

\[i\].result

string

大模型返回结果。

\[i\].truncated

boolean

是否发生了截断。

示例json如下：

```
[
    {
        "name": "fgVnGvkqj5xA",
        "result": "这个问题似乎缺少一些具体的背景信息，比如“有几个人”是指在某个特定场景下，还是指某个特定群体中的人数。",
        "truncated": false
    }
]
```

## 请求示例

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
  "model": "tingwu-meeting",
  "input": {
    "dataId": "***",
    "task": "getTask"
  }
}'
```

## 返回示例

```
{
    "output": {
        "autoChaptersPath": "https://oss.example.com/...",
        "customPromptPath": "https://oss.example.com/...",
        "meetingAssistancePath": "https://oss.example.com/...",
        "playbackUrl": "https://oss.example.com/...",
        "pptExtractionPath": "https://oss.example.com/...",
        "status": 0,
        "summarizationPath": "https://oss.example.com/...",
        "textPolishPath": "https://oss.example.com/...",
        "transcriptionPath": "https://oss.example.com/...",
        "translationsPath": "https://oss.example.com/..."
    },
    "usage": {},
    "request_id": "ac5e2400-5aaf-44a6-8cf0-481bab4cefe3"
}
```
