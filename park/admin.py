from django.contrib import admin

from park.models import Option as OptionModel
from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel
from park.models import BookMark as BookMarkModel


admin.site.register(OptionModel)
admin.site.register(ParkModel)
admin.site.register(ParkCommentModel)
admin.site.register(BookMarkModel)