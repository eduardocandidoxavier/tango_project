from datetime import datetime

def visitor_cookie_handler(request):
    visits = int(return_cookie_value(request, 'visits', '1'))
    last_time_visit = return_cookie_value(request, 'last_time_visit', str(datetime.now()))
    last_time = datetime.strptime(last_time_visit[:-7],'%Y-%m-%d %H:%M:%S')
    if((datetime.now() - last_time).seconds > 1):
        visits = visits + 1
        last_time_visit = str(datetime.now())
    request.session['last_time_visit'] = last_time_visit
    request.session['visits'] = str(visits)

def return_cookie_value(request, cookie, default=None):
    val = request.session.get(cookie)
    if not val:
        val = default
    return val

