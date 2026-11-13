from fastapi import APIRouter, status

from app.schemas import MenuResponse, PostMenuRequest
from app.schemas.menu import PatchMenuRequest
from app.services import MenuService


PREFIX = "/menus"


router = APIRouter(prefix=PREFIX)
service = MenuService()  # Need to find a way to inject this dependency. MenuRouter object? Passing a service as an argument to route functions is bad because FastAPI expects all parameters to be parameters found in the request.


@router.get("", summary="Returns the menus for the given restaurant")
def get_all_menus_by_restaurant_id(restaurant_id: str) -> list[MenuResponse]:
    raise NotImplementedError()


@router.get("/{menu_id}", summary="Get a menu by ID")
def get_menu_by_id(menu_id: str) -> MenuResponse:
    raise NotImplementedError()


@router.post(
    "",
    summary="Creates a new menu",
    status_code=status.HTTP_201_CREATED,
)
def post_menu(request: PostMenuRequest) -> MenuResponse:
    raise NotImplementedError()


@router.patch("/{menu_id}", summary="Updates a menu")
def patch_menu(request: PatchMenuRequest) -> MenuResponse:
    raise NotImplementedError()


@router.delete("/{menu_id}", summary="Deletes a menu")
def delete_menu(request: PatchMenuRequest) -> MenuResponse:
    raise NotImplementedError()
