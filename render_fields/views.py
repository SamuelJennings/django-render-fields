class FieldsetsMixin:
    fields = []
    fieldsets = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fieldsets"] = self.get_fieldsets()
        return context

    def get_fieldsets(self):
        """
        Returns a list of fieldsets for the object.
        """
        fieldsets = None
        if self.fields and not self.fieldsets:
            # If fields are defined but fieldsets are not, create fieldsets from fields
            fieldsets = [
                (
                    None,
                    {
                        "fields": self.fields,
                    },
                )
            ]
        elif isinstance(self.fieldsets, dict):
            # convert dict to list of tuples
            fieldsets = [(key, value) for key, value in self.fieldsets.items()]
        elif isinstance(self.fieldsets, (list, tuple)):
            # if fieldsets is already a list or tuple, do nothing
            fieldsets = self.fieldsets

        if fieldsets is None:
            # If fieldsets are not defined, raise an error
            raise ValueError("You must provide either field or fieldsets attribute on the view class.")
        return fieldsets
