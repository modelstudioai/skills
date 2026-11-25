# 调用插件

本文介绍如何在多模态交互中接入插件并在客户端调用。

<a id="插件简介"></a>

<a id="54aa3cb8f4pnk"></a>

## 插件简介

多模态交互开发套件支持三种插件：

1.  **推荐插件**
    
    -   多模态交互套件预置的实用插件
    -   支持天气查询、万年历、股价查询等常见场景
    -   开箱即用，无需额外配置
    
    此外还包括**油价查询**、**金价查询**、**银价查询**、**汇率查询**、**新闻资讯**、**路线规划**和**本地生活**等插件，所有推荐插件默认已启用。
    
2.  **插件广场中的插件**
3.  **自定义插件**

插件广场和自定义插件介绍请参见[插件概述](../application-user-guide/plug-in/plug-in-overview.md)。

<a id="接入流程"></a>

<a id="4270554ad2fn8"></a>

## 接入流程

-   **推荐插件**：默认接入，取消勾选禁用。
    
-   **插件广场插件**：单击**添加**按钮接入。
    
-   **自定义插件**：
    
    1.  创建插件：详情请参见[自定义插件](../application-user-guide/plug-in/custom-plug-ins.md)。
        
        注意，需要确保【创建插件】和【创建工具】两个步骤均完成并发布。如果您返回到多模态交互控制台，在自定义插件中无法选中自己刚创建的插件，可优先检查是否未完成【创建工具】并【发布】操作。
        
    2.  绑定插件：单击**添加**按钮绑定创建的插件（如“寝室公约查询工具”）。
        
        在**选择插件**面板中，切换到**自定义插件**页签即可找到已创建的插件。
        

<a id="客户端调用插件"></a>

<a id="5fd50e389d3i6"></a>

## 客户端调用插件

-   **推荐插件**：SDK已集成，无需自行调用
-   **插件广场插件**：同自定义插件
-   **自定义插件**：通过 SDK 调用，在参数中设置插件中指定的变量值

<a id="code-block"></a>

```java
//Java & Android
HashMap<String, Object> pluginParams = new HashMap<>();
pluginParams.put("article_index",2);
HashMap<String, Object> userDefinedParams = new HashMap<>();
userDefinedParams.put("your_plugin_code",pluginParams);
MultiModalRequestParam.BizParams bizParams = MultiModalRequestParam.BizParams
   .builder()
   .userDefinedParams(userDefinedParams)
   .build();
```

<a id="code-block-2"></a>

```python
plugin_parm = {"article_index": "2"}
user_defined_params = {"your_plugin_code": plugin_parm}
biz_params = BizParams(user_defined_params=user_defined_params)
```

<a id="code-block-3"></a>

```swift
var pluginParam = ["article_index" : 2]
var userDefinedParams = ["your_plugin_code" : pluginParam]
multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
  bizBuilder in
  bizBuilder.userDefinedParams = userDefinedParams
})
```

<a id="插件参数说明"></a>

<a id="8a9725f7cdsoc"></a>

## 插件参数说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>三级参数</strong></p></th><th><p><strong>四级参数</strong></p></th><th><p><strong>参数说明</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>biz_params</p></td><td></td><td></td><td></td><td><p>多模请求参数中的biz_params</p></td></tr><tr><td rowspan="3"><p>user_defined_params</p></td><td></td><td></td><td><p>透传用户自定义参数</p></td></tr><tr><td rowspan="2"><p>your_plugin_code</p></td><td></td><td><p>导入的百炼应用 id，参考<a href="../application-user-guide/plug-in/custom-plug-ins.md">自定义插件</a>获取工具ID</p></td></tr><tr><td><p>your_plugin_param</p></td><td><p>类型为 Object</p><p>对应与插件配置的信息</p></td></tr></tbody></table>

示例：

<a id="code-block-4"></a>

```json
{
    "biz_params": {
        "user_defined_params": {
            "${your_plugin_code}": {
                "article_index": 2
            }
        }
    }
}
```
