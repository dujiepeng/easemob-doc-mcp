 # 发送单聊消息

 ## 功能说明

<Toc />

环信即时通讯 IM 支持在服务端实现单聊场景中全类型消息的发送与接收，包括文本消息、图片消息、语音消息、视频消息、透传消息和自定义消息。

### 发送方式

单聊场景下，发送各类型的消息调用同一 RESTful API，不同类型的消息只是请求体中的 body 字段内容存在差异。

<table>
<tbody>
<tr>
<td width="161">
<p><strong>消息类型</strong></p>
</td>
<td width="189">
<p><strong>发送方式</strong></p>
</td>
<td width="279">
<p><strong>备注</strong></p>
</td>
</tr>
<tr>
<td width="161">
<p>文本/透传消息</p>
</td>
<td width="189">
<p>调用发送消息方法，在请求 body 中传入消息内容。</p>
</td>
<td rowspan="2" width="279">
<p>1.发送消息时，可选的 `from` 字段用于指定发送方。</p>
<p>2. 消息支持扩展属性 `ext`，可添加自定义信息。同时，推送通知也支持自定义扩展字段，详见 <a href="https://doc.easemob.com/document/ios/push/push_display.html#%E4%BD%BF%E7%94%A8%E6%B6%88%E6%81%AF%E6%89%A9%E5%B1%95%E5%AD%97%E6%AE%B5%E8%AE%BE%E7%BD%AE%E6%8E%A8%E9%80%81%E9%80%9A%E7%9F%A5%E6%98%BE%E7%A4%BA%E5%86%85%E5%AE%B9">APNs 自定义显示</a>和 <a href="https://doc.easemob.com/document/android/push/push_display.html#%E4%BD%BF%E7%94%A8%E6%B6%88%E6%81%AF%E6%89%A9%E5%B1%95%E5%AD%97%E6%AE%B5%E8%AE%BE%E7%BD%AE%E6%8E%A8%E9%80%81%E9%80%9A%E7%9F%A5%E6%98%BE%E7%A4%BA%E5%86%85%E5%AE%B9">Android 推送字段说明</a>。</p>
</td>
</tr>
<tr>
<td width="161">
<p>图片/语音/视频/文件消息</p>
</td>
<td width="189">
<p>1. 调用<a href="https://doc.easemob.com/document/server-side/message_download.html#%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6">文件上传</a>方法上传图片、语音、视频或其他类型文件，并从响应 body 中获取文件 UUID。</p>
<p>2. 调用发送消息方法，在请求 body 中传入该 UUID。</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>

### 特别说明

- 接口调用过程中，请求体和扩展字段的总长度不能超过 5 KB。
- 该接口默认不会检查发送方和接收方的好友关系。若你在环信控制台开启了 [好友关系检查](/product/enable_and_configure_IM.html#好友关系检查)，该接口会检查发送方和接收方的好友关系。
- 该接口不会检查接收方是否在黑名单上，同时不会检查发送方是否被禁言。
- 该接口不校验传入的发送方和接收方的用户 ID。如果你传入的用户 ID 不存在，服务器并不会提示，仍照常发送消息。
- 你可以设置消息发送成功后，是否将消息同步到发送方的所有在线设备（`sync_device` 参数）。
- 你可以设置哪些用户拉漫游消息时拉不到该消息（`roam_ignore_users` 参数）。
- 你可以只将消息发送给在线用户，离线用户则无法收到消息（`routetype`）。
- 通过 RESTful 接口发送的消息默认不写入会话列表，若需要此类消息写入会话列表，需在 [环信即时通讯控制台开通](/product/enable_and_configure_IM.html#设置通过-restful-api-发送的消息写入会话列表)。
- 调用该接口会触发发送后回调事件，请参见 [回调事件文档](callback_message_send.html#发送单聊消息)。
- [内容审核服务会关注消息 body 中指定字段的内容，不同类型的消息审核不同的字段](/product/moderation/moderation_mechanism.html)，若创建消息时在这些字段中传入了很多业务信息，可能会影响审核效果。因此，创建消息时需要注意内容审核的字段不涉及业务信息，建议业务信息放在扩展字段中。

### 调用频率上限

对于单个 app，该 REST API 存在以下三个限制：

<table>
<tbody>
<tr>
<td width="110">
<p><strong>限制</strong></p>
</td>
<td>
<p><strong>描述</strong></p>
</td>
<td>
<p><strong>超限报错</strong></p>
</td>
<td>
<p><strong>是否可调</strong></p>
</td>
</tr>
<tr>
<td>
<p>100 次/秒</p>
</td>
<td>
<p>每秒限调 100 次</p>
</td>
<td>
<p>若超限，报 429 错误 即 &ldquo;This request has reached api limit&rdquo;。</p>
</td>
<td rowspan="2">
<p>两个限制均<strong>可调</strong>且相互关联，即上调其中一个，另一个自动等比例提升。</p>
<p>例如，将 100 次/秒上调至 200 次/秒后，每分钟限发消息条数也会自动上调至 12000，即 12000 条/分钟。反之，若将 6000 条/分钟上调至 12000 条/分钟，每秒的调用次数上限也自动提升至 200，即 200 次/秒。</p>
</td>
</tr>
<tr>
<td>
<p>6000 条/分钟</p>
</td>
<td>
<p>每分钟限发 6000 条消息</p>
</td>
<td>
<p>若超限，报 403 错误，即 " message send reach limit"。</p>
<p>&nbsp;</p>
</td>
</tr>
<tr>
<td>
<p>600 人/次</p>
</td>
<td>
<p>每次限发 600 人。</p>
<p>例如，一次向 600 人发消息，视为 600 条消息。</p>
</td>
<td>
<p>若超限，报 400 错误，即 "param to exceed limit"。</p>
</td>
<td>
<p>不可调。</p>
</td>
</tr>
</tbody>
</table>

## 前提条件

要调用环信即时通讯 REST API，请确保满足以下要求：

- 已在环信即时通讯控制台 [开通配置环信即时通讯 IM 服务](enable_and_configure_IM.html)。
- 了解环信 IM REST API 的调用频率限制，详见 [接口频率限制](limitationapi.html)。

## 公共参数 

### 请求参数

| 参数       | 类型   | 是否必需 | 描述        |
| :--------- | :----- | :------- | :----------------------- |
| `host`     | String | 是       | 环信即时通讯 IM 分配的用于访问 RESTful API 的域名。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。 |
| `org_name` | String | 是       | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |
| `app_name` | String | 是       | 你在环信即时通讯云控制台创建应用时填入的应用名称。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |
| `username` | String | 是       | 用户 ID。              |

### 响应参数

| 参数              | 类型   | 描述          |
| :---------------- | :----- | :------------------------------- |
| `action`          | String | 请求方法。                                                                     |
| `organization`    | String | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识，与请求参数 `org_name` 相同。 |
| `application`     | String | 应用在系统内的唯一标识。该标识由系统生成，开发者无需关心。                     |
| `applicationName` | String | 你在环信即时通讯云控制台创建应用时填入的应用名称，与请求参数 `app_name` 相同。 |
| `uri`             | String | 请求 URL。                                                                     |
| `path`            | String | 请求路径，属于请求 URL 的一部分，开发者无需关注。                              |
| `timestamp`       | Long   | HTTP 响应的 Unix 时间戳，单位为毫秒。                                          |
| `duration`        | Int    | 从发送 HTTP 请求到响应的时长，单位为毫秒。                                     |

## 认证方式

环信即时通讯 REST API 要求 Bearer HTTP 认证。每次发送 HTTP 请求时，都必须在请求头部填入如下 `Authorization` 字段：

`Authorization: Bearer YourAppToken`

为提高项目的安全性，环信使用 Token（动态密钥）对即将登录即时通讯系统的用户进行鉴权。本文涉及的所有消息管理 REST API 都需要使用 App Token 的鉴权方式，详见 [使用 App Token 鉴权](easemob_app_token.html)。

## 发送文本消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述           |
| :-------------- | :----- | :------- | :----------------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。        |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。       |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

下表为发送各类消息的通用请求体，为 JSON 对象，是所有消息的外层结构。不同类型的消息只是 `body` 字段内容存在差异。

| 参数            | 类型   | 是否必需 | 描述            |
| :-------------- | :----- | :------- | :----------------------------------------------------- |
| `from`          | String | 否       | 消息发送方的用户 ID。若不传入该字段，服务器默认设置为 `admin`。 <Container type="tip" title="提示">1. 服务器不校验传入的用户 ID 是否存在，因此，如果你传入的用户 ID 不存在，服务器并不会提示，仍照常发送消息。<br/>2. 若传入字段但值为空字符串 (“”)，请求失败。</Container>  |
| `to`            | List   | 是       | 消息接收方的用户 ID 数组。每次最多可向 600 个用户发送消息。<Container type="tip" title="提示">服务器不校验传入的用户 ID 是否存在，因此，如果你传入的用户 ID 不存在，服务器并不会提示，仍照常发送消息。</Container> |
| `type`          | String | 是       | 消息类型：<br/> - `txt`：文本消息；<br/> - `img`：图片消息；<br/> - `audio`：语音消息；<br/> - `video`：视频消息；<br/> - `file`：文件消息；<br/> - `loc`：位置消息；<br/> - `cmd`：透传消息；<br/> - `custom`：自定义消息。 |
| `body`          | JSON   | 是       | 消息内容。body 包含的字段见下表说明。     |
| `sync_device`   | Bool   | 否       | 消息发送成功后，是否将消息同步到发送方的所有在线设备。<br/> - `true`：是；<br/> - （默认）`false`：否。   |
| `roam_ignore_users`   | List   | 否 | 设置哪些用户拉漫游消息时拉不到该消息。|
| `routetype`     | String | 否       | 若传入该参数，其值为 `ROUTE_ONLINE`，表示接收方只有在线时才能收到消息，若接收方离线则无法收到消息。若不传入该参数，无论接收方在线还是离线都能收到消息。 |
| `ext`   | JSON   | 否       | 消息支持扩展字段，可添加自定义信息。不能对该参数传入 `null`。同时，推送通知也支持自定义扩展字段，详见 [APNs 自定义显示](/document/ios/push/push_display.html#使用消息扩展字段设置推送通知显示内容) 和 [Android 推送字段说明](/document/android/push/push_display.html#使用消息扩展字段设置推送通知显示内容)。 |
| `ext.em_ignore_notification` | Bool   | 否 | 是否发送静默消息：<br/> - `true`：是；<br/> - （默认）`false`：否。<br/> 发送静默消息指用户离线时，环信即时通讯 IM 服务不会通过第三方厂商的消息推送服务向该用户的设备推送消息通知。因此，用户不会收到消息推送通知。当用户再次上线时，会收到离线期间的所有消息。发送静默消息和免打扰模式下均为不推送消息，区别在于发送静默消息为发送方设置不推送消息，而免打扰模式为接收方设置在指定时间段内不接收推送通知。|

请求体中的 `body` 字段说明详见下表。

| 参数  | 类型   | 是否必需 | 描述       |
| :---- | :----- | :------- | :--------- |
| `msg` | String | 是       | 消息内容。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

发送给目标用户，消息无需同步给发送方：

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/users' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>'  \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "txt",
  "roam_ignore_users": [],
  "body": {
    "msg": "testmessages"
    },
  "ext": {
      "em_ignore_notification": true
    }
  }'
```

仅发送给在线用户，消息同步给发送方：

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/users' \
-H 'Content-Type: application/json' -H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "txt",
  "roam_ignore_users": [],
  "body": {
    "msg": "testmessages"
    },
  "ext": {
      "em_ignore_notification": true
    },
  "routetype":"ROUTE_ONLINE", 
  "sync_device":true
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

消息发送失败的响应示例：

```json
{
    "error": "message_send_error",
    "exception": "MessageSendException",
    "timestamp": 1748575460150,
    "duration": 0,
    "error_code": 14007,
    "error_description": "message is too large"
}
```

## 发送图片消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :------------------------------ |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。   |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。    |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数       | 类型   | 是否必需 | 描述   |
| :--------- | :----- | :------- | :------- |
| `filename` | String | 否       | 图片名称。建议传入该参数，否则客户端收到图片消息时无法显示图片名称。          |
| `secret`   | String | 否       | 图片的访问密钥，即成功上传图片后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果图片文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。 |
| `size`     | JSON   | 否       | 图片尺寸，单位为像素，包含以下字段：<br/> - `height`：图片高度；<br/> - `width`：图片宽度。   |
| `url`      | String | 是       | 图片 URL。格式为 `https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。其中 `file_uuid` 为图片文件 ID，成功上传图片文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。  |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/users' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \ 
-H 'Authorization: Bearer <YourAppToken>'\ 
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "img",
  "body": {
    "filename":"testimg.jpg",
    "secret":"VfXXXXNb_",
    "url":"https://XXXX/XXXX/XXXX/chatfiles/55f12940-XXXX-XXXX-8a5b-ff2336f03252",
    "size": {
      "width":480,
      "height":720
    }
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送语音消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述            |
| :-------------- | :----- | :------- | :------------ |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。   |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数       | 类型   | 是否必需 | 描述      |
| :--------- | :----- | :------- | :---------- |
| `filename` | String | 否       | 语音文件的名称。建议传入该参数，否则客户端收到语音消息时无法显示语音文件名称。    |
| `secret`   | String | 否       | 语音文件访问密钥，即成功上传语音文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。 如果语音文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。 |
| `Length`   | Int    | 否       | 语音时长，单位为秒。         |
| `url`      | String | 是       | 语音文件 URL。格式为 `https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。`file_uuid` 为文件 ID，成功上传语音文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。  |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

##### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/users' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "audio",
  "body": {
    "url": "https://XXXX/XXXX/XXXX/chatfiles/1dfc7f50-XXXX-XXXX-8a07-7d75b8fb3d42",
    "filename": "testaudio.amr",
    "length": 10,
    "secret": "HfXXXXCjM"
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送视频消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述    |
| :-------------- | :----- | :------- | :----------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。    |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。    |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数           | 类型   | 是否必需 | 描述    |
| :------------- | :----- | :------- | :---------------- |
| `filename` | String | 否       | 文件名称。建议传入该参数，否则客户端收到视频消息时无法显示视频文件名称。  |
| `thumb`        | String | 否       | 视频缩略图 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。`file_uuid` 为视频缩略图唯一标识，成功上传缩略图文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。 |
| `length`       | Int    | 否       | 视频时长，单位为秒。  |
| `secret`       | String | 否       | 视频文件访问密钥，即成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果视频文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。        |
| `file_length`  | Long   | 否      | 视频文件大小，单位为字节。  |
| `thumb_secret` | String | 否       | 视频缩略图访问密钥，即成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果缩略图文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。    |
| `url`          | String | 是       | 视频文件 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。其中 `file_uuid` 为文件 ID，成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。   |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

##### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/users' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "video",
  "body": {
    "filename" : "test.avi",
    "thumb" : "https://XXXX/XXXX/XXXX/chatfiles/67279b20-7f69-11e4-8eee-21d3334b3a97",
    "length" : 0,
    "secret":"VfXXXXNb_",
    "file_length" : 58103,
    "thumb_secret" : "ZyXXXX2I",
    "url" : "https://XXXX/XXXX/XXXX/chatfiles/671dfe30-XXXX-XXXX-ba67-8fef0d502f46"
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送文件消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述         |
| :-------------- | :----- | :------- | :---------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。     |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。    |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数       | 类型   | 是否必需 | 描述     |
| :--------- | :----- | :------- | :------------ |
| `filename` | String | 否       | 文件名称。建议传入该参数，否则客户端收到文件消息时无法显示文件名称。   |
| `secret`   | String | 否       | 文件访问密钥，即成功上传文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。      |
| `url`      | String | 是       | 文件 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。其中 `file_uuid` 为文件 ID，成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

##### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/users' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "file",
  "body": {
    "filename":"test.txt",
    "secret":"1-g0XXXXua",
    "url": "https://XXXX/XXXX/XXXX/chatfiles/d7eXXXX7444"
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送位置消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述      |
| :-------------- | :----- | :------- | :--------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。    |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。   |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数   | 类型   | 是否必需 | 描述                   |
| :----- | :----- | :------- | :--------------------- |
| `lat`  | String | 是       | 位置的纬度，单位为度。 |
| `lng`  | String | 是       | 位置的经度，单位为度。 |
| `addr` | String | 是       | 位置的文字描述。       |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i "https://XXXX/XXXX/XXXX/messages/users"  \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "loc",
  "body": {
    "lat": "39.966",
    "lng":"116.322",
    "addr":"中国北京市海淀区中关村"
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送透传消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述      |
| :-------------- | :----- | :------- | :--------------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。    |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。 |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数     | 类型   | 是否必需 | 描述       |
| :------- | :----- | :------- | :--------- |
| `action` | String | 是       | 命令内容。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i "https://XXXX/XXXX/XXXX/messages/users" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'  \
-H "Authorization:Bearer <YourAppToken>" \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "cmd",
  "body":{
    "action":"action1"
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送自定义消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。  

#### 请求 header

| 参数            | 类型   | 是否必需 | 描述      |
| :-------------- | :----- | :------- | :--------------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。    |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。 |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数          | 类型   | 是否必需 | 描述     |
| :------------ | :----- | :------- | :-------------------------------- |
| `customEvent` | String | 否       | 用户自定义的事件类型。该参数的值必须满足正则表达式 `[a-zA-Z0-9-_/\.]{1,32}`，长度为 1-32 个字符。  |
| `customExts`  | JSON   | 否       | 用户自定义的事件属性，类型必须是 `Map<String,String>`，最多可以包含 16 个元素。`customExts` 是可选的，不需要可以不传。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :----------------- |
| `data` | JSON | 响应中的数据详情。该字段的值为包含接收方用户 ID 和 发送的消息的 ID 的键值对。<br/>例如 "user2": "1029457500870543736"，表示向 user2 发送了消息 ID 为 1029457500870543736 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i "https://XXXX/XXXX/XXXX/messages/users" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \ 
-H "Authorization:Bearer <YourAppToken>" \
-d '{
  "from": "user1",
  "to": ["user2"],
  "type": "custom",
  "body": {
    "customEvent": "custom_event",
    "customExts":{
          "ext_key1":"ext_value1"
      }
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/users",
  "uri": "https://XXXX/XXXX/XXXX/messages/users",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "user2": "1029457500870543736"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 错误码

调用发送单聊消息的接口发送各类消息时，如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型  | 错误提示  | 可能原因     | 处理建议   |
|:---------|:-----------|:----------|:----------|:--------|
| 400      | invalid_request_body       | Request body is invalid. Please check body is correct. | 请求体格式不正确。  | 检查请求体内容是否合法(字段类型是否正确) 。  |
| 400      | message_send_error | param from can't be empty   | 请求参数 `from` 是空字符串。  | 输入正确的请求参数 `from`。若不传该字段， 服务器会默认设置为 `admin`。 |
| 400      | message_send_error | param to can't be empty    | 请求参数 `to` 是空数组。| 输入正确的请求参数 `to`。|
| 400      | message_send_error | param type can't be empty   | 请求参数 `type` 是空字符串。 | 输入正确的请求参数 `type`。 |
| 400      | message_send_error | param body can't be empty | 请求参数 `body` 是空 JSON。 | 输入正确的请求参数 `body`。 |
| 400      | message_send_error | param ext must be JSONObject | 请求参数 `ext` 类型不正确。 | 输入正确的请求参数 `ext`（JSON 格式）。    |
| 400      | message_send_error | params to's size can't exceed limit 600    | 请求参数 `to` 数量超出最大限制 600。                | 输入正确的请求参数 `to`（数量限制在 600 以内），即每次最多可向 600 人发送消息。 |
| 400      | message_send_error | message is too large                                   | 请求体内容中 `body` 和 `ext` 字段的内容过大。 | 限制 `body` 和 `ext` 字段的内容。请求体和扩展字段的总长度不能超过 5 KB。  |
| 403      | message_send_error | message send reach limit                               | 消息发送频率超出限制(默认 60 秒内只允许发送 6000 条单聊消息)。 | 限制消息发送频率，详见[文档说明](message_single.html)。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

