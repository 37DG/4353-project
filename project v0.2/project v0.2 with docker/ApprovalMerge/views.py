from django.shortcuts import render, redirect
from .models import GraduateStudentPetition as Grad_petition
from UserManagement.models import User
from django.conf import settings

import os
import subprocess
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now

def full_name_splitter(full_name):
    name_fragments = full_name.split(' ')

    if len(name_fragments) == 3:
        first_name = name_fragments[0]
        middle_name = name_fragments[1]
        last_name = name_fragments[2]
    else:
        first_name = name_fragments[0]
        middle_name = ""
        last_name = name_fragments[1]


    return [first_name, middle_name, last_name]

def generate_grad_latex(data, sig_path):
    """Generates LaTeX content from a dictionary of data."""
    if "name" in data:
        first_name, middle_name, last_name = full_name_splitter(data.get("name"))
    else:
        first_name = data.get("first_name")
        middle_name = data.get("middle_name")
        last_name = data.get("last_name")

    latex_content = f"""
    \\documentclass[a4paper,12pt]{{article}}
    \\usepackage{{geometry}}
    \\geometry{{top=1in, bottom=1in, left=1in, right=1in}}
    \\usepackage{{longtable}}
    \\usepackage{{amsmath}}
    \\usepackage{{graphicx}}

    \\title{{Graduate Student Petition Form}}
    \\author{{University of Houston}}
    \\date{{}}

    \\begin{{document}}

    \\maketitle

    \\section*{{Student Information}}
    \\begin{{tabbing}}
    First Name: \\hspace{{3cm}} \\= \\underline{{\\hspace{{5cm}} {first_name}}} \\\\
    Middle Name: \\> \\underline{{\\hspace{{5cm}} {middle_name}}} \\\\
    Last Name: \\> \\underline{{\\hspace{{5cm}} {last_name}}} \\\\
    UH ID: \\> \\underline{{\\hspace{{5cm}} {data.get("uh_id", "")}}} \\\\
    Contact Phone: \\> \\underline{{\\hspace{{5cm}} {data.get("contact_phone", "")}}} \\\\
    \\end{{tabbing}}

    \\section*{{Current Student Information}}
    \\begin{{tabbing}}
    Program: \\hspace{{3cm}} \\= \\underline{{\\hspace{{5cm}} {data.get("program", "")}}} \\\\
    Career: \\> \\underline{{\\hspace{{5cm}} {data.get("career", "")}}} \\\\
    \\end{{tabbing}}

    \\section*{{Petition Effective}}
    \\begin{{tabbing}}
    Effective Term: \\hspace{{2cm}} \\= \\underline{{\\hspace{{5cm}} {data.get("effective_term", "")}}} \\\\
    Year: \\> \\underline{{\\hspace{{5cm}} {data.get("year", "")}}} \\\\
    \\end{{tabbing}}

    \\section*{{Purpose of Petition}}
    \\begin{{enumerate}}
        \\item Update programs status/action (term activate, discontinue, etc) \\hfill [{ "yes" if data.get("update_program") else "no" }]
        \\item Admissions status change (e.g. conditional to unconditional) \\hfill [{ "yes" if data.get("admissions_status") else "no" }]
        \\item Add new concurrent degree or certificate objective (career/program/plan) \\hfill [{ "yes" if data.get("add_new_concurrent") else "no" }]
        \\item Change current degree objective (program/plan) \\hfill [{ "yes" if data.get("change_degree_objective") else "no" }]
        \\item Degree requirement exception or approved course substitution \\hfill [{ "yes" if data.get("degree_requirement_exception") else "no" }]
        \\item Leave of Absence (include specific term) \\hfill [{ "yes" if data.get("leave_of_absence") else "no" }]
        \\item Reinstatement to discontinued Career (provide explanation) \\hfill [{ "yes" if data.get("reinstatement") else "no" }]
        \\item Request to apply to graduate after the late filing period deadline \\hfill [{ "yes" if data.get("late_filing_graduation") else "no" }]
        \\item Transfer Credit \\hfill [{ "yes" if data.get("transfer_credit") else "no" }]
        \\item Change Admit Term \\hfill [{ "yes" if data.get("change_admit_term") else "no" }]
        \\item Early Submission of Thesis/Dissertation \\hfill [{ "yes" if data.get("early_submission") else "no" }]
        \\item Other (explain below) \\hfill [{ "yes" if data.get("other") else "no" }]
    \\end{{enumerate}}

    \\section*{{Explanation of Request}}
    \\begin{{flushleft}}
    \\underline{{\\hspace{{15cm}} {data.get("explanation", "")}}} \\\\
    \\end{{flushleft}}

    \\section*{{Signature Section}}
    Student Signature: \\\\
    \\includegraphics[width=7cm]{{{sig_path}}}

    \\end{{document}}
    """
    return latex_content

# Display Grad Petition form
def GradPetition(request):
    first_name, middle_name, last_name = full_name_splitter(User.objects.get(email=request.session.get("user_email")).name)
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    try:
        record = Grad_petition.objects.get(email=user['email'])

        if record.status == 'draft' or record.status =='returned':
            return render(request, 'GraduateStudentPetition.html', {"user": user, "form_url": settings.MEDIA_URL, "record": record})
        elif record.status == 'pending':
            return render(request, 'WaitForPending.html', {"user": user})
        elif record.status == 'approved':
            pdf_filename = f"{record.name.replace(' ', '_')}_GradPetition_{record.date.strftime('%Y-%m-%d_%H_%M_%S')}.pdf"
            return render(request, 'GradPetitionApproved.html', {"user": user, "pdf_filename": pdf_filename})
    except Grad_petition.DoesNotExist:
        return render(request, 'GraduateStudentPetition.html', {"user": user, "form_url": settings.MEDIA_URL})

# Send Grad Petition form to DB
def submitGradPetition(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        return_date = request.POST.get("return_date")
        signature = request.FILES.get("signature")

        print(signature)

        if (middle_name):
            name = first_name + ' ' + middle_name + ' ' + last_name
        else:
            name = first_name + ' ' + last_name

        newName = name.replace(" ", "_")
        form = 'GradPetition'
        file_path = ""
        signature_path = ""
        if signature:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            file_extension = signature.name.split('.')[-1]
            signature_filename = f"{newName}_{form}.{file_extension}"
            file_path = os.path.join(settings.MEDIA_ROOT, signature_filename)

            # Delete the old file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)

            filename = fs.save(signature_filename, signature)
            signature_path = file_path.replace('\\','/')

        date = now()

        Grad_petition.objects.update_or_create(
            email=email,
            defaults={
                'name': name,
                'uh_id': request.POST.get("uh_id"),
                'contact_phone': request.POST.get("contact_phone"),
                'program': request.POST.get("program"),
                'career': request.POST.get("career"),
                'effective_term': request.POST.get("effective_term"),
                'year': request.POST.get("year"),
                'update_program': True if request.POST.get("update_program") == 'on' else False,
                'admissions_status': True if request.POST.get("admissions_status") == 'on' else False,
                'add_new_concurrent': True if request.POST.get("add_new_concurrent") == 'on' else False,
                'change_degree_objective': True if request.POST.get("change_degree_objective") == 'on' else False,
                'degree_requirement_exception': True if request.POST.get("degree_requirement_exception") == 'on' else False,
                'leave_of_absence': True if request.POST.get("leave_of_absence") == 'on' else False,
                'leave_documentation': request.POST.get("leave_documentation"),
                'reinstatement': True if request.POST.get("reinstatement") == 'on' else False,
                'late_filing_graduation': True if request.POST.get("late_filing_graduation") == 'on' else False,
                'transfer_credit': True if request.POST.get("transfer_credit") == 'on' else False,
                'institution_name': request.POST.get("institution_name"),
                'city_state_zip': request.POST.get("city_state_zip"),
                'hours_transferred': int(request.POST.get("hours_transferred")) if request.POST.get("hours_transferred") != '' else 0,
                'transfer_credits': int(request.POST.get("transfer_credits")) if request.POST.get("transfer_credits") != '' else 0,
                'catalog_number': request.POST.get("catalog_number"),
                'semester_taken': request.POST.get("semester_taken"),
                'change_admit_term': True if request.POST.get("change_admit_term") == 'on' else False,
                'early_submission': True if request.POST.get("early_submission") == 'on' else False,
                'other': True if request.POST.get("other") == 'on' else False,
                'other_explanation': request.POST.get("other_explanation"),
                'explanation': request.POST.get("explanation"),
                'date': date,
                'status': 'pending'
            }
        )

        if return_date:
            record = Grad_petition.objects.get(email=email)
            record.return_date = return_date
            record.save()

        latex_path = os.path.abspath("Latex/")
        tex_name = f"{newName}_{form}_{date.strftime('%Y-%m-%d_%H_%M_%S')}.tex"
        file_path = os.path.join(latex_path, tex_name)

        filled_latex = generate_grad_latex(request.POST, signature_path)

        with open(file_path, "w") as file:
            file.write(filled_latex)

        process = subprocess.run(["make", "buildGradPetition", f"TEX_FILE={tex_name}"], cwd=latex_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            print("Make failed with error:", process.stderr.decode())
            return redirect('/')

        return render(request, 'WaitForPending.html', {"user": {"name": name}})

def finishGradPetition(request):
    record = Grad_petition.objects.get(email=request.session.get("user_email"))
    record.status = "draft"
    record.note = ""
    record.save()

    return redirect('/approvalsystem')