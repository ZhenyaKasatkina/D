from django.core.exceptions import ValidationError

from django import forms
from django.forms import BooleanField


from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("created_at", "updated_at",)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data.get('product_name')
        words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')
        for word in words:
            if word in cleaned_data:
                raise ValidationError(f"Слово {word} не может содержаться в названии")
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')
        for word in words:
            if word in cleaned_data:
                raise ValidationError(f"Слово {word} не может содержаться в описании")
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"

    def clean_is_active(self):
        # active = []
        cleaned_data = self.cleaned_data.get('is_active')
        # print(f'сейчас {cleaned_data}')
        active_version = Version.objects.filter(is_active=self.cleaned_data.get('is_active'),
                                                product=self.cleaned_data.get('product')).exists()

        # active.append(cleaned_data) if cleaned_data else None
        # print(len(active))
        # if len(active) == 1 and cleaned_data and active_version:
        if cleaned_data and active_version:
            raise ValidationError(f"Активная версия может быть только одна у продукта. \n"
                                  f"Снимите галочку активности с предыдущей версии, сохрани, \n"
                                  f"и только потом выбирай активную")
        return cleaned_data






