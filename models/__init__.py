# 1. Alembic이 뼈대를 잡을 수 있게 Base를 가져옵니다.
from database import Base

# 2. 쪼개놓은 파일들의 실제 이름(sqg_user)에 맞춰 불러옵니다.
from .sqg_users import User