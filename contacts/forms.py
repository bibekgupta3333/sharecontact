from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'mobile', 'email',
                  'address', 'image', 'profession', 'address', 'image', 'profession', 'email', "linkedin_url", 'facebook_url', 'github_url', 'bio_url', 'search_tags', 'status')

    def __init__(self,  *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True, *args, **kwargs):
        obj = super(ContactForm, self).save(commit=False, *args, **kwargs)

        from django.utils.text import slugify
        obj.slug = slugify(obj.name)
        if commit:
            obj.save()
        return obj


class ContactCreateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'mobile', 'email', 'author',
                  'address', 'image', 'profession', 'email',  "linkedin_url", 'facebook_url', 'github_url', 'bio_url', 'search_tags', 'status')

    def __init__(self,  *args, **kwargs):
        super(ContactCreateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'style': 'display:none;'})
        self.fields['author'].label = ''
