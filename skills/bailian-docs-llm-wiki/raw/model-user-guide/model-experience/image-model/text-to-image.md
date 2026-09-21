# 文本生成图像

通过文生图API，您可以基于文本描述创造出全新的图像。阿里云百炼提供万相（Wan）、千问（Qwen-Image）和z-image系列模型。

**在线体验**：[北京](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate?modelId=qwen-image)｜[新加坡](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate)

**在线体验**提供无需编程的网页版文生图功能，在页面中输入文本描述即可直接生成图像：

-   **体验中心**：点击上方的在线体验链接（**北京**、**新加坡**）进入，可选择模型、设置输出分辨率、开启**智能改写**后直接提交生成。
-   通义万相独立站：访问[通义万相](https://tongyi.aliyun.com/wan)，在**图像生成**中直接体验。

如需在自有应用中集成文生图能力，请使用下方的 API 调用方式。

## 模型效果

#### 千问（Qwen-image）

**复杂布局**

![c13672c7-6e05-9aeb-8d2c-8c4b66af5861\_qwen\_image3\_serving\_output\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5369106871/p1093777.png)

**长段落**

![e03efee1-35b1-9109-a988-e3977add0fac\_qwen\_image3\_serving\_output\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0469106871/p1093781.png)

**写实人像**

![2beecb7f-c3c3-9c10-9458-04325512bb8a\_qwen\_image3\_serving\_output\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5369106871/p1093776.png)

**UI设计**

![image (92)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5369106871/p1093142.png)

**PPT**

![image (90)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5369106871/p1093139.png)

**插画设计**

![e38cc145-78f6-92a7-9bdb-141be17dba04\_qwen\_image3\_serving\_output\_0](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5369106871/p1093779.png)

点击查看提示词

**复杂布局**：

```
这是一张横向展开的电商店铺招牌信息图，整体采用 16:9 的宽屏比例，完美适配电脑端与平板端的店铺首页顶部展示。画面整体背景采用高饱和度的墨西哥传统色彩体系，以明黄、赤红、孔雀蓝、翠绿为主色调，色彩之间通过柔和的水彩晕染效果自然过渡，背景纸张带有轻微的手绘水彩纹理与细腻的颗粒质感，营造出一种温暖、热情且充满异域风情的视觉氛围。画面最顶部和最底部边缘，装饰着传统的墨西哥剪纸（Papel Picado）镂空图案，这些剪纸图案由连续的菱形、三角形与波浪形组合而成，以明黄、赤红、翠绿、紫色交替排列，呈现出随风飘动的轻盈姿态，镂空部分透出背景的深邃星空蓝，增加了画面的层次感与呼吸感。顶部剪纸下方与底部剪纸上方，各有一条连续的阿兹特克几何图腾边框，由连续的阶梯状折线与菱形图案组成，采用纯白色与暗金色线条勾勒，为整个店招奠定了浓厚的墨西哥文化底蕴与复古手工艺基调。画面四角点缀着立体的彩色陶罐与微型仙人掌盆栽，陶罐表面绘制着经典的蓝白相间塔拉韦拉（Talavera）花纹，釉面带有高光反射，仙人掌则呈现出饱满的翠绿色，带有细微的刺状纹理，这些角落元素起到了平衡画面重心、丰富视觉细节的作用。

画面左侧三分之一区域为品牌主视觉与核心标识区，视觉中心是一个巨大的立体字“TodoTi”。字体设计巧妙融入了墨西哥自然元素，字母“T”的顶部延伸出两片翠绿的仙人掌叶片，叶片表面带有清晰的脉络纹理；字母“o”内部填充着赤红与明黄相间的太阳放射状光芒，光芒由十六条等距的直线构成；字母“d”的圆弧部分带有塔拉韦拉陶瓷的蓝白花纹，绘制着三朵牡丹与缠绕的藤蔓；字母“i”的点被替换为一颗立体的红色小番茄，表面带有白色的高光点。整个“TodoTi”字体采用粗犷的黑色描边，内部填充高饱和度的渐变色，并带有轻微的立体投影效果，使其在背景中跃然而出。在店名正下方，是一行醒目的品牌Slogan，文字内容为“TodoTi
你的色彩生活馆”，字体采用圆润可爱的无衬线粗体，颜色为纯白色，带有轻微的红色外发光效果，文字排版居中对齐，字间距适中，确保在远距离观看时依然清晰易读。Slogan下方是一行较小的副标题，文字内容为“源自墨西哥的热情
点亮每一个日常”，字体采用优雅的手写体风格，颜色为明黄色，排版同样居中，行距紧凑，与上方的Slogan形成良好的视觉层级。在文字后方的背景中，隐约浮现出一幅巨大的墨西哥太阳历（阿兹特克日历）半圆形浮雕，浮雕采用暗金色与古铜色渐变，表面刻有精细的几何纹路与人面图腾，人面图腾的眼睛呈菱形，嘴巴呈矩形，散发着柔和的金色光芒，为品牌标识提供了深厚的文化背景与视觉支撑。左侧边缘还垂直排列着三个小型的圆形徽章，分别写着“精选
好物”、“源头
直采”、“用心
服务”，徽章底色为孔雀蓝，文字为白色，边缘带有白色的虚线缝线效果，增强了手工质感。

画面中左部是核心插画与商品展示区，占据画面约四分之一的宽度。这里绘制了一幅充满墨西哥风情的生活场景插画。画面中心是一个戴着宽边草帽（Sombrero）、穿着彩色刺绣披风（Poncho）的卡通骷髅女孩（Catrina）。她的面部妆容精致，眼窝处画着黑色的心形图案，边缘带有白色的虚线装饰，脸颊点缀着红色的玫瑰花纹，花瓣层层叠叠，嘴角带着温暖甜美的微笑。她头上戴着巨大的明黄色宽边草帽，草帽边缘装饰着红绿相间的编织流苏，流苏长度约为五厘米；身上披着赤红与孔雀蓝交织的披风，披风上绣着繁复的阿兹特克几何图腾与盛开的万寿菊图案，万寿菊的花瓣呈放射状排列。她正微笑着推着一辆复古的木制手推车，手推车的轮子由彩色的马赛克瓷砖拼贴而成，瓷砖颜色包括蓝、白、黄、绿，充满艺术气息。手推车里装满了丰富且具体的日常用品，每一件商品都清晰可见并配有详细的标签。最前方是一个彩色的塔拉韦拉陶瓷马克杯，杯身绘制着蓝白相间的牡丹与藤蔓花纹，牡丹花瓣共有十二层，旁边漂浮着标签，文字为“塔拉韦拉陶瓷杯
耐高温 釉下彩
容量 350ml”。杯子后方是一个手工编织的收纳筐，筐体由天然剑麻编织而成，纹理呈人字形走向，带有两个皮革提手，标签文字为“手工编织收纳筐
天然剑麻 结实耐用
尺寸 30x20x15cm”。收纳筐上方放置着一个仙人掌形状的香薰蜡烛，蜡烛主体为翠绿色，表面带有细微的凸起纹理，顶部有一簇白色的火苗，火苗边缘带有淡黄色光晕，标签文字为“仙人掌香薰蜡烛
植物精油 助眠安神
燃烧时间 约40小时”。手推车的最里层堆放着几个色彩斑斓的抱枕，抱枕套采用棉麻材质，印着太阳神图腾与彩色条纹，四角带有长度约三厘米的流苏，标签文字为“墨西哥风情抱枕
棉麻材质 可拆洗
尺寸 45x45cm”。插画背景是一片阳光明媚的沙漠绿洲，远处有几棵高低错落的真实仙人掌，天空中飘浮着几朵洁白的云彩，整体光影采用温暖的侧逆光，为插画中的每一个元素镀上了一层宽度约两毫米的金色轮廓光，使画面充满生机与活力。

画面中右部是商品分类导航区，采用四个色彩鲜艳的圆角矩形卡片，呈 2x2 网格排列，每个卡片代表一个日常用品分类，卡片之间保持着均匀且明确的间距，确保信息布局充实有序。左上角的卡片底色为赤红色，表面带有轻微的纸张纹理，圆角半径为十五像素，顶部标题为“家居布艺”，字体为白色粗体，下方配有一个彩色编织挂毯的扁平化图标，挂毯底部带有长度约两厘米的流苏。卡片正文分为两行，文字内容为“地毯 抱枕 桌布 窗帘
采用优质棉麻，色彩鲜艳，
为家增添墨西哥热情。”，文字颜色为纯白色，排版左对齐，行距设定为 1.5 倍。右上角的卡片底色为孔雀蓝，顶部标题为“餐厨用具”，字体为白色粗体，下方配有一个塔拉韦拉陶瓷盘的图标，盘子边缘绘制着连续的波浪纹。正文文字为“碗碟 杯具 餐具 收纳
手工陶瓷质感，让每一餐
都充满异域风情。”，文字颜色为明黄色，形成鲜明的色彩对比。左下角的卡片底色为明黄色，顶部标题为“卫浴洗护”，字体为深棕色粗体，下方配有一个仙人掌形状的肥皂盒图标，肥皂盒表面带有三根短刺。正文文字为“浴巾 皂盒 牙刷杯 置物架
防水防潮材质，打造清爽
舒适的洗浴空间。”，文字颜色为深棕色，确保在亮色背景上的高可读性。右下角的卡片底色为翠绿色，顶部标题为“生活杂货”，字体为白色粗体，下方配有一个彩色风车图标，风车四个叶片分别为红、黄、蓝、绿四色。正文文字为“衣架 挂钩 纸巾盒 垃圾桶
实用与美观并存，细节之处
彰显生活品味。”，文字颜色为纯白色。这四个分类卡片提供了清晰的商品导航，其本身的设计也高度契合墨西哥色彩美学，图标与文字的搭配直观且富有吸引力。

画面右侧是促销与活动信息区，视觉主体是一个巨大的墨西哥吉他（Mariachi）形状的边框。吉他琴身采用温暖的原木色，表面绘制着精致的红色与金色雕花，雕花图案为缠绕的藤蔓与盛开的玫瑰，琴颈向上延伸，琴弦采用银白色线条绘制，闪烁着金属光泽。吉他琴身内部是核心的促销信息区域。顶部有一条横跨琴身的红色丝带横幅，上面写着“TodoTi
新店开业
狂欢季”，文字为白色粗体，带有轻微的立体阴影。横幅下方是巨大的促销数字，文字内容为“全场满 199
减 50”，数字“199”和“50”采用明黄色与赤红色交替的超大号立体字，极具视觉冲击力，文字“全场满”和“减”采用白色中号字体，排版紧凑且对齐。数字下方是一行较小的优惠说明，文字为“新人首单立减 20 元
包邮到家”，字体为白色手写体，显得亲切自然。吉他琴身底部排列着三个圆形的小徽章，分别写着“7天
随心
退换”、“极速
发货”、“正品
保障”，徽章底色为深蓝色，文字为白色，边缘带有宽度为一像素的金色细线描边。吉他琴颈部分延伸出几条彩色的丝带，丝带呈波浪状飘动，上面写着“活动时间
即日起至
本月底”，文字为深棕色，排版顺着丝带的弧度微微倾斜，增加了画面的动感与趣味性。

画面底部是一条横向的品牌故事与文化区，占据画面下方约四分之一的空间。背景是深蓝色的夜空，点缀着大小不一的白色星星，星星呈五角星形状，边缘带有微弱的发光效果，天空中还分布着黑色的仙人掌剪影，剪影轮廓清晰，营造出一种静谧而深邃的氛围，与上方鲜艳热烈的色彩形成完美的视觉平衡。左侧是一个醒目的标题块，文字为“关于
TodoTi”，字体为白色粗体，带有明黄色的外发光效果，排版垂直居中。标题右侧的内容分为三个等宽的列，每列都有独立的小标题和正文。第一列小标题为“设计理念”，字体为明黄色粗体，底部带有一条长度约五厘米的白色下划线，正文文字为“TodoTi 汲取墨西哥传统手工艺的色彩与灵感，
将阿兹特克图腾、塔拉韦拉陶瓷纹理与现代家居
实用主义完美结合，让日常用品成为家中的艺术品。”，文字为浅灰白色，排版左对齐，行距设定为 1.5 倍，确保长段落的阅读体验。第二列小标题为“品质承诺”，字体为明黄色粗体，底部同样带有白色下划线，正文文字为“我们严选全球优质供应商，每一件商品都经过
严格的质量检测。从材质挑选到工艺打磨，
只为给您提供安全、耐用、环保的生活好物。”，文字同样为浅灰白色，排版与第一列保持一致。第三列小标题为“生活哲学”，字体为明黄色粗体，底部带有白色下划线，正文文字为“生活需要丰富的色彩，TodoTi 倡导用色彩点亮日常。
像墨西哥人一样热爱生活、享受当下，让每一次
触摸、使用，都能感受到阳光般的温暖与热情。”，文字为浅灰白色。这三列文字内容详实，从设计、品质到理念，全方位展示了店铺的品牌内涵，配合底部的星空背景，整个店招兼具商业促销功能与品牌文化传播的深度。

在最底部的边缘，紧贴着阿兹特克几何图腾边框的上方，是一条细长的互动与引导区。背景为半透明的纯白色，带有轻微的毛玻璃模糊效果，使其与上方的深蓝色夜空背景自然融合。
获取更多家居灵感
官方认证 TodoTiOfficial，文字为深棕色，排版紧凑，图标与文字对齐，清晰明了。中间是一个模拟搜索框的设计，框体为白色圆角矩形，带有浅灰色的内阴影，内部左侧有一个放大镜图标，放大镜镜片为圆形，手柄向右下方倾斜四十五度，右侧写着“搜索
日常好物
开启色彩生活”，文字为赤红色，模拟用户输入的状态，引导顾客进行商品搜索。右侧是客服联系引导，配有一个耳麦形状的图标，耳麦线条圆润，文字为“有任何问题
随时联系我们
客服热线 400-888-TODO
在线时间 9:00-22:00”，文字为深棕色，排版与左侧对称。整个底部引导区信息明确，功能性强，为顾客提供了便捷的互动入口。
```

**超长段落**：

```
Vertical Western European 19th-century illustrated poetry page, Romantic maritime farewell theme, international English visual tradition, not an East Asian painting. The composition is a vertical art print or vintage book page with aged ivory paper, fine engraved linework, muted blue-gray watercolor washes, and elegant negative space. The main feature is a long English poem rendered clearly in elegant English copperplate-inspired calligraphy, highly legible, English alphabet only, standard left-to-right reading order, top-to-bottom layout, correct punctuation, exact line breaks, natural ink pressure, dark sepia-black lettering, subtle vintage letterpress texture, refined international typography.

Below and around the text, illustrate a cold twilight seashore: gray stones beside the sea, a small boat floating near the shore, distant ships moving toward a haven under low hills, pale evening mist over the water, faint moonlight, soft ripples, a lonely coastal atmosphere, melancholic but restrained. The mood is poetic, timeless, and elegant, like a Victorian English maritime lyric. No Chinese characters, no Chinese painting style, no seals, no stamps, no modern objects, no illegible glyphs, no random letters.

Render exactly the following 12 lines from Alfred, Lord Tennyson's public-domain poem “Break, Break, Break”; do not render the title or author name:

Break, break, break,
On thy cold gray stones, O Sea!
And I would that my tongue could utter
The thoughts that arise in me.
O well for the fisherman's boy,
That he shouts with his sister at play!
O well for the sailor lad,
That he sings in his boat on the bay!
And the stately ships go on
To their haven under the hill;
But O for the touch of a vanish'd hand,
And the sound of a voice that is still.

High resolution, masterful long-form English text rendering, poetic, elegant, museum-quality Western illustrated book page.
```

**写实人像**：

```
帮我生成一张生活化美食男生人像写真，呈现实拍电影质感。画面主体是一位24岁左右的年轻男生，五官清爽干净，眉眼温和，皮肤自然清透，保留真实的肤质细节。他穿着质地柔软的米白色粗棒针织毛衣，内搭纯白T恤微微露出领口，展现出温暖、精致且松弛的生活气息。人物坐在温馨的西餐厅餐桌前，身体微微前倾，右手握着银质刀叉正在轻轻切开盘中的惠灵顿牛排，左手自然轻扶着桌面边缘。他微微侧头看向镜头，嘴角带着若有似无的松弛浅笑，眼神温柔且带有生活感。木质桌面上摆满了精致的西餐餐食，旁边有装着琥珀色饮品的复古高脚杯和一小瓶淡雅的复古插花。人物身后是通透的玻璃墙面，上面印有浅金色的法文手写体菜单“Menu du Jour”，文字以丝印工艺自然贴合在玻璃表面，并带有轻微的环境反光。环境采用暖黄色室内顶光，光线柔和地洒在人物面部和桌面食物上，食物表面泛着诱人的高光，背景玻璃透出室外微弱的冷色环境光，形成电影感十足的冷暖光影对比。采用近距离平视取景，机位略带侧前方的呼吸感，避免死板居中，小景深让背景的玻璃墙面和餐厅环境轻微虚化，形成温暖的散景光斑，前景的插花和饮品边缘也带有自然的虚化过渡，整体色调温暖治愈，充满浓郁的生活氛围与美食诱惑。
```

**UI设计**：

```
这张图片是一款沉浸式亚洲雨林声音探索体验网站的宽屏电脑端界面设计，整体氛围暗沉静谧，设计灵感源自老式野外录音设备与模拟科学仪器。整体配色以深邃祖母绿、浓郁黑曜石黑与柔和大地棕为主，营造出安宁沉静的氛围。界面搭载细微水汽与薄雾特效，柔和斑驳的光影折射效果模拟阳光穿透茂密树冠的景象，背景融入纸张细纹、叶脉等自然肌理。整体画面写实度极高，风格对标英国广播公司高端自然纪实纪录片，构图富有电影质感，渲染细节极致精细。
页面最顶端横贯一整条极简半透明导航栏。最左侧为品牌标识，由精致线条绘制的老式模拟麦克风与龟背竹叶交织而成，搭配柔和米奶油色优雅衬线字体文字“RAINFOREST ARCHIVE”。导航栏右侧是导航菜单，包含四个极简文字链接，字体与颜色和品牌名保持一致：“Expeditions”、“Species”、“Field Notes”、“About”。
页面上三分之二区域为主视觉横幅板块。背景是一张画质超清、氛围感浓郁的古老亚洲龙脑香科雨林实景图，林间萦绕着轻柔绵延的薄雾；前景虚化的深绿色蕨类枝叶形成自然暗角。横幅板块左侧叠加主标题，采用大号高对比度精致衬线字体，文字为“Voices of the
Canopy”。标题正下方是字号更小、质感雅致的副标题，浅米奶油色，内容为“An auditory journey through the ancient
dipterocarp forests of Southeast Asia.”。文字带有轻微打字机质感，字符排布存在细微自然错落，强化复古模拟设备的复古氛围。
横幅板块中下位置是核心音频交互组件：一台复刻老式野外模拟录音机的精密播放器，原型为经典纳格拉或马兰茨磁带机。播放器机身采用拉丝深枪灰色金属材质，带有细微自然划痕与使用磨损痕迹；配有两个大型滚花金属旋钮，旋钮上印有小巧清晰的无衬线刻印文字“GAIN”与“MONITOR”。设备中央是经典音量表，内置温润柔和的琥珀色背光，表内指针轻靠零刻度位置。音量表右侧设有重型实体拨动开关，拨至上方代表“PLAY”播放状态。音频播放时，音量表向外缓缓扩散出同心波纹特效，形似轻柔水纹或细微声波，采用半透明雾绿色调，与薄雾背景自然融合。
横幅板块下方，页面布局切换为简约纪实风网格，用作声音素材库区域。板块顶部配有精致小型标题，全大写字母加宽字距排版，文字为“CURRENT EXPEDITIONS”。标题下方采用规整双栏网格，陈列四张风格各异的声景卡片。
左上第一张卡片：背景是氛围感暗沉的薄雾河岸缩略图，标题文字“Dawn Chorus in Danum Valley”，下方标注信息“Location: Sabah, Borneo”、“Duration: 42:15”，卡片右侧配有一枚小巧琥珀色标识，标注“Currently Playing”。
右上第二张卡片：画面为湿润宽大绿叶特写，标题文字“Monsoon Rain on Broadleaves”，标注信息“Location: Khao Yai, Thailand”、“Duration: 1:15:30”，附带细线条边框按钮，文字“Listen”。
左下第三张卡片：画面是黄昏时分森林树冠朦胧剪影，标题文字“Nocturnal Gibbon Calls”，标注信息“Location: Khao Sok, Thailand”、“Duration: 58:02”，附带细线条边框按钮，文字“Listen”。
右下第四张卡片：画面为树皮纹理微距特写，标题文字“Hornbill Wingbeats”，标注信息“Location: Taman Negara, Malaysia”、“Duration: 24:40”，附带细线条边框按钮，文字“Listen”。
声景网格最右侧，纵向贯穿该下半区域的竖版面板，设计复刻老式野外科学记录本内页。纸张带有柔和复古米黄肌理，页面右下角留有淡咖啡渍痕迹。面板标题采用打字机等宽字体，文字“FIELD NOTES”；正文墨水色调雅致、微微褪色，内容为：
“Recorded using
parabolic microphones
and Nagra IV-S
tape recorders.
Humidity: 94%
Temp: 24°C”
文字旁配有深棕乌墨手绘精致猪笼草植物速写。
页面最底端是极简页脚，整页宽度贯通，上方设有一条细深绿色分隔线。页脚左侧文字“Copyright 2024 Rainforest Archive”，右侧文字“Funded by the Wildlife Conservation Society”，两处文字均采用柔和低调的精致小号衬线字体。
```
**PPT制作：**
```
这是一张宽高比为 16:9 的专业教育类 PPT 幻灯片，整体背景采用极淡的蓝灰色柔和渐变，叠加有极低透明度的正弦波暗纹与微弱的网格点阵纹理，营造出严谨的物理学术氛围与科技感。画面顶部居中位置是主标题区域，文字为巨大的深藏青色无衬线粗体“AC Circuit Anaysis: Resistor with Sinusoidal Voltage”，标题下方紧贴一条明亮的橙色细横线作为视觉分割，横线两端带有微小的圆形端点装饰，增强版式的仪式感。画面主体分为左右两列，采用严谨的栅格对齐系统，左右两列宽度比例约为 1:1.2，确保右侧复杂的公式计算拥有充足的展示空间。左侧列顶部是一个圆角矩形橙色标题栏，内部居中显示白色加粗文字“PROBLEM DATA & WAVEFORM”，标题栏底部带有轻微的投影，使其具有浮起的立体质感。橙色标题栏下方是一个浅灰白色的圆角数据卡片，卡片边缘有极细的浅蓝色边框，内部垂直排列四个数据要点，每个要点左侧配有纯灰色的极简线性图标，依次为电阻符号、波浪线、电压箭头和时钟符号。四个要点的文字采用深灰色清晰字体，依次为“Resistor (R) = 10 Ω”、“Waveform = Sinusoidal”、“Peak Voltage (V subscript p) = 311 V”、“Period (T) = 0.02 s”，文字排版整齐，行距舒适，关键数字使用稍深的颜色进行视觉强调。数据卡片下方是图表区域，顶部居中显示深灰色图表标题“Voltage vs. Time”。图表主体是一个带有浅灰色网格线的二维坐标系，垂直 Y 轴左侧标有深灰色文字“Voltage (V)”，刻度线旁分别标有白色背景框包裹的深蓝色文字“+311”、“0”和“-311”。水平 X 轴下方标有深灰色文字“Time (s)”，刻度线旁标有“0.01”和“0.02”。坐标系中央绘制了一条平滑、饱满且带有轻微发光效果的鲜红色正弦波曲线，曲线线条粗细适中，展现出完美的周期性。在正弦波的波峰处，有一条深蓝色的垂直双向箭头指示振幅，箭头旁标有深蓝色文字“V subscript p = 311 V”。在 X 轴的一个完整周期上方，有一条深蓝色的水平尺寸标注线，两端带有垂直引出线，中间标有深蓝色文字“T = 0.02 s”。图表区域整体留白充足，视觉焦点集中在红色波形上。右侧列顶部同样是一个圆角矩形橙色标题栏，与左侧标题栏高度对齐，内部居中显示白色加粗文字“SOLUTION STEPS & CALCULATIONS”。橙色标题栏下方垂直排列四个浅蓝色渐变的圆角卡片，卡片之间保持均匀的垂直间距，内部留有充足的呼吸空间。第一个卡片左上角有一个深蓝色的圆形编号徽章，内部显示白色数字“1”。卡片标题为深蓝色加粗文字“1. Maximum Current (I subscript p)”。下方正文分为三行，采用标准数学公式的视觉样式排版，呈现为分数线、上下标和根号的优雅形态，文字内容为深灰色“Formula: Ohm’s Law, I subscript p = V subscript p over R”，接着是计算过程“I subscript p = 311 V over 10 Ω = 31.1 A”。卡片右下角有一个亮黄色底色的圆角高亮框，内部显示加粗的深蓝色文字“I subscript p = 31.1 A”。第二个卡片左上角编号徽章显示“2”，标题为“2. AC Voltmeter Reading (V subscript rms)”。正文包含说明“Voltmeters read RMS value.”，公式“V subscript rms = V subscript p over square root of 2”，以及计算“V subscript rms = 311 V over 1.414 ≈ 220 V”，右下角高亮框显示“V subscript rms ≈ 220 V”。第三个卡片编号徽章显示“3”，标题为“3. Actual Power Dissipated (P subscript avg)”。正文包含“Using RMS values.”，公式“P subscript avg = (V subscript rms) squared over R”，计算过程“P subscript avg = (220 V) squared over 10 Ω = 48400 over 10 W = 4840 W”，右下角高亮框显示“P subscript avg = 4.84 kW”。第四个卡片编号徽章显示“4”，标题为“4. Joule Heat in Half Cycle (Q subscript half)”。正文包含“Energy = Power × Time”，时间计算“Time = T over 2 = 0.01 s”，主计算“Q subscript half = P subscript avg × (0.01 s) = 4840 W × 0.01 s = 48.4 J”，右下角高亮框显示“Q subscript half = 48.4 J”。四个卡片的高亮框统一位于右下角，形成整齐的视觉对齐与阅读动线。画面最底部是一条极细的浅灰色横向分隔线，分隔线下方居中显示浅灰色小号无衬线字体“Experimental Physics - AC Circuits Analysis Module”。页脚区域保持极简，其余背景保持纯图形与留白。整张幻灯片色彩系统以深藏青、亮橙色、浅蓝灰和纯白为主，红色波形与黄色高亮框作为视觉点缀，打破了单调，提升了画面的活力与专业度。所有文字边缘锐利，对比度极高，确保在投影或屏幕上清晰可读。光影处理克制，仅通过卡片底部的微弱投影和标题栏的轻微高光来增强层次感，整体呈现出高度成熟、结构清晰、信息饱满的专业物理教学课件质感。
```
**插画设计：**
```
这幅画作以柔和的米白色水彩纸为底，呈现一幅手绘水彩插图。纸张表面展现出传统植物艺术的特征，包括清晰可见的颜料颗粒和湿画法带来的柔和色彩晕染。画面上方中央区域绘有一簇簇紫罗兰和三色堇。花瓣由淡紫色、深紫色和淡紫色渐变交织而成，花心呈金黄色。花朵旁点缀着一片翠绿色的小叶，以半透明的水彩晕染和精细的叶脉刻画而成。柔和的定向光线照亮画面，突显了水彩纸的质感和颜料的微妙变化。在花卉图案正下方，纸张下半部分水平居中的位置，是“Виолета”字样。该字样以弧形书法体书写，并使用了金属金色墨水。字母造型采用流畅、连续的笔画，并略带浮雕立体感，在光线照射下呈现出柔和的金属光泽。
```

#### 万相

**人像写真**

![p1023408-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0286332671/p1023592.webp)

**写实摄影**

![p1023409-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0286332671/p1023593.webp)

**绘画流派**

![p1023411](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0286332671/p1023615.png)

**文字生成**

![p1023399](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0286332671/p1023596.png)

**海报设计**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2637090871/p1023602.png)

**组图生成**

![p1023424-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0286332671/p1023598.webp)

点击查看提示词

**人像写真**：照片，摄影人像，写实人像：背景是故宫红墙，女子身穿黑色旗袍，手握扇子，长曝光摄影，王家卫电影感，故事感，人来人往，迷离的光线，形成迷离的轨迹，柔焦摄影，眼神深邃神秘，艺术气息十足。

**写实摄影**：写实摄影，一只狐狸在森林中凝视镜头，鱼眼视角带来强烈的透视效果，毛发细节清晰，背景树木呈圆形拉伸，水彩风格，柔和色调。

**绘画流派**：一束野花插在旧陶罐中，背景是乡村厨房，印象派风格，柔和笔触，温暖光线，油画质感

**文字生成：**毛笔水墨画风格，宣纸纹理清晰可见，淡墨晕染出朦胧的客厅轮廓。一位身着素色长裙的东方少女盘坐于虚化边缘的旧式布艺沙发上，侧脸低垂，手持一卷展开的诗稿，窗外竹影婆娑，微风拂动帘栊。画面大量留白，右侧题有小楷诗句“闲坐悲双鬓，幽梦入青烟”，左下角钤朱文印章。墨色浓淡相宜，飞白笔触勾勒出光影流动感，意境空寂深远，似有古琴余音缭绕其间。

**海报设计：**扁平几何插画风格，一张端午节海报，杂志封面，色调与背景：以粉色渐变为主色调，营造出柔和且富有节日氛围的背景，奠定温馨且传统的基调。 文字元素：绿色字体搭配阴影效果，主文案突出"DRAGONBOAT FESTIVAL"与"端午"分两行不分开，正文信息下方"2025/05/31"、"农历五月初五"突出端午数字时间信息"2025/05/31"。 主体图案： 一艘绿色龙身搭配粉色龙鳍的龙船，高饱和色调，色彩对比强烈，高周围点缀祥云元素，船上坐着人物，进一步呼应赛龙舟的场景，增添节日活力。 细节点缀：添加 "中国传统节日" 字样，搭配小型粽子图标，丰富文化细节。高级简约排版方式，大师杰出作品。简约，时尚，大气，新中式传统海报，字体不要有阴影样式。

**组图生成**：四宫格日系Q版漫画，赛璐璐风格。第一格：戴黑框眼镜的程序员面对屏幕弹出的红色报错，瞳孔地震，冷汗飞溅，背景变为裂开的像素深渊。第二格：他撸起袖子敲击键盘，自信挑眉，头顶冒出“这不过是五行代码的事！”对话框。第三格：屏幕布满混乱的报错符号，他头发炸立，眼圈发黑，椅子后仰45度，天花板飘满废弃的流程图。第四格：误删一行灰色注释后，绿色对勾闪现，他歪头呆滞，屏幕上浮起问号气泡：“……所以它只是个幻觉？”

## 模型选型

-   **qwen-image-3.0-pro**：千问图像3.0旗舰版，支持prompt智能改写，擅长文本渲染，能精准生成贴合物理材质的中英文。
-   **wan2.7-image-pro**：功能最全面，支持组图生成和高达4096x4096的分辨率，并增强了五官控制、色彩控制和超长文字渲染能力。
-   **z-image-turbo**：追求速度与性价比。生成速度快、成本低，擅长高逼真度的人像与产品图。

## 使用方式

文生图提供两种使用方式，请按需选择：

**使用方式**

**是否需要编程**

**入口**

**适用场景**

网页版在线体验

否

**体验中心**（见本文开篇的**在线体验**链接）；[通义万相独立站](https://tongyi.aliyun.com/wan)

快速试用模型、验证提示词效果、少量出图

API 调用

是

见下方**快速开始**

在自有应用或服务中批量、自动化地集成文生图能力

## 快速开始

#### 前提条件

在调用前，请[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过DashScope SDK进行调用，还需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

#### 示例代码

**调用方式说明**：

-   千问生图模型（qwen-image-3.0系列、qwen-image-2.0系列）均支持同步调用，其中qwen-image-3.0系列、qwen-image-plus、qwen-image模型支持异步调用，详情请参见[千问-图像生成与编辑3.0](raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)和[千问-文生图](raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)。
-   万相文生图模型均支持异步调用，其中wan2.7-image-pro、wan2.7-image、wan2.6-image、wan2.6-t2i支持同步调用，详情请参见[万相-图像生成与编辑2.7](raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)、[万相-图像生成与编辑2.6](raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)和[万相-文生图V2](raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

#### 千问-同步调用

#### Python

```
import os
import base64
import mimetypes
import dashscope
from dashscope import MultiModalConversation

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-image-3.0-pro",
    messages=[{
        "role": "user",
        "content": [
            {"text": "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。"}
        ]
    }],
    prompt_extend=True
)

print(response)
if response.status_code == 200:
    url = response.output.choices[0].message.content[0]["image"]
    print(f"Generated image URL: {url}")
else:
    print(f"Error: {response.code} - {response.message}")
```

#### Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.utils.Constants;

public class ImageEditExample {
    public static void main(String[] args) {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
            .role(Role.USER.getValue())
            .content(Arrays.asList(
                Collections.singletonMap("text", "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。")
            ))
            .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen-image-3.0-pro")
            .messages(Arrays.asList(userMessage))
            .parameter("prompt_extend", true)
            .build();
        try {
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.utils.Constants;

public class ImageEditExample {
    public static void main(String[] args) {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
            .role(Role.USER.getValue())
            .content(Arrays.asList(
                Collections.singletonMap("text", "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。")
            ))
            .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen-image-3.0-pro")
            .messages(Arrays.asList(userMessage))
            .parameter("prompt_extend", true)
            .build();
        try {
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### curl

##### 请求示例

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-image-3.0-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "prompt_extend": true
    }
}'
```

##### 响应示例

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": [
                        {
                            "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ],
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "output_height": 1024,
        "output_width": 1024,
        "input_image_count": 0,
        "input_image_type": "qima_input_1k",
        "output_image_count": 1,
        "output_image_type": "qima_output_1k"
    },
    "request_id": "571ae02f-5c9d-436c-83c2-f221e6df0xxx"
}
```

#### dashscope CLI

```
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope image-synthesis create -m wanx2.1-t2i-turbo -p "一只可爱的猫" -n 1
```

**重要**SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见

[DashScope SDK Expert](raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

#### 万相-异步调用

#### Python

##### 请求示例

```
import os
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

# 以下为北京地域base_url，各地域的base_url不同
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def main():
    message = Message(
        role="user",
        content=[
            {"text": "一位年轻女性，自然随性的自拍风格，超高清写实人物生活照。她身着黄色碎花长袖上衣，长发自然垂落且略带波浪卷。画面背景为户外自然景色，近处有绿植，远处可见水域和山峦。自然柔和的阳光洒在人物脸上和身上，形成自然的光影效果，拍摄机位为人物手持设备的中景自拍视角，人物身体自然站立，展现出轻松自在的状态。角度自然，随手一拍的快照风格，不经意间的抓拍。"}
        ]
    )

    # 提交异步任务
    print("提交异步任务...")
    response = ImageGeneration.async_call(
        model="wan2.7-image-pro",
        api_key=api_key,
        messages=[message],
        enable_sequential=False,
        n=1,
        size="2K"
    )

    if response.status_code == 200:
        print(f"任务提交成功，任务ID: {response.output.task_id}")

        # 等待任务完成
        status = ImageGeneration.wait(task=response, api_key=api_key)

        if status.output.task_status == "SUCCEEDED":
            print("任务完成!")
            print(f"结果:")
            print(status)
        else:
            print(f"任务失败，状态: {status.output.task_status}")
    else:
        print(f"任务创建失败: {response.code} - {response.message}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
        "task_status": "PENDING"
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0
    }
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "56e318fd-ed60-99e8-8ca1-cdef25ca4xxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-31 23:04:46.166",
        "scheduled_time": "2026-03-31 23:04:46.208",
        "end_time": "2026-03-31 23:05:11.664",
        "finished": true
    },
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "characters": 0,
        "size": "2048*2048",
        "total_tokens": 731,
        "image_count": 1
    }
}
```

#### Java

##### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.Collections;

public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static ImageGenerationResult waitTask(String taskId)
            throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        return imageGeneration.wait(taskId, apiKey);
    }

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "一位年轻女性，自然随性的自拍风格，超高清写实人物生活照。她身着黄色碎花长袖上衣，长发自然垂落且略带波浪卷。画面背景为户外自然景色，近处有绿植，远处可见水域和山峦。自然柔和的阳光洒在人物脸上和身上，形成自然的光影效果，拍摄机位为人物手持设备的中景自拍视角，人物身体自然站立，展现出轻松自在的状态。角度自然，随手一拍的快照风格，不经意间的抓拍。")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .enableSequential(false)
                .n(1)
                .size("2K")
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult taskResult = null;
        try {
            System.out.println("----async call, creating task----");
            taskResult = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("Task created: " + JsonUtils.toJson(taskResult));

        // 等待任务完成
        String taskId = taskResult.getOutput().getTaskId();
        ImageGenerationResult result = waitTask(taskId);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            asyncCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "requestId": "7d026dc1-e8c9-9caa-84ac-e82e2da97xxx",
    "output": {
        "task_id": "2de18c56-c151-4b80-8105-1d164733exxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

```
{
    "requestId": "daea7295-4ce0-928a-9a11-4d2bea058xxx",
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "total_tokens": 731,
        "image_count": 1,
        "size": "2048*2048"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "2de18c56-c151-4b80-8105-1d164733exxx",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-03-31 19:49:53.124",
        "scheduled_time": "2026-03-31 19:49:53.175",
        "end_time": "2026-03-31 19:50:53.160"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

#### curl

**说明**

-   异步调用必须设置 Header 参数`X-DashScope-Async` 为`enable`。
-   异步任务的 `task_id` 查询有效期为 24 小时，过期后任务状态将变为 `UNKNOWN`。
-   适用于所有模型，新手建议使用 [Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)调用API。

##### 步骤1：发起创建任务请求

该请求会返回一个任务ID（`task_id`）。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false,
        "thinking_mode": true
    }
}'
```

##### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，通过接口轮询任务状态，直到 `task_status` 变为 SUCCEEDED 或 FAILED。

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 关键能力

### 1\. 指令遵循（提示词）

参数：`messages.content.text`或`input.prompt`（必选）、`negative_prompt`（可选）。

-   **text \\ prompt（正向提示词）**：描述希望在画面中看到的内容、主体、场景、风格、光照和构图。文生图的核心控制参数。
-   **negative\_prompt（反向提示词）**：描述不希望在画面中出现的内容，如“模糊”、“多余的手指”等。仅用于辅助优化生成质量。
-   **文本渲染（画面中的文字）**：模型可在画面中生成中英文文字，但对长文本（如完整古诗、长段落或多行文字）难以逐字精准还原，易出现错字、漏字或形近字替代。如对画面内文字的准确性有要求，建议尽量缩短画面内文字、仅保留关键标题或短语，或对成图中的关键文字进行后期编辑。

撰写技巧：一个结构化的 Prompt 通常能带来更好的效果，撰写技巧请参见[文生图Prompt指南](raw/model-user-guide/use-cases/text-to-image-prompt.md)。

> wan2.7-image-pro、wan2.7-image不支持`negative_prompt`参数，对于不希望出现的元素，请在正向提示词中描述（不要出现xxx）。

### 2\. 开启prompt智能改写

参数: `parameters.prompt_extend` (bool, **默认为 true**)。

此功能可自动扩展和优化**较短的Prompt**，提升出图效果。开启此功能额外耗时 3-5 秒。此耗时为使用大模型改写文本。

实践建议：

-   建议开启：当输入 Prompt 较简洁或宽泛时，此功能可显著提升图像效果。
-   建议关闭：若需控制画面细节、或已提供详细描述，或对响应延迟敏感。请将参数 `prompt_extend` **显式设为**`false`。

> wan2.7-image-pro、wan2.7-image不支持`prompt_extend`参数，可通过开启`thinking_mode`提升出图质量。

参数: `parameters.prompt_extend_mode` (string，可选，默认为 `direct`)。仅qwen-image-3.0系列支持，用于指定`prompt_extend`开启后的改写方式：

-   `direct`：直接提示词增强（DPE），适用于大多数场景。文生图（T2I）和图生图/图像编辑（I2I）均支持。
-   `agent`：智能体提示词增强（APE），提供更精细的改写效果，仅支持文生图（T2I）。图生图/图像编辑（I2I）场景传入`agent`将返回400错误。

### 3\. 设置输出图像分辨率

参数: parameters.size (string)，格式为 `"宽*高"`。

**模型**

**size格式**

**总像素支持范围**

**默认**

**宽高比**

wan2.7-image-pro

缩写

`1K`（1024\*1024）、`2K`（2048\*2048）、`4K`（4096\*4096）

`2K`（2048\*2048）

1:8 – 8:1

自定义 `"宽*高"`

768\*768 – 4096\*4096

wan2.7-image

缩写

`1K`（1024\*1024）、`2K`（2048\*2048）

`2K`（2048\*2048）

1:8 – 8:1

自定义 `"宽*高"`

768\*768 – 2048\*2048

wan2.6-image（图文混排输出模式）

自定义 `"宽*高"`

768\*768 – 1280\*1280

匹配输入宽高比 (≤1280\*1280)

1:4 – 4:1

wan2.6-t2i, wan2.5-t2i-preview

自定义 `"宽*高"`

1280\*1280 – 1440\*1440

1280\*1280

1:4 – 4:1

wan2.2 及更早的 t2i 模型

自定义 `"宽*高"`

\[512, 1440\]，且总像素 ≤1440\*1440

1024\*1024

\-

qwen-image-3.0 系列

自定义 `"宽*高"`

512\*512 – 2048\*2048

模型自动推荐

1:8 – 8:1

qwen-image-2.0 系列

自定义 `"宽*高"`

512\*512 – 2048\*2048

2048\*2048

\-

qwen-image-max / qwen-image-plus 系列

仅限固定预设尺寸

见下方预设尺寸

1664\*928 (16:9)

\-

> wan2.7-image-pro仅文生图场景（无图片输入、非组图生成）支持4K与自定义4096_4096分辨率，其余场景仅支持2K与2048_2048分辨率。

**qwen-image-max、qwen-image-plus 系列**：仅支持以下 5 种固定的分辨率：

-   `1664*928`（默认值）：16:9
-   `1472*1104`：4:3
-   `1328*1328`：1:1
-   `1104*1472`：3:4
-   `928*1664`：9:16

推荐分辨率：

**宽高比**

**4K (wan2.7-image-pro)**

**2K (wan2.7-image, qwen-image-3.0系列, qwen-image-2.0系列)**

**1K (Wan t2i)**

1:1

4096\*4096

2048\*2048

1280\*1280

16:9

4096\*2304

2688\*1536

1696\*960

9:16

2304\*4096

1536\*2688

960\*1696

4:3

4096\*3072

2368\*1728

1472\*1104

3:4

3072\*4096

1728\*2368

1104\*1472

### 4\. 组图生成

参数：`parameters.enable_sequential`（bool，默认为 false）。仅`wan2.7-image-pro`和`wan2.7-image`支持。

设为`true`时启用组图模式，模型将根据提示词和参考图片的内容一次性生成多张有故事连贯性的图像。

-   **生成数量**：通过`n`参数控制，开启组图模式时，取值范围1~12（默认12），实际数量由模型决定且不超过n。
-   **注意**：开启组图模式时，`thinking_mode`和`color_palette`参数不可用。

### 5\. 思考模式

参数：`parameters.thinking_mode`（bool，**默认为 true**）。仅`wan2.7-image-pro`和`wan2.7-image`支持。

开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。

> 仅在关闭组图模式（`enable_sequential=false`）时可用。

### 6\. 自定义颜色主题

参数：`parameters.color_palette`（array）。仅`wan2.7-image-pro`和`wan2.7-image`支持。

通过传入包含颜色（hex）和占比（ratio）的对象数组，自定义生成图像的颜色方案。需包含3至10种颜色，推荐设置为8种。所有ratio值相加总和必须为100.00%。

> 仅在关闭组图模式（`enable_sequential=false`）时可用。

点击查看输入示例

```
"color_palette": [
    {
        "hex": "#C2D1E6",
        "ratio": "23.51%"
    },
    {
        "hex": "#CDD8E9",
        "ratio": "20.13%"
    },
    {
        "hex": "#B5C8DB",
        "ratio": "15.88%"
    },
    {
        "hex": "#C0B5B4",
        "ratio": "13.27%"
    },
    {
        "hex": "#DAE0EC",
        "ratio": "10.11%"
    },
    {
        "hex": "#636574",
        "ratio": "8.93%"
    },
    {
        "hex": "#CACAD2",
        "ratio": "5.55%"
    },
    {
        "hex": "#CBD4E4",
        "ratio": "2.62%"
    }
]
```

### 7\. 其他通用参数

参数：`parameters.n`（integer，可选，**默认为 1**）。输出图像的数量。qwen-image-3.0 系列支持 1~6 张；`wan2.7-image-pro`、`wan2.7-image` 在关闭组图模式时支持 1~4 张；开启组图模式时表示最大生成图像数量（取值范围 1~12，默认为 12），详见上文“组图生成”。

> n 直接影响费用：费用 = 单价 × 成功生成的图片张数。

参数：`parameters.seed`（integer，可选，取值范围 `[0, 2147483647]`）。随机数种子，未传入时由服务随机选择；使用相同 seed 可使生成结果保持相对稳定。具体支持情况以各模型的 API 参考为准。

参数：`parameters.watermark`（bool，可选，**默认为 false**）。是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

## 应用于生产环境

-   **容错策略**
    -   **处理限流**：当 API 返回 `Throttling` 错误码或 HTTP 429 状态码时，表明已触发限流，限流处理请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    -   **异步任务轮询**：轮询查询异步任务结果时，建议采用合理的轮询策略（如前30秒每3秒一次，之后拉长间隔），避免因过于频繁的请求而触发限流。为任务设置一个最终超时时间（如 2 分钟），超时后标记为失败。
-   **风险防范**
    -   **结果持久化**：API 返回的图片 URL 有 24 小时有效期。生产系统必须在获取 URL 后立即下载图片，并转存至您自己的持久化存储服务中（如阿里云对象存储 OSS）。
    -   **内容安全审核**：所有 `prompt` 和 `negative_prompt` 都会经过内容安全审核。若输入内容不合规，请求将被拦截并返回 `DataInspectionFailed` 错误。
    -   **生成内容的版权与合规风险**：请确保您的提示词内容符合相关法律法规。生成包含品牌商标、名人肖像、受版权保护的 IP 形象等内容可能涉及侵权风险，请您自行评估并承担相应责任。

## API文档

-   [千问-图像生成与编辑3.0](raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
-   [千问 Qwen-Image](raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
-   [万相-图像生成与编辑2.7](raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
-   [万相-图像生成与编辑2.6](raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
-   [万相-文生图V2](raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
-   [文生图Z-Image](raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 常见问题

**Q: 图片 URL 多久会失效？我应该如何永久保存图片？**

A: 图片 URL 的有效期为 24 小时。您必须在获取到 URL 后，立即通过程序下载图片，并将其保存到您自己的持久化存储中，例如本地服务器或阿里云对象存储 OSS。

**Q: 调用API返回DataInspectionFailed错误，如何处理？**

A: 该错误表示输入文本触发了内容安全审核。请检查并修改prompt或negative\_prompt中的文本，移除可能违规的内容后重试。

**Q: prompt\_extend参数应该开启还是关闭？**

A: 当输入的prompt比较简洁或希望模型发挥更多创意时，建议保持开启（默认）。当prompt已经非常详细、专业，或对API响应延迟有严格要求时，建议显式设置为false。

注意：wan2.7-image-pro、wan2.7-image不支持`prompt_extend`参数，可通过开启`thinking_mode`提升出图质量。

**Q:**[体验中心](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate)如何清空会话的内容？

A: 点击控制台右上角**清空当前对话**。
