# 鞋靴模特

鞋靴模特生成对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，可用于模特商品图设计、新鞋AI试穿、模特穿戴布局重绘等场景。

**重要**

-   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   shoemodel-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费。

## 基本介绍

鞋靴模特生成支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，最终生成图片的效果，布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新鞋AI试穿、模特穿戴布局重绘等场景。

### 特色优势

-   效果业界领先：鞋靴模特生成图像语义一致性更精准，AI局部创作布局自然、细节丰富、画面细腻、结果逼真，又保持视觉效果的和谐与专业性，无需担心人工合成的痕迹。
-   稳定、易用平台服务：提供在高并发、大流量下的稳定鞋靴模特生成图片生成响应，可直接调用的简单推理API 接口，服务简单易用，易被集成，兼容性强。

### 使用场景

-   鞋靴商品设计：鞋靴商品设计领域，结合AI技术的优势，设计师们能够以前所未有的速度和精确度探索创新设计。设计师可以输入从复古皮革靴到未来感十足的运动鞋极速模特AI试穿，确保每一款新品都能商品图极速上架。
-   新鞋创意试穿：顾客在选购鞋靴时，难以全面体验心仪款式直接试穿。而新鞋创意试穿应用，顾客只需简单输入本人照片，就能“穿上”任何一款店铺新款鞋靴，直观感受外观搭配效果，大大提升了购物的便捷性和趣味性。
-   模特穿戴重绘：模特试穿能轻松更换模特展示的鞋靴款式，都能与模特的服装、背景完美融合，创造出多样化的时尚造型。这一过程无需重新拍摄，既节省成本又提高了效率。模特穿戴重绘都能帮助品牌快速响应市场变化。

### 模型概览

**模型名**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**计费单价**

**限流（含主账号与RAM子账号）**

**任务下发接口QPS限制**

**同时处理中任务数量**

shoemodel-v1

500张

目前仅供免费体验。

> 免费额度用完后不可调用，敬请关注后续动态。

2

1

## 快速开始

**输入限制**

模特模板图：

-   图片比例 ：图长边与短边的比例需在`[2:3, 3:2]` 范围内，推荐比例为`4:3`。
-   图片格式：JPEG，PNG，JPG，BMP，WEB，AVIF。
-   图片大小：建议不超过5M。

鞋靴多视角图：

-   图片比例：图长边与短边的比例需在`[2:3, 3:2]` 范围内，推荐与模特模板图一样，比例为`4:3`。
-   图片格式：JPEG，PNG，JPG，BMP，WEB，AVIF。
-   图片大小：建议不超过5M。
-   图片个数：多视角图片个数小于3。

URL地址：

-   不能包含中文字符。

**模特模板图（template\_image\_url）**

**鞋靴多视角图（shoe\_image\_url）**

**输出结果**

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809310.webp)

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809301.webp)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809309.png)

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

#### curl

**1、创建鞋靴布局重绘任务**

接口返回任务ID，可根据任务ID查询图像生成的结果。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "shoemodel-v1",
    "input": {
        "template_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E9%9E%8B%E9%9D%B4%E5%9B%BE.webp",
        "shoe_image_url": ["https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E9%9E%8B%E9%9D%B4temp.webp"]
    },
    "parameters": {
        "n": 1
    }
}'
```
**2、根据任务ID查询任务状态与结果**
```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X GET \
--header 'Authorization: Bearer <YOUR-DASHSCOPE-API-KEY>' \
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/13b1848b-5493-4c0e-8c44-xxxxxxxxxxxx
```

## 输入示例示范

### 正确输入示例

**模特模板图**

**鞋靴图**

**输出结果**

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809304.jpeg)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809306.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809308.png)

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809297.webp)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809300.jpeg)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809311.png)

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809298.webp)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809299.jpeg)![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809302.jpeg)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809307.png)

### 错误输入示例

**没有脚**

**脚部缺失or姿态非正常站立**

**膝盖缺失 or 鞋靴边界距离图片左右边界太近**

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809303.jpeg)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809312.jpeg)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809305.jpeg)

## API参考

API的输入输出参数，请参见[鞋靴模特](raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)。
