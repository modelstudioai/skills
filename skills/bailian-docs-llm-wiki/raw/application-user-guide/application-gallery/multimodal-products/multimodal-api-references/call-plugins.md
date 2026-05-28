# 调用插件

本文介绍如何在多模态交互中接入插件并在客户端调用。

## **插件简介**

多模态交互开发套件支持三种插件：

1.  **推荐插件**
    
    -   多模态交互套件预置的实用插件
        
    -   支持天气查询、万年历、股价查询等常见场景
        
    -   开箱即用，无需额外配置
        
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2517343571/p987781.png)
    
2.  **插件广场中的插件**
    
3.  **自定义插件**
    

插件广场和自定义插件介绍请参见[插件概述](https://help.aliyun.com/zh/model-studio/plug-in-overview)。

## **接入流程**

-   **推荐插件**：默认接入，取消勾选禁用。
    
-   **插件广场插件**：单击**添加**按钮接入。
    
-   **自定义插件**：
    
    1.  创建插件：详情请参见[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins)。
        
        注意，需要确保【创建插件】和【创建工具】两个步骤均完成并发布。如果您返回到多模态交互控制台，在自定义插件中无法选中自己刚创建的插件，可优先检查是否未完成【创建工具】并【发布】操作。
        
    2.  绑定插件：单击**添加**按钮绑定创建的插件（如“寝室公约查询工具”）。
        
        ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2517343571/p987782.png)
        

## **客户端调用插件**

-   **推荐插件**：SDK已集成，无需自行调用
    
-   **插件广场插件**：同自定义插件
    
-   **自定义插件**：通过 SDK 调用，在参数中设置插件中指定的变量值
    
    Java
    
    ```
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
    
    Python
    
    ```
    plugin_parm = {"article_index": "2"}
    user_defined_params = {"your_plugin_code": plugin_parm}
    biz_params = BizParams(user_defined_params=user_defined_params)
    ```
    
    Swift
    
    ```
    var pluginParam = ["article_index" : 2]
    var userDefinedParams = ["your_plugin_code" : pluginParam]
    
    multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
      bizBuilder in
      bizBuilder.userDefinedParams = userDefinedParams
    })
    ```
    

## **插件参数说明**

**一级参数**

**二级参数**

**三级参数**

**四级参数**

**参数说明**

biz\_params

多模请求参数中的biz\_params

user\_defined\_params

透传用户自定义参数

your\_plugin\_code

导入的百炼应用 id，参考[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins#::text=%E8%B0%83%E7%94%A8%E5%B7%A5%E5%85%B7%E3%80%82-,%E8%8E%B7%E5%8F%96%E5%B7%A5%E5%85%B7ID,-%E5%B7%A5%E5%85%B7ID%E7%94%A8%E4%BA%8E)获取工具ID

your\_plugin\_param

类型为 Object

对应与插件配置的信息

示例：

```
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
