from gerver.auth import encode
from .models import Profile
from .serializers import GroupSerializer, ProfileSerializer
from django.db.utils import IntegrityError
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register_user(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            serializer.save()
        except IntegrityError:
            error = {"msg": "Username already exist."}
            return Response(error,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(encode(serializer.validated_data),
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_group(request):
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            serializer.save()
        except IntegrityError:
            error = {"status": 500, "msg": "Group already exist."}
            return Response(error,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.validated_data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def authenticate_user(request):
    pass
