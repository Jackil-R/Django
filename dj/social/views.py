from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from social.models import Member, Profile, Message, Requests
from django.contrib.auth.hashers import PBKDF2PasswordHasher

appname = 'Facemagazine'

# decorator that tests whether user is logged in
def loggedin(f):
    def test(request):
        if 'username' in request.session:
            return f(request)
        else:
            template = loader.get_template('social/not-logged-in.html')
            context = RequestContext(request, {})
            return HttpResponse(template.render(context))
    return test

def index(request):
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
    		'appname': appname,
    	})
    return HttpResponse(template.render(context))

def signup(request):
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
    		'appname': appname,
    	})
    return HttpResponse(template.render(context))

def register(request):
    u = request.POST['user']
    p = request.POST['pass']
    hasher = PBKDF2PasswordHasher()
    p = hasher.encode(password=p, salt='salt', iterations=50000)
    user = Member(username=u, password=p,date=timezone.now())
    user.save()
    template = loader.get_template('social/user-registered.html')    
    context = RequestContext(request, {
        'appname': appname,
        'username' : u
        })
    return HttpResponse(template.render(context))

def login(request):

    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            return render(request, 'social/login.html', {
                'appname': appname,
                'name': "User Doesn't Exist!",
                'loggedin': False}
                )
	hasher = PBKDF2PasswordHasher()
   	p = hasher.encode(password=p, salt='salt', iterations=50000)
        if p == member.password:
            request.session['username'] = u;
            request.session['password'] = p;
            allRequests = Requests.objects.filter(requestTo=u)
            newRequests = allRequests.count()
            request.session['newRequests'] = newRequests
	        #return if the member get the username and password correct
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
		        'newRequests': request.session['newRequests'],
                'loggedin': True}
                )
        else:
            #return if the user has got the password wrong
            return render(request, 'social/login.html', {
                'appname': appname,
 		        'password': "Incorrect Password",
                'loggedin': False}
                )

@loggedin
#friends view 
def friends(request):
    username = request.session['username'] 
    member_obj = Member.objects.get(pk=username)
    allRequests = Requests.objects.all()

    if 'request' in request.GET:
        friend = request.GET['request']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.add(friend_obj)
        member_obj.save()
	#adding request
	if Requests.objects.filter(requestFrom=username, requestTo=friend).exists():
        	var = "e"
	else:
		requests_obj = Requests(requestFrom=username, requestTo=friend)
		requests_obj.save()
    
    # accept friend's request
    if 'accept' in request.GET:
        friend = request.GET['accept']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friends.add(friend_obj)
	

    	#followng remove
    	member_obj = Member.objects.get(pk=friend)
    	f = Member.objects.get(pk=username)
    	member_obj.following.remove(f)
        member_obj.save()
        
        #removing a request
        if Requests.objects.filter(requestFrom=friend, requestTo=username).exists():
            deleteRequest = Requests.objects.get(requestFrom=friend, requestTo=username)
            deleteRequest.delete()
        else:
            var = "e"


    # decline friend's request	
    if 'decline' in request.GET:
        friend = request.GET['decline']
        member_obj = Member.objects.get(pk=friend)
        friend_obj = Member.objects.get(pk=username)
        member_obj.following.remove(friend_obj)
        member_obj.save()

        #removing a request
        if Requests.objects.filter(requestFrom=friend, requestTo=username).exists():
            deleteRequest = Requests.objects.get(requestFrom=friend, requestTo=username)
            deleteRequest.delete()
        else:
            var = "e"

    #adding a friend
    if 'unfriend' in request.GET:
        friend = request.GET['unfriend']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friends.remove(friend_obj)
        member_obj.save()

    
    # list of friends recommendation
    friendOfFriend = Member.objects.filter(friends__friends__username=username).exclude(friends=username).exclude(pk=username).distinct()[:8]
    
    # gets current user
    member_obj = Member.objects.get(pk=username)
    # list of all Request
    allRequests = Requests.objects.all()
    # list of all Request where requestTo equals username
    pending = allRequests.filter(requestTo=username)
    # list of all Request
    allPending = Requests.objects.all()
    # list of all member
    friends = member_obj.friends.all()
    # list of all other members
    friendSuggestion = Member.objects.exclude(pk=username)[:3]
    # list of all following
    following = member_obj.following.all()

    pendingsToFrom = []
    for p in allPending:
	    pendingsToFrom.extend([p.requestFrom])

    # updating newRequest session
    allRequests = Requests.objects.filter(requestTo=username)
    request.session['newRequests'] = allRequests.count()
    # END updating


    return render(request, 'social/friends.html', {
        'appname': appname,
        'username': username,
        'members': members,
        'pending': pending,
        'friends': friends,
        'friendSuggestion': friendSuggestion,
    	'pendingsToFrom': pendingsToFrom,
    	'following': following,
    	'friendOfFriend': friendOfFriend,
    	'newRequests': request.session['newRequests'],
        'loggedin': True}
        )


@loggedin
def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
        raise Http404("Can't logout, you are not logged in")

def member(request, view_user):
    username = request.session['username']
    member = Member.objects.get(pk=view_user)

    if view_user == username:
        greeting = "Your"
    else:
        greeting = view_user + "'s"

    if member.profile:
        text = member.about
    else:
        text = ""

    # updating newRequest session
    allRequests = Requests.objects.filter(requestTo=username)
    request.session['newRequests'] = allRequests.count()
    # END updating
    return render(request, 'social/member.html', {
        'appname': appname,
        'username': username,
        'view_user': view_user,
        'greeting': greeting,
        'profile': text,
	    'newRequests': request.session['newRequests'],
        'loggedin': True}
        )

@loggedin
def members(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    allRequests = Requests.objects.all()
    
    # sending the friend request
    if 'request' in request.GET:
        friend = request.GET['request']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.add(friend_obj)
        member_obj.save()
    	#adding request
        #adding request
        if Requests.objects.filter(requestFrom=username, requestTo=friend).exists():
                var = "e"
        else:
            requests_obj = Requests(requestFrom=username, requestTo=friend)
            requests_obj.save()
    	


    # cancelling a friend request
    if 'cancel' in request.GET:
        friend = request.GET['cancel']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.remove(friend_obj)
        member_obj.save()
  
        #removing a request
        if Requests.objects.filter(requestFrom=username, requestTo=friend).exists():
            deleteRequest = Requests.objects.get(requestFrom=username, requestTo=friend)
            deleteRequest.delete() 
        else:
            var ="e"
    	

    #unfriend an existing friend
    if 'unfriend' in request.GET:
        friend = request.GET['unfriend']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friends.remove(friend_obj)
        member_obj.save()


    # view user profile
    if 'view' in request.GET:
        return member(request, request.GET['view'])
    else:
        pending = allRequests.filter(requestTo=username)
        # list of all other members
        members = Member.objects.exclude(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        friends = member_obj.friends.all()
        # list of all other members
        member_list = Member.objects.exclude(pk=username);
        # list of all requests
        request_list = Requests.objects.all()
        
        new_list = []

        # list of which user has request sent to the current user
        check = True 
        for m in member_list:
            check = True
            for r in request_list:
                if m.username == r.requestFrom:
                    if username == r.requestTo:
                        check = False
                else:
                    var = m
            if check:
                new_list.extend([m.username])    
        

        # updating newRequest session
        allRequests = Requests.objects.filter(requestTo=username)
        request.session['newRequests'] = allRequests.count()
        # END updating

        # render reponse
        return render(request, 'social/members.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'pending': pending,
            'friends': friends,
            'nonRequest':new_list,
	    'newRequests': request.session['newRequests'],
            'loggedin': True}
            )

@loggedin
def profile(request):
    u = request.session['username']
    member = Member.objects.get(pk=u)
    
    
    if 'text' in request.POST:
        text = request.POST['text']
    	email = request.POST['email']
    	gender = request.POST['gender_info']
    	city = request.POST['city']

        # store profile information in the member table
    	member.email = email
    	member.about = text
    	member.gender = gender
    	member.city = city
	
        if member.profile:
            member.profile.text = text
            member.profile.save()
        else:
            profile = Profile(text=text)
            profile.save()
            member.profile = profile
        member.save()
    else:
        if member.profile:
            text = member.profile.text
        else:
            text = ""

    # updating newRequest session
    allRequests = Requests.objects.filter(requestTo=u)
    request.session['newRequests'] = allRequests.count()
    # END updating
    return render(request, 'social/profile.html', {
        'appname': appname,
        'username': u,
        'text' : text,
	'city' : member.city,
	'about' : member.about,
	'email' : member.email,
	'newRequests': request.session['newRequests'],
        'loggedin': True}
        )

@loggedin
def messages(request):
    username = request.session['username']
    user = Member.objects.get(pk=username)
    # Whose message's are we viewing?
    if 'view' in request.GET:
        view = request.GET['view']
    else:
        view = username
    recip = Member.objects.get(pk=view)
    # If message was deleted
    if 'erase' in request.GET:
        msg_id = request.GET['erase']
        Message.objects.get(id=msg_id).delete()
    # If text was posted then save on DB
    if 'text' in request.POST:
        text = request.POST['text']
        pm = request.POST['pm'] == "0"
        message = Message(user=user,recip=recip,pm=pm,time=timezone.now(),text=text)
        message.save()
    messages = Message.objects.filter(recip=recip)
    profile_obj = Member.objects.get(pk=view).profile
    profile = profile_obj.text if profile_obj else ""

    # updating newRequest session
    allRequests = Requests.objects.filter(requestTo=username)
    request.session['newRequests'] = allRequests.count()
    # END updating
    return render(request, 'social/messages.html', {
        'appname': appname,
        'username': username,
        'profile': profile,
        'view': view,
        'messages': messages,
	'newRequests': request.session['newRequests'],
        'loggedin': True}
        )

def checkuser(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return render(request, "social/username_taken.html", RequestContext(request, locals()))
        else:
            return render(request, "social/username_free.html", RequestContext(request, locals()))

@loggedin
def search(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    allRequests = Requests.objects.all()
    
    # view user profile
    if 'view' in request.GET:
        return member(request, request.GET['view'])

    # updating newRequest session
    allRequests = Requests.objects.filter(requestTo=username)
    request.session['newRequests'] = allRequests.count()
    # END updating
    
    # String that user has searched
    if 'user' in request.POST:
        u = request.POST['user']
        
        # if the string is empty
        if not u:
            return render(request, 'social/search.html', {
                'found' : False,
                'appname': appname,
                'username' : username,
                'searchPhase' : "empty",
		        'newRequests': request.session['newRequests'],
                'loggedin': True}
            )
        # if the string is not empty and contains something
        else:

            # retur list and filter all other the member that contain the string and
            member = Member.objects.filter(username__contains=u,).exclude(pk=username)
            
            # if the member is empty
            if not member:
                return render(request, 'social/search.html', {
                    'found' : False,
                    'appname': appname,
                    'username' : username,
                    'searchPhase': u,
                    'member': member,
		    'newRequests': request.session['newRequests'],
                    'loggedin': True}
                )
            else:
            # if the membe is not empty and contain elements from the database
                return render(request, 'social/search.html', {
                    'found' : True,
                    'appname': appname,
                    'username' : username,
                    'searchPhase': u,
                    'member': member,
		    'newRequests': request.session['newRequests'],
                    'loggedin': True}
                )

    else:
        return render(request, 'social/search.html', {
                    #'found' : False,
                    'appname': appname,
                    'username' : username,
                    #'searchPhase': u,
                    #'member': member,
                    'newRequests': request.session['newRequests'],
                    'loggedin': True}
                )
