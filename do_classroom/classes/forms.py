from django import forms

from models import Class, Teacher
from utils.do_tools import list_regions, list_images, list_sizes

class NewClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewClassForm, self).__init__(*args, **kwargs)
        self.fields['droplet_image'] = forms.ChoiceField(choices=list_images())
        self.fields['droplet_region'] = forms.ChoiceField(choices=list_regions(),
                                        initial='nyc3')
        self.fields['droplet_size'] = forms.ChoiceField(choices=list_sizes())

    class Meta:
        model = Class
        fields = ['name', 'droplet_image', 'droplet_size', 'droplet_region',
                  'class_size', 'packages']
                  #'droplet_priv_net', 'droplet_ipv6', 'class_size']
        widgets = {
            'packages': forms.TextInput(),
        }