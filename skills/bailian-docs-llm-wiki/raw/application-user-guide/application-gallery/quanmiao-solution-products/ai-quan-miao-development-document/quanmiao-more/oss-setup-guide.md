# 全妙云存储（OSS）设置指南

## **名词定义**

-   云存储（OSS）
    

阿里云对象存储服务（Object Storage Service），本文特指阿里云OSS。

-   OSS授权设置
    

指在全妙控制台中完成「RAM角色授权」+「Bucket参数配置」的完整流程，使全妙具备对指定OSS Bucket子目录`/aimiaobi`的安全读写能力。

**说明**

妙搜默认使用其自有存储，启用OSS为可选增强能力，妙搜的使用指南请参考《[妙搜](https://help.aliyun.com/zh/model-studio/ai-miaosou)》。

## 为什么需要OSS授权设置？

**场景**

**说明**

安全合规

敏感业务数据需留存于客户自有云环境，满足等保、行业监管或内部IT策略要求。

资源可控

客户完全掌握存储权限、生命周期、访问日志与审计能力，规避第三方存储依赖风险。

成本优化

复用企业已购OSS资源（如包年包月容量、CDN回源带宽），降低长期存储与流量成本。

## OSS授权设置全流程

### **步骤1：准备OSS资源**

#### **① 开通OSS服务**

登录[OSS控制台](https://oss.console.aliyun.com/)，确保账号已开通OSS服务。

#### **② 创建Bucket**

新Bucket：推荐地域：`cn-beijing`（华北2），也可以复用已有Bucket。

#### **③ 创建根目录**

在Bucket内手动创建路径：`/aimiaobi`。

**说明**

此步骤必须存在！全妙仅被授予该前缀下文件的读写权限（最小权限原则）。

#### **④ 配置CORS（跨域）**

**说明**

此步骤必须配置，否则控制台预览/上传将失败。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9736823771/p1059007.png)

-   入口：oss控制台 > Bucket > 数据安全 > CORS设置，也可以点击下面的链接进行访问：[https://oss.console.aliyun.com/bucket/oss-{region}/{bucket}/data-security/cors](https://oss.console.aliyun.com/bucket/oss-{region}/{bucket}/data-security/cors)；
    
-   CORS规则配置（严格按此填写）：
    

**字段**

**值**

**说明**

来源（Origin）

`https://aimiaobi.console.aliyun.com`

全妙控制台域名（不可省略协议）

允许Methods

`GET, PUT, POST, DELETE, HEAD`

全选

允许Headers

`*`

支持任意请求头（含`Authorization`, `Content-Type`等）

其他

默认即可

### **步骤2：妙搜中授权与配置**

进入[妙搜控制台](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_search#/searchSystemConfig?activeKey=storageSetting)，进入**配置**，在云存储设置中进行授权和配置。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9736823771/p1057658.png)

#### **① 授权（RAM角色绑定）**

点击 「授权」按钮 ：授权成功后按钮变为「已授权」，全妙有所有bucket下/aimiaobi目录的读写权限，但此时文件仍上传至全妙自有存储（因尚未配置Bucket参数）。

#### **② 设置（绑定Bucket）**

-   填写以下2项并点击 「保存」：
    
    -   Endpoint：OSS服务地址（如 `oss-cn-shanghai.aliyuncs.com`）；
        
    -   Bucket名称：您创建的Bucket名（如`quanmiao-xxxx`）；
        
-   保存时自动执行：向 `/aimiaobi` 下上传测试文件并校验读写，显示 「验证通过」 → 表示OSS连通性、权限、CORS均正常。
    

## 取消OSS授权配置

进入[RAM访问控制>角色](https://ram.console.aliyun.com/roles)，筛选[AliyunServiceRoleForAIMiaoBiAccessingOss](https://ram.console.aliyun.com/roles/detail?roleName=AliyunServiceRoleForAIMiaoBiAccessingOss)角色名称，进行删除。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9736823771/p1059016.png)

## **无活跃订单**

在阿里云RAM控制台删除全妙关联的RAM角色：RAM访问控制 > 角色 > 搜索“`AliyunServiceRoleForAIMiaoBiAccessingOss`” > 删除角色。

## **存在有效订单**

禁止自行删除RAM角色！（避免影响历史数据）。

请联系全妙产研支持：

-   钉钉群号：166725003249（注明：【OSS解绑】+ aliUid + 原因）；
    
-   产研将为您：打标为可删除，之后同上方式可以删除。
    

## 关键使用限制与行为说明

**功能点**

**行为逻辑**

**补充说明**

文件上传

新增文件直传OSS `/aimiaobi/` 下，全妙仅存元数据（URL、大小等）。

不占用全妙存储配额

文件删除

强一致性同步删除：

在控制台删除文档/数据集时，同时删除OSS中对应文件。

删除不可逆！

文件下载/预览

通过全妙后端代理跳转，或生成OSS临时STS签名URL（取决于安全策略）。

目录隔离

全妙仅能访问 `/aimiaobi/` 及其子路径，无法列出Bucket其他目录，无法删除/修改其他路径文件。

符合最小权限安全设计
