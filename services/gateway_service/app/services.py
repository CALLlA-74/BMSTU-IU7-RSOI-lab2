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
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"/{settings['prefix']}/reservations"
    header = {'X-User-Name', username}




async def get_loyalty(username: str):
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}/loyalty"
    return serviceRequests.get(url_loyalty_serv, headers={'X-User-Name': username}).json()
