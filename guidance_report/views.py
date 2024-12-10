from html import unescape

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
from calculator.models import UserPoints, SubjectGrade
from goals.models import Goal
from psychometric.models import TestResult, TestResultDetail, PsychometricTest
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




class GenerateGuidanceReportGPT(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            # Fetch the student record
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({"success": False, "message": "Student record not found."}, status=404)

            # Fetch the CV record for the student
            try:
                cv = CV.objects.get(user=student)
            except CV.DoesNotExist:
                cv = None

            # Gather Personal Information
            personal_info = {
                "first_name": student.first_name or "Not provided",
                "last_name": student.last_name or "Not provided",
                "full_name": student.full_name or "Not provided",
                "city": cv.city if cv else "Not provided",
                "county": cv.town if cv else "Not provided",
                "eircode": cv.eircode if cv else "Not provided",
                "school": student.school or "Not provided",
            }

            # Parse request body
            data = request.data

            # Helper function to structure test results
            def structure_test_results(test_name):
                test_obj = PsychometricTest.objects.filter(name__iexact=test_name).first()
                if not test_obj:
                    return None
                test_result = TestResult.objects.filter(user=student, test=test_obj).first()
                if not test_result:
                    return None
                question_scores = TestResultDetail.objects.filter(result=test_result).values(
                    "question__type__type", "answer__weightage"
                )
                breakdown = {}
                for detail in question_scores:
                    question_type = detail["question__type__type"]
                    weightage = detail["answer__weightage"]
                    breakdown[question_type] = breakdown.get(question_type, 0) + weightage
                return {
                    "score": test_result.score,
                    "total_score": sum(breakdown.values()),
                    "details": [{"category": question_type, "score": score} for question_type, score in breakdown.items()],
                }

            # Gather Self-Assessment Results
            assessment_results = {}
            if data.get("mis") == "Yes":
                assessment_results["multiple_intelligence"] = structure_test_results("Multiple Intelligence")
            if data.get("values_assessment") == "Yes":
                assessment_results["values"] = structure_test_results("Occupational Values Assesment")
            if data.get("interest_assessment") == "Yes":
                assessment_results["interest"] = structure_test_results("Occupational Interest Assesment")

            # Gather CV Data
            cv_data = {}
            if cv:
                if data.get("personal_statement") == "Yes":
                    cv_data["personal_statement"] = cv.objective or "Not provided"
                if data.get("work_experience") == "Yes":
                    cv_data["work_experience"] = list(
                        Experience.objects.filter(user=student).values(
                            "job_title", "company", "city", "country", "description", "startdate", "enddate", "is_current_work"
                        )
                    )
                if data.get("skills") == "Yes":
                    cv_data["skills"] = list(Skills.objects.filter(user=student).values_list("description", flat=True))
                if data.get("interest") == "Yes":
                    cv_data["interests"] = list(Interests.objects.filter(user=student).values_list("interests", flat=True))
                    cv_data["qualities"] = list(Qualities.objects.filter(user=student).values_list("description", flat=True))

            # Gather Predicted Points and Subjects
            predicted_points = None
            if data.get("predicted_points_and_subjects") == "Yes":
                user_points = UserPoints.objects.filter(user=student).first()
                if user_points:
                    predicted_points = {
                        "total_points": user_points.total_points,
                        "grades": list(user_points.grades.values("subject__name", "grade", "point")),
                    }

            # Gather Goals
            goals = None
            if data.get("my_stated_goals") == "Yes":
                goals = list(
                    Goal.objects.filter(user=student).values("proffession", "goal", "description", "realistic", "countdown")
                )

            # Gather Education Options
            education_options = {}
            if data.get("education_options"):
                options = data.get("education_options")
                if "level 5(plc)" in options:
                    education_options["level_5"] = list(Level5.objects.filter(choice__user=student).values())
                if "level 6/7" in options:
                    education_options["level_6_7"] = list(Level6.objects.filter(choice__user=student).values())
                if "level 8" in options:
                    education_options["level_8"] = list(Level8.objects.filter(choice__user=student).values())
                if "apprenticeship" in options:
                    education_options["apprenticeship"] = list(Apprentice.objects.filter(choice__user=student).values())

            # Combine all gathered data
            response_data = {
                "personal_info": personal_info,
                "self_assessment_results": assessment_results,
                "cv_data": cv_data,
                "predicted_points": predicted_points,
                "goals": goals,
                "education_options": education_options,
            }

            # Construct a generic prompt
            prompt = f"""
            You are creating a career guidance report for a student.

            The final output should be a fully structured HTML page with the following sections:

            1. Introduction:
               - Include the student's name, approximate age (if not given, you may estimate based on educational stage), 
                 and educational stage or current context (e.g., high school student, college student).
               - Provide a brief introduction to the purpose of the report.

            2. Self-Assessment Results:
               - Overview the student's Multiple Intelligence scores, Occupational Values, and Occupational Interests if available.
               - Highlight the top three skills and top three qualities from their CV data.
               - Discuss what these strengths may indicate about suitable career paths.
               - Suggest 5 possible future careers that align with these results.

            3. Suggested Study Techniques and Advice:
               - Provide study techniques tailored to the student's learning style based on their multiple intelligences.

            4. Academic Achievement:
               - Use the predicted points/grades/achievements to comment on courses or areas of study that would suit their strengths.

            5. Career Exploration:
               - Offer advice on how the student can further explore these potential careers (e.g. shadowing, volunteering, online courses).

            6. Goals of Student:
               - Outline short-term (3 months) and long-term (1 year) goals, referencing the student's stated goals if provided.

            7. Compatible Courses:
               - List 10 compatible courses at one educational level (e.g., Level 8) if provided.
               - List 10 courses at another educational level (e.g., Level 6/7) if provided.
               - List 5 apprenticeships (if applicable).
               - List 3 QQI Level 5 courses (if applicable).
               - Provide a few non-education-based options for personal or professional development.

            8. Conclusion:
               - Summarize the student's strengths, potential career areas, and encourage next steps.

            Use the data provided below to inform your report. Only use what's relevant. If some data isn't available, you can skip that part.
            The final output should be in valid HTML (no Markdown, no code fences).
            Just produce the HTML document, including <html> and <body> tags.

            Data provided:
            Personal Info: {response_data['personal_info']}
            Self-Assessment Results: {response_data['self_assessment_results']}
            CV Data: {response_data['cv_data']}
            Predicted Points: {response_data['predicted_points']}
            Goals: {response_data['goals']}
            Education Options: {response_data['education_options']}
            """

            # Generate the GPT response
            gpt_response = generate_gpt_response(prompt)

            # Return the response
            return Response({"success": True, "message": gpt_response}, status=200)

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=400)