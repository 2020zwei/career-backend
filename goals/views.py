import os
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import GoalSerializer, GoalSerializer2
from .models import Goal, Action
from users.models import Student
from django.template.loader import render_to_string
from weasyprint import HTML
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PyPDF2 import PdfReader, PdfWriter, PageObject
from io import BytesIO
from reportlab.platypus import BaseDocTemplate,PageTemplate,SimpleDocTemplate, Paragraph, Image, Frame
from reportlab.lib import colors


# Create your views here.
class GoalViewRelated(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer

    def get(self, request):
        """Get goals of user"""
        try:
          student =self.request.user
          print(student)
          goal_obj =Goal.objects.filter(user=student.student)
          print(goal_obj)
          temp_name = "general/templates/" 
          goal_template = str(student.student.full_name)+"-"+"goal" + ".html"
          open(temp_name + goal_template, "w").write(render_to_string('goal.html', {'student_detail': student,'goal_detail':goal_obj}))
          HTML(temp_name + goal_template).write_pdf(str(student.student.first_name)+'.pdf')
          file_location = f'{student.student.first_name}.pdf'
          with open(file_location, 'rb') as f:
            file_data = f.read()
          response = HttpResponse(file_data, content_type='application/pdf')
          response['Content-Disposition'] = 'attachment; filename="'+ student.student.first_name +'".pdf'
          return response
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
          user_obj=request.user
          proffession=request.data.get('proffession')
          goal=request.data.get('goal')
          # actions=request.data.get('actions')
          realistic=request.data.get('realistic')
          countdown_str = request.data.get('date')
          countdown = datetime.strptime(countdown_str, '%Y-%m-%dT%H:%M:%S.%fZ')
          print(countdown)
          goal_obj=Goal.objects.create(user_id=user_obj.id,proffession=proffession, goal=goal,realistic=realistic, countdown=countdown)
          goal_obj.save()

          return Response(data={'success': True, 'Goals': goal_obj.goal, 'Date': countdown}, status=status.HTTP_200_OK)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# Create your views2 here.
class GoalViewRelated2(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer2

    def get(self, request):
        """Get goals of user"""
        try:
          student =self.request.user
          print(student)
          goal_obj =Goal.objects.filter(user=student.student).last()
          serializer = GoalSerializer2(goal_obj, many=False)
          return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
          user_obj=self.request.user
          print(user_obj.student)
          proffession=request.data.get('proffession')
          goal=request.data.get('goal')
          realistic=request.data.get('realistic')
          countdown_str = request.data.get('date')
          actions = request.data.get('actions', [])
          action_list = []

          # Extract the actions from the dictionary
          for key, value in actions.items():
              action_list.append(value)
          countdown = datetime.strptime(countdown_str, '%d-%m-%Y')
          print(countdown)
          goal_obj=Goal.objects.create(user=user_obj.student,proffession=proffession, goal=goal,realistic=realistic, countdown=countdown)
          goal_obj.save()
          for action_text in action_list:
            Action.objects.create(goal=goal_obj, action=action_text)

          return Response(data={'success': True, 'Goals': goal_obj.goal}, status=status.HTTP_200_OK)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class GoalPDF(CreateAPIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     """Get goals of user"""
    #     try:
    #       student =self.request.user
    #       print(student)
    #       goal_obj =Goal.objects.filter(user=student.student).last()
    #       print(goal_obj)
    #       temp_name = "general/templates/" 
    #       goal_template = str(student.student.full_name)+"-"+"goal" + ".html"
    #       open(temp_name + goal_template, "w").write(render_to_string('goal.html', {'student_detail': student,'goal_detail':goal_obj}))
    #       HTML(temp_name + goal_template).write_pdf(str(student.student.full_name)+'.pdf')
    #       file_location = f'{student.student.first_name}.pdf'
    #       with open(file_location, 'rb') as f:
    #         file_data = f.read()
    #       response = HttpResponse(file_data, content_type='application/pdf')
    #       response['Content-Disposition'] = 'attachment; filename="'+ student.student.full_name +'".pdf'
    #       return response
    #     except Exception as e:
    #       return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
      
custom_styles = {
    'bold_centered': ParagraphStyle('BoldCentered', parent=getSampleStyleSheet()['Normal'], fontName='Times-Bold', fontSize=26, leading=30, alignment=1, textColor=(0.2, 0.2, 0.2)),
    'italic_centered': ParagraphStyle('ItalicCentered', parent=getSampleStyleSheet()['Normal'], fontName='Times-Italic', fontSize=22, leading=30, alignment=1, textColor=(0.099, 0.111, 0.222)),
    'italic_bold_centered': ParagraphStyle('ItalicBoldCentered', parent=getSampleStyleSheet()['Normal'], fontName='Times-BoldItalic', fontSize=23, leading=30, alignment=1, textColor=(0.29296875, 0.453125, 0.609375)),
    'centered': ParagraphStyle('BoldCentered', parent=getSampleStyleSheet()['Normal'], fontName='Times-Bold', fontSize=12,leading=20, textColor=(292, 453, 609)),
}

def create_pdf_with_content(content_data, student, goal_obj, action_obj):
    # Create a buffer to store the PDF content
    buffer = BytesIO()

    # Create a BaseDocTemplate with the buffer and specify A4 page size
    doc = BaseDocTemplate(buffer, pagesize=A4)

    # Create a list to store the content
    content = []

    # Calculate the center position to position the frame within the A4 page size
    frame_width = 600  # Adjust this value to set the width of the frame
    frame_height = 600  # Adjust this value to set the height of the frame
    x_offset = (A4[0] - frame_width) / 2
    y_offset = (A4[1] - frame_height) / 2

    # Add the data to the content list using custom layouts (Frames and Paragraphs)
    frame = Frame(x_offset, y_offset, frame_width, frame_height, showBoundary=0,
                  leftPadding=220,
                  topPadding=240,  # Adjust this value to add space between logo and first line
                  rightPadding=0,
                  bottomPadding=0)

    image = Image('general/templates/logo.png', width=280, height=50)  # Adjust the width and height as needed
    content.append(image)

    # Add the Paragraphs to the frame
    content.append(Paragraph(" hello ", custom_styles['centered']))
    content.append(Paragraph(f"{student.student.full_name} Goal", custom_styles['italic_bold_centered']))
    content.append(Paragraph(f"{goal_obj.proffession}", custom_styles['italic_centered']))
    content.append(Paragraph(f"Specific Goals for {goal_obj.goal}", custom_styles['italic_centered']))

    # Add the "By doing:" text followed by a line break and the action_obj
    # content.append(Paragraph(f"By doing:<br/>{action_obj}", custom_styles['italic_centered']))
    actions_text = "<br/>".join([str(action) for action in action_obj])
    # Now add the actions_text to the content list
    content.append(Paragraph(f"By doing:<br/>{actions_text}", custom_styles['italic_centered']))


    if goal_obj.realistic is True:
        content.append(Paragraph(f"I can do this {goal_obj.realistic}", custom_styles['italic_centered']))
        content.append(Paragraph(f"Deadline", custom_styles['italic_bold_centered']))
        content.append(Paragraph(f"{goal_obj.countdown}", custom_styles['italic_centered']))

    # Build the content and save it to the buffer
    doc.addPageTemplates([PageTemplate(frames=[frame])])
    doc.build(content)

    # Move the buffer's file pointer to the beginning
    buffer.seek(0)

    return buffer

class GoalPDF(CreateAPIView):
    # ... Your existing code ...

    def get(self, request):
        try:
            student =self.request.user
            print(student)
            goal_obj =Goal.objects.filter(user=student.student).last()
            action_obj=Action.objects.filter(goal=goal_obj)
            print(goal_obj)

            # Get the additional data that you want to add to the PDF
            additional_data = f"""
                Logo

                {student.student.first_name} Goal

                {goal_obj.proffession}

                Specific Goals for {goal_obj.goal}

                {goal_obj.proffession}

                By doing:

                I can do this {goal_obj.realistic}

                Deadline
                {goal_obj.countdown}
                """

            # Convert the additional data to a PDF page using reportlab
            additional_data_page = create_pdf_with_content(additional_data,student, goal_obj,action_obj)

            # Load the existing PDF
            existing_pdf_path = 'general/templates/frame.pdf'
            pdf = PdfReader(existing_pdf_path)

            existing_page = pdf.pages[0]

            # Load the additional data PDF using PdfReader
            additional_pdf_reader = PdfReader(additional_data_page)

            # Get the first page of the additional data
            additional_page = additional_pdf_reader.pages[0]

            # Merge the additional data with the existing page
            existing_page.merge_page(additional_page)

            # Create a new PDF writer
            output_pdf = PdfWriter()

            # Add the updated existing page to the new PDF writer
            output_pdf.add_page(existing_page)

            # Add the remaining pages of the existing PDF to the new PDF writer
            for page_num in range(1, len(pdf.pages)):
                page = pdf.pages[page_num]
                output_pdf.add_page(page)

            # Create a buffer to store the updated PDF content
            buffer = BytesIO()
            output_pdf.write(buffer)

            # Move the buffer's file pointer to the beginning
            buffer.seek(0)

            # Provide the updated PDF as a response for download
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{student.student.full_name}.pdf"'

            # Close the buffer
            buffer.close()

            return response

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)        
class GoalDetail(APIView):
    """
    Retrieve, update or delete a goal instance.
    """
    def get_object(self, pk):
        try:
            return Goal.objects.get(pk=pk)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        goal = self.get_object(pk)
        serializer = GoalSerializer(goal)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        goal = self.get_object(pk)
        user_obj=request.user
        serializer = GoalSerializer(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        goal = self.get_object(pk)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
