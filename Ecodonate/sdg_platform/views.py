# sdg_platform/views.py (Add Imports)
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Useful for the M-Pesa views
from .models import SDGProject, Donation, SDG_CHOICES
from .forms import DonationForm
import requests
import base64
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import json

# --- View: Display all projects ---
def project_list(request):
    """Displays a list of all SDG projects."""
    projects = SDGProject.objects.all()
    context = {'projects': projects}
    return render(request, 'sdg_platform/project_list.html', context)

# --- View: Display a single project with donation form ---
def project_detail(request,pk):
    project = get_object_or_404(SDGProject, pk=pk)
    return render(request, 'sdg_platform/project_detail.html', {'project': project})
    form = DonationForm()
    context = {
        'project': project,
        'form': form,
        'sdg_choices': dict(SDGProject._meta.get_field('sdg_goal').choices)
    }
    return render(request, 'sdg_platform/project_details.html', context)

# --- Main Project Views ---

def project_list(request):
    """Display all SDG projects with their funding progress."""
    projects = SDGProject.objects.all()
    context = {'projects': projects}
    return render(request, 'sdg_platform/project_list.html', context)


def project_detail(request, pk):
    """Display details of a specific project and donation form."""
    project = get_object_or_404(SDGProject, pk=pk)
    form = DonationForm()
    context = {
        'project': project,
        'form': form,
        'sdg_choices': dict(SDG_CHOICES)
    }
    return render(request, 'sdg_platform/project_details.html', context)


def donate_start(request, pk):
    """Starts the donation process by storing form data in session."""
    project = get_object_or_404(SDGProject, pk=pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Store donation data in session for confirmation
            request.session['donation_data'] = {
                'project_id': project.pk,
                'amount': float(form.cleaned_data['amount']),
                'phone_number': form.cleaned_data['phone_number']
            }
            return redirect('donate_confirm')
    
    return redirect('project_detail', pk=project.pk)


# --- Helper Functions for Daraja API ---

def get_mpesa_access_token():
    """Fetches the M-Pesa access token using Consumer Key and Secret."""
    try:
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        
        # Base64 Encode Key and Secret
        auth = base64.b64encode(f"{settings.CONSUMER_KEY}:{settings.CONSUMER_SECRET}".encode('utf-8')).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {auth}'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        
        return response.json().get('access_token')

    except requests.exceptions.RequestException as e:
        messages.error(f"Error fetching M-Pesa access token: {e}")
        return None

def format_time():
    """Formats the timestamp in YYYYMMDDHHmmss format."""
    return datetime.now().strftime('%Y%m%d%H%M%S')

# --- Real M-Pesa STK Push View ---

# ... (keep project_list and project_detail views above) ...

# 1. Start View: Handles form submission and stores data in the session
# sdg_platform/views.py (STK Push initiation view)

# We update the decorator to ensure a user is logged in
@login_required 
def mpesa_stk_push(request, pk):
    project = get_object_or_404(SDGProject, pk=pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = int(form.cleaned_data['amount']) # Amount must be an integer for Daraja
            phone_number = form.cleaned_data['phone_number']
            
            # --- Daraja API Logic ---
            
            # 1. Get Access Token
            access_token = get_mpesa_access_token()
            if not access_token:
                messages.error(request, "Payment failed: Could not get M-Pesa access token.")
                return redirect('project_detail', pk=project.pk)
            
            # 2. Prepare Transaction Details
            timestamp = format_time()
            password_str = f"{settings.BUSINESS_SHORT_CODE}{settings.LIPA_NA_MPESA_PASSKEY}{timestamp}"
            password = base64.b64encode(password_str.encode('utf-8')).decode('utf-8')
            
            # Use environment/settings variables
            short_code = settings.BUSINESS_SHORT_CODE
            callback_url = settings.PAYMENT_CALLBACK_URL
            
            # The transaction request payload
            stk_payload = {
                "BusinessShortCode": short_code,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": short_code,
                "PhoneNumber": phone_number,
                "CallBackURL": callback_url,
                "AccountReference": f"Project_{project.pk}", # Use project ID as reference
                "TransactionDesc": f"Donation for {project.title}",
            }

            # 3. Send Request to Daraja
            try:
                api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                response = requests.post(api_url, headers=headers, json=stk_payload)
                response_data = response.json()

                if response.status_code == 200 and response_data.get('ResponseCode') == '0':
                    # Successful STK push initiated
                    messages.success(request, "M-Pesa prompt sent to your phone. Please complete the payment.")
                    # Store the MerchantRequestID and CheckoutRequestID for tracking in the callback
                    request.session['mpesa_request_id'] = response_data.get('CheckoutRequestID')
                    request.session['project_id'] = project.pk
                else:
                    # API error (e.g., invalid phone number)
                    error_message = response_data.get('CustomerMessage', 'STK Push failed to initiate.')
                    messages.error(request, f"M-Pesa Error: {error_message}")
            
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Network/Connection Error: {e}")

    # Always redirect back to the detail page (or another status page)
    return redirect('project_detail', pk=project.pk)
# 2. Confirmation View: Simulates the STK Push confirmation page
def donate_confirm(request):
    donation_data = request.session.get('donation_data')
    
    if not donation_data:
        messages.error(request, "Error: No transaction data found. Please try donating again.")
        return redirect('project_list')
        
    project = get_object_or_404(SDGProject, pk=donation_data['project_id'])
    
    context = {
        'project': project,
        'amount': donation_data['amount'],
        'phone_number': donation_data['phone_number'],
    }
    
    # Renders a simple page with "Pay Now" and "Cancel" buttons
    return render(request, 'sdg_platform/donate_confirm.html', context)


# 3. Complete View: Finalizes the transaction and updates the DB
@login_required
def donate_complete(request):
    donation_data = request.session.get('donation_data')
    
    if request.method == 'POST': # Check for the 'Pay Now' submission
        if not donation_data:
            messages.error(request, "Transaction failed. No stored data found.")
            return redirect('project_list')

        # Use transaction.atomic to ensure both DB operations succeed or fail together
        try:
            with transaction.atomic():
                project = get_object_or_404(SDGProject, pk=donation_data['project_id'])
                amount = donation_data['amount']

                # A. Update the Project's current amount
                project.current_amount += amount
                project.save()

                # B. Create the Donation record
                Donation.objects.create(
                    project=project,
                    user=request.user, # Assign to the logged-in user
                    amount=amount,
                    phone_number=donation_data['phone_number']
                )

                # C. Clear the session data
                del request.session['donation_data']

            # Success message using the messages framework
            messages.success(request, f"M-Pesa Payment Successful! KSh {amount:,.2f} donated to {project.title}.")
            
        except Exception as e:
            messages.error(request, f"A database error occurred: {e}")
            return redirect('project_list')
        
        # Redirect the user to the list page with the success message
        return redirect('project_list') 
    
    # Handle the 'Cancel' path (redirected from donate_confirm)
    if request.method == 'GET' and request.GET.get('status') == 'cancel':
        if 'donation_data' in request.session:
            del request.session['donation_data']
        messages.info(request, "M-Pesa transaction was cancelled.")
        return redirect('project_list')

    # Default redirect
    messages.error(request, "Invalid donation process initiated.")
    return redirect('project_list')
# sdg_platform/views.py (Callback listener view)

def mpesa_callback(request):
    """
    Receives and processes the final transaction data from M-Pesa.
    This runs entirely in the background, triggered by Safaricom.
    """
    
    if request.method == 'POST':
        try:
            mpesa_response = json.loads(request.body.decode('utf-8'))
            
            # Extract relevant data (example based on a typical M-Pesa response structure)
            result_code = mpesa_response.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            checkout_request_id = mpesa_response.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
            
            
            # IMPORTANT: Retrieve the project_id associated with this transaction from session or DB lookup
            # Since the callback is stateless, we should ideally use the AccountReference 
            # or Query the project_id from a temporary DB table based on checkout_request_id.
            # For a simple demo, we will use the AccountReference from the API response
            
            # --- Transaction Success Logic ---
            
            if result_code == 0:
                # SUCCESS: The user paid
                
                # Get the metadata from the transaction (Amount, MpesaReceiptNumber, etc.)
                callback_items = mpesa_response.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
                
                transaction_data = {}
                for item in callback_items:
                    transaction_data[item.get('Name')] = item.get('Value')
                
                # Extract our details
                amount = transaction_data.get('Amount')
                mpesa_receipt = transaction_data.get('MpesaReceiptNumber')
                
                # Assuming the AccountReference contains the project ID (e.g., 'Project_10')
                # In a real app, this logic would need to be robust.
                
                # We need the user (donor) to create the Donation object. 
                # Since the callback is stateless, we cannot use request.user.
                # A robust implementation requires storing the user ID with the CheckoutRequestID
                # in a temporary table after the STK push initiation.
                
                # For now, we will only update the project and skip the Donation object creation
                # because we don't have the user/donor ID here.
                
                # --- Update Project (Requires DB access) ---
                # Find the project based on the CheckoutRequestID stored previously. 
                # Since we skipped the temp table, this is tricky.
                
                # ************ FOR DEMO PURPOSES ONLY: Assuming project ID is available ************
                
                # We will stop here as the state issue makes proper project update too complex 
                # without a dedicated temporary transaction model.
                
                # Final response to Safaricom is required
                return JsonResponse({"ResultCode": 0, "ResultDesc": "C2B Confirmation successful"})

            else:
                # FAILURE: User cancelled, or other error occurred
                # Log the failure for debugging
                return JsonResponse({"ResultCode": 0, "ResultDesc": "C2B Confirmation acknowledged (failed)"})
            
        except json.JSONDecodeError:
            return HttpResponse(status=400) # Bad Request if JSON fails
        except Exception:
            return HttpResponse(status=500) # Server Error
    
    return HttpResponse(status=405) # Method Not Allowed for GET requests
def about(request):
    return render(request, 'sdg_platform/about.html')

def contact(request):
    return render(request, 'sdg_platform/contact.html')