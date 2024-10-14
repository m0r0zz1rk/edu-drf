from django.contrib import admin

from apps.docs.selectors.pay_doc import pay_doc_model


@admin.register(pay_doc_model)
class PayDocAdmin(admin.ModelAdmin):
    """Класс отображения документов об оплате в адмиинистративной панели"""
    list_fields = ('student_display_name', 'date_create')
    search_fields = ('student__display_name', )

    def student_display_name(self, obj):
        return obj.student.display_name

    student_display_name.short_description = 'ФИО студента'
