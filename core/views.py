from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Item as Model
from .forms import ItemForm as ModelForm

def ping_view(request):
    return HttpResponse("pong", content_type="text/plain", status=200)

def list_view(request):
    all_fields = Model._meta.fields
    headers = [field.verbose_name for field in all_fields]
    
    records = []
    for item in Model.objects.all():
        row_values = [getattr(item, field.name) for field in all_fields]
        records.append({"pk": item.pk, "values": row_values})
        
    return render(request, "core/index.html", {"headers": headers, "rows": records})

def create_view(request):
    if request.method == "POST":
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно создана.")
            return redirect("index")
        messages.error(request, "Исправьте ошибки в форме.")
        return render(request, "core/form.html", {"form": form}, status=400)
    
    return render(request, "core/form.html", {"form": ModelForm()})

def update_view(request, pk):
    instance = get_object_or_404(Model, pk=pk)
    if request.method == "POST":
        form = ModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно обновлена.")
            return redirect("index")
        messages.error(request, "Исправьте ошибки в форме.")
        return render(request, "core/form.html", {"form": form, "object": instance}, status=400)
        
    return render(request, "core/form.html", {"form": ModelForm(instance=instance), "object": instance})

def delete_view(request, pk):
    instance = get_object_or_404(Model, pk=pk)
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Запись успешно удалена.")
        return redirect("index")
        
    return render(request, "core/confirm_delete.html", {"object": instance})
