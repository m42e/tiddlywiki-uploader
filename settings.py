import os

FILES_DIR = "./files/"
MAX_UPLOADS_PER_DAY = 1000
MAX_UPLOADS_PER_HOUR = 100
MAX_UPLOADS_PER_MINUTE = 20
ALLOWED_ORIGINS = ["*"]
NAME_STRATEGY = 'randomstr'
MAX_SIZE_MB = 16

for variable in [item for item in globals() if not item.startswith("__")]:
    NULL = "NULL"
    env_var = os.getenv(variable, NULL).strip()
    if env_var is not NULL:
        try:
            env_var = eval(env_var)
        except Exception:
            pass
    globals()[variable] = env_var if env_var is not NULL else globals()[variable]
