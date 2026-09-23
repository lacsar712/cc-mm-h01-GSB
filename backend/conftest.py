import os
import tempfile

# 测试用临时 SQLite，必须在导入 app.main（其中创建引擎）之前设置
_db_fd, _db_path = tempfile.mkstemp(prefix="methane-test-", suffix=".db")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"
os.environ.setdefault("JWT_SECRET", "mine-methane-test-secret")
