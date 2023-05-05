from django.contrib import admin
from .models import Emprestimo, Pagamento

# Register your models here.
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(cliente=request.user)


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(cliente=request.user)


