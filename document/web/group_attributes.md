# 群属性管理

<Toc />

群组是支持多人沟通的即时通讯系统，本文指导你如何使用环信即时通讯 IM Web SDK 在实时互动 app 中实现群组属性相关功能。

## 技术原理

环信即时通讯 IM Web SDK 提供群组管理，支持你通过调用 API 在项目中实现如下功能：

- 修改群组信息；
- 管理群公告；
- 管理共享文件；

## 前提条件

- 完成 SDK 初始化，详见 [快速开始](quickstart.html)。
- 了解环信即时通讯 IM API 的接口调用频率限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

### 修改群组信息

仅群主和群管理员可以调用 `modifyGroup` 方法修改群组信息，包括群名称、群描述和群组扩展信息，其他成员会收到 `updateInfo` 事件。

群名称的长度限制为 128 个字符。群描述的长度限制为 512 个字符。

示例代码如下：

```javascript
let option = {
    groupId: "groupId",
    groupName: "groupName",
    description: "A description of group",
    ext: "group detail extensions",
};
conn.modifyGroup(option).then(res => console.log(res))
```

### 管理群组头像

自 SDK 4.14.0 开始，支持群组头像功能。

#### 设置群组头像

- 创建群组时，可设置群组头像：

```javascript
conn.createGroupVNext({
    groupName: 'groupname',
    avatar: 'group avatar', // 群组头像 URL
    members: ['user1', 'user2']
})
```

- 创建群组后，若设置群组头像，可调用 [修改群组头像](#修改群组头像) API 设置头像。

#### 修改群组头像

创建群组完成后，群主或管理员可调用 `modifyGroup` 设置或修改群组头像：

```javascript
conn.modifyGroup({
    groupId: 'groupId',
    avatar: 'group avatar url'
})
```

群头像被修改后，其他群成员会收到 `onGroupEvent#updateInfo` 回调：

```javascript
conn.addEventHandler("eventName", {
    onGroupEvent: function (msg) {
        switch (msg.operation) {
            case 'updateInfo':
                console.log(msg)
                break;
        }
    }
})  

```

#### 获取群组头像

群成员可以通过获取群详情的方法，获取群组头像：

```javascript
conn.getGroupInfo({
    groupId: 'groupId'
})
.then((res) => {
    console.log(res)
})
```

### 管理群公告

#### 获取群公告

所有群成员均可调用 `fetchGroupAnnouncement` 方法获取群公告。

示例代码如下：

```javascript
let option = {
    groupId: "groupId"
};
conn.fetchGroupAnnouncement(option).then(res => console.log(res))
```

#### 设置/更新群公告

仅群主和群管理员可以调用 `updateGroupAnnouncement` 方法设置和更新群公告。群公告的长度限制为 512 个字符。

群公告发生变化时，群成员会收到 `updateAnnouncement` 监听事件。

示例代码如下：

```javascript
let option = {
    groupId: "groupId",
    announcement: "A announcement of group"
};
conn.updateGroupAnnouncement(option).then(res => console.log(res))
```

### 管理共享文件

#### 上传共享文件

所有群组成员均可调用 `uploadGroupSharedFile` 方法上传共享文件至群组，单个群共享文件大小限制为 10 MB。上传共享文件后，其他群成员收到 `uploadFile` 事件。

```javascript
let option = {
    groupId: "groupId",
    file: file, // <input type="file"/>获取的文件对象。
    onFileUploadProgress: function(resp) {},   // 上传进度的回调。
    onFileUploadComplete: function(resp) {},   // 上传完成时的回调。
    onFileUploadError: function(e) {},         // 上传失败的回调。
    onFileUploadCanceled: function(e) {}       // 上传取消的回调。
};
conn.uploadGroupSharedFile(option);
```

#### 下载共享文件

所有群成员均可调用 `downloadGroupSharedFile` 方法下载共享文件。

```javascript
let option = {
    groupId: "groupId",
    fileId: "fileId", // 文件 ID。
    onFileDownloadComplete: function(resp) {}, // 下载成功的回调。
    onFileDownloadError: function(e) {},       // 下载失败的回调。
};
conn.downloadGroupSharedFile(option);
```

#### 删除群共享文件

所有群成员均可以调用 `deleteGroupSharedFile` 方法删除群共享文件。删除共享文件后，其他群成员收到 `deleteFile` 事件。

群主和群管理员可删除全部群共享文件，群成员只能删除自己上传的群文件。

示例代码如下：

```javascript
let option = {
    groupId: "groupId",
    fileId: "fileId", // 文件 ID。
};
conn.deleteGroupSharedFile(option).then(res => console.log(res))
```

#### 获取群共享文件列表

所有群成员均可调用 `getGroupSharedFilelist` 方法获取群组的共享文件列表。

```javascript
let option = {
    groupId: "groupId"
};
conn.getGroupSharedFilelist(option).then(res => console.log(res))
```
### 监听群组事件

有关详细信息，请参阅 [监听群组事件](group_manage.html#监听群组事件)。