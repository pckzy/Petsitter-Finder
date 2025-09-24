from django import forms
from .models import *
from django.core.exceptions import ValidationError
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
            # self.add_error('username', 'ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาเลือกชื่ออื่น')
            errors.append(ValidationError("ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาเลือกชื่ออื่น"))

        if phone and not re.match(r'^0\d{9}$', phone):
            # self.add_error('phone_number', 'กรุณากรอกเบอร์โทรศัพท์ที่ขึ้นต้นด้วย 0 และมีทั้งหมด 10 หลัก')
            errors.append(ValidationError("กรุณากรอกเบอร์โทรศัพท์ 10 หลักให้ถูกต้อง"))

        if errors:
            raise ValidationError(errors)

        return cleaned_data
