# 创意海报生成

创意海报生成，您的创意海报魔法工厂！它能够根据您的要求自动生成海报的背景和文字排版，支持多种海报风格。从宣传到祝福，让每一张海报都成为你的个性宣言。无需设计基础，帮助您轻松制作出彩作品，让创意触手可及。

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   wanx-poster-generation-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[文本生成图像](../../../model-experience/image-and-video-generation/image-model/text-to-image.md)获取替代方案。

<a id="基本介绍"></a>

<a id="27f97170c4lr2"></a>

## 基本介绍

<a id="使用场景"></a>

<a id="dd3dfac4a86ro"></a>

### 使用场景

-   **社交媒体与个人创作**：社交媒体用户和内容创作者可以根据自己的使用场景，生成相册或者视频的封面，或者是制作祝福卡片等。借助AI的创造力，帮助提升个人IP品牌形象，快速掌握流量密码。
-   **新品发布会预热宣传**：通过输入产品特点和目标受众的偏好，包含产品的亮点、上市日期以及引人入胜的口号，用于社交媒体、电子邮件营销和线下广告，有效吸引潜在顾客的注意力，激发他们对新产品的兴趣。
-   **节日促销活动推广**：商家可以利用AI创意海报生成工具快速设计出吸引眼球的产品宣传海报，只需输入“圣诞节”、“春节”等关键词，AI就能结合节日元素和品牌风格，创作出充满节日气氛的视觉作品。
-   **艺术文化活动宣传**：只需提供音乐会或艺术展览活动名称、时间、地点和主题色彩等信息，AI就能生成多款风格各异的海报设计供选择，通过独特的视觉效果激发观众的兴趣，增加活动的曝光度和参与度。

<a id="特色优势"></a>

<a id="41888131a3hn2"></a>

### 特色优势

-   百变创意风格：一键生成海报，创意无限，涵盖"剪纸工艺"、"折纸工艺"、"中国水墨"、"中国刺绣"、"真实场景"、"2D卡通"、"儿童水彩"、"赛博背景"等各类场景和风格。
-   多样化版式生成：支持自动生成海报的背景和文字智能排版，支持横版和竖版海报，支持超高分辨率提升和高清二次精致修复模式，可极速制作多样化出彩海报作品。
-   效果业界领先：创意海报生成图像语义一致性更精准，AI局部创作布局自然、细节丰富、画面细腻、结果逼真，又保持视觉效果的和谐与专业性，无需担心人工合成的痕迹。
-   稳定、易用平台服务：提供在高并发、大流量下的稳定创意海报生成响应，可直接调用的简单推理API 接口，服务简单易用，易被集成，兼容性强。

<a id="模型概览"></a>

<a id="c46f30c71ekzj"></a>

### 模型概览

<table><tbody><tr><td rowspan="2"><strong>模型名</strong></td><td rowspan="2"><p><strong>免费额度</strong><a href="../../../test-1/new-free-quota.md">（查看）</a></p></td><td rowspan="2"><strong>计费单价</strong></td><td colspan="2"><strong>限流（含主账号与RAM子账号）</strong></td></tr><tr><td><strong>任务下发接口QPS限制</strong></td><td><strong>同时处理中任务数量</strong></td></tr><tr><td><p>wanx-poster-generation-v1</p></td><td><p>500张</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../../../model-experience/image-and-video-generation/image-model/text-to-image.md">文本生成图像</a>获取替代方案。</p></blockquote></td><td><p>2</p></td><td><p>1</p></td></tr></tbody></table>

<a id="快速开始"></a>

<a id="b451aa4726ffa"></a>

## 快速开始

输入限制：

-   提示词输入限制：中文和英文提示词二者至少选其一，也可以都选。两者加起来最多50个字/单词。
-   主标题字符限制：最多30个字符。
-   副标题字符限制：最多30个字符。
-   正文字符限制：最多50个字符。

<table><tbody><tr><td><strong>请求参数</strong></td><td><strong>输出的海报效果图</strong></td></tr><tr><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;春节快乐&quot;,
        &quot;sub_title&quot;: &quot;家庭团聚，共享天伦之乐&quot;,
        &quot;body_text&quot;: &quot;春节是中国最重要的传统节日之一，它象征着新的开始和希望&quot;,
        &quot;prompt_text_zh&quot;: &quot;灯笼，小猫，梅花&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;lora_name&quot;: &quot;童话油画&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.7,
        &quot;ctrl_step&quot;: 0.7,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4644874271/p829105.png" alt="jianguo.wjg_通用海报专项_results_cache_dashscope_2024-08-01_2024-08-01-07-38-57_66f607dc-dc0b-4f06-a306-2e880b7826d8_0.render (1).png"></td></tr></tbody></table>

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取与配置 API Key](../../../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="sec-tabs"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

**1、创建创意海报生成任务**

接口返回任务ID，可根据任务ID查询图像生成的结果。

<a id="code-block-2"></a>

```bash
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wanx-poster-generation-v1",
    "input": {
        "title": "春节快乐",
        "sub_title": "家庭团聚，共享天伦之乐",
        "body_text": "春节是中国最重要的传统节日之一，它象征着新的开始和希望",
        "prompt_text_zh": "灯笼，小猫，梅花",
        "wh_ratios": "竖版",
        "lora_name": "童话油画",
        "lora_weight": 0.8,
        "ctrl_ratio": 0.7,
        "ctrl_step": 0.7,
        "generate_mode": "generate",
        "generate_num": 1
    },
    "parameters": {}
}'
```

**2、根据任务ID查询结果**

<a id="code-block-3"></a>

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{your_task_id} \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="创意海报风格示例"></a>

<a id="051f862c0aij1"></a>

## 创意海报风格示例

<table><tbody><tr><td><strong>海报风格</strong></td><td><strong>海报效果图</strong></td><td><strong>参数示例</strong></td></tr><tr><td><p>中国刺绣</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849338.png" alt="image"></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;谷雨&quot;,
        &quot;sub_title&quot;: &quot;24 SOLAR TERMS&quot;,
        &quot;body_text&quot;: &quot;遥看春雨润百谷\n听闻万象正生长&quot;,
        &quot;prompt_text_zh&quot;: &quot;中国龙，梅花，云朵&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;lora_name&quot;: &quot;中国刺绣&quot;,
        &quot;lora_weight&quot;: 0.5,
        &quot;ctrl_ratio&quot;: 0.7,
        &quot;ctrl_step&quot;: 0.7,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>2D插画1</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849343.png" alt="image"></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;抽象艺术家&quot;,
        &quot;sub_title&quot;: &quot;有趣的灵魂终要相遇&quot;,
        &quot;body_text&quot;: &quot;创意海报生成，自由设计，瞬间点亮创意生活&quot;,
        &quot;prompt_text_zh&quot;: &quot;抽象艺术，几何形状，流动线条，极简主义，明亮色彩&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;lora_name&quot;: &quot;2D插画1&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.6,
        &quot;ctrl_step&quot;: 0.6,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>不设置lora_name参数，在prompt指定海报风格</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849389.png" alt="image"></td><td><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;清明&quot;,
        &quot;sub_title&quot;: &quot;袅绕青烟\n穿越天上人间&quot;,
        &quot;body_text&quot;: &quot;人间四月芳菲始\n春归清明雨时节&quot;,
        &quot;prompt_text_zh&quot;: &quot;朦胧远山，柳树，雨水，2D插画&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;ctrl_ratio&quot;: 0.7,
        &quot;ctrl_step&quot;: 0.7,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>浅蓝抽象</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849345.png" alt="image"></td><td><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;抽象艺术家&quot;,
        &quot;sub_title&quot;: &quot;有趣的灵魂终要相遇&quot;,
        &quot;body_text&quot;: &quot;创意海报生成，自由设计，瞬间点亮创意生活&quot;,
        &quot;prompt_text_en&quot;:&quot;master piece, high quality, futuristic city, streamlined, neon, light blue and light purple, glass texture&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;lora_name&quot;:&quot;浅蓝抽象&quot;,
        &quot;lora_weight&quot;:0.8,
        &quot;ctrl_ratio&quot;: 0.6,
        &quot;ctrl_step&quot;: 0.6,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>深蓝抽象</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849351.png" alt="image"></td><td><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;抽象艺术家&quot;,
        &quot;sub_title&quot;: &quot;有趣的灵魂终要相遇&quot;,
        &quot;body_text&quot;: &quot;创意海报生成，自由设计，瞬间点亮创意生活&quot;,
        &quot;prompt_text_en&quot;: &quot;uminous Particles, Streamlined, holography, Particles, Abstract, Blue and Purple, Tech Style&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;lora_name&quot;: &quot;深蓝抽象&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.6,
        &quot;ctrl_step&quot;: 0.6,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>童话油画</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849353.png" alt="image"></td><td><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;元宵节&quot;,
        &quot;sub_title&quot;: &quot;正月十五&quot;,
        &quot;body_text&quot;: &quot;团圆时节，汤圆香甜，祝你幸福美满！&quot;,
        &quot;prompt_text_zh&quot;: &quot;灯笼，小猫，梅花&quot;,
        &quot;wh_ratios&quot;: &quot;竖版&quot;,
        &quot;lora_name&quot;: &quot;童话油画&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.7,
        &quot;ctrl_step&quot;: 0.7,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>童话油画</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849356.png" alt="image"></td><td><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;元宵节&quot;,
        &quot;sub_title&quot;: &quot;正月十五&quot;,
        &quot;body_text&quot;: &quot;团圆时节，汤圆香甜，祝你幸福美满！&quot;,
        &quot;prompt_text_zh&quot;: &quot;灯笼，小猫，梅花&quot;,
        &quot;wh_ratios&quot;: &quot;横版&quot;,
        &quot;lora_name&quot;: &quot;童话油画&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.7,
        &quot;ctrl_step&quot;: 0.7,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>剪纸工艺</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849357.png" alt="image"></td><td><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;星河浩瀚&quot;,
        &quot;sub_title&quot;: &quot;一闪一闪亮晶晶&quot;,
        &quot;body_text&quot;: &quot;创意海报生成，自由设计，瞬间点亮创意生活&quot;,
        &quot;prompt_text_zh&quot;: &quot;闪亮的星星，月亮，银河，卫星 &quot;,
        &quot;wh_ratios&quot;: &quot;横版&quot;,
        &quot;lora_name&quot;: &quot;剪纸工艺&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.6,
        &quot;ctrl_step&quot;: 0.6,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr><tr><td><p>浓郁色彩</p></td><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8949386271/p849359.png" alt="image"></td><td><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;: &quot;科技改变生活&quot;,
        &quot;sub_title&quot;: &quot;有趣的灵魂终要相遇&quot;,
        &quot;body_text&quot;: &quot;创意海报生成，自由设计，瞬间点亮创意生活&quot;,
        &quot;prompt_text_zh&quot;: &quot;黑色背景上的色彩爆炸，精细渲染的纹理，简单曲线，创新的页面设计，高速胶片，流线型的形式&quot;,
        &quot;wh_ratios&quot;: &quot;横版&quot;,
        &quot;lora_name&quot;: &quot;浓郁色彩&quot;,
        &quot;lora_weight&quot;: 0.8,
        &quot;ctrl_ratio&quot;: 0.8,
        &quot;ctrl_step&quot;: 0.7,
        &quot;generate_mode&quot;: &quot;generate&quot;,
        &quot;generate_num&quot;: 1
    },
    &quot;parameters&quot;: {}
}
</code></pre></td></tr></tbody></table>

<a id="api参考"></a>

<a id="8db33ec4b87vm"></a>

## API参考

API的输入输出参数，请参见[创意海报生成](../../../../model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)。
