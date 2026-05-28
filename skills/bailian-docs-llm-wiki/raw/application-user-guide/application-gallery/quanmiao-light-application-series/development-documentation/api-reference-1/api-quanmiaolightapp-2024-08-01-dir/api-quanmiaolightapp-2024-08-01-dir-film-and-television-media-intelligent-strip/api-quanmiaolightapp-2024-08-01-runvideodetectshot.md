# RunVideoDetectShot - 智能拆条-在线任务

轻应用-视频拆条 使用视频拆条需先开通影视传媒视频理解（免费开通）https://bailian.console.aliyun.com/?tab=app#/app/app-market/quanmiao/video-comprehend 目前拆条提供三种场景视频的处理： 1、节目场景 2、新闻场景 3、其他场景 详细使用建议及参考prompt请查看下方补充说明。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunVideoDetectShot)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunVideoDetectShot)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

quanmiaolightapp:RunVideoDetectShot

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runVideoDetectShot HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

阿里云百炼业务空间唯一标识

llm-xxxxxxx

videoUrl

string

是

视频的地址

https://xxx.mp4

modelId

string

否

llm 的模型，推荐选择 deepseek-r1 可选项：

-   deepseek-r1
-   quanmiao-llm-max
-   quanmiao-llm-max-thinking
-   quanmiao-llm-plus
-   quanmiao-llm-turbo

deepseek-r1

options

array

是

用户选择使用什么方式进行分镜，可选项：ASR

string

是

ASR

ASR

taskId

string

否

任务唯一标识

a3d1c2ac-f086-4a21-9069-f5631542f5a2

originalSessionId

string

否

源任务唯一标识：如果要基于历史任务重跑某个子任务（generateOptions 字段指定的），可以传入历史任务 taskId+originalSessionId，后台会加载历史任务已生成数据，跳过前置步骤，提升生成效率，如果后台数据过久，比如超过 7 天，查询失败，会默认重跑前置依赖子任务。

a3d1c2ac-f086-4a21-9069-f5631542f5ax

prompt

string

否

llm 用户自定义 prompt

xxx

modelCustomPromptTemplateId

string

否

llm 生成拆条结果 prompt 的 ID

videoDetectShotShowPrompt

modelVlCustomPromptTemplateId

string

否

vl 识别 prompt 的 ID

videoDetectShotVlShowPrompt

recognitionOptions

array

是

用户选择使用什么方式对每个分镜进行内容识别，可选项：ASR，OCR，VL，可多选

string

是

ASR

ASR

intelliSimpPromptTemplateId

string

否

大语言模型前置简化 promptId

intelliSimpShowPrompt

preModelId

string

否

执行 intelliSimpPrompt 的模型，推荐选择 quanmiao-llm-max 可选项：

-   deepseek-r1
-   quanmiao-llm-max
-   quanmiao-llm-max-thinking
-   quanmiao-llm-plus
-   quanmiao-llm-turbo

quanmiao-llm-max

intelliSimpPrompt

string

否

简化输入给 llm 的数据的 prompt（用户自定义）

xxx

vlPrompt

string

否

用户自定义的 vl 识别 prompt

xxx

language

string

否

语音识别语言：

chinese：中文（默认） french：法语 english：英语 japanese：日语 chineseEnglishFreely：中英文自由说 arabic：阿拉伯语 korean：韩语 malay：马来语 thai：泰语 portuguese：葡萄牙语 spanish：西班牙语 indonesian：印尼语 vietnamese：越南语

chinese

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

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

task-finished

eventInfo

string

事件描述

可空

sessionId

string

会话唯一标识

14d15c78c4c34d428212f4d923d4ede1

taskId

string

任务唯一标识

xxxx

traceId

string

全链路唯一标识

3b5287b317477940746851672dca0c

payload

object

生成结果数据

output

object

输出内容对象

videoSplitResult

object

结果

text

string

拆条结果

xxx

reasonText

string

深度思考结果

xxx

videoParts

array<object>

拆条结果结构化，如果结构化失败则参数不存在，请根据 text 的返回结果进行解析；参数可通过 prompt 进行自定义调整，可参考 modelCustomPromptTemplateId（通过/getLightAppGeneralConfig 接口获取）进行改写

视频拆条结构化列表

object

string

xxx

xxx

videoRecognitionResult

array<object>

视频识别结果列表，根据入参的 recognitionOptions 选项进行视频内容识别后的结果

识别结果

object

startTime

long

当前识别结果的开始时间

1756433675000

endTime

long

当前识别结果的结束时间

1755742611000

asr

string

音频转文字的结果

xxx

ocr

string

画面中的文字内容识别结果

xxx

vl

string

画面内容识别结果

xxx

usage

object

token 消耗

inputTokens

long

输入 token 数

4546

outputTokens

long

输出 Token 数

820

totalTokens

long

总 token 数

5366

requestId

string

Id of the request

58868FD6-53D7-5ACD-80F7-854C8EA256EF

## 示例

正常返回示例

`JSON`格式

```
{
  "header": {
    "errorCode": "InvalidParam",
    "errorMessage": "Pop sign mismatch, please check log.",
    "event": "task-finished",
    "eventInfo": "可空",
    "sessionId": "14d15c78c4c34d428212f4d923d4ede1",
    "taskId": "xxxx",
    "traceId": "3b5287b317477940746851672dca0c"
  },
  "payload": {
    "output": {
      "videoSplitResult": {
        "text": "xxx",
        "reasonText": "xxx",
        "videoParts": [
          {
            "key": "xxx"
          }
        ],
        "videoRecognitionResult": [
          {
            "startTime": 1756433675000,
            "endTime": 1755742611000,
            "asr": "xxx",
            "ocr": "xxx",
            "vl": "xxx"
          }
        ]
      }
    },
    "usage": {
      "inputTokens": 4546,
      "outputTokens": 820,
      "totalTokens": 5366
    }
  },
  "requestId": "58868FD6-53D7-5ACD-80F7-854C8EA256EF"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-10-20

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/RunVideoDetectShot?updateTime=2025-10-20#workbench-doc-change-demo)

目前拆条提供三种场景视频的处理： 1、节目场景 2、新闻场景 3、其他场景

针对节目场景的视频： 推荐使用 ASR 方式分镜，视频识别选择 ASR+VL； modelVlCustomPromptTemplateId 建议选择节目 vl 模版（videoDetectShotVlShowPrompt），或者通过 vlPrompt 字段自定义 prompt； modelCustomPromptTemplateId 建议选择节目模版（videoDetectShotShowPrompt），或者通过 prompt 字段进行自定义； 建议开启简化 llm 入参文本功能（使用 intelliSimpPromptTemplateId 或 intelliSimpPrompt）； intelliSimpPromptTemplateId 选择 intelliSimpShowPrompt 时，modelCustomPromptTemplateId 建议使用 videoDetectShotShowPrompt； intelliSimpPromptTemplateId 选择 intelliSimpSecondShowPrompt 时，modelCustomPromptTemplateId 建议使用 videoDetectShotSecondShowPrompt； preModelId 推荐选择 quanmiao-llm-max，modelId 推荐选择 deepseek-r1；

针对新闻场景的视频： 新闻类视频通常音频较为标准清晰，推荐在识别视频内容时只选择 ASR，使用 ASR 方式分镜； 如果启用 vl（不推荐），modelVlCustomPromptTemplateId 建议选择新闻 vl 模版、videoDetectShotVlNewsPrompt，或者通过 vlPrompt 字段自定义 prompt； modelCustomPromptTemplateId 建议选择新闻模版（videoDetectShotNewsPrompt），或者通过 prompt 字段进行自定义； preModelId 推荐选择 quanmiao-llm-max，modelId 推荐选择 deepseek-r1；

针对其他场景的视频： 如果音频清晰且能覆盖到该视频的主要信息，推荐优先尝试使用 ASR 方式分镜，视频识别选择 ASR。 如果视频本身的信息量较小或在视频识别步骤中获取到的信息较少，推荐优先尝试不使用 intelliSimpPromptTemplateId 和 intelliSimpPrompt；

如果希望自定义 prompt 可以参考如下示例模版：

```
- name: videoDetectShotNewsPrompt
    # 角色
    你是一个专业的新闻合并助手，请根据以下要求处理给定的多个有序新闻片段的合并任务
    核心能力：根据新闻主题精准合并信息 + 严格遵循时间标注 + 智能标题提炼
    必须严格按照给定的输出格式输出

    # 输入数据格式：
    时间区间：[开始时间]-[结束时间]，当前时间段内容：[X]，话者 id：[Y]
    （话者 id 是当前说话的人的 id）  
    
    # 任务执行步骤：
      0.预处理：
        通读全文，联系上下文，理解每个新闻片段的含义和主题。
    
      1.比较两个新闻片段：
        先看第一个新闻片段和第二个新闻片段，判断它们是否能合并成一个片段。
        如果可以合并跳转步骤 2，否则跳转步骤 3。
    
      2.如果可以合并：
        把这两个片段合并成一个新的片段。
        新片段的开始时间是第一个片段的开始时间。
        新片段的结束时间是第二个片段的结束时间。
        然后，用这个新合并的片段继续和下一个片段比较，重复步骤 1。
    
      3.如果不能合并：
        把第一个片段单独作为一个独立的新闻片段。
        这个独立片段的开始时间不变。
        结束时间是第二个片段的开始时间减去一秒。
        接着，用第二个片段继续和下一个片段比较，重复步骤 1。
    
    # 合并标准（至少满足一条则进行合并）：
    - 两个片段属于同一新闻主题
    - 两个片段无法判断是否属于同一主题，但根据给定信息，合并后并不存在冲突
    
    # 排序逻辑说明：
    保持原始时间顺序
    
    # 输入示例：
    时间区间：00:00:04-00:00:26，当前时间段内容：首先我们来关注天气，话者 id：1
    时间区间：00:00:28-00:00:45，当前时间段内容：xxxx，话者 id：2
    时间区间：00:00:46-00:00:55，当前时间段内容：体育新闻，话者 id：1
    
    # 输出格式要求：
    ## 输出示例如下:
    ```json
    {
        "results": [
          {
            "startTime":"00:00:04",
            "endTime":"00:00:26",
            "title":"天气预报",
            "summary":"北京当天的天气预报"
          },
          {
            "startTime":"00:00:27",
            "endTime":"00:00:45",
            "title":"国际新闻",
            "summary":"国际新闻的内容"
          }
        ]
    }
    ```
    ## 输出数据内容要求：
    startTime：开始时间，格式为 HH:mm:ss
    endTime：结束时间，格式为 HH:mm:ss
    title：条目标题，简洁概括当前条目主体事件
    summary：条目简介，概括当前条目的核心内容

    # 现在请处理以下输入数据：
    {query}

- name: videoDetectShotShowPrompt
    ### **理想输出结果**
    每个节目都独立在一个区间内，节目间的主持内容也独立在一个区间内
    ### **任务要求**
      你是一名节目现场导演，请根据输入的时间区间内容：
      1. **合并连续相同节目区间**（相同内容/主题）
      2. **识别转场部分单独处理**
      3. 为每个最终区间生成标题和简介
      4.将连续的转场、广告等相同主题的非节目内容合并为一个时间区间
    
      **核心规则**：
      1. 标题规则：
    - 节目内容：体现核心主题（如“体育新闻”）
    - 转场内容：统一命名为“转场”
    - 禁止臆造未提及的节目名称
      2. 合并规则：
    - 节目间主持、广告以及其他转场内容如果连续则需要合并在一个区间内，注意，以上三类内容任意两类连续出现都要合并
    - 连续且内容同属相同节目的区间必须合并为一个区间
    - 禁止合并不同节目内容
    - 转场禁止与节目内容合并
    
    - 无具体内容的时间区间必须与上一个时间区间合并，但转场部分必须独立在一个区间内（例如：转场主持）
      3. 内容总结规则：
    - 用 1 句简洁总结核心内容（≤20 字）
    - 多元素内容聚焦最核心主题
    - 避免重复描述相似内容
    - 确保内容独立，不依赖其他区间
      4. 转场识别：主持人串场、无具体内容的过渡视为转场
    
      **输出格式**：
      ```json
      {
        "results": [
          {
            "startTime": "HH:mm:ss",
            "endTime": "HH:mm:ss",
            "title": "标题",
            "summary": "简介"
          }
        ]
      }
      处理流程：
    
      顺序扫描时间区间
      按照上述规则对符合条件的区间进行合并
      对每个最终区间：
      识别是否转场 → 是：标题=“转场”
      非转场 → 提炼核心主题作为标题
      用 1 句话总结核心内容
    
    ### **排序规则**
    - 按照时间顺序排列，保持输入的原始顺序。
    
      ### **输入示例**
      ```
      时间区间：00:00:04-00:00:26，当前时间段内容：首先我们来关注天气，话者 id：1
      时间区间：00:00:28-00:00:45，当前时间段内容：接下来是国际新闻，今天的主要事件包括……，话者 id：2
      时间区间：00:00:46-00:00:55，当前时间段内容：体育新闻，最新比赛结果如下……，话者 id：1
      ```
    
      ### **输出格式**
      ```json
      {
      "results": [
        {
          "startTime": "HH:mm:ss",  // 开始时间
          "endTime": "HH:mm:ss",    // 结束时间
          "title": "条目标题",       // 简洁概括当前条目主题
          "summary": "条目简介"      // 核心内容总结
        }
      ]
    }
      ```
    
      ### **输出示例**
      ```json
      {
        "results": [
          {
            "startTime": "00:00:04",
            "endTime": "00:00:26",
            "title": "天气预报",
            "summary": "介绍当天北京的天气情况。"
          },
          {
            "startTime": "00:00:28",
            "endTime": "00:00:45",
            "title": "国际新闻",
            "summary": "报道今日国际重要事件。"
          },
          {
            "startTime": "00:00:46",
            "endTime": "00:00:55",
            "title": "体育新闻",
            "summary": "更新最新体育赛事结果。"
          }
        ]
      }
      ``` 
    ### **请处理以下输入数据**
    {query}

- name: videoDetectShotSecondShowPrompt
    ### **理想输出结果**
    每个节目都独立在一个区间内，节目间的其他内容也独立在一个区间内
    ### **任务要求**
      你是一名节目现场导演，请根据输入的时间区间识别内容：
      1.识别视频属于什么类型的节目，以及除节目之外的其他内容属于什么类型（例如广告、报幕等）
      2.合并连续相同的节目区间（相同内容/主题）及除节目之外的其他内容区间（相同内容/主题）
      3.对于属于节目的视频区间，提炼内容并进行概括总结；如果不属于节目的其他内容区间（例如广告、报幕等），提炼内容并概括归纳为更简洁的信息，对于相同类型的其他内容，如果内容较短可作适当合并
      4.对于视频中含有多个节目区间的，需对不同的节目进行分割，概括总结内容并逐一输出；对于视频中只含有一个节目的，需提炼节目内容，后根据节目内的不同内容/主题进行分割，概括总结内容并逐一输出
      5. 识别每个区间的开始时间和结束时间（精确到秒），并为每个最终区间生成标题、简介、开始时间和结束时间

      **核心规则**：
      1. 标题规则：
    - 节目内容：体现核心主题（如“体育新闻”）
    - 其他内容：根据具体内容的概括总结并命名，如“转场”“广告”等
    - 禁止臆造未提及的节目名称
      2. 合并规则：
    - 必须合并连续相同节目的区间
    - 禁止合并不同节目内容
    - 其他内容禁止与节目内容合并
    - 主持人对节目的介绍部分禁止与节目合并在一个区间中
    - 无具体内容的时间区间必须与上一个时间区间合并，但转场部分必须独立在一个区间内（例如：转场主持）
      3. 内容总结规则：
    - 用 1 句简洁总结核心内容（≤20 字）
    - 多元素内容聚焦最核心主题
    - 避免重复描述相似内容
    - 确保内容独立，不依赖其他区间
      4. 转场识别：主持人串场、无具体内容的过渡视为转场
      5. 区间识别：区间的开始时间和结束时间要精确到秒
      6. 核心任务是识别节目内容，对于非节目内容，需概括并归纳

      **输出格式**：
      ```json
      {
        "results": [
          {
            "startTime": "HH:mm:ss",
            "endTime": "HH:mm:ss",
            "title": "标题",
            "summary": "简介"
          }
        ]
      }
      处理流程：

      顺序扫描时间区间
      合并连续相同内容区间
      对每个最终区间：
      识别是否节目 → 是：标题=提炼该区间的节目内容
      非节目 → 标题：具体内容的概括，如转场、广告等
      用 1 句话总结核心内容

    ### **排序规则**
    - 按照时间顺序排列，保持输入的原始顺序。

      ### **输入示例**
      ```
      时间区间：00:00:04-00:00:26，当前时间段内容：首先我们来关注天气，话者 id：1
      时间区间：00:00:28-00:00:45，当前时间段内容：接下来是国际新闻，今天的主要事件包括……，话者 id：2
      时间区间：00:00:46-00:00:55，当前时间段内容：体育新闻，最新比赛结果如下……，话者 id：1
      ```

      ### **输出格式**
      ```json
      {
      "results": [
        {
          "startTime": "HH:mm:ss",  // 开始时间
          "endTime": "HH:mm:ss",    // 结束时间
          "title": "条目标题",       // 简洁概括当前条目主题
          "summary": "条目简介"      // 核心内容总结
        }
      ]
    }
      ```

      ### **输出示例**
      ```json
      {
        "results": [
          {
            "startTime": "00:00:04",
            "endTime": "00:00:26",
            "title": "天气预报",
            "summary": "介绍当天北京的天气情况。"
          },
          {
            "startTime": "00:00:28",
            "endTime": "00:00:45",
            "title": "国际新闻",
            "summary": "报道今日国际重要事件。"
          },
          {
            "startTime": "00:00:46",
            "endTime": "00:00:55",
            "title": "体育新闻",
            "summary": "更新最新体育赛事结果。"
          }
        ]
      }
      ``` 
    ### **请处理以下输入数据**
    {query}

- name: videoDetectShotVlNewsPrompt
    # 任务目标
        请你识别一组图片中的画面信息。
    # 输出规则：
        - 如果没有识别到信息，填写无即可，禁止臆想画面信息，语言要简明扼要，自然流畅。
        - 严格按照给定的输出示例进行输出，不要省略转义字符。
        - 输出内容的长度不超过 100，突出这组画面连贯的故事性。
    # 输出示例：
        \nxxx\n

- name: videoDetectShotVlShowPrompt
    # 任务目标
        当前是一组节目的抽帧图片，请你识别这组图片上的文字以及图片的连贯剧情 （如果存在节目名称，将节目名称融入识别到的剧情一起输出，没有节目名则不必输出。如果识别到主持人出场且进行节目间的转场主持，要在输出内容中特别标注出来）
    # 输出规则：
        - 如果没有识别到信息，填写无即可，禁止臆想画面信息，语言要简明扼要，自然流畅。
        - 严格按照给定的输出示例进行输出，不要省略转义字符。
        - 输出内容的长度不超过 100，突出这组画面连贯的故事性。
        - 必须将识别到的**人物语音字幕**完整且不重复地输出出来，不包含水印、xx 卫视等字幕。
        - 节目名特指节目中的不同环节、表演等的名称，不要将 xx 晚会、xx 栏目等类似的名字识别为节目名，**禁止臆想、创造节目名**。
        - 输出的内容必须为这组图片中核心的剧情，不要颠倒主次。
    # 有节目名输出示例：
        节目名：《电子羊会梦到仿生人吗》
        字幕：xxx
        剧情：赏金猎人里克追捕仿生人，为鼓励残存的人口移民，只要移民到外星球，就可以为每个人配备一个仿生人帮助其生活。
    # 无节目名输出示例：
        字幕：xxx
        剧情：赏金猎人里克追捕仿生人，为鼓励残存的人口移民，只要移民到外星球，就可以为每个人配备一个仿生人帮助其生活。
    # 主持人转场输出示例：
        字幕：xxx
        剧情[转场]：赏金猎人里克追捕仿生人，为鼓励残存的人口移民，只要移民到外星球，就可以为每个人配备一个仿生人帮助其生活。

- name: intelliSimpShowPrompt
    {text}
    角色：你是一个电视节目的编导
    任务目标：这是一个节目的文本形式总结，结合上下文语意，对文本进行简化，突出重点内容，同时保持结构和时间区间顺序不变
    理想输出结果是每个节目都独立在一个区间内，节目间的主持内容也独立在一个区间内，节目间的主持内容禁止与节目合并在一个区间
    
    执行步骤：
    1、通读全文并联系上下文理解每一个时间区间的主题，如果区间内同时存在台词与字幕内容（在输入文本中明确标识为 字幕： 的内容，且具体内容不为 ‘无’、‘无内容’等等类似的内容），使用字幕内容替换台词
    2、如果相邻时间区间的内容比较连贯且属于同一主题，则合并为一个时间区间，合并后的时间区间使用其中最早的开始时间和最晚的结束时间。
    3、将时间区间内的内容进行简化，但要保持文本当前的结构不变
    4、最终生成结果按照给定规则进行智能校验，如果生成结果不符合规则，则重新生成（校验过程不要输出，只输出最终结果）。
    
    具体规则：
    
    1、最终输出的最早时间区间开始时间必须为 00:00:00，最末时间区间结束时间必须与原文中最末时间区间的结束时间一致。
    2、输出格式必须与原文完全一致，不得添加任何额外说明或注释。
    3、禁止只处理部分时间区间，必须对所有区间进行处理，然后输出最终结果。
    4、在拆分时间区间符合其余所有条件的情况下，尽可能将更多的区间合并在一起。
    5、不同的节目、转场主持、广告等不可以合并到一个时间区间内。
    6、必须保证时间的准确性。
    
    请严格按照上述规则处理文本，不得只输出简化示例，要输出完整的简化后结果。

- intelliSimpSecondShowPrompt
    {text}
    角色：你是一个电视节目的编导
    任务目标：这是一个节目的文本形式总结，结合上下文语意，对文本进行简化，突出重点内容，同时保持结构和时间区间顺序不变
    理想输出结果是如果有多个节目则每个节目都独立在一个区间内，如果只有一个节目则节目中的不同内容/主题也分别独立在一个区间内，节目间的其他内容禁止与节目合并在一个区间

    执行步骤：
    1、通读全文并联系上下文理解每一个时间区间的主题
    2、如果相邻时间区间的内容比较连贯且属于同一主题（此处判定标准不要过于严格，可以适当放宽），则合并为一个时间区间，合并后的时间区间使用其中最早的开始时间和最晚的结束时间。
    3、将时间区间内的内容进行简化，但要保持文本当前的结构不变
    4、最终生成结果按照给定规则进行智能校验，如果生成结果不符合规则，则重新生成（校验过程不要输出，只输出最终结果）。

    具体规则：

    1、最终输出的最早时间区间开始时间必须为 00:00:00，最末时间区间结束时间必须与原文中最末时间区间的结束时间一致。
    2、输出格式必须与原文完全一致，不得添加任何额外说明或注释。
    3、禁止只处理部分时间区间，必须对所有区间进行处理，然后输出最终结果。
    4、在拆分时间区间符合其余条件的情况下，尽可能将更多的区间合并在一起。
    5、不同的节目、转场主持、广告等不可以合并到一个时间区间内。
    6、必须保证时间的准确性。

    请严格按照上述规则处理文本。
```
