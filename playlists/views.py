# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from playlists.models import Playlist, PlaylistTracks
from annoying.decorators import ajax_request
import simplejson as json


@ajax_request
@login_required
def list(request):
    playlist_objects = Playlist.objects.filter(user=request.user).order_by("-id")
    playlists = [pl.for_json() for pl in playlist_objects]
    return {"status": "OK", "count": len(playlists), "lists": playlists}


@ajax_request
@login_required
def new(request):
    name = request.POST.get("name")
    if not name:
        return {"status": "NeOK", "message": u"No specified playlist name"}

    playlist = Playlist.objects.create(user=request.user, title=name)
    playlist.save()
    return {"status": "OK", "message": u"Playlist created"}


@ajax_request
@login_required
def remove(request):
    id = request.POST.get("id")
    if not id:
        return {"status": "NeOK", "message": u"No ID"}

    try:
        Playlist.objects.get(id=id).delete()
        return {"status": "OK", "message": u"Playlist deleted"}
    except:
        return {"status": "NeOK", "message": u"Failed to delete playlist"}


@ajax_request
@login_required
def add(request):
    id = request.POST.get("id")
    tracks = json.loads(request.POST.get("tracks"))
    if not id:
        return {"status": "NeOK", "message": u"No ID"}

    playlist = Playlist.objects.get(id=id)
    if playlist.count >= 150:
        return {"status": "NeOK", "message": u"A limit of 150 tracks. Create a new playlist or remove tracks from this playlist"}

    for track in tracks:
        if PlaylistTracks.objects.filter(playlist=playlist, track_id=track).count() == 0:
            track = PlaylistTracks.objects.create(playlist=playlist, track_id=track)
            track.save()
            if track.track_position >= 150:
                return {"status": "NeOK", "message": u"Some of the tracks were not added because there is a limit of 150 tracks. Remove tracks or move to another playlist"}

    return {"status": "OK", "message": u"Tracks added to playlist"}


@ajax_request
@login_required
def get(request):
    id = request.POST.get("id")
    if not id:
        return {"status": "NeOK", "message": u"No ID"}

    playlist = Playlist.objects.get(id=id)
    track_objects = PlaylistTracks.objects.filter(playlist__id=id).order_by("track_position")[:150]
    track_list = [t.for_json() for t in track_objects]
    return {"status": "OK", "list": {"_id": id, "tracks": track_list, "title": playlist.title}}


@ajax_request
@login_required
def delete(request):
    playlist_id = request.POST.get("playlist_id")
    track_id = request.POST.get("track_id")
    if not playlist_id or not track_id:
        return {"status": "NeOK", "message": u"No ID"}

    try:
        PlaylistTracks.objects.filter(track_id=track_id, playlist__id=playlist_id).delete()
        return {"status": "OK", "message": u"Track with ID %s deleted" % track_id}
    except Exception, ex:
        return {"status": "NeOK", "message": u"Problem with deleting playlist: " + ex}


@ajax_request
@login_required
def sorted(request):
    playlist_id = request.POST.get("id")
    sorted_ids = json.loads(request.POST.get("sorted"))
    if not playlist_id:
        return {"status": "NeOK", "message": u"Playlist ID not specified"}
    if not sorted_ids:
        return {"status": "NeOK", "message": u"List is empty"}

    try:
        for position, track_id in enumerate(sorted_ids):
            track = PlaylistTracks.objects.get(playlist__id=playlist_id, track_id=track_id)
            if track:
                track.track_position = position
                track.save_without_recount()

        return {"status": "OK", "message": u"Playlist successfully saved"}
    except Exception, ex:
        return {"status": "NeOK", "message": ex}
