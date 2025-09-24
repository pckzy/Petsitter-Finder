from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone

import re

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'กรอกชื่อผู้ใช้งาน',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'กรอกรหัสผ่าน',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username, password=password)
                cleaned_data["user"] = user
            except User.DoesNotExist:
                raise ValidationError("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง โปรดลองอีกครั้ง")

        return cleaned_data
    

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'phone_number', 'email', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'กรอกชื่อ', 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'กรอกนามสกุล', 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'username': forms.TextInput(attrs={'placeholder': 'กรอกชื่อผู้ใช้งาน', 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'กรอกเบอร์โทรศัพท์', 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'email': forms.EmailInput(attrs={'placeholder': 'กรอกอีเมล', 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'กรอกรหัสผ่าน', 'class': 'mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        phone = cleaned_data.get('phone_number')
        errors = []

        if username and User.objects.filter(username=username).exists():
            errors.append(ValidationError("ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาเลือกชื่ออื่น"))

        if phone and not re.match(r'^0\d{9}$', phone):
            errors.append(ValidationError("กรุณากรอกเบอร์โทรศัพท์ 10 หลักให้ถูกต้อง"))

        if errors:
            raise ValidationError(errors)

        return cleaned_data


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'pet_name', 'pet_type', 'special_instructions']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'pet_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'ชื่อสัตว์เลี้ยงของคุณ'
            }),
            'pet_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'special_instructions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'คำแนะนำพิเศษสำหรับการดูแลสัตว์เลี้ยงของคุณ'
            }),
        }

    def __init__(self, *args, **kwargs):
        sitter = kwargs.pop('sitter', None)
        super().__init__(*args, **kwargs)

        if sitter:
            self.fields['pet_type'].queryset = sitter.pet_types.all()

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        now = timezone.now()

        errors = []

        if start and start < now:
            errors.append(ValidationError("วันเริ่มต้นการจองต้องเป็นเวลาปัจจุบันหรืออนาคต"))

        if start and end and end <= start:
            errors.append(ValidationError("วันสิ้นสุดการจองต้องอยู่หลังวันเริ่มต้น"))

        if errors:
            raise ValidationError(errors)

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} ดาว') for i in range(1, 6)], attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'แบ่งปันประสบการณ์การใช้บริการ...'
            }),
        }