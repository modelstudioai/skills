# 千问-图像生成与编辑3.0 API参考

千问-图像生成与编辑3.0模型同时支持文生图（T2I）和图生图/图像编辑（I2I），可根据文本提示词直接生成图像，也可基于1-3张参考图结合编辑指令进行精确编辑。

**重要**

该模型目前处于邀测阶段，您需要前往模型广场申请开通后方可使用。

## **模型概览**

**模型名称**

**模型简介**

**输出图像规格**

qwen-image-3.0-pro

千问图像生成与编辑3.0模型，同时支持文生图（T2I）和图生图/图像编辑（I2I）。

图像分辨率：

-   **文生图（T2I）**：总像素需在512\*512至2048\*2048之间。
    
-   **图生图（I2I）**：总像素需在512\*512至2048\*2048之间。
    
-   **默认**：不指定`size`时，模型根据提示词自动推荐分辨率。
    

图像格式：png

## **前提条件**

在调用前，您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。目前，该SDK已支持Python和Java。

**重要**

华北2（北京）和新加坡地域拥有独立的 **API Key** 与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

**重要**

阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
    
-   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
    

其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

## HTTP调用

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**新加坡地域**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

#### 请求参数

## 文生图（T2I）

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

## 图生图/图像编辑（I2I）

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

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称，当前可用模型为`qwen-image-3.0-pro`。

**input** `_object_` **（必选）**

输入参数对象，包含以下字段：

**属性**

**messages** `_array_` **（必选）**

请求内容数组。**当前仅支持单轮对话**，因此数组内**有且只有一个对象**，该对象包含`role`和`content`两个属性。

**属性**

**role** `_string_` **（必选）**

消息发送者角色，必须设置为`user`。

**content** `_array_` **（必选）**

消息内容数组，根据使用场景有不同的组合方式：

-   **文生图（T2I）**：仅包含一个`{"text": "..."}`对象。
    
-   **图生图（I2I）**：包含1-3个`{"image": "..."}`对象和1个`{"text": "..."}`对象。
    

**属性**

**image** `_string_` （可选）

输入图像的 URL 或 Base64 编码数据。I2I场景下支持传入1-3张图像。多图输入时，按照数组顺序定义图像顺序。

**图像要求：**

-   图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP和GIF。
    
-   图像分辨率：建议图像的宽和高均在384像素至2048像素之间。
    
-   图像大小：不超过10MB。
    

**支持的输入格式**

1.  公网URL：支持 HTTP 和 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
    
2.  Base64 编码：格式为`data:{MIME_type};base64,{base64_data}`。
    

**text** `_string_` **（必选）**

正向提示词，用于描述您期望生成或编辑的图像内容、风格和构图。支持中英文。

**注意**：仅支持传入一个text，不传或传入多个将报错。

**parameters** `_object_` （可选）

控制图像生成的附加参数。

**属性**

**prompt\_extend** `_boolean_` （可选）

是否开启提示词智能改写，默认值为 `true`（建议开启）。开启后，模型会优化正向提示词，对描述较简单的提示词效果提升明显。

**n** `_integer_` （可选）

输出图像的数量，支持输出1-6张图片，默认值为1。

**size** `_string_` （可选）

设置输出图像的分辨率，格式为`宽*高`，例如`"1024*1024"`。未指定时由模型根据提示词自动推荐分辨率。

-   **文生图（T2I）**：像素范围512\*512至2048\*2048。
    
-   **图生图（I2I）**：像素范围512\*512至2048\*2048。
    

**negative\_prompt** `_string_` （可选）

反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。

**seed** `_integer_` （可选）

随机数种子，取值范围`[0, 2147483647]`。固定种子可使生成结果相对稳定。

**watermark** `_boolean_` （可选）

是否添加水印，默认值为 `false`。

#### 响应参数

## 任务执行成功

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

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
        "width": 1024,
        "height": 1024,
        "image_count": 1
    },
    "request_id": "571ae02f-5c9d-436c-83c2-f221e6df0xxx"
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "31f808fd-8eef-9004-xxxxx",
    "code": "InvalidApiKey",
    "message": "Invalid API-key provided."
}
```

**output** `_object_`

包含模型生成结果。

**属性**

**choices** `_array_`

结果选项列表。

**属性**

**finish\_reason** `_string_`

任务停止原因，自然停止时为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

消息内容，包含生成的图像信息。

**属性**

**image** `_string_`

生成图像的 URL，格式为PNG。**链接有效期为24小时**，请及时下载并保存图像。

**usage** `_object_`

本次调用的资源使用情况，仅调用成功时返回。

**属性**

**width** `_integer_`

生成图像的宽度（像素）。

**height** `_integer_`

生成图像的高度（像素）。

**image\_count** `_integer_`

生成图像的张数。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

## SDK调用

以下以图生图/图像编辑（I2I）为示例，展示Python和Java SDK的调用方式。

## Python

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

## Java

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

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
