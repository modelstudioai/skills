# 万相3.0-视频生成

wan3.0系列是All-in-One视频生成模型，在有声视频生成、多模态参考和视频编辑能力上全面升级。单次生成时长最长30秒、输出帧率30fps，并原生输出台词、BGM和音效，单次支持最多20个多模态素材参考（图片、视频、音频、文档、网页），支持首帧/首尾帧控制和视频编辑与延长。

## 适用范围

-   各地域支持的模型有所差异，且资源相互独立。各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。
-   调用前，先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。
-   调用时，确保**模型、Endpoint URL 和 API Key 均属于同一地域**，跨地域调用将会失败。

**说明**示例代码适用于**北京地域**。

## 模型能力

wan3.0-video / wan3.0-video-prime 是 All-in-One 模型，无需切换模型名称即可覆盖以下全部任务类型。模型根据 `input.media` 中的 `type` 字段和提示词意图自动路由。

**说明**每种任务类型仅支持传入下表中对应的 `type` 值，不同任务类型的 `type` 不可混用。例如，首尾帧模式仅支持 `first_frame` 和 `last_frame`，不可同时传入 `reference_audio` 等其他类型。详细组合规则请参见[素材组合](https://help.aliyun.com/zh/model-studio/wan3-video-generation-api-reference#w30media_combo_t)。

**任务类型**

**触发方式**

**使用说明**

文生视频

仅传入 `prompt`，不传 `media`

支持自由设置分辨率、宽高比和时长

图生视频

首帧生视频

`type` 设为 `first_frame`

`ratio` 建议设为 `adaptive`，模型自动匹配首帧宽高比

首尾帧生视频

`type` 设为 `first_frame` 和 `last_frame`

`ratio` 建议设为 `adaptive`，模型自动匹配首帧宽高比

全模态参考

图片参考

`type` 设为 `reference_image`

最多10张，单张≤20MB

视频参考

`type` 设为 `reference_video`

最多5段，总时长≤15秒，单文件≤100MB

音频参考

`type` 设为 `reference_audio`

最多5段，总时长≤15秒，单文件≤15MB

组合参考

`type` 设为 `reference_image`/`reference_video`/`reference_audio` 组合

参考图片/视频/音频，支持三种参考素材任意组合

-   图片+视频
    
-   图片+音频
    
-   视频+音频
    
-   图片+视频+音频
    

文件/网页生视频参考

`type` 设为 `file` 或 `link`（二选一，各限1个），可与 `reference_image`/`reference_video`/`reference_audio` 组合

解析文档/网页内容生成视频

文档和网页链接仅支持无需登录的公开页面

视频编辑

`type` 设为 `reference_video`（可与 `reference_image`/`reference_audio` 组合）+ 提示词含编辑意图（如"编辑视频""去掉""替换""改成"等）

增删改元素、风格转换、光线编辑、台词编辑。`ratio` 建议 `adaptive`，`duration` 建议 `-1`（自动保持原视频宽高比和时长）

视频延长

`type` 设为 `reference_video`（可与 `reference_image`/`reference_audio` 组合）+ 提示词含延长意图（如"延长""延续""续写""向前/向后延长"等）

向前/向后/双向延长。`ratio` 建议 `adaptive`（自动保持原视频宽高比）

## 提示词技巧

平台提供万相3.0 提示词优化 Skill，方便您对提示词进行调优。

**下载 Skill**：[wan3-pe.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9f66.zip)（下载后解压）

**使用方式**：在 AI 对话框输入 `/wan3-pe` + 您的提示词内容，开始调试提示词。例如：

```
/wan3-pe 基于skill对提示词进行完善，提示词为：一只猫在草地上奔跑
```

## 主要功能

### 文生视频

仅通过提示词生成视频，无需传入任何媒体文件。原生支持最长30秒多镜头叙事，自动生成同步台词、BGM和音效。

-   支持单镜头和多镜头分镜格式（每镜头4~6秒，时间戳标注）。
-   有声视频：原生生成人声台词、环境音效和背景音乐，无需后期配音。
-   智能时长：`duration` 设为 `-1` 时模型自动推荐合适时长。

**参数配置**：`resolution`\=480P/720P/1080P（默认），`ratio`\=21:9/16:9/4:3/1:1/3:4/9:16，`duration`\=2~30秒或-1（智能时长）。

示例1提示词

20秒超宽银幕毛绒宇宙冒险片段，整体采用超精细毛绒材质、电影级太空尺度、可爱外形与强烈动作反差、夸张FPV运镜和真实软体物理。一艘由毛绒布、纽扣、拉链与填充棉制成的宇宙飞船，载着兔子、狐狸和乌鸦三只小型毛绒动物，在由巨大毛线行星、绒毛星云和布偶巨兽组成的宇宙中高速逃亡。一只覆盖深蓝长绒毛、眼睛像两枚玻璃纽扣的巨大星际鲸兽从星云中追赶飞船。动态包括拉链飞船弹射起航、贴着毛线行星高速绕行、巨鲸从后方冲出、穿越纽扣小行星带、被鲸兽吞入体内、沿金色拉链从背部逃出、巨鲸如泄掉填充棉般缓慢变扁、最终穿越粉紫色绒毛星云向彩色纽扣太阳飞去。

示例2提示词

内容梗概

这是一场发生在色彩明亮的未来废土上、充满了冷幽默与荒诞感的“加油”事件。在一个被遗忘的、类似66号公路的加油站，百无聊赖的工作人员迎来了一位奇特的客人——一个骑着真马的酷酷女牛仔。就在工作人员以为这只是个路过的疯子时，女牛仔却径直走向加油机，拿起油枪，为她的马“加满”了新鲜的青草。这超现实的一幕，让见多识广的工作人员彻底陷入了认知失调的呆滞状态。

场景描述与光影美学

视觉风格: 写实风格，色彩处理上采用高饱和度、高亮度的电影调色，营造出一种“晴朗”感，让荒诞的故事发生在一个无比正常、甚至有点美好的环境里。

色彩美学: 严格遵循明亮的“青橙配色”体系。

青色（Teal）: 万里无云的天空是明亮、清澈的蔚蓝色（偏青）。加油站的主要建筑是复古的黄橙蓝配色，建筑微微褪色。加油机是褪色的复古红。

橙色（Orange）: 地面是龟裂的橙色干涸土地。远处的山脉呈现出温暖的赤陶色。女牛仔的围巾或夹克是橙色的。

角色与场景:

女牛仔: 形象酷飒，沉默寡言。戴着一顶宽檐牛仔帽。穿着耐磨的工装靴和牛仔裤，身上有长途旅行的风尘痕迹。

马: 一匹神态淡定、毛色普通的真马，仿佛对这一切早已司空见惯。

加油站工作人员: 穿着油腻的蓝色工装，戴着一副巨大的黑色墨镜，百无聊赖地靠在椅子上，嘴里叼着一根牙签。他是本片的核心“反应镜头”担当。

加油站: 经典的66号公路风格，旁边有一个小小的便利店，门口放着一台褪色的可乐贩卖机，充满了美式复古感。

3.  运镜风格描述

运镜风格是“冷静的旁观与荒诞的特写（Calm Observation & Absurd Close-up）”：

大量使用固定的中景镜头和缓慢的横移，以一种非常冷静、客观的视角来记录事件，不做任何情绪引导。

在关键的荒诞行为发生时，镜头会突然给到一个极端的特写，比如油枪喷出草的瞬间，或者工作人员呆滞的面部表情，通过这种突兀的放大来制造笑点。

4.  分镜描述

0s - 8s：序幕：无聊的午后

大全景（固定）。蓝天，风沙。一个复古的黄橙蓝配色微微褪色的加油站孤独地立在公路旁。加油站门口，一个工作人员戴着墨镜，懒洋洋地躺在椅子上打盹。一切都安静得只剩下风声。

远景。地平线上，一个骑着马的女牛仔缓缓出现，打破了这份宁静。

中景。工作人员被马蹄声惊醒，他扶了扶墨镜，不耐烦地坐直了身体，看着这个奇怪的组合，嘴里叼着的牙签动了动，脸上写满了“又是个问路的”。

8s - 16s：破：一本正经的胡闹

女牛仔没有说话，她利落地翻身下马，牵着马，径直走向一台老式的加油机。马儿熟练地将头伸到加油机旁。

工作人员的主观视角（略带鱼眼）: 镜头模仿他从墨镜后看出去的视角，那个女人和马的组合显得更加古怪。他看到女牛仔真的拿起了加油枪。

近景。工作人员的眉头皱了起来，他觉得这女人在寻开心。他摘下了墨镜，准备开口呵斥。

慢动作特写: 就在他摘下墨镜的瞬间，他看到女牛仔将油枪的喷嘴对准了马嘴，然后扣动了扳机。

16s - 24s：急：【高潮】认知崩溃的瞬间

【终极反差】:

特写: 油枪喷嘴。喷出的不是汽油，而是一股股新鲜翠绿、还带着水珠的青草！

极端特写: 镜头快切到工作人员那张呆若木鸡的脸上。他的眼睛瞪得像铜铃，嘴巴微微张开，叼着的牙签都忘记了动弹。他的表情凝固了，仿佛世界观在这一秒被彻底颠覆。

中景。马儿吃得津津有味，幸福地眯上了眼睛，然后心满意足地、有力地甩了一下尾巴。马尾扫起的灰尘，正好扑了旁边还在呆滞的工作人员一脸。

24s - 30s：合：绝尘而去，留下呆滞

“加满”了草。女牛仔将油枪挂回原位。她从口袋里掏出几枚硬币，走到便利店门口，“叮叮当当”地扔进了柜台上的一个铁皮罐子里。

她回头看了一眼还在石化状态的工作人员，帽檐下的嘴角似乎微微上扬了一下。

【终极定格】: 她翻身上马，绝尘而去。

镜头缓缓推向工作人员。他依然保持着那个呆若木鸡的姿势，满脸灰尘，手里还捏着刚刚摘下的墨镜，嘴里的牙签终于“啪嗒”一声掉在了地上。

定格在他这张怀疑人生的脸上，全片在荒诞的寂静中结束，只留下一阵风吹过时，牙签在地上滚动的声音。

示例3提示词

镜头1 \[0秒-30秒\]

近景，平视视角，连续快速摇镜，一镜到底（单镜头连续无缝运镜）：

画面左侧是身穿黑色潮流导演马甲、戴着高档专业工作耳麦的导演，其左下方放置着一台巨大的专业电影摄像机。右侧是妆容精致、留着时尚韩式逗号刘海、身穿高定制西装的关系户小鲜肉。背景是宽敞的专业影棚拍摄现场，可见巨大的绿色幕布、数个高耸的影视级C型灯架、缠绕的电线，以及在背景中穿梭忙碌的灯光师和化妆师等工作人员。

专业影棚人工光。柔和的LED柔光箱光源从右侧洒入，将三位主角的面部均匀照亮，场景色彩饱满。背景的摄影器材与绿幕在充足的影棚灯光下投射出淡淡的阴影，呈现出真实而忙碌的现代化大制作片场质感。

镜头手持拍摄一镜到底，近景，镜头一开始，拍摄导演，导演无所谓的表情，瞥了一眼画面右侧斜前方画外的一眼关系户小鲜肉，对他下达指令，说道：“媒体故意黑你，做个表情看看”。说完后镜头快速右摇到关系户面部近景，镜头不要切镜，关系户小鲜肉，面部朝向画面左侧斜前方画外导演方向，神色自若，眼神真挚而自信。他嘴唇微动，神情专业地向对方阐述到““就这种事情来说，情绪可以有好几种”，说话时，头部伴有极其轻微的自然晃动，说完后镜头快速左摇到导演面部近景，镜头不要切镜，导演思索了一下，一边挑衅似地歪了歪头，向关系户小鲜肉说到““狗仔爆料你深夜幽会”，导演说完台词后，镜头迅速右摇到小鲜肉面部近景，不要切镜，关系户小鲜肉，面部朝向画面左侧斜前方画外导演方向，并快速进入表演状态，他眉头紧锁，眼神慌乱、焦急地快速游移，随后他狠狠地咬紧下唇，闭上双眼，整张脸（虽带着精致妆容）因极度的焦虑而紧绷，完美呈现出面对偶像生涯毁灭时，内心惊恐、紧张交织的挣扎状态。表演完后， 镜头再次迅速左摇到导演近景，不要切镜，导演面部表情微变，语速加快，说到““媒体又帮你洗白了，说那是你亲姐！”导演说完后，镜头再次迅速右摇到小鲜肉近景，镜头不要切镜，镜头中，关系户小鲜肉，面部朝向画面左侧斜前方画外导演方向，他的表情在千分之一秒内完成神级转换。他先是面部一滞，随后双眼猛地眯起，嘴角极大程度地咧开，露出一排白皙的牙齿，展露出一个极其夸张、甚至有些变形的狂喜笑容。这种“星途尽毁的绝望”与“彻底摆脱束缚”交织的疯魔情绪在他脸上扭曲呈现。角色表演完后，镜头再次迅速左摇到导演近景，镜头不要切镜，导演说到“你亲姐向媒体透露，你是领养的”，导演说完后，镜头再次迅速右摇到小鲜肉近景。镜头不要切镜，镜头内，关系户小鲜肉面部朝向画面左侧斜前方画外导演方向，只见他双眼暴睁，眼球凸出，精心修剪的眉毛高高扬起，嘴巴震惊地张成“O”形。紧接着，他的嘴角再次无法克制地向上拉扯，露出一副不可思议、惊魂未定却的复杂神态。 角色表演完后，镜头再次快速左摇到导演近景，镜头不要切镜，紧接着导演露出有点惊讶的表情说到“其实你是千亿豪门真少爷”。导演说完，镜头再次随即迅速右摇到小鲜肉近景，镜头不要切镜，镜头内，关系户小鲜肉面部朝向画面左侧斜前方画外导演方向，他瞬间爆发出极度魔性的狂喜。他整个人激动得微微颤抖，双眼笑得眯成了一条缝，双手甚至抬起至胸前，双手小幅度快速连续鼓掌，身体前倾摇晃，将一夜暴富、无法自持的癫狂喜悦演绎得淋漓尽致。 角色表演完后，镜头再次快速左摇到导演近景，镜头不要切镜，导演说到“你姐卷款跑路”导演说完，镜头再次迅速右摇到小鲜肉近景。小鲜肉面部朝向画面左侧斜前方画外导演方向，只见他的双眼再次瞪大，瞳孔颤抖，嘴角向下耷拉，神情在一秒钟之内从天堂坠入地狱，写满了惊愕、痛苦与不知所措。画面最后定格在这个表情上。

#### Python SDK

**重要**请先更新 DashScope Python SDK 至 **1.26.2.1** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(
    api_key=api_key,
    model='wan3.0-video',
    prompt='20秒超宽银幕毛绒宇宙冒险片段，整体采用超精细毛绒材质、电影级太空尺度、可爱外形与强烈动作反差、夸张FPV运镜和真实软体物理。一艘由毛绒布、纽扣、拉链与填充棉制成的宇宙飞船，载着兔子、狐狸和乌鸦三只小型毛绒动物，在由巨大毛线行星、绒毛星云和布偶巨兽组成的宇宙中高速逃亡。一只覆盖深蓝长绒毛、眼睛像两枚玻璃纽扣的巨大星际鲸兽从星云中追赶飞船。动态包括拉链飞船弹射起航、贴着毛线行星高速绕行、巨鲸从后方冲出、穿越纽扣小行星带、被鲸兽吞入体内、沿金色拉链从背部逃出、巨鲸如泄掉填充棉般缓慢变扁、最终穿越粉紫色绒毛星云向彩色纽扣太阳飞去。',
    resolution="480P",
    ratio="adaptive",
    duration=20,
    prompt_extend=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请先更新 DashScope Java SDK 至 **2.22.31** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Text2Video {

    static {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan3.0-video")
                        .prompt("20秒超宽银幕毛绒宇宙冒险片段，整体采用超精细毛绒材质、电影级太空尺度、可爱外形与强烈动作反差、夸张FPV运镜和真实软体物理。一艘由毛绒布、纽扣、拉链与填充棉制成的宇宙飞船，载着兔子、狐狸和乌鸦三只小型毛绒动物，在由巨大毛线行星、绒毛星云和布偶巨兽组成的宇宙中高速逃亡。")
                        .resolution("480P")
                        .ratio("adaptive")
                        .duration(20)
                        .promptExtend(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e) {
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "20秒超宽银幕毛绒宇宙冒险片段，整体采用超精细毛绒材质、电影级太空尺度、可爱外形与强烈动作反差、夸张FPV运镜和真实软体物理。一艘由毛绒布、纽扣、拉链与填充棉制成的宇宙飞船，载着兔子、狐狸和乌鸦三只小型毛绒动物，在由巨大毛线行星、绒毛星云和布偶巨兽组成的宇宙中高速逃亡。一只覆盖深蓝长绒毛、眼睛像两枚玻璃纽扣的巨大星际鲸兽从星云中追赶飞船。动态包括拉链飞船弹射起航、贴着毛线行星高速绕行、巨鲸从后方冲出、穿越纽扣小行星带、被鲸兽吞入体内、沿金色拉链从背部逃出、巨鲸如泄掉填充棉般缓慢变扁、最终穿越粉紫色绒毛星云向彩色纽扣太阳飞去。"
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 20,
        "prompt_extend": true
    }
}'
```
**步骤2：根据任务ID获取结果**
```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 图生视频（首帧/首尾帧）

通过 `first_frame`/`last_frame` 严格指定视频首帧或尾帧图像，像素级还原参考画面。适用于需要精准控制起止画面的场景。

-   首帧生视频：传入一张图片作为视频第一帧，模型生成后续运动。
-   首尾帧生视频：同时指定第一帧和最后一帧，模型自动生成中间过渡运动。
-   支持有声视频输出，提示词中可指定台词和音效。

**参数配置**：`ratio` 建议设为 `adaptive`（自动匹配输入图片宽高比），`duration`\=2~30秒或-1。

**能力**

**输入提示词**

**输入首帧或尾帧**

**输出视频**

首帧生视频

(0:00 - 0:03) 运镜：中景。画面：沿用 图片1 的水墨竹林场景。头戴斗笠、身着墨色长袍的刀客，其剪影伫立在浓雾环绕、竹影婆娑的中心。动作：刀客左手轻按刀柄，竹叶随风飘落。氛围：寂静，压抑，水墨晕染的颗粒感清晰可见。

> 完整提示词见表格下方折叠框。

![dbdaddafe0e1a8af2bcd975f61010426](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097154.png)

首尾帧生视频

【一镜到底，慢速唯美运镜，无剪辑，15秒长镜头，岩彩画矿物颜料质感与3D渲染碰撞，青蓝×鎏金撞色】

> 完整提示词见表格下方折叠框。

首帧

![Wan\_Image\_first\_frame](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097225.png)

尾帧

![Wan\_Image\_last\_frame](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097158.png)

提示词：首帧生视频

(0:00 - 0:03) 运镜：中景。画面：沿用 图片1 的水墨竹林场景。头戴斗笠、身着墨色长袍的刀客，其剪影伫立在浓雾环绕、竹影婆娑的中心。动作：刀客左手轻按刀柄，竹叶随风飘落。氛围：寂静，压抑，水墨晕染的颗粒感清晰可见。

(0:03 - 0:08) 剧情引入，运镜：特写。剧情：刀客察觉杀气。画面：镜头快速推进到刀客斗笠下的特写。细节：斗笠边缘露出一双凌厉、决绝的眼睛，眼神如刀。水墨晕染的“汗珠”从额头滑落。动作：刀客右手缓缓握紧刀柄，指关节泛白。竹叶飘落的速度加快。

(0:08 - 0:13) 运镜：快速环绕。画面：镜头以刀客为中心快速环绕。剧情：两名同样是水墨剪影的刺客从竹林深处杀出，手持双钩和短刃。细节：刺客的动作也是水墨笔触构成的，如墨迹流动。镜头快速掠过刺客的身影，强调速度感。

(0:13 - 0:18) 运镜：手持感，高速捕捉。打斗：刀客猛然拔刀，刀光是一道纯白色的水墨裂痕。刺客双钩攻来。细节：一击：刀客回身一斩，刀刃与刺客双钩碰撞，迸发出无数黑白相间、带有书法感的火花和墨点。二击：刀客虚晃一枪，利用竹竿弹射，从高处劈下。刺客翻滚躲避。竹竿被打断，化作飞散的墨痕。三击：刀客刀尖直指另一刺客咽喉，刺客以短刃格挡，镜头捕捉刀刃与短刃摩擦时细微的墨迹崩裂细节。

(0:18 - 0:20) 运镜：慢镜头至定格。\* **画面：** 刀客的刀停在刺客颈侧，刺客凝固。\* **细节：** 刀客的斗笠在打斗中略微倾斜。竹林归于平静，更多竹叶飞舞。\* **氛围：** 镜头慢慢拉远，回到中景，定格在刀客收刀、刺客倒地的画面。\* **文字（可选）：** 画面下方显现水墨风文字：“江湖，不过一笔勾销。”**风格说明：** 整个过程保持 `图片1` 的高度黑白、水墨画风格，动作必须有毛笔触感，速度要快，细节要足（墨滴、火花、墨痕裂口）。

提示词：首尾帧生视频

【一镜到底，慢速唯美运镜，无剪辑，15秒长镜头，岩彩画矿物颜料质感与3D渲染碰撞，青蓝×鎏金撞色】

全局设定：国风岩彩画质感，矿物颜料颗粒肌理，金箔质感，青蓝与鎏金强烈撞色。场景为清晨薄雾中的西湖：湖面呈哑光青蓝晕染，金色晨光穿透云层形成丁达尔光柱，远处三潭印月的石塔与雷峰塔在雾中若隐若现，近处有荷叶与荷花。画面主体是西湖水神"西子"：岩彩画质感，鹅蛋脸，柳叶眉，丹凤眼，眉心一点朱砂花钿，肌肤如羊脂白玉泛着柔光，头后悬浮一轮淡金色圆光；高挽发髻插一支鎏金荷花发簪，她的裙摆与披帛由流动的湖水构成，青蓝色渐变，表面水光粼粼。

配音与音效：背景为轻柔的古筝与竹笛，环境音有细微的水波声与清晨鸟鸣。第8秒起，一位空灵温柔的女声缓慢吟诵："欲把西湖比西子——"；回眸段接下半句："淡妆浓抹，总相宜。"语速缓慢，带轻微回响，余韵悠长。

\[0-3秒：一滴水\]极近微距，清晨的荷叶边缘，一颗水珠凝聚饱满，映着金色晨光，缓缓坠落。镜头跟随水珠下摇（Tilt down），水珠滴入湖中，激起一圈金蓝色涟漪，涟漪层层扩散。

\[3-7秒：水聚成形\]涟漪中心，湖水缓缓隆起，凝聚成神女"西子"的身形：湖水化作她的青蓝色裙摆与半透明披帛，细小水流在她周身环绕流动。她从湖心缓缓升起，双眸轻闭又缓缓睁开，鎏金荷花簪亮起微光。镜头缓慢环绕（Orbit）她半垂的眼眸与流水织成的裙摆。

\[7-11秒：一步一莲\]她赤足踏在湖面上缓缓前行，每一步脚下都漾开一圈金色涟漪，涟漪中荷花次第绽放。镜头后撤拉远成中全景：薄雾散开，远处三潭印月的三座石塔亮起温暖灯光，雷峰塔在晨光中显现，岸边垂柳拂水。第8秒，女声旁白起："欲把西湖比西子——"她的披帛在身后拖出长长的金蓝色水光。

\[11-15秒：回眸·总相宜\]她停下脚步，回眸看向镜头，镜头缓缓推近至半身特写：晨光洒在她的脸上，湖水披帛在身侧轻轻飘动，几滴发光的水珠从发梢滴落，在空中化作细碎光点。旁白接下半句："淡妆浓抹，总相宜。"她浅浅微笑，身后是晨光中的雷峰塔与朦胧的三潭印月。最后一秒画面完全定格在她的回眸特写，定格为完美的电影海报构图。

#### Python SDK

**重要**请先更新 DashScope Python SDK 至 **1.26.2.1** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(
    api_key=api_key,
    model='wan3.0-video',
    prompt='一只猫在草地上奔跑',
    media=[{"type": "first_frame", "url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"}],
    resolution="720P",
    ratio="adaptive",
    duration=5,
    prompt_extend=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请先更新 DashScope Java SDK 至 **2.22.31** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class FirstFrame2Video {

    static {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<>();
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://cdn.translate.alibaba.com/r/wanx-demo-1.png")
                    .type("first_frame")
                    .build());
        
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan3.0-video")
                        .prompt("一只猫在草地上奔跑")
                        .media(media)
                        .resolution("720P")
                        .ratio("adaptive")
                        .duration(5)
                        .promptExtend(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e) {
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "media": [
            {
                "type": "first_frame",
                "url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```
**步骤2：根据任务ID获取结果**
```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 全模态参考生视频

最多传入20个参考素材（图片、视频、音频、文档、网页），模型自动理解参考意图生成视频。在提示词中使用"图片1"或"图1""视频1""音频1"等指代 `input.media` 数组中对应顺序的素材。

**说明****素材指代规则**：图片、视频和音频**分别计数**。`input.media` 数组中第1个 `reference_image` 对应提示词中的"图1"或"图片1"，第2个对应"图2"或"图片2"；第1个 `reference_video` 对应"视频1"，第2个对应"视频2"；第1个 `reference_audio` 对应"音频1"，第2个对应"音频2"，以此类推。三者互不冲突，可同时存在"图1""视频1""音频1"。

-   **角色/物品参考**：传入角色或物品图片，保持外观一致性生成视频。
-   **运镜/动作参考**：传入参考视频，复刻其运镜方式或动作编排。
-   **风格参考**：传入风格参考图，将其美学风格应用到生成视频中。
-   **音频参考**：传入音乐或语音，生成与节拍/语调同步的舞蹈、口型动画。
-   **文档/网页生视频**：传入文档或公开网页链接，自动解析内容生成视频。

**参数配置**：`ratio` 建议设为 `adaptive`（自适应参考素材），`duration`\=2~30秒或-1。

##### 1\. 参考图片/视频/音频

**能力**

**输入提示词**

**输入参考素材**

**输出视频**

参考图片

使用唇釉产品图1 ，生成模特试色视频，15秒，竖屏，突出唇色效果

![5eecdaf48460cde5fbbc2c464cec524f5d9972026d69774e75b8339e1c4c24831b75b38faadcd24bec177c308ebd5304ec45867da4df4d505ff298ada22ab8bc3b4fc6aa4c1faca825e838ced1f82ac8f6990daa07af56984fb4c8ed7016461c](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097165.png)

参考图片+视频+音频

将图片 图像1 的男性角色无缝替换至 视频1 的女生。角色坐在窗边，手持手机贴耳说话。

【音色与台词】提取 音频1 中的音色特征，并让角色说出以下台词：“真的吗？听起来很棒！你什么时候回来啊。我好想你啊.”

【口型与神态】生成的语音需精准驱动角色的口型自然开合。说话时伴随自然的眨眼、轻微的头部点动和呼吸感，面部微表情需与台词中的关怀、回忆情绪完美契合。

【光影与场景】人物面部需自然接收室内暖光与窗外霓虹冷光的混合照明。背景窗外雨滴持续缓慢滑落，桌上咖啡有轻微热气升腾，人物与场景边缘融合自然，无抠图痕迹。

【镜头与画质】15秒长镜头，镜头极缓慢向前推进，画面极度稳定，电影级光影，8K分辨率，照片级真实感。

参考图片

![c647161f46b757a2bc7ace26bab49d5e](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097184.png)

参考视频

参考音频

#### Python SDK

**重要**请先更新 DashScope Python SDK 至 **1.26.2.1** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(
    api_key=api_key,
    model='wan3.0-video',
    prompt='视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道："今天的阳光真好。"图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道："真好听，能不能再唱一遍"。',
    media=[
        {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"},
        {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"},
        {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"},
        {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"},
        {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"}
    ],
    resolution="720P",
    ratio="adaptive",
    duration=5,
    prompt_extend=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请先更新 DashScope Java SDK 至 **2.22.31** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class Reference2Video {

    static {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<>();
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg")
                    .type("reference_image")
                    .build());
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4")
                    .type("reference_video")
                    .build());
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png")
                    .type("reference_image")
                    .build());
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png")
                    .type("reference_image")
                    .build());
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png")
                    .type("reference_image")
                    .build());
        
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan3.0-video")
                        .prompt("视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：\"今天的阳光真好。\"图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：\"真好听，能不能再唱一遍\"。")
                        .media(media)
                        .resolution("720P")
                        .ratio("adaptive")
                        .duration(5)
                        .promptExtend(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e) {
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：\"今天的阳光真好。\"图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：\"真好听，能不能再唱一遍\"。",
        "media": [
            {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"},
            {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"},
            {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"},
            {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"},
            {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"}
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```
**步骤2：根据任务ID获取结果**
```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### 2\. 参考文件或网页

**能力**

**输入提示词**

**输入素材**

**输出视频**

参考文件-基于PPT生视频

一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。

> 完整提示词见表格下方折叠框。

[glass.pptx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260825/msmbpl/glass.pptx)

参考文件-基于Excel生视频

总时长22秒，4个片段顺序拼接。全片纯白底，柔色色块与简洁线条图表，Apple Keynote式极简商务风格，无衬线深灰字体。

> 完整提示词见表格下方折叠框。

[H1-2026跨境电商月度GMV.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260825/lepucv/H1-2026%E8%B7%A8%E5%A2%83%E7%94%B5%E5%95%86%E6%9C%88%E5%BA%A6GMV.xlsx)

参考网页

根据该王维的百科介绍，我要给一年级的孩子们做一个“谁是王维”的动画视频

`[https://baike.baidu.com/item/%E7%8E%8B%E7%BB%B4/37558](https://baike.baidu.com/item/%E7%8E%8B%E7%BB%B4/37558)`

提示词：参考文件-基于PPT生视频

一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。

提示词：参考文件-基于Excel生视频

总时长22秒，4个片段顺序拼接。全片纯白底，柔色色块与简洁线条图表，Apple Keynote式极简商务风格，无衬线深灰字体。BGM（必须有，贯穿全片，音量清晰可闻）：一段轻快的商务背景音乐，节奏稳定、旋律简洁，从第一秒开始就有音乐，全程不间断，旁白出现时音乐不消失、音量略低于人声。音效层：色块滑入时'嗖'的whoosh声、数字跳动时轻键盘'咔嗒'声、关键数据弹出时清脆的'叮'一声bell。旁白：英文男声或女声，明快自信，语速约2.5词/秒，像在季度会上做presentation的语气——专业但不冰冷，有节奏感，关键数字处微微加重。

H1-2026跨境电商月度GMV.xlsx

片段1：全景，中心构图，纯白底，柔光，极简商务风格，视觉参考参考图1的干净白底+柔和色块。纯白画面从中央展开，无数金色光粒子从画面四周向中心汇聚聚拢，粒子碰撞闪烁后凝结成标题文字'H1 2026 · Wan'，文字表面泛着流动的数据流光效，边缘有微光粒子持续环绕飘散，整体炫酷而高级。停留片刻后标题化作粒子流散消失，下方同时滑入两组大号深灰数字——左侧是第7行B7单元格的值$1,580（1月GMV）、右侧是G7单元格的值$3,460（6月GMV），中间一个浅灰色箭头连接，箭头下方浮出浅灰小字'Monthly GMV Growth'。底部弹出一枚珊瑚色圆角标签，显示第8行H8单元格的值+45.7%（H1整体增幅），弹出时伴随清脆的'叮'一声。旁白明快自信地说道：'In the first half of 2026, monthly GMV grew from 15.8 to 34.6 million dollars.' BGM从画面第一秒起就清晰响起，轻快节奏贯穿，色块滑入时带轻微的'嗖'whoosh声。片段末尾色块向两侧平滑滑开，露出下一段画面。

片段2：全景，左侧Y轴+底部X轴构图，纯白底+浅灰点状网格，柔光，极简商务风格，视觉参考参考图2的趋势线图风格。画面底部X轴从左到右依次清晰标注六个月份标签：Jan、Feb、Mar、Apr、May、Jun，等距排列，浅灰色无衬线字体。左侧Y轴标注数值刻度。画面从左向右同时绘制三条趋势线——珊瑚色代表东南亚（数据取自第4行：B4=$580, C4=$640, D4=$750, E4=$880, F4=$1,050, G4=$1,280）、青蓝色代表北美（第5行：B5=$420, C5=$480, D5=$560, E5=$680, F5=$860, G5=$1,260）、琥珀色代表欧洲（第6行：B6=$580, C6=$610, D6=$680, E6=$750, F6=$830, G6=$920），三条线从Jan同一位置出发，随节奏向右上方延伸至Jun。线条下方各带30%透明度渐变填充。每个月份节点到达时，数据点轻弹一下，正上方浮出该点的精确数值标签——标签只显示美元数值，不显示百分比、不显示其他文字，数值必须与上述单元格完全一致。右上角滑出图例：三个色块配市场英文名。六个点全部到达后画面定格片刻。旁白节奏稳定地说道：'All three markets — Southeast Asia, North America, and Europe — showed consistent month-over-month growth, with no single dip.' BGM持续可闻，数字弹出时伴随细碎的'咔嗒'键盘音。6月终点标签放大填满画面后缩小重组，过渡至下一段。

片段3：全景，左60%柱状图+右40%数据列构图，纯白底，柔光，极简商务风格，视觉参考参考图1的柱状图风格。白底上从左到右依次升起6根青蓝色圆角柱体，分别对应1月至6月——必须完整展示6根柱子，柱体高度严格对应第5行North America各月数值：B5=$420, C5=$480, D5=$560, E5=$680, F5=$860, G5=$1,260，从低到高递增排列，呈现明显的逐月增长趋势。每根柱体升起时带轻微的'嗖'弹性音效，柱顶浮出对应的精确美元数值标签。柱体全部就位后，右侧纵向排列滑出5个北美逐月环比增长率，分别由相邻两月数值计算得出：Feb +14.3%（C5相对B5）、Mar +16.7%（D5相对C5）、Apr +21.4%（E5相对D5）、May +26.5%（F5相对E5）、Jun +46.5%（G5相对F5）。每个增长率显示为：翠绿色向上箭头图标 + 百分比数值（如↑+14.3%），整体呈阶梯状从上到下依次排列，绿色箭头强调增长态势，字体略大确保清晰可读。每个数字滑入时带一声细碎的'咔嗒'。最后，北美整体增幅用珊瑚色大号字体从中央弹出：+200%（由G5=$1,260相对B5=$420计算），伴随清脆的'叮'一声bell，停留片刻，数字周围散发轻微光晕。旁白在关键数据处微微加重语气：'North America was our growth engine — up two hundred percent in just six months, accelerating every single month.' BGM持续清晰，节奏逐渐推向高点。整体增幅数字居中放大，周围元素柔和淡出，过渡至尾段。

片段4：全景，中心构图偏上，纯白底，柔光，极简商务风格，视觉参考参考图3的环形图风格。白底中央浮现一个简约环形图（甜甜圈图），只有三段弧形，分别用珊瑚色、青蓝色、琥珀色渲染三个市场的H1占比——东南亚占比由H4=5180计算、北美由H5=4260计算、欧洲由H6=4370计算，三者总和H7=13810。三段弧形之间用白色间隙分隔，环形图整体干净简洁，图表上没有任何百分比符号、没有任何数字标注、没有任何散落的标签，只有纯粹的三段色弧。环形图以约10°/s的速度缓缓旋转。环形图正中央显示一个大号深灰数字，该数字从0快速跳动至H7单元格的值$138.1M（即13810万美元），跳动时伴随连续的细碎'咔嗒'声，最终数字落定时一声清脆的'叮'。下方淡入一行浅灰副标题'Three Markets · All Growing · Zero Downturn'。旁白沉稳收尾，说完留1秒静音：'138 million in total — all markets growing, zero downturns.' BGM持续可闻，最后缓缓衰减，1秒静音后全片结束。

#### Python SDK

**重要**请先更新 DashScope Python SDK 至 **1.26.2.1** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(
    api_key=api_key,
    model='wan3.0-video',
    prompt='一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。',
    media=[
        {"type": "file", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx"}
    ],
    resolution="480P",
    ratio="adaptive",
    duration=10,
    prompt_extend=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请先更新 DashScope Java SDK 至 **2.22.31** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class File2Video {

    static {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<>();
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx")
                    .type("file")
                    .build());
        
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan3.0-video")
                        .prompt("一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调。")
                        .media(media)
                        .resolution("480P")
                        .ratio("adaptive")
                        .duration(10)
                        .promptExtend(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e) {
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。",
        "media": [
            {
                "type": "file",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx"
            }
        ]
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 10,
        "prompt_extend": true
    }
}'
```
**步骤2：根据任务ID获取结果**
```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 视频编辑

传入参考视频，通过自然语言指令对视频进行精准编辑，未指定修改的部分保持不变。

-   **增加元素**：在视频指定位置添加新物体或角色。
-   **删除元素**：移除视频中的物体或角色，自动填充背景。
-   **修改元素**：替换角色外观、服装、年龄等属性。
-   **风格/光线编辑**：转换整体画面风格（如粘土、水墨）或调整光线。
-   **台词编辑**：修改视频中人物的台词内容。
-   **参考编辑**：传入参考图片，将其中的元素添加到视频中。

**参数配置**：`ratio` 建议设为 `adaptive`，`duration` 建议设为 `-1`（自动保持原视频宽高比和时长）。提示词中需包含编辑意图关键词（如"编辑视频""去掉""替换""改成"等）。

**能力**

**输入提示词**

**输入参考视频**

**输出视频**

修改风格

将整个画面转换为黏土风格

台词编辑

编辑视频，将视频中男生的台词改为：“The deal is done.Now... we disappear."

参考编辑

编辑视频，视频1中的女人戴上 图片1 中的帽子，自然贴合头型。 视频1 中的男人戴上中 图片2 的帽子，自然贴合头型，男人的赭棕色衬衫换成 图片3 中的蓝色水洗宽松牛仔衬衫，翻领敞开、袖子卷至前臂。两人的动作、服装和画面其余部分保持不变。

参考视频

参考图片（3张）

![straw\_hat](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097268.png)![baseball\_cap](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097267.png)![jeans\_shirt](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1509667871/p1097269.png)

#### Python SDK

**重要**请先更新 DashScope Python SDK 至 **1.26.2.1** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(
    api_key=api_key,
    model='wan3.0-video',
    prompt='将整个画面转换为黏土风格',
    media=[
        {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"}
    ],
    resolution="720P",
    duration=-1,
    prompt_extend=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请先更新 DashScope Java SDK 至 **2.22.31** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class VideoEdit {

    static {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<>();
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4")
                    .type("reference_video")
                    .build());
        
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan3.0-video")
                        .prompt("将整个画面转换为黏土风格")
                        .media(media)
                        .resolution("720P")
                        .duration(-1)
                        .promptExtend(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e) {
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "将整个画面转换为黏土风格",
        "media": [
            {
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "duration": -1,
        "prompt_extend": true
    }
}'
```
**步骤2：根据任务ID获取结果**
```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 视频延长

对已有视频进行时长延长，支持向前、向后或双向延长。画面风格和角色保持连贯，提示词描述延长部分的动态变化。

-   **向后延长**：以视频最后一帧为起点继续生成后续内容。
-   **向前延长**：以视频第一帧为终点生成前序内容。
-   **双向延长**：以视频为中间段，同时向前和向后延长。

**参数配置**：`ratio` 建议设为 `adaptive`（保持原视频宽高比）。提示词中需包含延长意图关键词（如"延长""延续""向前/向后延长"等）。

-   `duration` 建议设为 `-1`（模型根据输入内容自动推荐合适时长），或指定生成视频的时长，即输入视频时长 + 预期延长的时长总和。如原始视频5秒、预期向后延长2秒，`duration` 可设为 `-1` 或 `7`。
-   需注意输入时长 + 输出时长总计≤30秒。

**能力**

**输入提示词**

**输入参考视频**

**输出视频**

向后延长

面包师端上刷好的面包，将刷子放到一旁，镜头跟随面包师，去斜后方的烤炉进行烤制，面包师关上烤炉门，他站在烤炉旁边，看着正在烤炉里的面包，闻了闻面包的香气，说："so good"。

向前延长

将视频1向前延长15s。角色A为穿黑色燕尾服、白色衬衫、黑色领结及米色马甲的深棕色短发男性，角色B为穿米色泡泡袖复古长裙、裙身带黑色蕾丝花边、佩戴深色水滴耳环的棕色盘发女性。

> 完整提示词见表格下方折叠框。

向前向后延长

以视频为中间段向前续写两秒：镜头平滑跟随，女孩向镜头缓缓走来，停下脚步，温柔地微微抬头，在冷空气中深吸一口气，嘴唇微张；以视频为中间段向后续写三秒：女孩搓完手，直视镜头，绽放出温暖灿烂的笑容。她缓缓抬起一只戴着手套的手，去接一片轻轻飘落的雪花，镜头缓慢后拉成中远景，展现阳光雪林小路，黄金时刻逆光，镜头光晕，浅景深，温暖治愈氛围。

提示词：向前延长

将视频1向前延长15s。角色A为穿黑色燕尾服、白色衬衫、黑色领结及米色马甲的深棕色短发男性，角色B为穿米色泡泡袖复古长裙、裙身带黑色蕾丝花边、佩戴深色水滴耳环的棕色盘发女性。舞厅内水晶吊灯光芒映照大理石地面，宾客们三两交谈持杯低语，一段悠扬的华尔兹弦乐前奏缓缓响起，人群的谈话声逐渐安静。角色B从舞厅一侧缓步走来，裙摆轻拂过大理石地面，目光环顾四周。角色A从人群中走出，穿过宾客径直来到角色B面前，微微欠身伸出右手，目光温柔注视着她。角色B垂眸浅笑，将右手轻轻搭上角色A的掌心，两人相视一笑，角色A引领角色B步入舞池中央，周围宾客自然后退让出空间，目光齐聚二人。角色A左手握住角色B右手举起，右手轻扶她的腰后，两人摆好华尔兹舞姿，随弦乐正拍踏出第一步，开始旋转。19世纪宫廷舞会的典雅氛围，暖金色调。

#### Python SDK

**重要**请先更新 DashScope Python SDK 至 **1.26.2.1** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(
    api_key=api_key,
    model='wan3.0-video',
    prompt='将视频1向后延长，面包师端上刷好的面包，将刷子放到一旁，镜头跟随面包师，去斜后方的烤炉进行烤制',
    media=[
        {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/rptnhd/wan2.7-i2v-video-continuation-2.mp4"}
    ],
    resolution="720P",
    ratio="adaptive",
    duration=5,
    prompt_extend=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请先更新 DashScope Java SDK 至 **2.22.31** 或以上版本，再运行以下代码。更新方法请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class VideoExtend {

    static {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<>();
        media.add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/rptnhd/wan2.7-i2v-video-continuation-2.mp4")
                    .type("reference_video")
                    .build());
        
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan3.0-video")
                        .prompt("将视频1向后延长，面包师端上刷好的面包，将刷子放到一旁，镜头跟随面包师，去斜后方的烤炉进行烤制")
                        .media(media)
                        .resolution("720P")
                        .ratio("adaptive")
                        .duration(5)
                        .promptExtend(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e) {
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "将视频1向后延长，面包师端上刷好的面包，将刷子放到一旁，镜头跟随面包师，去斜后方的烤炉进行烤制",
        "media": [
            {
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/rptnhd/wan2.7-i2v-video-continuation-2.mp4"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```
**步骤2：根据任务ID获取结果**
```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 输入素材

`input.media` 数组中每个元素包含 `type` 和 `url` 两个字段。支持的 type 及限制如下：

**type**

**说明**

**限制**

`first_frame`

首帧图像，严格作为视频第一帧

最多1张

`last_frame`

尾帧图像，严格作为视频最后一帧

最多1张

`reference_image`

参考图像

最多10张

`reference_video`

参考视频

最多5段，总时长不超过15秒

`reference_audio`

参考音频

最多5段，总时长不超过15秒

`file`

文件（docx、doc、xlsx、xls、pptx、ppt、pdf、txt、md）

最多1个，不可与 link 同时输入

`link`

网页链接（公开网页）

最多1个，不可与 file 同时输入

**重要**`reference_xx`/`file`/`link` 类型和 `first_frame`/`last_frame` 类型互斥，不能在同一请求中混用。

## 输出视频

-   **分辨率**：480P、720P、1080P（默认）。
-   **宽高比**：16:9、4:3、1:1、3:4、9:16、adaptive（默认，自适应输入素材）。
-   **时长**：2~30秒；-1（智能时长，默认5秒）。有视频输入时，输入+输出总时长≤30秒。
-   **格式**：MP4，帧率30fps。
-   **有声视频**：默认开启，可通过 `audio`\=false 关闭。
-   视频URL有效期24小时，请及时保存。

## 计费与限流

-   计费详情请参见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。
-   限流详情请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## API文档

[万相3.0-视频生成 API参考](raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
