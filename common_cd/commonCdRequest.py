from pydantic import BaseModel
from typing import Optional

class CommonGroupCdSearchRequest(BaseModel):
    group_cd: Optional[str] = None
    group_name: Optional[str] = None
    use_yn: str = 'Y'

class CommonGroupCdInsertRequest(BaseModel):
    group_cd: str
    group_name: str
    use_yn: str = 'Y'

class CommonGroupCdUpdateRequest(BaseModel):
    group_cd: str
    group_name: Optional[str] = None
    use_yn: Optional[str] = None
    end_date: Optional[str] = None

class CommonCdSearchRequest(BaseModel):
    group_cd: str
    code: Optional[str] = None
    use_yn: str = 'Y'

class CommonCdInsertRequest(BaseModel):
    group_cd: str
    code: str
    code_name: str
    code_seq: int
    reference_1: Optional[str] = None
    reference_2: Optional[str] = None
    reference_3: Optional[str] = None
    reference_4: Optional[str] = None
    use_yn: str = 'Y'

class CommonCdUpdateRequest(BaseModel):
    group_cd: str
    code: str
    code_name: Optional[str] = None
    code_seq: Optional[int] = None
    reference_1: Optional[str] = None
    reference_2: Optional[str] = None
    reference_3: Optional[str] = None
    reference_4: Optional[str] = None
    use_yn: Optional[str] = None

