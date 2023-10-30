from pydantic import BaseModel, validator
from typing import Literal, Annotated, List
from uuid import UUID
from datetime import datetime, date


class LoyaltyInfoResponse(BaseModel):
    status: Literal['BRONZE', 'SILVER', 'GOLD']
    discount: int
    reservationCount: int


class HotelInfo(BaseModel):
    hotelUid: UUID
    name: str
    fullAddress: str
    stars: int


class HotelResponse(BaseModel):
    hotelUid: UUID
    name: str
    country: str
    city: str
    address: str
    stars: int
    price: float


class PaginationResponse(BaseModel):
    page: int
    pageSize: int
    totalElements: int
    items: List[HotelResponse]


class PaymentInfo(BaseModel):
    status: Literal['PAID', 'RESERVED', 'CANCELED']
    price: float


class CreateReservationRequest(BaseModel):
    hotel: HotelInfo
    startDate: date
    endDate: date

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


class CreateReservationResponse(BaseModel):
    reservationUid: UUID
    hotelUid: UUID
    startDate: date
    endDate: date
    discount: int
    status: Literal['PAID', 'RESERVED', 'CANCELED']
    payment: PaymentInfo

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


class ReservationResponse(BaseModel):
    reservationUid: UUID
    hotel: HotelInfo
    startDate: date
    endDate: date
    status: Literal['PAID', 'RESERVED', 'CANCELED']
    payment: PaymentInfo

    @validator("startDate", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


class UserInfoResponse(BaseModel):
    reservations: List[ReservationResponse]
    loyalty: LoyaltyInfoResponse


class ErrorResponse(BaseModel):
    message: str = 'not found'


class ErrorDescription(BaseModel):
    field: str
    error: str


class ValidationErrorResponse(BaseModel):
    message: str
    errors: List[ErrorDescription]
