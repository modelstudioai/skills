# 指令列表

<a id="指令简介"></a>

<a id="cfd5dc1454c3t"></a>

## 指令简介

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

<a id="指令列表"></a>

<a id="ca48f685c5jt1"></a>

## 指令列表

<a id="多模态交互应用指令"></a>

<a id="f438872d78f6e"></a>

### 多模态交互应用指令

<a id="系统指令"></a>

<a id="88c79d10dba7k"></a>

#### 系统指令

<a id="c056c375cacsv"></a>

##### 亮度设置

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数示例</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>increase_brightness</p></td><td rowspan="2"><p>调高亮度</p></td><td rowspan="2"><p>亮度调高10</p></td><td><p>number</p></td><td><p>亮度值</p></td><td><p>亮度调高10|number=10</p></td></tr><tr><td><p>to</p></td><td><p>到、至、为、...</p></td><td><p>亮度调高到10|to=到</p></td></tr><tr><td><p>increase_brightness_default</p></td><td><p>默认调高亮度</p></td><td><p>亮度调高点</p></td><td></td><td></td><td></td></tr><tr><td rowspan="2"><p>decrease_brightness</p></td><td rowspan="2"><p>调低亮度</p></td><td rowspan="2"><p>亮度调低10</p></td><td><p>number</p></td><td><p>亮度值</p></td><td><p>亮度调低10|number=10</p></td></tr><tr><td><p>to</p></td><td><p>到、至、为、...</p></td><td><p>亮度调低到10|to=到</p></td></tr><tr><td><p>decrease_brightness_default</p></td><td><p>默认调低亮度</p></td><td><p>亮度调低点</p></td><td></td><td></td><td></td></tr><tr><td rowspan="2"><p>set_brightness</p></td><td rowspan="2"><p>设置亮度</p></td><td rowspan="2"><p>亮度调到50</p></td><td><p>number</p></td><td><p>亮度值</p></td><td><p>亮度调到50|number=50</p></td></tr><tr><td><p>to</p></td><td><p>到、至、为、...</p></td><td><p>亮度调到50|to=到</p></td></tr></tbody></table>

<a id="167bf9ced12hc"></a>

##### 音量设置

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数示例</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>increase_volume</p></td><td rowspan="3"><p>调高音量</p></td><td rowspan="3"><p>音量调高10</p></td><td><p>number</p></td><td><p>音量值</p></td><td><p>音量调高10|number=10</p></td></tr><tr><td><p>to</p></td><td><p>到、至、为、...</p></td><td><p>音量调高到10|to=到</p></td></tr><tr><td><p>for</p></td><td><p>音量类别，包括：系统、媒体、通话</p></td><td><p>媒体音量调高到30|for=媒体</p></td></tr><tr><td><p>increase_volume_default</p></td><td><p>默认调高音量</p></td><td><p>音量调高点</p></td><td></td><td></td><td></td></tr><tr><td rowspan="3"><p>decrease_volume</p></td><td rowspan="3"><p>调低音量</p></td><td rowspan="3"><p>音量调低10</p></td><td><p>number</p></td><td><p>音量值</p></td><td><p>音量调低10|number=10</p></td></tr><tr><td><p>to</p></td><td><p>到、至、为、...</p></td><td><p>音量调低到10|to=到</p></td></tr><tr><td><p>for</p></td><td><p>音量类别，包括：系统、媒体、通话</p></td><td><p>系统音量调低到30|for=系统</p></td></tr><tr><td><p>decrease_volume_default</p></td><td><p>默认调低音量</p></td><td><p>音量调低点</p></td><td></td><td></td><td></td></tr><tr><td rowspan="3"><p>set_volume</p></td><td rowspan="3"><p>调节音量</p></td><td rowspan="3"><p>音量调到50</p></td><td><p>number</p></td><td><p>音量值</p></td><td><p>音量调到50|number=50</p></td></tr><tr><td><p>to</p></td><td><p>到、至、为、...</p></td><td><p>音量调到50|to=到</p></td></tr><tr><td><p>for</p></td><td><p>音量类别，包括：系统、媒体、通话</p></td><td><p>电话音量调到30|for=通话</p></td></tr><tr><td><p>mute</p></td><td><p>静音</p></td><td><p>静音</p></td><td></td><td></td><td></td></tr><tr><td><p>unmute</p></td><td><p>取消静音</p></td><td><p>取消静音</p></td><td></td><td></td><td></td></tr></tbody></table>

<a id="bef3d3dfcb4z0"></a>

##### 设备控制

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数示例 |
| --- | --- | --- | --- | --- | --- |
| shutdown | 关机 | 关机、关闭电脑 |  |  |  |
| quit | 退出 | 退出、回聊、结束会话、退出语音助手 |  |  |  |
| back | 返回 | 回到上一级 |  |  |  |
| confirm | 确认 | 好的 | record | 是否录音 | 确认并录音\|record=True |
| cancel | 取消 | 不用了 |  |  |  |
| select | 选择 | 选择第二个 | index | 序列号 | 选择第二个\|index=2 |
| check\_battery | 电量查询 | 现在还剩多少电 |  |  |  |

<a id="e00e9d71c3tnd"></a>

##### 屏幕控制

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数示例 |
| --- | --- | --- | --- | --- | --- |
| screen\_off | 熄屏/待机模式 | 熄屏、进入待机状态 |  |  |  |
| screen\_shot | 截屏 | 帮我截个屏 |  |  |  |
| screen\_recording | 录屏 | 帮我录下屏 |  |  |  |
| stop\_screen\_recording | 结束录屏 | 结束录屏 |  |  |  |

<a id="0c17301505opr"></a>

##### 多媒体控制

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数示例 |
| --- | --- | --- | --- | --- | --- |
| play | 播放（除音乐外） | 播放播客、放电影 |  |  |  |
| start\_over | 从头播放 | 重新从头播吧 |  |  |  |
| stop | 暂停 | 暂停播放 |  |  |  |
| resume\_play | 继续播放 | 继续播放 |  |  |  |
| next | 下一个 | 下一首歌 | unit | 单位 | 下一首歌\|unit=首 |
| previous | 上一个 | 上一首歌 | unit | 单位 | 上一首歌\|unit=首 |
| change | 换一个 | 换一首歌 | unit | 单位 | 换一首歌\|unit=首 |

<a id="99ed6145adxd5"></a>

##### 应用开关

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数示例 |
| --- | --- | --- | --- | --- | --- |
| open\_notification | 打开消息通知 | 打开消息通知 |  |  |  |
| exit\_notification | 关闭消息通知 | 关闭消息通知 |  |  |  |
| clean\_notification | 清除消息通知 | 清除所有通知 |  |  |  |
| open\_photos | 打开相册 | 打开相册 |  |  |  |
| quit\_photos | 退出相册 | 退出相册 |  |  |  |
| open\_player | 打开多媒体（蓝牙音频播控） | 打开多媒体 |  |  |  |
| quit\_player | 退出多媒体 | 退出多媒体 |  |  |  |
| open\_app\_center | 打开应用中心 | 打开应用中心 |  |  |  |
| quit\_app\_center | 退出应用中心 | 退出应用中心 |  |  |  |
| open\_Prompter | 打开提词器 | 打开提词器 |  |  |  |
| quit\_Prompter | 退出提词器 | 退出提词器 |  |  |  |
| open\_app | 打开第三方应用 | 打开微信 | app\_name | 应用名称，例如：微博、网易新闻、小红书、飞书、钉钉； | 打开微信\|app\_name=微信 |
| quit\_app | 退出第三方应用 | 退出微信 | app\_name | 应用名称 | 退出微信\|app\_name=微信 |
| open\_setting | 打开设置 | 打开设置 | type | 设置类型，例如：系统、通用、显示、音量、应用、设备连接、隐私政策； | 打开通用设置\|type=通用 |
| quit\_setting | 退出设置 | 退出设置 | type | 设置类型 | 退出通用设置\|type=通用 |
| open\_system\_update | 打开系统更新 | 打开系统更新页面 |  |  |  |
| quit\_system\_update | 退出系统更新 | 关闭系统更新页面 |  |  |  |
| open\_dnd\_mode | 打开勿扰模式 | 打开勿扰模式 |  |  |  |
| quit\_dnd\_mode | 关闭勿扰模式 | 关闭勿扰模式 |  |  |  |
| open\_auto\_brightness | 打开智能感光 | 打开感光模式 |  |  |  |
| quit\_auto\_brightness | 关闭智能感光 | 关闭智能感光 |  |  |  |
| open\_vr\_calibration | 打开虚实标定 | 打开虚实标定页面 |  |  |  |
| quit\_vr\_calibration | 退出虚实标定 | 关闭虚实标定页面 |  |  |  |

<a id="5cae65e11393q"></a>

##### 音乐

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数示例</strong></p></th></tr></thead><tbody><tr><td rowspan="10"><p>play_music</p></td><td rowspan="10"><p>播放音乐</p></td><td rowspan="10"><p>放首歌</p></td><td><p>song</p></td><td><p>歌曲名称</p></td><td><p>我要听十年|song=十年</p></td></tr><tr><td><p>artist</p></td><td><p>歌手</p></td><td><p>我要听周杰伦的歌|artist=周杰伦</p></td></tr><tr><td><p>album</p></td><td><p>专辑</p></td><td><p>我要听八度空间专辑|album=八度空间</p></td></tr><tr><td><p>style</p></td><td><p>风格/流派</p></td><td><p>我要听摇滚乐|style=摇滚</p></td></tr><tr><td><p>language</p></td><td><p>方言/语种</p></td><td><p>我要听粤语歌|language=粤语</p></td></tr><tr><td><p>general_tag</p></td><td><p>场景/标签</p></td><td><p>我要听轻松的歌|general_tag=轻松</p></td></tr><tr><td><p>era</p></td><td><p>年代</p></td><td><p>来电八十年代的歌|era=八十年代</p></td></tr><tr><td><p>sort</p></td><td><p>排序，包括：最新、最热</p></td><td><p>来首最新的歌|sort=最新</p></td></tr><tr><td><p>music_type</p></td><td><p>音乐类型，包括：歌曲、专辑、歌单</p></td><td><p>我要听刘德华的专辑|music_type=专辑</p></td></tr><tr><td><p>media_name</p></td><td><p>播放平台</p></td><td><p>播放虾米音乐的歌曲|media_name=虾米音乐</p></td></tr><tr><td><p>play_daily_playlist</p></td><td><p>播放每日推荐歌单</p></td><td><p>播放每日推荐歌单</p></td><td></td><td></td><td></td></tr><tr><td><p>play_my_collection</p></td><td><p>播放我喜欢的歌单</p></td><td><p>播放我喜欢的歌单</p></td><td></td><td></td><td></td></tr><tr><td><p>play_randomly</p></td><td><p>猜你喜欢</p></td><td><p>随便放点歌</p></td><td></td><td></td><td></td></tr><tr><td><p>like</p></td><td><p>喜欢/收藏</p></td><td><p>喜欢这首歌</p></td><td></td><td></td><td></td></tr><tr><td><p>unlike</p></td><td><p>不喜欢/取消收藏</p></td><td><p>不喜欢这个歌</p></td><td></td><td></td><td></td></tr></tbody></table>

<a id="9fdf58df9b06d"></a>

##### 拍照录像

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数示例 |
| --- | --- | --- | --- | --- | --- |
| take\_photo | 拍照 | 拍张照片 |  |  |  |
| quick\_burst | 连拍 | 连拍三张 | number | 拍照数量 | 连拍三张\|number=3 |
| open\_camera | 打开相机 | 打开相机 |  |  |  |
| quit\_camera | 退出相机 | 退出相机 |  |  |  |
| open\_photo\_mode | 打开拍照模式 | 打开拍照模式 |  |  |  |
| quit\_photo\_mode | 退出拍照模式 | 关闭拍照模式 |  |  |  |
| open\_camera\_preview | 打开相机预览模式 | 打开相机预览模式 |  |  |  |
| quit\_camera\_preview | 关闭相机预览模式 | 关闭相机预览模式 |  |  |  |
| video\_recording | 录像 | 录制视频吧 |  |  |  |
| open\_video\_mode | 打开摄影模式 | 打开摄影模式 |  |  |  |
| quit\_video\_mode | 退出摄影模式 | 关闭摄影模式 |  |  |  |

<a id="b616a93f85bz3"></a>

##### 打电话

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数示例</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>call</p></td><td rowspan="5"><p>打电话</p></td><td rowspan="5"><p>拨打电话</p></td><td><p>contact_name</p></td><td><p>联系人名称</p></td><td><p>打给小明|contact_name=小明</p></td></tr><tr><td><p>phone_number</p></td><td><p>电话号码</p></td><td><p>拨打10086|phone_number=10086</p></td></tr><tr><td><p>phone_type</p></td><td><p>电话类型</p></td><td><p>拨打小明的工作电话|phone_type=工作</p></td></tr><tr><td><p>phone_entity</p></td><td><p>电话实体</p></td><td><p>拨打火警|phone_entity=火警</p></td></tr><tr><td><p>record</p></td><td><p>是否需要录音</p></td><td><p>拨打并录音|record=True</p></td></tr><tr><td><p>confirm</p></td><td><p>确认</p></td><td><p>好的</p></td><td><p>record</p></td><td><p>是否录音</p></td><td><p>确认并录音|record=True</p></td></tr><tr><td><p>cancel</p></td><td><p>取消</p></td><td><p>不用了</p></td><td></td><td></td><td></td></tr><tr><td><p>open_call</p></td><td><p>打开电话</p></td><td><p>打开电话应用</p></td><td></td><td></td><td></td></tr><tr><td><p>quit_call</p></td><td><p>退出电话</p></td><td><p>退出电话应用</p></td><td></td><td></td><td></td></tr><tr><td rowspan="2"><p>answer_call</p></td><td rowspan="2"><p>接听电话</p></td><td rowspan="2"><p>接电话</p></td><td><p>contact_name</p></td><td><p>联系人名称</p></td><td><p>接一下小明的电话|contact_name=小明</p></td></tr><tr><td><p>record</p></td><td><p>是否需要录音</p></td><td><p>接听并录音|record=True</p></td></tr><tr><td><p>reject_phone</p></td><td><p>拒听电话</p></td><td><p>不接了</p></td><td></td><td></td><td></td></tr><tr><td><p>update_contacts</p></td><td><p>更新通讯录</p></td><td><p>更新通讯录</p></td><td></td><td></td><td></td></tr></tbody></table>

<a id="7de4280108laz"></a>

##### 录音

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数示例 |
| --- | --- | --- | --- | --- | --- |
| audio\_recording | 录音 | 开始录音 | audio\_type | 音频类型，包括：内部、外部、通话 | 录制蓝牙音乐\|audio\_type=内部<br><br>开始现场录音\|audio\_type=外部<br><br>开启电话录音\|audio\_type=通话 |
| quit\_audio\_recording | 退出录音 | 关闭录音应用 |  |  |  |
| stop\_audio\_recording | 停止录音 | 暂停录音 |  |  |  |

<a id="自定义指令"></a>

<a id="9882dcaee7ob1"></a>

#### 自定义指令

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

<a id="语音交互应用指令"></a>

<a id="913226b210111"></a>

### 语音交互应用指令

<a id="系统指令-2"></a>

<a id="f5f026a9bbuda"></a>

#### 系统指令

<a id="70cdb1bcd9a2x"></a>

##### 打电话

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>MAKE_A_PHONE_CALL_phone_call</p></td><td rowspan="2"><p>打电话</p></td><td rowspan="2"><p>拨打10086</p><p>拨打火警</p><p>拨打小明的工作电话</p></td><td><p>phone_num</p></td><td><p>String</p></td><td><p>电话号码</p></td><td><p>否</p></td></tr><tr><td><p>contact_name</p></td><td><p>String</p></td><td><p>联系人</p></td><td><p>否</p></td></tr><tr><td><p>CANCEL_phone_call</p></td><td><p>取消呼叫</p></td><td><p>不用了</p></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2"><p>CREATE_contacts</p></td><td rowspan="2"><p>新建联系人</p></td><td rowspan="2"><p>创建一个联系人，小王，12345678901</p></td><td><p>phone_num</p></td><td><p>String</p></td><td><p>电话号码</p></td><td><p>是</p></td></tr><tr><td><p>contact_name</p></td><td><p>String</p></td><td><p>联系人名称</p></td><td><p>是</p></td></tr><tr><td><p>ANSWER_phone_call</p></td><td><p>接电话</p></td><td><p>接电话</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>REJECT_phone_call</p></td><td><p>拒听电话</p></td><td><p>不接了</p></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="3"><p>UPDATE_contacts</p></td><td rowspan="3"><p>更新通讯录</p></td><td rowspan="3"><p>把小王的电话更新为12345678901</p></td><td><p>contact_name</p></td><td><p>String</p></td><td><p>待更新的联系人</p></td><td><p>是</p></td></tr><tr><td><p>update_name</p></td><td><p>String</p></td><td><p>若更新联系人名字，更新后的名字</p></td><td><p>否</p></td></tr><tr><td><p>update_phone</p></td><td><p>String</p></td><td><p>若更新联系人电话，更新后的电话</p></td><td><p>否</p></td></tr></tbody></table>

<a id="d3cf1db876xui"></a>

##### 定闹钟

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>SET_clock</p></td><td rowspan="4"><p>设定闹钟</p></td><td rowspan="4"><p>定个明天早上六点的闹钟</p><p>每周五下午三点半提醒我开会</p></td><td><p>time</p></td><td><p>String</p></td><td><p>设置时间</p></td><td><p>是</p></td></tr><tr><td><p>date</p></td><td><p>String</p></td><td><p>设置日期，标准格式：YYYY-MM-DD</p></td><td><p>否</p></td></tr><tr><td><p>content</p></td><td><p>String</p></td><td><p>闹钟内容、标签，例如设置目的</p></td><td><p>否</p></td></tr><tr><td><p>repeat</p></td><td><p>String</p></td><td><p>重复设置的日期，例如：每天/工作日/周一/周二/周三/周四/周五/周六/周日，默认不重复</p></td><td><p>否</p></td></tr></tbody></table>

<a id="33a20aae5e9cf"></a>

##### 亮度设置

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>CHANGE_brightness</p></td><td rowspan="3"><p>将亮度调节到某个具体值</p></td><td rowspan="3"><p>亮度调到50</p></td><td><p>value</p></td><td><p>Integer</p></td><td><p>亮度值</p></td><td><p>否</p></td></tr><tr><td><p>level</p></td><td><p>Integer</p></td><td><p>非连续模式下，亮度设置的等级，例如：一级/五级</p></td><td><p>否</p></td></tr><tr><td><p>mode</p></td><td><p>String</p></td><td><p>亮度模式，例如：自动/正常/夜间/阅读/游戏/观影</p></td><td><p>否</p></td></tr><tr><td rowspan="3"><p>INCREASE_brightness</p></td><td rowspan="3"><p>调高屏幕或照明设备的亮度，支持通过具体数值或预设档位调节。</p></td><td rowspan="3"><p>亮度调高10</p></td><td><p>number</p></td><td><p>Integer</p></td><td><p>亮度值</p></td><td><p>否</p></td></tr><tr><td><p>to</p></td><td><p>Integer</p></td><td><p>到、至、为、...</p></td><td><p>否</p></td></tr><tr><td><p>level</p></td><td><p>Integer</p></td><td><p>非连续模式下，亮度增加的等级</p></td><td><p>否</p></td></tr><tr><td rowspan="3"><p>DECREASE_brightness</p></td><td rowspan="3"><p>降低屏幕或照明设备的亮度，支持通过具体数值或预设档位调节。</p></td><td rowspan="3"><p>亮度调低10</p></td><td><p>number</p></td><td><p>Integer</p></td><td><p>亮度值</p></td><td><p>否</p></td></tr><tr><td><p>to</p></td><td><p>Integer</p></td><td><p>到、至、为、...</p></td><td><p>否</p></td></tr><tr><td><p>level</p></td><td><p>Integer</p></td><td><p>非连续模式下，亮度降低的等级</p></td><td><p>否</p></td></tr><tr><td><p>INCREASE_DEFAULT_brightness</p></td><td><p>默认调高亮度（未明确指定调高数值）</p></td><td><p>亮度调高点</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>DECREASE_DEFAULT_brightness</p></td><td><p>默认调低亮度（未明确指定调低数值）</p></td><td><p>亮度调低点</p></td><td></td><td></td><td></td><td></td></tr></tbody></table>

<a id="0518c7b37azfp"></a>

##### 色温设置

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td><p>CHANGE_color_temperature</p></td><td><p>将色温调节到某个具体值</p></td><td><p>色温调到20</p></td><td><p>amount</p></td><td><p>Integer</p></td><td><p>色温增减的具体数值</p></td><td><p>是</p></td></tr><tr><td rowspan="2"><p>INCREASE_color_temperature</p></td><td rowspan="2"><p>增加屏幕或显示器的色温（变冷），支持设置调节幅度，或无具体数值</p></td><td rowspan="2"><p>色温调高20</p></td><td><p>amount</p></td><td><p>Integer</p></td><td><p>色温增加的具体数值</p></td><td><p>否</p></td></tr><tr><td><p>to</p></td><td><p>Integer</p></td><td><p>到、至、为、...</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>DECREASE_color_temperature</p></td><td rowspan="2"><p>减小屏幕或显示器的色温（变暖），支持设置调节幅度，或无具体数值</p></td><td rowspan="2"><p>色温调低20</p></td><td><p>amount</p></td><td><p>Integer</p></td><td><p>色温减少的具体数值</p></td><td><p>否</p></td></tr><tr><td><p>to</p></td><td><p>Integer</p></td><td><p>到、至、为、...</p></td><td><p>否</p></td></tr></tbody></table>

<a id="7ba71b20d88f8"></a>

##### 音量设置

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td><p>CHANGE_volume</p></td><td><p>将音量调节到某个具体值</p></td><td><p>音量调到50</p></td><td><p>amount</p></td><td><p>Integer</p></td><td><p>音量增加的具体数值</p></td><td><p>是</p></td></tr><tr><td rowspan="2"><p>PLUS_volume</p></td><td rowspan="2"><p>将音量调高，支持通过具体数值调节。</p></td><td rowspan="2"><p>音量调高10</p></td><td><p>amount</p></td><td><p>Integer</p></td><td><p>音量增加的具体数值</p></td><td><p>否</p></td></tr><tr><td><p>to</p></td><td><p>Integer</p></td><td><p>到、至、为、...</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>MINUS_volume</p></td><td rowspan="2"><p>将音量调低，支持通过具体数值调节。</p></td><td rowspan="2"><p>音量调低10</p></td><td><p>amount</p></td><td><p>Integer</p></td><td><p>音量减小的具体数值</p></td><td><p>否</p></td></tr><tr><td><p>to</p></td><td><p>Integer</p></td><td><p>到、至、为、...</p></td><td><p>否</p></td></tr><tr><td><p>INCREASE_DEFAULT_volume</p></td><td><p>默认调高音量（未明确指定调高数值）</p></td><td><p>音量调高点</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>DECREASE_DEFAULT_volume</p></td><td><p>默认调低音量（未明确指定调低数值）</p></td><td><p>音量调低点</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>MUTE_volume</p></td><td><p>静音</p></td><td><p>静音</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>UNMUTE_volume</p></td><td><p>取消静音</p></td><td><p>取消静音</p></td><td></td><td></td><td></td><td></td></tr></tbody></table>

<a id="e6c5194be6gth"></a>

##### 蓝牙

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数说明 | 参数是否必选 |
| --- | --- | --- | --- | --- | --- | --- |
| DEVICE\_LIST\_bluetooth | 列出所有已配对的蓝牙设备 | 打开蓝牙列表 |  |  |  |  |
| SCAN\_bluetooth | 搜索附近的可配对蓝牙设备 | 搜索蓝牙 |  |  |  |  |
| TURN\_OFF\_bluetooth | 关闭蓝牙功能 | 关闭蓝牙 |  |  |  |  |
| TURN\_ON\_bluetooth | 开启蓝牙功能 | 打开蓝牙 |  |  |  |  |

<a id="4301c859a0xmd"></a>

##### 应用开关

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td><p>OPEN_device</p></td><td><p>打开、启动设备</p></td><td><p>打开耳机</p></td><td><p>device</p></td><td><p>String</p></td><td><p>设备名称，默认为当前设备</p></td><td><p>是</p></td></tr><tr><td rowspan="2"><p>LAUNCH_app</p></td><td rowspan="2"><p>启动应用</p></td><td rowspan="2"><p>打开播客</p><p>打开播客，开始播放</p></td><td><p>name</p></td><td><p>String</p></td><td><p>应用名称，默认为当前应用，例如：相册、应用中心、应用宝、微博、网易新闻、小红书、飞书、钉钉、bilibili、哔哩哔哩、B站、抖音、喜马拉雅、优酷、腾讯视频、爱奇艺、芒果tv、微信</p></td><td><p>是</p></td></tr><tr><td><p>intent</p></td><td><p>String</p></td><td><p>打开应用之后的意图/下一步动作</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>CLOSE_device_or_app</p></td><td rowspan="2"><p>关闭、退出设备或应用</p></td><td rowspan="2"><p>耳机关机</p><p>退出播客</p></td><td><p>device</p></td><td><p>String</p></td><td><p>设备名称，默认为当前设备</p></td><td><p>否</p></td></tr><tr><td><p>app</p></td><td><p>String</p></td><td><p>应用名称，默认为当前应用，例如：相册、应用中心、应用宝、微博、网易新闻、小红书、飞书、钉钉、bilibili、哔哩哔哩、B站、抖音、喜马拉雅、优酷、腾讯视频、爱奇艺、芒果tv、微信</p></td><td><p>否</p></td></tr><tr><td><p>RESTART_device</p></td><td><p>重启设备</p></td><td><p>重启眼镜</p></td><td><p>device</p></td><td><p>String</p></td><td><p>设备名称，默认为当前设备</p></td><td><p>否</p></td></tr><tr><td><p>SHUTDOWN_assistant</p></td><td><p>关闭智能助手服务</p></td><td><p>退出语音助手</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>OPEN_notification</p></td><td><p>打开消息通知</p></td><td><p>打开消息通知</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>EXIT_notification</p></td><td><p>关闭消息通知</p></td><td><p>关闭消息通知</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>CLEAN_notification</p></td><td><p>清除消息通知</p></td><td><p>清除所有通知</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>OPEN_setting</p></td><td><p>打开设置</p></td><td><p>打开设置</p></td><td><p>type</p></td><td><p>String</p></td><td><p>设置类型，包括：系统、通用、显示、音量、应用、设备连接、隐私政策；</p></td><td><p>否</p></td></tr><tr><td><p>EXIT_setting</p></td><td><p>退出设置</p></td><td><p>退出设置</p></td><td></td><td></td><td></td><td></td></tr></tbody></table>

<a id="6ce0f8193cu39"></a>

##### 设备控制

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数说明 | 参数是否必选 |
| --- | --- | --- | --- | --- | --- | --- |
| BACK | 返回 | 回到上一级 |  |  |  |  |
| CONFIRM | 确认 | 好的 |  |  |  |  |
| CANCEL | 取消 | 不用了 |  |  |  |  |
| SELECT | 选择 | 选择第二个 | index | Integer | 序列号 | 否 |
| CHECK\_battery | 电量查询 | 现在还剩多少电 |  |  |  |  |

<a id="1f90b3c7365gi"></a>

##### 音乐播放

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="11"><p>PLAY_music</p></td><td rowspan="11"><p>播放音乐</p></td><td rowspan="11"><p>放一首青花瓷</p><p>放一首纯音乐</p><p>打开虾米音乐播放青花瓷</p></td><td><p>song</p></td><td><p>String</p></td><td><p>歌曲名称</p></td><td><p>否</p></td></tr><tr><td><p>artist</p></td><td><p>String</p></td><td><p>歌手</p></td><td><p>否</p></td></tr><tr><td><p>album</p></td><td><p>String</p></td><td><p>专辑</p></td><td><p>否</p></td></tr><tr><td><p>type</p></td><td><p>String</p></td><td><p>音乐类型，如：电子、流行、摇滚、抒情、乡村、爵士、纯音乐等</p></td><td><p>否</p></td></tr><tr><td><p>style</p></td><td><p>String</p></td><td><p>风格/流派</p></td><td><p>否</p></td></tr><tr><td><p>language</p></td><td><p>String</p></td><td><p>方言/语种</p></td><td><p>否</p></td></tr><tr><td><p>general_tag</p></td><td><p>String</p></td><td><p>场景/标签</p></td><td><p>否</p></td></tr><tr><td><p>era</p></td><td><p>String</p></td><td><p>年代</p></td><td><p>否</p></td></tr><tr><td><p>sort</p></td><td><p>String</p></td><td><p>排序，包括：最新、最热</p></td><td><p>否</p></td></tr><tr><td><p>mode</p></td><td><p>String</p></td><td><p>播放模式，例如：单曲循环、列表循环、随机播放、心动模式</p></td><td><p>否</p></td></tr><tr><td><p>player</p></td><td><p>String</p></td><td><p>播放音乐的应用程序或设备</p></td><td><p>否</p></td></tr><tr><td><p>PLAY_DAILYLIST_music</p></td><td><p>播放每日推荐歌单</p></td><td><p>播放每日推荐歌单</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>PLAY_COLLECTION_music</p></td><td><p>播放我喜欢的歌单</p></td><td><p>播放我喜欢的歌单</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>PLAY_RANDOM_music</p></td><td><p>随机播放歌曲（猜你喜欢），适合用户未指定任何歌曲信息时调用</p></td><td><p>随便放点歌</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>LIKE_music</p></td><td><p>喜欢/收藏</p></td><td><p>喜欢这首歌</p></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>

<a id="c349c51f53e9k"></a>

##### 视频播放

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="10"><p>PLAY_video</p></td><td rowspan="10"><p>播放视频</p></td><td rowspan="10"><p>播放一个刘德华的电影</p><p>播放一个张艺谋导演的电影</p><p>播放一个喜剧片</p><p>4K播放电影</p><p>播放一个和时尚有关的电影</p><p>播放一个法语电影</p><p>播放一个美国电影</p><p>播放一个九十年代的电影</p><p>打开优酷播放流浪地球</p></td><td><p>title</p></td><td><p>String</p></td><td><p>视频名称</p></td><td><p>否</p></td></tr><tr><td><p>actor</p></td><td><p>String</p></td><td><p>主演/主要人物</p></td><td><p>否</p></td></tr><tr><td><p>director</p></td><td><p>String</p></td><td><p>导演/作者</p></td><td><p>否</p></td></tr><tr><td><p>genre</p></td><td><p>String</p></td><td><p>视频类型或电影类型</p></td><td><p>否</p></td></tr><tr><td><p>theme</p></td><td><p>String</p></td><td><p>主题</p></td><td><p>否</p></td></tr><tr><td><p>language</p></td><td><p>String</p></td><td><p>语言</p></td><td><p>否</p></td></tr><tr><td><p>region</p></td><td><p>String</p></td><td><p>地区</p></td><td><p>否</p></td></tr><tr><td><p>year</p></td><td><p>String</p></td><td><p>年份</p></td><td><p>否</p></td></tr><tr><td><p>resolution</p></td><td><p>String</p></td><td><p>分辨率，可选：标清/高清/超清/4K</p></td><td><p>否</p></td></tr><tr><td><p>player</p></td><td><p>String</p></td><td><p>播放视频的应用程序或设备</p></td><td><p>否</p></td></tr></tbody></table>

<a id="7b0c71cdb811p"></a>

##### 多媒体控制

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>PREVIOUS_resource</p></td><td rowspan="2"><p>播放上一个多媒体资源（如歌曲、音视频等）</p></td><td rowspan="2"><p>播放上一首歌</p><p>优酷播放上一集</p></td><td><p>resource_type</p></td><td><p>String</p></td><td><p>需要切换到下一个的资源类型，例如：音乐、视频、新闻、故事、图片等</p></td><td><p>否</p></td></tr><tr><td><p>player</p></td><td><p>String</p></td><td><p>播放多媒体内容的应用程序或设备</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>NEXT_resource</p></td><td rowspan="2"><p>播放下一个多媒体资源（如歌曲、音视频等）</p></td><td rowspan="2"><p>播放下一首歌</p><p>优酷播放下一集</p></td><td><p>resource_type</p></td><td><p>String</p></td><td><p>需要切换到下一个的资源类型，例如：音乐、视频、新闻、故事、图片等</p></td><td><p>否</p></td></tr><tr><td><p>player</p></td><td><p>String</p></td><td><p>播放多媒体内容的应用程序或设备</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>CHANGE_resource</p></td><td rowspan="2"><p>换一个多媒体资源播放（如歌曲、音视频等）</p></td><td rowspan="2"><p>换一首歌</p><p>优酷换一个电影播放</p></td><td><p>resource_type</p></td><td><p>String</p></td><td><p>需要切换到下一个的资源类型，例如：音乐、视频、新闻、故事、图片等</p></td><td><p>否</p></td></tr><tr><td><p>player</p></td><td><p>String</p></td><td><p>播放多媒体内容的应用程序或设备</p></td><td><p>否</p></td></tr><tr><td rowspan="3"><p>REPLAY_resource</p></td><td rowspan="3"><p>重新播放当前的多媒体资源（如歌曲、音视频等）</p></td><td rowspan="3"><p>重新播放七里香</p><p>电影从头开始播放</p><p>优酷视频从头播放</p></td><td><p>name</p></td><td><p>String</p></td><td><p>需要重新播放的资源名称</p></td><td><p>否</p></td></tr><tr><td><p>resource_type</p></td><td><p>String</p></td><td><p>需要重新播放的资源类型，例如：音乐、视频、新闻、故事、图片等</p></td><td><p>否</p></td></tr><tr><td><p>player</p></td><td><p>String</p></td><td><p>播放多媒体内容的应用程序或设备</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>RESUME_operation_on_device</p></td><td rowspan="2"><p>恢复设备上被暂停或中断的操作，例如音乐/视频播放、录音等。</p></td><td rowspan="2"><p>耳机继续播放</p><p>音乐继续播放</p></td><td></td><td><p>String</p></td><td><p>需要恢复操作的设备名称，如未指定则默认当前设备</p></td><td><p>否</p></td></tr><tr><td><p>operation_type</p></td><td><p>String</p></td><td><p>需要恢复的操作类型，例如音乐播放、录像、录音等</p></td><td><p>否</p></td></tr><tr><td rowspan="2"><p>PAUSE_operation_on_device</p></td><td rowspan="2"><p>暂停设备上的当前进行的操作，例如音乐/视频播放、录音等。</p></td><td rowspan="2"><p>耳机暂停一下</p><p>音乐暂停</p></td><td><p>device_name</p></td><td><p>String</p></td><td><p>需要暂停操作的设备名称，如未指定则默认当前设备</p></td><td><p>否</p></td></tr><tr><td><p>operation_type</p></td><td><p>String</p></td><td><p>需要暂停的具体操作类型，例如音乐播放、录像、录音等</p></td><td><p>否</p></td></tr></tbody></table>

<a id="baff8a215cjvi"></a>

##### 拍照录像

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td><p>PHOTO_camera</p></td><td><p>拍照</p></td><td><p>拍张照片</p></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="9"></td><td rowspan="9"><p>相机设置（支持模式切换、镜头控制、基础参数调整）</p></td><td rowspan="9"><p>打开夜景拍照模式</p><p>切到前置摄像头</p><p>关闭闪光灯</p><p>图像分辨率调到4k</p><p>打开自动对焦</p><p>曝光补偿值调到1</p><p>打开白平衡自动</p><p>把网格线关掉</p><p>打开高动态范围成像</p></td><td><p>mode</p></td><td><p>String</p></td><td><p>摄像模式，可选参数: 拍照/录像/慢动作/延时摄影/全景/夜景</p></td><td><p>否</p></td></tr><tr><td><p>lens_switch</p></td><td><p>String</p></td><td><p>前后置镜头切换，可选参数: 前置/后置/外部镜头（如支持）</p></td><td><p>否</p></td></tr><tr><td><p>flash_mode</p></td><td><p>String</p></td><td><p>闪光灯模式，例如: 自动/开启/关闭/防红眼</p></td><td><p>否</p></td></tr><tr><td><p>resolution</p></td><td><p>String</p></td><td><p>图像分辨率，例如: 1080p/4K/8K（根据设备支持）</p></td><td><p>否</p></td></tr><tr><td><p>focus_mode</p></td><td><p>String</p></td><td><p>对焦模式，例如: 自动/手动/连续自动对焦</p></td><td><p>否</p></td></tr><tr><td><p>exposure_compensation</p></td><td><p>Integer</p></td><td><p>曝光补偿值（EV）</p></td><td><p>否</p></td></tr><tr><td><p>white_balance</p></td><td><p>String</p></td><td><p>白平衡设置，例如: 自动/日光/阴天/白炽灯/荧光灯</p></td><td><p>否</p></td></tr><tr><td><p>grid_lines</p></td><td><p>String</p></td><td><p>网格线是否显示，例如: 开启/关闭</p></td><td><p>否</p></td></tr><tr><td><p>hdr</p></td><td><p>String</p></td><td><p>高动态范围成像，例如: 开启/关闭</p></td><td><p>否</p></td></tr><tr><td><p>QUICK_BURST_camera</p></td><td><p>连拍</p></td><td><p>连拍5张</p></td><td><p>number</p></td><td><p>Integer</p></td><td><p>连拍数量设置，默认为5</p></td><td><p>是</p></td></tr><tr><td><p>VIDEO_recording</p></td><td><p>录像</p></td><td><p>录制视频吧</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>STOP_VIDEO_recording</p></td><td><p>停止录像</p></td><td><p>停止录像</p></td><td></td><td></td><td></td><td></td></tr><tr><td><p>SWITCH_MODE_camera</p></td><td><p>切换相机模式</p></td><td><p>换成录影模式</p></td><td><p>mode</p></td><td><p>String</p></td><td><p>相机模式设置，例如: 拍照模式/摄影模式/预览模式</p></td><td><p>是</p></td></tr></tbody></table>

<a id="e64098ebb0cmf"></a>

##### 录音

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数说明 | 参数是否必选 |
| --- | --- | --- | --- | --- | --- | --- |
| AUDIO\_recording | 录音 | 开始录制通话语音 | audio\_app | String | 需要录制音频的应用，例如：电话, 录音机 | 否 |
| STOP\_AUDIO\_recording | 停止录音 | 暂停录音 |  |  |  |  |

<a id="6495aea8816tj"></a>

##### 朗读文字

| 指令名称 | 指令说明 | 指令示例 | 参数名称 | 参数说明 | 参数说明 | 参数是否必选 |
| --- | --- | --- | --- | --- | --- | --- |
| READ\_screen | 读取当前屏幕上显示的内容（主要为文本），转化为音频播放 |  |  |  |  |  |

<a id="c7099061b8r20"></a>

##### 打开地图

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="8"><p>ROUTE_map</p></td><td rowspan="8"><p>打开并显示从起点位置到终点位置的地图路线（也可以仅包含终点），仅显示路线，不进行导航</p></td><td></td><td><p>endLoc_city</p></td><td><p>String</p></td><td><p>终点城市</p></td><td><p>否</p></td></tr><tr><td></td><td><p>startLoc_province</p></td><td><p>String</p></td><td><p>起点省份</p></td><td><p>否</p></td></tr><tr><td></td><td><p>endLoc_poi</p></td><td><p>String</p></td><td><p>终点地名</p></td><td><p>否</p></td></tr><tr><td></td><td><p>startLoc_area</p></td><td><p>String</p></td><td><p>起点行政区（小于市级地区、大于具体地点的区域划分）</p></td><td><p>否</p></td></tr><tr><td></td><td><p>startLoc_poi</p></td><td><p>String</p></td><td><p>起点地名</p></td><td><p>否</p></td></tr><tr><td></td><td><p>startLoc_city</p></td><td><p>String</p></td><td><p>起点城市</p></td><td><p>否</p></td></tr><tr><td></td><td><p>endLoc_province</p></td><td><p>String</p></td><td><p>终点省份</p></td><td><p>否</p></td></tr><tr><td></td><td><p>endLoc_area</p></td><td><p>String</p></td><td><p>终点行政区（小于市级地区、大于具体地点的区域划分）</p></td><td><p>否</p></td></tr></tbody></table>

<a id="7db399af5bu9f"></a>

##### 发短信

<table><thead><tr><th><p><strong>指令名称</strong></p></th><th><p><strong>指令说明</strong></p></th><th><p><strong>指令示例</strong></p></th><th><p><strong>参数名称</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数说明</strong></p></th><th><p><strong>参数是否必选</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>SENDCONTACTS_message</p></td><td rowspan="3"><p>给指定联系人发送其他联系人信息</p></td><td></td><td><p>category</p></td><td><p>String</p></td><td><p>信息类型，如手机</p></td><td><p>否</p></td></tr><tr><td></td><td><p>receiver</p></td><td><p>String</p></td><td><p>接收人</p></td><td><p>是</p></td></tr><tr><td></td><td><p>name</p></td><td><p>String</p></td><td><p>需要发送的联系人</p></td><td><p>是</p></td></tr><tr><td rowspan="3"><p>SEND_message</p></td><td rowspan="3"><p>给指定联系人发送信息</p></td><td></td><td><p>content</p></td><td><p>String</p></td><td><p>信息内容</p></td><td><p>否</p></td></tr><tr><td></td><td><p>contact</p></td><td><p>String</p></td><td><p>接收信息的联系人</p></td><td><p>是</p></td></tr><tr><td></td><td><p>phone</p></td><td><p>String</p></td><td><p>接收人的手机号码</p></td><td><p>否</p></td></tr><tr><td><p>VIEW_message</p></td><td><p>查看消息</p></td><td></td><td><p>message_type</p></td><td><p>String</p></td><td><p>消息类型。如：短信、邮件等</p></td><td><p>是</p></td></tr></tbody></table>

<a id="自定义指令-2"></a>

<a id="54567f9ca1a0s"></a>

#### 自定义指令

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
