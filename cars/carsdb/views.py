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
    paginator = Paginator(parts_list, 15)  # 15 parts per page
    
    page = request.GET.get('page')
    try:
        partsm = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, show the first page
        partsm = paginator.page(1)
    except EmptyPage:
        # If page is out of range, show the last page
        partsm = paginator.page(paginator.num_pages)
    
    context = {
        'partsm': partsm,
    }
    return render(request, 'carsdb/parts.html', context=context)

def cars_f(request):
    cars_list = cars.objects.all().order_by('-id')
    paginator = Paginator(cars_list, 15)  # 15 cars per page
    
    page = request.GET.get('page')
    try:
        carsm = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, show the first page
        carsm = paginator.page(1)
    except EmptyPage:
        # If page is out of range, show the last page
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


# Error handlers
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
    permission_required = 'carsdb.add_cars'  # Permission to add cars

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, f'Car "{form.cleaned_data["name"]}" was added successfully!')
            return HttpResponseRedirect(reverse('cars'))
        except IntegrityError as e:
            messages.error(self.request, 'Error: That car already exists or the data is invalid.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'An error occurred while adding the car: {str(e)}')
            return self.form_invalid(form)


class UpdateCars(PermissionRequiredMixin, UpdateView):
    model = cars
    template_name = 'carsdb/editcars.html'
    form_class = AddCars
    success_url = reverse_lazy('cars')
    permission_required = 'carsdb.change_cars'  # Permission to change cars

    def get_object(self, queryset=None):
        obj = get_object_or_404(cars, pk=self.kwargs['pk'])
        return obj
    
    def form_valid(self, form):
        try:
            # Save the car (do not call form.save() — the form has a custom create method)
            car = self.get_object()
            car.name = form.cleaned_data['name']
            car.margin = form.cleaned_data['margin']
            
            # Remove old links
            car_part.objects.filter(car=car).delete()
            
            # Create new links
            if 'parts' in form.cleaned_data and form.cleaned_data['parts']:
                for part in form.cleaned_data['parts']:
                    car_part.objects.create(car=car, part=part, name=car.name)
            else:
                messages.warning(self.request, 'Warning: Car saved with no parts.')
            
            # Saving the car recalculates the price based on the new links
            car.save()
            messages.success(self.request, f'Car "{car.name}" was updated successfully!')
            
            return HttpResponseRedirect(self.get_success_url())
            
        except IntegrityError as e:
            messages.error(self.request, 'Data integrity error: possible duplicate parts.')
            return self.form_invalid(form)
        except DatabaseError as e:
            messages.error(self.request, 'Database error. Please try again later.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'An unexpected error occurred: {str(e)}')
            return self.form_invalid(form)


class DeleteCars(PermissionRequiredMixin, DeleteView):
    model = cars
    template_name = 'carsdb/deletecars.html'
    success_url = reverse_lazy('cars')
    permission_required = 'carsdb.delete_cars'  # Permission to delete cars

    def get_object(self, queryset=None):
        obj = get_object_or_404(cars, pk=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Find all parts used in this car
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
            messages.success(request, f'Car "{car_name}" was deleted successfully!')
            return response
        except DatabaseError as e:
            messages.error(request, 'Database error while deleting the car.')
            return HttpResponseRedirect(reverse_lazy('cars'))
        except Exception as e:
            messages.error(request, f'Failed to delete the car: {str(e)}')
            return HttpResponseRedirect(reverse_lazy('cars'))


class addparts_f(PermissionRequiredMixin, CreateView):
    model = parts
    template_name = 'carsdb/addparts.html'
    success_url = '/parts/'
    form_class = AddParts
    permission_required = 'carsdb.add_parts'  # Permission to add parts

    def form_valid(self, form):
        try:
            w = form.save(commit=False)
            w.author = self.request.user
            w.save()
            messages.success(self.request, f'Part "{w.model_p}" was added successfully!')
            return HttpResponseRedirect(reverse('parts'))
        except IntegrityError as e:
            messages.error(self.request, 'Error: That part already exists.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'An error occurred while adding the part: {str(e)}')
            return self.form_invalid(form)


class UpdateParts(PermissionRequiredMixin, UpdateView):
    model = parts
    template_name = 'carsdb/editparts.html'
    form_class = AddParts
    success_url = reverse_lazy('parts')
    permission_required = 'carsdb.change_parts'  # Permission to change parts

    def get_object(self, queryset=None):
        obj = get_object_or_404(parts, pk=self.kwargs['pk'])
        return obj
    
    def form_valid(self, form):
        try:
            part = form.save()
            messages.success(self.request, f'Part "{part.model_p}" was updated successfully!')
            # Recalculate prices for all cars that use this part
            related_cars = cars.objects.filter(parts=part)
            for car in related_cars:
                car.save()  # Recalculates the price
            if related_cars.count() > 0:
                messages.info(self.request, f'Updated prices for {related_cars.count()} car(s) using this part.')
            return HttpResponseRedirect(self.get_success_url())
        except DatabaseError as e:
            messages.error(self.request, 'Database error while updating the part.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'An error occurred while updating the part: {str(e)}')
            return self.form_invalid(form)


class DeleteParts(PermissionRequiredMixin, DeleteView):
    model = parts
    template_name = 'carsdb/deleteparts.html'
    success_url = reverse_lazy('parts')
    permission_required = 'carsdb.delete_parts'  # Permission to delete parts

    def get_object(self, queryset=None):
        obj = get_object_or_404(parts, pk=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Find all cars that use this part
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
                messages.warning(request, f'Warning: Part is used in {related_cars_count} car(s). Their prices will be recalculated.')
            
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f'Part "{part_name}" was deleted successfully!')
            return response
        except DatabaseError as e:
            messages.error(request, 'Database error while deleting the part.')
            return HttpResponseRedirect(reverse_lazy('parts'))
        except Exception as e:
            messages.error(request, f'Failed to delete the part: {str(e)}')
            return HttpResponseRedirect(reverse_lazy('parts'))
