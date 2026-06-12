from rest_framework import serializers

class RoadMapStepSerializer(serializers.Serializer):
    stepTitle = serializers.CharField()
    stepDesc = serializers.CharField()
    stepEstimatedTime = serializers.CharField()  # kept string because AI returns "number of days"


class BookSerializer(serializers.Serializer):
    bookTitle = serializers.CharField()
    bookAuthor = serializers.CharField()
    bookDesc = serializers.CharField()


class ResourcesSerializer(serializers.Serializer):
    books = BookSerializer(many=True)
    videos = serializers.ListField(
        child=serializers.URLField()
    )


class RoadMapSerializer(serializers.Serializer):
    greetings = serializers.CharField()
    author = serializers.CharField()
    roadmapTitle = serializers.CharField()
    roadmapDesc = serializers.CharField()
    roadmapSteps = RoadMapStepSerializer(many=True)
    resources = ResourcesSerializer()
    lastWords = serializers.CharField()
