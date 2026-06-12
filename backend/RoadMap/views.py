import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializer


from .utils.AskAi import askAi

from .db import RoadMaps_collection

@api_view(['POST'])
def RoadMapView(request):
    
    prompt = request.data['prompt']
    userId = request.data.get('userId')
    
    data = askAi(prompt)

    data["author"] = userId
    
    RoadMaps_collection.insert_one(data)
    
    data["_id"] = str(data["_id"])
    data["author"] = str(data["author"])
    
    return Response({
        "message": "Success",
        "data": data
    })

    
    
    
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