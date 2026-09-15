# 人物实例分割

人物实例分割可以识别出图像中的不同人物对象，并画出每个对象边界的像素级掩码。

**重要**

-   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   image-instance-segmentation 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费。

## 基本介绍

人物实例分割运用了检测和分割技术，不仅能够在图像中识别出不同的对象，而且还能准确地画出每一个对象边界的像素级掩码（mask）。

推荐配合使用[图像擦除补全](raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)接口来进行AI人体消除，选择完整人体mask区域来消除一个或多个人物。

### 使用场景

-   人像主体抠图：人体分割通过将摄影主体人物从背景中分割出来，将背景虚化，以达到大光圈浅景深效果，突出人物主体。
-   证件照制作：上传或拍摄一张多人生活照，可将人物精细地分割出来，再搭配擦除补全处理能力，最终制作出单人证件照。
-   营销广告制作：在广告制作中，需要将产品图片与特定场景或人物分割，分离原始图片中可能包含不需要的前景或背景元素。

### 特色优势

-   适应复杂背景：即使人物处于复杂背景环境，依然可以将人体准确地从背景中分割出来。
-   企业级平台服务提供在高并发、大流量下的稳定写真图片生成响应，可直接调用的简单推理API接口。

### 模型概览

**模型名**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**计费单价**

**限流（含主账号与RAM子账号）**

**任务下发接口QPS限制**

**同时处理中任务数量**

image-instance-segmentation

500张

目前仅供免费体验。

> 免费额度用完后不可调用，敬请关注后续动态。

2

1

## 快速开始

图像输入限制：

-   图片分辨率：可支持输入分辨率范围：单边不小于512且不超过4096。
-   图片格式：JPEG，PNG，JPG，BMP，WEBP。
-   图片大小：不超过10M。
-   URL地址中不能包含中文字符。

**输入图像**

**输出结果1：像素级掩码图像**

**输出结果2：可视化图像**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p841095.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p841096.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7854345271/p844284.png)

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

#### curl

**1、创建人物实例分割任务**

接口返回任务ID，可根据任务ID查询图像生成的结果

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
    "model": "image-instance-segmentation",
    "input": {
        "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E4%BA%BA%E5%83%8F%E5%88%86%E5%89%B2.png"
    },
    "parameters": {}
}'
```
**2、根据任务ID查询结果**
```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{your_task_id} \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
```

## API参考

API的输入输出参数，请参见[人物实例分割](raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)。
