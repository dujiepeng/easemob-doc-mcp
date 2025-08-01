# 发送群聊消息

<Toc />

 ## 功能说明

环信即时通讯 IM 支持在服务端实现群聊场景中全类型消息的发送与接收，包括文本消息、图片消息、语音消息、视频消息、文件消息、透传消息和自定义消息。

### 发送方式

群组聊天场景下，发送各类型的消息调用需调用同一 RESTful API，不同类型的消息只是请求体中的 body 字段内容存在差异，发送方式与单聊类似。

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
- 该接口不校验传入的发送方用户 ID 和作为接收方的群组 ID。如果你传入的发送方用户 ID 和群组 ID 不存在，服务器并不会提示，仍照常发送消息。
- 群组中发送的消息均同步给发送方。
- 你可以只将消息发送给在线用户，若群组中的用户离线则无法收到消息（`routetype` 参数）。
- 你可以设置哪些用户拉漫游消息时拉不到该消息（`roam_ignore_users` 参数）。
- 通过 RESTful 接口发送的消息默认不写入会话列表，若需要此类消息写入会话列表，需在 [环信即时通讯控制台开通](/product/enable_and_configure_IM.html#设置通过-restful-api-发送的消息写入会话列表)。
- 调用该接口会触发发送后回调事件，请查看 [回调事件文档](callback_message_send.html#发送群组消息)。
- [内容审核服务会关注消息 body 中指定字段的内容，不同类型的消息审核不同的字段](/product/moderation/moderation_mechanism.html)，若创建消息时在这些字段中传入了很多业务信息，可能会影响审核效果。因此，创建消息时需要注意内容审核的字段不涉及业务信息，建议业务信息放在扩展字段中。

### 调用频率上限

对于单个 app，该 REST API 存在以下三个限制：

<table>
<tbody>
<tr>
<td width="100">
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
<p>20 次/秒</p>
</td>
<td>
<p>每秒限调 20 次。</p>
</td>
<td>
<p>例如，你每次调用该 API 向单个或多个群组发送消息，可调用 20 次。第 21 次调用时会报 429 错误 &ldquo;This request has reached api limit&rdquo;。</p>
</td>
<td rowspan="2">
<p>两个限制均<strong>可调</strong>。若上调其中一个，另一个自动等比例提升。</p>
<p>例如，将 20 次/秒上调至 100 次/秒后，每秒限发条数也会自动上调至 100，即 100 条/秒。反之，将 20 条/秒上调至 100 条/秒后，每秒限调次数自动上调至 100，即 100 次/秒。</p>
</td>
</tr>
<tr>
<td>
<p>20 条/秒</p>
</td>
<td>
<p>每秒限发 20 条消息。</p>
</td>
<td>
<p>例如，你每次向 3 个群组发送消息，即发送了 3 条消息，你每秒最多可调用 7 次。第 8 次调用时，则报 403 错误，即 " message send reach limit"。</p>
</td>
</tr>
<tr>
<td>
<p>3 个群/次</p>
</td>
<td>
<p>每次限发 3 个群。</p>
</td>
<td>
<p>若超限，报 400 错误，即 "param to exceed limit"。</p>
</td>
<td>
<p>不可调</p>
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
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。

#### 请求 header

| 参数       | 类型   | 是否必需 | 描述          |
| :-------------- | :----- | :------- | :-------------- |
| `Content-Type`  | String | 是       | 内容类型。填入 `application/json`。       |
| `Accept`        | String | 是       | 内容类型。填入 `application/json`。      |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

下表为发送各类消息的通用请求体，为 JSON 对象，是所有消息的外层结构。与单聊消息类似，不同类型的消息的请求体只是 `body` 字段内容存在差异。

:::tip
1. 群聊消息的通用请求体中的参数与[发送单聊消息](message_single.html)类似，唯一区别在于群聊中的 `to` 字段表示消息接收方群组 ID 数组。<br/>
:::

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :--------------- |
| `from`          | String | 否       | 消息发送方的用户 ID。若不传入该字段，服务器默认设置为 `admin`。<Container type="tip" title="提示">1. 服务器不校验传入的用户 ID 是否存在，因此，如果你传入的用户 ID 不存在，服务器并不会提示，仍照常发送消息。<br/>2. 若传入字段但值为空字符串 (“”)，请求失败。</Container>  |
| `to`            | Array   | 是       | 消息接收方群组 ID 数组。每次最多可向 3 个群组发送消息。<Container type="tip" title="提示">服务器不校验传入的群组 ID 是否存在，因此，如果你传入的群组 ID 不存在，服务器并不会提示，仍照常发送消息。</Container> |
| `type`          | String | 是       | 消息类型：<br/> - `txt`：文本消息；<br/> - `img`：图片消息；<br/> - `audio`：语音消息；<br/> - `video`：视频消息；<br/> - `file`：文件消息；<br/> - `loc`：位置消息；<br/> - `cmd`：透传消息；<br/> - `custom`：自定义消息。    |
| `need_group_ack` | Bool | 否 | 该条消息发送后是否需要已读回执：<br/> - `true`：需要；<br/> -（默认）`false`：不需要。 |
| `body`          | JSON   | 是       | 消息内容。body 包含的字段见下表说明。       |
| `roam_ignore_users`   | List   | 否 | 设置哪些用户拉漫游消息时拉不到该消息。每次最多可传入 20 个用户 ID。|
| `routetype`     | String | 否       | 若传入该参数，其值为 `ROUTE_ONLINE`，表示接收方只有在线时才能收到消息，若接收方离线则无法收到消息。若不传入该参数，无论接收方在线还是离线都能收到消息。  |
| `ext`           | JSON   | 否       | 消息支持扩展字段，可添加自定义信息。不能对该参数传入 `null`。同时，推送通知也支持自定义扩展字段，详见 [APNs 自定义显示](/document/ios/push/push_display.html#使用消息扩展字段设置推送通知显示内容) 和 [Android 推送字段说明](/document/android/push/push_display.html#使用消息扩展字段设置推送通知显示内容)。 |
| `ext.em_ignore_notification` | Bool   | 否 | 是否发送静默消息：<br/> - `true`：是；<br/> - （默认）`false`：否。<br/> 发送静默消息指用户离线时，环信即时通讯 IM 服务不会通过第三方厂商的消息推送服务向该用户的设备推送消息通知。因此，用户不会收到消息推送通知。当用户再次上线时，会收到离线期间的所有消息。发送静默消息和免打扰模式下均为不推送消息，区别在于发送静默消息为发送方设置不推送消息，而免打扰模式为接收方设置在指定时间段内不接收推送通知。| 

请求体中的 `body` 字段说明详见下表。

| 参数  | 类型   | 是否必需 | 描述       |
| :---- | :----- | :------- | :--------- |
| `msg` | String | 是       | 消息内容。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

发送给群组内所有成员，不论这些成员是否在线：

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "txt",
    "need_group_ack": false,
    "body": {
        "msg": "testmessages"
    },
    "roam_ignore_users": [],
    "ext": {
       "em_ignore_notification": true
    }
}'
```

仅发送给在线用户，即 `routetype` 设置为 `ROUTE_ONLINE`：

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups' 
-H 'Content-Type: application/json' 
-H 'Accept: application/json' 
-H 'Authorization: Bearer <YourAppToken>' 
-d '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "txt",
    "need_group_ack": false,
    "body": {
        "msg": "testmessages"
    },
    "ext": {
       "em_ignore_notification": true
    },
    "routetype":"ROUTE_ONLINE"
}'
```

#### 响应示例

消息发送成功的响应示例如下所示：

```json
{
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

消息发送失败的响应示例如下所示：

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
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。

#### 请求 header

| 参数       | 类型   | 是否必需 | 描述          |
| :-------------- | :----- | :------- | :-------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。       |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。      |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

关于通用请求体，详见[发送文本消息](#发送文本消息)。

请求体中的 `body` 字段说明详见下表。

| 参数       | 类型   | 是否必需 | 描述   |
| :--------- | :----- | :------- | :------- |
| `filename` | String | 否       | 图片名称。建议传入该参数，否则客户端收到图片消息时无法显示图片名称。          |
| `secret`   | String | 否       | 图片的访问密钥，即成功上传图片后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果图片文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。 |
| `size`     | JSON   | 否      | 图片尺寸，单位为像素，包含以下字段：<br/> - `height`：图片高度；<br/> - `width`：图片宽度。   |
| `url`      | String | 是       | 图片 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。其中 `file_uuid` 为文件 ID，成功上传图片文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。  |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "img",
    "body": {
        "filename":"testimg.jpg",
        "secret":"VfXXXXNb_",
        "url":"https://XXXX/XXXX/XXXX/chatfiles/55f12940-XXXX-XXXX-8a5b-ff2336f03252",
        "size":{
            "width":480,
            "height":720
        }
    }
}'
```

#### 响应示例

```json
{
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送语音消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
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
| `Length`   | Int    | 否      | 语音时长，单位为秒。         |
| `url`      | String | 是       | 语音文件 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。`file_uuid` 为文件 ID，成功上传语音文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。  |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups' \
-H 'Content-Type: application/json' -H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
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
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送视频消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
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

| 参数           | 类型   | 是否必需 | 描述    |
| :------------- | :----- | :------- | :---------------- |
| `filename` | String | 否 | 视频文件名称。建议传入该参数，否则客户端收到视频消息时无法显示视频文件名称。 |
| `thumb`        | String | 否       | 视频缩略图 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。`file_uuid` 为视频缩略图唯一标识，成功上传缩略图文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。 |
| `length`       | Int    | 否      | 视频时长，单位为秒。  |
| `secret`       | String | 否       | 视频文件访问密钥，即成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果视频文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。        |
| `file_length`  | Long   | 否      | 视频文件大小，单位为字节。  |
| `thumb_secret` | String | 否       | 视频缩略图访问密钥，即成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果缩略图文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。    |
| `url`          | String | 是       | 视频文件 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。其中 `file_uuid` 为文件 ID，成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。   |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d  '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "video",
    "body": {
        "filename" : "test.avi"
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
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送文件消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
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

| 参数       | 类型   | 是否必需 | 描述     |
| :--------- | :----- | :------- | :------------ |
| `filename` | String | 否       | 文件名称。 建议传入该参数，否则客户端收到文件消息时无法显示文件名称。  |
| `secret`   | String | 否       | 文件访问密钥，即成功上传文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取的 `share-secret`。如果文件上传时设置了文件访问限制（`restrict-access`），则该字段为必填。      |
| `url`      | String | 是       | 文件 URL 地址：`https://{host}/{org_name}/{app_name}/chatfiles/{file_uuid}`。其中 `file_uuid` 为文件 ID，成功上传视频文件后，从 [文件上传](message_download.html#上传文件) 的响应 body 中获取。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token
curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "file",
    "body": {
        "filename":"test.txt",
        "secret":"1-g0XXXXua",
        "url":"https://XXXX/XXXX/XXXX/chatfiles/d7eXXXX7444"
    }
}'
```

#### 响应示例

```json
{
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送位置消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
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

| 参数   | 类型   | 是否必需 | 描述                   |
| :----- | :----- | :------- | :--------------------- |
| `lat`  | String | 是       | 位置的纬度，单位为度。 |
| `lng`  | String | 是       | 位置的经度，单位为度。 |
| `addr` | String | 是       | 位置的文字描述。       |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups'  \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "loc",
    "body":{
        "lat": "39.966",
        "lng":"116.322",
        "addr":"中国北京市海淀区中关村"
    }
}'
```

#### 响应示例

```json
{
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送透传消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
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

| 参数     | 类型   | 是否必需 | 描述       |
| :------- | :----- | :------- | :--------- |
| `action` | String | 是       | 命令内容。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i "https://XXXX/XXXX/XXXX/messages/chatgroups" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'  \
-H 'Authorization: Bearer <YourAppToken>'  \
-d '{
  "from": "user1",
  "to": ["184524748161025"],
  "type": "cmd",
  "body": {
    "action": "action1"
  }
}'
```

#### 响应示例

```json
{
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送自定义消息

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups
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

| 参数          | 类型   | 是否必需 | 描述     |
| :------------ | :----- | :------- | :-------------------------------- |
| `customEvent` | String | 否       | 用户自定义的事件类型。该参数的值必须满足正则表达式 `[a-zA-Z0-9-_/\.]{1,32}`，长度为 1-32 个字符。  |
| `customExts`  | JSON   | 否       | 用户自定义的事件属性，类型必须是 `Map<String,String>`，最多可以包含 16 个元素。`customExts` 是可选的，不需要可以不传。 |

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i "https://XXXX/XXXX/XXXX/messages/chatgroups" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json'  \
-H "Authorization:Bearer <YourAppToken>" \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
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
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 发送定向消息

你可以向群组中指定的一个或多个成员发送消息，单次只能向 **一个群组** 中的 **20 个用户** 发送定向消息。对于定向消息，只有作为接收方的指定成员才能看到消息，其他群成员则看不到该消息。

:::tip
1. 定向消息不写入会话列表，不计入群组会话的未读消息数。
2. 群组定向消息的漫游功能默认关闭，使用前需联系商务开通。
3. 群组中发送的定向消息均同步给发送方。
4. 如果作为接收方的一些用户为离线状态，对于定向消息，可以收到离线推送通（若配置了离线推送服务），上线后可以收到离线消息（若未超过离线消息的存储时长）。
:::

**发送频率**：100 次/秒/App Key

以下以文本消息为例介绍如何在群组中发送定向消息。

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/messages/chatgroups/users
```

#### 路径参数

参数及说明详见 [公共参数](#公共参数)。

#### 请求 header

| 参数       | 类型   | 是否必需 | 描述          |
| :-------------- | :----- | :------- | :-------------- |
| `Content-Type`  | String | 是       | 内容类型。填入 `application/json`。       |
| `Accept`        | String | 是       | 内容类型。填入 `application/json`。      |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### 请求 body

下表为发送各类消息的通用请求体，为 JSON 对象，是所有消息的外层结构。

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :--------------- |
| `from`          | String | 否       | 消息发送方的用户 ID。若不传入该字段，服务器默认设置为管理员，即 “admin”；若传入字段但值为空字符串 (“”)，请求失败。  |
| `to`            | Array   | 是       | 消息接收方所属的群组 ID。每次只能传 1 个群组。 |
| `type`          | String | 是       | 消息类型：<br/> - `txt`：文本消息；<br/> - `img`：图片消息；<br/> - `audio`：语音消息；<br/> - `video`：视频消息；<br/> - `file`：文件消息；<br/> - `loc`：位置消息；<br/> - `cmd`：透传消息；<br/> - `custom`：自定义消息。    |
| `body`          | JSON   | 是       | 消息内容。body 包含的字段见下表说明。       |
| `ext`           | JSON   | 否       | 消息支持扩展字段，可添加自定义信息。不能对该参数传入 `null`。同时，推送通知也支持自定义扩展字段，详见 [APNs 自定义显示](/document/ios/push/push_display.html#使用消息扩展字段设置推送通知显示内容) 和 [Android 推送字段说明](/document/android/push/push_display.html#使用消息扩展字段设置推送通知显示内容)。 |
| `ext.em_ignore_notification` | Bool   | 否 | 是否发送静默消息：<br/> - `true`：是；<br/> - （默认）`false`：否。<br/> 发送静默消息指用户离线时，环信即时通讯 IM 服务不会通过第三方厂商的消息推送服务向该用户的设备推送消息通知。因此，用户不会收到消息推送通知。当用户再次上线时，会收到离线期间的所有消息。发送静默消息和免打扰模式下均为不推送消息，区别在于发送静默消息为发送方设置不推送消息，而免打扰模式为接收方设置在指定时间段内不接收推送通知。|
| `users` | Array | 是       | 接收消息的群成员的用户 ID 数组。每次最多可传 20 个用户 ID。 |


请求体中的 `body` 字段说明详见下表。

| 参数  | 类型   | 是否必需 | 描述       |
| :---- | :----- | :------- | :--------- |
| `msg` | String | 是       | 消息内容。 |

对于其他类型的消息，`body` 字段的说明详见发送各类型的普通群聊消息的请求体中的 `body` 字段说明。

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数   | 类型 | 描述     |
| :----- | :--- | :--------------- |
| `data` | JSON | 返回数据详情。该字段的值为包含群组 ID 和 发送的消息的 ID 的键值对。<br/>例如 "184524748161025": "1029544257947437432"，表示在 ID 为 184524748161025 的群组中发送了消息 ID 为 1029544257947437432 的消息。 |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

### 示例

#### 请求示例

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -i 'https://XXXX/XXXX/XXXX/messages/chatgroups/users' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
    "from": "user1",
    "to": ["184524748161025"],
    "type": "txt",
    "body": {
        "msg": "testmessages"
    },
    "ext": {
       "em_ignore_notification": true
    },
    "users": ["user2", "user3"]
}'
```

#### 响应示例

```json
{
  "path": "/messages/chatgroups",
  "uri": "https://XXXX/XXXX/XXXX/messages/chatgroups",
  "timestamp": 1657254052191,
  "organization": "XXXX",
  "application": "e82bcc5f-XXXX-XXXX-a7c1-92de917ea2b0",
  "action": "post",
  "data": {
    "184524748161025": "1029544257947437432"
  },
  "duration": 0,
  "applicationName": "XXXX"
}
```

## 错误码

1. 调用发送群聊消息的接口发送各类消息时，如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型      | 错误提示        | 可能原因      | 处理建议    |
|:---------|:-------------------|:------------|:-----------|:---------|
| 400      | invalid_request_body                   | Request body is invalid. Please check body is correct. | 请求体格式不正确。 | 检查请求体内容是否合法(字段类型是否正确)。 |
| 400      | message_send_error | param from can't be empty   | 请求参数 `from` 是空字符串。| 输入正确的请求参数 `from`。若不传该字段， 服务器会默认设置为 `admin`。|
| 400      | message_send_error | param to can't be empty   | 请求参数 `to` 是空数组。| 输入正确的请求参数 `to`。每次最多可向 3 个群组发送消息。   |
| 400      | message_send_error | param type can't be empty | 请求参数 `type` 是空字符串。 | 输入正确的请求参数 `type`。         |
| 400      | message_send_error | param body can't be empty    | 请求参数 `body` 是空 JSON。 | 输入正确的请求参数 `body`。         |
| 400      | message_send_error | param ext must be JSONObject  | 请求参数 `ext` 类型不正确。 | 输入正确的请求参数 `ext`（JSON 格式）。  |
| 400      | message_send_error | params to's size can't exceed limit 3  | 请求参数 `to` 数量超出最大限制 3 个群组 ID。 | 输入正确的请求参数 `to`（数量限制在 3 个群组 ID 以内）。 |
| 400      | message_send_error | message is too large    | 请求体内容中 `body` 和 `ext` 字段的内容过大。  | 限制 `body` 和 `ext` 字段的内容。   |
| 403      | message_send_error | message send reach limit  | 消息发送频率超出限制(默认 1 秒内只允许发送 20 条群聊消息) | 限制消息发送频率，详见[文档说明](message_group.html)。|

2. 对于定向消息来说，如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型      | 错误提示          | 可能原因       | 处理建议       |
|:---------|:-------------------|:-------------------|:-----------|:----------------------|
| 400      | invalid_request_body     | Request body is invalid. Please check body is correct. | 请求体格式不正确。    | 检查请求体内容是否合法(字段类型是否正确)。 |
| 400      | message_send_error | param from can't be empty | 请求参数 `from` 是空字符串。   | 输入正确的请求参数 `from`。若不传该字段， 服务器会默认设置为 `admin`。|
| 400      | message_send_error | param to can't be empty  | 请求参数 `to` 是空数组。  | 输入正确的请求参数 `to`。  |
| 400      | message_send_error | param type can't be empty | 请求参数 `type` 是空字符串。   | 输入正确的请求参数 `type`。         |
| 400      | message_send_error | param body can't be empty  | 请求参数 `body` 是空 JSON。   | 输入正确的请求参数 `body`。         |
| 400      | message_send_error | param ext must be JSONObject  | 请求参数 `ext` 类型不正确。  | 输入正确的请求参数 `ext`（JSON 格式）。  |
| 400      | message_send_error | param users can't be empty  | 请求参数 `users` 是空数组。 | 输入正确的请求参数 `users`。每次最多可传 20 个用户 ID。 |
| 400      | message_send_error | params to's size can't exceed limit 3   | 请求参数 `to` 数量超出最大限制 3。 | 输入正确的请求参数 `to`。每次最多能传入 3 个群组 ID。 |
| 400      | message_send_error | message is too large   | 请求体内容中 `body` 和 `ext` 字段的内容过大。 | 限制 `body` 和 `ext` 字段的内容。         |
| 403      | message_send_error | message send reach limit  | 消息发送频率超出限制(默认 1 秒内只允许发送 100 条定向消息) | 限制消息发送频率，详见[文档说明](message_group.html#发送定向消息)。  |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

