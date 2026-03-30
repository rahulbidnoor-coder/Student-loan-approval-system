from django.shortcuts import render, redirect

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "1234":
            return redirect('loan')
        else:
            return render(request, 'loan_app/login.html', {'error': 'Invalid Login'})

    return render(request, 'loan_app/login.html')

# Loan Logic
def loan_view(request):
    result = None

    if request.method == "POST":
        name = request.POST.get("name")
        percentage = int(request.POST.get("percentage"))
        stream = request.POST.get("stream")
        required_amount = int(request.POST.get("amount"))

        # Step 1: Set max loan based on stream
        if stream in ["engineering", "medical"]:
            max_amount = 500000   # 5 lakh
        else:
            max_amount = 300000   # 3 lakh

        # Step 2: Calculate eligibility based on percentage
        if percentage >= 90:
            eligible_amount = max_amount
            status = "Loan Approved (100%)"
        elif percentage >= 85:
            eligible_amount = int(max_amount * 0.9)
            status = "Loan Approved (90%)"
        elif percentage >= 70:
            eligible_amount = int(max_amount * 0.75)
            status = "Loan Approved (75%)"
        else:
            return render(request, 'loan_app/loan.html', {
                'result': f"❌ Sorry {name}, you are not eligible for loan."
            })

        # Step 3: Compare requested vs eligible
        if required_amount <= eligible_amount:
            result = (
                f"✅ {name}, Loan Approved. "
                f"You are eligible for maximum ₹{eligible_amount}. "
                f"You requested ₹{required_amount} and it is approved."
            )
        else:
            result = (
                f"⚠️ {name}, Loan Approved. "
                f"You are eligible for maximum ₹{eligible_amount}. "
                f"But you requested ₹{required_amount}. "
                f"You can get only ₹{eligible_amount}."
            )
    return render(request, 'loan_app/loan.html', {'result': result})

def loan_view(request):
    result = None

    if request.method == "POST":
        name = request.POST.get("name")
        percentage = int(request.POST.get("percentage"))
        stream = request.POST.get("stream")
        amount = int(request.POST.get("amount"))

        # Max loan based on stream
        if stream in ["engineering", "medical"]:
            max_amount = 500000
        else:
            max_amount = 300000

        # Percentage logic
        if percentage >= 90:
            eligible = max_amount
        elif percentage >= 85:
            eligible = int(max_amount * 0.9)
        elif percentage >= 70:
            eligible = int(max_amount * 0.75)
        else:
            eligible = 0

        # 👉 STORE in session
        request.session['eligible_amount'] = eligible

        if eligible == 0:
            result = f"❌ {name}, You are not eligible for loan"
        else:
            result = f"✅ {name}, You are eligible for ₹{eligible}"

    return render(request, 'loan_app/loan.html', {'result': result})

def repayment_view(request):
    loan = request.session.get('eligible_amount', 0)

    return render(request, 'loan_app/repayment.html', {'loan': loan})