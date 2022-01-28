from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=50, verbose_name='Titulo')
    
    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phonenumber = models.CharField(max_length=50)
    email = models.EmailField()
    job = models.CharField(max_length=100)
    company = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.get_fullname()
    
    def get_fullname(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('id',)


class Course(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    
    def __str__(self) -> str:
        return self.name
