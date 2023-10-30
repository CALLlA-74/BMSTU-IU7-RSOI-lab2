from fastapi import APIRouter, status, Request, Header
from fastapi.responses import Response, JSONResponse

import services as GatewayService
import schemas.dto as schemas
from schemas.responses import ResponsesEnum
from config.config import get_settings

router = APIRouter(prefix='', tags=['Gateway API'])
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/hotels', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaginationResponse.value
            })
async def get_all_hotels(page: int = 0, size: int = 0):
    return (await GatewayService.get_all_hotels(page, size)).json()


@router.get(f'{settings["prefix"]}/me', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.UserInfoResponse.value
            })
async def get_user_info(username: str = Header(alias='X-User-Name')):
    return await GatewayService.get_user_info(username)


@router.get(f'{settings["prefix"]}/loyalty', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.LoyaltyInfoResponse.value
            })
async def get_loyalty(username: str = Header(alias='X-User-Name')):
    return await GatewayService.get_loyalty(username)


@router.get(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationsResponse.value
            })
async def get_reservations(username: str = Header(alias='X-User-Name')):
    return await GatewayService.get_reservations(username)


@router.get(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value,
                status.HTTP_404_NOT_FOUND: ResponsesEnum.ErrorResponse.value
            })
async def get_reservation_by_uid(reservaionUid: str, username: str = Header(alias='X-User-Name')):
    reservaion = await GatewayService.get_reservation_by_uid(reservaionUid, username)
    if reservaion is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=schemas.ErrorResponse().model_dump())


"""@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponsesEnum.CreatedNewPersonResponce.value,
                 status.HTTP_400_BAD_REQUEST: ResponsesEnum.InvalidDataResponse.value,
             })
async def create_person(data: PersonDTO = None, db: Session = Depends(app_db.get_db)):
    person = PersonService.create_person(data, db)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/api/v1/persons/{person.id}"}
    )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponsesEnum.PersonByIDDeleteResponse.value
               })
async def delete_person(id: int = None, db: Session = Depends(app_db.get_db)):
    PersonService.delete_person(id, db)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )"""
