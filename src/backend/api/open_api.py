from drf_yasg import openapi
from .serializers import CollectionSerializer

add_new_bookmark_description = "Add a new bookmark"

add_bookmark_responses = {
    201: CollectionSerializer,
    400: "id закладки указан некорректно или не указан вовсе",
    401: "Учетные данные не были предоставлены.",
    404: "Страница не найдена.",
}

delete_bookmark_response = add_bookmark_responses.copy()

delete_bookmark_response.update({200: CollectionSerializer, 201: None})

add_delete_bookmark_collection_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["bookmark_id"],
    properties={"bookmark_id": openapi.Schema(type=openapi.TYPE_INTEGER)},
)
