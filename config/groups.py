from jrdbnntt_com.util.acl import GroupManager

groups = GroupManager(
    db_groups=[
        GroupManager.USER
    ],
    extra_groups=[
        GroupManager.ADMIN
    ]
)