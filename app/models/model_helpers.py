from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.functions import FunctionElement
from sqlalchemy.types import DateTime


class utcnow(FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "sqlite")
def sqlite_utcnow(element, compiler, **kw):
    return r"(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))"
