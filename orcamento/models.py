
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    """Manager para o model user."""

    def create_user(self, email, password=None, **extra_field):
        """Criar, salvar e retornar um novo usuário"""
        email = self.normalize_email(email)
        
        if not email:
            raise ValueError('Usuário deve ter um endereço de email.')
    
        exist_email = self.get_queryset().filter(email=email).exists()
        if exist_email:
            raise ValueError('Esse email já existe.')
    
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, **extra_field):
        """Create, save e return um super usuário"""
        user = self.create_user(email, password, **extra_field)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
        
    

class User(AbstractBaseUser, PermissionsMixin):
    """Model para os usuários do sistema."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'Usuario'


class Receita(models.Model):
    descricao = models.CharField(max_length=255, blank=True, null=True)
    valor = models.FloatField()
    data = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        default=None, 
        blank=True,
        null=True,
        db_column='usuario',

    )
    class Meta:
        db_table = 'Receitas'


class Despesa(models.Model):
    CODIGO_DESPESA =(
        ('F', 'Despesa fixa'),
        ('E', 'Despesa eventual')
    )
    descricao = models.CharField(max_length=255, blank=True, null=True)
    valor = models.FloatField()
    data = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        default=None, 
        blank=True,
        null=True,
        db_column='usuario',
    )
    codigo_despesa = models.CharField(max_length=1, choices=CODIGO_DESPESA)

    class Meta:
        db_table = 'Despesas'

class ResumoMes(models.Model):
    """Tabela que é atualizada toda vez que uma receita e despesa são cadastradas."""
    data = models.DateField()
    receita_total = models.FloatField(null=True, blank=True, default=0)
    despesa_fixa_total = models.FloatField(null=True, blank=True, default=0)
    despesa_eventual_total = models.FloatField(null=True, blank=True, default=0)
    saldo_final = models.FloatField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        default=None, 
        blank=True,
        null=True,
        db_column='usuario',

    )

    class Meta:
        db_table = 'Resumo do Mes'

    def save(self, *args, **kwargs):
        self.saldo_final = self.receita_total - (self.despesa_fixa_total + self.despesa_eventual_total)
        return super().save(*args, **kwargs)
