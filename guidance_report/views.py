from django.http import HttpResponse
from .utils import generate_gpt_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from weasyprint import HTML
import os
from django.template.loader import render_to_string
from users.models import Student
from cv.models import Skills, Experience, Interests, CV, Qualities
from choices.models import Level5, Level6, Level8, Apprentice
from calculator.models import UserPoints, Subject, SubjectGrade
from goals.models import Goal
from psychometric.models import TestResult
from django.forms.models import model_to_dict
from django.db.models import QuerySet


def serialize_students_data(instance):
    return model_to_dict(instance)

class GuidanceReportModels(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            models = {
                "main_models": [
                    "predicted points and subjects",
                    "my studied goals",
                    "multiple intelligence score",
                    "values assessment",
                    "interest assessment"
                ],
                "cv_models": [
                    "address",
                    "personal statement",
                    "work experience",
                    "skills",
                    "qualities",
                    "interests",
                ],
                "education_models": [
                    "level 8",
                    "level 6/7",
                    "level 5(plc)",
                    "apprentices",
                ]
            }
            return Response({"success": True, "models": models}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GenerateGpt(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = self.request.user
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"success": False, "message": "User does not exist or not a student"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            prompt = """Based on the student's data, create a guidance report for student on these topics 
            \nExecutive Summary
            \nSelf Assessment Results
            \nStudy Advice
            \nAcademic Record
            \nCareer Assessment
            \nGoal Setting
            \nEducational Options
            \nSuggested Resources 
            \nConclusion
            
            student data:
            \n"""

            # Main Models
            main_models = request.data.get('main_models', [])
            if "predicted points and subjects" in main_models:
                user_points = UserPoints.objects.filter(user=student).first()
                # subject = SubjectGrade.objects.filter(user=student).first()

                if user_points:
                    prompt += f"Predicted points and subjects: {user_points.total_points},\n"
                else:
                    prompt += "Predicted points and subjects: Not available\n"

            if "my studied goals" in main_models:
                goals = Goal.objects.filter(user=student).first()
                if goals:
                    prompt += f"My studied goals: {goals.goal}, {goals.description}\n"
                else:
                    prompt += "My studied goals: Not available\n"

            if "multiple intelligence score" in main_models:
                mi_score = TestResult.objects.filter(user=student, test__name='Multiple Intelligence').first()
                if mi_score:
                    prompt += f"Multiple intelligence score: {mi_score.score}\n"
                else:
                    prompt += "Multiple intelligence score: Not available\n"

            print("prompt: ", prompt)

            # CV Section
            cv = CV.objects.filter(user=student).first()
            if cv:
                prompt += f"Address: {cv.address}, {cv.city}, {cv.town}\n"
                prompt += f"Personal Statement: {cv.objective}\n"
            else:
                prompt += "CV data: Not available\n"

            work_experience = Experience.objects.filter(user=student)
            if work_experience.exists():
                experience_list = "\n".join([f"{exp.job_title} at {exp.company}" for exp in work_experience])
                prompt += f"Work Experience: {experience_list}\n"
            else:
                prompt += "Work Experience: Not available\n"

            skills = Skills.objects.filter(user=student)
            if skills.exists():
                skills_list = ", ".join([skill.skill_dropdown for skill in skills])
                prompt += f"Skills: {skills_list}\n"
            else:
                prompt += "Skills: Not available\n"

            qualities = Qualities.objects.filter(user=student)
            if qualities.exists():
                qualities_list = ", ".join([quality.quality_dropdown for quality in qualities])
                prompt += f"Qualities: {qualities_list}\n"
            else:
                prompt += "Qualities: Not available\n"

            interests = Interests.objects.filter(user=student)
            if interests.exists():
                interests_list = ", ".join([interest.interests for interest in interests])
                prompt += f"Interests: {interests_list}\n"
            else:
                prompt += "Interests: Not available\n"

            print("prompt: ", prompt)            # Education Options
            education_mappings = {
                "level 8": Level8.objects.filter(student=student).first(),
                "level 6/7": Level6.objects.filter(student=student).first(),
                "level 5(plc)": Level5.objects.filter(student=student).first(),
                "apprentices": Apprentice.objects.filter(student=student).first()
            }

            education_models = request.data.get('education_models', [])
            for key in education_models:
                if key in education_mappings:
                    label = education_mappings[key]
                    if label:
                        prompt += f"Education Option - {key.replace('_', ' ').title()}: {label}\n"
                    else:
                        prompt += f"Education Option - {key.replace('_', ' ').title()}: Not available\n"

            # gpt_response = generate_gpt_response(prompt)

            response = {"success": True, "message": "gpt report generated successfully", "prompt": prompt}
            return Response(response, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"success": False, "message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GeneratePDFReport(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            student = self.request.user
            user_obj = Student.objects.get(id=student.student.id)
            temp_name = "general/templates/"
            report_template = str(user_obj.first_name) + "-" + str(user_obj.last_name) + "-" + "guidance_report" + ".html"
            full_name = user_obj.full_name

            executive_summary = "A brief overview of the entire report, summarizing the key findings and recommendations based on your self-assessment and career goals. It highlights the main points that will be discussed in the following sections."
            self_assessment_result = "A brief overview of the entire report, summarizing the key findings and recommendations based on your self-assessment and career goals. It highlights the main points that will be discussed in the following sections."
            study_advice = "Tailored recommendations on study <b>habits, strategies, and academic</b> planning based on your self-assessment results. This may include advice on study techniques, time management, and areas to focus on."
            academic_record = "A summary of your academic history, including grades, courses taken, and any relevant academic achievements. It may also include an analysis of your performance trends over time."
            career_assessment = "An evaluation of potential career paths based on your self-assessment results, interests, and academic record. It may include suggested careers, job roles, and industries that align with your profile."

            context = {
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "executive_summary": executive_summary,
                "self_assessment_result": self_assessment_result,
                "study_advice": study_advice,
                "academic_record": academic_record,
                "career_assessment": career_assessment,

            }
            rendered_template = render_to_string('guidance_report.html', context)
            open(temp_name + report_template, "w").write(rendered_template)
            HTML(temp_name + report_template).write_pdf(str("guidance_report") + '.pdf')
            file_location = f'{"guidance_report"}.pdf'
            with open(file_location, 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{full_name} Guidance Report.pdf"'
            os.remove(temp_name + report_template)
            os.remove("guidance_report.pdf")
            return response

        except Exception as e:
            return Response({'message': "All steps of Guidance Report should be completed . " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChatbotAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        welcome_message = "Welcome to the Guidance Chatbot! Type your message to start the conversation."
        return Response({"success": True, "message": welcome_message}, status=status.HTTP_200_OK)

    def post(self, request):
        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"success": False, "message": "Message content is missing"}, status=status.HTTP_400_BAD_REQUEST)

        gpt_response = generate_gpt_response(user_message)

        return Response({"success": True, "response": gpt_response}, status=status.HTTP_200_OK)
