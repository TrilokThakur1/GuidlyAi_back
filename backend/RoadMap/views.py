import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializer
import traceback

from .utils.AskAi import askAi

from .db import RoadMaps_collection

@api_view(['POST'])
def RoadMapView(request):
    try:
        print("REQUEST DATA:", request.data)

        prompt = request.data.get("prompt")
        userId = request.data.get("userId")

        if not prompt:
            return Response(
                {"message": "Prompt is required"},
                status=400
            )

        data = askAi(prompt)

        # print("AI RESPONSE:", data)

        data["author"] = userId

        result = RoadMaps_collection.insert_one(data)

        data["_id"] = str(result.inserted_id)
        data["author"] = str(userId)

        return Response({
            "message": "Success",
            "data": data
        })

    except Exception as e:
        print("ROADMAP ERROR:", str(e))
        traceback.print_exc()

        return Response(
            {"error": str(e)},
            status=500
        )

    
    
    
@api_view(['GET'])
def MyPlans(request):
    
    # Query Paramiter:
    userId = request.GET.get("userId")
    
    print("--------------")
    print("|",userId,"|")
    print("--------------")
    
    data = list(RoadMaps_collection.find({"author": userId}))
    
    for i in range(len(data)):
        data[i]["_id"] = str(data[i]["_id"])
        data[i]["author"] = str(data[i]["author"])
      
    
    return Response({
        "message": "Success",
        "data": data
    })