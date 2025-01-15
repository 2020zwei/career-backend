import os

from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from calculator.models import UserPoints
from choices.models import Level5, Level6, Level8, Apprentice
from cv.models import Skills, Experience, Interests, CV, Qualities
from goals.models import Goal
from psychometric.models import TestResult, TestResultDetail, PsychometricTest
from users.models import Student
from .utils import generate_gpt_response


def serialize_students_data(instance):
    return model_to_dict(instance)


class GuidanceReportModels(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            models = {
                "main_models": ["predicted points and subjects", "my studied goals", "multiple intelligence score",
                                "values assessment", "interest assessment"],
                "cv_models": ["address", "personal statement", "work experience", "skills", "qualities",
                              "interests", ],
                "education_models": ["level 8", "level 6/7", "level 5(plc)", "apprentices", ]}
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

            print("prompt: ", prompt)  # Education Options
            education_mappings = {"level 8": Level8.objects.filter(student=student).first(),
                                  "level 6/7": Level6.objects.filter(student=student).first(),
                                  "level 5(plc)": Level5.objects.filter(student=student).first(),
                                  "apprentices": Apprentice.objects.filter(student=student).first()}

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
            report_template = str(user_obj.first_name) + "-" + str(
                user_obj.last_name) + "-" + "guidance_report" + ".html"
            full_name = user_obj.full_name

            executive_summary = ("A brief overview of the entire report, summarizing the key findings and "
                                 "recommendations based on your self-assessment and career goals. It highlights the "
                                 "main points that will be discussed in the following sections.")
            self_assessment_result = ("A brief overview of the entire report, summarizing the key findings and "
                                      "recommendations based on your self-assessment and career goals. It highlights "
                                      "the main points that will be discussed in the following sections.")
            study_advice = ("Tailored recommendations on study <b>habits, strategies, and academic</b> planning based "
                            "on your self-assessment results. This may include advice on study techniques, "
                            "time management, and areas to focus on.")
            academic_record = ("A summary of your academic history, including grades, courses taken, and any relevant "
                               "academic achievements. It may also include an analysis of your performance trends "
                               "over time.")
            career_assessment = ("An evaluation of potential career paths based on your self-assessment results, "
                                 "interests, and academic record. It may include suggested careers, job roles, "
                                 "and industries that align with your profile.")

            context = {"first_name": user_obj.first_name, "last_name": user_obj.last_name,
                       "executive_summary": executive_summary, "self_assessment_result": self_assessment_result,
                       "study_advice": study_advice, "academic_record": academic_record,
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
            return Response({'message': "All steps of Guidance Report should be completed . " + str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class GenerateGuidanceReportGPT(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            # Fetch student record
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({"success": False, "message": "Student record not found."}, status=404)

            # Fetch CV record if available
            cv = CV.objects.filter(user=student).first()

            # Gather personal info
            personal_info = {
                "first_name": student.first_name or None,
                "last_name": student.last_name or None,
                "full_name": student.full_name or None,
                "city": cv.city if cv and cv.city else None,
                "county": cv.town if cv and cv.town else None,
                "eircode": cv.eircode if cv and cv.eircode else None,
                "school": student.school if student.school else None
            }

            data = request.data
            feedback = data.get("feedback", None)
            previous_response = data.get("previous_response", None)

            multiple_intelligence_max_scores = 40
            occupational_interest_max_scores = 70
            occupational_values_max_scores = 28

            def structure_test_results(test_name, reference_max_score):
                test_obj = PsychometricTest.objects.filter(name__iexact=test_name).first()
                if not test_obj:
                    return None
                test_result = TestResult.objects.filter(user=student, test=test_obj).first()
                if not test_result:
                    return None
                question_scores = TestResultDetail.objects.filter(result=test_result).values("question__type__type", "answer__weightage")
                breakdown = {}
                for detail in question_scores:
                    question_type = detail["question__type__type"]
                    weightage = detail["answer__weightage"]
                    breakdown[question_type] = breakdown.get(question_type, 0) + weightage

                if not breakdown:
                    return None

                details_list = []
                for category, score in breakdown.items():
                    details_list.append({"category": category, "score": f"{score}/{reference_max_score}"})

                if not details_list:
                    return None

                total_possible = len(breakdown) * reference_max_score
                return {
                    "total_score": f"{test_result.score}/{total_possible}",
                    "details": details_list
                }

            # Gather Self-Assessment Results if requested
            assessment_results = {}
            if data.get("mis") == "Yes":
                mis_data = structure_test_results("Multiple Intelligence", multiple_intelligence_max_scores)
                if mis_data:
                    assessment_results["multiple_intelligence"] = mis_data
            if data.get("values_assessment") == "Yes":
                va_data = structure_test_results("Occupational Values Assesment", occupational_values_max_scores)
                if va_data:
                    assessment_results["values"] = va_data
            if data.get("interest_assessment") == "Yes":
                ia_data = structure_test_results("Occupational Interest Assesment", occupational_interest_max_scores)
                if ia_data:
                    assessment_results["interest"] = ia_data

            # Gather CV Data if requested
            cv_data = {}
            if cv:
                if data.get("personal_statement") == "Yes" and cv.objective:
                    cv_data["personal_statement"] = cv.objective
                if data.get("work_experience") == "Yes":
                    experiences = Experience.objects.filter(user=student)
                    if experiences.exists():
                        cv_data["work_experience"] = list(
                            experiences.values(
                                "job_title", "company", "city", "country",
                                "description", "startdate", "enddate", "is_current_work"
                            )
                        )
                if data.get("skills") == "Yes":
                    skill_objs = Skills.objects.filter(user=student)
                    if skill_objs.exists():
                        cv_data["skills"] = list(skill_objs.values_list("description", flat=True))
                if data.get("interest") == "Yes":
                    interests = Interests.objects.filter(user=student)
                    qualities = Qualities.objects.filter(user=student)
                    if interests.exists():
                        cv_data["interests"] = list(interests.values_list("interests", flat=True))
                    if qualities.exists():
                        cv_data["qualities"] = list(qualities.values_list("description", flat=True))

            # Gather Predicted Points and Subjects if requested
            predicted_points = []
            if data.get("predicted_points_and_subjects") == "Yes":
                user_points_records = UserPoints.objects.filter(user=student)
                if user_points_records.exists():
                    for up in user_points_records:
                        grades = up.grades.all().values("subject__name", "grade", "point")
                        if grades.exists():
                            predicted_points.append({
                                "total_points": up.total_points,
                                "grades": list(grades)
                            })

            if not predicted_points:
                predicted_points = None

            # Gather Goals if requested
            goals = None
            if data.get("my_stated_goals") == "Yes":
                goal_objs = Goal.objects.filter(user=student)
                if goal_objs.exists():
                    goals = list(goal_objs.values("proffession", "goal", "description", "realistic", "countdown"))

            # Gather Education Options if requested
            education_options = {}
            requested_options = data.get("education_options", [])
            if requested_options:
                if "level 5(plc)" in requested_options:
                    lvl5 = Level5.objects.filter(choice__user=student)
                    if lvl5.exists():
                        education_options["level_5"] = list(lvl5.values())
                if "level 6/7" in requested_options:
                    lvl6_7 = Level6.objects.filter(choice__user=student)
                    if lvl6_7.exists():
                        education_options["level_6_7"] = list(lvl6_7.values())
                if "level 8" in requested_options:
                    lvl8 = Level8.objects.filter(choice__user=student)
                    if lvl8.exists():
                        education_options["level_8"] = list(lvl8.values())
                if "apprenticeship" in requested_options:
                    appr = Apprentice.objects.filter(choice__user=student)
                    if appr.exists():
                        education_options["apprenticeship"] = list(appr.values())

            def get_first_word_of_first_chosen_course(courses):
                if not courses:
                    return None
                first_course = courses[0]
                title = first_course.get("title")
                if title and title.strip():
                    return title.split()[0]
                return None

            def fetch_recommendations(model, chosen_courses, keyword, limit=5):
                if not keyword:
                    return []
                chosen_ids = [c["id"] for c in chosen_courses] if chosen_courses else []
                recs = model.objects.filter(title__icontains=keyword).exclude(id__in=chosen_ids)[:limit]
                return list(recs.values()) if recs.exists() else []

            recommended_courses = {}
            if education_options.get("level_5"):
                keyword_5 = get_first_word_of_first_chosen_course(education_options["level_5"])
                if keyword_5:
                    recommended_courses["level_5"] = fetch_recommendations(Level5, education_options["level_5"], keyword_5)
            if education_options.get("level_6_7"):
                keyword_6_7 = get_first_word_of_first_chosen_course(education_options["level_6_7"])
                if keyword_6_7:
                    recommended_courses["level_6_7"] = fetch_recommendations(Level6, education_options["level_6_7"], keyword_6_7)
            if education_options.get("level_8"):
                keyword_8 = get_first_word_of_first_chosen_course(education_options["level_8"])
                if keyword_8:
                    recommended_courses["level_8"] = fetch_recommendations(Level8, education_options["level_8"], keyword_8)

            recommended_courses = {k: v for k, v in recommended_courses.items() if v}

            response_data = {
                "personal_info": personal_info,
                "self_assessment_results": assessment_results if assessment_results else {},
                "cv_data": cv_data if cv_data else {},
                "predicted_points": predicted_points if predicted_points else {},
                "goals": goals if goals else {},
                "education_options": education_options if education_options else {},
                "recommended_courses": recommended_courses if recommended_courses else {}
            }

            # Return the collected data as JSON
            return Response({"success": True, "data": response_data}, status=200)

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=400)
