from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi, BaseView, expose, has_access

from . import appbuilder, db

from .models import UploadRegistry

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


#db.create_all()


from wtforms.fields import SelectField
from wtforms.form import Form

tab_data_choices_legacy_raw = ['SDTMv EARLY PHASE IG 3.1.2 Amendment1', 'SDTMv LATE PHASE IG 3.1.2 Amendment1', 
'SDTMv IG 3.2', 'GDM', 'SHOGUN', 'OTHER']
tab_data_legacy_choices = [(x,x) for x in tab_data_choices_legacy_raw]
tab_data_choices_cdisc_raw = ["SDTM IG 3.1.2 Amendment 1", "SDTM IG 3.2", "OTHER"]
tab_data_cdisc_choices = [(x,x) for x in tab_data_choices_cdisc_raw]
tab_data_choices = {'legacy': tab_data_legacy_choices,'cdisc': tab_data_cdisc_choices}


class UploadRegistryView(ModelView):


    datamodel = SQLAInterface(UploadRegistry)                    

    list_title = "Upload History"
    list_columns = ["fab_id", "car_brand", "car_model", "created", "uploaded_file_name"]

#db.create_all()

# register views
appbuilder.add_link("Upload File", icon="fa-upload", href="/uploadregistryview/add")
#appbuilder.add_view(SpaUploaderView, "Upload")
appbuilder.add_view(UploadRegistryView, "History", icon="fa-history")

# add roles

public_perms = {"can_about", "menu_access"}
contrib_perms = {"can_list", "can_show", "menu_access", "can_about", "can_add", "can_spauploader"}
views_to_add_perms = ["UploadRegistryView", "History", "Upload File"]

role_contributor = appbuilder.sm.find_role('Contributor')
role_public = appbuilder.sm.find_role('Public')

if not role_contributor:
    appbuilder.sm.add_role('Contributor')
    
for view_name in views_to_add_perms:
    print(view_name)
    view_menu = appbuilder.sm.find_view_menu(view_name)
    perms = appbuilder.sm.find_permissions_view_menu(view_menu)
    for perm in perms:
        if perm.permission.name in public_perms:
            appbuilder.sm.add_permission_role(role_public, perm)
        if perm.permission.name in contrib_perms and role_contributor:
            appbuilder.sm.add_permission_role(role_contributor, perm)

print("Loading views finished!!!")
