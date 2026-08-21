# 指令列表

## **指令简介**

指令是指由多模态交互下发，设备终端执行的任务，如打开台灯、调高音量等。

多模态交互开发套件提供一系列系统指令，您只需勾选需要的指令，对应指令将自动在对话中生效并下发。详细的指令列表请查看下文。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1003686.png)

如果需要修改下发指令，可以在设置页中调整。

![截屏2025-11-26 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3052464671/p1029732.png)

如果需要下发指令的同时给出模型回复，可以在设置页中选择回复模式：

-   根据执行情况回复（默认）：下发指令后，等待端侧返回成功/失败信息，模型生成对应回复，如“已将空调调整到26度”、“已经是最高音量，无法继续调高”。
    
-   自动回复：下发指令的同时，自动输出回复。
    

![截屏2025-11-25 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3052464671/p1029367.png)

如果您需要自定义指令，例如“打开小云电台”，可以使用自定义指令能力。支持下发指令配置，默认与指令名称一致，可手动修改。

## **指令列表**

### **多模态交互应用指令**

#### **系统指令**

##### **亮度设置**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

increase\_brightness

调高亮度

亮度调高10

number

亮度值

亮度调高10|number=10

to

到、至、为、...

亮度调高到10|to=到

increase\_brightness\_default

默认调高亮度

亮度调高点

decrease\_brightness

调低亮度

亮度调低10

number

亮度值

亮度调低10|number=10

to

到、至、为、...

亮度调低到10|to=到

decrease\_brightness\_default

默认调低亮度

亮度调低点

set\_brightness

设置亮度

亮度调到50

number

亮度值

亮度调到50|number=50

to

到、至、为、...

亮度调到50|to=到

##### **音量设置**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

increase\_volume

调高音量

音量调高10

number

音量值

音量调高10|number=10

to

到、至、为、...

音量调高到10|to=到

for

音量类别，包括：系统、媒体、通话

媒体音量调高到30|for=媒体

increase\_volume\_default

默认调高音量

音量调高点

decrease\_volume

调低音量

音量调低10

number

音量值

音量调低10|number=10

to

到、至、为、...

音量调低到10|to=到

for

音量类别，包括：系统、媒体、通话

系统音量调低到30|for=系统

decrease\_volume\_default

默认调低音量

音量调低点

set\_volume

调节音量

音量调到50

number

音量值

音量调到50|number=50

to

到、至、为、...

音量调到50|to=到

for

音量类别，包括：系统、媒体、通话

电话音量调到30|for=通话

mute

静音

静音

unmute

取消静音

取消静音

##### **设备控制**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

shutdown

关机

关机、关闭电脑

quit

退出

退出、回聊、结束会话、退出语音助手

back

返回

回到上一级

confirm

确认

好的

record

是否录音

确认并录音|record=True

cancel

取消

不用了

select

选择

选择第二个

index

序列号

选择第二个|index=2

check\_battery

电量查询

现在还剩多少电

##### **屏幕控制**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

screen\_off

熄屏/待机模式

熄屏、进入待机状态

screen\_shot

截屏

帮我截个屏

screen\_recording

录屏

帮我录下屏

stop\_screen\_recording

结束录屏

结束录屏

##### **多媒体控制**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

play

播放（除音乐外）

播放播客、放电影

start\_over

从头播放

重新从头播吧

stop

暂停

暂停播放

resume\_play

继续播放

继续播放

next

下一个

下一首歌

unit

单位

下一首歌|unit=首

previous

上一个

上一首歌

unit

单位

上一首歌|unit=首

change

换一个

换一首歌

unit

单位

换一首歌|unit=首

##### **应用开关**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

open\_notification

打开消息通知

打开消息通知

exit\_notification

关闭消息通知

关闭消息通知

clean\_notification

清除消息通知

清除所有通知

open\_photos

打开相册

打开相册

quit\_photos

退出相册

退出相册

open\_player

打开多媒体（蓝牙音频播控）

打开多媒体

quit\_player

退出多媒体

退出多媒体

open\_app\_center

打开应用中心

打开应用中心

quit\_app\_center

退出应用中心

退出应用中心

open\_Prompter

打开提词器

打开提词器

quit\_Prompter

退出提词器

退出提词器

open\_app

打开第三方应用

打开微信

app\_name

应用名称，例如：微博、网易新闻、小红书、飞书、钉钉；

打开微信|app\_name=微信

quit\_app

退出第三方应用

退出微信

app\_name

应用名称

退出微信|app\_name=微信

open\_setting

打开设置

打开设置

type

设置类型，例如：系统、通用、显示、音量、应用、设备连接、隐私政策；

打开通用设置|type=通用

quit\_setting

退出设置

退出设置

type

设置类型

退出通用设置|type=通用

open\_system\_update

打开系统更新

打开系统更新页面

quit\_system\_update

退出系统更新

关闭系统更新页面

open\_dnd\_mode

打开勿扰模式

打开勿扰模式

quit\_dnd\_mode

关闭勿扰模式

关闭勿扰模式

open\_auto\_brightness

打开智能感光

打开感光模式

quit\_auto\_brightness

关闭智能感光

关闭智能感光

open\_vr\_calibration

打开虚实标定

打开虚实标定页面

quit\_vr\_calibration

退出虚实标定

关闭虚实标定页面

##### **音乐**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

play\_music

播放音乐

放首歌

song

歌曲名称

我要听十年|song=十年

artist

歌手

我要听周杰伦的歌|artist=周杰伦

album

专辑

我要听八度空间专辑|album=八度空间

style

风格/流派

我要听摇滚乐|style=摇滚

language

方言/语种

我要听粤语歌|language=粤语

general\_tag

场景/标签

我要听轻松的歌|general\_tag=轻松

era

年代

来电八十年代的歌|era=八十年代

sort

排序，包括：最新、最热

来首最新的歌|sort=最新

music\_type

音乐类型，包括：歌曲、专辑、歌单

我要听刘德华的专辑|music\_type=专辑

media\_name

播放平台

播放虾米音乐的歌曲|media\_name=虾米音乐

play\_daily\_playlist

播放每日推荐歌单

播放每日推荐歌单

play\_my\_collection

播放我喜欢的歌单

播放我喜欢的歌单

play\_randomly

猜你喜欢

随便放点歌

like

喜欢/收藏

喜欢这首歌

unlike

不喜欢/取消收藏

不喜欢这个歌

##### **拍照录像**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

take\_photo

拍照

拍张照片

quick\_burst

连拍

连拍三张

number

拍照数量

连拍三张|number=3

open\_camera

打开相机

打开相机

quit\_camera

退出相机

退出相机

open\_photo\_mode

打开拍照模式

打开拍照模式

quit\_photo\_mode

退出拍照模式

关闭拍照模式

open\_camera\_preview

打开相机预览模式

打开相机预览模式

quit\_camera\_preview

关闭相机预览模式

关闭相机预览模式

video\_recording

录像

录制视频吧

open\_video\_mode

打开摄影模式

打开摄影模式

quit\_video\_mode

退出摄影模式

关闭摄影模式

##### **打电话**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

call

打电话

拨打电话

contact\_name

联系人名称

打给小明|contact\_name=小明

phone\_number

电话号码

拨打10086|phone\_number=10086

phone\_type

电话类型

拨打小明的工作电话|phone\_type=工作

phone\_entity

电话实体

拨打火警|phone\_entity=火警

record

是否需要录音

拨打并录音|record=True

confirm

确认

好的

record

是否录音

确认并录音|record=True

cancel

取消

不用了

open\_call

打开电话

打开电话应用

quit\_call

退出电话

退出电话应用

answer\_call

接听电话

接电话

contact\_name

联系人名称

接一下小明的电话|contact\_name=小明

record

是否需要录音

接听并录音|record=True

reject\_phone

拒听电话

不接了

update\_contacts

更新通讯录

更新通讯录

##### **录音**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数示例**

audio\_recording

录音

开始录音

audio\_type

音频类型，包括：内部、外部、通话

录制蓝牙音乐|audio\_type=内部

开始现场录音|audio\_type=外部

开启电话录音|audio\_type=通话

quit\_audio\_recording

退出录音

关闭录音应用

stop\_audio\_recording

停止录音

暂停录音

#### **自定义指令**

除上述系统指令外，如果您需要实现更多控制技能，可以使用自定义指令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8207470571/p967008.png)

自定义指令的结构与系统指令一致，每个指令类型可以创建多个指令。

每个指令包含指令名称、指令说明、指令示例；如果需要参数，还可以添加参数名称、参数说明和参数示例。

-   指令名称：建议使用英文，用于下发对应指令。
    
-   指令说明：解释该指令的作用。
    
-   指令示例：可以提供多条语料，提升模型对指令的下发准确率。
    
-   参数：支持设置多个参数，例如具体的调节数值；提供示例有助于模型理解参数的具体意义，下发更准确。
    

例如，设置一组指令用于调整台灯的亮度：

1.  创建一个指令类型，命名为“台灯亮度控制”。
    
2.  创建一个指令，命名为“brightness\_increase”，作用是下发调高亮度的指令。可以填写一些命中该指令的语料，用于模型训练，例如“台灯调亮点”、台灯亮度调高20”。
    
3.  如果需要下发具体参数，可以添加参数，填写名称、说明和示例。例如设置参数“to”，用于传递具体将台灯亮度调高到某个数值。提供参数示例，例如“亮度调高到20，to=20”。
    

每个指令类型可以创建多个指令，每个指令可以设置多个参数，也可以不设置任何参数。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9207470571/p967010.png)

创建指令后，在自定义指令列表中勾选并确定，即可将该指令添加到当前应用中自动生效。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8207470571/p967011.png)

如需测试指令是否生效，点击下方“立即运行”，即可开始测试。

您也可以配置更加精细的自定义指令：

1.  设置string、number、boolean、date、enum、time等参数类型，其中：
    
    1.  number：支持设置具体的数值范围，如“空调温度”可以设置为18-30，当用户指令中参数超出范围时，模型会主动追问。
        
    2.  enum：支持设置有限的枚举值，当用户指令中参数超出枚举值范围时，模型会主动追问。
        
2.  设置必填，当必填参数为空时，模型主动追问。
    
3.  指令示例支持填写不同参数的值，让模型理解更准确。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0220503771/p1057779.png)

### **语音交互应用指令**

#### **系统指令**

##### **打电话**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

MAKE\_A\_PHONE\_CALL\_phone\_call

打电话

拨打10086

拨打火警

拨打小明的工作电话

phone\_num

String

电话号码

否

contact\_name

String

联系人

否

CANCEL\_phone\_call

取消呼叫

不用了

CREATE\_contacts

新建联系人

创建一个联系人，小王，12345678901

phone\_num

String

电话号码

是

contact\_name

String

联系人名称

是

ANSWER\_phone\_call

接电话

接电话

REJECT\_phone\_call

拒听电话

不接了

UPDATE\_contacts

更新通讯录

把小王的电话更新为12345678901

contact\_name

String

待更新的联系人

是

update\_name

String

若更新联系人名字，更新后的名字

否

update\_phone

String

若更新联系人电话，更新后的电话

否

##### **定闹钟**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

SET\_clock

设定闹钟

定个明天早上六点的闹钟

每周五下午三点半提醒我开会

time

String

设置时间

是

date

String

设置日期，标准格式：YYYY-MM-DD

否

content

String

闹钟内容、标签，例如设置目的

否

repeat

String

重复设置的日期，例如：每天/工作日/周一/周二/周三/周四/周五/周六/周日，默认不重复

否

##### **亮度设置**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

CHANGE\_brightness

将亮度调节到某个具体值

亮度调到50

value

Integer

亮度值

否

level

Integer

非连续模式下，亮度设置的等级，例如：一级/五级

否

mode

String

亮度模式，例如：自动/正常/夜间/阅读/游戏/观影

否

INCREASE\_brightness

调高屏幕或照明设备的亮度，支持通过具体数值或预设档位调节。

亮度调高10

number

Integer

亮度值

否

to

Integer

到、至、为、...

否

level

Integer

非连续模式下，亮度增加的等级

否

DECREASE\_brightness

降低屏幕或照明设备的亮度，支持通过具体数值或预设档位调节。

亮度调低10

number

Integer

亮度值

否

to

Integer

到、至、为、...

否

level

Integer

非连续模式下，亮度降低的等级

否

INCREASE\_DEFAULT\_brightness

默认调高亮度（未明确指定调高数值）

亮度调高点

DECREASE\_DEFAULT\_brightness

默认调低亮度（未明确指定调低数值）

亮度调低点

##### **色温设置**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

CHANGE\_color\_temperature

将色温调节到某个具体值

色温调到20

amount

Integer

色温增减的具体数值

是

INCREASE\_color\_temperature

增加屏幕或显示器的色温（变冷），支持设置调节幅度，或无具体数值

色温调高20

amount

Integer

色温增加的具体数值

否

to

Integer

到、至、为、...

否

DECREASE\_color\_temperature

减小屏幕或显示器的色温（变暖），支持设置调节幅度，或无具体数值

色温调低20

amount

Integer

色温减少的具体数值

否

to

Integer

到、至、为、...

否

##### **音量设置**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

CHANGE\_volume

将音量调节到某个具体值

音量调到50

amount

Integer

音量增加的具体数值

是

PLUS\_volume

将音量调高，支持通过具体数值调节。

音量调高10

amount

Integer

音量增加的具体数值

否

to

Integer

到、至、为、...

否

MINUS\_volume

将音量调低，支持通过具体数值调节。

音量调低10

amount

Integer

音量减小的具体数值

否

to

Integer

到、至、为、...

否

INCREASE\_DEFAULT\_volume

默认调高音量（未明确指定调高数值）

音量调高点

DECREASE\_DEFAULT\_volume

默认调低音量（未明确指定调低数值）

音量调低点

MUTE\_volume

静音

静音

UNMUTE\_volume

取消静音

取消静音

##### **蓝牙**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

DEVICE\_LIST\_bluetooth

列出所有已配对的蓝牙设备

打开蓝牙列表

SCAN\_bluetooth

搜索附近的可配对蓝牙设备

搜索蓝牙

TURN\_OFF\_bluetooth

关闭蓝牙功能

关闭蓝牙

TURN\_ON\_bluetooth

开启蓝牙功能

打开蓝牙

##### **应用开关**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

OPEN\_device

打开、启动设备

打开耳机

device

String

设备名称，默认为当前设备

是

LAUNCH\_app

启动应用

打开播客

打开播客，开始播放

name

String

应用名称，默认为当前应用，例如：相册、应用中心、应用宝、微博、网易新闻、小红书、飞书、钉钉、bilibili、哔哩哔哩、B站、抖音、喜马拉雅、优酷、腾讯视频、爱奇艺、芒果tv、微信

是

intent

String

打开应用之后的意图/下一步动作

否

CLOSE\_device\_or\_app

关闭、退出设备或应用

耳机关机

退出播客

device

String

设备名称，默认为当前设备

否

app

String

应用名称，默认为当前应用，例如：相册、应用中心、应用宝、微博、网易新闻、小红书、飞书、钉钉、bilibili、哔哩哔哩、B站、抖音、喜马拉雅、优酷、腾讯视频、爱奇艺、芒果tv、微信

否

RESTART\_device

重启设备

重启眼镜

device

String

设备名称，默认为当前设备

否

SHUTDOWN\_assistant

关闭智能助手服务

退出语音助手

OPEN\_notification

打开消息通知

打开消息通知

EXIT\_notification

关闭消息通知

关闭消息通知

CLEAN\_notification

清除消息通知

清除所有通知

OPEN\_setting

打开设置

打开设置

type

String

设置类型，包括：系统、通用、显示、音量、应用、设备连接、隐私政策；

否

EXIT\_setting

退出设置

退出设置

##### **设备控制**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

BACK

返回

回到上一级

CONFIRM

确认

好的

CANCEL

取消

不用了

SELECT

选择

选择第二个

index

Integer

序列号

否

CHECK\_battery

电量查询

现在还剩多少电

##### **音乐播放**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

PLAY\_music

播放音乐

放一首青花瓷

放一首纯音乐

打开虾米音乐播放青花瓷

song

String

歌曲名称

否

artist

String

歌手

否

album

String

专辑

否

type

String

音乐类型，如：电子、流行、摇滚、抒情、乡村、爵士、纯音乐等

否

style

String

风格/流派

否

language

String

方言/语种

否

general\_tag

String

场景/标签

否

era

String

年代

否

sort

String

排序，包括：最新、最热

否

mode

String

播放模式，例如：单曲循环、列表循环、随机播放、心动模式

否

player

String

播放音乐的应用程序或设备

否

PLAY\_DAILYLIST\_music

播放每日推荐歌单

播放每日推荐歌单

PLAY\_COLLECTION\_music

播放我喜欢的歌单

播放我喜欢的歌单

PLAY\_RANDOM\_music

随机播放歌曲（猜你喜欢），适合用户未指定任何歌曲信息时调用

随便放点歌

LIKE\_music

喜欢/收藏

喜欢这首歌

##### **视频播放**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

PLAY\_video

播放视频

播放一个刘德华的电影

播放一个张艺谋导演的电影

播放一个喜剧片

4K播放电影

播放一个和时尚有关的电影

播放一个法语电影

播放一个美国电影

播放一个九十年代的电影

打开优酷播放流浪地球

title

String

视频名称

否

actor

String

主演/主要人物

否

director

String

导演/作者

否

genre

String

视频类型或电影类型

否

theme

String

主题

否

language

String

语言

否

region

String

地区

否

year

String

年份

否

resolution

String

分辨率，可选：标清/高清/超清/4K

否

player

String

播放视频的应用程序或设备

否

##### **多媒体控制**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

PREVIOUS\_resource

播放上一个多媒体资源（如歌曲、音视频等）

播放上一首歌

优酷播放上一集

resource\_type

String

需要切换到下一个的资源类型，例如：音乐、视频、新闻、故事、图片等

否

player

String

播放多媒体内容的应用程序或设备

否

NEXT\_resource

播放下一个多媒体资源（如歌曲、音视频等）

播放下一首歌

优酷播放下一集

resource\_type

String

需要切换到下一个的资源类型，例如：音乐、视频、新闻、故事、图片等

否

player

String

播放多媒体内容的应用程序或设备

否

CHANGE\_resource

换一个多媒体资源播放（如歌曲、音视频等）

换一首歌

优酷换一个电影播放

resource\_type

String

需要切换到下一个的资源类型，例如：音乐、视频、新闻、故事、图片等

否

player

String

播放多媒体内容的应用程序或设备

否

REPLAY\_resource

重新播放当前的多媒体资源（如歌曲、音视频等）

重新播放七里香

电影从头开始播放

优酷视频从头播放

name

String

需要重新播放的资源名称

否

resource\_type

String

需要重新播放的资源类型，例如：音乐、视频、新闻、故事、图片等

否

player

String

播放多媒体内容的应用程序或设备

否

RESUME\_operation\_on\_device

恢复设备上被暂停或中断的操作，例如音乐/视频播放、录音等。

耳机继续播放

音乐继续播放

String

需要恢复操作的设备名称，如未指定则默认当前设备

否

operation\_type

String

需要恢复的操作类型，例如音乐播放、录像、录音等

否

PAUSE\_operation\_on\_device

暂停设备上的当前进行的操作，例如音乐/视频播放、录音等。

耳机暂停一下

音乐暂停

device\_name

String

需要暂停操作的设备名称，如未指定则默认当前设备

否

operation\_type

String

需要暂停的具体操作类型，例如音乐播放、录像、录音等

否

##### **拍照录像**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

PHOTO\_camera

拍照

拍张照片

相机设置（支持模式切换、镜头控制、基础参数调整）

打开夜景拍照模式

切到前置摄像头

关闭闪光灯

图像分辨率调到4k

打开自动对焦

曝光补偿值调到1

打开白平衡自动

把网格线关掉

打开高动态范围成像

mode

String

摄像模式，可选参数: 拍照/录像/慢动作/延时摄影/全景/夜景

否

lens\_switch

String

前后置镜头切换，可选参数: 前置/后置/外部镜头（如支持）

否

flash\_mode

String

闪光灯模式，例如: 自动/开启/关闭/防红眼

否

resolution

String

图像分辨率，例如: 1080p/4K/8K（根据设备支持）

否

focus\_mode

String

对焦模式，例如: 自动/手动/连续自动对焦

否

exposure\_compensation

Integer

曝光补偿值（EV）

否

white\_balance

String

白平衡设置，例如: 自动/日光/阴天/白炽灯/荧光灯

否

grid\_lines

String

网格线是否显示，例如: 开启/关闭

否

hdr

String

高动态范围成像，例如: 开启/关闭

否

QUICK\_BURST\_camera

连拍

连拍5张

number

Integer

连拍数量设置，默认为5

是

VIDEO\_recording

录像

录制视频吧

STOP\_VIDEO\_recording

停止录像

停止录像

SWITCH\_MODE\_camera

切换相机模式

换成录影模式

mode

String

相机模式设置，例如: 拍照模式/摄影模式/预览模式

是

##### **录音**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

AUDIO\_recording

录音

开始录制通话语音

audio\_app

String

需要录制音频的应用，例如：电话, 录音机

否

STOP\_AUDIO\_recording

停止录音

暂停录音

##### **朗读文字**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

READ\_screen

读取当前屏幕上显示的内容（主要为文本），转化为音频播放

##### **打开地图**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

ROUTE\_map

打开并显示从起点位置到终点位置的地图路线（也可以仅包含终点），仅显示路线，不进行导航

endLoc\_city

String

终点城市

否

startLoc\_province

String

起点省份

否

endLoc\_poi

String

终点地名

否

startLoc\_area

String

起点行政区（小于市级地区、大于具体地点的区域划分）

否

startLoc\_poi

String

起点地名

否

startLoc\_city

String

起点城市

否

endLoc\_province

String

终点省份

否

endLoc\_area

String

终点行政区（小于市级地区、大于具体地点的区域划分）

否

##### **发短信**

**指令名称**

**指令说明**

**指令示例**

**参数名称**

**参数说明**

**参数说明**

**参数是否必选**

SENDCONTACTS\_message

给指定联系人发送其他联系人信息

category

String

信息类型，如手机

否

receiver

String

接收人

是

name

String

需要发送的联系人

是

SEND\_message

给指定联系人发送信息

content

String

信息内容

否

contact

String

接收信息的联系人

是

phone

String

接收人的手机号码

否

VIEW\_message

查看消息

message\_type

String

消息类型。如：短信、邮件等

是

#### **自定义指令**

除上述系统指令外，如果您需要实现更多控制技能，可以使用自定义指令。

![截屏2026-01-23 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1558149671/p1048804.png)

自定义指令的结构与系统指令一致，每个指令类型可以创建多个指令。

每个指令包含指令名称、指令说明、指令示例；如果需要参数，还可以添加参数名称、参数说明和参数示例。

-   指令名称：建议使用英文，用于下发对应指令。
    
-   指令说明：解释该指令的作用。
    
-   指令示例：可以提供多条语料，提升模型对指令的下发准确率。
    
-   参数：支持设置多个参数，例如具体的调节数值；提供示例有助于模型理解参数的具体意义，下发更准确。
    

![截屏2026-01-23 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1558149671/p1048817.png)

创建指令后，在自定义指令列表中勾选并确定，即可将该指令添加到当前应用中自动生效。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8207470571/p967011.png)

如需测试指令是否生效，点击下方“立即运行”，即可开始测试。
