from pydantic import BaseModel

class GeneralStatus(BaseModel):
    """
    FastAPIの非エラー時通常応答
    """
    status: int
    message: str
    detail: str = ""
