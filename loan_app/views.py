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
        stream = request.POST.get("stream")
        requested_amount = int(request.POST.get("amount"))

        # Max loan based on stream
        if stream in ["engineering", "medical"]:
            max_amount = 500000  # 5 lakh
        else:
            max_amount = 300000  # 3 lakh

        # Store eligible amount in session
        request.session['eligible_amount'] = max_amount

        # Prepare result message
        if requested_amount <= max_amount:
            result = (
                f"✅ {name}, You are eligible for ₹{requested_amount}."
            )
        else:
            result = (
                f"⚠️ {name}, You are eligible for maximum ₹{max_amount}. "
                f"You requested ₹{requested_amount}. You can get only ₹{max_amount}."
            )

    return render(request, 'loan_app/loan.html', {'result': result})


# Repayment Logic
def repayment_view(request):
    loan = request.session.get('eligible_amount', 0)
    return render(request, 'loan_app/repayment.html', {'loan': loan})