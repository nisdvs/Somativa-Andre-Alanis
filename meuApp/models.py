from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Usuario(models.Model):
    CATEGORIAS_USUARIO = (
        ('BIBLIOTECARIO', 'Bibliotecário'),
        ('AUTOR', 'Autor'),
        ('ADMIN', 'Administrador'),
        ('USUARIO', 'Usuário'),
    )

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_USUARIO)

    def __str__(self):
        return self.nome


class Formato(models.Model):
    CATEGORIAS_FORMATO = (
        ('EBOOK', 'E-book'),
        ('FISICO', 'Físico'),
    )

    categoria = models.CharField(max_length=20, choices=CATEGORIAS_FORMATO, primary_key=True)

    def __str__(self):
        return self.categoria


class Genero(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    nome = models.CharField(max_length=200)
    autor = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    ano = models.PositiveIntegerField()
    genero = models.ForeignKey('Genero', on_delete=models.CASCADE)
    qtd_paginas = models.PositiveIntegerField()
    formato = models.ForeignKey('Formato', on_delete=models.CASCADE)
    numero_edicao = models.PositiveIntegerField()
    descricao = models.TextField()
    valor_emprestimo = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_estoque = models.PositiveIntegerField()
    estrelas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    imagem_capa = models.ImageField(upload_to='livros_capas/')

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    livro = models.ForeignKey('Livro', on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    valor_total_emprestimo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.usuario.nome} - {self.livro.nome}"

    def save(self, *args, **kwargs):
        if not self.data_devolucao:
            self.data_devolucao = self.data_emprestimo + timezone.timedelta(days=7)
        super().save(*args, **kwargs)