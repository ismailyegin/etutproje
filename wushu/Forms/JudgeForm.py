from django.forms import ModelForm

from wushu.models import Judge


class JudgeForm(ModelForm):
    class Meta:
        model = Judge
