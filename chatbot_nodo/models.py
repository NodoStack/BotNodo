from django.db import models

class ChatUser(models.Model):
    telefono = models.CharField(max_length=30, unique=True)
    estado = models.CharField(max_length=50, default="START")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.telefono


class ChatMessage(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    texto = models.TextField()
    direccion = models.CharField(max_length=3)  # 'in' / 'out'
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.direccion}: {self.texto[:20]}"


class Lead(models.Model):
    STATUS_CHOICES = (
        ("nuevo", "Nuevo"),
        ("interesado", "Interesado"),
        ("calificado", "Calificado"),
        ("agenda", "Agendó reunión"),
        ("descartado", "Descartado"),
    )

    user = models.OneToOneField(ChatUser, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="nuevo"
    )

    tipo_proyecto = models.CharField(max_length=50, blank=True, null=True)
    descripcion_proyecto = models.TextField(blank=True, null=True)
    idea = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Lead {self.user.telefono} ({self.status})"

