# 创建和管理群组及监听群组事件

<Toc />

群组是支持多人沟通的即时通讯系统，本文介绍如何使用环信即时通讯 IM Web SDK 在实时互动 app 中创建和管理群组，并实现群组相关功能。

如需查看消息相关内容，参见 [消息管理](message_overview.html)。

## 技术原理

环信即时通讯 IM Web SDK 支持你通过调用 API 在项目中实现以下群组管理功能：

- 创建、解散群组
- 获取群组详情
- 获取群成员列表
- 获取群组列表：获取加入和创建的群组列表和公开群列表
- 查询当前用户已加入的群组数
- 屏蔽群消息、解除屏蔽群消息和检查当前用户是否已屏蔽群消息
- 监听群组事件

## 前提条件

开始前，请确保满足以下条件：

- 完成 SDK 初始化，详见 [快速开始](quickstart.html)。
- 了解环信即时通讯 IM API 的接口调用频率限制，详见 [使用限制](/product/limitation.html)。
- 了解群组和群成员数量限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

### 创建群组

1、调用 `createGroupVNext` 方法新建群组，设置群组参数。

群组分为私有群和公开群。私有群无法搜索到，公开群可通过群 ID 搜索到。

创建群组时，需设置以下参数：

| 参数                | 类型   | 描述          |
| :------------- | :----- | :--------------------------------------------- |
| `groupName` | String | 群组名称。 |
| `avatar` | String | 群组头像。 |
| `description` | String | 群组描述。 |
| `members` | `Array<string>` | 群成员的用户 ID 组成的数组，不包含群主的用户 ID。 |
| `isPublic` | Boolean | 是否为公开群：<br/> - `true`：是；<br/> - `false`：否。该群组为私有群。 |
| `needApprovalToJoin` | Boolean | 入群申请是否需群主或管理员审批：<br/> - `true`：需要；<br/> - `false`：不需要。<br/>由于私有群不支持用户申请入群，只能通过邀请方式进群，因此该参数仅对公开群有效，即 `isPublic` 设置为 `true` 时，对私有群无效。 |
| `allowMemberToInvite` | Boolean | 是否允许普通群成员邀请人入群：<br/> - `true`：允许；<br/> - `false`：不允许。只有群主和管理员才可以向群组添加用户。<br/>该参数仅对私有群有效，即 `isPublic` 设置为 `false` 时， 因为公开群（isPublic：`true`）仅支持群主和群管理员邀请人入群，不支持普通群成员邀请人入群。 |
| `inviteNeedConfirm` | Boolean | 邀请加群时是否需要受邀用户确认：<br/> - `true`：受邀用户需同意才会加入群组；<br/> - `false`：受邀用户直接加入群组，无需确认。 |
| `maxMemberCount` | Int | 群组最大成员数，默认为 `200`。不同套餐支持的人数上限不同，详见  [IM 套餐包功能详情](/product/product_package_feature.html)。 |
| `extension` | string | 群组扩展信息，例如可以给群组添加业务相关的标记，不要超过 8 KB。|


创建群组的示例代码如下：

```javascript
conn.createGroupVNext({
    groupName: 'groupname',
    avatar: 'group avatar',
    description: 'this is my group',
    members: ['user1', 'user2'],
    isPublic: true,
    needApprovalToJoin: false,
    allowMemberToInvite: true,
    inviteNeedConfirm: false,
    maxMemberCount: 200,
    extension: JSON.stringify({info: 'group info'})
})
.then((res) => {
    console.log(res)
})
```

2、邀请用户入群。

公开群只支持群主和管理员邀请用户入群。对于私有群，除了群主和群管理员，群成员是否也能邀请其他用户进群取决于 `allowinvites` 选项的设置。

邀请用户加群流程如下：

1. 群成员调用 `inviteUsersToGroup` 方法邀请用户入群。

```javascript
conn.inviteUsersToGroup({ groupId: "groupId", users: ["user1", "user2"] });
```

2. 受邀用户会收到 `inviteToJoin` 事件，自动进群或确认是否加入群组。

   入群邀请是否需受邀用户确认取决于群组选项 `inviteNeedConfirm` 的设置：

   - `inviteNeedConfirm` 设置为 `false` 时，受邀用户直接进群，无需确认，群组所有成员会收到 `membersPresence` 事件。
   - `inviteNeedConfirm` 设置为 `true` 时，受邀用户需确认是否加入群组。

     - 受邀用户同意加入群组，需要调用 `acceptGroupJoinRequest` 方法。用户加入成功后，邀请人会收到 `acceptInvite` 事件，群组所有成员会收到 `membersPresence` 事件。

     ```javascript
     conn.acceptGroupInvite({ invitee: "myUserId", groupId: "groupId" });
     ```

     - 受邀用户拒绝入群，需要调用 `rejectGroupJoinRequest` 方法。邀请人会收到 `rejectInvite` 事件。

     ```javascript
     conn.rejectGroupInvite({ invitee: "myUserId", groupId: "groupId" });
     ```

3、用户加入群组后，可以收发群消息。

### 解散群组

仅群主可以调用 `destroyGroup` 方法解散群组。群组解散时，其他群组成员收到 `destroy` 事件并被踢出群组。

示例代码如下：

```javascript
let option = {
  groupId: "groupId",
};
conn.destroyGroup(option).then((res) => console.log(res));
```

### 获取群组详情信息

所有群成员均可调用 `getGroupInfo` 方法根据群组 ID 获取单个或多个群组的详情，包括群组 ID、群组名称、群组描述、群组基本属性、群成员列表、是否已屏蔽群组消息以及群组是否禁用。

:::tip
对于公有群，用户即使不加入群也能获取群组详情，而对于私有群，用户只有加入了群组才能获取群详情。
:::

示例代码如下：

```javascript
let option = {
  // 单个群组 ID 或群组 ID 数组。
  groupId: "groupId",
};
conn.getGroupInfo(option).then((res) => {
  console.log(res);
});
```

### 获取群成员列表

自 SDK 4.15.0 开始，所有群成员均可调用 `getGroupMembers` 方法获取群成员信息，包括用户 ID 和用户角色。原方法 `listGroupMembers` 废弃。

```javascript
conn
// limit：每页获取的群成员数量，取值范围为 [1,50]，默认值为 50。
  .getGroupMembers({ cursor: "", limit: 50, groupId: "groupId" })
  .then((res) => {
    console.log(res);
  });
```

### 获取群组列表

- 用户可以调用 `getJoinedGroups` 方法获取当前用户加入和创建的群组列表，代码如下：

```javascript
conn.getJoinedGroups({
  pageNum: 0,
  pageSize: 20,
  needAffiliations: true,
  needRole: true,
});
```

- 用户还可以分页获取公开群列表：

```javascript
let option = {
  limit: 20,
  cursor: cursor,
};
conn.getPublicGroups(option).then((res) => console.log(res));
```

### 查询当前用户已加入的群组数

自 4.15.1 版本开始，你可以调用 `getJoinedGroupsCount` 方法从服务器获取当前用户已加入的群组数量。单个用户可加入群组数量的上限取决于订阅的即时通讯的套餐包，详见 [IM 套餐包功能详情](/product/product_package_feature.html)。

```javascript
conn.getJoinedGroupsCount().then((res) => {
        console.log(res.data);
});
```

### 屏蔽群消息

自 4.15.1 版本开始，群成员可以调用 `blockGroupMessage` 方法屏蔽群消息。屏蔽群消息后，该成员不再从指定群组接收群消息，群主和群管理员不能进行此操作。示例代码如下：

```javascript
conn.blockGroupMessage({ groupId: 'groupId' });
```

### 解除屏蔽群消息

自 4.15.1 版本开始，群成员可以调用 `unblockGroupMessage` 方法解除屏蔽群消息。示例代码如下：

```javascript
conn.unblockGroupMessage({ groupId: 'groupId' });
```

### 检查当前用户是否已屏蔽群消息

自 4.15.1 版本开始，群成员可以调用 `getGroupInfo` 方法检查自己是否屏蔽了该群的消息。示例代码如下：

```javascript
conn.getGroupInfo({ groupId: 'groupId' }).then((res) => {
        console.log(res.data[0].shieldgroup);
});
```

### 监听群组事件

SDK 提供 `addEventHandler` 方法用于注册监听事件。开发者可以通过设置此监听，获取群组中的事件。

示例代码如下：

```javascript
// 创建一个群组事件监听器
// 在该方法的举例中，用户 A 表示当前用户。
conn.addEventHandler("eventName", {
  onGroupEvent: function (msg) {
    switch (msg.operation) {
      // 有新群组创建。群主的其他设备会收到该回调。
      case "create":
        break;
      // 关闭群组一键禁言。群组所有成员（除操作者外）会收到该回调。
      case "unmuteAllMembers":
        break;
      // 开启群组一键禁言。群组所有成员（除操作者外）会收到该回调。
      case "muteAllMembers":
        break;
      // 有成员从群白名单中移出。被移出的成员及群主和群管理员（除操作者外）会收到该回调。
      case "removeAllowlistMember":
        break;
      // 有成员添加至群白名单。被添加的成员及群主和群管理员（除操作者外）会收到该回调。
      case "addUserToAllowlist":
        break;
      // 删除群共享文件。群组所有成员会收到该回调。
      case "deleteFile":
        break;
      // 上传群共享文件。群组所有成员会收到该回调。
      case "uploadFile":
        break;
      // 删除群公告。群组所有成员会收到该回调。
      case "deleteAnnouncement":
        break;
      // 更新群公告。群组所有成员会收到该回调。
      case "updateAnnouncement":
        break;
      // 更新群组信息，如群组名称和群组描述。群组所有成员会收到该回调。
      case "updateInfo":
        break;  
      // 有成员被移出禁言列表。被解除禁言的成员及群主和群管理员（除操作者外）会收到该回调。
      case "unmuteMember":
        break;
      // 有群组成员被加入禁言列表。被禁言的成员及群主和群管理员（除操作者外）会收到该回调。
      case "muteMember":
        break;
      // 有管理员被移出管理员列表。群主、被移除的管理员和其他管理员会收到该回调。
      case "removeAdmin":
        break;
      // 设置管理员。群主、新管理员和其他管理员会收到该回调。
      case "setAdmin":
        break;
      // 转让群组。新群主会收到该回调。
      case "changeOwner":
        break;
      // 群组所有者和管理员拉用户进群时，无需用户确认时会触发该回调。被拉进群的用户会收到该回调。
      case "directJoined":
        break;
      // 群成员（单个）退群。除退群成员外，其他群成员会收到该回调。
      case "memberAbsence":
        break;
      // 群成员（单个或多个）退群。除退群成员外，其他群成员会收到该回调。
      case "membersAbsence":
        break;
      // 用户（单个）加群。除新成员外，其他群成员会收到该回调。
      case "memberPresence":
        break;
      // 用户（单个或多个）加群。除新成员外，其他群成员会收到该回调。
      case "membersPresence":
        break; 
      // 用户被移出群组。被踢出群组的成员会收到该回调。
      case "removeMember":
        break;
      // 当前用户的入群邀请被拒绝。邀请人会收到该回调。例如，用户 B 拒绝了用户 A 的入群邀请，用户 A 会收到该回调。
      case "rejectInvite":
        break;
      // 当前用户的入群邀请被接受。邀请人会收到该回调。例如，用户 B 接受了用户 A 的入群邀请，则用户 A 会收到该回调。
      case "acceptInvite":
        break;
      // 当前用户收到了入群邀请。受邀用户会收到该回调。例如，用户 B 邀请用户 A 入群，则用户 A 会收到该回调。
      case "inviteToJoin":
        break;
      // 当前用户的入群申请被拒绝。申请人会收到该回调。例如，用户 B 拒绝用户 A 的入群申请后，用户 A 会收到该回调。
      case "joinPublicGroupDeclined":
        break;
      // 当前用户的入群申请被接受。申请人会收到该回调。例如，用户 B 接受用户 A 的入群申请后，用户 A 会收到该回调。
      case "acceptRequest":
        break;
      // 当前用户发送入群申请。群主和群管理员会收到该回调。
      case "requestToJoin":
        break;
      // 群组被解散。群主解散群组时，所有群成员均会收到该回调。
      case "destroy":
        break;
      // 设置群成员的自定义属性。群组内其他成员均会收到该回调。
      case "memberAttributesUpdate":
        break;  
      default:
        break;
    }
  },
});
```
