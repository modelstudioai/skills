# PodcastTaskResultQuery - 播客任务结果查询

ai播客生成任务结果查询。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AIPodcast/2025-02-28/PodcastTaskResultQuery)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AIPodcast/2025-02-28/PodcastTaskResultQuery)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

aipodcast:PodcastTaskResultQuery

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /podcast/task HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

当前请求所使用的百炼业务空间 id

llm-ep8ba0dr6seiddri

taskId

string

是

任务唯一标识

63c4e0eaab3b4c0db208ecafa990e8d1

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

响应状态码。

"success"

message

string

响应消息。

"success"

requestId

string

请求 id，用于追溯 API 调用链路。

C38F034D-7F36-531C-95AC-0C752F80E840

success

boolean

是否成功：true 成功，false 失败

True

httpStatusCode

string

HTTP 状态码

200

data

object

响应数据。

taskId

string

任务唯一标识

63c4e0eaab3b4c0db208ecafa990e8d1

taskStatus

string

任务状态。

-   PENDING：待执行
-   RUNNING：执行中
-   SUCCEEDED：成功
-   INVALID：失效
-   FAILED：失败
-   UNKNOWN： 未知

SUCCEEDED

script

string

播客文字稿(未交互增强)

"\[{\\"text\\": \\"听众朋友们，晚上好！今天咱们聊聊最近大家都很关心的一个话题——甲流来袭，我们该怎么应对？\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"嗯，这个话题确实挺重要。甲流听起来有点吓人，但其实只要科学防护，就不用太担心。\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"没错，先给大家科普一下，甲流全名叫甲型流感，是由甲型流感病毒感染引起的流行性感冒。跟普通感冒比起来，它的症状更重，传播也更快。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"哦？那具体都有哪些症状呢？我记得好像会发烧吧。\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"对的，高烧是甲流最常见的症状之一，体温可能高达39到40度。除了发烧，还会有头痛、全身肌肉和关节疼痛、乏力、食欲不振等症状。有些人甚至会出现恶心、呕吐的情况。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"听起来确实不太好受。不过婴儿的症状是不是会稍微不一样？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"是的，婴儿可能会表现为高烧、烦躁、哭闹增加，还有吃奶减少等。所以家长要特别注意观察孩子的状态。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"嗯，说到这，我突然想到一个问题：甲流是怎么传播的呢？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"主要通过呼吸道传播和接触传播。比如近距离接触甲流病人或者高度疑似病人后，就可能被感染。另外，患者的分泌物也可能携带病毒，直接或间接接触这些分泌物也会有风险。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"哦，原来如此。那易感人群有哪些呢？是不是老年人和小孩更容易中招？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"没错，老人、孕妇、小孩都是易感人群。此外，患有慢性疾病、肥胖或者免疫功能低下的人群也要格外小心。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"听你这么一说，感觉预防真的很重要啊。那有没有什么有效的预防措施呢？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"当然有！最有效的方法就是接种疫苗。每年9到10月份接种流感疫苗，保护效力可以持续到冬春流感高发季节。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"嗯，除了打疫苗，还有什么其他办法吗？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"保持良好的卫生习惯也很重要。比如勤洗手，尽量避免用手接触眼、鼻、口。同时，避免在拥挤的场所逗留，减少人际接触。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"嗯，这点我特别赞同。现在很多人都习惯了戴口罩，这其实也是个很好的防护措施。\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"没错，戴口罩能有效阻断飞沫传播。另外，增强免疫力也很关键。保持充足的睡眠、均衡的饮食和适量的运动都能帮助身体更好地抵抗病毒。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"听你这么一说，感觉生活中的小细节真的很重要。比如咳嗽或打喷嚏时，用纸巾、手肘遮住口鼻，就能减少病毒传播。\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"对，还有别忘了保持环境清洁和通风。家里、教室每天勤开窗通风，必要时进行消毒。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"看来这些看似简单的小事，其实都能起到大作用。那万一真的不幸中招了，该怎么办呢？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"如果确诊是甲型流感，一定要隔离、卧床休息，并遵医嘱用药。比如磷酸奥司他韦胶囊就是一种常用的抗病毒药物。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"哦，原来还有专门针对甲流的药。不过如果症状比较严重，比如持续高烧或者呼吸困难，那就得赶紧去医院了。\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"没错，千万别拖延病情。医院可以排查是否有并发症，比如肺炎之类的。总之，早发现、早治疗很重要。\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"总结一下，甲流虽然可怕，但只要我们做好防护，及时就医，就没啥好怕的。大家记住了吗？\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"记住了！接种疫苗、勤洗手、戴口罩、增强免疫力，还有必要时及时就医。希望大家都能健健康康地度过这个季节！\\", \\"speaker\\": \\"speaker-1\\"}, {\\"text\\": \\"好了，今天的节目就到这里。感谢大家收听，我们下期再见！\\", \\"speaker\\": \\"speaker-2\\"}, {\\"text\\": \\"再见！\\", \\"speaker\\": \\"speaker-1\\"}\]"

resultUrl

any

以 URL 形式返回的解析结果，链接有效期为一小时。

{"audio":"http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/audio.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748853849&Signature=e1KlRgmjAjuUkPVWIEhoRbn4X0w%3D","script":"http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/script.txt?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748853511&Signature=th5sI%2BB1FZuQ6tRLg4qGGX1fevI%3D"}

extraResult

any

播客分段音频等详细信息

extraResult 详细结构描述如下

```
- extraResult.segment(list[float]):分段音频时长坐标
- extraResult.segmentDetails.index(int):分段音频下标
- extraResult.segmentDetails.time(list[float]):分段音频位置
- extraResult.segmentDetails.audioSegmentUrl(str):分段音频可下载链接，有效期一小时
- extraResult.segmentDetails.script.speaker(str):分段音频主理人
- extraResult.segmentDetails.script.text(str):分段音频文字稿
```

{ "segment": \[ \[ 0.0, 6370.0 \], \[ 6370.0, 15020.0 \], \[ 15020.0, 26071.791 \], \[ 26071.791, 31001.791 \], \[ 31001.791, 45646.582 \], \[ 45646.582, 50816.582 \], \[ 50816.582, 59501.418 \], \[ 59501.418, 63631.418 \], \[ 63631.418, 77161.25 \], \[ 77161.25, 84691.25 \], \[ 84691.25, 93623.086 \], \[ 93623.086, 99233.086 \], \[ 99233.086, 108894.875 \], \[ 108894.875, 111864.875 \], \[ 111864.875, 121678.664 \], \[ 121678.664, 128448.664 \], \[ 128448.664, 139774.45 \], \[ 139774.45, 149824.45 \], \[ 149824.45, 157966.25 \], \[ 157966.25, 164576.25 \], \[ 164576.25, 175432.08 \], \[ 175432.08, 184482.08 \], \[ 184482.08, 192451.88 \], \[ 192451.88, 199781.88 \], \[ 199781.88, 208151.88 \], \[ 208151.88, 212601.88 \], \[ 212601.88, 213131.88 \] \], "segmentDetails": \[ { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_0.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=cWk2X%2B7MtbIEm%2Fu1mwVts59hpwU%3D", "index": 0, "time": \[ 0.0, 6370.0 \], "script": { "speaker": "speaker-1", "text": "听众朋友们，晚上好！今天咱们聊聊最近大家都很关心的一个话题——甲流来袭，我们该怎么应对？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_1.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=CFGULg%2FJ8I3htf0YvVL5mz7FLXg%3D", "index": 1, "time": \[ 6370.0, 15020.0 \], "script": { "speaker": "speaker-2", "text": "嗯，这个话题确实挺重要。甲流听起来有点吓人，但其实只要科学防护，就不用太担心。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_2.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=Q2Ck9DLRqsvJ1Bt6aqMh0rnPPDQ%3D", "index": 2, "time": \[ 15020.0, 26071.791 \], "script": { "speaker": "speaker-1", "text": "没错，先给大家科普一下，甲流全名叫甲型流感，是由甲型流感病毒感染引起的流行性感冒。（对）跟普通感冒比起来，它的症状更重，传播也更快。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_3.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=vPwoJQnhKv2Ti4aovV6v3lP4V5w%3D", "index": 3, "time": \[ 26071.791, 31001.791 \], "script": { "speaker": "speaker-2", "text": "哦？那具体都有哪些症状呢？我记得好像会发烧吧。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_4.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=fUh04j4iLyYG4GV5wQ1f5GkFvJE%3D", "index": 4, "time": \[ 31001.791, 45646.582 \], "script": { "speaker": "speaker-1", "text": "对的，高烧是甲流最常见的症状之一，体温可能高达39到40度。（嗯）除了发烧，还会有头痛、全身肌肉和关节疼痛、乏力、食欲不振等症状。有些人甚至会出现恶心、呕吐的情况。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_5.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=v5c0d%2Bk4OmjmRRFVCKZ5JhDOq5o%3D", "index": 5, "time": \[ 45646.582, 50816.582 \], "script": { "speaker": "speaker-2", "text": "听起来确实不太好受。不过婴儿的症状是不是会稍微不一样？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_6.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=ZeyAxNn8wbRFXK4qXPJMKKGhIl0%3D", "index": 6, "time": \[ 50816.582, 59501.418 \], "script": { "speaker": "speaker-1", "text": "是的，婴儿可能会表现为高烧、烦躁、哭闹增加，还有吃奶减少等。（确实）所以家长要特别注意观察孩子的状态。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_7.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854445&Signature=UEyc%2BbAqgIa1C3SS4EjtNegTDTg%3D", "index": 7, "time": \[ 59501.418, 63631.418 \], "script": { "speaker": "speaker-2", "text": "嗯，说到这，我突然想到一个问题：甲流是怎么传播的呢？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_8.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=JYlAsSnLJNMFDEv9Bm5hSf4SrNY%3D", "index": 8, "time": \[ 63631.418, 77161.25 \], "script": { "speaker": "speaker-1", "text": "主要通过呼吸道传播和接触传播。（没错）比如近距离接触甲流病人或者高度疑似病人后，就可能被感染。另外，患者的分泌物也可能携带病毒，直接或间接接触这些分泌物也会有风险。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_9.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=eHG1QMbfsSSqfHwAD79Xs531kFw%3D", "index": 9, "time": \[ 77161.25, 84691.25 \], "script": { "speaker": "speaker-2", "text": "哦，原来如此。那易感人群有哪些呢？是不是老年人和小孩更容易中招？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_10.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=rElcCYlOaChj%2BJWT94c7%2F%2FMlTUo%3D", "index": 10, "time": \[ 84691.25, 93623.086 \], "script": { "speaker": "speaker-1", "text": "没错，老人、孕妇、小孩都是易感人群。（真的）此外，患有慢性疾病、肥胖或者免疫功能低下的人群也要格外小心。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_11.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=dBjOIrNqHSiF3RCrbsWyLtrE6Ow%3D", "index": 11, "time": \[ 93623.086, 99233.086 \], "script": { "speaker": "speaker-2", "text": "听你这么一说，感觉预防真的很重要啊。那有没有什么有效的预防措施呢？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_12.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=EJ0qCENMhqIUEu6UZ0RTP0cdibQ%3D", "index": 12, "time": \[ 99233.086, 108894.875 \], "script": { "speaker": "speaker-1", "text": "当然有！最有效的方法就是接种疫苗。（对）每年9到10月份接种流感疫苗，保护效力可以持续到冬春流感高发季节。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_13.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=nH02zWlwtrLK2fcskFbRvuMTD3s%3D", "index": 13, "time": \[ 108894.875, 111864.875 \], "script": { "speaker": "speaker-2", "text": "嗯，除了打疫苗，还有什么其他办法吗？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_14.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=9y3D2UGy6zg77gFWP4qFtHkF5S4%3D", "index": 14, "time": \[ 111864.875, 121678.664 \], "script": { "speaker": "speaker-1", "text": "保持良好的卫生习惯也很重要。比如勤洗手，尽量避免用手接触眼、鼻、口。（没错）同时，避免在拥挤的场所逗留，减少人际接触。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_15.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854446&Signature=EbwEURP7u9HpwrsrPC2Thwd4XUg%3D", "index": 15, "time": \[ 121678.664, 128448.664 \], "script": { "speaker": "speaker-2", "text": "嗯，这点我特别赞同。现在很多人都习惯了戴口罩，这其实也是个很好的防护措施。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_16.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=4rj5XQD0SaspVCj7QmGFrIGyACA%3D", "index": 16, "time": \[ 128448.664, 139774.45 \], "script": { "speaker": "speaker-1", "text": "没错，戴口罩能有效阻断飞沫传播。另外，增强免疫力也很关键。（嗯）保持充足的睡眠、均衡的饮食和适量的运动都能帮助身体更好地抵抗病毒。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_17.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=1aGlxcVI8r3ac7kY%2FHAt2%2Bg2Jss%3D", "index": 17, "time": \[ 139774.45, 149824.45 \], "script": { "speaker": "speaker-2", "text": "听你这么一说，感觉生活中的小细节真的很重要。比如咳嗽或打喷嚏时，用纸巾、手肘遮住口鼻，就能减少病毒传播。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_18.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=41GmphAH1k2hwtKm5xG5HU8sZYU%3D", "index": 18, "time": \[ 149824.45, 157966.25 \], "script": { "speaker": "speaker-1", "text": "对，还有别忘了保持环境清洁和通风。（确实）家里、教室每天勤开窗通风，必要时进行消毒。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_19.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=1yD7PvQwmJCFtDVZxiBSCgxFQWE%3D", "index": 19, "time": \[ 157966.25, 164576.25 \], "script": { "speaker": "speaker-2", "text": "看来这些看似简单的小事，其实都能起到大作用。那万一真的不幸中招了，该怎么办呢？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_20.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=D%2BVKscQXjtyzbNx5NJhx%2Fyny1qI%3D", "index": 20, "time": \[ 164576.25, 175432.08 \], "script": { "speaker": "speaker-1", "text": "如果确诊是甲型流感，一定要隔离、卧床休息，并遵医嘱用药。（没错）比如磷酸奥司他韦胶囊就是一种常用的抗病毒药物。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_21.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=Ugt6%2FUFdc7ACT%2BFxJm4Tk8VOX84%3D", "index": 21, "time": \[ 175432.08, 184482.08 \], "script": { "speaker": "speaker-2", "text": "哦，原来还有专门针对甲流的药。不过如果症状比较严重，比如持续高烧或者呼吸困难，那就得赶紧去医院了。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_22.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=YJy3rQ2cpGwjtW%2BSzehQscSFicg%3D", "index": 22, "time": \[ 184482.08, 192451.88 \], "script": { "speaker": "speaker-1", "text": "没错，千万别拖延病情。医院可以排查是否有并发症，比如肺炎之类的。（对）总之，早发现、早治疗很重要。" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_23.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854447&Signature=5WvLaj3cCmK5m%2FAS8EiIbaAgxYs%3D", "index": 23, "time": \[ 192451.88, 199781.88 \], "script": { "speaker": "speaker-2", "text": "总结一下，甲流虽然可怕，但只要我们做好防护，及时就医，就没啥好怕的。大家记住了吗？" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_24.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854448&Signature=H4gi%2B%2BUJ%2BJ36rjZeUecTsqFjTqY%3D", "index": 24, "time": \[ 199781.88, 208151.88 \], "script": { "speaker": "speaker-1", "text": "记住了！接种疫苗、勤洗手、戴口罩、增强免疫力，还有必要时及时就医。希望大家都能健健康康地度过这个季节！" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_25.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854448&Signature=oGTU2Ki3FkmV2hvL3sPFVM7ZPGI%3D", "index": 25, "time": \[ 208151.88, 212601.88 \], "script": { "speaker": "speaker-2", "text": "好了，今天的节目就到这里。感谢大家收听，我们下期再见！" } }, { "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment\_26.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ\*\*\*\*&Expires=1748854448&Signature=N4lXSxOmRSjsRFounST8hBM3FnY%3D", "index": 26, "time": \[ 212601.88, 213131.88 \], "script": { "speaker": "speaker-1", "text": "再见！" } } \] }

resultUrl 中 script 返回的内容为交互增强后的播客稿内容与 script 参数内容不一致。

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "C38F034D-7F36-531C-95AC-0C752F80E840",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "63c4e0eaab3b4c0db208ecafa990e8d1\n",
    "taskStatus": "SUCCEEDED",
    "script": [
      {
        "text": "听众朋友们，晚上好！今天咱们聊聊最近大家都很关心的一个话题——甲流来袭，我们该怎么应对？",
        "speaker": "speaker-1"
      },
      {
        "text": "嗯，这个话题确实挺重要。甲流听起来有点吓人，但其实只要科学防护，就不用太担心。",
        "speaker": "speaker-2"
      },
      {
        "text": "没错，先给大家科普一下，甲流全名叫甲型流感，是由甲型流感病毒感染引起的流行性感冒。跟普通感冒比起来，它的症状更重，传播也更快。",
        "speaker": "speaker-1"
      },
      {
        "text": "哦？那具体都有哪些症状呢？我记得好像会发烧吧。",
        "speaker": "speaker-2"
      },
      {
        "text": "对的，高烧是甲流最常见的症状之一，体温可能高达39到40度。除了发烧，还会有头痛、全身肌肉和关节疼痛、乏力、食欲不振等症状。有些人甚至会出现恶心、呕吐的情况。",
        "speaker": "speaker-1"
      },
      {
        "text": "听起来确实不太好受。不过婴儿的症状是不是会稍微不一样？",
        "speaker": "speaker-2"
      },
      {
        "text": "是的，婴儿可能会表现为高烧、烦躁、哭闹增加，还有吃奶减少等。所以家长要特别注意观察孩子的状态。",
        "speaker": "speaker-1"
      },
      {
        "text": "嗯，说到这，我突然想到一个问题：甲流是怎么传播的呢？",
        "speaker": "speaker-2"
      },
      {
        "text": "主要通过呼吸道传播和接触传播。比如近距离接触甲流病人或者高度疑似病人后，就可能被感染。另外，患者的分泌物也可能携带病毒，直接或间接接触这些分泌物也会有风险。",
        "speaker": "speaker-1"
      },
      {
        "text": "哦，原来如此。那易感人群有哪些呢？是不是老年人和小孩更容易中招？",
        "speaker": "speaker-2"
      },
      {
        "text": "没错，老人、孕妇、小孩都是易感人群。此外，患有慢性疾病、肥胖或者免疫功能低下的人群也要格外小心。",
        "speaker": "speaker-1"
      },
      {
        "text": "听你这么一说，感觉预防真的很重要啊。那有没有什么有效的预防措施呢？",
        "speaker": "speaker-2"
      },
      {
        "text": "当然有！最有效的方法就是接种疫苗。每年9到10月份接种流感疫苗，保护效力可以持续到冬春流感高发季节。",
        "speaker": "speaker-1"
      },
      {
        "text": "嗯，除了打疫苗，还有什么其他办法吗？",
        "speaker": "speaker-2"
      },
      {
        "text": "保持良好的卫生习惯也很重要。比如勤洗手，尽量避免用手接触眼、鼻、口。同时，避免在拥挤的场所逗留，减少人际接触。",
        "speaker": "speaker-1"
      },
      {
        "text": "嗯，这点我特别赞同。现在很多人都习惯了戴口罩，这其实也是个很好的防护措施。",
        "speaker": "speaker-2"
      },
      {
        "text": "没错，戴口罩能有效阻断飞沫传播。另外，增强免疫力也很关键。保持充足的睡眠、均衡的饮食和适量的运动都能帮助身体更好地抵抗病毒。",
        "speaker": "speaker-1"
      },
      {
        "text": "听你这么一说，感觉生活中的小细节真的很重要。比如咳嗽或打喷嚏时，用纸巾、手肘遮住口鼻，就能减少病毒传播。",
        "speaker": "speaker-2"
      },
      {
        "text": "对，还有别忘了保持环境清洁和通风。家里、教室每天勤开窗通风，必要时进行消毒。",
        "speaker": "speaker-1"
      },
      {
        "text": "看来这些看似简单的小事，其实都能起到大作用。那万一真的不幸中招了，该怎么办呢？",
        "speaker": "speaker-2"
      },
      {
        "text": "如果确诊是甲型流感，一定要隔离、卧床休息，并遵医嘱用药。比如磷酸奥司他韦胶囊就是一种常用的抗病毒药物。",
        "speaker": "speaker-1"
      },
      {
        "text": "哦，原来还有专门针对甲流的药。不过如果症状比较严重，比如持续高烧或者呼吸困难，那就得赶紧去医院了。",
        "speaker": "speaker-2"
      },
      {
        "text": "没错，千万别拖延病情。医院可以排查是否有并发症，比如肺炎之类的。总之，早发现、早治疗很重要。",
        "speaker": "speaker-1"
      },
      {
        "text": "总结一下，甲流虽然可怕，但只要我们做好防护，及时就医，就没啥好怕的。大家记住了吗？",
        "speaker": "speaker-2"
      },
      {
        "text": "记住了！接种疫苗、勤洗手、戴口罩、增强免疫力，还有必要时及时就医。希望大家都能健健康康地度过这个季节！",
        "speaker": "speaker-1"
      },
      {
        "text": "好了，今天的节目就到这里。感谢大家收听，我们下期再见！",
        "speaker": "speaker-2"
      },
      {
        "text": "再见！",
        "speaker": "speaker-1"
      }
    ],
    "resultUrl": {
      "audio": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/audio.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748853849&Signature=e1KlRgmjAjuUkPVWIEhoRbn4X0w%3D",
      "script": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/script.txt?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748853511&Signature=th5sI%2BB1FZuQ6tRLg4qGGX1fevI%3D"
    },
    "extraResult": {
      "segment": [
        [
          0,
          6370
        ],
        [
          6370,
          15020
        ],
        [
          15020,
          26071.791
        ],
        [
          26071.791,
          31001.791
        ],
        [
          31001.791,
          45646.582
        ],
        [
          45646.582,
          50816.582
        ],
        [
          50816.582,
          59501.418
        ],
        [
          59501.418,
          63631.418
        ],
        [
          63631.418,
          77161.25
        ],
        [
          77161.25,
          84691.25
        ],
        [
          84691.25,
          93623.086
        ],
        [
          93623.086,
          99233.086
        ],
        [
          99233.086,
          108894.875
        ],
        [
          108894.875,
          111864.875
        ],
        [
          111864.875,
          121678.664
        ],
        [
          121678.664,
          128448.664
        ],
        [
          128448.664,
          139774.45
        ],
        [
          139774.45,
          149824.45
        ],
        [
          149824.45,
          157966.25
        ],
        [
          157966.25,
          164576.25
        ],
        [
          164576.25,
          175432.08
        ],
        [
          175432.08,
          184482.08
        ],
        [
          184482.08,
          192451.88
        ],
        [
          192451.88,
          199781.88
        ],
        [
          199781.88,
          208151.88
        ],
        [
          208151.88,
          212601.88
        ],
        [
          212601.88,
          213131.88
        ]
      ],
      "segmentDetails": [
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_0.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=cWk2X%2B7MtbIEm%2Fu1mwVts59hpwU%3D",
          "index": 0,
          "time": [
            0,
            6370
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "听众朋友们，晚上好！今天咱们聊聊最近大家都很关心的一个话题——甲流来袭，我们该怎么应对？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_1.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=CFGULg%2FJ8I3htf0YvVL5mz7FLXg%3D",
          "index": 1,
          "time": [
            6370,
            15020
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "嗯，这个话题确实挺重要。甲流听起来有点吓人，但其实只要科学防护，就不用太担心。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_2.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=Q2Ck9DLRqsvJ1Bt6aqMh0rnPPDQ%3D",
          "index": 2,
          "time": [
            15020,
            26071.791
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "没错，先给大家科普一下，甲流全名叫甲型流感，是由甲型流感病毒感染引起的流行性感冒。（对）跟普通感冒比起来，它的症状更重，传播也更快。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_3.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=vPwoJQnhKv2Ti4aovV6v3lP4V5w%3D",
          "index": 3,
          "time": [
            26071.791,
            31001.791
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "哦？那具体都有哪些症状呢？我记得好像会发烧吧。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_4.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=fUh04j4iLyYG4GV5wQ1f5GkFvJE%3D",
          "index": 4,
          "time": [
            31001.791,
            45646.582
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "对的，高烧是甲流最常见的症状之一，体温可能高达39到40度。（嗯）除了发烧，还会有头痛、全身肌肉和关节疼痛、乏力、食欲不振等症状。有些人甚至会出现恶心、呕吐的情况。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_5.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=v5c0d%2Bk4OmjmRRFVCKZ5JhDOq5o%3D",
          "index": 5,
          "time": [
            45646.582,
            50816.582
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "听起来确实不太好受。不过婴儿的症状是不是会稍微不一样？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_6.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=ZeyAxNn8wbRFXK4qXPJMKKGhIl0%3D",
          "index": 6,
          "time": [
            50816.582,
            59501.418
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "是的，婴儿可能会表现为高烧、烦躁、哭闹增加，还有吃奶减少等。（确实）所以家长要特别注意观察孩子的状态。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_7.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854445&Signature=UEyc%2BbAqgIa1C3SS4EjtNegTDTg%3D",
          "index": 7,
          "time": [
            59501.418,
            63631.418
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "嗯，说到这，我突然想到一个问题：甲流是怎么传播的呢？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_8.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=JYlAsSnLJNMFDEv9Bm5hSf4SrNY%3D",
          "index": 8,
          "time": [
            63631.418,
            77161.25
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "主要通过呼吸道传播和接触传播。（没错）比如近距离接触甲流病人或者高度疑似病人后，就可能被感染。另外，患者的分泌物也可能携带病毒，直接或间接接触这些分泌物也会有风险。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_9.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=eHG1QMbfsSSqfHwAD79Xs531kFw%3D",
          "index": 9,
          "time": [
            77161.25,
            84691.25
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "哦，原来如此。那易感人群有哪些呢？是不是老年人和小孩更容易中招？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_10.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=rElcCYlOaChj%2BJWT94c7%2F%2FMlTUo%3D",
          "index": 10,
          "time": [
            84691.25,
            93623.086
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "没错，老人、孕妇、小孩都是易感人群。（真的）此外，患有慢性疾病、肥胖或者免疫功能低下的人群也要格外小心。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_11.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=dBjOIrNqHSiF3RCrbsWyLtrE6Ow%3D",
          "index": 11,
          "time": [
            93623.086,
            99233.086
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "听你这么一说，感觉预防真的很重要啊。那有没有什么有效的预防措施呢？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_12.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=EJ0qCENMhqIUEu6UZ0RTP0cdibQ%3D",
          "index": 12,
          "time": [
            99233.086,
            108894.875
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "当然有！最有效的方法就是接种疫苗。（对）每年9到10月份接种流感疫苗，保护效力可以持续到冬春流感高发季节。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_13.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=nH02zWlwtrLK2fcskFbRvuMTD3s%3D",
          "index": 13,
          "time": [
            108894.875,
            111864.875
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "嗯，除了打疫苗，还有什么其他办法吗？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_14.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=9y3D2UGy6zg77gFWP4qFtHkF5S4%3D",
          "index": 14,
          "time": [
            111864.875,
            121678.664
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "保持良好的卫生习惯也很重要。比如勤洗手，尽量避免用手接触眼、鼻、口。（没错）同时，避免在拥挤的场所逗留，减少人际接触。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_15.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854446&Signature=EbwEURP7u9HpwrsrPC2Thwd4XUg%3D",
          "index": 15,
          "time": [
            121678.664,
            128448.664
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "嗯，这点我特别赞同。现在很多人都习惯了戴口罩，这其实也是个很好的防护措施。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_16.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=4rj5XQD0SaspVCj7QmGFrIGyACA%3D",
          "index": 16,
          "time": [
            128448.664,
            139774.45
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "没错，戴口罩能有效阻断飞沫传播。另外，增强免疫力也很关键。（嗯）保持充足的睡眠、均衡的饮食和适量的运动都能帮助身体更好地抵抗病毒。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_17.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=1aGlxcVI8r3ac7kY%2FHAt2%2Bg2Jss%3D",
          "index": 17,
          "time": [
            139774.45,
            149824.45
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "听你这么一说，感觉生活中的小细节真的很重要。比如咳嗽或打喷嚏时，用纸巾、手肘遮住口鼻，就能减少病毒传播。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_18.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=41GmphAH1k2hwtKm5xG5HU8sZYU%3D",
          "index": 18,
          "time": [
            149824.45,
            157966.25
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "对，还有别忘了保持环境清洁和通风。（确实）家里、教室每天勤开窗通风，必要时进行消毒。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_19.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=1yD7PvQwmJCFtDVZxiBSCgxFQWE%3D",
          "index": 19,
          "time": [
            157966.25,
            164576.25
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "看来这些看似简单的小事，其实都能起到大作用。那万一真的不幸中招了，该怎么办呢？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_20.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=D%2BVKscQXjtyzbNx5NJhx%2Fyny1qI%3D",
          "index": 20,
          "time": [
            164576.25,
            175432.08
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "如果确诊是甲型流感，一定要隔离、卧床休息，并遵医嘱用药。（没错）比如磷酸奥司他韦胶囊就是一种常用的抗病毒药物。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_21.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=Ugt6%2FUFdc7ACT%2BFxJm4Tk8VOX84%3D",
          "index": 21,
          "time": [
            175432.08,
            184482.08
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "哦，原来还有专门针对甲流的药。不过如果症状比较严重，比如持续高烧或者呼吸困难，那就得赶紧去医院了。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_22.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=YJy3rQ2cpGwjtW%2BSzehQscSFicg%3D",
          "index": 22,
          "time": [
            184482.08,
            192451.88
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "没错，千万别拖延病情。医院可以排查是否有并发症，比如肺炎之类的。（对）总之，早发现、早治疗很重要。"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_23.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854447&Signature=5WvLaj3cCmK5m%2FAS8EiIbaAgxYs%3D",
          "index": 23,
          "time": [
            192451.88,
            199781.88
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "总结一下，甲流虽然可怕，但只要我们做好防护，及时就医，就没啥好怕的。大家记住了吗？"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_24.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854448&Signature=H4gi%2B%2BUJ%2BJ36rjZeUecTsqFjTqY%3D",
          "index": 24,
          "time": [
            199781.88,
            208151.88
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "记住了！接种疫苗、勤洗手、戴口罩、增强免疫力，还有必要时及时就医。希望大家都能健健康康地度过这个季节！"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_25.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854448&Signature=oGTU2Ki3FkmV2hvL3sPFVM7ZPGI%3D",
          "index": 25,
          "time": [
            208151.88,
            212601.88
          ],
          "script": {
            "speaker": "speaker-2",
            "text": "好了，今天的节目就到这里。感谢大家收听，我们下期再见！"
          }
        },
        {
          "audioSegmentUrl": "http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202506021536413361/segment_26.mp3?OSSAccessKeyId=LTAI5tPLWJfJHNkZbfnQ****&Expires=1748854448&Signature=N4lXSxOmRSjsRFounST8hBM3FnY%3D",
          "index": 26,
          "time": [
            212601.88,
            213131.88
          ],
          "script": {
            "speaker": "speaker-1",
            "text": "再见！"
          }
        }
      ]
    }
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AIPodcast/2025-02-28/errorCode>)查看更多错误码。
