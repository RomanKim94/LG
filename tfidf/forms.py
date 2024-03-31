from django.forms import ModelForm

from tfidf.models import TextFile


class FileForm(ModelForm):

    class Meta:
        model = TextFile
        fields = ['file']
