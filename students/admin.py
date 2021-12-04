from django.contrib import admin
from adminsortable.admin import SortableAdmin

from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Lesson, Word, MyWord

from import_export.admin import ImportMixin, ImportExportActionModelAdmin
from import_export.fields import Field
from import_export.formats import base_formats
from import_export.resources import ModelResource
from import_export import widgets
from import_export.widgets import ForeignKeyWidget

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin import AdminSite


@admin.register(MyWord)
class MyWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'new_word', 'meaning')

# import csv settings
class LessonResource(ModelResource):
    id = Field(attribute='id', column_name='UUID')
    student = Field(attribute='student', widget=ForeignKeyWidget(User, 'username'))
    course = Field(attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    teacher = Field(attribute='teacher', widget=ForeignKeyWidget(User, 'username'))
    textbook = Field(attribute='textbook')
    page = Field(attribute='page')
    score = Field(attribute='score')
    comment = Field(attribute='comment')
    created = Field(attribute='created')
    updated = Field(attribute='updated')
    completed = Field(attribute='completed')


    class Meta:
        model = Lesson

        import_order = ('id', 'student', 'course', 'teacher', 'textbook', 'page', 'score', 'comment', 'created', 'updated', 'completed')
        import_id_fields = ['id']


class WordResource(ModelResource):
    id = Field(attribute='id', column_name='UUID')
    word_eng = Field(attribute='word_eng')
    word_jap = Field(attribute='word_jap')

    class Meta:
        model = Word
        import_order = ('id', 'word_eng', 'word_jap',)
        import_id_fields = ['id']


class SubModelResource(ModelResource):
    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names
    # overriding import_row to ignore errors and skip rows that fail to import
    # without failing the entire import
    def import_row(self, row, instance_loader, **kwargs):
        import_result = super(ModelResource, self).import_row(row, instance_loader, **kwargs)

        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [row.get(name, '') for name in self.get_field_names()]
            # Add a column with the error message
            import_result.diff.append("Errors: {}".format(
                [err.error for err in import_result.errors]
            ))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP
        return import_result


class LessonAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'teacher', 'textbook', 'page', 'completed', 'score', 'comment', 'created', 'updated')
    # avoiding n+1 issue
    list_select_related = ('student', 'course', 'teacher',)
    # Able to edit on the list display
    list_editable = ('teacher', 'score', 'comment')
    # Able to search by student, course, teacher, textbook, and dates
    search_fields = ('student__username', 'course__course_name', 'teacher__username', 'textbook', 'created', 'updated')
    ordering = ('textbook', 'page')
    # Able to filter by course, textbook, and dates
    list_filter = ('course', 'textbook', 'created', 'updated',)
    # Change the status of the lesson: completed or unfinished
    actions = ("completed", 'unfinished')
    # import csv setting
    resource_class = LessonResource
    formats = [base_formats.CSV]


    def completed(self, request, queryset):
        queryset.update(completed=True)

    completed.short_description = "Completed"

    def unfinished(self, request, queryset):
        queryset.update(completed=False)

    unfinished.short_description = "Unfinished"


# Teachers can access admin page to edit lessons
class TeacherAdminSite(AdminSite):
    site_header = 'MyPage'
    site_title = 'MyPage'
    index_title = 'Home'
    
    site_url = None
    # Non-staff users to access TeacherAdminSite with limited permissions
    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active


class WordAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'word_eng', 'word_jap')
    list_editable = ('word_eng', 'word_jap')

    resource_class = WordResource
    formats = [base_formats.CSV]

# Instantiate new admin-site and set models to show
mypage_site = TeacherAdminSite(name="mypage")
mypage_site.register(Lesson, LessonAdmin)
mypage_site.register(Word, WordAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Word, WordAdmin)




