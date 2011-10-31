from django import forms
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _

class EntryAddForm(forms.Form):

    title = forms.CharField(min_length=3, max_length=40,
                           label=_('Title'),
                           widget=forms.TextInput(attrs={'size':'40',
                                                         'autocomplete':'off'}))
    
    author = forms.CharField(min_length=3, max_length=40,
                           label=_('Author'),
                           widget=forms.TextInput(attrs={'size':'40',
                                                         'autocomplete':'off'}))
    
    content = forms.CharField(widget=TinyMCE(attrs={'cols':60, 'rows':20}))
    

class EntryEditForm(forms.Form):

    name = forms.CharField(min_length=3, max_length=40,
                           label=_('News Entry Name'),
                           widget=forms.TextInput(attrs={'size':'40',
                                                         'autocomplete':'off'}))
    summary = forms.CharField(min_length=3, max_length=40,
                           label=_('News Entry Summary'),
                           widget=forms.TextInput(attrs={'size':'250',
                                                         'autocomplete':'off'}))

