#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vincent'

import os
import logging.handlers
import click

from app.utils.loggers import log_hander
import sys
from app import create_app, db
from app.models.users import User

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


reload(sys)
sys.setdefaultencoding("utf-8")

default_config_name=''

app = create_app(default_config_name)

if log_hander not in app.logger.handlers:
    app.logger.addHandler(log_hander)

app.logger.setLevel(logging.DEBUG)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User
    )



# # 加载一些命令行工具包
# manager = Manager(app)
#
# def make_shell_context():
#     return dict(app=app, db=db, User=User)
# # 命令行工具- 新增一个命令行参数 shell ，自动加载 对象
# manager.add_command('shell', Shell(make_context=make_shell_context))
#
# # 命令行工具- 添加一个命令行参数 db 加载数据库迁移命令
# manager.add_command('db', MigrateCommand)


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('初始化数据库-开始')
    db.drop_all()
    db.create_all()
    click.echo('初始化数据库-结束')

@app.cli.command()
def test():
    """运行这个单元测试"""

    import unittest
    default_config_name='TestConfig'

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# if __name__ == '__main__':
#     manager.run()


