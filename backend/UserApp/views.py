from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pydantic import BaseModel
from .jwt_utils import *
from .utils import *
from typing import Any, Optional
from uuid  import UUID
import os
from django.conf import settings
from uuid import uuid4

from .helper import BaseResponse

#  return Response({
#           "message": "User Found",
#           "id": str(user['_id']),
#           "name": user['name'],
#           "avatar": user['avatar'],
#           "email": user['email']  
#           }, status=status.HTTP_200_OK)
#    else:
class UserResponce(BaseModel):
    id:Optional[UUID]=None
    name:str
    avatar:str
    email:str


from .serializer import *

from .db import users_collection
from .utils import hash_password


@api_view(['POST'])
def RegisterView(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        data = serializer.validated_data

        avatar = data['avatar']

        # unique filename
        file_name = f"{uuid4()}_{avatar.name}"

        upload_path = os.path.join(
            settings.MEDIA_ROOT,
            "avatars"
        )

        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(
            upload_path,
            file_name
        )

        # Save Image
        with open(file_path, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)

        avatar_url = f"/media/avatars/{file_name}"

        newUser = users_collection.insert_one({
            "name": data['name'],
            "avatar": avatar_url,
            "email": data['email'],
            "password": hash_password(data['password'])
        })

        if newUser:

            access_token = generate_access_token({
                "email": data['email']
            })

            refresh_token = generate_refresh_token({
                "email": data['email']
            })

            return Response({
                "message": "User Registered Successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
            })

        return Response({
            "message": "Registration Failed"
        }, status=400)

    return Response({
        "message": "Invalid Data",
        "errors": serializer.errors
    }, status=400)
        

@api_view(['POST'])
def LoginView(request):
    email = request.data['email']
    password = request.data['password']
    
    user = users_collection.find_one({"email": email})
    
    if user:
        if check_password(password, user['password']):
            acess_Token = generate_access_token({"email": email})
            refresh_Token = generate_refresh_token({"email":email})
            
            return Response({
                "message": "User Logged In Successfully",
                "refresh_token": refresh_Token,
                "access_token": acess_Token
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid Password"
                }, status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['GET'])
def UserDetails(request):

    try:

        # -----------------------------
        # Authorization Check
        # -----------------------------

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            response = BaseResponse(
                success=False,
                message="Authorization token missing"
            )

            return Response(
                response.model_dump(),
                status=status.HTTP_401_UNAUTHORIZED
            )

        # -----------------------------
        # Token Extract
        # -----------------------------

        token = auth_header.split(" ")[1]

        if token == "null":

            response = BaseResponse(
                success=False,
                message="Invalid token"
            )

            return Response(
                response.model_dump(),
                status=status.HTTP_401_UNAUTHORIZED
            )

        # -----------------------------
        # Extract Email
        # -----------------------------

        email = extract_email(token)

        print("EMAIL:", email)

        # -----------------------------
        # Find User
        # -----------------------------

        user = users_collection.find_one({
            "email": email
        })

        if not user:

            response = BaseResponse(
                success=False,
                message="User not found"
            )

            return Response(
                response.model_dump(),
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------
        # Success Response
        # -----------------------------

        user_data = {
         "id": str(user["_id"]),
         "name": user["name"],
         "avatar": request.build_absolute_uri(user["avatar"]),
         "email": user["email"]
         }
        response = BaseResponse(
            success=True,
            message="User fetched successfully",
            data=user_data
        )

        return Response(
            response.model_dump(),
            status=status.HTTP_200_OK
        )

    except Exception as e:

        print("ERROR:", e)

        response = BaseResponse(
            success=False,
            message=str(e)
        )

        return Response(
            response.model_dump(),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )