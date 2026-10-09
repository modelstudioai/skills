# Qwen-Audio-TTS音色列表

查看 Qwen-Audio-TTS 各模型的系统音色，试听音色效果，并下载基础音色列表和试听音频。

**说明**

-   所选音色（`voice`）必须属于当前模型（`model`）支持的音色列表，不能跨模型混用。音色不匹配时，服务会返回 `InvalidParameter` 错误，例如 `[cosyvoice:]Engine error [411]: TTS speak operation failed`。
-   待合成文本（`text`）应使用所选音色支持的语言，否则可能出现发音错误或语音不自然。

如需专属音色，请参见[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)或[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)。

## 系统音色

### qwen-audio-3.1-tts-flash

以下音色适用于 `qwen-audio-3.1-tts-flash`。`voice` 值区分大小写。

#### 多语种与方言音色

以下四个音色均支持下列全部方言和语言。

-   方言：上海话、广东话、东北话、重庆话、陕西话、云南话、宁波话、甘肃话。
-   语言：日语、韩语、法语、德语、葡萄牙语、意大利语、越南语、印尼语。

名称

voice 参数

性别

试听

龙安欢\_v3.1

`longanhuan_v3.1`

女

重庆话

宁波话

韩语

印尼语

龙安灵心\_v3.1

`longanlingxin_v3.1`

女

云南话

陕西话

上海话

法语

意大利语

龙安风悦\_v3.1

`longanfengyue_v3.1`

女

东北话

越南语

日语

许南川

`xunanchuan_v3.1`

男

甘肃话

东北话

法语

葡萄牙语

#### 精品中文音色

以下音色仅支持中文普通话。

名称

voice 参数

性别

声线特质

适用场景

试听

于小云

`yuxiaoyun_v3.1`

女

元气、亲切、自然

广告营销、广播、客服助手、旁白

乔小娇

`qiaoxiaojiao_v3.1`

女

俏丽、可爱

广告营销、客服助手、有声书

夏小晨

`xiaxiaochen_v3.1`

女

元气、明亮

广告营销、有声书

安明远

`anmingyuan_v3.1`

男

清亮、自然

广告营销、有声书、旁白

温怀清

`wenhuaiqing_v3.1`

女

清亮、柔和

儿童故事、客服助手、广告营销、新闻播报

安小岚

`anxiaolan_v3.1`

女

清甜、纯净

有声书、客服助手、旁白、新闻播报、广告营销

谢舒柔

`xieshurou_v3.1`

女

柔和、自然、知性

有声书、客服助手、旁白

白清岚

`baiqinglan_v3.1`

女

明亮、清纯

语音助手、客服助手

许玉远

`xuyuyuan_v3.1`

女

知性、成熟、质感

广告营销、新闻播报、旁白、客服助手、有声书

安若柔

`anruorou_v3.1`

女

气声、知性

旁白、语音助手

闻怀之

`wenhuaizhi_v3.1`

女

稳重、成熟

有声书、新闻播报、广告营销、客服助手、旁白

萧行之

`xiaoxingzhi_v3.1`

女

端庄、贵气

新闻播报、有声书、旁白、客服助手

顾云舒

`guyunshu_v3.1`

女

成熟、稳重

音乐电台、客服助手、有声书、旁白

霍拙石

`huozhuoshi_v3.1`

男

清亮

有声书、广告营销、旁白

叶清禾

`yeqinghe_v3.1`

女

亲切、温柔

有声书、广告营销、旁白、客服助手

云欢欢

`yunhuanhuan_v3.1`

女

高亢、热情

有声书、旁白、客服助手

徐小俏

`xuxiaoqiao_v3.1`

女

自然、俏皮

有声书、旁白、客服助手

白安然

`baianran_v3.1`

女

低沉、浑厚、气声

配音讲解、有声书、旁白

许言初

`xuyanchu_v3.1`

女

沉稳、磁性

新闻播报、有声书

叶知晴

`yezhiqing_v3.1`

女

轻快、自然

儿童故事、客服助手、语音助手

安迪

`andi_v3.1`

男

ABC口音

语音助手

安语晴

`anyuqing_v3.1`

女

甜妹

语音助手、旁白、新闻播报

#### 精品英文音色

以下音色仅支持英文。

名称

voice 参数

性别

口音

试听

Emily

`Emily_v3.1`

女

英式女声

Luna

`Luna_v3.1`

女

英式女声

Eric

`Eric_v3.1`

男

英式男声

Luca

`Luca_v3.1`

男

英式男声

Abby

`Abby_v3.1`

女

美式女声

Annie

`Annie_v3.1`

女

美式女声

Ava

`Ava_v3.1`

女

美式女声

Beth

`Beth_v3.1`

女

美式女声

Betty

`Betty_v3.1`

女

美式女声

Cally

`Cally_v3.1`

女

美式女声

Cindy

`Cindy_v3.1`

女

美式女声

Donna

`Donna_v3.1`

女

美式女声

Andy

`Andy_v3.1`

男

美式男声

Brian

`Brian_v3.1`

男

美式男声

David

`David_v3.1`

男

美式男声

#### 其他系统音色

名称

voice 参数

性别

声线特质

适用场景

试听

龙安元妃\_v3.1

`longanyuanfei_v3.1`

女

高傲妃子音

社交陪伴

龙杰力豆\_v3.1

`longjielidou_v3.1`

男

天真男童音

儿童陪伴

龙安灵希\_v3.1

`longanlingxi_v3.1`

女

可爱甜美音

社交陪伴（精品中文）

龙火火\_v3.1

`longhuohuo_v3.1`

男

顽皮少年音

角色音

龙应桃\_v3.1

`longyingtao_v3.1`

女

温柔淡定女

客服

龙安雅\_v3.1

`longanya_v3.1`

女

高雅气质女

社交陪伴

龙婉\_v3.1

`longwan_v3.1`

女

细腻柔声女

社交陪伴

龙星\_v3.1

`longxing_v3.1`

女

温婉邻家女

社交陪伴

龙华\_v3.1

`longhua_v3.1`

女

元气甜美女

社交陪伴

龙寒\_v3.1

`longhan_v3.1`

男

温暖痴情男

社交陪伴

龙安智\_v3.1

`longanzhi_v3.1`

男

睿智轻熟男

社交陪伴

龙哲\_v3.1

`longzhe_v3.1`

男

呆板大暖男

社交陪伴

龙安洋\_v3.1

`longanyang_v3.1`

男

阳光大男孩

社交陪伴（标杆音色）

李白\_v3.1

`libai_v3.1`

男

古代诗仙男

诗词朗诵

龙铃\_v3.1

`longling_v3.1`

女

稚气呆板女

童声

龙牛牛\_v3.1

`longniuniu_v3.1`

男

阳光男童声

消费电子-儿童有声书

龙闪闪\_v3.1

`longshanshan_v3.1`

男

戏剧化童声

消费电子-儿童有声书

龙泡泡\_v3.1

`longpaopao_v3.1`

女

飞天泡泡音

消费电子-儿童陪伴

loongstella\_v3.1

`loongstella_v3.1`

女

飒爽利落女

新闻播报

龙媛\_v3.1

`longyuan_v3.1`

女

温暖治愈女

有声书

龙妙\_v3.1

`longmiao_v3.1`

女

抑扬顿挫女

有声书

龙三叔\_v3.1

`longsanshu_v3.1`

男

沉稳质感男

有声书

龙安莉\_v3.1

`longanli_v3.1`

女

利落从容女

语音助手

龙安温\_v3.1

`longanwen_v3.1`

女

优雅知性女

语音助手

龙安朗\_v3.1

`longanlang_v3.1`

男

清爽利落男

语音助手

龙小夏\_v3.1

`longxiaoxia_v3.1`

女

沉稳权威女

语音助手

龙安冲\_v3.1

`longanchong_v3.1`

男

激情推销男

直播带货

### qwen-audio-3.0-tts-plus

**适用场景**

**音色信息**

**音频试听（右键保存音频）**

社交陪伴（旗舰音色）

**名称**：龙安灵心

**voice参数**：longanlingxin

**特质**：知心温暖音

**年龄**：25岁

**性别**：女

**语言**：中文（普通话）、英文

**名称**：龙安鲁风

**voice参数**：longanlufeng

**特质**：明亮开朗音

**年龄**：25岁

**性别**：男

**语言**：中文（普通话）、英文

### qwen-audio-3.0-tts-flash

**适用场景**

**音色信息**

**音频试听（右键保存音频）**

社交陪伴（精品中文）

**名称**：龙安风悦

**voice参数**：longanfengyue

**特质**：自然亲切音

**年龄**：30岁

**性别**：女

**语言**：中文（普通话）、英文

**名称**：龙安元妃

**voice参数**：longanyuanfei

**特质**：高傲妃子音

**年龄**：30岁

**性别**：女

**语言**：中文（普通话）、英文

**名称**：龙安灵希

**voice参数**：longanlingxi

**特质**：可爱甜美音

**年龄**：25岁

**性别**：女

**语言**：中文（普通话）、英文

**名称**：龙安小昕

**voice参数**：longanxiaoxin

**特质**：亲切活泼音

**年龄**：22岁

**性别**：女

**语言**：中文（普通话）、英文

**名称**：龙安欢

**voice参数**：longanhuan\_v3.6

**年龄**：25岁

**性别**：女

**语言**：中文（普通话）、英文

儿童陪伴/智能玩具（精品儿童）

**名称**：龙杰力豆

**voice参数**：longjielidou\_v3.6

**特质**：天真男童

**年龄**：5岁

**性别**：男

**语言**：中文（普通话）、英文

**名称**：龙泡泡

**voice参数**：longpaopao\_v3.6

**特质**：软糯可爱音

**年龄**：5岁

**性别**：女

**语言**：中文（普通话）、英文

角色音/游戏（精品中文）

**名称**：龙火火

**voice参数**：longhuohuo\_v3.6

**特质**：顽皮少年音

**年龄**：8岁

**性别**：男

**语言**：中文（普通话）、英文

**名称**：龙川叔

**voice参数**：longchuanshu\_v3.6

**特质**：川普大叔音

**年龄**：40岁

**性别**：男

**语言**：中文（普通话）、英文

社交陪伴/语音助手（精品英文）

**名称**：loongmary

**voice参数**：loongmary

**特质**：温暖英音

**年龄**：20岁

**性别**：女

**语言**：英文

**名称**：loongeva

**voice参数**：loongeva\_v3.6

**特质**：高智美音

**年龄**：28岁

**性别**：女

**语言**：英文

**名称**：loongJohn

**voice参数**：loongjohn

**特质**：沉稳亲切美音

**年龄**：28岁

**性别**：男

**语言**：英文

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
