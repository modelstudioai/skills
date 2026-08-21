# GetAutoClipsTaskInfo - 获得剪辑任务信息

获得剪辑任务状态

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAutoClipsTaskInfo)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAutoClipsTaskInfo)

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

aimiaobi:GetAutoClipsTaskInfo

get

\*全部资源

`*`

无

无

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

TaskId

string

是

任务唯一 ID

0dbf1055f8a2475d99904c3b76a0ffba

WorkspaceId

string

是

[工作空间](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

百炼工作空间Id

ShowResourceInfo

boolean

否

展示视频素材信息

false

ShowAnalysisResults

boolean

否

展示视频理解结果

false

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

RequestId

string

Id of the request

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Code

string

状态码

successful

Data

object

业务数据

TaskId

string

任务唯一 ID

e5a1a59c82d0454fad6454e8a04d0093

Step

string

当前所处状态

clips

Status

integer

状态

0-待执行、1-执行中、2-执行成功、3-暂停、4-执行失败-可重试、5-执行失败-不可重试,6-任务取消

Content

string

全部口播内容

口播内容

Timelines

array<object>

口播时间线数组

array<object>

口播时间线

TimelineId

string

时间线 id

20774ebd9abc71ef80486632b68f0102

Content

string

口播内容

口播内容

Clips

array<object>

剪辑片段数组

object

剪辑片段

ClipId

string

剪辑 Id

20774ebd9abc71ef80486632b68f0102

VideoName

string

视频名字

123.mp4

VideoId

string

视频 Id

20774ebd9abc71ef80486632b68f0102

In

integer

片段开始时间（秒）已经废弃

0

Out

integer

片段结束时间（秒）已经废弃

5

ContentInner

string

口播分段内容

口播分段内容

InEx

number

片段开始时间（毫秒）

0.33

OutEx

number

片段结束时间 (毫秒)

3.45

VoiceStyle

string

口播声音类型

温柔女声

MusicStyle

string

推荐音乐类型

国风

MusicUrl

string

背景音乐地址

http://music.mp4

MusicVolume

integer

音乐音量

5

VoiceVolume

integer

口播音量

5

SubtitleFontSize

integer

字幕大小

5

OutputVideoUrl

string

成片地址

http://output.mp4

MediaCloudTimeline

string

视频云 timeline

视频云格式timeline

ColorWords

array<object>

花字信息数组

object

花字信息元素

Content

string

花字内容

花字内容

TimelineIn

integer

花字开始时间（秒）

0

TimelineOut

integer

花字结束时间（秒）

5

X

number

花字位置横坐标

0.2

Y

number

花字位置纵坐标

0.5

FontSize

integer

花字大小

5

EffectColorStyle

string

花字效果

CS0002-000008

ErrorMessage

string

错误信息

错误信息

CloseVoice

boolean

关闭口播

CloseSubtitle

boolean

关闭字幕

CloseMusic

boolean

关闭音乐

CustomVoiceUrl

string

自定义声道文件地址

http://xxx/xxx.mp4

CustomVoiceVolume

integer

自定义声道音量

0

Stickers

array<object>

贴纸数组

object

贴纸结构

Url

string

贴纸 gif 文件地址

http://xxx/xxx.gif

TimelineIn

integer

贴纸开始时间（秒）

10

Duration

integer

贴纸出现时长

10

X

number

贴纸出现位置横坐标

100

Y

number

贴纸出现位置纵坐标

100

Width

integer

贴纸宽度

200

Height

integer

贴纸高度

200

DyncFrames

integer

贴纸高度

8

CustomVoiceStyle

string

cosyvoice 的音色

longxian\_normal

OutputVideoFileKey

string

输出结果 fileKey

oss://xxx/xxx.mp4

OpeningCreditsUrl

string

片头视频地址

http://xxx/xxx.mp4

ClosingCreditsUrl

string

片尾视频地址

http://xxx/xxx.mp4

SourceVideos

array<object>

剪辑素材结构列表

object

剪辑素材结构

VideoId

string

视频 ID

fdaswe

VideoName

string

视频名称

video001.mp4

VideoUrl

string

视频地址。

http://xxx/xxx.mp4

ReferenceVideo

object

参考视频信息

VideoId

string

视频 ID

90ca686b11c371f08339752281ed0102

VideoName

string

视频名称

video001.mp4

VideoUrl

string

视频 URL

http://xxx/xxx.mp4

AnalysisResults

array<object>

视频理解结果列表

array<object>

视频理解结果

MediaId

string

视频 Id

975e1d91a8d057e132cc5d88e4d5b360

MediaName

string

视频名字

video001.mp4

MediaUrl

string

视频地址

http://xxx/xxx.mp4

LensInfos

array<object>

镜头信息列表

array<object>

镜头信息

StartTime

object

开始时间

Hour

integer

小时

2

Minute

integer

分钟

1

Second

integer

秒

30

MillSecond

integer

毫秒

100

EndTime

object

结束时间

Hour

integer

时

2

Minute

integer

分

1

Second

integer

秒

30

MillSecond

integer

毫秒

100

AnalysisContent

string

理解内容

视频理解内容

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "successful",
  "Data": {
    "TaskId": "e5a1a59c82d0454fad6454e8a04d0093",
    "Step": "clips",
    "Status": 0,
    "Content": "口播内容",
    "Timelines": [
      {
        "TimelineId": "20774ebd9abc71ef80486632b68f0102",
        "Content": "口播内容",
        "Clips": [
          {
            "ClipId": "20774ebd9abc71ef80486632b68f0102\n",
            "VideoName": "123.mp4",
            "VideoId": "20774ebd9abc71ef80486632b68f0102",
            "In": 0,
            "Out": 5,
            "ContentInner": "口播分段内容",
            "InEx": 0.33,
            "OutEx": 3.45
          }
        ]
      }
    ],
    "VoiceStyle": "温柔女声",
    "MusicStyle": "国风",
    "MusicUrl": "http://music.mp4",
    "MusicVolume": 5,
    "VoiceVolume": 5,
    "SubtitleFontSize": 5,
    "OutputVideoUrl": "http://output.mp4",
    "MediaCloudTimeline": "视频云格式timeline",
    "ColorWords": [
      {
        "Content": "花字内容",
        "TimelineIn": 0,
        "TimelineOut": 5,
        "X": 0.2,
        "Y": 0.5,
        "FontSize": 5,
        "EffectColorStyle": "CS0002-000008"
      }
    ],
    "ErrorMessage": "错误信息",
    "CloseVoice": true,
    "CloseSubtitle": true,
    "CloseMusic": true,
    "CustomVoiceUrl": "http://xxx/xxx.mp4",
    "CustomVoiceVolume": 0,
    "Stickers": [
      {
        "Url": "http://xxx/xxx.gif",
        "TimelineIn": 10,
        "Duration": 10,
        "X": 100,
        "Y": 100,
        "Width": 200,
        "Height": 200,
        "DyncFrames": 8
      }
    ],
    "CustomVoiceStyle": "longxian_normal",
    "OutputVideoFileKey": "oss://xxx/xxx.mp4",
    "OpeningCreditsUrl": "http://xxx/xxx.mp4",
    "ClosingCreditsUrl": "http://xxx/xxx.mp4",
    "SourceVideos": [
      {
        "VideoId": "fdaswe",
        "VideoName": "video001.mp4",
        "VideoUrl": "http://xxx/xxx.mp4"
      }
    ],
    "ReferenceVideo": {
      "VideoId": "90ca686b11c371f08339752281ed0102",
      "VideoName": "video001.mp4",
      "VideoUrl": "http://xxx/xxx.mp4"
    },
    "AnalysisResults": [
      {
        "MediaId": "975e1d91a8d057e132cc5d88e4d5b360",
        "MediaName": "video001.mp4",
        "MediaUrl": "http://xxx/xxx.mp4",
        "LensInfos": [
          {
            "StartTime": {
              "Hour": 2,
              "Minute": 1,
              "Second": 30,
              "MillSecond": 100
            },
            "EndTime": {
              "Hour": 2,
              "Minute": 1,
              "Second": 30,
              "MillSecond": 100
            },
            "AnalysisContent": "视频理解内容"
          }
        ]
      }
    ]
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetAutoClipsTaskInfo#workbench-doc-change-demo)。
