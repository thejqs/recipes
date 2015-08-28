from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django import forms
from django.forms import ModelForm
from main.models import Recipe, Ingredient


class UserCreationForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    username = forms.CharField(widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Username',
                                   }))

    email = forms.CharField(validators=[EmailValidator],
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Email',
                                }))

    password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password',
                                    }))

    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password Verification',
                                    }))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class RecipeForm(ModelForm):
    RATING_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    DIFFICULTY_CHOICES = (
        (0, ''),
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard'),
    )

    MEAL_CHOICES = (
        (0, ''),
        (1, 'Breakfast'),
        (2, 'Lunch'),
        (3, 'Dinner'),
        (4, 'Snack'),
        (5, 'Dessert'),
    )
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}))
    instructions = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Instructions'}))
    notes = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Notes'}))
    source = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Where you got the recipe from'}))
    servings = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    rating = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=RATING_CHOICES)
    difficulty = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=DIFFICULTY_CHOICES)
    meal = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=MEAL_CHOICES)

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['creator', 'created', 'modified', 'exclude_from_search']


class IngredientForm(ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'quantity', 'recipe']
