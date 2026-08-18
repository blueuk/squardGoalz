# 1. Alembic이 뼈대를 잡을 수 있게 Base를 가져옵니다.
from database import Base

# 2. 쪼개놓은 파일들의 실제 이름(sqg_user)에 맞춰 불러옵니다.
from .sqg_users import User

from .CommonCdB import CommonCdB
from .CommonGroupCdB import CommonGroupCdB  
from .TeamAccountL import TeamAccountL
from .TeamArrangeL import TeamArrangeL
from .TeamInfoB import TeamInfoB
from .TeamMemberL import TeamMemberL
from .TeamMemberScoreL import TeamMemberScoreL
from .TeamPaymentL import TeamPaymentL
from .TeamRecordL import TeamRecordL
from .TeamScheduleL import TeamScheduleL
from .TeamStartdiumL import TeamStartdiumL
from .TeamVoteL import TeamVoteL
from .UserB import UserB
from .UserH import UserH    