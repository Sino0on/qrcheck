from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from server.forms import LoginForm, ParaForm, UserRegisterForm, GradeForm
from server.models import Para, Lesson, Grade, generate_qrcode
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html', {'loginform': LoginForm})


def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    print(password)
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        if user.is_teacher:
            return redirect('/create')
        return redirect('/camera')
    return redirect('/')


@login_required(redirect_field_name='/')
def camera(request):
    return render(request, 'camera.html')


@login_required(redirect_field_name='/')
def grade(request):
    return render(request, 'grade.html')


@login_required(redirect_field_name='/')
def new(request, pk):
    para = get_object_or_404(Para, id=pk)
    qrcode = f'http://192.168.88.96:8000/link/{para.qrcode}'
    return render(request, 'new.html', {'para': para, 'qrcode': qrcode})


@login_required(redirect_field_name='/')
def teacher(request):
    return render(request, 'teacher.html')


def user(request):
    return render(request, 'user.html')


@login_required(redirect_field_name='/')
def create(request):
    if request.method == 'POST':
        lesson = request.POST['lesson']
        lesson = get_object_or_404(Lesson, id=lesson)
        if request.user in lesson.teacher.all():
            para = Para.objects.create(lesson=lesson, teacher=request.user)
            return redirect(f'/new/{para.pk}')
        return redirect('/')
    return render(request, 'create.html', {'paraform': ParaForm})


@login_required(redirect_field_name='/')
def link(request, qrcode):
    para = get_object_or_404(Para, qrcode=qrcode)
    if para.is_active:
        para.students.add(request.user)
        para.save()
        return redirect(f'/para/{para.pk}')
    return redirect('/camera')


@login_required(redirect_field_name='/')
def para(request, pk):
    context = {}
    para1 = get_object_or_404(Para, id=pk)
    if request.method == 'POST':
        data = GradeForm(request.POST)
        if data.is_valid():
            grade = data.save(commit=False)
            grade.student = request.user
            grade.para = para1
            grade.save()
    if request.user in para1.students.all():
        if Grade.objects.filter(student=request.user, para=para1).count() == 0:
            context = {'form': GradeForm}
        return render(request, 'ballrequest.html', context)
    return redirect('/')


@login_required(redirect_field_name='/')
def update_qrcode(request, pk):
    para = get_object_or_404(Para, id=pk)
    if request.user == para.teacher:
        para.qrcode = generate_qrcode()
        para.save()
        return redirect(f'/new/{para.pk}')
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            das = form.save(commit=False)
            das.save()
            print(das)
            return redirect('/')
        else:
            print(form.errors)
    form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(redirect_field_name='/')
def para_end(request, pk):
    para = get_object_or_404(Para, id=pk)
    if request.user == para.teacher:
        para.is_active = False
        para.save()
        return redirect('/create')
    return redirect('/')


@login_required(redirect_field_name='/')
def requests(request, pk):
    para = get_object_or_404(Para, id=pk)
    if request.user == para.teacher:
        grades = Grade.objects.filter(para=para, is_active=False)
        return render(request, 'requests.html', {'grades': grades})
    return redirect('/')


@login_required(redirect_field_name='/')
def success_grade(request, pk):
    grade = get_object_or_404(Grade, id=pk)
    if request.user == grade.para.teacher:
        grade.is_active = True
        grade.save()
        return redirect(f'/requests/{grade.para.pk}')
    return redirect('/')
