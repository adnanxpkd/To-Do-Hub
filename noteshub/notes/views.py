from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm


# 🧾 All Notes List
@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user, is_deleted=False).order_by('-is_pinned', '-updated_at')
    return render(request, "notes/list.html", {"notes": notes})


# ➕ Add Note
@login_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully!")
            return redirect("notes_list")
    else:
        form = NoteForm()
    return render(request, "notes/add.html", {"form": form})


# ✏️ Edit Note
@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect("notes_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/edit.html", {"form": form})


# 🗑️ Move Note to Trash (soft delete)
@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)
    note.is_deleted = True
    note.save()
    messages.warning(request, "Note moved to trash.")
    return redirect("notes_list")


# 🧹 Trash List
@login_required
def trash_list(request):
    notes = Note.objects.filter(user=request.user, is_deleted=True)
    return render(request, "notes/trash.html", {"notes": notes})


# 🔁 Restore Note from Trash
@login_required
def restore_note(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)
    note.is_deleted = False
    note.save()
    messages.success(request, "Note restored successfully!")
    return redirect("trash_list")


# 💀 Delete Note Permanently
@login_required
def delete_permanently(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)
    note.delete()
    messages.error(request, "Note deleted permanently.")
    return redirect("trash_list")
