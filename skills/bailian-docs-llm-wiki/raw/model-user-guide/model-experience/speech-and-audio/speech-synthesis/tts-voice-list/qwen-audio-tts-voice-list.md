# Qwen-Audio-TTS音色列表

查看 Qwen-Audio-TTS 各模型的系统音色，试听音色效果，并下载基础音色列表和试听音频。

> **说明**
>
> -   所选音色（`voice`）必须属于当前模型（`model`）支持的音色列表，不能跨模型混用。音色不匹配时，服务会返回 `InvalidParameter` 错误，例如 `[cosyvoice:]Engine error [411]: TTS speak operation failed`。
> -   待合成文本（`text`）应使用所选音色支持的语言，否则可能出现发音错误或语音不自然。
>
> 如需专属音色，请参见[音色复刻](../voice-customization/voice-cloning-user-guide.md)或[音色设计](../voice-customization/voice-design-user-guide.md)。

<a id="系统音色"></a>

<a id="system-voices"></a>

## 系统音色

对于支持方言指令的音色，可通过指令控制字段 `instruction` 指定方言，例如 `请讲上海话。`。

<a id="qwen-audio-3-1-tts-plus"></a>

<a id="qwen-tts31-plus-voices"></a>

### qwen-audio-3.1-tts-plus

<a id="sec-tabs"></a>

<a id="旗舰音色"></a>

<a id="旗舰音色-h4"></a>

#### 旗舰音色

<table><thead><tr><th><strong>名称</strong></th><th><strong>性别</strong></th><th><strong>特性支持</strong></th><th><strong>试听</strong></th></tr></thead><tbody><tr><td><p><strong>名称</strong>: 龙安灵心_v3.1</p><p><strong>voice 参数</strong>: <code>longanlingxin_v3.1</code></p></td><td><p>女</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td><a id="sec-tabs-2"></a><section><a id="试听1"></a><section><a id="试听1-h4"></a><h4>试听1</h4><a id="code-block"></a><pre class="language-text"><code>你好呀，我是龙安灵心。在这个快节奏的世界里，我想做你耳畔最温柔的守候。无论是深夜的失眠还是清晨的微光，只要你需要，我都会在这里，用声音拥抱你的每一个情绪瞬间。
</code></pre></section><a id="试听2"></a><section><a id="试听2-h4"></a><h4>试听2</h4><a id="code-block-2"></a><pre class="language-text"><code>今天过得怎么样？有没有遇到什么开心的小事，或者让你眉头紧锁的烦恼？别担心，慢慢说给我听。我会安静地陪伴着你，帮你梳理思绪，让心情像雨后的天空一样，重新变得清澈明亮。
</code></pre></section><a id="试听3"></a><section><a id="试听3-h4"></a><h4>试听3</h4><a id="code-block-3"></a><pre class="language-text"><code>月亮已经爬上了树梢，星星在眨着眼睛。闭上眼睛，想象自己躺在柔软的云朵上，随着微风轻轻飘荡。所有的疲惫都随风散去，现在，请安心入睡，愿你在甜美的梦乡中，遇见最美的风景。
</code></pre></section></section></td></tr><tr><td><p><strong>名称</strong>: 许南川</p><p><strong>voice 参数</strong>: <code>xunanchuan_v3.1</code></p></td><td><p>男</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td><a id="sec-tabs-3"></a><section><a id="试听1-2"></a><section><a id="试听1-2-h4"></a><h4>试听1</h4><a id="code-block-4"></a><pre class="language-text"><code>遇见你之前，我的世界是黑白单调的；遇见你之后，色彩斑斓如雨后彩虹。我想牵着你的手，走过春夏秋冬，看遍世间繁华。无论风雨如何变幻，只要你在身边，便是人间最美风景。
</code></pre></section><a id="试听2-2"></a><section><a id="试听2-2-h4"></a><h4>试听2</h4><a id="code-block-5"></a><pre class="language-text"><code>我是许南川，一个喜欢用声音讲述故事的人。我的声音或许不够华丽，但足够真诚。希望能通过这磁性的语调，带你走进不同的世界，感受文字背后的温度与力量，期待与你相遇。
</code></pre></section><a id="试听3-2"></a><section><a id="试听3-2-h4"></a><h4>试听3</h4><a id="code-block-6"></a><pre class="language-text"><code>在这个喧嚣的时代，保持清醒是一种奢侈。我喜欢在安静的午后，泡一杯茶，读一本好书。那种心灵的宁静，比任何物质的享受都来得珍贵。你呢？是否也渴望这样片刻的安宁？
</code></pre></section></section></td></tr><tr><td><p><strong>名称</strong>: 龙安欢_v3.1</p><p><strong>voice 参数</strong>: <code>longanhuan_v3.1</code></p></td><td><p>女</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td><a id="sec-tabs-4"></a><section><a id="试听1-3"></a><section><a id="试听1-3-h4"></a><h4>试听1</h4><a id="code-block-7"></a><pre class="language-text"><code>嗨，大家好！我是龙安欢。我喜欢笑，喜欢热闹，更喜欢看到大家快乐的样子。有什么烦心事尽管找我，保证让你笑着走出阴霾。让我们一起快乐起来吧！
</code></pre></section><a id="试听2-3"></a><section><a id="试听2-3-h4"></a><h4>试听2</h4><a id="code-block-8"></a><pre class="language-text"><code>买衣服不要只看款式，更要看面料和剪裁。这件大衣版型正，羊毛含量高，穿在身上既保暖又有型。性价比超高，闭眼入都不会错。信我的准没错，赶紧入手一件过冬吧！
</code></pre></section><a id="试听3-3"></a><section><a id="试听3-3-h4"></a><h4>试听3</h4><a id="code-block-9"></a><pre class="language-text"><code>天哪，今天的天气简直太糟糕了！出门忘带伞，结果淋成落汤鸡。不过没关系，回家喝杯热姜茶，洗个热水澡，又是一条好汉！你们今天过得怎么样？有没有什么趣事跟我分享呀？
</code></pre></section></section></td></tr><tr><td><p><strong>名称</strong>: 龙安风悦_v3.1</p><p><strong>voice 参数</strong>: <code>longanfengyue_v3.1</code></p></td><td><p>女</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td><a id="sec-tabs-5"></a><section><a id="试听1-4"></a><section><a id="试听1-4-h4"></a><h4>试听1</h4><a id="code-block-10"></a><pre class="language-text"><code>明天白天多云转晴，气温适宜，最高二十度，最低十五度。风力不大，非常适合户外活动。不过早晚温差较大，建议大家适当增减衣物，预防感冒。出行前记得查看实时路况哦。
</code></pre></section><a id="试听2-4"></a><section><a id="试听2-4-h4"></a><h4>试听2</h4><a id="code-block-11"></a><pre class="language-text"><code>最近我在看一部老电影，里面的配乐特别经典，听得我忍不住单曲循环。你平时喜欢听什么类型的音乐？是轻快的流行乐，还是安静的纯音乐？推荐几首给我呗，我想换换口味。
</code></pre></section><a id="试听3-4"></a><section><a id="试听3-4-h4"></a><h4>试听3</h4><a id="code-block-12"></a><pre class="language-text"><code>外婆坐在藤椅上，手里织着那条没完工的围巾，针脚细密而整齐。夕阳透过窗棂洒在她银白的发丝上，泛着柔和的光晕。她抬起头，笑着对我说：‘天凉了，快戴上吧。’那一刻，时光仿佛静止。
</code></pre></section></section></td></tr></tbody></table>

<a id="qwen-audio-3-1-tts-flash"></a>

<a id="qwen-tts31-voices"></a>

### qwen-audio-3.1-tts-flash

> **说明**
>
> 多语种与方言音色、精品英文音色、小语种音色支持北京和新加坡地域，其他类型音色仅支持北京地域。

<a id="sec-tabs-6"></a>

<a id="多语种与方言音色"></a>

<a id="多语种与方言音色-h4"></a>

#### 多语种与方言音色

<a id="qwen-tts31-multilingual"></a>

以下四个音色均支持下列全部方言和语言。

-   方言：上海话、广东话、东北话、重庆话、陕西话、云南话、宁波话、甘肃话。
-   语言：日语、韩语、法语、德语、葡萄牙语、意大利语、越南语、印尼语。

<a id="qwen-tts31-language-hints"></a>

使用下表中的音色合成方言或部分小语种时，可通过 `language_hints` 指定目标语种或方言。

<a id="accordion-点击查看语种和方言的设置方法"></a>

点击查看语种和方言的设置方法

将语种或方言代号作为数组传给 `language_hints`，每次只传一个代号。待合成文本应与指定的语种或方言一致。合成普通话或英语时，无需设置此参数。

> **说明**
>
> 如果同时使用 `instruction`，可用它控制语气或情感。不要在 `instruction` 中重复指定语种或方言，也不要指定不同的语种或方言。

**示例**

<a id="code-block-13"></a>

```json
{
  "text": "侬好，今朝天气蛮好。",
  "voice": "longanlingxin_v3.1",
  "language_hints": ["zh-sh"]
}
```

**语种和方言取值范围**

> **说明**
>
> 未列出的语种或方言可传 `["other"]`，但不保证所选音色支持。

<a id="sec-tabs-7"></a>

<a id="语种"></a>

<a id="语种-h4"></a>

#### 语种

-   日语：`ja`
-   韩语：`ko`
-   法语：`fr`
-   德语：`de`
-   葡萄牙语：`pt`
-   意大利语：`it`
-   越南语：`vi`
-   印度尼西亚语：`id`
-   阿拉伯语：`ar`
-   西班牙语：`es`
-   马来语：`ms`
-   俄语：`ru`
-   泰语：`th`
-   菲律宾语：`tl`

<a id="方言"></a>

<a id="方言-h4"></a>

#### 方言

-   广东话：`zh-yue`
-   东北话：`zh-ne`
-   甘肃话：`zh-gs`
-   贵州话：`zh-gz`
-   河南话：`zh-ha`
-   河北话：`zh-he`
-   湖北话：`zh-hb`
-   湖南话：`zh-hn`
-   宁夏话：`zh-nx`
-   陕西话：`zh-sx`
-   山西话：`zh-shan`
-   山东话：`zh-sd`
-   青岛话：`zh-qd`
-   四川话：`zh-sc`
-   重庆话：`zh-cq`
-   云南话：`zh-yn`
-   江西话：`zh-jx`
-   浙江话：`zh-zj`
-   宁波话：`zh-nb`
-   上海话：`zh-sh`

| 音色信息 | 性别 | 特性支持 | 试听 |
| --- | --- | --- | --- |
| **名称**: 龙安欢\_v3.1<br><br>**voice 参数**: `longanhuan_v3.1` | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 | <a id="sec-tabs-8"></a><br><br><a id="重庆话"></a><br><br><a id="重庆话-h4"></a><br><br>#### 重庆话<br><br><a id="宁波话"></a><br><br><a id="宁波话-h4"></a><br><br>#### 宁波话<br><br><a id="韩语"></a><br><br><a id="韩语-h4"></a><br><br>#### 韩语<br><br><a id="印尼语"></a><br><br><a id="印尼语-h4"></a><br><br>#### 印尼语 |
| **名称**: 龙安灵心\_v3.1<br><br>**voice 参数**: `longanlingxin_v3.1` | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 | <a id="sec-tabs-9"></a><br><br><a id="云南话"></a><br><br><a id="云南话-h4"></a><br><br>#### 云南话<br><br><a id="陕西话"></a><br><br><a id="陕西话-h4"></a><br><br>#### 陕西话<br><br><a id="上海话"></a><br><br><a id="上海话-h4"></a><br><br>#### 上海话<br><br><a id="法语"></a><br><br><a id="法语-h4"></a><br><br>#### 法语<br><br><a id="意大利语"></a><br><br><a id="意大利语-h4"></a><br><br>#### 意大利语 |
| **名称**: 龙安风悦\_v3.1<br><br>**voice 参数**: `longanfengyue_v3.1` | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 | <a id="sec-tabs-10"></a><br><br><a id="东北话"></a><br><br><a id="东北话-h4"></a><br><br>#### 东北话<br><br><a id="越南语"></a><br><br><a id="越南语-h4"></a><br><br>#### 越南语<br><br><a id="日语"></a><br><br><a id="日语-h4"></a><br><br>#### 日语 |
| **名称**: 许南川<br><br>**voice 参数**: `xunanchuan_v3.1` | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 | <a id="sec-tabs-11"></a><br><br><a id="甘肃话"></a><br><br><a id="甘肃话-h4"></a><br><br>#### 甘肃话<br><br><a id="东北话-2"></a><br><br><a id="东北话-2-h4"></a><br><br>#### 东北话<br><br><a id="法语-2"></a><br><br><a id="法语-2-h4"></a><br><br>#### 法语<br><br><a id="葡萄牙语"></a><br><br><a id="葡萄牙语-h4"></a><br><br>#### 葡萄牙语 |

<a id="精品中文音色"></a>

<a id="精品中文音色-h4"></a>

#### 精品中文音色

<a id="qwen-tts31-chinese"></a>

以下音色仅支持中文普通话。

> **说明**
>
> Bella\_v3.1 同时支持中文普通话和英文。

| 音色信息 | 性别 | 声线特质 | 适用场景 | 特性支持 | 试听 |
| --- | --- | --- | --- | --- | --- |
| **名称**: 于小云<br><br>**voice 参数**: `yuxiaoyun_v3.1` | 女 | 元气、亲切、自然 | 广告营销、广播、客服助手、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 乔小娇<br><br>**voice 参数**: `qiaoxiaojiao_v3.1` | 女 | 俏丽、可爱 | 广告营销、客服助手、有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 夏小晨<br><br>**voice 参数**: `xiaxiaochen_v3.1` | 女 | 元气、明亮 | 广告营销、有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 安明远<br><br>**voice 参数**: `anmingyuan_v3.1` | 男 | 清亮、自然 | 广告营销、有声书、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 温怀清<br><br>**voice 参数**: `wenhuaiqing_v3.1` | 女 | 清亮、柔和 | 儿童故事、客服助手、广告营销、新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 安小岚<br><br>**voice 参数**: `anxiaolan_v3.1` | 女 | 清甜、纯净 | 有声书、客服助手、旁白、新闻播报、广告营销 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 谢舒柔<br><br>**voice 参数**: `xieshurou_v3.1` | 女 | 柔和、自然、知性 | 有声书、客服助手、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 白清岚<br><br>**voice 参数**: `baiqinglan_v3.1` | 女 | 明亮、清纯 | 语音助手、客服助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 许玉远<br><br>**voice 参数**: `xuyuyuan_v3.1` | 女 | 知性、成熟、质感 | 广告营销、新闻播报、旁白、客服助手、有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 安若柔<br><br>**voice 参数**: `anruorou_v3.1` | 女 | 气声、知性 | 旁白、语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 闻怀之<br><br>**voice 参数**: `wenhuaizhi_v3.1` | 女 | 稳重、成熟 | 有声书、新闻播报、广告营销、客服助手、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 萧行之<br><br>**voice 参数**: `xiaoxingzhi_v3.1` | 女 | 端庄、贵气 | 新闻播报、有声书、旁白、客服助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 顾云舒<br><br>**voice 参数**: `guyunshu_v3.1` | 女 | 成熟、稳重 | 音乐电台、客服助手、有声书、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 霍拙石<br><br>**voice 参数**: `huozhuoshi_v3.1` | 男 | 清亮 | 有声书、广告营销、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 叶清禾<br><br>**voice 参数**: `yeqinghe_v3.1` | 女 | 亲切、温柔 | 有声书、广告营销、旁白、客服助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 云欢欢<br><br>**voice 参数**: `yunhuanhuan_v3.1` | 女 | 高亢、热情 | 有声书、旁白、客服助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 徐小俏<br><br>**voice 参数**: `xuxiaoqiao_v3.1` | 女 | 自然、俏皮 | 有声书、旁白、客服助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 白安然<br><br>**voice 参数**: `baianran_v3.1` | 女 | 低沉、浑厚、气声 | 配音讲解、有声书、旁白 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 许言初<br><br>**voice 参数**: `xuyanchu_v3.1` | 女 | 沉稳、磁性 | 新闻播报、有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 叶知晴<br><br>**voice 参数**: `yezhiqing_v3.1` | 女 | 轻快、自然 | 儿童故事、客服助手、语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 安迪<br><br>**voice 参数**: `andi_v3.1` | 男 | ABC口音 | 语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 安语晴<br><br>**voice 参数**: `anyuqing_v3.1` | 女 | 甜妹 | 语音助手、旁白、新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 林小灵<br><br>**voice 参数**: `linxiaoling_v3.1` | 女 | 甜妹 | 语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙菲菲\_v3.1<br><br>**voice 参数**: `longfeifei_v3.1` | 女 | 甜妹 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙婧\_v3.1<br><br>**voice 参数**: `longjing_v3.1` | 女 | 质感、沉稳 | 新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙嫱\_v3.1<br><br>**voice 参数**: `longqiang_v3.1` | 女 | 浪漫、风情 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙颜\_v3.1<br><br>**voice 参数**: `longyan_v3.1` | 女 | 温暖、自然、亲切 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙小白\_v3.1<br><br>**voice 参数**: `longxiaobai_v3.1` | 女 | 磁性、质感 | 新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙悦\_v3.1<br><br>**voice 参数**: `longyue_v3.1` | 女 | 温暖、磁性 | 有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙橙\_v3.1<br><br>**voice 参数**: `longcheng_v3.1` | 男 | 智慧、磁性 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙老铁\_v3.1<br><br>**voice 参数**: `longlaotie_v3.1` | 男 | 东北、直率 | 方言 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙邵\_v3.1<br><br>**voice 参数**: `longshao_v3.1` | 男 | 积极、元气 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙书\_v3.1<br><br>**voice 参数**: `longshu_v3.1` | 男 | 沉稳、磁性 | 新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙泽\_v3.1<br><br>**voice 参数**: `longze_v3.1` | 男 | 温暖、元气、自然 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙浩\_v3.1<br><br>**voice 参数**: `longhao_v3.1` | 男 | 多情、忧郁 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙津\_v3.1<br><br>**voice 参数**: `longjin_v3.1` | 男 | 优雅、温润 | 诗词朗诵 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙楠\_v3.1<br><br>**voice 参数**: `longnan_v3.1` | 男 | 睿智 | 有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙硕\_v3.1<br><br>**voice 参数**: `longshuo_v3.1` | 男 | 博才、干练 | 新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙天\_v3.1<br><br>**voice 参数**: `longtian_v3.1` | 男 | 磁性、理智 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙小诚\_v3.1<br><br>**voice 参数**: `longxiaocheng_v3.1` | 男 | 磁性、低音 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙可\_v3.1<br><br>**voice 参数**: `longke_v3.1` | 儿童 | 懵懂 | 童声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Bella\_v3.1<br><br>**voice 参数**: `loongbella_v3.1` | 女 | 干练、磁性、知性 | 英文、新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 | <a id="sec-tabs-12"></a><br><br><a id="中文试听"></a><br><br><a id="中文试听-h4"></a><br><br>#### 中文试听<br><br><a id="英文试听"></a><br><br><a id="英文试听-h4"></a><br><br>#### 英文试听 |

<a id="精品英文音色"></a>

<a id="精品英文音色-h4"></a>

#### 精品英文音色

<a id="qwen-tts31-english"></a>

以下音色仅支持英文。

| 音色信息 | 性别 | 口音 | 特性支持 | 试听 |
| --- | --- | --- | --- | --- |
| **名称**: Emily<br><br>**voice 参数**: `Emily_v3.1` | 女 | 英式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Luna<br><br>**voice 参数**: `Luna_v3.1` | 女 | 英式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Eric<br><br>**voice 参数**: `Eric_v3.1` | 男 | 英式男声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Luca<br><br>**voice 参数**: `Luca_v3.1` | 男 | 英式男声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Abby<br><br>**voice 参数**: `Abby_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Annie<br><br>**voice 参数**: `Annie_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Ava<br><br>**voice 参数**: `Ava_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Beth<br><br>**voice 参数**: `Beth_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Betty<br><br>**voice 参数**: `Betty_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Cally<br><br>**voice 参数**: `Cally_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Cindy<br><br>**voice 参数**: `Cindy_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Donna<br><br>**voice 参数**: `Donna_v3.1` | 女 | 美式女声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Andy<br><br>**voice 参数**: `Andy_v3.1` | 男 | 美式男声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: Brian<br><br>**voice 参数**: `Brian_v3.1` | 男 | 美式男声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: David<br><br>**voice 参数**: `David_v3.1` | 男 | 美式男声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |

<a id="其他系统音色"></a>

<a id="其他系统音色-h4"></a>

#### 其他系统音色

<a id="qwen-tts31-additional"></a>

| 音色信息 | 性别 | 声线特质 | 适用场景 | 特性支持 | 试听 |
| --- | --- | --- | --- | --- | --- |
| **名称**: 龙安元妃\_v3.1<br><br>**voice 参数**: `longanyuanfei_v3.1` | 女 | 高傲妃子音 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙杰力豆\_v3.1<br><br>**voice 参数**: `longjielidou_v3.1` | 男 | 天真男童音 | 儿童陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安灵希\_v3.1<br><br>**voice 参数**: `longanlingxi_v3.1` | 女 | 可爱甜美音 | 社交陪伴（精品中文） | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙火火\_v3.1<br><br>**voice 参数**: `longhuohuo_v3.1` | 男 | 顽皮少年音 | 角色音 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙应桃\_v3.1<br><br>**voice 参数**: `longyingtao_v3.1` | 女 | 温柔淡定女 | 客服 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安雅\_v3.1<br><br>**voice 参数**: `longanya_v3.1` | 女 | 高雅气质女 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙婉\_v3.1<br><br>**voice 参数**: `longwan_v3.1` | 女 | 细腻柔声女 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙星\_v3.1<br><br>**voice 参数**: `longxing_v3.1` | 女 | 温婉邻家女 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙华\_v3.1<br><br>**voice 参数**: `longhua_v3.1` | 女 | 元气甜美女 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙寒\_v3.1<br><br>**voice 参数**: `longhan_v3.1` | 男 | 温暖痴情男 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安智\_v3.1<br><br>**voice 参数**: `longanzhi_v3.1` | 男 | 睿智轻熟男 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙哲\_v3.1<br><br>**voice 参数**: `longzhe_v3.1` | 男 | 呆板大暖男 | 社交陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安洋\_v3.1<br><br>**voice 参数**: `longanyang_v3.1` | 男 | 阳光大男孩 | 社交陪伴（标杆音色） | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 李白\_v3.1<br><br>**voice 参数**: `libai_v3.1` | 男 | 古代诗仙男 | 诗词朗诵 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙铃\_v3.1<br><br>**voice 参数**: `longling_v3.1` | 女 | 稚气呆板女 | 童声 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙牛牛\_v3.1<br><br>**voice 参数**: `longniuniu_v3.1` | 男 | 阳光男童声 | 消费电子-儿童有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙闪闪\_v3.1<br><br>**voice 参数**: `longshanshan_v3.1` | 男 | 戏剧化童声 | 消费电子-儿童有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙泡泡\_v3.1<br><br>**voice 参数**: `longpaopao_v3.1` | 女 | 飞天泡泡音 | 消费电子-儿童陪伴 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: loongstella\_v3.1<br><br>**voice 参数**: `loongstella_v3.1` | 女 | 飒爽利落女 | 新闻播报 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙媛\_v3.1<br><br>**voice 参数**: `longyuan_v3.1` | 女 | 温暖治愈女 | 有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙妙\_v3.1<br><br>**voice 参数**: `longmiao_v3.1` | 女 | 抑扬顿挫女 | 有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙三叔\_v3.1<br><br>**voice 参数**: `longsanshu_v3.1` | 男 | 沉稳质感男 | 有声书 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安莉\_v3.1<br><br>**voice 参数**: `longanli_v3.1` | 女 | 利落从容女 | 语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安温\_v3.1<br><br>**voice 参数**: `longanwen_v3.1` | 女 | 优雅知性女 | 语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安朗\_v3.1<br><br>**voice 参数**: `longanlang_v3.1` | 男 | 清爽利落男 | 语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙小夏\_v3.1<br><br>**voice 参数**: `longxiaoxia_v3.1` | 女 | 沉稳权威女 | 语音助手 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **名称**: 龙安冲\_v3.1<br><br>**voice 参数**: `longanchong_v3.1` | 男 | 激情推销男 | 直播带货 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |

<a id="小语种音色"></a>

<a id="小语种音色-h4"></a>

#### 小语种音色

| 音色信息 | 语种 | 性别 | 特性支持 | 试听 |
| --- | --- | --- | --- | --- |
| **音色名称**: Zora<br><br>**本地名称**: Зора<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zora_bg` | 保加利亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Linde<br><br>**本地名称**: Linde<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-linde_nl` | 荷兰语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Hajnal<br><br>**本地名称**: Hajnal<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-hajnal_hu` | 匈牙利语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Senin<br><br>**本地名称**: Senin<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-senin_ro` | 罗马尼亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Birk<br><br>**本地名称**: Birk<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-birk_da` | 丹麦语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Lipa<br><br>**本地名称**: Lipa<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-lipa_hr` | 克罗地亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Avgi<br><br>**本地名称**: Αυγή<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-avgi_el` | 希腊语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Jitrenka<br><br>**本地名称**: Jitřenka<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-jitrenka_cs` | 捷克语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Solglimt<br><br>**本地名称**: Solglimt<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-solglimt_nn` | 挪威语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Glimma<br><br>**本地名称**: Glimma<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-glimma_sv` | 瑞典语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Svar<br><br>**本地名称**: स्वर<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-svar_hi` | 印地语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Iskra<br><br>**本地名称**: Iskra<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-iskra_sk` | 斯洛伐克语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Aava<br><br>**本地名称**: Aava<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-aava_fi` | 芬兰语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Sahar<br><br>**本地名称**: سحر<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-sahar_ur` | 乌尔都语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Jasna<br><br>**本地名称**: Јасна<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-jasna_sr` | 塞尔维亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Brisa<br><br>**本地名称**: Brisa<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-brisa_es_mx` | 墨西哥西班牙语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Ausra<br><br>**本地名称**: Aušra<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-ausra_lt` | 立陶宛语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Rasa<br><br>**本地名称**: Rasa<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-rasa_lv` | 拉脱维亚语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Deniz<br><br>**本地名称**: Deniz<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-deniz_tr` | 土耳其语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Ava<br><br>**本地名称**: آوا<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-ava_fa` | 波斯语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Or<br><br>**本地名称**: אור<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-or_he` | 希伯来语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Ayalguu<br><br>**本地名称**: Аялгуу<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-ayalguu_mn` | 蒙古语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Zarja<br><br>**本地名称**: Zarja<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zarja_sl` | 斯洛文尼亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Ishiq<br><br>**本地名称**: İşıq<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-ishiq_az` | 阿塞拜疆语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Zorza<br><br>**本地名称**: Zorza<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zorza_pl` | 波兰语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Alba<br><br>**本地名称**: Alba<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-alba_ca` | 加泰罗尼亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Romduol<br><br>**本地名称**: រំដួល<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-romduol_km` | 高棉语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Aurora<br><br>**本地名称**: Aurora<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-aurora_pt_br` | 巴西葡萄牙语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Dao<br><br>**本地名称**: ດາວ<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-dao_lo` | 老挝语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Tsiskari<br><br>**本地名称**: ცისკარი<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-tsiskari_ka` | 格鲁吉亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Lente<br><br>**本地名称**: Lente<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-lente_af` | 南非荷兰语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Kiran<br><br>**本地名称**: किरण<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-kiran_ne` | 尼泊尔语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Zorka<br><br>**本地名称**: Зорка<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zorka_be` | 白俄罗斯语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Nilaav<br><br>**本地名称**: നിലാവ്<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-nilaav_ml` | 马拉雅拉姆语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Staer<br><br>**本地名称**: Stär<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-staer_lb` | 卢森堡语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Drita<br><br>**本地名称**: Drita<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-drita_sq` | 阿尔巴尼亚语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Nila<br><br>**本地名称**: நிலா<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-nila_ta` | 泰米尔语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Aruna<br><br>**本地名称**: අරුණ<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-aruna_si` | 僧伽罗语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Vennela<br><br>**本地名称**: వెన్నెల<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-vennela_te` | 泰卢固语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Sade<br><br>**本地名称**: Säde<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-sade_et` | 爱沙尼亚语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Bituon<br><br>**本地名称**: Bituon<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-bituon_ceb` | 宿务语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Vedrina<br><br>**本地名称**: Vedrina<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-vedrina_bs` | 波斯尼亚语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: LaYaung<br><br>**本地名称**: လရောင်<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-layaung_my` | 缅甸语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Luys<br><br>**本地名称**: Լույս<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-luys_hy` | 亚美尼亚语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Lumen<br><br>**本地名称**: Lumen<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-lumen_la` | 拉丁语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Birta<br><br>**本地名称**: Birta<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-birta_is` | 冰岛语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Zerniq<br><br>**本地名称**: Żerniq<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zerniq_mt` | 马耳他语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Nuru<br><br>**本地名称**: Nuru<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-nuru_sw` | 斯瓦希里语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Arai<br><br>**本地名称**: Арай<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-arai_kk` | 哈萨克语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Zetwal<br><br>**本地名称**: Zetwal<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zetwal_crs` | 塞舌尔克里奥尔语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Zoria<br><br>**本地名称**: Зоря<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-zoria_uk` | 乌克兰语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Nagi<br><br>**本地名称**: 凪<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-nagi_ja` | 日语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Haneul<br><br>**本地名称**: 하늘<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-haneul_ko` | 韩语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Aube<br><br>**本地名称**: Aube<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-aube_fr` | 法语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Lerche<br><br>**本地名称**: Lerche<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-lerche_de` | 德语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Veter<br><br>**本地名称**: Ветер<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-veter_ru` | 俄语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Rugiada<br><br>**本地名称**: Rugiada<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-rugiada_it` | 意大利语 | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Albor<br><br>**本地名称**: Albor<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-albor_es` | 西班牙语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Farol<br><br>**本地名称**: Farol<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-farol_pt` | 葡萄牙语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Naseem<br><br>**本地名称**: نسيم<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-naseem_ar` | 阿拉伯语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Embun<br><br>**本地名称**: Embun<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-embun_id` | 印尼语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: May<br><br>**本地名称**: Mây<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-may_vi` | 越南语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Bayu<br><br>**本地名称**: Bayu<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-bayu_ms` | 马来语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Sailom<br><br>**本地名称**: สายลม<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-sailom_th` | 泰语 | 男 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |
| **音色名称**: Hiraya<br><br>**本地名称**: Hiraya<br><br>**voice 参数**: `qwen-audio-3.1-tts-flash-hiraya_tl` | 菲律宾语（他加禄语） | 女 | SSML: 支持<br><br>指令控制: 支持<br><br>时间戳: 支持 |  |

<a id="qwen-audio-3-0-tts-plus"></a>

<a id="f399ce27bcc8"></a>

### qwen-audio-3.0-tts-plus

<table><thead><tr><th><p><strong>适用场景</strong></p></th><th><p><strong>音色信息</strong></p></th><th><p><strong>特性支持</strong></p></th><th><p><strong>音频试听（右键保存音频）</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>社交陪伴（旗舰音色）</p></td><td><p><strong>名称</strong>：龙安灵心</p><p><strong>voice参数</strong>：longanlingxin</p><p><strong>特质</strong>：知心温暖音</p><p><strong>年龄</strong>：25岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙安鲁风</p><p><strong>voice参数</strong>：longanlufeng</p><p><strong>特质</strong>：明亮开朗音</p><p><strong>年龄</strong>：25岁</p><p><strong>性别</strong>：男</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr></tbody></table>

<a id="qwen-audio-3-0-tts-flash"></a>

<a id="f399ce27bcc8flash"></a>

### qwen-audio-3.0-tts-flash

<table><thead><tr><th><p><strong>适用场景</strong></p></th><th><p><strong>音色信息</strong></p></th><th><p><strong>特性支持</strong></p></th><th><p><strong>音频试听（右键保存音频）</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p>社交陪伴（精品中文）</p></td><td><p><strong>名称</strong>：龙安风悦</p><p><strong>voice参数</strong>：longanfengyue</p><p><strong>特质</strong>：自然亲切音</p><p><strong>年龄</strong>：30岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙安元妃</p><p><strong>voice参数</strong>：longanyuanfei</p><p><strong>特质</strong>：高傲妃子音</p><p><strong>年龄</strong>：30岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙安灵希</p><p><strong>voice参数</strong>：longanlingxi</p><p><strong>特质</strong>：可爱甜美音</p><p><strong>年龄</strong>：25岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙安小昕</p><p><strong>voice参数</strong>：longanxiaoxin</p><p><strong>特质</strong>：亲切活泼音</p><p><strong>年龄</strong>：22岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙安欢</p><p><strong>voice参数</strong>：longanhuan_v3.6</p><p><strong>年龄</strong>：25岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td rowspan="2"><p>儿童陪伴/智能玩具（精品儿童）</p></td><td><p><strong>名称</strong>：龙杰力豆</p><p><strong>voice参数</strong>：longjielidou_v3.6</p><p><strong>特质</strong>：天真男童</p><p><strong>年龄</strong>：5岁</p><p><strong>性别</strong>：男</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙泡泡</p><p><strong>voice参数</strong>：longpaopao_v3.6</p><p><strong>特质</strong>：软糯可爱音</p><p><strong>年龄</strong>：5岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td rowspan="2"><p>角色音/游戏（精品中文）</p></td><td><p><strong>名称</strong>：龙火火</p><p><strong>voice参数</strong>：longhuohuo_v3.6</p><p><strong>特质</strong>：顽皮少年音</p><p><strong>年龄</strong>：8岁</p><p><strong>性别</strong>：男</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：龙川叔</p><p><strong>voice参数</strong>：longchuanshu_v3.6</p><p><strong>特质</strong>：川普大叔音</p><p><strong>年龄</strong>：40岁</p><p><strong>性别</strong>：男</p><p><strong>语言</strong>：中文（普通话）、英文</p></td><td><p>SSML: 支持</p><p>指令控制: 支持</p><p>时间戳: 支持</p></td><td></td></tr><tr><td rowspan="3"><p>社交陪伴/语音助手（精品英文）</p></td><td><p><strong>名称</strong>：loongmary</p><p><strong>voice参数</strong>：loongmary</p><p><strong>特质</strong>：温暖英音</p><p><strong>年龄</strong>：20岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：英文</p></td><td><p>SSML: 不支持</p><p>指令控制: 不支持</p><p>时间戳: 不支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：loongeva</p><p><strong>voice参数</strong>：loongeva_v3.6</p><p><strong>特质</strong>：高智美音</p><p><strong>年龄</strong>：28岁</p><p><strong>性别</strong>：女</p><p><strong>语言</strong>：英文</p></td><td><p>SSML: 不支持</p><p>指令控制: 不支持</p><p>时间戳: 不支持</p></td><td></td></tr><tr><td><p><strong>名称</strong>：loongJohn</p><p><strong>voice参数</strong>：loongjohn</p><p><strong>特质</strong>：沉稳亲切美音</p><p><strong>年龄</strong>：28岁</p><p><strong>性别</strong>：男</p><p><strong>语言</strong>：英文</p></td><td><p>SSML: 不支持</p><p>指令控制: 不支持</p><p>时间戳: 不支持</p></td><td></td></tr></tbody></table>

<a id="基础音色"></a>

<a id="ext-voices-title"></a>

## 基础音色

> **说明**
>
> 建议优先使用系统音色，以获得更稳定的语音合成效果。如需定制音色，可通过[音色复刻](../voice-customization/voice-cloning-user-guide.md)或[音色设计](../voice-customization/voice-design-user-guide.md)创建专属音色。基础音色提供更多选择，使用前建议试听并评估其是否符合业务需求。

除上述系统音色外，qwen-audio-3.0-tts-plus和qwen-audio-3.0-tts-flash各自还提供500余个通过音色复刻生成的基础音色，调用方式与系统音色一致。

<a id="base-voice-usage"></a>

基础音色命名格式为`qwen-audio-3.0-tts-{plus|flash}-{音色后缀}`，两个模型同一后缀对应同一套试听音频。

<a id="base-voice-downloads"></a>

-   qwen-audio-3.0-tts-plus基础音色列表（Excel）：[qwen-audio-3.0-tts-plus基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/ydwqqz/qwen-audio-3.0-tts-plus%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
-   qwen-audio-3.0-tts-flash基础音色列表（Excel）：[qwen-audio-3.0-tts-flash基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/thosjr/qwen-audio-3.0-tts-flash%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
-   基础音色试听音频包（plus和flash共用）：[基础音色试听音频包.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/files/6a4b3c2d1e0f9016.zip)

**试听步骤**

<a id="base-voice-preview"></a>

1.  下载Excel和试听音频包，将音频包解压到本地。
2.  在Excel中找到“预览音频文件名”列，获取音频文件名。
3.  在解压目录中找到对应文件，使用播放器打开试听。
