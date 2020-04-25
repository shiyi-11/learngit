# coding=utf8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app, db

app = create_app('develop')

# 创建脚本管理器
manager = Manager(app)
# 让迁移时，app和数据库建立关联
Migrate(app, db)
# 增加db脚本命令
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
	# app.run()
	manager.run()