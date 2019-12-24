# super Table 

## Attr
|name|comment|example|
|------|------|------|
|permsEdit|编辑权限|permsEdit="user.alert"|
|permsDelete|删除权限|permsDelete="user.delete"|
|permsAdd|添加权限|permsAdd="user.create"|
|expand|下拉列列表|:expand="true"|
|data|表格数据|{`content`: __Array__, `labels`: __Object__, `options`: __Object__, ~~`pageRequest`:Object~~}|
|dataFormRules|表格编辑规则|{username: {message: "请输入用户名",trigger: "blur"}}|

## method
|name|comment|
|------|------|
|select|获取表格数据后|
|edit|编辑数据后|
|delete|删除数据后|
|search|查询数据后|


## labels - Object Attr
| attr         | comment                                     | type     | default             | example |
|--------------|---------------------------------------------|----------|---------------------|--|
| label        | 列显示文字                                  | String   | ""                  |
| user_edit    | 是否编辑时需要编辑                          | bool     | True                |
| edit         | 编辑时候展示的控件                          | String   | "el-input"          |
| edit_slot    | 使用特殊格式显示的编辑列                    | bool     | false               |
| edit_formatt | 编辑前原有数据格式化                        | function | val => {return val} |
| slot         | 使用特殊格式显示的列                        | bool     | false               | slot的数据用filter:{} {{data\| filter method}} 进行格式化
| show_props   | 显示控件的属性值                            | Object   | {}                  | {text: "hello world"} |
| show_list    | 是否显示在table                             | bool     | true                |
