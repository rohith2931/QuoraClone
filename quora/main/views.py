from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Answer
from .forms import UserRegistration, AnswerForm


def home(request):
    # TODO: use prefetch_related
    # Done
    questions = Question.objects.prefetch_related('votes').all()
    for question in questions:
        question.user_liked = question.votes.filter(id=request.user.id).exists()
    return render(request, "main/home.html", {"questions": questions})


def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(
                request,
                f"Hi {username} !!\nYour Account has been created! You can now able to login ",
            )
            return redirect(reverse("login"))
    else:
        form = UserRegistration()
    return render(request, "main/register.html", {"form": form})


def question_detail(request, id):
    """
    Retrieve question details and associated answers for display.

    Args:
        request: The HTTP request object.
        id: The unique identifier of the question.

    Returns:
        The rendered question detail page with the retrieved context.
    """

    context = {}
    try:
        question = Question.objects.prefetch_related("answer_set").get(id=id)
        question.user_liked = question.votes.filter(id=request.user.id).exists()

        context["question"] = question
        answers = question.answer_set.all()
        for answer in answers:
            answer.user_liked = answer.votes.filter(id=request.user.id).exists()
        context["answers"] = answers

    except Question.DoesNotExist as e:
        # TODO: Display error message on the UI
        # Done
        messages.warning(request,"Sorry, The page you requested does not exist.")
        print(e.__str__())
        return redirect(to="/")

    return render(request, "main/question.html", context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "description"]
    template_name = "main/new_question.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def post_answer(request, qid):
    user_answer = None

    try:
        question = Question.objects.get(id=qid)
        user_answer = question.answer_set.filter(answered_by=request.user).first()
        # form.answer = user_answer.answer
    except Question.DoesNotExist:
        # TODO: Display error message on the UI
        # Done
        messages.warning(request,"Sorry, The page you requested does not exist.")
        return redirect("/")

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.cleaned_data["answer"]
            if user_answer:
                if new_answer.strip() != user_answer.answer.strip():
                    user_answer.answer = new_answer
                    user_answer.save()
                else:
                    messages.warning(request, "Please update the answer")
            else:
                Answer.objects.create(
                    answer=new_answer, question=question, answered_by=request.user
                )
            return redirect(reverse("question", args=[qid]))
        
    if request.method == "GET":
        form = None
        if user_answer:
            form=AnswerForm({'answer':user_answer.answer})
        else:
            form=AnswerForm()

    return render(
        request, "main/post_answer.html", {"form": form, "question": question}
    )


@login_required
def upvote_question(request, qid):
    redirect_to = request.GET.get("redirect_to")
    print(redirect_to)
    if not redirect_to:
        redirect_to = "/"

    try:
        question = Question.objects.get(id=qid)
        is_user_upvoted = question.votes.filter(id=request.user.id).exists()
    except Question.DoesNotExist:
        return redirect("/")

    if is_user_upvoted:
        question.votes.remove(request.user)
    else:
        question.votes.add(request.user)
    return redirect(to=redirect_to)


@login_required
def upvote_answer(request, aid):
    redirect_to = request.GET.get("redirect_to")
    if not redirect_to:
        redirect_to = "/"
    try:
        answer = Answer.objects.get(id=aid)
        if_user_upvoked = answer.votes.filter(id=request.user.id).exists()
    except Question.DoesNotExist:
        return redirect("/")
    if if_user_upvoked:
        answer.votes.remove(request.user)
    else:
        answer.votes.add(request.user)
    return redirect(to=redirect_to)


@login_required
def profile(request):
    return render(request, "main/profile.html")
