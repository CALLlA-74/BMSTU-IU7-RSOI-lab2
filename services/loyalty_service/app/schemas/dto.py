from pydantic import BaseModel


class LoyaltyInfoResponse(BaseModel):
    status: str
    discount: int
    reservationCount: int


class LoyaltyInfoRequest(BaseModel):
    status: str | None = None
    discount: int | None = None
    reservationCount: int | None = None
