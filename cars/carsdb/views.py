from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from carsdb.forms import *
from carsdb.models import *

def parts_f(request):
    parts_list = parts.objects.all().order_by('-id')
    paginator = Paginator(parts_list, 15)  # 15 деталей на страницу
    
    page = request.GET.get('page')
    try:
        partsm = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, показываем первую страницу
        partsm = paginator.page(1)
    except EmptyPage:
        # Если страница за пределами диапазона, показываем последнюю страницу
        partsm = paginator.page(paginator.num_pages)
    
    context = {
        'partsm': partsm,
    }
    return render(request, 'carsdb/parts.html', context=context)

def cars_f(request):
    cars_list = cars.objects.all().order_by('-id')
    paginator = Paginator(cars_list, 15)  # 15 автомобилей на страницу
    
    page = request.GET.get('page')
    try:
        carsm = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, показываем первую страницу
        carsm = paginator.page(1)
    except EmptyPage:
        # Если страница за пределами диапазона, показываем последнюю страницу
        carsm = paginator.page(paginator.num_pages)
    
    context = {
        'carsm': carsm,
    }
    return render(request, 'carsdb/cars.html', context=context)

def acces_f(request):
    acess = car_part.objects.all()
    context={
        'acess':acess,
    }
    return render(request, 'carsdb/acessor.html', context=context)

def index(request):
    return render(request, 'carsdb/index.html')


# Обработчики ошибок
def error_403(request, exception=None):
    return render(request, 'carsdb/403.html', status=403)


def error_404(request, exception=None):
    return render(request, 'carsdb/404.html', status=404)


def error_500(request):
    return render(request, 'carsdb/500.html', status=500)


class addcars_f(PermissionRequiredMixin, CreateView):
    model = cars
    template_name = 'carsdb/addcars.html'
    success_url = '/cars/'
    form_class = AddCars
    permission_required = 'carsdb.add_cars'  # Разрешение на добавление автомобилей

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, f'Автомобиль "{form.cleaned_data["name"]}" успешно добавлен!')
            return HttpResponseRedirect(reverse('cars'))
        except IntegrityError as e:
            messages.error(self.request, 'Ошибка: Такой автомобиль уже существует или проблема с данными.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Произошла ошибка при добавлении автомобиля: {str(e)}')
            return self.form_invalid(form)


class UpdateCars(PermissionRequiredMixin, UpdateView):
    model = cars
    template_name = 'carsdb/editcars.html'
    form_class = AddCars
    success_url = reverse_lazy('cars')
    permission_required = 'carsdb.change_cars'  # Разрешение на изменение автомобилей

    def get_object(self, queryset=None):
        obj = get_object_or_404(cars, pk=self.kwargs['pk'])
        return obj
    
    def form_valid(self, form):
        try:
            # Сохраняем автомобиль (но не вызываем form.save(), так как у формы специальный метод)
            car = self.get_object()
            car.name = form.cleaned_data['name']
            car.margin = form.cleaned_data['margin']
            
            # Удаляем старые связи
            car_part.objects.filter(car=car).delete()
            
            # Создаем новые связи
            if 'parts' in form.cleaned_data and form.cleaned_data['parts']:
                for part in form.cleaned_data['parts']:
                    car_part.objects.create(car=car, part=part, name=car.name)
            else:
                messages.warning(self.request, 'Внимание: Автомобиль сохранен без деталей.')
            
            # Сохраняем автомобиль - это вызовет пересчет цены на основе новых связей
            car.save()
            messages.success(self.request, f'Автомобиль "{car.name}" успешно обновлен!')
            
            return HttpResponseRedirect(self.get_success_url())
            
        except IntegrityError as e:
            messages.error(self.request, 'Ошибка целостности данных: возможно, дублирование деталей.')
            return self.form_invalid(form)
        except DatabaseError as e:
            messages.error(self.request, 'Ошибка базы данных. Попробуйте позже.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Произошла непредвиденная ошибка: {str(e)}')
            return self.form_invalid(form)


class DeleteCars(PermissionRequiredMixin, DeleteView):
    model = cars
    template_name = 'carsdb/deletecars.html'
    success_url = reverse_lazy('cars')
    permission_required = 'carsdb.delete_cars'  # Разрешение на удаление автомобилей

    def get_object(self, queryset=None):
        obj = get_object_or_404(cars, pk=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Находим все детали, используемые в этом автомобиле
        car_obj = self.get_object()
        related_parts = car_obj.parts.all()
        context['related_parts'] = related_parts
        context['parts_count'] = related_parts.count()
        return context
    
    def delete(self, request, *args, **kwargs):
        try:
            car = self.get_object()
            car_name = car.name
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f'Автомобиль "{car_name}" успешно удален!')
            return response
        except DatabaseError as e:
            messages.error(request, 'Ошибка базы данных при удалении автомобиля.')
            return HttpResponseRedirect(reverse_lazy('cars'))
        except Exception as e:
            messages.error(request, f'Не удалось удалить автомобиль: {str(e)}')
            return HttpResponseRedirect(reverse_lazy('cars'))


class addparts_f(PermissionRequiredMixin, CreateView):
    model = parts
    template_name = 'carsdb/addparts.html'
    success_url = '/parts/'
    form_class = AddParts
    permission_required = 'carsdb.add_parts'  # Разрешение на добавление деталей

    def form_valid(self, form):
        try:
            w = form.save(commit=False)
            w.author = self.request.user
            w.save()
            messages.success(self.request, f'Деталь "{w.model_p}" успешно добавлена!')
            return HttpResponseRedirect(reverse('parts'))
        except IntegrityError as e:
            messages.error(self.request, 'Ошибка: Такая деталь уже существует.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Произошла ошибка при добавлении детали: {str(e)}')
            return self.form_invalid(form)


class UpdateParts(PermissionRequiredMixin, UpdateView):
    model = parts
    template_name = 'carsdb/editparts.html'
    form_class = AddParts
    success_url = reverse_lazy('parts')
    permission_required = 'carsdb.change_parts'  # Разрешение на изменение деталей

    def get_object(self, queryset=None):
        obj = get_object_or_404(parts, pk=self.kwargs['pk'])
        return obj
    
    def form_valid(self, form):
        try:
            part = form.save()
            messages.success(self.request, f'Деталь "{part.model_p}" успешно обновлена!')
            # После обновления детали нужно пересчитать цены всех автомобилей, которые используют эту деталь
            related_cars = cars.objects.filter(parts=part)
            for car in related_cars:
                car.save()  # Пересчитает цену
            if related_cars.count() > 0:
                messages.info(self.request, f'Обновлены цены {related_cars.count()} автомобиле(й) с этой деталью.')
            return HttpResponseRedirect(self.get_success_url())
        except DatabaseError as e:
            messages.error(self.request, 'Ошибка базы данных при обновлении детали.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Произошла ошибка при обновлении детали: {str(e)}')
            return self.form_invalid(form)


class DeleteParts(PermissionRequiredMixin, DeleteView):
    model = parts
    template_name = 'carsdb/deleteparts.html'
    success_url = reverse_lazy('parts')
    permission_required = 'carsdb.delete_parts'  # Разрешение на удаление деталей

    def get_object(self, queryset=None):
        obj = get_object_or_404(parts, pk=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Находим все автомобили, которые используют эту деталь
        part_obj = self.get_object()
        related_cars = cars.objects.filter(parts=part_obj)
        context['related_cars'] = related_cars
        context['cars_count'] = related_cars.count()
        return context
    
    def delete(self, request, *args, **kwargs):
        try:
            part = self.get_object()
            part_name = part.model_p
            related_cars_count = cars.objects.filter(parts=part).count()
            
            if related_cars_count > 0:
                messages.warning(request, f'Внимание: Деталь используется в {related_cars_count} автомобиле(ях). Их цены будут пересчитаны.')
            
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f'Деталь "{part_name}" успешно удалена!')
            return response
        except DatabaseError as e:
            messages.error(request, 'Ошибка базы данных при удалении детали.')
            return HttpResponseRedirect(reverse_lazy('parts'))
        except Exception as e:
            messages.error(request, f'Не удалось удалить деталь: {str(e)}')
            return HttpResponseRedirect(reverse_lazy('parts'))

