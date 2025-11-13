"""
App initialization hooks.
"""

import os


def _init_mysql_driver() -> None:
    """
    Ensure PyMySQL masquerades as MySQLdb when MySQL is enabled.
    """
    use_mysql = os.environ.get('USE_MYSQL', 'False').lower() == 'true'
    if not use_mysql:
        return

    try:
        import pymysql
    except ModuleNotFoundError:  # pragma: no cover - defensive guard
        return

    pymysql.install_as_MySQLdb()


_init_mysql_driver()

