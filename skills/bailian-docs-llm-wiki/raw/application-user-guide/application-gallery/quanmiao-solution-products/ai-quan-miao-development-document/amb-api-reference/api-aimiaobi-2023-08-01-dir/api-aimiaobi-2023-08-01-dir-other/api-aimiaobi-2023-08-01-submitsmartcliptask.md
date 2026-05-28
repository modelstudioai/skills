# SubmitSmartClipTask - 提交智能一键成片任务

提交一键成片剪辑任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitSmartClipTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitSmartClipTask)

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

aimiaobi:SubmitSmartClipTask

create

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

业务空间ID

InputConfig

object

是

输入配置

VideoIds

array<object>

是

视频素材 ID 对象列表

object

否

素材 ID 对象

Type

string

是

ID 的类型： materialId：妙笔素材库引用 ID fileKey：妙笔 FileKey url：可公开访问的 URL

fileKey

Id

string

是

素材 ID

oss://default/bucket-name/filepath/video.mp4

Titles

array

否

标题列表

string

否

标题

视频标题

BackgroundMusics

array<object>

否

背景音乐 ID 列表

object

否

背景音乐 ID 对象

Type

string

是

ID 的类型： materialId：妙笔素材库引用 ID fileKey：妙笔 FileKey url：可公开访问的 URL

fileKey

Id

string

是

背景音乐 ID

oss://default/bucket-name/filepath/video.mp3

Stickers

array<object>

否

贴纸列表

object

否

贴纸对象

X

double

是

贴纸左上角 X 坐标

0.5

Y

double

是

贴纸左上角 Y 坐标

0.5

Width

double

是

贴纸宽度

0.5

Height

double

是

贴纸高度

0.5

StickerId

object

是

贴纸 ID

Type

string

是

ID 的类型： materialId：妙笔素材库引用 ID fileKey：妙笔 FileKey url：可公开访问的 URL

fileKey

Id

string

是

贴纸 ID

oss://default/bucket-name/filepath/sticker.png

SpeechTexts

array

否

口播脚本文本列表

string

否

口播脚本文本

大家好，欢迎来到我的频道xxx

OutputConfig

object

否

输出配置

FileName

string

否

输出文件名，必须包含{index}

test\_{index}.mp4

Width

integer

否

输出视频宽

1920

Height

integer

否

输出视频高

1080

Count

integer

否

输出视频数量

1

MaxDuration

integer

否

输出视频最大时长，单位：秒

120

SaveToGeneratedContent

boolean

否

是否保存至内容管理

true

EditingConfig

object

否

剪辑配置

TitleConfig

object

否

标题配置

X

float

否

横幅文字左上角距离输出视频左上角的横向距离。注：支持百分比和像素两种形式。当取值为\[0～0.9999\] 时，表示相对输出视频宽的占比。当取值为>=2 的整数时，表示绝对像素。默认为 0。该坐标会按照素材尺寸和成片尺寸进行缩放。

100

Y

float

否

横幅文字左上角距离输出视频左上角的纵向距离。注：支持百分比和像素两种形式。当取值为\[0～0.9999\] 时，表示相对输出视频高的占比。当取值为>=2 的整数时，表示绝对像素。默认为 0。该坐标会按照素材尺寸和成片尺寸进行缩放

100

TimelineIn

float

否

标题出现的时间

2

TimelineOut

float

否

标题消失的时间

3

Alignment

string

否

TopLeft：视频左上角 TopCenter：视频竖直中轴线上侧 TopRight：视频右上角 CenterLeft：视频水平中轴线左侧 CenterCenter：视频中心位置 CenterRight：视频水平中轴线右侧 BottomLeft：视频左下角 BottomCenter：视频竖直中轴线下侧 BottomRight：视频右下角

TopLeft

MediaConfig

object

否

媒体配置

Volume

double

否

视频素材声音（0：静音）

SpeechConfig

object

否

口播配置

Volume

double

否

口播音频的音量，默认 1。取值：\[0, 10.0\]，支持小数，例：0.5。

0.5

Voice

string

否

指定单个或多个口播音色（英文逗号分隔）。当指定多个 voice 时，会随机选取一个合成。音色的可选范围请参见[智能语音效果示例](https://help.aliyun.com/zh/ims/developer-reference/smart-voice-effect-example)。例："zhimiao\_emo,zhilun"。

Style

string

否

口播声音风格，默认为空。若同时指定 Voice 和 Style，则优先取用 Voice "Gentle": 柔和 "Serious"：严肃 "Entertainment"：娱乐

SpeechRate

double

否

口播脚本语速 语速，取值范围：-500～500，默认值：0。 \[-500, 0, 500\] 对应的语速倍速区间为 \[0.5, 1.0, 2.0\]。

计算方法如下： 0.8 倍速（1-1/0.8）/0.002 = -125 1.2 倍速（1-1/1.2）/0.001 = 166 小于 1 倍速时，使用 0.002 系数。 大于 1 倍速时，使用 0.001 系数。 实际算法结果取近似值。

0

AsrConfig

object

否

字幕参数配置

X

float

否

横幅文字左上角距离输出视频左上角的横向距离 注：支持百分比和像素两种形式。当取值为\[0～0.9999\]时，表示相对输出视频宽的占比。当取值为>=2 的整数时，表示绝对像素。默认为 0。该坐标会按照素材尺寸和成片尺寸进行缩放。

Y

float

否

横幅文字左上角距离输出视频左上角的纵向距离 注：支持百分比和像素两种形式。当取值为\[0～0.9999\]时，表示相对输出视频高的占比。当取值为>=2 的整数时，表示绝对像素。默认为 0。该坐标会按照素材尺寸和成片尺寸进行缩放。

Alignment

string

否

字幕对齐 TopLeft：视频左上角 TopCenter：视频竖直中轴线上侧 TopRight：视频右上角 CenterLeft：视频水平中轴线左侧 CenterCenter：视频中心位置 CenterRight：视频水平中轴线右侧 BottomLeft：视频左下角 BottomCenter：视频竖直中轴线下侧 BottomRight：视频右下角

Font

string

否

字幕文字的字体。具体支持的字体参见字体列表。默认为 SimSun 字体。

SimSun

FontColor

string

否

字幕文字的颜色，格式为#后跟 16 进制值。例如：#ffffff。

#ffffff

FontSize

string

否

字幕文字的字号。该字号会根据素材尺寸和成片尺寸进行缩放。默认为 0，最大支持设置到 5000。

0

Spacing

string

否

横幅文字字间距。单位：像素值

0

BackgroundMusicConfig

object

否

背景音乐配置

Volume

double

否

背景音乐的音量，取值：\[0, 10.0\]

0.2

Style

string

否

背景音乐风格，默认为空，若 InputConfig 中已配置背景音乐，此字段不生效 取值如下： "bgm-beauty"：时尚 "bgm-chinese-style"：中国风 "bgm-cuisine"：美食 "bgm-dynamic"：动感 "bgm-quirky"：怪诞 "bgm-relaxing"：轻松 "bgm-romantic"：浪漫 "bgm-upbeat"：欢快

ExtendParam

string

否

其他扩展参数（会与 inputConfig、outputConfig、editingConfig 合并）

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

NoData

Data

object

任务提交结果

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

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
