from django.forms import ModelForm

from wushu.models import Coach


class CoachForm(ModelForm):
    class Meta:
        model = Coach
