# SubmitVideoAnalysisTask - 视频理解-提交异步任务

阿里云百炼轻应用-提交视频理解离线异步任务。

## 接口说明

### 异步任务说明

区别于在线同步接口，提交异步任务后实时返回，无需等待执行结束。任务由后台异步调度（排队、并行），结果可通过"获取异步任务状态和结果"接口查询。

### 接口调用说明

-   支持绝大部分开发语言 SDK 方式接入
    
-   可在 OpenAPI 门户 直接调试和使用
    
-   也可前往 [轻应用-影视传媒视频理解控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)，切换到"API"页签查看调用 Demo
    

### 并发说明

项目

说明

默认并发

2 并发（异步任务运行并发，非接口调用并发）

可调上限

通过 `UpdateVideoAnalysisConfig` 配置接口可调整至 30

更高并发

业务量大可联系客服或运营申请更多并发

排队机制

并发数 = 后台同时运行的任务数，超过并发数的任务自动后台排队

### 角色识别说明

-   通过 API 接口实现"识别视频中的人物身份"
    
-   **默认可识别**：16 个人物，每个角色 1 张图片
    
-   **放宽限制**：如需进一步放宽，请加入钉钉群 `116015001424` 联系产研
    
-   **超时风险**：一个视频理解任务中做太多次人物角色匹配，存在超时风险
    

### 调度轮询最佳实践

因接口调用并发有限制，建议如下：

-   **扩并发**：扩的是异步处理任务的并发，非提交任务接口的并发
    
-   **提交任务**：理论串行即可。任务多时可适当 2~3 个并发提交
    
-   **结果轮询**：任务按提交顺序调度，只需周期轮询最早未完成的 top n（n == 异步任务并发数）即可。更多任务状态只会是排队中，轮询意义不大
    

### Agent 集成

Agent 可通过 Skill 直接使用视频理解能力：

-   **Skill 名称**：`alibabacloud-bailian-videoanalysis`
    
-   **Skill 地址**：[https://skills.aliyun.com/skills/alibabacloud-bailian-videoanalysis](https://skills.aliyun.com/skills/alibabacloud-bailian-videoanalysis)
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitVideoAnalysisTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitVideoAnalysisTask)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

quanmiaolightapp:SubmitVideoAnalysisTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/videoAnalysis/submitVideoAnalysisTask HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

videoUrl

string

否

视频 url

http://xxxx.mp4

videoModelId

string

否

视频 vl 任务模型唯一标识，支持的模型：

-   quanmiao-vl-turbo
    
-   quanmiao-vl-plus
    
-   quanmiao-vl-max-thinking
    
-   quanmiao-vl-max
    
-   Qwen-VL-Post
    

quanmiao-vl-turbo

videoModelCustomPromptTemplate

string

否

视频 vl 任务 prompt 模版：必须包含{videoAsrText}变量，{videoAsrText}是视频的 ASR 文本信息，默认取页面看到的默认值。

\# 角色 你是一名视频分析师，擅长对各种视频片段进行理解。 # 任务描述 给你一个视频片段的多张关键帧图片，请你完成以下任务。 - 输出每张图片的画面信息，包括人物、物体、动作、文字、字幕、镜头语言等。 - 把每张图片的信息串联起来，生成视频的详细概述，还原该片段的剧情。 # 限制 - 分析范围严格限定于提供的视频子片段，不涉及视频之外的任何推测或背景信息。 - 总结时需严格依据视频内容，不可添加个人臆测或创意性内容。 - 保持对所有视频元素（尤其是文字和字幕）的高保真还原，避免信息遗漏或误解。 # 输入数据 ## 视频片段ASR信息 （如果输入为空则忽略ASR信息） {videoAsrText} # 输出格式 直接按照任务目标里即可,先输出每张图片的描述，再串联起来输出整个视频片段的剧情。

modelId

string

否

视频总结（文本加工）依赖的大模型唯一标识，

**如果文本加工阶段想跑多任务**，可以走 textProcessTasks 字段，如果传入了 textProcessTasks，则当前字段和当前字段对应的 prompt 模版 id，prompt 模版将不再生效。

-   quanmiao-llm-max
    
-   quanmiao-llm-max-thinking
    
-   quanmiao-llm-plus
    
-   quanmiao-llm-turbo
    

quanmiao-llm-max

modelCustomPromptTemplateId

string

否

视频总结依赖的大模型 prompt 模版唯一标识：

-   PlotDetail：剧情详解（默认）；
    
-   Summary：内容概述；
    
-   ExtractVideoTag：提取标签；
    
-   ExplosivePointAnalysis：爆点分析；
    
-   MultiTask：多类任务；
    

如果 modelCustomPromptTemplate 未传，则会取模版唯一标识对应的默认 prompt，modelCustomPromptTemplate 优先级高于 modelCustomPromptTemplateId。

PlotDetail

modelCustomPromptTemplate

string

否

视频总结依赖的大模型 prompt 模版：必须同时包含{videoAsrText} 和 {videoAnalysisText}变量，{videoAsrText}是视频的 ASR 文本信息，{videoAnalysisText}是视频的各个子镜头的 VL 视觉信息（视觉语言分析结果）。

\# 角色 你是一个专业的视频标注专员，擅长结合视频镜头信息来分析处理各种视频任务。 # 任务目标 请你结合输入数据串联、还原出整个视频的详细剧情。 # 限制 1.如出现语法上错误，或逻辑不通，请直接修改 2.在视频分镜中，如果包含台词，可能会出现说话者与其所说内容不匹配的情况。因此，必须根据剧情的进展，准确判断每段台词的真实说话者 3.如果视频分镜中无台词，请根据视频音频文字为其匹配台词 4.修改后的故事请适当保留视频分镜中对人物、场景的描写 5.帮忙润色一下故事，使其更具逻辑性 6.结合视频分镜中的人物外观特点，如果有外观相近的人物是同一个角色。因此，需要将不同分镜中的人物角色统一。 # 输入数据 ## 资料一：视频分镜信息（视频各镜头的视觉描述信息） {videoAnalysisText} ## 资料二：视频ASR转录信息（未标注出说话者，可能有错误和遗漏，如果没有输入ASR，则忽略此信息） {videoAsrText} # 输出格式 直接输出视频剧情，不要输出其他信息。

generateOptions

array

否

视频理解生成任务选项。

string

否

视频理解生成任务选项：包含的任务，会自动前置执行。

-   videoAnalysis：视频语言分析（VL）：如果仅传次值，则运行到视频语言分析后就结束了，不再跑后面的文本加工等子任务；
    
-   **videoGenerate：文本加工-视频总结（默认）**，包含 videoAnalysis；
    
-   videoTitleGenerate：视频标题生成，包含 videoAnalysis、videoGenerate；
    
-   videoMindMappingGenerate：视频思维导图生成，包含 videoAnalysis、videoGenerate；videoRoleRecognition：角色自动识别。
    

videoGenerate

videoExtraInfo

string

否

和视频相关的补充文字资料：您可以自定义扩展文本素材，应用到生成中，需要手动调整 prompt 模版，增加{videoExtraInfo}变量，传入的内容可以是视频摘要、视频简介或视频 ASR 转录信息。

视频描述了：xx

snapshotInterval

number

否

抽帧间隔：X 秒一帧，取值范围\[1, 10\]，间隔越大模型能提取到的信息越少，耗时越长，成本越高，默认已是最佳实践，一般无需修改，如果要修改，请根据视频时长来定，建议\[1~3\]。 建议使用：当前字段优先级高于 frameSampleMethod.interval，一般场景可以使用 frameSampleMethod 字段自定义（userdefined）模式下的 interval，区别在于 frameSampleMethod 自定义模式 interval 取值需要在指定的视频时长对应抽帧间隔范围内。

2

splitInterval

integer

否

视频分镜最小间隔：单位秒，取值范围\[1, 150\]，默认根据视频长度取推荐值

10

language

string

否

语言，可传参数

-   chinese：中文（默认）
    
-   french：法语
    
-   english：英语
    
-   japanese：日语
    
-   chineseEnglishFreely：中英文自由说
    
-   arabic：阿拉伯语
    
-   korean：韩语
    
-   malay：马来语
    
-   thai：泰语
    
-   portuguese：葡萄牙语
    
-   spanish：西班牙语
    
-   indonesian：印尼语
    
-   vietnamese：越南语
    

chinese

frameSampleMethod

object

否

抽帧方式

english

methodName

string

否

抽帧类型，可传参数包括

-   fast：快速/更低成本
    
-   standard：标准（默认）
    
-   userdefined：自定义
    

standard

interval

number

否

抽帧间隔：单位秒，仅在 userdefined 模式下有效

2

pixel

integer

否

抽帧像素：每一帧最大边像素，仅在 userdefined 模式下有效，取值范围是 300 到 768

768

videoRoles

array<object>

否

识别视频中的人物身份列表

array<object>

否

识别视频中的人物身份

roleName

string

否

人物名称

张三

roleInfo

string

否

人物信息描述

张三是一个男生

urls

array

否

人物头像地址

string

否

人物头像地址

http://xxx

isAutoRecognition

boolean

否

自动识别是否使用的是自动识别单独的视频地址（是：则人脸图片无法使用时间与视频帧用时间对应，因为可能是不同的视频）

false

timeIntervals

array<object>

否

角色出场时间段列表

object

否

startTime

integer

否

开始时间

0

endTime

integer

否

结束时间

345546789

textProcessTasks

array<object>

否

视频总结(文本加工)任务列表:最多支持 3 个

object

否

视频总结(文本加工)任务

modelId

string

否

视频总结依赖的大模型唯一标识，支持的模型

-   qwen-max-latest
    
-   qwen-max
    
-   qwen-plus-latest
    
-   qwen-plus
    
-   qwen2.5-7b-instruct-1m
    
-   deepseek-r1
    

qwen-max-latest

modelCustomPromptTemplate

string

否

视频总结依赖的大模型 prompt 模版：必须同时包含{videoAsrText} 和 {videoAnalysisText}变量，{videoAsrText}是视频的 ASR 文本信息，{videoAnalysisText}是视频的各个子镜头的 VL 视觉信息（视觉语言分析结果）。

xx

modelCustomPromptTemplateId

string

否

视频总结依赖的大模型 prompt 模版唯一标识：

-   PlotDetail：剧情详解（默认）；
    
-   Summary：内容概述；
    
-   ExtractVideoTag：提取标签；
    
-   ExplosivePointAnalysis：爆点分析；
    
-   MultiTask：多类任务；
    

如果 modelCustomPromptTemplate 未传，则会取模版唯一标识对应的默认 prompt，modelCustomPromptTemplate 优先级高于 modelCustomPromptTemplateId。

PlotDetail

faceIdentitySimilarityMinScore

number

否

人物识别相似度阈值：0~1

0.7

videoShotFaceIdentityCount

integer

否

人物匹配时，单镜头(分镜)，参与匹配的抽帧（图片）数量：\[1~5\]

2

deduplicationId

string

否

排重字段：可以根据业务需要和业务场景定义自己的业务唯一标识，当前字段重复的数据，系统会保证至少 72h 内不允许重复提交

1

excludeGenerateOptions

array

否

排除的生成步骤：

-   videoCaption：视频语音识别
    

string

否

排除的生成步骤：

-   videoCaption：视频语音识别
    

\[\\"videoCaption\\"\]

videoCaptionInfo

object

否

字幕（asr）信息

videoCaptions

array<object>

否

字幕（ASR）内容，和 videoCaptionsFIleUrl 二选一

object

否

字幕（asr）内容

startTime

integer

否

当前句子开始时间：毫秒

1000

endTime

integer

否

当前句子结束时间：毫秒

10000

text

string

否

内容

你好

speaker

string

否

角色

张三

videoCaptionFileUrl

string

否

视频字幕（ASR）文件

oss:// | http://

autoRoleRecognitionVideoUrl

string

否

自动识别功能单独的视频地址 Url

http://

splitType

string

否

分镜类型：minDuration(限制分镜最小时长), fixDuration(按照固定时长分镜)，默认采用 minDuration 模式

fixDuration

addDocumentParam

object

否

指定数据集后：视频理解结果作为 meta 信息和视频一起上传到妙搜

datasetId

integer

否

数据集 id：如果期望上传到妙搜，这个字段必选

3031

datasetName

string

否

数据集名称

xxx

document

object

否

上传妙搜相关参数：不录入会自动生成

title

string

否

视频名称

xx

docId

string

否

文档业务唯一标识：同数据集会排重

xxx

categoryUuid

string

否

文档类目唯一标识

xx

tags

array

否

标签

string

否

标签

xx

extend1

string

否

扩展字段 1

xx

extend2

string

否

扩展字段 2

xx

extend3

string

否

扩展字段 3

xx

metadata

object

否

元数据

keyValues

array<object>

否

keyValue 结构的元数据

object

否

keyValue 结构的元数据

key

string

否

字段名称

summary

value

string

否

字段值

xxx

videoUrls

array

否

多视频 url

string

否

多视频 url：会合并成一个视频处理，适合短视频场景

xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

requestId

string

请求唯一标识

085BE2D2-BB7E-59A6-B688-F2CB32124E7F

success

boolean

是否成功：true 成功，false 失败

True

code

string

状态码

xx

message

string

错误说明

success

httpStatusCode

integer

http 状态码

200

data

object

结果

taskId

string

任务唯一标识

3feb69ed02d9b1a17d0f1a942675d300

## 示例

正常返回示例

`JSON`格式

```
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

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/SubmitVideoAnalysisTask#workbench-doc-change-demo)。
