from core.models import User

admin = User.objects.get(username='admin123')
print(f'Username: {admin.username}')
print(f'Role: "{admin.role}"')
print(f'Has ADMIN role: {admin.role == "ADMIN"}')

# List all users and their roles
print("\nAll users:")
for user in User.objects.all():
    print(f"  {user.username}: {user.role}")
