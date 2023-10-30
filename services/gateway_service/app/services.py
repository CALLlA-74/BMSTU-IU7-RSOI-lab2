from fastapi import Request, Response, status, HTTPException
from config.config import get_settings
from typing import Final
from schemas import dto as schemas
import serviceRequests

username_in_header: Final = 'X-User-Name'
settings = get_settings()


async def get_all_hotels(page: int, size: int):
    url = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}/{settings['prefix']}" \
          f"/hotels&page={page}&size={size}"
    return serviceRequests.get(url).json()


async def get_user_info(username: str):
    loyalty_response = await get_loyalty(username)
    reservation_response = await get_reservations(username)
    return schemas.UserInfoResponse(reservations=reservation_response, loyalty=loyalty_response)


async def get_reservations(username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"/{settings['prefix']}/reservations"
    reservation_response = serviceRequests.get(url_reserv_serv, headers={'X-User-Name': username})
    if reservation_response is None or reservation_response.status_code != status.HTTP_200_OK:
        return []
    return reservation_response.json()


async def get_reservation_by_uid(reservaionUid: str, username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"/{settings['prefix']}/reservations/{reservaionUid}"
    reservation_response = serviceRequests.get(url_reserv_serv, headers={'X-User-Name': username})
    if reservation_response is None or reservation_response.status_code != status.HTTP_200_OK:
        return None
    return reservation_response.json()


async def create_reservation(reservRequest: schemas.CreateReservationRequest, username: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}"
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    header = {'X-User-Name': username}
    resp = serviceRequests.get(url_reserv_serv + f'{settings["prefix"]}/hotels/{reservRequest.hotelUid}')

    if resp is None or resp.status_code != status.HTTP_200_OK:
        return None
    hotel_resp: schemas.HotelResponse = resp
    cost = (reservRequest.endDate - reservRequest.startDate)*hotel_resp.price
    loyalty_info: schemas.LoyaltyInfoResponse = (await get_loyalty(username))

    if loyalty_info is None:
        return Non

    cost *= (0.01*(100-loyalty_info.discount))
    resp = serviceRequests.post(url_payment_serv + f'{settings["prefix"]}/payments', headers={'X-Payment-Price': cost})

    if resp is None or resp.status_code != status.HTTP_200_OK:
        return Non

    pay_info: schemas.PaymentInfo = resp
    resp = serviceRequests.patch(url_loyalty_serv, headers=header)

    if resp is None or resp.status_code != status.HTTP_200_OK:
        return Non

    resp = serviceRequests.post(url_reserv_serv + f'{settings["prefix"]}/reservations', headers=header)

    if resp is None or resp.status_code != status.HTTP_200_OK:
        return Non

    reservResponse: schemas.CreateReservationResponseFromReservService = resp
    return schemas.CreateReservationResponse(
        reservationUid=reservResponse.reservationUid,
        hotelUid=reservResponse.hotelUid,
        startDate=reservResponse.startDate,
        endDate=reservResponse.endDate,
        discount=loyalty_info.discount,
        status=reservResponse.status,
        payment=pay_info
    )


async def delete_reservation(eservationUid: str, username: str):
    pass


async def get_loyalty(username: str):
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    response = serviceRequests.get(url_loyalty_serv, headers={'X-User-Name': username})

    if response is None or response.status_code != status.HTTP_200_OK:
        return None
    return response.json()
