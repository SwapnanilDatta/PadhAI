from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
import os
from .llm_utils import get_groq_response
from django.http import HttpResponse
import csv
import io

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'chatbot/home.html')

from .models import ChatSession, ChatMessage, UploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def chat_list_view(request):
    sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chatbot/chat_list.html', {'sessions': sessions})

@login_required
def new_chat_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        chat = ChatSession.objects.create(user=request.user, title=title)
        return redirect('chat_detail', session_id=chat.id)
    return render(request, 'chatbot/new_chat.html')

@login_required
def chat_detail_view(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    if request.method == 'POST':
        msg = request.POST['message']
        ChatMessage.objects.create(session=session, role='user', content=msg)

        # ✅ Get LLM response
        ai_reply = get_groq_response(session)

        ChatMessage.objects.create(session=session, role='assistant', content=ai_reply)
        return redirect('chat_detail', session_id=session.id)

    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    return render(request, 'chatbot/chat_detail.html', {
        'session': session,
        'messages': messages
    })


from .vision_utils import gemini_vision_response

@login_required
def upload_file_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded = request.FILES['file']
        user_question = request.POST.get('question', '').strip()
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded.name, uploaded)
        filepath = fs.path(filename)

        ext = os.path.splitext(filename)[-1].lower()
        if ext in ['.png', '.jpg', '.jpeg']:
            # Create custom prompt based on user's question
            if user_question:
                prompt = f"User's question: {user_question}\n\nPlease analyze this image and answer the user's question. Provide a detailed, educational explanation like a tutor would."
                user_message = f"[Image Uploaded: {filename}]\nQuestion: {user_question}"
            else:
                prompt = "This is a student query image. Explain it like a tutor would, providing educational insights and explanations."
                user_message = f"[Image Uploaded: {filename}]"
            
            # Image → Gemini Vision
            ai_reply = gemini_vision_response(filepath, prompt=prompt)
        else:
            ai_reply = "Sorry, only image files (PNG, JPG, JPEG) are supported for analysis."
            user_message = f"[File Upload Failed: {filename}] - Unsupported format"

        # Always create a new chat session for each image upload
        chat_title = "Image Analysis Chat"
        if user_question:
            # Use first few words of question as title
            chat_title = f"Q: {user_question[:30]}..." if len(user_question) > 30 else f"Q: {user_question}"
        new_chat = ChatSession.objects.create(user=request.user, title=chat_title)
        
        ChatMessage.objects.create(session=new_chat, role='user', content=user_message)
        ChatMessage.objects.create(session=new_chat, role='assistant', content=ai_reply)

        # Clean up uploaded file after processing
        try:
            os.remove(filepath)
        except:
            pass

        return redirect('chat_detail', session_id=new_chat.id)

    return render(request, 'chatbot/upload.html')

@login_required
def download_notes(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    
    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Role', 'Content', 'Timestamp'])
    
    for msg in messages:
        writer.writerow([msg.role, msg.content, msg.timestamp])
    
    # Create the HTTP response with CSV content
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="chat_notes_{session_id}.csv"'
    
    return response
