# TikTok Profile Fields Extractable via curl

Source: `__UNIVERSAL_DATA_FOR_REHYDRATION__` → `__DEFAULT_SCOPE__` → `webapp.user-detail` → `userInfo`

## user object keys (observed 2025)

| Key | Type | Description |
|-----|------|-------------|
| `uniqueId` | string | @username |
| `nickname` | string | Display name |
| `signature` | string | Bio text |
| `verified` | bool | Blue checkmark |
| `id` | string | Numeric user ID |
| `secUid` | string | Secure UID (needed for API calls) |
| `shortId` | string | Short numeric ID (often empty) |
| `createTime` | int | Unix timestamp of account creation |
| `nickNameModifyTime` | int | Unix timestamp of last nickname change |
| `uniqueIdModifyTime` | int | Unix timestamp of last username change |
| `language` | string | Account language (e.g., "id") |
| `region` | string | Account region (may differ from page region) |
| `privateAccount` | bool | Is account private |
| `secret` | bool | Secret account flag |
| `openFavorite` | bool | Are favorites public |
| `relation` | int | Relationship to viewer (0=none) |
| `roomId` | string | Current LIVE room ID (empty if not live) |
| `isOrganization` | int | Organization/business account flag |
| `isADVirtual` | bool | Ad virtual account |
| `isEmbedBanned` | bool | Embed banned |
| `ftc` | bool | FTC compliance flag |
| `ttSeller` | bool | Official TikTok Shop seller |
| `canExpPlaylist` | bool | Can create playlists |
| `profileEmbedPermission` | int | Embed permission level |
| `commentSetting` | int | Comment permissions (0=everyone) |
| `duetSetting` | int | Duet permissions (0=everyone) |
| `stitchSetting` | int | Stitch permissions (0=everyone) |
| `downloadSetting` | int | Download permissions |
| `followingVisibility` | int | Following list visibility |
| `suggestAccountBind` | bool | Account bind suggestion |

## commerceUserInfo sub-object

| Key | Type | Description |
|-----|------|-------------|
| `commerceUser` | bool | Is commerce/shop user |
| `category` | string | Shop category (e.g., "Clothing & Accessories") |
| `categoryButton` | bool | Category button visible |
| `downLoadLink.android` | string | App download link (Android) |
| `downLoadLink.ios` | string | App download link (iOS) |

## stats object

| Key | Type | Description |
|-----|------|-------------|
| `followerCount` | int | Number of followers |
| `followingCount` | int | Number following |
| `heartCount` | int | Total likes received |
| `heart` | int | Same as heartCount |
| `videoCount` | int | Number of public videos |
| `diggCount` | int | Number of videos user has liked |

## profileTab sub-object

| Key | Type | Description |
|-----|------|-------------|
| `showMusicTab` | bool | Music tab visible |
| `showQuestionTab` | bool | Q&A tab visible |
| `showPlayListTab` | bool | Playlist tab visible |

## avatars

| Key | Description |
|-----|-------------|
| `avatarLarger` | High-res profile pic URL |
| `avatarMedium` | Medium profile pic URL |
| `avatarThumb` | Thumbnail profile pic URL |

## Notes

- `itemList` (video list) is typically **empty** when fetched via curl due to bot detection
- `botType: "others"` and `needFix: true` indicate bot detection was triggered
- Profile stats remain accurate even when video list is withheld
- The page region in `webapp.app-context` may show "SG" even for Indonesian accounts (CDN routing)
