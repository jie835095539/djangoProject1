from django import forms
class BootStrapModelForm(forms.ModelForm):
    """继承类，modelform样式修改与附加"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            #print(name,field)
            if field.widget.attrs:
                field.widget.attrs["class"]="form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder":field.label
                                      }