from django.contrib import admin

from apps.docs.selectors.pay_doc import pay_doc_model


@admin.register(pay_doc_model)
class PayDocAdmin(admin.ModelAdmin):
    """Класс отображения документов об оплате в адмиинистративной панели"""
    list_fields = ('group_code', 'student_display_name', 'date_create')
    search_fields = ('group__code', 'student__display_name')

    def group_code(self, obj):
        return obj.group.code

    def student_display_name(self, obj):
        return obj.student.display_name

    group_code.short_description = 'Шифр группы'
    student_display_name.short_description = 'ФИО студента'
