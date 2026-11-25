# 万相-图生视频-视频特效列表

万相提供视频特效功能， 无需输入提示词，只需指定特效模板 ，即可轻松生成预设的动态效果。

视频特效列表仅支持在“[图生视频-基于首帧](legacy-image-to-video-api-reference-8b02dd673da405f1.md)”和“[图生视频-基于首尾帧](legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)”中使用。

<a id="使用方法"></a>

<a id="17153ae3a3x2r"></a>

## 使用方法

视频特效与图生视频的使用方式不同，请遵循以下规则：

-   **仅需一张首帧图像**：无论选用的是“基于首帧”还是“基于首尾帧”的模型，**只需要提供一张首帧图像**。
-   **无需任何提示词**：在特效模式下，模型会忽略 prompt 字段。建议不传入该参数，专注于选择视觉效果。
-   **选择一个模板**：通过 `template` 参数从特效列表中选择一个动态效果。模型将根据模板生成指定的动态效果。

> **说明**
>
> 不同的模型支持的特效模板有所不同。请务必参考[特效列表-首帧生视频](wanx-video-effects-5b23bdd72b8e7944.md#89f64eb5a812c)和[特效列表-首尾帧生视频](wanx-video-effects-5b23bdd72b8e7944.md#6e5be7aaa1rc2)，确保所使用的 template 值与模型匹配。

**图生视频-基于首帧**

<table><thead><tr><th><strong>输入首帧</strong></th><th><strong>输入提示词</strong></th><th><strong>输入template</strong></th><th><strong>输出视频</strong></th></tr></thead><tbody><tr><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0458180571/p976602.png" alt="wanx-demo-1"></td><td><p>无需传入</p></td><td><p>flying</p><blockquote><p>使用“魔法悬浮”特效</p></blockquote></td><td></td></tr></tbody></table>

**图生视频-基于首尾帧**

<table><thead><tr><th><strong>输入首帧</strong></th><th><strong>输入尾帧</strong></th><th><strong>输入提示词</strong></th><th><strong>输入template</strong></th><th><strong>输出视频</strong></th></tr></thead><tbody><tr><td><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8150385571/p1000087.png" alt="首尾帧生视频-视频特效-demo"></td><td><p>无需传入</p></td><td><p>无需传入</p></td><td><p>hanfu-1</p><blockquote><p>使用“唐韵翩然”特效</p></blockquote></td><td></td></tr></tbody></table>

**示例代码**

<a id="sec-tabs"></a>

<a id="图生视频-基于首帧"></a>

<a id="图生视频-基于首帧-h4"></a>

#### 图生视频-基于首帧

**首帧特效**：对首帧图像生成特效视频。

<a id="code-block"></a>

```bash
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-i2v-turbo",
    "input": {
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
        "template": "flying"
    },
    "parameters": {
        "resolution": "720P"
    }
}'
```

> 完整代码请参见[图生视频-基于首帧](legacy-image-to-video-api-reference-8b02dd673da405f1.md)。

<a id="python-sdk"></a>

<a id="python-sdk-h4"></a>

#### Python SDK

<a id="code-block-2"></a>

```python
import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

def sample_async_call():
    # 异步提交视频生成任务
    # template（视频特效模板）为 input 段字段，不在具名签名内，经 extra_input 透传
    try:
        job = client.videos.jobs.create(model='wanx2.1-i2v-turbo',
                                        image_url='https://cdn.translate.alibaba.com/r/wanx-demo-1.png',
                                        extra_input={'template': 'flying'},
                                        resolution='720P')
        print(job)
        print("task_id: %s" % job.task_id)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return

    # 查询任务状态
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # 等待任务完成（指数退避轮询，默认总预算24小时）
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_async_call()
```

<a id="图生视频-基于首尾帧"></a>

<a id="图生视频-基于首尾帧-h4"></a>

#### 图生视频-基于首尾帧

**首尾帧特效**：只需提供一张首帧图像，无需尾帧图像，即可生成视频特效。

-   若同时提供first\_frame\_url、last\_frame\_url、template，将忽略last\_frame\_url。
-   若仅提供last\_frame\_url、template，请求将报错。

<a id="code-block-3"></a>

```bash
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-kf2v-plus",
    "input": {
        "first_frame_url": "https://ty-yuanfang.oss-cn-hangzhou.aliyuncs.com/lizhengjia.lzj/tmp/11.png",
        "template": "hanfu-1"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true
    }
}'
```

> 完整代码请参见[图生视频-基于首尾帧](legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)。

<a id="特效列表-首帧生视频"></a>

<a id="89f64eb5a812c"></a>

## 特效列表-首帧生视频

视频特效的使用方式请参见[使用方法](wanx-video-effects-5b23bdd72b8e7944.md#17153ae3a3x2r)。

视频效果取决于模板和输入图片。为获得最佳效果，请先预览模板示例，并参考其“输入图像建议”，再使用您自己的图片进行尝试。

<a id="通用特效"></a>

<a id="85838a9e35vnu"></a>

### 通用特效

<table><thead><tr><th><strong>特效名称</strong></th><th><strong>template参数值</strong></th><th><strong>示例效果</strong></th><th><strong>支持模型</strong></th><th><strong>输入图像建议</strong></th></tr></thead><tbody><tr><td><p>解压捏捏</p></td><td><strong>squish</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr><tr><td><p>转圈圈</p></td><td><strong>rotation</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr><tr><td><p>戳戳乐</p></td><td><strong>poke</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr><tr><td><p>气球膨胀</p></td><td><strong>inflate</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr><tr><td><p>分子扩散</p></td><td><strong>dissolve</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr><tr><td><p>热浪融化</p></td><td><strong>melt</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr><tr><td><p>冰淇淋星球</p></td><td><strong>icecream</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持任意主体</li><li>建议使用主体突出，与背景有明显区分度的图片</li></ul></td></tr></tbody></table>

<a id="单人特效"></a>

<a id="0868f6f028foz"></a>

### 单人特效

<table><thead><tr><th><strong>特效名称</strong></th><th><strong>template参数值</strong></th><th><strong>示例效果</strong></th><th><strong>支持模型</strong></th><th><strong>输入图像建议</strong></th></tr></thead><tbody><tr><td><p>时光木马</p></td><td><strong>carousel</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>爱你哟</p></td><td><strong>singleheart</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>摇摆时刻</p></td><td><strong>dance1</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>头号甩舞</p></td><td><strong>dance2</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用全身正面照片</li></ul></td></tr><tr><td><p>星摇时刻</p></td><td><strong>dance3</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用全身正面照片</li></ul></td></tr><tr><td><p>指感节奏</p></td><td><strong>dance4</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>舞动开关</p></td><td><strong>dance5</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>人鱼觉醒</p></td><td><strong>mermaid</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身的正面照片</li></ul></td></tr><tr><td><p>学术加冕</p></td><td><strong>graduation</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>巨兽追袭</p></td><td><strong>dragon</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>财从天降</p></td><td><strong>money</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>水母之约</p></td><td><strong>jellyfish</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>瞳孔穿越</p></td><td><strong>pupil</strong></td><td></td><td><p>wanx2.1-i2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr></tbody></table>

<a id="单人或动物特效"></a>

<a id="10a28193a1mm8"></a>

### 单人或动物特效

<table><thead><tr><th><strong>特效名称</strong></th><th><strong>template参数值</strong></th><th><strong>示例效果</strong></th><th><strong>支持模型</strong></th><th><strong>输入图像建议</strong></th></tr></thead><tbody><tr><td><p>魔法悬浮</p></td><td><strong>flying</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持单人或动物照片</li><li>建议使用全身的正面照片</li></ul></td></tr><tr><td><p>赠人玫瑰</p></td><td><strong>rose</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持单人或动物照片</li><li>建议使用半身至全身的正面照片，避免露出手部</li></ul></td></tr><tr><td><p>闪亮玫瑰</p></td><td><strong>crystalrose</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持单人或动物照片</li><li>建议使用半身至全身的正面照片，避免露出手部</li></ul></td></tr></tbody></table>

<a id="双人特效"></a>

<a id="4f2b5f26f1jst"></a>

### 双人特效

<table><thead><tr><th><strong>特效名称</strong></th><th><strong>template参数值</strong></th><th><strong>示例效果</strong></th><th><strong>支持模型</strong></th><th><strong>输入图像建议</strong></th></tr></thead><tbody><tr><td><p>爱的抱抱</p></td><td><strong>hug</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持双人照片</li><li>建议两人正面看向镜头或相对站立 （面对面），可为半身或全身照</li></ul></td></tr><tr><td><p>唇齿相依</p></td><td><strong>frenchkiss</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持双人照片</li><li>建议两人正面看向镜头或相对站立 （面对面），可为半身或全身照</li></ul></td></tr><tr><td><p>双倍心动</p></td><td><strong>coupleheart</strong></td><td></td><td><p>wanx2.1-i2v-plus</p><p>wanx2.1-i2v-turbo</p></td><td><ul><li>支持双人照片</li><li>建议两人正面看向镜头或相对站立 （面对面），可为半身或全身照</li></ul></td></tr></tbody></table>

<a id="特效列表-首尾帧生视频"></a>

<a id="6e5be7aaa1rc2"></a>

## 特效列表-首尾帧生视频

视频效果取决于模板和输入图片。为获得最佳效果，请先预览模板示例，并参考其“输入图像建议”，再使用您自己的图片进行尝试。

> **说明**
>
> 首尾帧生视频的特效是基于首尾帧模型训练，但实际使用时**仅需传入首帧图像**，无需提供尾帧，效果等同于首帧生成视频。具体请参见[使用方法](wanx-video-effects-5b23bdd72b8e7944.md#17153ae3a3x2r)。

<a id="单人特效-2"></a>

<a id="ee4c06cbd14r1"></a>

### 单人特效

<table><thead><tr><th><strong>特效名称</strong></th><th><strong>template参数值</strong></th><th><strong>示例效果</strong></th><th><strong>支持模型</strong></th><th><strong>输入图像建议</strong></th></tr></thead><tbody><tr><td><p>唐韵翩然</p></td><td><strong>hanfu-1</strong></td><td></td><td><p>wanx2.1-kf2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>机甲变身</p></td><td><strong>solaron</strong></td><td></td><td><p>wanx2.1-kf2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>闪耀封面</p></td><td><strong>magazine</strong></td><td></td><td><p>wanx2.1-kf2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>机械觉醒</p></td><td><strong>mech1</strong></td><td></td><td><p>wanx2.1-kf2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr><tr><td><p>赛博登场</p></td><td><strong>mech2</strong></td><td></td><td><p>wanx2.1-kf2v-plus</p></td><td><ul><li>支持单人照片</li><li>建议使用半身至全身的正面照片</li></ul></td></tr></tbody></table>

<a id="api参考"></a>

<a id="102ccf86556nk"></a>

## API参考

-   API参数说明和完整代码示例，请参见[图生视频-基于首帧](legacy-image-to-video-api-reference-8b02dd673da405f1.md)、[图生视频-基于首尾帧](legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)。

、
