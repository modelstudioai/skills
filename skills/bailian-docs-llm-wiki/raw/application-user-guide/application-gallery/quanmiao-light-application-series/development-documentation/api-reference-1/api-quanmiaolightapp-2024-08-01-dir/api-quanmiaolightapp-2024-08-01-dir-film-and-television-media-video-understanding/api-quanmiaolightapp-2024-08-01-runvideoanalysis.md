# RunVideoAnalysis - 视频理解-在线任务

阿里云百炼轻应用-影视传媒视频理解。

## 接口说明

阿里云百炼轻应用-视频理解：基于这接口，可以传入一个视频，进行字幕提取、视频内容分析、视频总结、标题抽取、思维导图生成等任务，也可以通过自定义 prompt 来实现差异化的视频内容生成。

-   欢迎前往[轻应用-影视传媒视频理解](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)直接体验。
    
-   通过 SDK 方式调用 API 可参考视频理解控制台“API”下的示例。
    
    **重要** 当通过 SDK 调用当前 API 时，因“**调试**”-OpenAPI 门户对 SSE 协议支持还不够完善，建议参考**调用示例**，详见[**轻应用-影视传媒视频理解**](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)\-切换**API 页签**。
    

## API-SDK 调用说明

### API 接口说明

调用视频理解 API 有 **2** 种方式，对应 2 个接口

-   调用[离线异步 API](https://help.aliyun.com/zh/model-studio/user-guide/api-quanmiaolightapp-2024-08-01-submitvideoanalysistask?spm=a2c4g.11186623.help-menu-2400256.d_1_2_4_3_1_3_3_1.3b2e46c2wjL7dc&scm=20140722.H_2867156._.OR_help-T_cn~zh-V_1)（**推荐**）：默认支持 2 并发，可以通过配置接口调整并发到 10，如果业务量大，可以联系客服（或运营等）申请更多并发，无需等待执行结束，异步调度，并发数等于后台同时跑的任务数，超过并发数的任务会排队，sdk 支持绝大部分开发语言，openapi 门户可以直接调试和使用，也可以到[**轻应用-影视传媒视频理解**](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)控制台，切换到“API” 页签下查看调用 demo。
    
-   调用[在线同步 API](https://help.aliyun.com/zh/model-studio/user-guide/api-quanmiaolightapp-2024-08-01-runvideoanalysis?spm=a2c4g.11186623.help-menu-2400256.d_1_2_4_3_1_3_3_0.396c36b9Pjqtm9&scm=20140722.H_2846254._.OR_help-T_cn~zh-V_1)（**不推荐**）：本文档对应接口，全局只有 **1** 并发，需保持链接等待结果，sdk 支持的语言有限（java、python），openapi 门户页面不支持调试和调用（sse）（copy 出来代码无法直接使用），一般少量体验用，调用需到[**轻应用-影视传媒视频理解**](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)控制台，切换到“API” 页签下查看调用 demo。
    

### 在线同步 API 调用说明

推荐**Java（异步 sdk）、Python**语言的 SDK，其中 Java（异步 sdk）依赖如下：

```
<dependency>
   <groupId>com.aliyun</groupId>
   <artifactId>alibabacloud-quanmiaolightapp20240801</artifactId>
   <version>取最新版本</version>
 </dependency>
```

-   获取[Java（异步）最新版本依赖](https://api.aliyun.com/api-tools/sdk/QuanMiaoLightApp?version=2024-08-01&language=java-async-tea&tab=primer-doc)。
    
-   获取[AccessKey ID、AccessKey Secret](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。
    

## 权限说明

### 前置条件

-   登录阿里云百炼控制台，确认阿里云百炼是开通可用状态。
    
-   主账号调用：默认有所有 API 调用权限。
    
-   子账号调用：子账号默认无权限（AccessForbid）调用当前 API，需要同时在 **RAM 控制台**和**阿里云百炼控制台**中做授权。
    

### RAM 控制台授权说明

去 [RAM 控制台](https://ram.console.aliyun.com/users)授权，具体 RAM 授权操作，参考 [RAM 文档](https://help.aliyun.com/zh/ram/user-guide/create-a-custom-policy)，步骤如下：

#### 方案一（推荐）：授予内置权限策略

授予子账号” [AliyunQuanMiaoLightAppFullAccess](https://ram.console.aliyun.com/policies/AliyunQuanMiaoLightAppFullAccess/System/content) “ 权限。

如果要同时访问控制台，请同时授予” [AliyunAiMiaoBiFullAccess](https://ram.console.aliyun.com/policies/AliyunAiMiaoBiFullAccess/System/content) “权限。

#### 方案二：自定义授权策略并赋予权限

适用于精细化管理 API 维度访问的场景。

-   **自定义授权策略**：菜单“**权限管理-权限策略**”下，创建权限策略，脚本编辑方式录入如下任意一个方案中 json。 授权子子账号指定接口，比如视频理解“RunVideoAnalysis”。
    

```
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "quanmiaolightapp:RunVideoAnalysis",
            "Resource": "*"
        }
    ]
}
```

如果要同时访问控制台，请同时授予如下接口权限。

```
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "aimiaobi:GetVideoAnalysisConfig",
            "Resource": "*"
        }
    ]
}
```

-   **给子账号授权**：菜单“**身份管理-用户**”下，找到对应用户，新增授权，切换自定义授权，添加上面自定义的授权策略。
    

### 阿里云百炼控制台授权说明

使用主账号或有阿里云百炼管理员权限的子账号，登录阿里云百炼控制台，在[权限管理-用户管理](https://bailian.console.aliyun.com/?tab=app#/authority)页面添加子账号。

## 接口部分入参取值说明

### 抽帧配置字段（frameSampleMethod）

用于调整抽帧的参数，包括抽帧间隔、抽帧像素。抽帧方式默认为标准方式，目前共提供三种方式可供选择，标准、快速/更低成本、自定义。

-   使用“标准”方式进行抽帧时，应用系统内置参数进行抽帧，抽帧间隔与抽帧像素无需用户自定义。标准方式抽帧间隔和抽帧像素取值规则为：
    -   根据视频时长选择不同档位，具体请参见[视频理解控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)，“效果调试”页签下的高级功能 > 抽帧方式 > 自定义中的“推荐取值范围 1.0 ~6.0”和“推荐取值范围 650 ~ 750”右侧的“？”提示信息。
        
    -   视频时长和档位映射关系为：取视频时长和档位时长举例最近的档，如果相同，取档位时长大的。
        
-   使用“快速/更低成本”方式进行抽帧时，应用系统内置参数系数运算后的结果进行抽帧，抽帧间隔与抽帧像素无需用户自定义。
    
-   使用“自定义”方式时，则需要用户传入抽帧间隔、抽帧像素两个参数，参数的取值范围对不同时长的视频存在不同的限制，取值范围具体计算规则如下：
    -   最小抽帧间隔 = max("标准"方式对应抽帧间隔 - 0.2，1)
        
    -   最大抽帧间隔 = "标准"方式对应抽帧间隔 + 5
        
    -   最小抽帧像素 = max("标准"方式对应抽帧像素 - 50，300)
        
    -   最大抽帧像素 = "标准"方式对应抽帧像素 + 50
        

## Agent 集成

Agent 可通过 Skill 直接使用视频理解能力：

-   **Skill 名称**：`alibabacloud-bailian-videoanalysis`
    
-   **Skill 地址**：[https://skills.aliyun.com/skills/alibabacloud-bailian-videoanalysis](https://skills.aliyun.com/skills/alibabacloud-bailian-videoanalysis)
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunVideoAnalysis)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunVideoAnalysis)

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

quanmiaolightapp:RunVideoAnalysis

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runVideoAnalysis HTTP/1.1
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

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/use-workspace)

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

视频链接

**说明**

-   videoUrl 字段必填（如果填写了 originalSessionId 字段，videoUrl 可不填）。
    
-   不支持上传本地视频，您需填入可下载的 URL 地址。
    

http://xxxx.mp4

videoModelId

string

否

视频 VL 任务模型唯一标识，支持的模型：

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

视频总结（文本加工）依赖的大模型唯一标识，支持的模型，如果文本加工阶段想跑多任务，可以走 textProcessTasks 字段，如果传入了 textProcessTasks，则当前字段和当前字段对应的 prompt 模版 id，prompt 模版将不再生效。

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

taskId

string

否

生成任务唯一标识：不传会默认生成

a3d1c2ac-f086-4a21-9069-f5631542f5a2

originalSessionId

string

否

源任务唯一标识：如果要基于历史任务重跑某个子任务（generateOptions 字段指定的），可以传入历史任务 taskId+originalSessionId，后台会加载历史任务已生成数据，跳过前置步骤，提升生成效率，如果后台数据过久，比如超过 7 天，查询失败，会默认重跑前置依赖子任务。

a3d1c2ac-f086-4a21-9069-f5631542f5ax

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

语音识别语言：

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
    

english

frameSampleMethod

object

否

抽帧模式选型

english

methodName

string

否

抽帧模式选项，可传参数包括

-   standard（标准）--默认
    
-   fast（快速/更低成本）
    
-   userdefined（自定义）
    

standard

interval

number

否

抽帧间隔：单位秒，仅在 userdefined 模式下有效

4

pixel

integer

否

抽帧像素：每一帧最大边像素，仅在 userdefined 模式下有效，取值范围是 300 到 768

400

videoRoles

array<object>

否

人物

array<object>

否

人物

roleName

string

否

人物名称

张三

roleInfo

string

否

人物信息

是个xx

urls

array

否

人物头像

string

否

人物头像

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

开始时间，单位毫秒

0

endTime

integer

否

结束时间，单位毫秒

1748491200000

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
    

qwen-max

modelCustomPromptTemplate

string

否

视频总结依赖的大模型 prompt 模版：必须同时包含{videoAsrText} 和 {videoAnalysisText}变量，{videoAsrText}是视频的 ASR 文本信息，{videoAnalysisText}是视频的各个子镜头的 VL 视觉信息（视觉语言分析结果）。

xxx

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

人物识别相似度阈值：（0~1）

0.7

videoShotFaceIdentityCount

integer

否

人物匹配时，单镜头(分镜)，参与匹配的抽帧（图片）数量：\[1~5\]

3

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

videoUrls

array

否

多视频 url

string

否

视频 url

http://xxx

addDocumentParam

object

否

指定数据集后：视频理解结果作为 meta 信息和视频一起上传到妙搜

datasetId

integer

否

数据集 id：如果期望上传到妙搜，这个字段必选

890

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

xxx

docId

string

否

文档业务唯一标识：同数据集会排重

xxx

categoryUuid

string

否

类目唯一标识

xxx

tags

array

否

标签

string

否

标签值

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

xxx

value

string

否

字段值

xx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应数据

header

object

流式输出 header 头，包含返回通用信息

errorCode

string

异常错误码

InvalidParam

errorMessage

string

异常错误信息

Pop sign mismatch, please check log.

event

string

事件类型

task-progress-start-generating

eventInfo

string

事件描述

可空

sessionId

string

一次生成唯一标识

xxx

taskId

string

生成唯一标识

xxx

traceId

string

链路 traceid

2150432017236011824686132ecdbc

payload

object

生成结果数据

output

object

输出内容对象

videoAnalysisResult

object

视频语言 vl 生成结果

generateFinished

boolean

当前任务是否已生成结束

true

text

string

生成内容

根据xxx

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

imageTokens

integer

图片识别 token 数量

20

videoShotAnalysisResults

array<object>

视频每个分镜对应语言分析结果：：因内容较大，请从 resultJsonFileUrl 文件中获取

object

视频每个分镜对应语言分析结果

endTime

integer

结束时间，相对时间，单位毫秒

10000

startTime

integer

开始时间，相对时间，单位毫秒

1000

text

string

分镜对应生成内容

根据xxx

modelId

string

实际使用的模型唯一标识

qwen-vl-max

videoCaptionResult

object

视频字幕结果

generateFinished

boolean

当前任务是否已生成结束

true

videoCaptions

array<object>

视频字幕列表

object

视频字幕

endTime

integer

结束时间：相对时间，单位毫秒

20000

endTimeFormat

string

结束时间，格式化结果：00:01

00:01

startTime

integer

开始时间，相对时间，单位毫秒

1000

startTimeFormat

string

开始时间，格式化结果：00:01

00:01

text

string

字幕内容

xxx

speaker

string

角色

张三

videoGenerateResult

object

视频总结结果

generateFinished

boolean

当前任务是否已生成结束

true

text

string

视频总结内容

根据xxx

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

modelId

string

实际使用的模型唯一标识

qwen-max

modelReduce

boolean

模型是否被降级：如果模型是 qwen-max 或 qwen-max-latest，且超过 prompt 输入上限时，会尝试降级到 qwen-plus-latest 模型，保证信息完整性

qwen-plus-latest

reasonText

string

模型思考过程

xxx

index

integer

多任务标号：1 开始

1

videoMindMappingGenerateResult

object

视频思维导图结果

generateFinished

boolean

当前任务是否已生成结束

true

text

string

生成原始内容

根据xxx

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

videoMindMappings

array<object>

思维导图

array<object>

思维导图

childNodes

array<object>

子节点

array<object>

子节点

childNodes

array<object>

子节点

object

子节点

name

string

节点描述

三级

name

string

节点描述

二级

name

string

节点描述

一级

modelId

string

实际使用的模型唯一标识

true

modelReduce

boolean

模型是否被降级：如果模型是 qwen-max 或 qwen-max-latest，且超过 prompt 输入上限时，会尝试降级到 qwen-plus-latest 模型，保证信息完整性

true

videoTitleGenerateResult

object

视频标题结果

generateFinished

boolean

当前任务是否已生成结束

true

text

string

生成内容

标题

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

modelId

string

实际使用的模型唯一标识

qwen-max

modelReduce

boolean

模型是否被降级：如果模型是 qwen-max 或 qwen-max-latest，且超过 prompt 输入上限时，会尝试降级到 qwen-plus-latest 模型，保证信息完整性

true

videoShotSnapshotResult

object

切片抽帧结果：因内容较大，请从 resultJsonFileUrl 文件中获取

videoShots

array<object>

片段列表

array<object>

片段

startTime

integer

开始时间：相对时间，单位 ms

0

endTime

integer

结束时间：相对时间，单位 ms

0

startTimeFormat

string

开始时间（格式化）：相对时间，比如 00:01

00:01

endTimeFormat

string

结束时间（格式化）：相对时间，比如 00:01

00:02

videoSnapshots

array<object>

帧列表

object

帧

url

string

帧 url：带有效期的可公网访问地址，如需要下载，请在有效期内下载

http://xxx

resultJsonFileUrl

string

结果 json 文件地址：

由于响应结果过大，部分数据获取改为文件方式，可以通过当前字段 url 下载文件，并解析使用：

-   当前包含的字段：数据结构定义见 RunVideoAnalysis 接口
    -   videoShotSnapshotResult：每个分片抽帧信息，包括每帧 url
        
    -   videoShotAnalysisResults：每个分片语言分析结果明细
        
-   其他字段获取方式不变，文本方式返回。
    
-   文件类型：json
    
-   文件内容：全量报文，包含文本方式返回的 返回 event：task-finished
    

http://

videoGenerateResults

array<object>

当入参为多任务时（textProcessTasks 有值），返回文本加工结果对应这个字段，可以通过数据所在数组位置（下标）或 index（1 开始）找到对应结果。

array<object>

文本分析结果

generateFinished

boolean

当前任务是否已生成结束

true

modelId

string

模型 ID

qwen-max-latest

index

integer

序号：1 开始

1

text

string

视频总结内容

xxx

reasonText

string

模型思考过程

xxx

usage

object

用量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

videoRoleRecognitionResult

object

自动识别结果

videoRoles

array<object>

角色列表

array<object>

roleName

string

角色名称

test-role

roleInfo

string

人物信息描述

角色身份

timeIntervals

array<object>

出场时间段

object

startTime

integer

开始时间，单位毫秒

0

endTime

integer

结束时间，单位毫秒

1735535279000

timestamp

integer

角色出现时间

23333333

url

string

图片 url

https://img.alicdn.com/imgextra/i1/O1CN01qtgazV1oZ3djafcFz\_!!6000000005238-0-tps-1540-1540.jpg

ratio

number

出场率

0.06

isAutoRecognition

boolean

自动识别是否使用的是自动识别单独的视频地址（是：则人脸图片无法使用时间与视频帧用时间对应，因为可能是不同的视频）

true

videoCalculatorResult

object

费用估算结果

items

array<object>

计费项明细

object

计费项明细

name

string

计费项名称

xxx

type

string

计费项类型

模型推理

inputToken

integer

输入 token

123

outputToken

integer

输出 token

13

time

integer

计费时长

9

inputExpense

number

输入 token 价格

0.234

outputExpense

number

输出 token 价格

0.124

timeExpense

number

时间计费

0.02

totalExpense

number

总计费

0.378

addDatasetDocumentsResult

object

自动保存执行结果

status

integer

自动保存任务状态：1 成功，0 失败

1

title

string

视频名称

xxx

docId

string

视频 docId

xxx

errorMessage

string

如果自动保存失败，则输出错误信息

xxx

docUuid

string

视频的 docUuid

uuid

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

requestId

string

请求唯一标识

117F5ABE-CF02-5502-9A3F-E56BC9081A64

## 示例

正常返回示例

`JSON`格式

```
{
  "header": {
    "errorCode": "InvalidParam",
    "errorMessage": "Pop sign mismatch, please check log.",
    "event": "task-progress-start-generating",
    "eventInfo": "可空",
    "sessionId": "xxx",
    "taskId": "xxx",
    "traceId": "2150432017236011824686132ecdbc"
  },
  "payload": {
    "output": {
      "videoAnalysisResult": {
        "generateFinished": true,
        "text": "根据xxx",
        "usage": {
          "inputTokens": 1,
          "outputTokens": 1,
          "totalTokens": 2,
          "imageTokens": 20
        },
        "videoShotAnalysisResults": [
          {
            "endTime": 10000,
            "startTime": 1000,
            "text": "根据xxx"
          }
        ],
        "modelId": "qwen-vl-max"
      },
      "videoCaptionResult": {
        "generateFinished": true,
        "videoCaptions": [
          {
            "endTime": 20000,
            "endTimeFormat": "00:01",
            "startTime": 1000,
            "startTimeFormat": "00:01",
            "text": "xxx",
            "speaker": "张三"
          }
        ]
      },
      "videoGenerateResult": {
        "generateFinished": true,
        "text": "根据xxx",
        "usage": {
          "inputTokens": 1,
          "outputTokens": 1,
          "totalTokens": 2
        },
        "modelId": "qwen-max",
        "modelReduce": true,
        "reasonText": "xxx",
        "index": 1
      },
      "videoMindMappingGenerateResult": {
        "generateFinished": true,
        "text": "根据xxx",
        "usage": {
          "inputTokens": 1,
          "outputTokens": 1,
          "totalTokens": 2
        },
        "videoMindMappings": [
          {
            "childNodes": [
              {
                "childNodes": [
                  {
                    "name": "三级"
                  }
                ],
                "name": "二级"
              }
            ],
            "name": "一级"
          }
        ],
        "modelId": "true",
        "modelReduce": true
      },
      "videoTitleGenerateResult": {
        "generateFinished": true,
        "text": "标题",
        "usage": {
          "inputTokens": 1,
          "outputTokens": 1,
          "totalTokens": 2
        },
        "modelId": "qwen-max",
        "modelReduce": true
      },
      "videoShotSnapshotResult": {
        "videoShots": [
          {
            "startTime": 0,
            "endTime": 0,
            "startTimeFormat": "00:01",
            "endTimeFormat": "00:02",
            "videoSnapshots": [
              {
                "url": "http://xxx"
              }
            ]
          }
        ]
      },
      "resultJsonFileUrl": "http://",
      "videoGenerateResults": [
        {
          "generateFinished": true,
          "modelId": "qwen-max-latest",
          "index": 1,
          "text": "xxx",
          "reasonText": "xxx",
          "usage": {
            "inputTokens": 1,
            "outputTokens": 1,
            "totalTokens": 2
          }
        }
      ],
      "videoRoleRecognitionResult": {
        "videoRoles": [
          {
            "roleName": "test-role",
            "roleInfo": "角色身份",
            "timeIntervals": [
              {
                "startTime": 0,
                "endTime": 1735535279000,
                "timestamp": 23333333,
                "url": "https://img.alicdn.com/imgextra/i1/O1CN01qtgazV1oZ3djafcFz_!!6000000005238-0-tps-1540-1540.jpg"
              }
            ],
            "ratio": 0.06,
            "isAutoRecognition": true
          }
        ]
      },
      "videoCalculatorResult": {
        "items": [
          {
            "name": "xxx",
            "type": "模型推理",
            "inputToken": 123,
            "outputToken": 13,
            "time": 9,
            "inputExpense": 0.234,
            "outputExpense": 0.124,
            "timeExpense": 0.02,
            "totalExpense": 0.378
          }
        ]
      },
      "addDatasetDocumentsResult": {
        "status": 1,
        "title": "xxx",
        "docId": "xxx",
        "errorMessage": "xxx",
        "docUuid": "uuid"
      }
    },
    "usage": {
      "inputTokens": 1,
      "outputTokens": 1,
      "totalTokens": 2
    }
  },
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/RunVideoAnalysis#workbench-doc-change-demo)。
