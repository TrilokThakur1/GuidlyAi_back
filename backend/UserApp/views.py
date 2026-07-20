# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from pydantic import BaseModel

from backend.settings import JWT_SECRET
from .jwt_utils import *
from .utils import *
from typing import Any, Optional
from uuid import UUID

# 1. IMPORT CLOUDINARY UPLOADER
import cloudinary.uploader

from .helper import BaseResponse
from .serializer import *
from .db import users_collection
from .utils import hash_password

class UserResponce(BaseModel):
    id: Optional[UUID] = None
    name: str
    avatar: str
    email: str


@api_view(['POST'])
def RegisterView(request):
    try:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            avatar = data.get('avatar')

            avatar_url = None
            if avatar:
                print("UPLOADING TO CLOUDINARY...")
                try:
                    upload_result = cloudinary.uploader.upload(
                        avatar,
                        folder="avatars",
                        resource_type="image"
                    )
                    avatar_url = upload_result.get("secure_url")
                except Exception as cloud_err:
                    print("CLOUDINARY CONFIG/UPLOAD ERROR:", str(cloud_err))
                    return Response(
                        {"error": f"Cloudinary failed: {str(cloud_err)}. Did you set up Env variables on Render?"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            print("SAVING TO MONGO...")
            newUser = users_collection.insert_one({
                "name": data['name'],
                "avatar": avatar_url if avatar_url else "/default-avatar.png", 
                "email": data['email'],
                "password": hash_password(data['password'])
            })

            return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("REGISTER CRITICAL EXCEPTION:", str(e))
        return Response({"error": f"Internal Server Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def LoginView(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        print("EMAIL:", email)

        user = users_collection.find_one({"email": email})

        # print("USER:", user)

        if not user:
            return Response({"message": "User not found"}, status=404)

        print("STORED PASSWORD:", user.get("password"))

        if not check_password(password, user['password']):
            return Response({"message": "Invalid Password"}, status=401)

        access_token = generate_access_token({"email": email})
        refresh_token = generate_refresh_token({"email": email})

        return Response({
            "message": "User Logged In Successfully",
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        return Response({
            "error": str(e)
        }, status=500)
    



@api_view(['GET'])
def UserDetails(request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or "Bearer " not in auth_header:
            return Response(BaseResponse(success=False, message="Invalid token").model_dump(), status=401)

        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")

        user = users_collection.find_one({"email": email})
        if not user:
            return Response(BaseResponse(success=False, message="User not found").model_dump(), status=404)

        # 3. SIMPLIFIED USER DATA RESPONSE
        # Since 'avatar' is now a full hosted URL (https://res.cloudinary.com/...),
        # we don't need request.build_absolute_uri() anymore. 
        user_data = {
            "id": str(user["_id"]),
            "name": user["name"],
            "avatar": user["avatar"],  
            "email": user["email"]
        }

        response = BaseResponse(
            success=True,
            message="User fetched successfully",
            data=user_data
        )
        return Response(response.model_dump(), status=status.HTTP_200_OK)

    except (ExpiredSignatureError, InvalidTokenError):
        return Response(BaseResponse(success=False, message="Invalid or expired token").model_dump(), status=401)
    except Exception as e:
        return Response(BaseResponse(success=False, message=str(e)).model_dump(), status=500)