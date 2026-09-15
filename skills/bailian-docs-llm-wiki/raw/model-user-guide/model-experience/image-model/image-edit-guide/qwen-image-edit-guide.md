# 千问-图像编辑Qwen-Image-Edit

千问-图像编辑模型支持多图输入和多图输出，可精确修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节。

## 快速开始

在调用前，您需要[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。目前，该SDK已支持Python和Java。

> 请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

#### Python

```
import os
import base64
import mimetypes
import dashscope
from dashscope import MultiModalConversation

dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Unsupported or unrecognized image format")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# [方法一] 使用公网图像URL
image_url = "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png"

# [方法二] 使用Base64编码图像
# image_url = encode_file("./your_image.png")

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-image-3.0-pro",
    messages=[{
        "role": "user",
        "content": [
            {"image": image_url},
            {"text": "帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物换上一套彰显高雅气质的都市职场穿搭，场景设定在一家装修现代简约的高端咖啡店内。"}
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
import java.util.Base64;
import java.util.Collections;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.utils.Constants;

public class ImageEditExample {
    public static void main(String[] args) {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";

        // [方法一] 使用公网图像URL
        String imageUrl = "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png";

        // [方法二] 使用Base64编码图像
        // String imageUrl = encodeFile("/path/to/your/image.png");

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
            .role(Role.USER.getValue())
            .content(Arrays.asList(
                Collections.singletonMap("image", imageUrl),
                Collections.singletonMap("text", "帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物换上一套彰显高雅气质的都市职场穿搭，场景设定在一家装修现代简约的高端咖啡店内。")
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

    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("File does not exist: " + filePath);
        }
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("Cannot detect file type: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("Unsupported or unrecognized image format");
        }
        byte[] fileBytes = null;
        try {
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("Cannot read file content: " + filePath);
        }
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }
}
```

#### curl

以下为华北2（北京）地域的URL，各地域的URL不同。如果使用新加坡地域的模型，需将URL替换为：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

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
                        "image": "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/yBRq1ZPYEaXdyOdv/img/33a80a19-7ac7-4c64-b0fa-7d685b7046a0.png"
                    },
                    {
                        "text": "帮我生成一张充满高级感的都市风格女性写真，画面中人物完美保留输入图片中这位年轻女性的面部特征与一头柔顺的黑色长发。人物脱下原本的米色针织上衣，换上一套彰显高雅气质的都市职场穿搭，身穿一件质感垂顺的香槟色真丝衬衫，外搭一件剪裁利落的深灰色休闲西装外套，下身搭配同色系的高腰阔腿裤，整体造型既干练又富有女人味。场景设定在一家装修现代简约的高端咖啡店内，背景是通透的落地玻璃窗，窗外隐约可见繁华的城市街景，室内摆放着深色实木长桌和舒适的皮质座椅，桌面上放置着一台打开的银色笔记本电脑、一份文件和一杯热气腾腾的美式咖啡。人物呈现出慵懒而放松的办公姿态，身体微微后仰倚靠在椅背上，一只手臂自然搭在扶手上，另一只手轻轻握着咖啡杯置于桌边，头部微侧，眼神清澈从容且带有一丝慵懒地直视镜头，嘴角挂着一抹优雅自信的微笑。人物化着精致得体的正式场合妆容，底妆清透干净，眉眼线条清晰利落，唇部涂抹着显气色的豆沙色口红，展现出成熟知性的魅力。光线采用午后柔和的自然光，从侧面透过落地窗洒入，在人物的面部轮廓和衣物褶皱上留下细腻的光影过渡，背景呈现自然的景深虚化效果，色彩以大地色、灰色和暖白色为主调，营造出宁静、高级且充满故事感的都市办公氛围，构图采用经典的竖幅七分身人像视角，人物位于画面视觉中心略偏右，比例协调，画质清晰细腻。"
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

响应示例

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

通过URL下载图像到本地

Code 1

```
# 需要安装requests以下载图像: pip install requests
import requests

def download_image(image_url, save_path='output.png'):
    try:
        response = requests.get(image_url, stream=True, timeout=300)  # 设置超时
        response.raise_for_status()  # 如果HTTP状态码不是200，则引发异常
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"图像已成功下载到: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"图像下载失败: {e}")

image_url = "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
download_image(image_url, save_path='output.png')
```

Code 2

```
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class ImageDownloader {
    public static void downloadImage(String imageUrl, String savePath) {
        try {
            URL url = new URL(imageUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(300000);
            connection.setRequestMethod("GET");
            InputStream inputStream = connection.getInputStream();
            FileOutputStream outputStream = new FileOutputStream(savePath);
            byte[] buffer = new byte[8192];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
            inputStream.close();
            outputStream.close();

            System.out.println("图像已成功下载到: " + savePath);
        } catch (Exception e) {
            System.err.println("图像下载失败: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String imageUrl = "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx?Expires=xxx";
        String savePath = "output.png";
        downloadImage(imageUrl, savePath);
    }
}
```

## 模型选型建议

-   `qwen-image-3.0-pro`**系列（推荐）：**千问图像3.0旗舰版，图像生成与编辑能力全面升级，文字渲染、真实质感、语义遵循能力更强。
-   `qwen-image-3.0`**系列：**千问图像3.0标准版，兼顾质量与速度。

各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)模型列表。

## 输入说明

### 输入图像（messages）

`messages` 是一个数组，且必须仅包含一个对象。该对象需包含 `role` 和 `content` 属性。其中`role`必须设置为`user`，`content`需要同时包含`image`（1-3张图像）和`text`（一条编辑指令）。

输入图片必须满足以下要求：

-   图片格式：JPG、JPEG、PNG、BMP、TIFF、WEBP和GIF。
    
    > 输出图像为PNG格式，对于GIF动图，仅处理其第一帧。
    
-   图片分辨率：为获得最佳效果，建议图像的宽和高均在384像素至3072像素之间。分辨率过低可能导致生成效果模糊，过高则会增加处理时长。
    
-   文件大小：单张图片文件大小不得超过 10MB。
    

```
"messages": [
    {
        "role": "user",
        "content": [
            { "image": "图1的公网URL或Base64数据" },
            { "image": "图2的公网URL或Base64数据" },
            { "image": "图3的公网URL或Base64数据" },
            { "text": "您的编辑指令，例如：'图1中的女生穿着图2中的黑色裙子按图3的姿势坐下'" }
        ]
    }
]
```

### 图像输入顺序

多图输入时，按照数组中的顺序定义图像顺序。因此，提示词引用的图像编号需要**与图像数组中的顺序一一对应**，例如：数组中的第一张图片为"图1"，第二张为"图2"，或者使用标记形式如"\[图1\]"、"\[图2\]"。

```
{
    "content": [
        {"text": "编辑指令，如：将图1中的闹钟放置到图2的餐桌的花瓶旁边位置"},
        {"image": "https://example.com/image1.png"},
        {"image": "https://example.com/image2.png"}
    ]
}
```

**输入图像**

**输出图像**

![image (19)-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1025838.webp)

图1

![image (20)-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7142593671/p1025839.webp)

图2

![04e0fc39-7ad6-41e0-9df9-1f69ac3ce825-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1021092.webp)

提示词：把图1移动到图2上

![36ed450d-bd54-4169-b13f-3d0f26d9d360-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1021093.webp)

提示词：把图2移动到图1上

### 图像传入方式

**公网URL**

-   提供一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。本地文件请参见[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
-   示例值：`https://xxxx/img.png`。

**Base64编码**

将图像文件转换为 Base64 编码字符串，并按格式拼接：`data:{mime_type};base64,{base64_data}`。

-   `{mime_type}`：图像的媒体类型，需与文件格式对应。
-   `{base64_data}`：文件经过 Base64 编码后的字符串。
-   示例值：`data:image/jpeg;base64,GDU7MtCZz...`（示例已截断，仅做演示）

完整示例代码请参见[Python SDK调用](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api#a3ad9a3b6d9if)、[Java SDK调用](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api#589b80853e6rn)。

### 更多参数

可以通过以下**可选**参数调整生成效果：

-   **n**：指定输出图像数量，默认值为1。qwen-image-3.0系列、qwen-image-2.0系列、qwen-image-edit-max和qwen-image-edit-plus系列模型支持输出1-6张图片，`qwen-image-edit`模型仅支持输出1张图片。
-   **negative\_prompt（反向提示词）**：描述不希望在画面中出现的内容，如“模糊”、“多余的手指”等，用于辅助优化生成质量。
-   **watermark**：是否在图像右下角添加 "Qwen-Image" 水印。默认值为 `false`。
-   **seed**：随机数种子。取值范围是`[0, 2147483647]`。如果不提供，则算法自动生成一个随机数作为种子。使用相同的 seed 值可帮助生成内容保持相对稳定。

以下**可选**参数仅qwen-image-3.0系列、qwen-image-2.0系列、qwen-image-edit-max、qwen-image-edit-plus系列模型支持：

-   **size**：设置输出图像的分辨率，格式为`宽*高`，例如`"1024*2048"`。对于qwen-image-3.0系列模型，像素面积范围为512_512至2048_2048，宽高比限制为1:8至8:1，未指定时由模型根据提示词自动推荐分辨率。对于qwen-image-2.0系列模型，支持自由设置宽高，输出图像总像素需在512_512至2048_2048之间，默认分辨率与输入图（多图输入时为最后一张图）一致。对于qwen-image-edit-max、qwen-image-edit-plus系列模型，宽和高的取值范围均为\[512, 2048\]像素，默认保持与原图相似的长宽比，总像素接近`1024*1024`分辨率。
-   **prompt\_extend：**是否开启prompt智能改写功能，默认值为 `true`。开启后，模型将优化提示词，对描述性不足、较为简单的prompt提升效果较明显。

完整参数列表请参考[千问-图像编辑API](raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)。

## 效果概览

### 多图融合

**输入图像1**

**输入图像2**

**输入图像3**

**输出图像**

![image83](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1082029571/p1011712.webp)

![image103](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1082029571/p1011753.webp)

![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105461671/p1012002.webp)

![2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3105461671/p1012004.webp)

图1中的女生戴着图2中的项链，左肩挎着图3中的包

### 主体一致性保持

**输入图像**

**输出图像1**

**输出图像2**

**输出图像3**

![image5](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011789.webp)

![image4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011790.webp)

修改为蓝底证件照，人物穿上白色衬衫，黑色西装，打着条纹领带

![image6](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011791.webp)

人物穿上白色衬衫，灰色西装，打着条纹领带，一只手摸着领带，浅色背景

![image7](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011792.webp)

人物穿着粗笔刷字体的“千问图像”的黑色卫衣，依靠在护栏边，阳光照在发丝上，身后是大桥和海

![image12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1012037.webp)

![image13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1012038.webp)

把这个空调放在客厅，沙发旁边

![image14](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1012039.webp)

在空调出风口增加雾气，一直到沙发上，并且增加绿叶。

![image15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1012040.webp)

在上方增加白色的手写体"自然新风 畅享呼吸"

### 草图创作

**输入图像**

**输出图像**

![image42](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011821.webp)

![image43](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011822.webp)

生成一张图像，符合图1所勾勒出的精致形状，并遵循以下描述：一位年轻的女子在阳光明媚的日子里微笑着，她戴着一副棕色的圆形太阳镜，镜框上有豹纹图案。她的头发被整齐地盘起，耳朵上佩戴着珍珠耳环，脖子上围着一条带有紫色星星图案的深蓝色围巾，穿着一件黑色皮夹克。

![image44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011824.webp)

生成一张图像，符合图1所勾勒出的精致形状，并遵循以下描述：一位年老的老人朝着镜头微笑，他的脸上布满皱纹，头发在风中凌乱，戴着一副圆框的老花镜。脖子上戴着一条破旧的红色围巾，上面有星星图案。穿着一件棉衣。

### 文创生成

**输入图像**

**输出图像**

![图片 1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999719.png)

![image23](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011685.webp)

让这只熊坐在月亮下（用白色背景上的浅灰弯月轮廓表示），抱着吉他，周围漂浮着小星星和诗句气泡，如“Be Kind”。

![image22](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011686.webp)

将这个图案印在一件T恤和一个手提纸袋上。一个女模特正在展示这些物品。这个女生还戴着一顶鸭舌帽，帽子上写着"Be kind”。

![image21](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011687.webp)

一个超逼真的1/7比例角色模型，设计为商业产品成品，放置在一台带有白色键盘的iMac电脑桌上。模型站在一个干净、圆形的透明亚克力底座上，没有标签或文字。专业的摄影棚灯光凸显了雕刻细节。在背景的iMac屏幕上，展示同一模型的ZBrush建模过程。在模型旁边，放置一个包装盒，前面带有透明窗户，仅显示内部透明塑料壳，其高度略高于模型，尺寸合理以容纳模型。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999632.png)

这只熊穿着宇航服，伸出手指向远方

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999633.png)

这只熊穿着华丽的舞裙，双臂展开，做出优雅的舞蹈动作

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999630.png)

这只熊穿着运动服，手里拿着篮球，单腿弯曲

### 根据深度图生成图像

**输入图像**

**输出图像**

![image36](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011810.webp)

![image37](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011811.webp)

生成一张图像，符合图1所勾勒出的深度图，并遵循以下描述：在一条街边的小巷中停放着一辆蓝色的自行车，背景中有几株从石缝中长出来的杂草

![image38](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011812.webp)

生成一张图像，符合图1所勾勒出的深度图，并遵循以下描述：一辆红色的破旧的自行车停在一条泥泞的小路上，背景是茂密的原始森林

### 根据关键点生成图像

**输入图像**

**输出图像**

![image40](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011817.webp)

![image41](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011818.webp)

生成一张图像，符合图1所勾勒出的人体姿态，并遵循以下描述：一位身穿着汉服的中国美女，在雨中撑着油纸伞，背景是苏州园林。

![image39](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011819.webp)

生成一张图像，符合图1所勾勒出的人体姿态，并遵循以下描述：一位男生，站在地铁站台上，他头上戴着一顶棒球帽，穿着T恤和牛仔裤。背后是飞驰而过的列车。

### 文字编辑

**输入图像**

**输出图像**

**输入图像**

**输出图像**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999641.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999642.png)

将拼字游戏方块上'HEALTH INSURANCE’ **替换为'明天会更好'**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p1000039.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p1000062.png)

将便条上的短语“Take a Breather”**更改为“Relax and Recharge”**

**输入图像**

**输出图像**

![image53](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011772.webp)

![image45](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011774.webp)

将“Qwen-Image”换成黑色的滴墨字体

![image46](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011775.webp)

将“Qwen-Image”换成黑色的手写字体

![image49](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011776.webp)

将“Qwen-Image”换成黑色的像素字体

![image54](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3892029571/p1011777.jpeg)

将“Qwen-Image”换成红色

![image57](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011779.jpeg)

将“Qwen-Image”换成蓝紫渐变色

![image59](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011780.jpeg)

将“Qwen-Image”换成糖果色

![image63](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011783.webp)

将“Qwen-Image”材质换成金属

![image64](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011784.webp)

将“Qwen-Image”材质换成云朵

![image67](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011786.webp)

将“Qwen-Image”材质换成玻璃

### 增删改

**能力**

**输入图像**

**输出图像**

**新增元素**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999647.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999648.png)

在企鹅前方添加一个小型木制标牌，上面写着“Welcome to Penguin Beach”。

**删除元素**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999649.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999650.png)

删除餐盘上的头发

### 视角转换

**输入图像**

**输出图像**

**输入图像**

**输出图像**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999964.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999968.png)

获得正视视角

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999969.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999970.png)

朝向左侧

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999974.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999975.png)

获得后侧视角

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999971.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999972.png)

朝向右侧

### 老照片处理

**能力**

**输入图像**

**输出图像**

**老照片修复及上色**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999552.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4766809571/p999554.png)

修复老照片，去除划痕，降低噪点，增强细节，高分辨率，画面真实，肤色自然，面部特征清晰，无变形。

![image31](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011757.webp)

![image32](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4892029571/p1011759.webp)

根据内容智能上色，使图像更生动

## API参考

API的输入输出参数，请参见[千问-图像编辑](raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 常见问题

### Q：千问图像编辑模型支持哪些语言？

A：目前正式支持**简体中文和英文**；其他语言可自行尝试，但效果存在不确定性。

#### Q: 如何查看模型调用量？

A: 模型调用完一小时后，请在[**模型监控**（北京）](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[**模型监控**（新加坡）](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry) 页面，查看模型的调用次数、成功率等指标。详情请参见[账单查询与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

#### Q：如何获取图像存储的访问域名白名单？

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL（链接有效期为 24 小时，请及时下载保存）。图片URL的域名格式为`dashscope-{标识}.oss-accelerate.aliyuncs.com`或`dashscope-{标识}.oss-cn-{地域}.aliyuncs.com`。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会动态变更，以下bucket名称仅供参考，可能随时更新：dashscope-a717、dashscope-66f3、dashscope-7c2c、dashscope-2522、dashscope-c72b、dashscope-0484、dashscope-7e0f、dashscope-5859、dashscope-5496、dashscope-35f9、dashscope-31d9、dashscope-7f1f、dashscope-cc75、dashscope-64e9。为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。API当前仅支持返回URL格式，不支持base64格式输出。

更多问题请参见[图像生成常见问题](raw/model-api-reference/image-generation/image-faq.md)。
