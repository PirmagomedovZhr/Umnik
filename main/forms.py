from django import forms
from .models import User, Groups, Disciplin, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'disciplin']

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # используем метку поля как placeholder
            field.label = ""  # убираем метку поля


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "Email",
            'placeholder': "Имя пользователя"
        }),
    )
    position = forms.ChoiceField(
        choices=[
            ('Студент', 'Студент'),
            ('Преподаватель', 'Преподаватель'),
        ],
        widget=forms.Select(attrs={
            'class': "form-control mt-2",
            'id':'position'
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "password",
            'placeholder': "Пароль"
        }),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "repassword",
            'placeholder': "Повторите пароль"
        }),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control mt-2",
            'id': "first_name",
            'placeholder': "Имя"
        }),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control mt-2",
            'id': "last_name",
            'placeholder': "Фамилия"
        }),
    )
    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            is_active=True,
            position=self.cleaned_data["position"],
        )
        return user


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Имя пользователя"
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
            'placeholder': "Пароль"
        })

    )

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        for index, question in enumerate(self.questions, start=1):
            if question.question_type == 'MC':  # Multiple Choice Question
                self.fields[f'question_{index}'] = forms.ModelChoiceField(
                    queryset=question.answers.all(),
                    widget=forms.RadioSelect,
                    empty_label=None,
                    label=question.text,
                )
            elif question.question_type == 'TF':  # Text Field Question
                self.fields[f'question_{index}'] = forms.CharField(
                    label=question.text,
                    widget=forms.TextInput(attrs={'placeholder': 'Введите ответ', 'class': 'text-input'})
                )



class QuizFinalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        super(QuizFinalForm, self).__init__(*args, **kwargs)
        for index, question in enumerate(self.questions, start=1):
            if question.question_type == 'MC':
                self.fields[f'question_{index}'] = forms.ModelChoiceField(
                    queryset=question.answers.all(),
                    widget=forms.RadioSelect,
                    empty_label=None,
                    label=question.text,
                )
                self.fields[f'answer_{index}'] = forms.ModelChoiceField(
                    queryset=question.answers.all(),
                    empty_label=None,
                    widget=forms.HiddenInput(),
                )
            elif question.question_type == 'TF':
                self.fields[f'question_{index}'] = forms.CharField(
                    label=question.text,
                    widget=forms.TextInput(attrs={'placeholder': 'Введите ответ', 'class': 'text-input'})
                )
                self.fields[f'answer_{index}'] = forms.CharField(
                    initial=question.correct_answer,
                    widget=forms.HiddenInput(),
                )

class GroupForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите название группы'}),
        label=''  # это уберет метку 'name'
    )

    class Meta:
        model = Groups
        fields = ['name']


class DisciplineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DisciplineForm, self).__init__(*args, **kwargs)

        self.fields['groups'].queryset = Groups.objects.filter(user=user)
        self.fields['groups'].widget.attrs.update({
            'class': 'custom-select',
            'placeholder': 'Выберите группу',
        })
        self.fields['groups'].label = ""  # убираем метку

        self.fields['name'].widget.attrs.update({'placeholder': 'Введите название'})  # placeholder для поля name
        self.fields['name'].label = ""  # убираем метку

        self.fields['token'].widget.attrs.update({'placeholder': 'Введите токен'})  # placeholder для поля token
        self.fields['token'].label = ""  # убираем метку

    class Meta:
        model = Disciplin
        fields = ['name', 'token', 'groups' ]




from django import forms
from .models import Question, Answer


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['text', 'image', 'difficulty_block', 'question_type', 'disciplin']
#
#     def __init__(self, *args, **kwargs):
#         super(QuestionForm, self).__init__(*args, **kwargs)
#         self.fields['disciplin'].queryset = Disciplin.objects.none()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image', 'difficulty_block', 'question_type', 'disciplin']

    disciplin = forms.ModelChoiceField(
        queryset=Disciplin.objects.all(),
        to_field_name="name",
        label='Дисциплина',
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select'})  # добавлен класс
    )

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['disciplin'].label_from_instance = self.label_from_instance
        for field in self.fields.values():  # для каждого поля
            field.widget.attrs['class'] = 'form-control'  # добавляем класс
            if field.label:  # если у поля есть метка
                field.widget.attrs['placeholder'] = field.label  # устанавливаем placeholder


    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.groups.name})"





class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):  # Проверяем, является ли виджет чекбоксом
                field.widget.attrs['class'] = 'form-checkbox'  # применяем другой класс
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label  # используем метку поля как placeholder
                field.label = ""  # убираем метку поля




class TokenForm(forms.Form):
    token = forms.CharField(label="")