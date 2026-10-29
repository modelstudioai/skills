# Qwen-Audio-TTS音色列表

查看 Qwen-Audio-TTS 各模型的系统音色，试听音色效果，并下载基础音色列表和试听音频。

**说明**

-   所选音色（`voice`）必须属于当前模型（`model`）支持的音色列表，不能跨模型混用。音色不匹配时，服务会返回 `InvalidParameter` 错误，例如 `[cosyvoice:]Engine error [411]: TTS speak operation failed`。
-   待合成文本（`text`）应使用所选音色支持的语言，否则可能出现发音错误或语音不自然。

如需专属音色，请参见[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)或[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)。

## 系统音色

对于支持方言指令的音色，可通过指令控制字段 `instruction` 指定方言，例如 `请讲上海话。`。

### qwen-audio-3.1-tts-plus

#### 旗舰音色

**名称**

**性别**

**特性支持**

**试听**

**名称**: 龙安灵心\_v3.1

**voice 参数**: `longanlingxin_v3.1`

女

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 试听1

```
你好呀，我是龙安灵心。在这个快节奏的世界里，我想做你耳畔最温柔的守候。无论是深夜的失眠还是清晨的微光，只要你需要，我都会在这里，用声音拥抱你的每一个情绪瞬间。
```

#### 试听2

```
今天过得怎么样？有没有遇到什么开心的小事，或者让你眉头紧锁的烦恼？别担心，慢慢说给我听。我会安静地陪伴着你，帮你梳理思绪，让心情像雨后的天空一样，重新变得清澈明亮。
```

#### 试听3

```
月亮已经爬上了树梢，星星在眨着眼睛。闭上眼睛，想象自己躺在柔软的云朵上，随着微风轻轻飘荡。所有的疲惫都随风散去，现在，请安心入睡，愿你在甜美的梦乡中，遇见最美的风景。
```

**名称**: 许南川

**voice 参数**: `xunanchuan_v3.1`

男

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 试听1

```
遇见你之前，我的世界是黑白单调的；遇见你之后，色彩斑斓如雨后彩虹。我想牵着你的手，走过春夏秋冬，看遍世间繁华。无论风雨如何变幻，只要你在身边，便是人间最美风景。
```

#### 试听2

```
我是许南川，一个喜欢用声音讲述故事的人。我的声音或许不够华丽，但足够真诚。希望能通过这磁性的语调，带你走进不同的世界，感受文字背后的温度与力量，期待与你相遇。
```

#### 试听3

```
在这个喧嚣的时代，保持清醒是一种奢侈。我喜欢在安静的午后，泡一杯茶，读一本好书。那种心灵的宁静，比任何物质的享受都来得珍贵。你呢？是否也渴望这样片刻的安宁？
```

**名称**: 龙安欢\_v3.1

**voice 参数**: `longanhuan_v3.1`

女

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 试听1

```
嗨，大家好！我是龙安欢。我喜欢笑，喜欢热闹，更喜欢看到大家快乐的样子。有什么烦心事尽管找我，保证让你笑着走出阴霾。让我们一起快乐起来吧！
```

#### 试听2

```
买衣服不要只看款式，更要看面料和剪裁。这件大衣版型正，羊毛含量高，穿在身上既保暖又有型。性价比超高，闭眼入都不会错。信我的准没错，赶紧入手一件过冬吧！
```

#### 试听3

```
天哪，今天的天气简直太糟糕了！出门忘带伞，结果淋成落汤鸡。不过没关系，回家喝杯热姜茶，洗个热水澡，又是一条好汉！你们今天过得怎么样？有没有什么趣事跟我分享呀？
```

**名称**: 龙安风悦\_v3.1

**voice 参数**: `longanfengyue_v3.1`

女

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 试听1

```
明天白天多云转晴，气温适宜，最高二十度，最低十五度。风力不大，非常适合户外活动。不过早晚温差较大，建议大家适当增减衣物，预防感冒。出行前记得查看实时路况哦。
```

#### 试听2

```
最近我在看一部老电影，里面的配乐特别经典，听得我忍不住单曲循环。你平时喜欢听什么类型的音乐？是轻快的流行乐，还是安静的纯音乐？推荐几首给我呗，我想换换口味。
```

#### 试听3

```
外婆坐在藤椅上，手里织着那条没完工的围巾，针脚细密而整齐。夕阳透过窗棂洒在她银白的发丝上，泛着柔和的光晕。她抬起头，笑着对我说：‘天凉了，快戴上吧。’那一刻，时光仿佛静止。
```

### qwen-audio-3.1-tts-flash

**说明**多语种与方言音色、精品英文音色、小语种音色支持北京和新加坡地域，其他类型音色仅支持北京地域。

#### 多语种与方言音色

以下四个音色均支持下列全部方言和语言。

-   方言：上海话、广东话、东北话、重庆话、陕西话、云南话、宁波话、甘肃话。
-   语言：日语、韩语、法语、德语、葡萄牙语、意大利语、越南语、印尼语。

**音色信息**

**性别**

**特性支持**

**试听**

**名称**: 龙安欢\_v3.1

**voice 参数**: `longanhuan_v3.1`

女

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 重庆话

#### 宁波话

#### 韩语

#### 印尼语

**名称**: 龙安灵心\_v3.1

**voice 参数**: `longanlingxin_v3.1`

女

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 云南话

#### 陕西话

#### 上海话

#### 法语

#### 意大利语

**名称**: 龙安风悦\_v3.1

**voice 参数**: `longanfengyue_v3.1`

女

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 东北话

#### 越南语

#### 日语

**名称**: 许南川

**voice 参数**: `xunanchuan_v3.1`

男

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 甘肃话

#### 东北话

#### 法语

#### 葡萄牙语

#### 精品中文音色

以下音色仅支持中文普通话。

**说明**Bella\_v3.1 同时支持中文普通话和英文。

**音色信息**

**性别**

**声线特质**

**适用场景**

**特性支持**

**试听**

**名称**: 于小云

**voice 参数**: `yuxiaoyun_v3.1`

女

元气、亲切、自然

广告营销、广播、客服助手、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 乔小娇

**voice 参数**: `qiaoxiaojiao_v3.1`

女

俏丽、可爱

广告营销、客服助手、有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 夏小晨

**voice 参数**: `xiaxiaochen_v3.1`

女

元气、明亮

广告营销、有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 安明远

**voice 参数**: `anmingyuan_v3.1`

男

清亮、自然

广告营销、有声书、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 温怀清

**voice 参数**: `wenhuaiqing_v3.1`

女

清亮、柔和

儿童故事、客服助手、广告营销、新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 安小岚

**voice 参数**: `anxiaolan_v3.1`

女

清甜、纯净

有声书、客服助手、旁白、新闻播报、广告营销

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 谢舒柔

**voice 参数**: `xieshurou_v3.1`

女

柔和、自然、知性

有声书、客服助手、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 白清岚

**voice 参数**: `baiqinglan_v3.1`

女

明亮、清纯

语音助手、客服助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 许玉远

**voice 参数**: `xuyuyuan_v3.1`

女

知性、成熟、质感

广告营销、新闻播报、旁白、客服助手、有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 安若柔

**voice 参数**: `anruorou_v3.1`

女

气声、知性

旁白、语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 闻怀之

**voice 参数**: `wenhuaizhi_v3.1`

女

稳重、成熟

有声书、新闻播报、广告营销、客服助手、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 萧行之

**voice 参数**: `xiaoxingzhi_v3.1`

女

端庄、贵气

新闻播报、有声书、旁白、客服助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 顾云舒

**voice 参数**: `guyunshu_v3.1`

女

成熟、稳重

音乐电台、客服助手、有声书、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 霍拙石

**voice 参数**: `huozhuoshi_v3.1`

男

清亮

有声书、广告营销、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 叶清禾

**voice 参数**: `yeqinghe_v3.1`

女

亲切、温柔

有声书、广告营销、旁白、客服助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 云欢欢

**voice 参数**: `yunhuanhuan_v3.1`

女

高亢、热情

有声书、旁白、客服助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 徐小俏

**voice 参数**: `xuxiaoqiao_v3.1`

女

自然、俏皮

有声书、旁白、客服助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 白安然

**voice 参数**: `baianran_v3.1`

女

低沉、浑厚、气声

配音讲解、有声书、旁白

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 许言初

**voice 参数**: `xuyanchu_v3.1`

女

沉稳、磁性

新闻播报、有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 叶知晴

**voice 参数**: `yezhiqing_v3.1`

女

轻快、自然

儿童故事、客服助手、语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 安迪

**voice 参数**: `andi_v3.1`

男

ABC口音

语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 安语晴

**voice 参数**: `anyuqing_v3.1`

女

甜妹

语音助手、旁白、新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 林小灵

**voice 参数**: `linxiaoling_v3.1`

女

甜妹

语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙菲菲\_v3.1

**voice 参数**: `longfeifei_v3.1`

女

甜妹

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙婧\_v3.1

**voice 参数**: `longjing_v3.1`

女

质感、沉稳

新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙嫱\_v3.1

**voice 参数**: `longqiang_v3.1`

女

浪漫、风情

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙颜\_v3.1

**voice 参数**: `longyan_v3.1`

女

温暖、自然、亲切

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙小白\_v3.1

**voice 参数**: `longxiaobai_v3.1`

女

磁性、质感

新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙悦\_v3.1

**voice 参数**: `longyue_v3.1`

女

温暖、磁性

有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙橙\_v3.1

**voice 参数**: `longcheng_v3.1`

男

智慧、磁性

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙老铁\_v3.1

**voice 参数**: `longlaotie_v3.1`

男

东北、直率

方言

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙邵\_v3.1

**voice 参数**: `longshao_v3.1`

男

积极、元气

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙书\_v3.1

**voice 参数**: `longshu_v3.1`

男

沉稳、磁性

新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙泽\_v3.1

**voice 参数**: `longze_v3.1`

男

温暖、元气、自然

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙浩\_v3.1

**voice 参数**: `longhao_v3.1`

男

多情、忧郁

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙津\_v3.1

**voice 参数**: `longjin_v3.1`

男

优雅、温润

诗词朗诵

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙楠\_v3.1

**voice 参数**: `longnan_v3.1`

男

睿智

有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙硕\_v3.1

**voice 参数**: `longshuo_v3.1`

男

博才、干练

新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙天\_v3.1

**voice 参数**: `longtian_v3.1`

男

磁性、理智

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙小诚\_v3.1

**voice 参数**: `longxiaocheng_v3.1`

男

磁性、低音

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙可\_v3.1

**voice 参数**: `longke_v3.1`

儿童

懵懂

童声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Bella\_v3.1

**voice 参数**: `loongbella_v3.1`

女

干练、磁性、知性

英文、新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 中文试听

#### 英文试听

#### 精品英文音色

以下音色仅支持英文。

**音色信息**

**性别**

**口音**

**特性支持**

**试听**

**名称**: Emily

**voice 参数**: `Emily_v3.1`

女

英式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Luna

**voice 参数**: `Luna_v3.1`

女

英式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Eric

**voice 参数**: `Eric_v3.1`

男

英式男声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Luca

**voice 参数**: `Luca_v3.1`

男

英式男声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Abby

**voice 参数**: `Abby_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Annie

**voice 参数**: `Annie_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Ava

**voice 参数**: `Ava_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Beth

**voice 参数**: `Beth_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Betty

**voice 参数**: `Betty_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Cally

**voice 参数**: `Cally_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Cindy

**voice 参数**: `Cindy_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Donna

**voice 参数**: `Donna_v3.1`

女

美式女声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Andy

**voice 参数**: `Andy_v3.1`

男

美式男声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: Brian

**voice 参数**: `Brian_v3.1`

男

美式男声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: David

**voice 参数**: `David_v3.1`

男

美式男声

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 其他系统音色

**音色信息**

**性别**

**声线特质**

**适用场景**

**特性支持**

**试听**

**名称**: 龙安元妃\_v3.1

**voice 参数**: `longanyuanfei_v3.1`

女

高傲妃子音

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙杰力豆\_v3.1

**voice 参数**: `longjielidou_v3.1`

男

天真男童音

儿童陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安灵希\_v3.1

**voice 参数**: `longanlingxi_v3.1`

女

可爱甜美音

社交陪伴（精品中文）

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙火火\_v3.1

**voice 参数**: `longhuohuo_v3.1`

男

顽皮少年音

角色音

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙应桃\_v3.1

**voice 参数**: `longyingtao_v3.1`

女

温柔淡定女

客服

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安雅\_v3.1

**voice 参数**: `longanya_v3.1`

女

高雅气质女

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙婉\_v3.1

**voice 参数**: `longwan_v3.1`

女

细腻柔声女

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙星\_v3.1

**voice 参数**: `longxing_v3.1`

女

温婉邻家女

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙华\_v3.1

**voice 参数**: `longhua_v3.1`

女

元气甜美女

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙寒\_v3.1

**voice 参数**: `longhan_v3.1`

男

温暖痴情男

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安智\_v3.1

**voice 参数**: `longanzhi_v3.1`

男

睿智轻熟男

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙哲\_v3.1

**voice 参数**: `longzhe_v3.1`

男

呆板大暖男

社交陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安洋\_v3.1

**voice 参数**: `longanyang_v3.1`

男

阳光大男孩

社交陪伴（标杆音色）

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 李白\_v3.1

**voice 参数**: `libai_v3.1`

男

古代诗仙男

诗词朗诵

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙铃\_v3.1

**voice 参数**: `longling_v3.1`

女

稚气呆板女

童声

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙牛牛\_v3.1

**voice 参数**: `longniuniu_v3.1`

男

阳光男童声

消费电子-儿童有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙闪闪\_v3.1

**voice 参数**: `longshanshan_v3.1`

男

戏剧化童声

消费电子-儿童有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙泡泡\_v3.1

**voice 参数**: `longpaopao_v3.1`

女

飞天泡泡音

消费电子-儿童陪伴

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: loongstella\_v3.1

**voice 参数**: `loongstella_v3.1`

女

飒爽利落女

新闻播报

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙媛\_v3.1

**voice 参数**: `longyuan_v3.1`

女

温暖治愈女

有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙妙\_v3.1

**voice 参数**: `longmiao_v3.1`

女

抑扬顿挫女

有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙三叔\_v3.1

**voice 参数**: `longsanshu_v3.1`

男

沉稳质感男

有声书

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安莉\_v3.1

**voice 参数**: `longanli_v3.1`

女

利落从容女

语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安温\_v3.1

**voice 参数**: `longanwen_v3.1`

女

优雅知性女

语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安朗\_v3.1

**voice 参数**: `longanlang_v3.1`

男

清爽利落男

语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙小夏\_v3.1

**voice 参数**: `longxiaoxia_v3.1`

女

沉稳权威女

语音助手

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**: 龙安冲\_v3.1

**voice 参数**: `longanchong_v3.1`

男

激情推销男

直播带货

SSML: 支持

指令控制: 支持

时间戳: 支持

#### 小语种音色

**音色信息**

**语种**

**性别**

**特性支持**

**试听**

**音色名称**: Zora

**本地名称**: Зора

**voice 参数**: `qwen-audio-3.1-tts-flash-zora_bg`

保加利亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Linde

**本地名称**: Linde

**voice 参数**: `qwen-audio-3.1-tts-flash-linde_nl`

荷兰语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Hajnal

**本地名称**: Hajnal

**voice 参数**: `qwen-audio-3.1-tts-flash-hajnal_hu`

匈牙利语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Senin

**本地名称**: Senin

**voice 参数**: `qwen-audio-3.1-tts-flash-senin_ro`

罗马尼亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Birk

**本地名称**: Birk

**voice 参数**: `qwen-audio-3.1-tts-flash-birk_da`

丹麦语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Lipa

**本地名称**: Lipa

**voice 参数**: `qwen-audio-3.1-tts-flash-lipa_hr`

克罗地亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Avgi

**本地名称**: Αυγή

**voice 参数**: `qwen-audio-3.1-tts-flash-avgi_el`

希腊语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Jitrenka

**本地名称**: Jitřenka

**voice 参数**: `qwen-audio-3.1-tts-flash-jitrenka_cs`

捷克语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Solglimt

**本地名称**: Solglimt

**voice 参数**: `qwen-audio-3.1-tts-flash-solglimt_nn`

挪威语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Glimma

**本地名称**: Glimma

**voice 参数**: `qwen-audio-3.1-tts-flash-glimma_sv`

瑞典语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Svar

**本地名称**: स्वर

**voice 参数**: `qwen-audio-3.1-tts-flash-svar_hi`

印地语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Iskra

**本地名称**: Iskra

**voice 参数**: `qwen-audio-3.1-tts-flash-iskra_sk`

斯洛伐克语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Aava

**本地名称**: Aava

**voice 参数**: `qwen-audio-3.1-tts-flash-aava_fi`

芬兰语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Sahar

**本地名称**: سحر

**voice 参数**: `qwen-audio-3.1-tts-flash-sahar_ur`

乌尔都语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Jasna

**本地名称**: Јасна

**voice 参数**: `qwen-audio-3.1-tts-flash-jasna_sr`

塞尔维亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Brisa

**本地名称**: Brisa

**voice 参数**: `qwen-audio-3.1-tts-flash-brisa_es_mx`

墨西哥西班牙语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Ausra

**本地名称**: Aušra

**voice 参数**: `qwen-audio-3.1-tts-flash-ausra_lt`

立陶宛语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Rasa

**本地名称**: Rasa

**voice 参数**: `qwen-audio-3.1-tts-flash-rasa_lv`

拉脱维亚语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Deniz

**本地名称**: Deniz

**voice 参数**: `qwen-audio-3.1-tts-flash-deniz_tr`

土耳其语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Ava

**本地名称**: آوا

**voice 参数**: `qwen-audio-3.1-tts-flash-ava_fa`

波斯语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Or

**本地名称**: אור

**voice 参数**: `qwen-audio-3.1-tts-flash-or_he`

希伯来语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Ayalguu

**本地名称**: Аялгуу

**voice 参数**: `qwen-audio-3.1-tts-flash-ayalguu_mn`

蒙古语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Zarja

**本地名称**: Zarja

**voice 参数**: `qwen-audio-3.1-tts-flash-zarja_sl`

斯洛文尼亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Ishiq

**本地名称**: İşıq

**voice 参数**: `qwen-audio-3.1-tts-flash-ishiq_az`

阿塞拜疆语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Zorza

**本地名称**: Zorza

**voice 参数**: `qwen-audio-3.1-tts-flash-zorza_pl`

波兰语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Alba

**本地名称**: Alba

**voice 参数**: `qwen-audio-3.1-tts-flash-alba_ca`

加泰罗尼亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Romduol

**本地名称**: រំដួល

**voice 参数**: `qwen-audio-3.1-tts-flash-romduol_km`

高棉语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Aurora

**本地名称**: Aurora

**voice 参数**: `qwen-audio-3.1-tts-flash-aurora_pt_br`

巴西葡萄牙语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Dao

**本地名称**: ດາວ

**voice 参数**: `qwen-audio-3.1-tts-flash-dao_lo`

老挝语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Tsiskari

**本地名称**: ცისკარი

**voice 参数**: `qwen-audio-3.1-tts-flash-tsiskari_ka`

格鲁吉亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Lente

**本地名称**: Lente

**voice 参数**: `qwen-audio-3.1-tts-flash-lente_af`

南非荷兰语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Kiran

**本地名称**: किरण

**voice 参数**: `qwen-audio-3.1-tts-flash-kiran_ne`

尼泊尔语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Zorka

**本地名称**: Зорка

**voice 参数**: `qwen-audio-3.1-tts-flash-zorka_be`

白俄罗斯语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Nilaav

**本地名称**: നിലാവ്

**voice 参数**: `qwen-audio-3.1-tts-flash-nilaav_ml`

马拉雅拉姆语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Staer

**本地名称**: Stär

**voice 参数**: `qwen-audio-3.1-tts-flash-staer_lb`

卢森堡语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Drita

**本地名称**: Drita

**voice 参数**: `qwen-audio-3.1-tts-flash-drita_sq`

阿尔巴尼亚语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Nila

**本地名称**: நிலா

**voice 参数**: `qwen-audio-3.1-tts-flash-nila_ta`

泰米尔语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Aruna

**本地名称**: අරුණ

**voice 参数**: `qwen-audio-3.1-tts-flash-aruna_si`

僧伽罗语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Vennela

**本地名称**: వెన్నెల

**voice 参数**: `qwen-audio-3.1-tts-flash-vennela_te`

泰卢固语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Sade

**本地名称**: Säde

**voice 参数**: `qwen-audio-3.1-tts-flash-sade_et`

爱沙尼亚语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Bituon

**本地名称**: Bituon

**voice 参数**: `qwen-audio-3.1-tts-flash-bituon_ceb`

宿务语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Vedrina

**本地名称**: Vedrina

**voice 参数**: `qwen-audio-3.1-tts-flash-vedrina_bs`

波斯尼亚语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: LaYaung

**本地名称**: လရောင်

**voice 参数**: `qwen-audio-3.1-tts-flash-layaung_my`

缅甸语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Luys

**本地名称**: Լույս

**voice 参数**: `qwen-audio-3.1-tts-flash-luys_hy`

亚美尼亚语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Lumen

**本地名称**: Lumen

**voice 参数**: `qwen-audio-3.1-tts-flash-lumen_la`

拉丁语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Birta

**本地名称**: Birta

**voice 参数**: `qwen-audio-3.1-tts-flash-birta_is`

冰岛语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Zerniq

**本地名称**: Żerniq

**voice 参数**: `qwen-audio-3.1-tts-flash-zerniq_mt`

马耳他语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Nuru

**本地名称**: Nuru

**voice 参数**: `qwen-audio-3.1-tts-flash-nuru_sw`

斯瓦希里语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Arai

**本地名称**: Арай

**voice 参数**: `qwen-audio-3.1-tts-flash-arai_kk`

哈萨克语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Zetwal

**本地名称**: Zetwal

**voice 参数**: `qwen-audio-3.1-tts-flash-zetwal_crs`

塞舌尔克里奥尔语

女

SSML: 支持

指令控制: 支持

时间戳: 支持

**音色名称**: Zoria

**本地名称**: Зоря

**voice 参数**: `qwen-audio-3.1-tts-flash-zoria_uk`

乌克兰语

男

SSML: 支持

指令控制: 支持

时间戳: 支持

### qwen-audio-3.0-tts-plus

**适用场景**

**音色信息**

**特性支持**

**音频试听（右键保存音频）**

社交陪伴（旗舰音色）

**名称**：龙安灵心

**voice参数**：longanlingxin

**特质**：知心温暖音

**年龄**：25岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙安鲁风

**voice参数**：longanlufeng

**特质**：明亮开朗音

**年龄**：25岁

**性别**：男

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

### qwen-audio-3.0-tts-flash

**适用场景**

**音色信息**

**特性支持**

**音频试听（右键保存音频）**

社交陪伴（精品中文）

**名称**：龙安风悦

**voice参数**：longanfengyue

**特质**：自然亲切音

**年龄**：30岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙安元妃

**voice参数**：longanyuanfei

**特质**：高傲妃子音

**年龄**：30岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙安灵希

**voice参数**：longanlingxi

**特质**：可爱甜美音

**年龄**：25岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙安小昕

**voice参数**：longanxiaoxin

**特质**：亲切活泼音

**年龄**：22岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙安欢

**voice参数**：longanhuan\_v3.6

**年龄**：25岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

儿童陪伴/智能玩具（精品儿童）

**名称**：龙杰力豆

**voice参数**：longjielidou\_v3.6

**特质**：天真男童

**年龄**：5岁

**性别**：男

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙泡泡

**voice参数**：longpaopao\_v3.6

**特质**：软糯可爱音

**年龄**：5岁

**性别**：女

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

角色音/游戏（精品中文）

**名称**：龙火火

**voice参数**：longhuohuo\_v3.6

**特质**：顽皮少年音

**年龄**：8岁

**性别**：男

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

**名称**：龙川叔

**voice参数**：longchuanshu\_v3.6

**特质**：川普大叔音

**年龄**：40岁

**性别**：男

**语言**：中文（普通话）、英文

SSML: 支持

指令控制: 支持

时间戳: 支持

社交陪伴/语音助手（精品英文）

**名称**：loongmary

**voice参数**：loongmary

**特质**：温暖英音

**年龄**：20岁

**性别**：女

**语言**：英文

SSML: 不支持

指令控制: 不支持

时间戳: 不支持

**名称**：loongeva

**voice参数**：loongeva\_v3.6

**特质**：高智美音

**年龄**：28岁

**性别**：女

**语言**：英文

SSML: 不支持

指令控制: 不支持

时间戳: 不支持

**名称**：loongJohn

**voice参数**：loongjohn

**特质**：沉稳亲切美音

**年龄**：28岁

**性别**：男

**语言**：英文

SSML: 不支持

指令控制: 不支持

时间戳: 不支持

## 基础音色

**说明**建议优先使用系统音色，以获得更稳定的语音合成效果。如需定制音色，可通过[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)或[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)创建专属音色。基础音色提供更多选择，使用前建议试听并评估其是否符合业务需求。

除上述系统音色外，`qwen-audio-3.0-tts-plus`和`qwen-audio-3.0-tts-flash`各自还提供500余个通过声音复刻生成的基础音色，调用方式与系统音色一致。

基础音色命名格式为`qwen-audio-3.0-tts-{plus|flash}-{音色后缀}`，两个模型同一后缀对应同一套试听音频。

-   `qwen-audio-3.0-tts-plus`基础音色列表（Excel）：[qwen-audio-3.0-tts-plus基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/ydwqqz/qwen-audio-3.0-tts-plus%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
-   `qwen-audio-3.0-tts-flash`基础音色列表（Excel）：[qwen-audio-3.0-tts-flash基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/thosjr/qwen-audio-3.0-tts-flash%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
-   基础音色试听音频包（plus和flash共用）：[基础音色试听音频包.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260720/tuuuqo/%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2%E8%AF%95%E5%90%AC%E9%9F%B3%E9%A2%91%E5%8C%85.zip)

**试听步骤**

1.  下载Excel和试听音频包，将音频包解压到本地。
2.  在Excel中找到“预览音频文件名”列，获取音频文件名。
3.  在解压目录中找到对应文件，使用播放器打开试听。
