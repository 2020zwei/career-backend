from django.http import JsonResponse
from .utils import generate_gpt_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class GenerateReport(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            prompt = "Provide a summary of the latest advancements in AI technology."
            gpt_response = generate_gpt_response(prompt)
            response = {"success": True, "message": "gpt report generated successfully", "gpt_response": gpt_response}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
