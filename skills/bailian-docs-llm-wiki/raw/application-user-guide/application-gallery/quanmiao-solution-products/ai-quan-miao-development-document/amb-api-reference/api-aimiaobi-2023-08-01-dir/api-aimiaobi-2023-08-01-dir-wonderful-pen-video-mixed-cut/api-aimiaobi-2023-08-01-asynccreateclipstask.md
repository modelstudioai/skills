# AsyncCreateClipsTask - 创建剪辑任务

生成剪辑视频

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncCreateClipsTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncCreateClipsTask)

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

aimiaobi:AsyncCreateClipsTask

create

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

17a299a9-f223-4707-b0dd-4c22519bddf5

VoiceStyle

string

否

口播语音类型

甜美女声 中国台湾话女声 舌尖男声 新闻男声 激昂解说 标准女声 悬疑解说 广告男声 温柔女声 资讯女声 新闻女声 萝莉女声 磁性男声

MusicUrl

string

否

背景音乐地址

http://music.mp4

ColorWords

array<object>

否

花字数组

object

否

花字结构

Content

string

否

花字内容

花字内容

TimelineIn

integer

否

花字出现时间（秒）

0

TimelineOut

integer

否

花字结束时间（秒）

5

X

number

否

花字位置横坐标

0.2

Y

number

否

花字位置纵坐标

0.5

FontSize

integer

否

花字大小

默认120

EffectColorStyle

string

否

花字样式

CS0002-000007 参考：https://help.aliyun.com/zh/ims/developer-reference/flower-effect-example?spm=a2c4g.11186623.0.0.6ee43d29lo1EWu#88bc5f6046mg2

WorkspaceId

string

是

[百炼业务空间 Id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-ipe7d81yq4sl5jmk

VoiceVolume

integer

否

口播音量

0-10，默认5

MusicVolume

integer

否

音乐音量

0-10，默认5

SubtitleFontSize

integer

否

字幕尺寸

默认120

Height

integer

否

视频高度

1920

Width

integer

否

视频宽度

1080

CloseVoice

boolean

否

关闭口播

CloseMusic

boolean

否

关闭背景音乐

CloseSubtitle

boolean

否

关闭字幕

CustomVoiceUrl

string

否

自定义声道语音地址

http://xxx/xxx.mp4

CustomVoiceVolume

integer

否

自定义声道音量

0

Stickers

array<object>

否

贴纸结构数组

object

否

贴纸数组元素

Url

string

否

gif 文件公网地址

http://xxx/xxx.gif

TimelineIn

integer

否

贴纸开始时间（妙）

5

Duration

integer

否

贴纸显示时间（秒）

10

X

number

否

贴纸位置 x 坐标

200

Y

number

否

贴纸位置 y 坐标

200

Width

integer

否

贴纸宽度

100

Height

integer

否

贴纸高度

100

DyncFrames

integer

否

gif 文件动态帧数

8

CustomVoiceStyle

string

否

cosyvoice 的音色

longxian\_normal

CosyVoiceAppKey

string

否

cosyvoice 的 appkey

ddgsase

CosyVoiceToken

string

否

cosyvoice 的 token

xxsfazs

MusicStyle

string

否

推荐音乐类型

浪漫, 美食,国风,轻快,动感,舒缓,搞怪,时尚

OpeningCreditsUrl

string

否

片头视频地址

http://xxx/xxx.mp4

ClosingCreditsUrl

string

否

片尾视频地址

http://xxx/xxx.mp4

HighDefSourceVideos

array<object>

否

高清视频结构列表

object

否

高清视频结构

VideoId

string

否

视频 id

00d59b6de13971f0bcd84531949c0102

VideoName

string

否

视频名字

video001.mp4

VideoUrl

string

否

视频 URL

http://fotor-cn-cutout.oss-cn-shanghai.aliyuncs.com/cutout\_tmp/01ba219486f043b4b339e7080e5cf11d.mp4

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

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

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
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/AsyncCreateClipsTask#workbench-doc-change-demo)。
