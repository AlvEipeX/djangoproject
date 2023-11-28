from django import forms


class CreateNewTask(forms.Form):
    title = forms.CharField(label="Titulo de tarea", max_length=200)
    description = forms.CharField(
        label="descripcion tarea", widget=forms.Textarea)


class CreateNewOtro(forms.Form):
    a = forms.CharField(label="AAA", max_length=200)
    b = forms.CharField(label="EEE", max_length=200)
