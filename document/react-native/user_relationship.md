# 管理用户关系

<Toc />

用户登录后，可进行添加联系人、获取好友列表等操作。

SDK 提供用户关系管理功能，包括好友列表管理和黑名单管理：

- 好友列表管理：查询好友列表、请求添加好友、接受好友请求、拒绝好友请求、删除好友和设置好友备注等操作。
- 黑名单管理：查询黑名单列表、添加用户至黑名单以及将用户移除黑名单等操作。

此外，环信即时通讯 IM 默认支持陌生人之间发送单聊消息，即无需添加好友即可聊天。若仅允许好友之间发送单聊消息，你需要在 [环信即时通讯云控制台](https://console.easemob.com/user/login) [开启好友关系检查](/product/enable_and_configure_IM.html#好友关系检查)。该功能开启后，SDK 会在用户发起单聊时检查好友关系，若用户向陌生人发送单聊消息，SDK 会提示错误码 221。

## 技术原理

环信即时通讯 IM React Native SDK 提供 `ChatContactManager` 类实现好友的添加移除，黑名单的添加移除等功能。主要方法如下：

- `addContact` 请求添加好友。
- `deleteContact` 删除好友。
- `acceptInvitation` 接受好友请求。
- `declineInvitation` 拒绝好友请求。
- `getAllContactsFromServer` 从服务器获取好友列表。
- `getAllContactsFromDB` 从缓存获取好友列表。
- `addUserToBlockList` 添加用户到黑名单。
- `removeUserFromBlockList` 将用户从黑名单移除。
- `getBlockListFromServer` 从服务器获取黑名单列表。

## 前提条件

开始前，请确保满足以下条件：

- 完成 SDK 初始化，并连接到服务器，详见 [初始化](initialization.html)文档。
- 了解环信即时通讯 IM 的使用限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

### 添加好友

1. 添加监听。

```typescript
      const listener = {
        onContactAdded: (userName: string) => {
          // 联系人已添加。用户 B 向用户 A 发送好友请求，用户 A 接受该请求，用户 A 收到该事件，而用户 B 收到 `onFriendRequestAccepted` 事件。
        },
        onContactDeleted: (userName: string) => {
          // 联系人被删除。用户 B 将用户 A 从联系人列表上删除，用户 A 收到该事件。
        },
        onContactInvited: (userName: string, reason?: string) => {
          // 接收到好友请求。用户 B 向用户 A 发送好友请求，用户 A 收到该事件。
        },
        onFriendRequestAccepted: (userName: string) => {
          // 对方接受了好友请求。用户 A 向用户 B 发送好友请求，用户 B 收到好友请求后，同意加好友，则用户 A 收到该事件。
        },
        onFriendRequestDeclined: (userName: string) => {
          // 对方拒绝了好友请求。用户 A 向用户 B 发送好友请求，用户 B 收到好友请求后，拒绝加好友，则用户 A 收到该事件。
        },
      } as ChatContactEventListener;
      // 添加联系人监听器
      ChatClient.getInstance().contactManager.removeContactListener(listener);
      // 移除联系人监听器
      ChatClient.getInstance().contactManager.addContactListener(listener);
```

2. 用户添加指定用户为好友。

```typescript
// 用户 ID
const userId = "foo";
// 申请加为好友的理由
const reason = "Request to add a friend.";
ChatClient.getInstance()
  .contactManager.addContact(userId, reason)
  .then(() => {
    console.log("request send success.");
  })
  .catch((reason) => {
    console.log("request send fail.", reason);
  });
```

3. 对端用户通过 `onContactInvited` 监听收到好友请求，确认是否成为好友。

   - 若接受好友请求，需调用 `acceptInvitation` 方法。请求方收到 `onFriendRequestAccepted` 事件。
，双方都收到 `onContactAdded` 事件。

```typescript
// 用户 ID
const userId = "bar";
ChatClient.getInstance()
  .contactManager.acceptInvitation(userId)
  .then(() => {
    console.log("accept request success.");
  })
  .catch((reason) => {
    console.log("accept request fail.", reason);
  });
```

```typescript
const contactEventListener = new (class implements ChatContactEventListener {
  that: any;
  constructor(parent: any) {
    this.that = parent;
  }
  onContactInvited(userId: string, reason?: string): void {
    console.log(`onContactInvited: ${userId}, ${reason}: `);
  }
})(this);
ChatClient.getInstance().contactManager.addContactListener(
  contactEventListener
);
```

- 若拒绝好友请求，需调用 `declineInvitation` 方法。请求方收到 `onFriendRequestDeclined` 事件。

```typescript
// 用户 ID
const userId = "bar";
ChatClient.getInstance()
  .contactManager.declineInvitation(userId)
  .then(() => {
    console.log("decline request success.");
  })
  .catch((reason) => {
    console.log("decline request fail.", reason);
  });
```

```typescript
const contactEventListener = new (class implements ChatContactEventListener {
  that: any;
  constructor(parent: any) {
    this.that = parent;
  }
  onFriendRequestDeclined(userId: string): void {
    console.log(`onFriendRequestDeclined: ${userId}: `);
  }
})(this);
ChatClient.getInstance().contactManager.addContactListener(
  contactEventListener
);
```

### 删除好友

删除好友时会同时删除对方联系人列表中的该用户，建议执行双重确认，以免发生误删操作。删除操作不需要对方同意或者拒绝。

```typescript
// 用户 ID
const userId = "tom";
// 是否保留聊天会话
const keepConversation = true;
ChatClient.getInstance()
  .contactManager.deleteContact(userId, keepConversation)
  .then(() => {
    console.log("remove success.");
  })
  .catch((reason) => {
    console.log("remove fail.", reason);
  });
```

调用 `deleteContact` 删除好友后，对方会收到 `onContactDeleted` 事件。

#### 设置好友备注

自 1.3.0 版本开始，你可以调用 `setContactRemark` 方法设置单个好友的备注。

好友备注的长度不能超过 100 个字符。

```typescript
ChatClient.getInstance()
  .contactManager.setContactRemark({ userId: "xxx", remark: "user remark" })
  .then()
  .catch();
```

#### 从服务端获取好友列表

自 1.3.0 版本开始，你可以调用 `fetchAllContacts` 或者 `fetchContacts` 方法从服务器一次性或分页获取好友列表，其中每个好友对象包含好友的用户 ID 和好友备注。

- 一次性获取服务端好友列表。

```typescript
ChatClient.getInstance()
  .contactManager.fetchAllContacts()
  .then((contactList: Contact[]) => {
    // todo: 从服务器返回所有的联系人列表。包括好友备注信息。
  })
  .catch();
```

- 分页获取服务端好友列表。

```typescript
// cursor 数据获取的起始位置，获取第一页设置为 `空字符串` 或者 `undefined`。
// pageSize 获取每页的最大数目,取值范围为 [1,50]。
ChatClient.getInstance()
  .contactManager.fetchContacts({
    cursor: undefined,
    pageSize: 20,
  })
  .then((contactList: Contact[]) => {
    // todo: 从服务器返回所有的联系人列表。包括好友备注信息。
  })
  .catch();
```

此外，你也可以调用 `getAllContactsFromServer` 方法从服务器获取所有好友的列表，该列表只包含好友的用户 ID。

```typescript
 ChatClient.getInstance()
   .contactManager.getAllContactsFromServer()
   .then((value) => {
     console.log("get contact success.", value);
   })
   .catch((reason) => {
     console.log("get contact fail.", reason);
   });
 ```

#### 从本地获取好友列表

自 1.3.0 版本开始，你可以调用 `getContact` 方法从本地获取单个好友的用户 ID 和好友备注；你也可以调用 `getAllContacts` 方法一次性获取整个好友列表，其中每个好友对象包含好友的用户 ID 和好友备注。

:::tip
需要从服务器获取好友列表之后，才能从本地获取到好友列表。
:::

- 获取本地单个好友。

```typescript
// userId 获取指定用户的好友备注。
ChatClient.getInstance()
  .contactManager.getContact(userId)
  .then((contactList: Contact | undefined) => {
    // todo: 获取好友备注对象。
  })
  .catch();
```

- 一次性获取本地好友列表。

```typescript
ChatClient.getInstance()
  .contactManager.getAllContacts()
  .then((contactList: Contact[]) => {
    // todo: 从服务器返回所有的联系人列表。包括好友备注信息。
  })
  .catch();
```

此外，你也可以调用 `getAllContactsFromDB` 方法从本地一次性获取所有好友的列表，该列表只包含好友的用户 ID。

```typescript
 ChatClient.getInstance()
   .contactManager.getAllContactsFromDB()
   .then((value) => {
     console.log("get contact success.", value);
   })
   .catch((reason) => {
     console.log("get contact fail.", reason);
   });
 ```

### 将用户加入黑名单

你可以调用 `addUserToBlockList` 添加用户到黑名单。用户被加入黑名单后，无法向你发送消息，也无法发送好友申请。

用户可以将任何其他用户添加到黑名单列表，无论该用户是否是好友。好友被加入黑名单后仍在好友列表上显示。

```typescript
// 用户 ID
const userId = "tom";
// 将用户添加到黑名单
ChatClient.getInstance()
  .contactManager.addUserToBlockList(userId)
  .then(() => {
    console.log("add block list success.");
  })
  .catch((reason) => {
    console.log("add block list fail.", reason);
  });
```

### 查看当前用户黑名单列表

1. 使用本地缓存获取黑名单列表

```typescript
ChatClient.getInstance()
  .contactManager.getBlockListFromDB()
  .then((list) => {
    console.log("get block list success: ", list);
  })
  .catch((reason) => {
    console.log("get block list fail.", reason);
  });
```

2. 通过服务器获取黑名单列表

从服务器获取黑名单列表之后，才能从本地数据库获取到黑名单列表。

```typescript
ChatClient.getInstance()
  .contactManager.getBlockListFromServer()
  .then((list) => {
    console.log("get block list success: ", list);
  })
  .catch((reason) => {
    console.log("get block list fail.", reason);
  });
```

### 从黑名单中移除用户

被移出黑名单后，用户发送消息等行为将恢复。

```typescript
// 用户 ID
const userId = "tom";
// 将用户从黑名单移除
ChatClient.getInstance()
  .contactManager.removeUserFromBlockList(userId)
  .then((list) => {
    console.log("remove user to block list success: ", list);
  })
  .catch((reason) => {
    console.log("remove user to block list fail.", reason);
  });
```