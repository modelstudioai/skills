# 全妙云存储（OSS）设置指南

<a id="名词定义"></a>

<a id="ece1bb6d92teh"></a>

## 名词定义

-   云存储（OSS）

阿里云对象存储服务（Object Storage Service），本文特指阿里云OSS。

-   OSS授权设置

指在全妙控制台中完成“RAM角色授权”+“Bucket参数配置”的完整流程，使全妙具备对指定OSS Bucket子目录`/aimiaobi`的安全读写能力。

> **说明**
>
> 妙搜默认使用其自有存储，启用OSS为可选增强能力，妙搜的使用指南请参考《[妙搜](ai-miaosou-8a30b5956dc67e7e.md)》。

<a id="为什么需要oss授权设置"></a>

<a id="a3e43fb25ahqu"></a>

## 为什么需要OSS授权设置？

| 场景 | 说明 |
| --- | --- |
| 安全合规 | 敏感业务数据需留存于客户自有云环境，满足等保、行业监管或内部IT策略要求。 |
| 资源可控 | 客户完全掌握存储权限、生命周期、访问日志与审计能力，规避第三方存储依赖风险。 |
| 成本优化 | 复用企业已购OSS资源（如包年包月容量、CDN回源带宽），降低长期存储与流量成本。 |

<a id="oss授权设置全流程"></a>

<a id="2f642f2139qxv"></a>

## OSS授权设置全流程

<a id="步骤1-准备oss资源"></a>

<a id="172680a5240ur"></a>

### 步骤1：准备OSS资源

<a id="①-开通oss服务"></a>

<a id="5c0696e98f0i7"></a>

#### ① 开通OSS服务

登录[OSS控制台](https://oss.console.aliyun.com/)，确保账号已开通OSS服务。

<a id="②-创建bucket"></a>

<a id="24813ede21h9j"></a>

#### ② 创建Bucket

新Bucket：推荐地域：`cn-beijing`（华北2），也可以复用已有Bucket。

<a id="③-创建根目录"></a>

<a id="6d2935ee48ep5"></a>

#### ③ 创建根目录

在Bucket内手动创建路径：`/aimiaobi`。

> **说明**
>
> 此步骤必须存在！全妙仅被授予该前缀下文件的读写权限（最小权限原则）。

<a id="④-配置cors-跨域"></a>

<a id="dac201d19cyy1"></a>

#### ④ 配置CORS（跨域）

> **说明**
>
> 此步骤必须配置，否则控制台预览/上传将失败。

-   入口：oss控制台 > Bucket > 数据安全 > CORS设置，也可以按以下格式拼接地址访问（将 {region} 与 {bucket} 替换为实际值）：`https://oss.console.aliyun.com/bucket/oss-{region}/{bucket}/data-security/cors`；
-   CORS规则配置（严格按此填写）。

| 字段 | 值 | 说明 |
| --- | --- | --- |
| 来源（Origin） | `https://aimiaobi.console.aliyun.com` | 全妙控制台域名（不可省略协议） |
| 允许Methods | `GET, PUT, POST, DELETE, HEAD` | 全选 |
| 允许Headers | `*` | 支持任意请求头（含`Authorization`, `Content-Type`等） |
| 其他 |  | 默认即可 |

<a id="步骤2-妙搜中授权与配置"></a>

<a id="adf1ba90d5ioc"></a>

### 步骤2：妙搜中授权与配置

进入[妙搜控制台](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_search#/searchSystemConfig?activeKey=storageSetting)，进入**配置**，在云存储设置中进行授权和配置。

<a id="授权-ram角色绑定"></a>

<a id="1236283b55irf"></a>

#### 授权（RAM角色绑定）

点击 “授权”按钮 ：授权成功后按钮变为“已授权”，全妙有所有bucket下/aimiaobi目录的读写权限，但此时文件仍上传至全妙自有存储（因尚未配置Bucket参数）。

<a id="设置-绑定bucket"></a>

<a id="6ab56686c353b"></a>

#### 设置（绑定Bucket）

-   填写以下2项并点击 “保存”：
    
    -   Endpoint：OSS服务地址（如 `oss-cn-shanghai.aliyuncs.com`）；
    -   Bucket名称：您创建的Bucket名（如`quanmiao-xxxx`）；
-   保存时自动执行：向 `/aimiaobi`下上传测试文件并校验读写，显示 “验证通过” → 表示OSS连通性、权限、CORS均正常。
    

<a id="取消oss授权配置"></a>

<a id="71aeb8f4a7c16"></a>

## 取消OSS授权配置

进入[RAM访问控制>角色](https://ram.console.aliyun.com/roles)，筛选[AliyunServiceRoleForAIMiaoBiAccessingOss](https://ram.console.aliyun.com/roles/detail?roleName=AliyunServiceRoleForAIMiaoBiAccessingOss)角色名称，进行删除。

<a id="无活跃订单"></a>

<a id="2ddc301c29vwf"></a>

## 无活跃订单

在阿里云RAM控制台删除全妙关联的RAM角色：RAM访问控制 > 角色 > 搜索“`AliyunServiceRoleForAIMiaoBiAccessingOss`” > 删除角色。

<a id="存在有效订单"></a>

<a id="32cfab4b23r55"></a>

## 存在有效订单

禁止自行删除RAM角色！（避免影响历史数据）。

请联系全妙产研支持：

-   钉钉群号：166725003249（注明：【OSS解绑】+ aliUid + 原因）；
-   产研将为您：打标为可删除，之后同上方式可以删除。

<a id="关键使用限制与行为说明"></a>

<a id="7e18be0482s2b"></a>

## 关键使用限制与行为说明

| 功能点 | 行为逻辑 | 补充说明 |
| --- | --- | --- |
| 文件上传 | 新增文件直传OSS `/aimiaobi/` 下，全妙仅存元数据（URL、大小等）。 | 不占用全妙存储配额 |
| 文件删除 | 强一致性同步删除：<br><br>在控制台删除文档/数据集时，同时删除OSS中对应文件。 | 删除不可逆！ |
| 文件下载/预览 | 通过全妙后端代理跳转，或生成OSS临时STS签名URL（取决于安全策略）。 |  |
| 目录隔离 | 全妙仅能访问 `/aimiaobi/` 及其子路径，无法列出Bucket其他目录，无法删除/修改其他路径文件。 | 符合最小权限安全设计 |
