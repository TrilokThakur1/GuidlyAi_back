from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.conf import settings
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache the response for 15 minutes
@api_view(["GET"])
def TechNewsView(request):

        url = "https://newsapi.org/v2/everything"

        params = {
            "q": "Tech in India",
            "sortBy": "publishedAt",
            "apiKey": settings.NEWS_API_KEY,
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            return Response(response.json())

        except requests.RequestException as e:
            return Response(
                {
                    "error": "Failed to fetch news",
                    "details": str(e)
                },
                status=500
            )