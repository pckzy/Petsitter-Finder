from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class PetType(models.Model):
    name = models.CharField(max_length=50, verbose_name='ประเภทสัตว์')
    icon = models.CharField(max_length=10, default='🐾')
    
    def __str__(self):
        return self.name
    
class PetSitter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name='แนะนำตัว')
    experience_years = models.PositiveIntegerField(verbose_name='ประสบการณ์ (ปี)')
    location = models.CharField(max_length=100, verbose_name='พื้นที่ให้บริการ')
    hourly_rate_min = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='ราคาต่ำสุด/ชม.')
    hourly_rate_max = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='ราคาสูงสุด/ชม.')
    pet_types = models.ManyToManyField(PetType, verbose_name='ประเภทสัตว์ที่ดูแลได้')
    is_available = models.BooleanField(default=True, verbose_name='พร้อมรับงาน')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รออนุมัติ'),
        ('confirmed', 'ยืนยันแล้ว'),
        ('completed', 'เสร็จสิ้น'),
        ('cancelled', 'ยกเลิก'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    sitter = models.ForeignKey(PetSitter, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateTimeField(verbose_name='วันเวลาเริ่มต้น')
    end_date = models.DateTimeField(verbose_name='วันเวลาสิ้นสุด')
    pet_name = models.CharField(max_length=50, verbose_name='ชื่อสัตว์เลี้ยง')
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    special_instructions = models.TextField(blank=True, verbose_name='คำแนะนำพิเศษ')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='ราคารวม')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.customer.first_name} - {self.sitter.user.first_name} ({self.start_date.date()})'