from django.shortcuts import render, get_object_or_404, redirect
from .models import Member
import os
import subprocess

def add_member(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Enroll member using PassKit SDK
        result = subprocess.run(
            ["python", "path/to/enrol-member.py", email, first_name, last_name],
            capture_output=True, text=True
        )

        # Process the result to get the member ID from PassKit
        passkit_member_id = result.stdout.strip()  # Adjust parsing as needed

        member = Member.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            passkit_member_id=passkit_member_id
        )
        return redirect('members:member_list')

    return render(request, 'members/add_member.html')

def member_list(request):
    members = Member.objects.all()
    return render(request, 'members/member_list.html', {'members': members})

def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.first_name = request.POST.get('first_name')
        member.last_name = request.POST.get('last_name')
        member.email = request.POST.get('email')
        member.phone_number = request.POST.get('phone_number')

        # Update member using PassKit SDK
        subprocess.run(
            ["python", "path/to/update-member.py", member.passkit_member_id, member.email, member.first_name, member.last_name],
            capture_output=True, text=True
        )

        member.save()
        return redirect('members:member_list')

    return render(request, 'members/edit_member.html', {'member': member})

def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    # Delete member using PassKit SDK
    subprocess.run(
        ["python", "path/to/delete-member.py", member.passkit_member_id],
        capture_output=True, text=True
    )

    member.delete()
    return redirect('members:member_list')

