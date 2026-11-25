# Vidu视频生成Prompt指南

本文涵盖从提示词公式、关键词词典到进阶案例的完整实践方法。

<a id="初阶教程"></a>

<a id="h2-basic"></a>

## 初阶教程

<a id="提示词公式"></a>

<a id="h3-prompt-structure"></a>

### 提示词公式

**主体/场景+场景描述+环境描述+艺术风格/媒介**

-   调整句式和语序，避免主体物过多/复杂、主体物分散的句式。
-   避免模糊的术语，表述尽可能准确。
-   使用流畅准确的口语化措辞，避免过度文学化的叙述。
-   丰富、准确和完整的描述才能生成符合特定艺术风格和需求的视频。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073369.png)

<a id="效果示例"></a>

<a id="h4-prompt-examples"></a>

#### 效果示例

提示词遵循**"主体/场景+场景描述+环境描述+艺术风格/媒介"**的基本结构，可提升视频生成效果。在不同位置重复和强化关键风格描述，有助于提高输出风格的一致性和画面丰富度。

以"柯基犬游泳"为例，扩写后的提示词重点在于营造视频整体温馨纯真的电影视觉效果。

> 扩写后的提示词分析：先定主体+场景+动作，再叠光影/色调/质感与镜头感，用温柔、柔和、优雅、宁静等同向氛围词在句首、景物、收束等处各点一次，避免同词机械重复；整体指向温馨、纯真、电影感。

|  |  |
| --- | --- |
| **提示词**：一只柯基幼犬在大泳池里游泳 | **扩写后的提示词（遵循提示词公式）：**捕捉柯基犬宝宝在阳光照耀下的大泳池中优雅游泳的宁静时刻。水下的视角展现了小狗温柔的笑容，柔和的金色灯光穿过水面，在池底形成光影的舞动。场景以柔和的粉色为主色调，烘托出梦幻般的空灵氛围。高分辨率的摄影作品捕捉到了水的纹理和柯基犬欢快表情的每一个精致细节，创造出一幅简单而又充满电影感的宁静和纯真的肖像。这种简约而富有情感的设置传达出一种平静和幸福的感觉，是宁静而具有视觉吸引力的电影镜头的理想选择。 |

<a id="提示词词典"></a>

<a id="h3-prompt-dict"></a>

### 提示词词典

特定提示词可触发 Vidu 的生成效果变化，如 prompt 带有"大动态"时视频运动幅度更大。

<table><thead><tr><th><strong>维度大类</strong></th><th><strong>维度细分</strong></th><th><strong>适用模型</strong></th><th><strong>触发关键词</strong></th></tr></thead><tbody><tr><td rowspan="3"><strong>主体动态</strong></td><td rowspan="3"><p>动态控制</p></td><td rowspan="3"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>大动态：大动态、快速运动、超大动效</p></td></tr><tr><td><p>中动态：中等动态、一般动效</p></td></tr><tr><td><p>小动态：小幅动态、小动态</p></td></tr><tr><td rowspan="25"><strong>运镜控制</strong></td><td rowspan="7"><p>基础运镜</p></td><td rowspan="7"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>左移：镜头向左移动、镜头move left、左移镜头、镜头track left等</p></td></tr><tr><td><p>右移：镜头向右移动、镜头move right、右移镜头、镜头track right等</p></td></tr><tr><td><p>升：镜头向上移动、镜头move up、升镜头等</p></td></tr><tr><td><p>降：镜头向下移动、镜头move down、降镜头等</p></td></tr><tr><td><p>推：镜头推进、镜头zoom in、推镜头等</p></td></tr><tr><td><p>拉：镜头拉远、镜头zoom out、拉镜头等</p></td></tr><tr><td><p>固定：镜头固定、Static shot、固定镜头等</p></td></tr><tr><td rowspan="4"><p>特殊拍摄手法</p></td><td rowspan="4"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>延时：延时摄影、Time Lapse shot</p></td></tr><tr><td><p>微距：微距镜头、Macro shot</p></td></tr><tr><td><p>第一人称：第一人称视角、FPV shot</p></td></tr><tr><td><p>航拍：航拍镜头、Aerial shot</p></td></tr><tr><td rowspan="5"><p>景别</p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073385.png" alt="image"></td><td rowspan="5"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>远景</p></td></tr><tr><td><p>全景</p></td></tr><tr><td><p>中景</p></td></tr><tr><td><p>近景</p></td></tr><tr><td><p>特写</p></td></tr><tr><td rowspan="4"><p>视角</p></td><td rowspan="4"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>低角度</p></td></tr><tr><td><p>高角度</p></td></tr><tr><td><p>平视镜头</p></td></tr><tr><td><p>鸟瞰镜头</p></td></tr><tr><td rowspan="5"><p>构图</p></td><td rowspan="5"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>对角线构图</p></td></tr><tr><td><p>三分构图</p></td></tr><tr><td><p>对称构图</p></td></tr><tr><td><p>越肩：越肩镜头、Over shoulder shot</p></td></tr><tr><td><p>荷兰角：荷兰角镜头、Dutch angle</p></td></tr><tr><td rowspan="17"><strong>视频风格</strong></td><td rowspan="7"><p>画面风格</p></td><td rowspan="7"><p>文生视频<br>参考生视频</p></td><td><p>2D动漫：2D动漫风格、2D anime style</p></td></tr><tr><td><p>3D渲染：3D Rendering style、3D cg style</p></td></tr><tr><td><p>写实：Realistic</p></td></tr><tr><td><p>水墨：水墨风格、Ink Wash Painting style</p></td></tr><tr><td><p>线稿：线稿风格、Line Art style</p></td></tr><tr><td><p>像素：像素风格、Pixel Art style</p></td></tr><tr><td><p>油画：油画风格、Oil Painting style</p></td></tr><tr><td rowspan="10"><p>导演风格</p><blockquote><p>仅适合动漫</p></blockquote></td><td rowspan="10"><p>文生视频</p></td><td><p>宫崎骏风格</p></td></tr><tr><td><p>新海诚风格</p></td></tr><tr><td><p>大友克洋风格</p></td></tr><tr><td><p>细田守风格</p></td></tr><tr><td><p>宮崎吾朗风格</p></td></tr><tr><td><p>汤浅政明风格</p></td></tr><tr><td><p>牛岛新一郎风格</p></td></tr><tr><td><p>山田尚子风格</p></td></tr><tr><td><p>石立太一风格</p></td></tr><tr><td><p>高畑勋风格、米林宏昌风格</p></td></tr><tr><td rowspan="7"><strong>特效</strong></td><td rowspan="7"><p>特效</p></td><td rowspan="7"><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>爆炸：爆炸特效、Explodes</p></td></tr><tr><td><p>旋涡：旋涡特效、Vortex</p></td></tr><tr><td><p>粉碎：粉碎特效、Shatters</p></td></tr><tr><td><p>扭曲：扭曲特效、Warps</p></td></tr><tr><td><p>融化：融化特效、Melt</p></td></tr><tr><td><p>消失：变成气泡消失了、变成雪花消失了等</p></td></tr><tr><td><p>石化：变成石头</p></td></tr><tr><td><strong>氛围</strong></td><td><p>氛围</p></td><td><p>文生视频<br>图生视频<br>参考生视频</p></td><td><p>快乐：明亮色彩</p><p>悲伤：冷色调</p><p>宁静：柔和色调</p><p>紧张：阴暗的光线</p><p>温馨浪漫：暖色调、柔和光线</p></td></tr></tbody></table>

<a id="提示词调优"></a>

<a id="h3-prompt-optimize"></a>

### 提示词调优

首次编写的提示词效果往往不够理想，发现缺陷后针对性修改提示词是必要的优化步骤。

<a id="图生视频"></a>

<a id="a0182bdfd31x9"></a>

#### 图生视频

**调优分析：**原始提示词有一定概率视觉上看起来火车是倒着开的。优化后通过主体跟背景的大小比例关系来营造运动的方向。

<table><thead><tr><th><strong>预期效果</strong></th><th><strong>输入图片</strong></th><th><strong>原始提示词</strong></th><th><strong>原始视频效果</strong></th><th><strong>调优后提示词</strong></th><th><strong>调优后视频效果</strong></th></tr></thead><tbody><tr><td><p>火车向前开</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073386.png" alt="image.png"></td><td><p>火车向前运动起来</p></td><td></td><td><p><strong># 主题</strong> 火车运动起来，车头被逐步放大，烟囱不断冒出，松树逐渐变小。</p><strong># 要求：</strong><ol><li>相机运动：向右跟随</li></ol></td><td></td></tr></tbody></table>

<a id="参考生视频"></a>

<a id="4dcfd974d445l"></a>

#### 参考生视频

**调优分析：**原始提示词走路效果不自然，可能与镜头固定有关。优化后增加镜头控制（镜头拉远），配合镜头运动后人物动作更自然。如需适配各种输入图片，可按上文方式继续调整。

**原始提示词示例：**

<table><thead><tr><th><strong>预期效果</strong></th><th><strong>输入图片</strong></th><th><strong>提示词和输出效果</strong></th></tr></thead><tbody><tr><td><p>森系动态写真-单人</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073393.png" alt="image"></td><td><p><strong>原始提示词：</strong>女子面向镜头轻盈向前走，步伐坚定而优雅。林间小道上，阳光透过斑驳的树影洒落在她肩头，微风拂过，裙摆轻轻摆动，透着自在与从容，落叶随步伐轻轻翻飞。</p><strong>调优后提示词</strong><p><strong># 主题</strong> 女子面向镜头轻盈向前走，步伐坚定而优雅。林间小道上，阳光透过斑驳的树影洒落在她肩头，微风拂过，裙摆轻轻摆动，透着自在与从容，落叶随步伐轻轻翻飞。</p><strong># 要求</strong><ol><li>相机运动：镜头拉远</li></ol></td></tr></tbody></table>

<a id="进阶教程"></a>

<a id="h2-advanced"></a>

## 进阶教程

<a id="参考生视频-保持主体一致性"></a>

<a id="h3-subject-consistency"></a>

### 参考生视频：保持主体一致性

Vidu 能保证角色和物体在多视角下的一致性，适用于复杂造型角色、人物面部表情和多主体交互等场景。

<a id="示例1-复杂主体的精准控制"></a>

<a id="h4-consist-eg1"></a>

#### 示例1：复杂主体的精准控制

造型复杂的3D动画角色，无论视角如何变化，Vidu始终确保头型、服饰的全角度细节一致。

|  |
| --- |
|  |

<a id="示例2-人物面部特征和动态表情的自然一致"></a>

<a id="h4-consist-eg2"></a>

#### 示例2：人物面部特征和动态表情的自然一致

人物特写镜头中，Vidu流畅保持面部特征和表情的连贯性，避免面部僵硬或失真。

|  |
| --- |
|  |

<a id="示例3-多主体一致性"></a>

<a id="h4-consist-eg3"></a>

#### 示例3：多主体一致性

Vidu支持上传多个主体图像（人物、道具、环境等），在视频生成中实现元素交互。例如上传主体、客体和环境的图片，可创建定制角色在定制空间内自由动作的场景。

此外，Vidu支持融合不同主体特征，例如将角色A正面与角色B反面无缝融合，创造全新角色或物体。

|  |  |
| --- | --- |
|  |  |

<a id="ai漫剧提示词案例"></a>

<a id="h3-manga-practice"></a>

### AI漫剧提示词案例

提示词编写原则与初阶教程一致（避免主体过多/复杂、避免模糊术语、使用口语化措辞、保持描述丰富准确完整）。

**漫剧提示词结构**：

-   **Part1. 风格/景别/机位/构图/运镜（可按需选填）**
    
    **风格**：二维漫画、真人写实、3D动漫、韩漫、洛丽塔、乙游、游戏原画、中世纪、古风、武侠、卡通、绘本、盲盒手办、赛博朋克、科技、金属机械、黑暗恐怖等
    
    **景别**：远景、全景、中景、近景、特写、大特写
    
    **机位**：轴线左侧/右侧、低角度、高角度、仰视、俯视、平视、鸟瞰、无人机等
    
    **构图**：三分、水平线、中心、荷兰角等
    
    **运镜**：固定、上/下/左/右移动、左上/左下/右上/右下移动、推进、摇镜、拉远、顺时针/逆时针环绕、旋转，可叠加组合（如"推进+顺时针旋转"）
    
-   **Part2. 画面描述**
    
    简单自然语言描述动作/画面/特效
    
-   **Part3. 图片强调**
    
    图1为\[场景\]；图2为\[角色xx\]；图3为\[道具xx\]
    

<a id="提示词案例"></a>

<a id="c4c58de0f55cq"></a>

#### 提示词案例

| 提示词 | 输入图参考 | 输出效果 |
| --- | --- | --- |
| 二维动漫风，中景，动作定格，镜头静止；水平线构图，轴线右侧机位，小蓝小红小明三人在图1桃花谷中漫步，她们正笑着，突然笑容凝固在脸上。图1为\[场景\]；图2为角色\[小蓝\]；图3为角色\[小红\]；图4为角色\[小明\]。 | 图1-4依次为：<br><br>![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073406.png)![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073407.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073411.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073412.png) |  |
| 2D二次元动漫风格，从下往上运镜，不拍到脸部，先特写拍摄脚步走出来，然后慢慢运镜到胸口，但是不露脸；固定机位，画面1中，巨大的光照射，慢慢显现出邪恶老人的真实模样，老人缓缓走出来，浑身散发诡异邪恶的能量。图1为\[可怕诡异震撼的环境\]；图2：\[邪恶老人\]。 | 图1-2依次为：<br><br>![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073413.png)![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073418.png) |  |
| 三维动漫风，特写近景，平视视角，轴线左侧机位，三分构图，萧非身体被漩涡卷的飞起，萧非的手死死抓住一块从地面凸起的岩壁，萧非在狂风中艰难地回头，对着身后大吼，表情狰狞，嘴巴不停说话，镜头剧烈晃动。图1为场景；图2为角色\[萧非\]。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073616.png) |  |

<a id="图像输入示例"></a>

<a id="6a04af34c897m"></a>

#### 图像输入示例

<table><thead><tr><th><p><strong>图片输入</strong></p></th><th><p><strong>示例</strong></p></th></tr></thead><tbody><tr><td><p><strong>角色</strong></p><ul><li><p>特写+三视图</p></li><li><p>同一个视频最好保证输入角色风格近似</p></li></ul></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073407.png" alt="image.png"></p><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073644.png" alt="image"></p></td></tr><tr><td><p><strong>环境</strong></p><ul><li><p>和角色风格统一</p></li><li><p>不要远景（短剧中很少用到，尤其竖屏场景中）</p></li><li><p>场景画面中尽量不要出现人物</p></li><li><p>多做中景/近景</p></li></ul></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073406.png" alt="image.png"></p><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073413.png" alt="image.png"></p></td></tr><tr><td><p><strong>道具</strong></p><ul><li><p>清晰物体</p></li><li><p>提示词中定义其外观、风格与使用方式</p></li></ul></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073619.png" alt="image.png"><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073620.png" alt="image.png"></p><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073641.png" alt="image"></p><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073642.png" alt="image"></p></td></tr><tr><td><p><strong>特效</strong></p><ul><li><p>描述在什么情况下会出现什么外观的特效</p></li></ul></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073624.png" alt="image"></p><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8822188771/p1073625.png" alt="image"></p></td></tr></tbody></table>
