from django.contrib.auth.models import User

# Obtenha o usuário existente com o nome de usuário 'admin'
user = User.objects.get(username='admin')

# Atualize o email e defina uma nova senha
user.email = 'admin@example.com'  # Certifique-se de que o email seja válido
user.set_password('Ptclinic2024')  # Defina uma senha segura
user.is_active = True  # Garanta que a conta esteja ativa
user.is_staff = True  # Garanta que o usuário tenha permissões de staff
user.is_superuser = True  # Garanta que o usuário seja superusuário
user.save()

print("Usuário 'admin' atualizado com sucesso.")

# Liste todos os usuários com is_staff=True
staff_users = User.objects.filter(is_staff=True)
for user in staff_users:
    print(user.username, user.email)