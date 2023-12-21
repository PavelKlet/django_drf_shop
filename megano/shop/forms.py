from django import forms
from django.utils import timezone
from .models import Sale


class SaleDateForm(forms.ModelForm):
    dateFrom = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    dateTo = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def clean(self):
        cleaned_data = super().clean()
        dateFrom = cleaned_data.get("dateFrom")
        dateTo = cleaned_data.get("dateTo")
        current_date = timezone.now().date()

        if dateFrom and dateTo:
            if dateTo < dateFrom or dateFrom < current_date:
                raise forms.ValidationError("Некорректный ввод даты")

        product = cleaned_data.get("product")
        existing_sales = Sale.objects.filter(
            product=product,
        )

        if existing_sales.exists():
            raise forms.ValidationError("Распродажа выбранного товара уже существует ")
        return cleaned_data
