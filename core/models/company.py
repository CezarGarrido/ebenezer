import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from core.models.base import Person
from django.contrib.auth.models import User, Group

def logo_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return f'images/company/logo_{instance.name}_{instance.id}{extension}'

class Company(Person):
    logo_file = models.ImageField(
        upload_to=logo_directory_path, default='images/logo.png', blank=True, null=True, verbose_name="Logo")
    cnae = models.CharField(max_length=10, blank=True, null=True, verbose_name="CNAE")
    iest = models.CharField(max_length=32, null=True, blank=True, verbose_name="Inscrição Estadual")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"


    def get_complete_path(self):
        if self.logo_file.name != 'images/logo.png':
            return os.path.join("MEDIA_ROOT", self.logo_file)
        else:
            return ''

    def save(self, *args, **kwargs):
        # Deletar logo se ja existir um
        try:
            obj = Company.objects.get(id=self.id)
            if obj.logo_file != self.logo_file and obj.logo_file != 'imagens/logo.png':
                obj.logo_file.delete(save=False)
        except:
            pass
        super(Company, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return u'%s' % self.name

# Deletar logo quando empresa for deletada
@receiver(post_delete, sender=Company)
def logo_post_delete_handler(sender, instance, **kwargs):
    # Nao deletar a imagem default 'logo.png'
    if instance.logo_file != 'imagens/logo.png':
        instance.logo_file.delete(False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, limit_choices_to={'person_type': 'J'}, verbose_name="Empresa")

    def __str__(self):
        return f"{self.user.username} ({self.company.name})"

class GroupCompany(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="group_company")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, limit_choices_to={'person_type': 'J'}, verbose_name="Empresa")

    def __str__(self):
        return f"{self.group.name} ({self.company.name})"