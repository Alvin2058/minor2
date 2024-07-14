from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from quiz.models import Mark, Question
from os.path import join

# Create your views here.
#@method_decorator(staff_member_required, name="dispatch")
class Manage(View):
    def get(self, request):
        panel_options = {
            # "Upload Questions": {
            #     "link": reverse("upload_question"),
            #     "btntxt": "Upload"
            # },
            # "Verify Questions": {
            #     "link": reverse("verify_question"),
            #     "btntxt": "Verify"
            # },
            "Add Questions": {
                "link": reverse("add_question"),
                "btntxt": "Add"
            }
        }
        return render(
            request,
            "management/manage.html",
            {"panel_options": panel_options}
        )

class AddQuestion(View):
    def get(self, request):
        return render(
            request, 
            "management/add_question.html",
            {
                "questions": range(1, settings.GLOBAL_SETTINGS["questions"]+1)
            }
        )
    
    def post(self, request):
        count, already_exists = 0, 0
        for i in range(1, settings.GLOBAL_SETTINGS["questions"]+1):
            data = request.POST
            q = data.get(f"q{i}", "")
            o1 = data.get(f"q{i}o1", "")
            o2 = data.get(f"q{i}o2", "")
            o3 = data.get(f"q{i}o3", "")
            o4 = data.get(f"q{i}o4", "")
            co = data.get(f"q{i}c", "")
            if Question.objects.filter(question=q).first():
                already_exists += 1
                continue
            question = Question(
                question=q,
                option1=o1,
                option2=o2,
                option3=o3,
                option4=o4,
                correct_option=co,
                creator=request.user
            )
            question.save()
            count += 1
        if already_exists:
            messages.warning(request, f"{already_exists} questions already exists")
        messages.success(request, f"{count} questions added. Wait until admin not verify it.")
        return redirect("management")


