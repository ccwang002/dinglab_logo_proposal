import sys
from pathlib import Path
from fabric.api import local, task, lcd, env
from fabric.contrib.console import confirm
from fabric.utils import abort

src_p = Path(env.real_fabfile).parent / 'src'


@task
def start_smtp():
    local('python3 -m smtpd -n -c DebuggingServer localhost:1025')


@task
def backup():
    cmd_dumpdata = 'python manage.py dumpdata '
    with lcd(src_p.as_posix()):
        local(
            cmd_dumpdata + 'users proposals | '
            'tee ../db_dump/user_proposals.json'
        )
        local(
            cmd_dumpdata + 'reviews | '
            'tee ../db_dump/reviews.json'
        )


@task
def cloc():
    with lcd(src_p.parent.as_posix()):
        local(
            'cloc --exclude-dir=vendors,migrations,assets ./src'
        )
