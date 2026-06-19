from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            current_widget = field.widget
            if isinstance(current_widget, forms.CheckboxInput):
                current_widget.attrs["class"] = f"{current_widget.attrs.get('class', '')} form-check-input".strip()
            elif isinstance(field, forms.DateTimeField):
                field.widget = forms.DateTimeInput(
                    attrs={"type": "datetime-local", "class": "form-control"},
                    format="%Y-%m-%dT%H:%M"
                )
                field.input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"]
            elif isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={"type": "date", "class": "form-control"},
                    format="%Y-%m-%d"
                )
                field.input_formats = ["%Y-%m-%d"]
            else:
                current_widget.attrs["class"] = f"{current_widget.attrs.get('class', '')} form-control".strip()
