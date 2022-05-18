from venue.models import VenuePictures


def get_venue_picture_by_id(picture_id):
    return VenuePictures.objects.get(pk=picture_id)


def delete_venue_picture(picture_id):
    get_venue_picture_by_id(picture_id).delete()
