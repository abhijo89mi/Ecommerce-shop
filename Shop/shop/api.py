from django.core.serializers.json import DjangoJSONEncoder


JSON_ENCODER = DjangoJSONEncoder().encode
def api(request, obj_model, obj_id=None):
    model = get_model(*obj_model.split())
    if model is None:
        raise Http404
    if obj_id is not None:
        results = model.objects.get(id=obj_id)
    else:
        results = model.objects.all()
    return HttpResponse(JSON_ENCODE(list(results)),
                        mimetype='application/javascript')
