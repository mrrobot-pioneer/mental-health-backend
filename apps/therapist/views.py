from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Q

from .models import Therapist
from .serializers import TherapistSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def therapist_list(request):
    queryset = Therapist.objects.all().order_by("-rating")

    q = request.GET.get("q")
    filter_param = request.GET.get("filter")

    # SEARCH
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) |
            Q(bio__icontains=q) |
            Q(specialization__icontains=q)
        )

    # FILTER
    if filter_param:
        filter_param = filter_param.lower()

        if filter_param == "verified":
            queryset = queryset.filter(is_verified=True)
        else:
            queryset = queryset.filter(
                specialization__icontains=filter_param
            )

    serializer = TherapistSerializer(queryset, many=True)
    return Response(serializer.data)